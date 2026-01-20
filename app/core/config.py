"""
Configurações da aplicação
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Configurações gerais da aplicação"""
    
    # App
    APP_NAME: str = "Agent Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/agentdb"
    )
    
    # Redis
    REDIS_URL: str = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379"
    )
    
    # Qdrant
    QDRANT_URL: str = os.getenv(
        "QDRANT_URL",
        "http://localhost:6333"
    )
    QDRANT_API_KEY: Optional[str] = None
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Groq (fallback)
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    
    # Anthropic (opcional)
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Twilio
    TWILIO_ACCOUNT_SID: Optional[str] = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: Optional[str] = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_WHATSAPP_FROM: Optional[str] = os.getenv("TWILIO_WHATSAPP_FROM")
    
    # MailerSend
    MAILERSEND_API_KEY: Optional[str] = os.getenv("MAILERSEND_API_KEY")
    MAILERSEND_FROM_EMAIL: Optional[str] = os.getenv("MAILERSEND_FROM_EMAIL")
    MAILERSEND_FROM_NAME: Optional[str] = os.getenv("MAILERSEND_FROM_NAME")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.railway.app",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
