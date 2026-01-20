"""Conversation Service"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Dict
import uuid

from app.models import Agent, Conversation, Message, MessageRole, ConversationStatus
from app.services.llm_service import LLMService

class ConversationService:
    
    @staticmethod
    def get_or_create_conversation(
        db: Session,
        agent_id: uuid.UUID,
        user_identifier: str,
        channel: str = "web"
    ) -> Conversation:
        conversation = db.query(Conversation).filter(
            Conversation.agent_id == agent_id,
            Conversation.user_identifier == user_identifier,
            Conversation.channel == channel,
            Conversation.status == ConversationStatus.active
        ).first()
        
        if conversation:
            return conversation
        
        conversation = Conversation(
            agent_id=agent_id,
            user_identifier=user_identifier,
            channel=channel,
            status=ConversationStatus.active
        )
        
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        return conversation
    
    @staticmethod
    def get_conversation_history(
        db: Session,
        conversation_id: uuid.UUID,
        limit: int = 20
    ) -> List[Message]:
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(desc(Message.created_at)).limit(limit).all()
        
        return list(reversed(messages))
    
    @staticmethod
    async def process_message(
        db: Session,
        agent_id: uuid.UUID,
        user_identifier: str,
        user_message: str,
        channel: str = "web"
    ) -> Dict:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        
        if not agent:
            raise ValueError(f"Agente {agent_id} não encontrado")
        
        conversation = ConversationService.get_or_create_conversation(
            db, agent_id, user_identifier, channel
        )
        
        user_msg = Message(
            conversation_id=conversation.id,
            role=MessageRole.user,
            content=user_message,
            tokens=0,
            cost=0.0
        )
        db.add(user_msg)
        db.commit()
        
        history = ConversationService.get_conversation_history(
            db, conversation.id, limit=20
        )
        
        messages = [
            {"role": "system", "content": agent.system_prompt}
        ]
        
        for msg in history:
            messages.append({
                "role": msg.role.value,
                "content": msg.content
            })
        
        llm_response = await LLMService.generate_response(
            messages=messages,
            model=agent.model,
            temperature=agent.temperature
        )
        
        assistant_msg = Message(
            conversation_id=conversation.id,
            role=MessageRole.assistant,
            content=llm_response["content"],
            tokens=llm_response["tokens"],
            cost=llm_response["cost"],
            processing_time=llm_response["processing_time"],
            extra_data={
                "model": llm_response["model"],
                "input_tokens": llm_response["input_tokens"],
                "output_tokens": llm_response["output_tokens"]
            }
        )
        db.add(assistant_msg)
        db.commit()
        
        return {
            "conversation_id": str(conversation.id),
            "response": llm_response["content"],
            "tokens": llm_response["tokens"],
            "cost": llm_response["cost"],
            "processing_time": llm_response["processing_time"]
        }
