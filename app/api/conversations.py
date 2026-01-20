"""Conversations API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from app.core.database import get_db
from app.services.conversation_service import ConversationService

router = APIRouter()

class ChatRequest(BaseModel):
    agent_id: uuid.UUID
    user_identifier: str
    message: str
    channel: str = "web"

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tokens: int
    cost: float
    processing_time: float

@router.post("/chat", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    try:
        result = await ConversationService.process_message(
            db=db,
            agent_id=request.agent_id,
            user_identifier=request.user_identifier,
            user_message=request.message,
            channel=request.channel
        )
        
        return ChatResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")
