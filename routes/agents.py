from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from database import get_db
from models import Agent
import sys
sys.path.append('..')

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

@router.get("", response_model=List[AgentResponse])
async def list_agents(db: Session = Depends(get_db)):
    # SEM deleted_at!
    agents = db.query(Agent).filter(Agent.is_active == True).order_by(Agent.created_at.desc()).all()
    return agents

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent
