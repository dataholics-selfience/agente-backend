"""
Database Models
"""
from sqlalchemy import Column, String, Boolean, Float, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class Agent(Base):
    """
    Modelo de Agente Conversacional
    """
    __tablename__ = "agents"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic Info
    name = Column(String(200), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    avatar_url = Column(String(500))
    
    # System Configuration
    system_prompt = Column(Text, nullable=False)
    model = Column(String(50), default="gpt-4o-mini")
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer, default=1500)
    top_p = Column(Float, default=1.0)
    frequency_penalty = Column(Float, default=0.0)
    presence_penalty = Column(Float, default=0.0)
    
    # Features
    rag_enabled = Column(Boolean, default=False)
    function_calling_enabled = Column(Boolean, default=False)
    
    # Channels
    whatsapp_enabled = Column(Boolean, default=False)
    whatsapp_number = Column(String(20))
    email_enabled = Column(Boolean, default=False)
    email_address = Column(String(200))
    web_enabled = Column(Boolean, default=True)
    
    # Public Access Control
    is_active = Column(Boolean, default=True)
    allow_public_access = Column(Boolean, default=True)
    
    # Branding (White-label)
    brand_color = Column(String(7), default="#4F46E5")
    welcome_message = Column(Text, default="Olá! Como posso ajudar?")
    input_placeholder = Column(String(100), default="Digite sua mensagem...")
    
    # SEO
    meta_title = Column(String(200))
    meta_description = Column(String(500))
    og_image_url = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete (opcional)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="agent", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="agent", cascade="all, delete-orphan")


class Conversation(Base):
    """
    Modelo de Conversa
    """
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    
    # User Identification
    user_identifier = Column(String(200))
    session_id = Column(UUID(as_uuid=True), index=True)
    
    # Channel
    channel = Column(String(20), default="web")  # web, whatsapp, email
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    agent = relationship("Agent", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """
    Modelo de Mensagem
    """
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    
    # Content
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    
    # Metadata
    tokens = Column(Integer)
    cost = Column(Float)
    processing_time = Column(Float)
    model_used = Column(String(50))
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")


class Document(Base):
    """
    Modelo de Documento RAG
    """
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    
    # File Info
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50))
    file_size = Column(Integer)
    file_url = Column(String(500))
    
    # Processing Status
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    chunks_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    
    # Relationships
    agent = relationship("Agent", back_populates="documents")
