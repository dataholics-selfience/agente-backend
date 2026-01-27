from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import sys
sys.path.append('..')
from database import get_db
from models import Agent

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/overview")
async def get_analytics_overview(period: str = "7d", db: Session = Depends(get_db)):
    """
    Retorna métricas globais do sistema
    
    Args:
        period: Período para análise (7d, 30d, 90d)
    """
    # Calcular datas
    now = datetime.utcnow()
    if period == "7d":
        start_date = now - timedelta(days=7)
    elif period == "30d":
        start_date = now - timedelta(days=30)
    elif period == "90d":
        start_date = now - timedelta(days=90)
    else:
        start_date = now - timedelta(days=7)
    
    # Total de agentes
    total_agents = db.query(Agent).filter(Agent.deleted_at.is_(None)).count()
    active_agents = db.query(Agent).filter(
        Agent.deleted_at.is_(None),
        Agent.is_active == True
    ).count()
    
    # Por enquanto, retornar zeros para métricas de conversas
    # (serão implementadas quando o modelo Conversation estiver completo)
    total_conversations = 0
    active_conversations = 0
    total_messages = 0
    messages_today = 0
    total_cost_today = 0.0
    total_cost_period = 0.0
    avg_response_time = 0.0
    
    # Calcular trends (simplificado)
    agents_trend = 0
    messages_trend = 0
    
    return {
        "total_agents": total_agents,
        "active_agents": active_agents,
        "total_conversations": total_conversations,
        "active_conversations": active_conversations,
        "total_messages": total_messages,
        "messages_today": messages_today,
        "total_cost_today": total_cost_today,
        "total_cost_period": total_cost_period,
        "avg_response_time": avg_response_time,
        "agents_trend": agents_trend,
        "messages_trend": messages_trend,
        "usage_trend": [],  # Array vazio por enquanto
        "channel_distribution": {
            "web": 0,
            "whatsapp": 0,
            "email": 0
        },
        "top_agents": []
    }

@router.get("/agents/{agent_id}")
async def get_agent_analytics(agent_id: str, period: str = "7d", db: Session = Depends(get_db)):
    """
    Métricas específicas de um agente
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent:
        return {"error": "Agent not found"}
    
    return {
        "agent": {
            "id": str(agent.id),
            "name": agent.name,
            "slug": agent.slug
        },
        "total_conversations": 0,
        "total_messages": 0,
        "total_cost": 0.0,
        "avg_response_time": 0.0,
        "automated_resolution_rate": 0.0,
        "escalation_rate": 0.0,
        "usage_by_day": [],
        "cost_by_day": [],
        "channel_breakdown": {
            "web": 0,
            "whatsapp": 0,
            "email": 0
        }
    }
