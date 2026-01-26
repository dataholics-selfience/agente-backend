from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import os

from database import get_db
from models import Agent
from schemas import AgentCreate, AgentUpdate, AgentResponse
from auth import get_current_user
from utils import normalize_slug, validate_slug

router = APIRouter(prefix="/api/agents", tags=["agents"], dependencies=[Depends(get_current_user)])

@router.get("", response_model=List[AgentResponse])
async def list_agents(db: Session = Depends(get_db)):
    agents = db.query(Agent).filter(Agent.deleted_at.is_(None)).order_by(Agent.created_at.desc()).all()
    for agent in agents:
        agent.public_url = f"https://agentes.genoibot.com/chat/{agent.slug}"
    return agents

@router.post("", response_model=AgentResponse, status_code=201)
async def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    slug = normalize_slug(agent.slug or agent.name)
    is_valid, error = validate_slug(slug)
    if not is_valid:
        raise HTTPException(400, error)
    
    exists = db.query(Agent).filter(Agent.slug == slug).first()
    if exists:
        raise HTTPException(400, "Slug already exists")
    
    new_agent = Agent(**agent.dict(exclude={"slug"}), slug=slug)
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    new_agent.public_url = f"https://agentes.genoibot.com/chat/{slug}"
    return new_agent

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: UUID, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id, Agent.deleted_at.is_(None)).first()
    if not agent:
        raise HTTPException(404, "Agent not found")
    agent.public_url = f"https://agentes.genoibot.com/chat/{agent.slug}"
    return agent

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: UUID, agent_update: AgentUpdate, db: Session = Depends(get_db)):
    existing = db.query(Agent).filter(Agent.id == agent_id, Agent.deleted_at.is_(None)).first()
    if not existing:
        raise HTTPException(404, "Agent not found")
    
    update_data = agent_update.dict(exclude_unset=True)
    
    if "slug" in update_data and update_data["slug"]:
        new_slug = normalize_slug(update_data["slug"])
        is_valid, error = validate_slug(new_slug)
        if not is_valid:
            raise HTTPException(400, error)
        
        if new_slug != existing.slug:
            duplicate = db.query(Agent).filter(Agent.slug == new_slug, Agent.id != agent_id).first()
            if duplicate:
                raise HTTPException(400, "Slug already in use")
            update_data["slug"] = new_slug
    
    for key, value in update_data.items():
        setattr(existing, key, value)
    
    db.commit()
    db.refresh(existing)
    existing.public_url = f"https://agentes.genoibot.com/chat/{existing.slug}"
    return existing

@router.delete("/{agent_id}", status_code=204)
async def delete_agent(agent_id: UUID, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id, Agent.deleted_at.is_(None)).first()
    if not agent:
        raise HTTPException(404, "Agent not found")
    db.delete(agent)
    db.commit()
    return None
