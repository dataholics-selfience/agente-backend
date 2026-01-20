"""
Agents API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import uuid

from app.core.database import get_db
from app.models import Agent
from app.schemas import AgentCreate, AgentUpdate, AgentResponse

router = APIRouter()


@router.post("/", response_model=AgentResponse, status_code=201)
def create_agent(
    agent_data: AgentCreate,
    db: Session = Depends(get_db),
):
    """
    Cria um novo agente
    """
    agent = Agent(
        id=uuid.uuid4(),
        **agent_data.model_dump()
    )
    
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    return agent


@router.get("/", response_model=List[AgentResponse])
def list_agents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Lista todos os agentes
    """
    agents = db.query(Agent).offset(skip).limit(limit).all()
    return agents


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(
    agent_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Busca um agente específico
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return agent


@router.put("/{agent_id}", response_model=AgentResponse)
def update_agent(
    agent_id: UUID,
    agent_data: AgentUpdate,
    db: Session = Depends(get_db),
):
    """
    Atualiza um agente
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Atualizar apenas campos fornecidos
    update_data = agent_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)
    
    db.commit()
    db.refresh(agent)
    
    return agent


@router.delete("/{agent_id}", status_code=204)
def delete_agent(
    agent_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Soft delete de um agente (marca como inativo)
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent.is_active = False
    db.commit()
    
    return None
