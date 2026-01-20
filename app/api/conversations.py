"""
Conversations API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import uuid

from app.core.database import get_db_dependency
from app.models import Conversation, Message
from app.services.conversation_service import ConversationService

router = APIRouter()

# Schemas
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

class MessageResponse(BaseModel):
    id: uuid.UUID
    role: str
    content: str
    tokens: int
    cost: float
    created_at: str
    
    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: uuid.UUID
    agent_id: uuid.UUID
    user_identifier: str
    channel: str
    status: str
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

# Endpoints
@router.post("/chat", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db_dependency)
):
    """
    Enviar mensagem para um agente
    
    O agente processará a mensagem e retornará uma resposta
    """
    
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
        raise HTTPException(status_code=500, detail=f"Erro ao processar mensagem: {str(e)}")

@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db_dependency)
):
    """Buscar detalhes de uma conversa"""
    
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    return conversation

@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: uuid.UUID,
    limit: int = 50,
    db: Session = Depends(get_db_dependency)
):
    """Buscar mensagens de uma conversa"""
    
    # Verificar se conversa existe
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    # Buscar mensagens
    messages = ConversationService.get_conversation_history(db, conversation_id, limit)
    
    return messages

@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    agent_id: Optional[uuid.UUID] = None,
    user_identifier: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db_dependency)
):
    """Listar conversas com filtros opcionais"""
    
    query = db.query(Conversation)
    
    if agent_id:
        query = query.filter(Conversation.agent_id == agent_id)
    
    if user_identifier:
        query = query.filter(Conversation.user_identifier == user_identifier)
    
    conversations = query.offset(skip).limit(limit).all()
    
    return conversations
