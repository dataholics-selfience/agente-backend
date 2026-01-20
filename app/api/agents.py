"""
Agents API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import uuid

from app.core.database import get_db_dependency
from app.models import Agent, AgentStatus

router = APIRouter()

# Schemas
class AgentCreate(BaseModel):
    name: str
    system_prompt: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    rag_enabled: bool = False
    whatsapp_enabled: bool = False
    email_enabled: bool = False

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    system_prompt: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    rag_enabled: Optional[bool] = None
    whatsapp_enabled: Optional[bool] = None
    email_enabled: Optional[bool] = None
    status: Optional[str] = None

class AgentResponse(BaseModel):
    id: uuid.UUID
    name: str
    system_prompt: str
    model: str
    temperature: float
    rag_enabled: bool
    whatsapp_enabled: bool
    email_enabled: bool
    status: str
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

# Endpoints
@router.get("/agents", response_model=List[AgentResponse])
async def list_agents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_dependency)
):
    """Listar todos os agentes"""
    agents = db.query(Agent).offset(skip).limit(limit).all()
    return agents

@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: uuid.UUID, db: Session = Depends(get_db_dependency)):
    """Buscar agente por ID"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agente não encontrado")
    
    return agent

@router.post("/agents", response_model=AgentResponse)
async def create_agent(agent_data: AgentCreate, db: Session = Depends(get_db_dependency)):
    """Criar novo agente"""
    
    agent = Agent(
        name=agent_data.name,
        system_prompt=agent_data.system_prompt,
        model=agent_data.model,
        temperature=agent_data.temperature,
        rag_enabled=agent_data.rag_enabled,
        whatsapp_enabled=agent_data.whatsapp_enabled,
        email_enabled=agent_data.email_enabled,
        status=AgentStatus.active
    )
    
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    return agent

@router.put("/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: uuid.UUID,
    agent_data: AgentUpdate,
    db: Session = Depends(get_db_dependency)
):
    """Atualizar agente"""
    
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agente não encontrado")
    
    # Atualizar campos fornecidos
    update_data = agent_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(agent, field, value)
    
    db.commit()
    db.refresh(agent)
    
    return agent

@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: uuid.UUID, db: Session = Depends(get_db_dependency)):
    """Deletar agente"""
    
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agente não encontrado")
    
    db.delete(agent)
    db.commit()
    
    return {"message": "Agente deletado com sucesso"}
