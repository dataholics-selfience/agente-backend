"""SQLAlchemy Models"""
from sqlalchemy import Column, String, Float, Boolean, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base

class AgentStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    archived = "archived"

class ConversationStatus(str, enum.Enum):
    active = "active"
    paused = "paused"
    closed = "closed"

class MessageRole(str, enum.Enum):
    user = "user"
    assistant = "assistant"
    system = "system"

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    system_prompt = Column(Text, nullable=False)
    model = Column(String(100), nullable=False, default="gpt-4o-mini")
    temperature = Column(Float, nullable=False, default=0.7)
    rag_enabled = Column(Boolean, nullable=False, default=False)
    whatsapp_enabled = Column(Boolean, nullable=False, default=False)
    email_enabled = Column(Boolean, nullable=False, default=False)
    status = Column(Enum(AgentStatus), nullable=False, default=AgentStatus.active)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    user_identifier = Column(String(255), nullable=False)
    channel = Column(String(50), nullable=False, default="web")
    status = Column(Enum(ConversationStatus), nullable=False, default=ConversationStatus.active)
    extra_data = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    tokens = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    processing_time = Column(Float, default=0.0)
    extra_data = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50))
    file_size = Column(Integer)
    status = Column(String(50), nullable=False, default="processing")
    chunks_count = Column(Integer, default=0)
    extra_data = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class ChannelConfig(Base):
    __tablename__ = "channel_configs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    channel = Column(String(50), nullable=False)
    config = Column(JSONB, default={})
    enabled = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
