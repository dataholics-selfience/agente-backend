"""Agents API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
import uuid

from app.core.database import get_db
from app.models import Agent, AgentStatus

router = APIRouter()

class AgentCreate(BaseModel):
    name: str
    system_prompt: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.7

class AgentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    name: str
    system_prompt: str
    model: str
    temperature: float
    status: str
    created_at: datetime
    updated_at: datetime

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
    agent = Agent(
        name=agent_data.name,
        system_prompt=agent_data.system_prompt,
        model=agent_data.model,
        temperature=agent_data.temperature,
        status=AgentStatus.active
    )
    
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    return agent
