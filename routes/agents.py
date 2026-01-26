"""
Agent CRUD Routes (CORRIGIDO)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
import logging

from database import get_db
from models import Agent
from schemas import AgentCreate, AgentUpdate, AgentResponse
from utils import normalize_slug, generate_unique_slug, validate_slug
from auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent: AgentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Criar novo agente
    
    - Gera slug automaticamente se não fornecido
    - Valida unicidade do slug
    - Normaliza slug (remove espaços, acentos, etc)
    """
    try:
        # Gerar ou normalizar slug
        if agent.slug:
            slug = normalize_slug(agent.slug)
        else:
            slug = normalize_slug(agent.name)
        
        # Validar slug
        is_valid, error_msg = validate_slug(slug)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        
        # Verificar unicidade
        existing = db.query(Agent).filter(Agent.slug == slug).first()
        if existing:
            # Gerar slug único com sufixo
            all_slugs = [a.slug for a in db.query(Agent.slug).all()]
            slug = generate_unique_slug(slug, all_slugs)
            logger.info(f"Slug collision, generated unique: {slug}")
        
        # Criar agente
        new_agent = Agent(
            name=agent.name,
            slug=slug,
            description=agent.description,
            avatar_url=agent.avatar_url,
            system_prompt=agent.system_prompt,
            model=agent.model,
            temperature=agent.temperature,
            max_tokens=agent.max_tokens,
            top_p=agent.top_p,
            frequency_penalty=agent.frequency_penalty,
            presence_penalty=agent.presence_penalty,
            rag_enabled=agent.rag_enabled,
            function_calling_enabled=agent.function_calling_enabled,
            whatsapp_enabled=agent.whatsapp_enabled,
            whatsapp_number=agent.whatsapp_number,
            email_enabled=agent.email_enabled,
            email_address=agent.email_address,
            web_enabled=agent.web_enabled,
            is_active=agent.is_active,
            allow_public_access=agent.allow_public_access,
            brand_color=agent.brand_color,
            welcome_message=agent.welcome_message,
            input_placeholder=agent.input_placeholder,
            meta_title=agent.meta_title,
            meta_description=agent.meta_description,
            og_image_url=agent.og_image_url,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(new_agent)
        db.commit()
        db.refresh(new_agent)
        
        logger.info(f"Agent created: {new_agent.id} - {new_agent.slug}")
        
        # Adicionar URL pública na resposta
        response_dict = {
            **{k: v for k, v in new_agent.__dict__.items() if not k.startswith('_')},
            "public_url": f"https://agentes.genoibot.com/{new_agent.slug}"
        }
        
        return response_dict
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create agent: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar agente: {str(e)}"
        )


