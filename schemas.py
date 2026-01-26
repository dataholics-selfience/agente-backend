from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class AgentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    slug: Optional[str] = None
    description: Optional[str] = None
    system_prompt: str = Field(..., min_length=10)
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 1500
    is_active: bool = True
    allow_public_access: bool = True
    brand_color: str = "#4F46E5"
    welcome_message: str = "Olá! Como posso ajudar?"

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    is_active: Optional[bool] = None

class AgentResponse(AgentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    public_url: str
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    conversation_id: UUID
    session_id: UUID
    response: str
    tokens: int
    cost: float

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
