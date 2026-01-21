"""Public API - Chat sem autenticação"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import uuid

from app.core.database import get_db
from app.models import Agent
from app.services.conversation_service import ConversationService

router = APIRouter()

class PublicAgentResponse(BaseModel):
    """Resposta pública (SEM system_prompt e dados sensíveis)"""
    slug: str
    name: str
    description: Optional[str]
    avatar_url: Optional[str]
    brand_color: str
    welcome_message: str
    input_placeholder: str
    meta_title: Optional[str]
    meta_description: Optional[str]
    og_image_url: Optional[str]

class PublicChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class PublicChatResponse(BaseModel):
    conversation_id: str
    session_id: str
    response: str
    tokens: int
    cost: float
    processing_time: float

@router.get("/agents/{slug}", response_model=PublicAgentResponse)
async def get_public_agent(slug: str, db: Session = Depends(get_db)):
    """
    Retorna configuração pública do agente (SEM system_prompt)
    
    Segurança:
    - NÃO retorna system_prompt
    - NÃO retorna parâmetros internos
    - Apenas dados necessários para UI
    """
    agent = db.query(Agent).filter(Agent.slug == slug).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agente não encontrado")
    
    if not agent.is_active or not agent.allow_public_access:
        raise HTTPException(status_code=404, detail="Agente não disponível")
    
    return PublicAgentResponse(
        slug=agent.slug,
        name=agent.name,
        description=agent.description,
        avatar_url=agent.avatar_url,
        brand_color=agent.brand_color,
        welcome_message=agent.welcome_message,
        input_placeholder=agent.input_placeholder,
        meta_title=agent.meta_title or f"Chat com {agent.name}",
        meta_description=agent.meta_description or f"Converse com {agent.name}",
        og_image_url=agent.og_image_url
    )

@router.post("/agents/{slug}/chat", response_model=PublicChatResponse)
async def public_chat(
    slug: str,
    request: PublicChatRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint público de chat (SEM autenticação)
    
    Args:
        slug: Identificador único do agente
        message: Mensagem do usuário
        session_id: UUID gerado no frontend para manter contexto
    
    Returns:
        Resposta do agente + metadados
    """
    # Busca agente
    agent = db.query(Agent).filter(Agent.slug == slug).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agente não encontrado")
    
    if not agent.is_active:
        raise HTTPException(status_code=403, detail="Agente não está ativo")
    
    # Gera session_id se não existir
    session_id = request.session_id or str(uuid.uuid4())
    
    # Usa session_id como user_identifier para chat público
    user_identifier = f"public_{session_id}"
    
    try:
        result = await ConversationService.process_message(
            db=db,
            agent_id=agent.id,
            user_identifier=user_identifier,
            user_message=request.message,
            channel="web"
        )
        
        return PublicChatResponse(
            conversation_id=result["conversation_id"],
            session_id=session_id,
            response=result["response"],
            tokens=result["tokens"],
            cost=result["cost"],
            processing_time=result["processing_time"]
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar mensagem: {str(e)}")

@router.get("/agents/{slug}/history/{session_id}")
async def get_public_conversation_history(
    slug: str,
    session_id: str,
    db: Session = Depends(get_db)
):
    """Retorna histórico da conversa pública"""
    agent = db.query(Agent).filter(Agent.slug == slug).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agente não encontrado")
    
    user_identifier = f"public_{session_id}"
    
    from app.models import Conversation, Message
    
    conversation = db.query(Conversation).filter(
        Conversation.agent_id == agent.id,
        Conversation.user_identifier == user_identifier
    ).first()
    
    if not conversation:
        return {"messages": []}
    
    messages = ConversationService.get_conversation_history(
        db, conversation.id, limit=50
    )
    
    return {
        "conversation_id": str(conversation.id),
        "messages": [
            {
                "role": msg.role.value,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]
    }
