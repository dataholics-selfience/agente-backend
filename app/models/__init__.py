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
    
    # IDs
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug = Column(String(100), unique=True, nullable=True, index=True)  # URL pública
    
    # Basic Info
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # System Configuration
    system_prompt = Column(Text, nullable=False)
    model = Column(String(100), nullable=False, default="gpt-4o-mini")
    temperature = Column(Float, nullable=False, default=0.7)
    max_tokens = Column(Integer, nullable=False, default=1000)
    top_p = Column(Float, nullable=False, default=1.0)
    frequency_penalty = Column(Float, nullable=False, default=0.0)
    presence_penalty = Column(Float, nullable=False, default=0.0)
    
    # Features
    rag_enabled = Column(Boolean, nullable=False, default=False)
    function_calling_enabled = Column(Boolean, nullable=False, default=False)
    
    # Channels
    whatsapp_enabled = Column(Boolean, nullable=False, default=False)
    whatsapp_number = Column(String(20), nullable=True)
    email_enabled = Column(Boolean, nullable=False, default=False)
    email_address = Column(String(200), nullable=True)
    web_enabled = Column(Boolean, nullable=False, default=True)
    
    # Public Access
    is_active = Column(Boolean, nullable=False, default=True)
    allow_public_access = Column(Boolean, nullable=False, default=True)
    
    # Customization (White-label)
    brand_color = Column(String(7), nullable=False, default="#4F46E5")
    welcome_message = Column(Text, nullable=False, default="Olá! Como posso ajudar?")
    input_placeholder = Column(String(100), nullable=False, default="Digite sua mensagem...")
    
    # SEO
    meta_title = Column(String(200), nullable=True)
    meta_description = Column(String(500), nullable=True)
    og_image_url = Column(String(500), nullable=True)
    
    # Legacy
    status = Column(Enum(AgentStatus), nullable=False, default=AgentStatus.active)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    user_identifier = Column(String(255), nullable=False)
    session_id = Column(UUID(as_uuid=True), nullable=True)  # Para público sem auth
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
