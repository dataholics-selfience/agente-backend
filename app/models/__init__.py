"""
SQLAlchemy Models
"""
from sqlalchemy import Column, String, Text, Boolean, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Agent(Base):
    """Modelo de Agente Conversacional"""
    __tablename__ = "agents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    system_prompt = Column(Text, nullable=False)
    model = Column(String(100), default="gpt-4o-mini")
    temperature = Column(Float, default=0.7)
    rag_enabled = Column(Boolean, default=False)
    whatsapp_enabled = Column(Boolean, default=False)
    email_enabled = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    conversations = relationship("Conversation", back_populates="agent")
    documents = relationship("Document", back_populates="agent")


class Conversation(Base):
    """Modelo de Conversa"""
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    user_identifier = Column(String(255), nullable=False)  # phone, email, session_id
    channel = Column(String(50), default="web")  # web, whatsapp, email
    status = Column(String(50), default="active")  # active, paused, closed
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    agent = relationship("Agent", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """Modelo de Mensagem"""
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    role = Column(String(50), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    model = Column(String(100))
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")


class Document(Base):
    """Modelo de Documento RAG"""
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(100))
    size = Column(Integer)
    chunk_count = Column(Integer, default=0)
    status = Column(String(50), default="processing")  # processing, ready, error
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    agent = relationship("Agent", back_populates="documents")


class ChannelConfig(Base):
    """Configuração de Canais (WhatsApp, Email)"""
    __tablename__ = "channel_configs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    channel = Column(String(50), nullable=False)  # whatsapp, email
    identifier = Column(String(255), nullable=False)  # phone number, email
    config = Column(JSON, default={})  # configurações específicas do canal
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
