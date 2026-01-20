from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID


# Agent Schemas
class AgentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    system_prompt: str = Field(..., min_length=1)
    model: str = Field(default="gpt-4o-mini")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    rag_enabled: bool = False
    whatsapp_enabled: bool = False
    email_enabled: bool = False


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    system_prompt: Optional[str] = Field(None, min_length=1)
    model: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    rag_enabled: Optional[bool] = None
    whatsapp_enabled: Optional[bool] = None
    email_enabled: Optional[bool] = None
    status: Optional[str] = None


class AgentResponse(AgentBase):
    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Message Schemas
class MessageBase(BaseModel):
    role: str
    content: str


class MessageCreate(MessageBase):
    conversation_id: Optional[UUID] = None


class MessageResponse(MessageBase):
    id: UUID
    conversation_id: UUID
    tokens: int
    cost: float
    processing_time: float
    extra_data: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Conversation Schemas
class ConversationBase(BaseModel):
    user_identifier: str
    channel: str = "web"


class ConversationCreate(ConversationBase):
    agent_id: UUID


class ConversationResponse(ConversationBase):
    id: UUID
    agent_id: UUID
    status: str
    extra_data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ConversationWithMessages(ConversationResponse):
    messages: List[MessageResponse] = []


# Chat Schemas
class ChatRequest(BaseModel):
    agent_id: UUID
    user_identifier: str
    message: str
    channel: str = "web"
    conversation_id: Optional[UUID] = None


class ChatResponse(BaseModel):
    conversation_id: UUID
    message: MessageResponse
    agent_response: MessageResponse


# Document Schemas
class DocumentBase(BaseModel):
    filename: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None


class DocumentCreate(DocumentBase):
    agent_id: UUID


class DocumentResponse(DocumentBase):
    id: UUID
    agent_id: UUID
    status: str
    chunks_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


# Health Check
class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str


# Analytics
class AnalyticsOverview(BaseModel):
    total_conversations: int
    total_messages: int
    total_cost: float
    average_response_time: float
    conversations_by_channel: Dict[str, int]
    messages_by_day: Dict[str, int]


__all__ = [
    "AgentBase",
    "AgentCreate",
    "AgentUpdate",
    "AgentResponse",
    "MessageBase",
    "MessageCreate",
    "MessageResponse",
    "ConversationBase",
    "ConversationCreate",
    "ConversationResponse",
    "ConversationWithMessages",
    "ChatRequest",
    "ChatResponse",
    "DocumentBase",
    "DocumentCreate",
    "DocumentResponse",
    "Token",
    "LoginRequest",
    "HealthResponse",
    "AnalyticsOverview",
]
