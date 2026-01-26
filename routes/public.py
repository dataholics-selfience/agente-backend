from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID, uuid4
from datetime import datetime
import time

from database import get_db
from models import Agent, Conversation, Message
from schemas import ChatRequest, ChatResponse
from utils import normalize_slug
from services.llm import LLMService

router = APIRouter(prefix="/api/public", tags=["public"])

@router.get("/agents/{slug}")
async def get_public_agent(slug: str, db: Session = Depends(get_db)):
    normalized = normalize_slug(slug)
    agent = db.query(Agent).filter(
        func.lower(Agent.slug) == normalized.lower(),
        Agent.is_active == True,
        Agent.allow_public_access == True,
        Agent.deleted_at.is_(None)
    ).first()
    
    if not agent:
        agent = db.query(Agent).filter(
            Agent.slug == slug,
            Agent.is_active == True,
            Agent.allow_public_access == True,
            Agent.deleted_at.is_(None)
        ).first()
    
    if not agent:
        raise HTTPException(404, "Agent not found")
    
    return {
        "id": str(agent.id),
        "slug": agent.slug,
        "name": agent.name,
        "description": agent.description,
        "brand_color": agent.brand_color,
        "welcome_message": agent.welcome_message,
        "input_placeholder": agent.input_placeholder,
        "meta_title": agent.meta_title,
        "meta_description": agent.meta_description
    }

@router.post("/agents/{slug}/chat", response_model=ChatResponse)
async def public_chat(slug: str, chat: ChatRequest, db: Session = Depends(get_db)):
    normalized = normalize_slug(slug)
    agent = db.query(Agent).filter(
        func.lower(Agent.slug) == normalized.lower(),
        Agent.is_active == True,
        Agent.deleted_at.is_(None)
    ).first()
    
    if not agent:
        raise HTTPException(404, "Agent not found")
    
    session_id = UUID(chat.session_id) if chat.session_id else uuid4()
    
    conv = db.query(Conversation).filter(
        Conversation.agent_id == agent.id,
        Conversation.session_id == session_id
    ).first()
    
    if not conv:
        conv = Conversation(agent_id=agent.id, session_id=session_id, channel="web")
        db.add(conv)
        db.commit()
    
    user_msg = Message(conversation_id=conv.id, role="user", content=chat.message)
    db.add(user_msg)
    db.commit()
    
    history = db.query(Message).filter(
        Message.conversation_id == conv.id
    ).order_by(Message.created_at.desc()).limit(20).all()
    
    messages = [{"role": "system", "content": agent.system_prompt}]
    messages.extend([{"role": m.role, "content": m.content} for m in reversed(history)])
    
    start = time.time()
    llm = LLMService()
    result = llm.generate(messages, model=agent.model, temperature=agent.temperature, max_tokens=agent.max_tokens)
    processing_time = time.time() - start
    
    assistant_msg = Message(
        conversation_id=conv.id,
        role="assistant",
        content=result["content"],
        tokens=result["tokens"],
        cost=result["cost"],
        processing_time=processing_time,
        model_used=agent.model
    )
    db.add(assistant_msg)
    db.commit()
    
    return ChatResponse(
        conversation_id=conv.id,
        session_id=session_id,
        response=result["content"],
        tokens=result["tokens"],
        cost=result["cost"]
    )
