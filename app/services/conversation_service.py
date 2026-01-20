from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional, List, Dict
from uuid import UUID
import time

from app.models import Conversation, Message, Agent, MessageRole
from app.services.llm_service import get_llm_service
from app.services.rag_service import get_rag_service


class ConversationService:
    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()
    
    async def get_or_create_conversation(
        self,
        db: AsyncSession,
        agent_id: UUID,
        user_identifier: str,
        channel: str = "web",
        conversation_id: Optional[UUID] = None,
    ) -> Conversation:
        """Busca conversa existente ou cria nova"""
        
        if conversation_id:
            result = await db.execute(
                select(Conversation).where(Conversation.id == conversation_id)
            )
            conversation = result.scalar_one_or_none()
            if conversation:
                return conversation
        
        # Busca conversa ativa do mesmo user com mesmo agente
        result = await db.execute(
            select(Conversation)
            .where(
                Conversation.agent_id == agent_id,
                Conversation.user_identifier == user_identifier,
                Conversation.channel == channel,
                Conversation.status == "active",
            )
            .order_by(desc(Conversation.updated_at))
        )
        conversation = result.scalar_one_or_none()
        
        if conversation:
            return conversation
        
        # Cria nova conversa
        conversation = Conversation(
            agent_id=agent_id,
            user_identifier=user_identifier,
            channel=channel,
            status="active",
        )
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        
        return conversation
    
    async def get_conversation_history(
        self,
        db: AsyncSession,
        conversation_id: UUID,
        limit: int = 20,
    ) -> List[Dict[str, str]]:
        """
        Busca histórico de mensagens e formata para LLM
        
        Returns:
            Lista no formato [{"role": "user", "content": "..."}, ...]
        """
        result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(desc(Message.created_at))
            .limit(limit)
        )
        messages = result.scalars().all()
        
        # Inverte ordem (mais antigas primeiro)
        messages = list(reversed(messages))
        
        # Formata para LLM
        return [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages
        ]
    
    async def send_message(
        self,
        db: AsyncSession,
        agent_id: UUID,
        user_identifier: str,
        content: str,
        channel: str = "web",
        conversation_id: Optional[UUID] = None,
    ) -> Dict:
        """
        Processa mensagem do usuário e gera resposta do agente
        
        Returns:
            {
                "conversation_id": UUID,
                "user_message": Message,
                "assistant_message": Message,
            }
        """
        start_time = time.time()
        
        # 1. Busca agente
        result = await db.execute(
            select(Agent).where(Agent.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        
        # 2. Busca ou cria conversa
        conversation = await self.get_or_create_conversation(
            db, agent_id, user_identifier, channel, conversation_id
        )
        
        # 3. Salva mensagem do usuário
        user_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=content,
        )
        db.add(user_message)
        await db.commit()
        await db.refresh(user_message)
        
        # 4. Busca histórico
        history = await self.get_conversation_history(db, conversation.id, limit=20)
        
        # 5. Prepara contexto RAG (se habilitado)
        rag_context = ""
        if agent.rag_enabled:
            rag_context = await self.rag_service.search_context(
                agent_id=agent.id,
                query=content,
                top_k=3,
            )
        
        # 6. Monta mensagens para LLM
        messages = []
        
        # System prompt
        system_content = agent.system_prompt
        if rag_context:
            system_content += f"\n\nKnowledge Base:\n{rag_context}"
        
        messages.append({
            "role": "system",
            "content": system_content,
        })
        
        # Histórico
        messages.extend(history)
        
        # 7. Chama LLM
        llm_response = self.llm_service.chat(
            messages=messages,
            model=agent.model,
            temperature=agent.temperature,
        )
        
        # 8. Salva resposta do assistente
        assistant_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=llm_response["content"],
            tokens=llm_response["tokens"],
            cost=llm_response["cost"],
            processing_time=llm_response["processing_time"],
            metadata={
                "model": llm_response["model"],
                "input_tokens": llm_response["input_tokens"],
                "output_tokens": llm_response["output_tokens"],
            },
        )
        db.add(assistant_message)
        await db.commit()
        await db.refresh(assistant_message)
        
        total_time = time.time() - start_time
        
        return {
            "conversation_id": conversation.id,
            "user_message": user_message,
            "assistant_message": assistant_message,
            "total_processing_time": total_time,
        }


# Singleton
_conversation_service: Optional[ConversationService] = None


def get_conversation_service() -> ConversationService:
    global _conversation_service
    if _conversation_service is None:
        _conversation_service = ConversationService()
    return _conversation_service
