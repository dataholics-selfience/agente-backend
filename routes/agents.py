from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, validator
from datetime import datetime
from slugify import slugify
import sys
sys.path.append('..')
from database import get_db
from models import Agent

router = APIRouter(prefix="/api/agents", tags=["agents"])

class AgentResponse(BaseModel):
    id: str
    slug: str
    name: str
    description: str | None
    avatar_url: str | None
    system_prompt: str
    model: str
    temperature: float
    max_tokens: int
    is_active: bool
    brand_color: str
    welcome_message: str
    
    class Config:
        from_attributes = True

class AgentCreate(BaseModel):
    name: str
    slug: str | None = None
    description: str | None = None
    system_prompt: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    
    @validator('slug', pre=True, always=True)
    def normalize_slug(cls, v, values):
        if v:
            # Normalizar slug fornecido
            return slugify(v, separator='-', lowercase=True)
        elif 'name' in values:
            # Gerar slug a partir do nome
            return slugify(values['name'], separator='-', lowercase=True)
        return None

@router.get("", response_model=List[AgentResponse])
async def list_agents(db: Session = Depends(get_db)):
    # Filtra por deleted_at IS NULL
    agents = db.query(Agent).filter(Agent.deleted_at.is_(None)).order_by(Agent.created_at.desc()).all()
    return agents

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id, Agent.deleted_at.is_(None)).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.post("", response_model=AgentResponse)
async def create_agent(agent_data: AgentCreate, db: Session = Depends(get_db)):
    # Verificar se slug já existe
    existing = db.query(Agent).filter(Agent.slug == agent_data.slug, Agent.deleted_at.is_(None)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Slug já existe. Escolha outro nome/slug.")
    
    agent = Agent(**agent_data.dict())
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: str, agent_data: dict, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id, Agent.deleted_at.is_(None)).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Se mudar o slug, normalizar
    if 'slug' in agent_data and agent_data['slug']:
        new_slug = slugify(agent_data['slug'], separator='-', lowercase=True)
        # Verificar se novo slug já existe (em outro agente)
        existing = db.query(Agent).filter(
            Agent.slug == new_slug,
            Agent.id != agent_id,
            Agent.deleted_at.is_(None)
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Slug já existe. Escolha outro.")
        agent_data['slug'] = new_slug
    
    # Atualizar campos
    for key, value in agent_data.items():
        if hasattr(agent, key):
            setattr(agent, key, value)
    
    db.commit()
    db.refresh(agent)
    return agent

@router.delete("/{agent_id}")
async def delete_agent(agent_id: str, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    # Soft delete
    agent.deleted_at = datetime.utcnow()
    db.commit()
    return {"message": "Agent deleted successfully"}
