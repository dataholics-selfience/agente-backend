from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from uuid import UUID

from app.core.database import get_async_db
from app.models import Conversation, Message
from app.schemas import (
    ChatRequest,
    ChatResponse,
    MessageResponse,
    ConversationResponse,
    ConversationWithMessages,
)
from app.services import get_conversation_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Envia mensagem para o agente e recebe resposta
    """
    conversation_service = get_conversation_service()
    
    try:
        result = await conversation_service.send_message(
            db=db,
            agent_id=request.agent_id,
            user_identifier=request.user_identifier,
            content=request.message,
            channel=request.channel,
            conversation_id=request.conversation_id,
        )
        
        return ChatResponse(
            conversation_id=result["conversation_id"],
            message=MessageResponse.model_validate(result["user_message"]),
            agent_response=MessageResponse.model_validate(result["assistant_message"]),
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    agent_id: UUID = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
):
    """Lista conversas"""
    query = select(Conversation).order_by(desc(Conversation.updated_at))
    
    if agent_id:
        query = query.where(Conversation.agent_id == agent_id)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    conversations = result.scalars().all()
    
    return conversations


@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
async def get_conversation(
    conversation_id: UUID,
    db: AsyncSession = Depends(get_async_db),
):
    """Busca conversa com mensagens"""
    result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation {conversation_id} not found"
        )
    
    # Busca mensagens
    messages_result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    messages = messages_result.scalars().all()
    
    # Formata resposta
    conversation_dict = {
        "id": conversation.id,
        "agent_id": conversation.agent_id,
        "user_identifier": conversation.user_identifier,
        "channel": conversation.channel,
        "status": conversation.status,
        "metadata": conversation.metadata,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at,
        "messages": [MessageResponse.model_validate(msg) for msg in messages],
    }
    
    return ConversationWithMessages(**conversation_dict)
