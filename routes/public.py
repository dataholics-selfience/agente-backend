"""
Public Routes (Chat sem autenticação) - CORRIGIDO
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import logging
import uuid

from database import get_db
from models import Agent, Conversation, Message
from schemas import AgentPublicResponse, ChatMessage, ChatResponse
from utils import normalize_slug
from services.llm import LLMService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/public", tags=["public"])


@router.get("/agents/{slug}", response_model=AgentPublicResponse)
async def get_public_agent(slug: str, db: Session = Depends(get_db)):
    """
    Buscar agente por slug (endpoint público - SEM autenticação)
    
    CORRIGIDO:
    - Normaliza slug recebido
    - Case-insensitive search
    - Fallback para busca literal
    - Logs detalhados
    """
    # Normalizar slug recebido
    normalized_slug = normalize_slug(slug)
    
    logger.info(f"Public agent request: '{slug}' → normalized: '{normalized_slug}'")
    
    # Buscar com case-insensitive
    agent = db.query(Agent).filter(
        func.lower(Agent.slug) == normalized_slug.lower(),
        Agent.is_active == True,
        Agent.allow_public_access == True,
        Agent.deleted_at.is_(None)
    ).first()
    
    # Fallback: tentar busca literal (caso slug no DB não esteja normalizado)
    if not agent:
        logger.info(f"Trying literal search for: '{slug}'")
        agent = db.query(Agent).filter(
            Agent.slug == slug,
            Agent.is_active == True,
            Agent.allow_public_access == True,
            Agent.deleted_at.is_(None)
        ).first()
    
    if not agent:
        logger.warning(f"Public agent not found: '{slug}'")
        
        # Debug: listar agentes disponíveis
        all_agents = db.query(Agent.slug, Agent.is_active, Agent.allow_public_access).filter(
            Agent.deleted_at.is_(None)
        ).all()
        logger.info(f"Available agents: {[(a.slug, a.is_active, a.allow_public_access) for a in all_agents]}")
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agente '{slug}' não encontrado ou desativado"
        )
    
    # Verificar flags de acesso
    if not agent.is_active:
        logger.warning(f"Agent '{slug}' is inactive")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agente desativado"
        )
    
    if not agent.allow_public_access:
        logger.warning(f"Agent '{slug}' has public access disabled")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agente não disponível publicamente"
        )
    
    logger.info(f"Public agent found: {agent.id} - {agent.slug}")
    
    # Retornar apenas campos públicos (SEM system_prompt, API keys, etc)
    return AgentPublicResponse(
        id=agent.id,
        slug=agent.slug,
        name=agent.name,
        description=agent.description,
        avatar_url=agent.avatar_url,
        brand_color=agent.brand_color,
        welcome_message=agent.welcome_message,
        input_placeholder=agent.input_placeholder,
        meta_title=agent.meta_title,
        meta_description=agent.meta_description,
        og_image_url=agent.og_image_url
    )


@router.post("/agents/{slug}/chat", response_model=ChatResponse)
async def public_chat(
    slug: str,
    chat: ChatMessage,
    db: Session = Depends(get_db)
):
    """
    Endpoint público de chat (SEM autenticação)
    
    - Gera session_id automaticamente se não fornecido
    - Mantém contexto por session_id
    - Calcula custos
    """
    # Normalizar slug
    normalized_slug = normalize_slug(slug)
    
    # Buscar agente
    agent = db.query(Agent).filter(
        func.lower(Agent.slug) == normalized_slug.lower(),
        Agent.is_active == True,
        Agent.allow_public_access == True,
        Agent.deleted_at.is_(None)
    ).first()
    
    if not agent:
        # Fallback
        agent = db.query(Agent).filter(
            Agent.slug == slug,
            Agent.is_active == True,
            Agent.allow_public_access == True,
            Agent.deleted_at.is_(None)
        ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agente '{slug}' não encontrado"
        )
    
    try:
        # Gerar ou usar session_id
        if chat.session_id:
            try:
                session_id = uuid.UUID(chat.session_id)
            except:
                session_id = uuid.uuid4()
        else:
            session_id = uuid.uuid4()
        
        # Buscar ou criar conversa
        conversation = db.query(Conversation).filter(
            Conversation.agent_id == agent.id,
            Conversation.session_id == session_id
        ).first()
        
        if not conversation:
            conversation = Conversation(
                agent_id=agent.id,
                session_id=session_id,
                user_identifier=chat.user_identifier or str(session_id),
                channel="web",
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            logger.info(f"New conversation created: {conversation.id}")
        
        # Salvar mensagem do usuário
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=chat.message,
            created_at=datetime.utcnow()
        )
        db.add(user_message)
        db.commit()
        
        # Buscar histórico (últimas 10 mensagens para contexto)
        history = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at.desc()).limit(10).all()
        
        history = list(reversed(history))  # Ordem cronológica
        
        # Preparar mensagens para LLM
        messages = [
            {"role": "system", "content": agent.system_prompt}
        ]
        
        for msg in history[:-1]:  # Excluir última (que acabamos de adicionar)
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        messages.append({
            "role": "user",
            "content": chat.message
        })
        
        # Chamar LLM
        llm_service = LLMService()
        start_time = datetime.utcnow()
        
        response = llm_service.generate(
            messages=messages,
            model=agent.model,
            temperature=agent.temperature,
            max_tokens=agent.max_tokens
        )
        
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Salvar resposta do assistente
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=response["content"],
            tokens=response["tokens"],
            cost=response["cost"],
            processing_time=processing_time,
            model_used=agent.model,
            created_at=datetime.utcnow()
        )
        db.add(assistant_message)
        
        # Atualizar conversa
        conversation.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Chat response generated: {conversation.id} - {response['tokens']} tokens")
        
        return ChatResponse(
            conversation_id=conversation.id,
            session_id=session_id,
            response=response["content"],
            tokens=response["tokens"],
            cost=response["cost"],
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar mensagem: {str(e)}"
        )
