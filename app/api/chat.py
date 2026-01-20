"""
Chat API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.schemas import ChatRequest, ChatResponse, ConversationResponse
from app.services.conversation_service import conversation_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Envia mensagem para um agente e recebe resposta
    
    - **agent_id**: ID do agente (UUID)
    - **user_identifier**: Email, telefone ou session ID
    - **message**: Mensagem do usuário
    - **channel**: Canal (web, whatsapp, email)
    """
    try:
        response = await conversation_service.send_message(
            db=db,
            agent_id=request.agent_id,
            user_identifier=request.user_identifier,
            message=request.message,
            channel=request.channel,
            metadata=request.metadata,
        )
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Busca detalhes de uma conversa incluindo histórico de mensagens
    
    - **conversation_id**: ID da conversa (UUID)
    """
    conversation = conversation_service.get_conversation(db, conversation_id)
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversation


@router.get("/conversations/{conversation_id}/messages")
async def get_messages(
    conversation_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Busca mensagens de uma conversa
    
    - **conversation_id**: ID da conversa (UUID)
    """
    conversation = conversation_service.get_conversation(db, conversation_id)
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "conversation_id": conversation["id"],
        "messages": conversation["messages"],
    }
