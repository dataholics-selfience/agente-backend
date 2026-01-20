"""Health Check API"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import os

from app.core.database import get_db

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    openai_configured = bool(os.getenv("OPENAI_API_KEY"))
    
    return {
        "status": "online",
        "database": db_status,
        "openai_configured": openai_configured,
        "version": "3.0.0"
    }

@router.get("/health/db")
async def database_health(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT COUNT(*) FROM agents"))
        agent_count = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) FROM conversations"))
        conversation_count = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) FROM messages"))
        message_count = result.fetchone()[0]
        
        return {
            "status": "healthy",
            "agents": agent_count,
            "conversations": conversation_count,
            "messages": message_count
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
