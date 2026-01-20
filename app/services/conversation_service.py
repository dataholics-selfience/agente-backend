"""
Conversation Service - Gestão de conversas
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, Dict, List
from uuid import UUID
import uuid
from datetime import datetime

from app.models import Agent, Conversation, Message
from app.services.llm_service import llm_service
from loguru import logger


class ConversationService:
    """Serviço para gerir conversas"""
    
    async def send_message(
        self,
        db: Session,
        agent_id: UUID,
        user_identifier: str,
        message: str,
        channel: str = "web",
        metadata: Optional[Dict] = None,
    ) -> Dict:
        """
        Envia mensagem e recebe resposta do agente
        
        Args:
            db: Sessão do banco
            agent_id: ID do agente
            user_identifier: Identificador do usuário (email, phone, session)
            message: Mensagem do usuário
            channel: Canal (web, whatsapp, email)
            metadata: Metadata adicional
        
        Returns:
            {
                "conversation_id": UUID,
                "message_id": UUID,
                "response": str,
                "tokens_used": int,
                "cost": float,
                "agent": {...}
            }
        """
        try:
            # 1. Buscar agente
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            if not agent:
                raise ValueError(f"Agent {agent_id} not found")
            
            if not agent.is_active:
                raise ValueError(f"Agent {agent_id} is not active")
            
            # 2. Buscar ou criar conversa
            conversation = self._get_or_create_conversation(
                db, agent_id, user_identifier, channel
            )
            
            # 3. Salvar mensagem do usuário
            user_message = Message(
                id=uuid.uuid4(),
                conversation_id=conversation.id,
                role="user",
                content=message,
                metadata=metadata or {},
            )
            db.add(user_message)
            db.commit()
            
            # 4. Buscar histórico
            history = self._get_conversation_history(db, conversation.id, limit=20)
            
            # 5. Montar contexto para LLM
            messages = self._build_llm_context(agent, history)
            
            # 6. Chamar LLM
            logger.info(f"Calling LLM for conversation {conversation.id}")
            llm_response = await llm_service.chat(
                messages=messages,
                model=agent.model,
                temperature=agent.temperature,
            )
            
            # 7. Salvar resposta do assistente
            assistant_message = Message(
                id=uuid.uuid4(),
                conversation_id=conversation.id,
                role="assistant",
                content=llm_response["content"],
                tokens_used=llm_response["tokens_used"],
                cost=llm_response["cost"],
                model=llm_response["model"],
                metadata={
                    "input_tokens": llm_response["input_tokens"],
                    "output_tokens": llm_response["output_tokens"],
                    "time": llm_response["time"],
                },
            )
            db.add(assistant_message)
            
            # 8. Atualizar timestamp da conversa
            conversation.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(assistant_message)
            
            logger.info(
                f"Conversation {conversation.id}: "
                f"{llm_response['tokens_used']} tokens, "
                f"${llm_response['cost']:.4f}"
            )
            
            return {
                "conversation_id": str(conversation.id),
                "message_id": str(assistant_message.id),
                "response": llm_response["content"],
                "tokens_used": llm_response["tokens_used"],
                "cost": llm_response["cost"],
                "agent": {
                    "id": str(agent.id),
                    "name": agent.name,
                    "model": agent.model,
                },
            }
            
        except Exception as e:
            logger.error(f"Error in send_message: {e}")
            db.rollback()
            raise
    
    def _get_or_create_conversation(
        self,
        db: Session,
        agent_id: UUID,
        user_identifier: str,
        channel: str,
    ) -> Conversation:
        """Busca conversa existente ou cria nova"""
        
        # Buscar conversa ativa
        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.agent_id == agent_id,
                Conversation.user_identifier == user_identifier,
                Conversation.channel == channel,
                Conversation.status == "active",
            )
            .first()
        )
        
        if conversation:
            return conversation
        
        # Criar nova conversa
        conversation = Conversation(
            id=uuid.uuid4(),
            agent_id=agent_id,
            user_identifier=user_identifier,
            channel=channel,
            status="active",
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        logger.info(f"Created new conversation {conversation.id}")
        return conversation
    
    def _get_conversation_history(
        self,
        db: Session,
        conversation_id: UUID,
        limit: int = 20,
    ) -> List[Message]:
        """Busca histórico de mensagens"""
        
        messages = (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(desc(Message.created_at))
            .limit(limit)
            .all()
        )
        
        # Reverter para ordem cronológica
        return list(reversed(messages))
    
    def _build_llm_context(
        self,
        agent: Agent,
        history: List[Message],
    ) -> List[Dict[str, str]]:
        """Monta contexto para enviar ao LLM"""
        
        messages = []
        
        # 1. System prompt
        messages.append({
            "role": "system",
            "content": agent.system_prompt,
        })
        
        # 2. Histórico
        for msg in history:
            if msg.role in ["user", "assistant"]:
                messages.append({
                    "role": msg.role,
                    "content": msg.content,
                })
        
        # TODO: Adicionar RAG context aqui se agent.rag_enabled
        
        return messages
    
    def get_conversation(
        self,
        db: Session,
        conversation_id: UUID,
    ) -> Optional[Dict]:
        """Busca detalhes de uma conversa"""
        
        conversation = (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )
        
        if not conversation:
            return None
        
        messages = self._get_conversation_history(db, conversation_id, limit=100)
        
        return {
            "id": str(conversation.id),
            "agent_id": str(conversation.agent_id),
            "user_identifier": conversation.user_identifier,
            "channel": conversation.channel,
            "status": conversation.status,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat() if conversation.updated_at else None,
            "message_count": len(messages),
            "messages": [
                {
                    "id": str(msg.id),
                    "role": msg.role,
                    "content": msg.content,
                    "tokens_used": msg.tokens_used,
                    "cost": msg.cost,
                    "created_at": msg.created_at.isoformat(),
                }
                for msg in messages
            ],
        }


# Instância global
conversation_service = ConversationService()
