"""
Pydantic Schemas para validação
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, List
from datetime import datetime
from uuid import UUID


# ===== CHAT SCHEMAS =====

class ChatRequest(BaseModel):
    """Request para enviar mensagem"""
    agent_id: UUID = Field(..., description="ID do agente")
    user_identifier: str = Field(..., description="Email, phone ou session ID")
    message: str = Field(..., min_length=1, description="Mensagem do usuário")
    channel: str = Field(default="web", description="Canal (web, whatsapp, email)")
    metadata: Optional[Dict] = Field(default=None, description="Metadata adicional")


class ChatResponse(BaseModel):
    """Response do chat"""
    conversation_id: str
    message_id: str
    response: str
    tokens_used: int
    cost: float
    agent: Dict


# ===== AGENT SCHEMAS =====

class AgentBase(BaseModel):
    """Base do agente"""
    name: str = Field(..., min_length=1, max_length=255)
    system_prompt: str = Field(..., min_length=10)
    model: str = Field(default="gpt-4o-mini")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    rag_enabled: bool = Field(default=False)
    whatsapp_enabled: bool = Field(default=False)
    email_enabled: bool = Field(default=False)
    metadata: Optional[Dict] = Field(default_factory=dict)


class AgentCreate(AgentBase):
    """Schema para criar agente"""
    pass


class AgentUpdate(BaseModel):
    """Schema para atualizar agente"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    system_prompt: Optional[str] = Field(None, min_length=10)
    model: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    rag_enabled: Optional[bool] = None
    whatsapp_enabled: Optional[bool] = None
    email_enabled: Optional[bool] = None
    is_active: Optional[bool] = None
    metadata: Optional[Dict] = None


class AgentResponse(AgentBase):
    """Response do agente"""
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ===== CONVERSATION SCHEMAS =====

class ConversationResponse(BaseModel):
    """Response de conversa"""
    id: str
    agent_id: str
    user_identifier: str
    channel: str
    status: str
    created_at: str
    updated_at: Optional[str] = None
    message_count: int
    messages: List[Dict]


# ===== MESSAGE SCHEMAS =====

class MessageResponse(BaseModel):
    """Response de mensagem"""
    id: str
    role: str
    content: str
    tokens_used: Optional[int] = None
    cost: Optional[float] = None
    created_at: str
