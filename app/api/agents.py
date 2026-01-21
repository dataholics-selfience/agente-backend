"""Agents API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime
import uuid
import re

from app.core.database import get_db
from app.models import Agent, AgentStatus

router = APIRouter()

def generate_slug(name: str) -> str:
    """Gera slug a partir do nome"""
    slug = name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

class AgentCreate(BaseModel):
    name: str
    system_prompt: str
    model: str = "gpt-4o-mini"
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, ge=1, le=4096)
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)
    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    brand_color: str = "#4F46E5"
    welcome_message: str = "Olá! Como posso ajudar?"
    input_placeholder: str = "Digite sua mensagem..."

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    system_prompt: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1, le=4096)
    top_p: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    frequency_penalty: Optional[float] = Field(default=None, ge=-2.0, le=2.0)
    presence_penalty: Optional[float] = Field(default=None, ge=-2.0, le=2.0)
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    brand_color: Optional[str] = None
    welcome_message: Optional[str] = None
    input_placeholder: Optional[str] = None
    is_active: Optional[bool] = None
    allow_public_access: Optional[bool] = None

class AgentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    slug: Optional[str]
    name: str
    description: Optional[str]
    avatar_url: Optional[str]
    system_prompt: str
    model: str
    temperature: float
    max_tokens: int
    top_p: float
    frequency_penalty: float
    presence_penalty: float
    brand_color: str
    welcome_message: str
    input_placeholder: str
    is_active: bool
    allow_public_access: bool
    rag_enabled: bool
    whatsapp_enabled: bool
    email_enabled: bool
    status: str
    created_at: datetime
    updated_at: datetime

class PublicAgentResponse(BaseModel):
    """Resposta pública (SEM system_prompt e dados sensíveis)"""
    model_config = ConfigDict(from_attributes=True)
    
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

@router.get("/agents", response_model=List[AgentResponse])
async def list_agents(db: Session = Depends(get_db)):
    agents = db.query(Agent).all()
    return agents

@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: uuid.UUID, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agente não encontrado")
    
    return agent

@router.post("/agents", response_model=AgentResponse)
async def create_agent(agent_data: AgentCreate, db: Session = Depends(get_db)):
    # Gera slug único
    base_slug = generate_slug(agent_data.name)
    slug = base_slug
    counter = 1
    
    while db.query(Agent).filter(Agent.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    agent = Agent(
        slug=slug,
        name=agent_data.name,
        description=agent_data.description,
        avatar_url=agent_data.avatar_url,
        system_prompt=agent_data.system_prompt,
        model=agent_data.model,
        temperature=agent_data.temperature,
        max_tokens=agent_data.max_tokens,
        top_p=agent_data.top_p,
        frequency_penalty=agent_data.frequency_penalty,
        presence_penalty=agent_data.presence_penalty,
        brand_color=agent_data.brand_color,
        welcome_message=agent_data.welcome_message,
        input_placeholder=agent_data.input_placeholder,
        status=AgentStatus.active,
        is_active=True,
        allow_public_access=True
    )
    
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    return agent

@router.put("/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: uuid.UUID,
    agent_data: AgentUpdate,
    db: Session = Depends(get_db)
):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agente não encontrado")
    
    # Atualiza apenas campos fornecidos
    update_data = agent_data.model_dump(exclude_unset=True)
    
    # Se nome mudou, atualiza slug
    if "name" in update_data and update_data["name"] != agent.name:
        base_slug = generate_slug(update_data["name"])
        slug = base_slug
        counter = 1
        
        while db.query(Agent).filter(Agent.slug == slug, Agent.id != agent_id).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        agent.slug = slug
    
    for key, value in update_data.items():
        setattr(agent, key, value)
    
    db.commit()
    db.refresh(agent)
    
    return agent

@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: uuid.UUID, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agente não encontrado")
    
    # Soft delete
    agent.is_active = False
    agent.status = AgentStatus.archived
    
    db.commit()
    
    return {"message": "Agente desativado com sucesso", "agent_id": str(agent_id)}
