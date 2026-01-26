"""
Pydantic Schemas for Request/Response Validation
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID


class AgentBase(BaseModel):
    """Base schema para Agent"""
    name: str = Field(..., min_length=1, max_length=200)
    slug: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    system_prompt: str = Field(..., min_length=10)
    model: str = Field(default="gpt-4o-mini")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1500, ge=1, le=4096)
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)
    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)
    rag_enabled: bool = Field(default=False)
    function_calling_enabled: bool = Field(default=False)
    whatsapp_enabled: bool = Field(default=False)
    whatsapp_number: Optional[str] = None
    email_enabled: bool = Field(default=False)
    email_address: Optional[str] = None
    web_enabled: bool = Field(default=True)
    is_active: bool = Field(default=True)
    allow_public_access: bool = Field(default=True)
    brand_color: str = Field(default="#4F46E5")
    welcome_message: str = Field(default="Olá! Como posso ajudar?")
    input_placeholder: str = Field(default="Digite sua mensagem...")
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    og_image_url: Optional[str] = None


class AgentCreate(AgentBase):
    """Schema para criar Agent"""
    pass


class AgentUpdate(BaseModel):
    """Schema para atualizar Agent (todos campos opcionais)"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    slug: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    system_prompt: Optional[str] = Field(None, min_length=10)
    model: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, ge=1, le=4096)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)
    frequency_penalty: Optional[float] = Field(None, ge=-2.0, le=2.0)
    presence_penalty: Optional[float] = Field(None, ge=-2.0, le=2.0)
    rag_enabled: Optional[bool] = None
    function_calling_enabled: Optional[bool] = None
    whatsapp_enabled: Optional[bool] = None
    whatsapp_number: Optional[str] = None
    email_enabled: Optional[bool] = None
    email_address: Optional[str] = None
    web_enabled: Optional[bool] = None
    is_active: Optional[bool] = None
    allow_public_access: Optional[bool] = None
    brand_color: Optional[str] = None
    welcome_message: Optional[str] = None
    input_placeholder: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    og_image_url: Optional[str] = None


class AgentResponse(BaseModel):
    """Schema para resposta de Agent"""
    id: UUID
    name: str
    slug: str
    description: Optional[str]
    avatar_url: Optional[str]
    system_prompt: str
    model: str
    temperature: float
    max_tokens: int
    top_p: float
    frequency_penalty: float
    presence_penalty: float
    rag_enabled: bool
    function_calling_enabled: bool
    whatsapp_enabled: bool
    whatsapp_number: Optional[str]
    email_enabled: bool
    email_address: Optional[str]
    web_enabled: bool
    is_active: bool
    allow_public_access: bool
    brand_color: str
    welcome_message: str
    input_placeholder: str
    meta_title: Optional[str]
    meta_description: Optional[str]
    og_image_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    public_url: str
    
    class Config:
        from_attributes = True


class AgentPublicResponse(BaseModel):
    """Schema para resposta pública de Agent (sem dados sensíveis)"""
    id: UUID
    slug: str
    name: str
    description: Optional[str]
    avatar_url: Optional[str]
    brand_color: str
    welcome_message: str
    input_placeholder: str
    meta_title: Optional[str]
    meta_description: Optional[str]
    og_image_url: Optional[str]
    
    class Config:
        from_attributes = True


class ChatMessage(BaseModel):
    """Schema para mensagem de chat"""
    message: str = Field(..., min_length=1, max_length=4000)
    session_id: Optional[str] = None
    user_identifier: Optional[str] = None


class ChatResponse(BaseModel):
    """Schema para resposta de chat"""
    conversation_id: UUID
    session_id: UUID
    response: str
    tokens: int
    cost: float
    processing_time: float
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Schema para login"""
    username: str
    password: str


class Token(BaseModel):
    """Schema para token JWT"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