@router.get("", response_model=List[AgentResponse])
async def list_agents(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Listar todos os agentes (apenas não-deletados)
    """
    agents = db.query(Agent).filter(
        Agent.deleted_at.is_(None)  # Filtrar deletados
    ).order_by(Agent.created_at.desc()).all()
    
    # Adicionar URL pública em cada agente
    response = []
    for agent in agents:
        agent_dict = {
            **{k: v for k, v in agent.__dict__.items() if not k.startswith('_')},
            "public_url": f"https://agentes.genoibot.com/{agent.slug}"
        }
        response.append(agent_dict)
    
    return response


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Buscar agente por ID
    """
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.deleted_at.is_(None)
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agente não encontrado"
        )
    
    agent_dict = {
        **{k: v for k, v in agent.__dict__.items() if not k.startswith('_')},
        "public_url": f"https://agentes.genoibot.com/{agent.slug}"
    }
    
    return agent_dict


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent: AgentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Atualizar agente
    
    CORRIGIDO:
    - Normaliza slug automaticamente
    - Valida unicidade
    - Atualiza apenas campos fornecidos
    """
    existing = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.deleted_at.is_(None)
    ).first()
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agente não encontrado"
        )
    
    try:
        # Atualizar campos
        if agent.name is not None:
            existing.name = agent.name
        
        # Slug: SEMPRE normalizar se fornecido
        if agent.slug is not None:
            new_slug = normalize_slug(agent.slug)
            
            # Validar
            is_valid, error_msg = validate_slug(new_slug)
            if not is_valid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_msg
                )
            
            # Verificar unicidade (se mudou)
            if new_slug != existing.slug:
                duplicate = db.query(Agent).filter(
                    Agent.slug == new_slug,
                    Agent.id != agent_id,
                    Agent.deleted_at.is_(None)
                ).first()
                
                if duplicate:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Slug '{new_slug}' já está em uso"
                    )
                
                logger.info(f"Agent {agent_id} slug updated: {existing.slug} → {new_slug}")
                existing.slug = new_slug
        
        # Outros campos
        if agent.description is not None:
            existing.description = agent.description
        
        if agent.avatar_url is not None:
            existing.avatar_url = agent.avatar_url
        
        if agent.system_prompt is not None:
            existing.system_prompt = agent.system_prompt
        
        if agent.model is not None:
            existing.model = agent.model
        
        if agent.temperature is not None:
            existing.temperature = agent.temperature
        
        if agent.max_tokens is not None:
            existing.max_tokens = agent.max_tokens
        
        if agent.top_p is not None:
            existing.top_p = agent.top_p
        
        if agent.frequency_penalty is not None:
            existing.frequency_penalty = agent.frequency_penalty
        
        if agent.presence_penalty is not None:
            existing.presence_penalty = agent.presence_penalty
        
        if agent.rag_enabled is not None:
            existing.rag_enabled = agent.rag_enabled
        
        if agent.function_calling_enabled is not None:
            existing.function_calling_enabled = agent.function_calling_enabled
        
        if agent.whatsapp_enabled is not None:
            existing.whatsapp_enabled = agent.whatsapp_enabled
        
        if agent.whatsapp_number is not None:
            existing.whatsapp_number = agent.whatsapp_number
        
        if agent.email_enabled is not None:
            existing.email_enabled = agent.email_enabled
        
        if agent.email_address is not None:
            existing.email_address = agent.email_address
        
        if agent.web_enabled is not None:
            existing.web_enabled = agent.web_enabled
        
        if agent.is_active is not None:
            existing.is_active = agent.is_active
        
        if agent.allow_public_access is not None:
            existing.allow_public_access = agent.allow_public_access
        
        if agent.brand_color is not None:
            existing.brand_color = agent.brand_color
        
        if agent.welcome_message is not None:
            existing.welcome_message = agent.welcome_message
        
        if agent.input_placeholder is not None:
            existing.input_placeholder = agent.input_placeholder
        
        if agent.meta_title is not None:
            existing.meta_title = agent.meta_title
        
        if agent.meta_description is not None:
            existing.meta_description = agent.meta_description
        
        if agent.og_image_url is not None:
            existing.og_image_url = agent.og_image_url
        
        # Timestamp
        existing.updated_at = datetime.utcnow()
        
        # Commit
        db.commit()
        db.refresh(existing)
        
        logger.info(f"Agent updated: {agent_id}")
        
        # Retornar com URL
        response_dict = {
            **{k: v for k, v in existing.__dict__.items() if not k.startswith('_')},
            "public_url": f"https://agentes.genoibot.com/{existing.slug}"
        }
        
        return response_dict
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update agent {agent_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar: {str(e)}"
        )


@router.delete("/{agent_id}", status_code=status.HTTP_200_OK)
async def delete_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Deletar agente (HARD DELETE - Remove do banco)
    
    CORRIGIDO: Agora realmente deleta o agente
    """
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.deleted_at.is_(None)
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agente não encontrado"
        )
    
    try:
        agent_slug = agent.slug
        
        # Hard delete (remover completamente)
        db.delete(agent)
        db.commit()
        
        logger.info(f"Agent deleted: {agent_id} - {agent_slug}")
        
        return {
            "message": "Agente deletado com sucesso",
            "id": str(agent_id),
            "slug": agent_slug
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete agent {agent_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar: {str(e)}"
        )
