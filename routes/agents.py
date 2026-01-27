from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
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
    slug: str
    description: str | None = None
    system_prompt: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.7

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
    agent = Agent(**agent_data.dict())
    db.add(agent)
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
