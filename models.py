from sqlalchemy import Column, String, Boolean, Float, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Agent(Base):
    __tablename__ = "agents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    avatar_url = Column(String(500))
    system_prompt = Column(Text, nullable=False)
    model = Column(String(50), default="gpt-4o-mini")
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer, default=1500)
    top_p = Column(Float, default=1.0)
    frequency_penalty = Column(Float, default=0.0)
    presence_penalty = Column(Float, default=0.0)
    rag_enabled = Column(Boolean, default=False)
    function_calling_enabled = Column(Boolean, default=False)
    whatsapp_enabled = Column(Boolean, default=False)
    whatsapp_number = Column(String(20))
    email_enabled = Column(Boolean, default=False)
    email_address = Column(String(200))
    web_enabled = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    allow_public_access = Column(Boolean, default=True)
    brand_color = Column(String(7), default="#4F46E5")
    welcome_message = Column(Text, default="Olá! Como posso ajudar?")
    input_placeholder = Column(String(100), default="Digite sua mensagem...")
    meta_title = Column(String(200))
    meta_description = Column(String(500))
    og_image_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    conversations = relationship("Conversation", back_populates="agent", cascade="all, delete-orphan")

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    user_identifier = Column(String(200))
    session_id = Column(UUID(as_uuid=True), index=True)
    channel = Column(String(20), default="web")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    agent = relationship("Agent", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    tokens = Column(Integer)
    cost = Column(Float)
    processing_time = Column(Float)
    model_used = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    conversation = relationship("Conversation", back_populates="messages")
