"""
FastAPI Application - AI Agent Backend
Versão FINAL para Railway
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import sys

from app.api import agents, conversations, health, public
from app.core.database import init_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle - inicializa banco automaticamente"""
    
    print("🚀 Iniciando aplicação...")
    
    try:
        init_database()
        print("✅ Sistema pronto!")
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)
    
    yield
    
    print("👋 Encerrando...")

app = FastAPI(
    title="AI Agent Backend - Dual Frontend",
    description="""
    Backend para Sistema de Agentes Conversacionais com Dual-Frontend:
    - **Admin API**: CRUD completo de agentes (autenticado)
    - **Public API**: Chat público via slug único (sem autenticação)
    
    ## Endpoints Principais
    
    ### Admin (Privado)
    - `GET /api/agents` - Lista todos agentes
    - `POST /api/agents` - Cria novo agente (gera slug automático)
    - `PUT /api/agents/{id}` - Atualiza agente
    - `DELETE /api/agents/{id}` - Desativa agente (soft delete)
    
    ### Public (Público)
    - `GET /api/public/agents/{slug}` - Dados públicos do agente
    - `POST /api/public/agents/{slug}/chat` - Envia mensagem
    - `GET /api/public/agents/{slug}/history/{session_id}` - Histórico
    
    ### Chat (Ambos)
    - `POST /api/chat` - Endpoint original de chat
    """,
    version="4.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(public.router, prefix="/api/public", tags=["Public Chat"])
app.include_router(agents.router, prefix="/api", tags=["Agents"])
app.include_router(conversations.router, prefix="/api", tags=["Conversations"])

@app.get("/")
async def root():
    return {
        "message": "AI Agent Backend - Dual Frontend",
        "version": "4.0.0",
        "status": "online",
        "docs": "/docs",
        "features": {
            "admin_api": "/api/agents",
            "public_chat": "/api/public/agents/{slug}/chat",
            "health": "/health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
