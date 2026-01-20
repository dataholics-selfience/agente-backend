"""
FastAPI Application - AI Agent Backend
Versão otimizada com inicialização automática do banco de dados
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import sys

# Importar rotas
from app.api import agents, conversations, health

# Importar inicializador do banco
from app.core.database import init_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events - executa na inicialização e shutdown"""
    
    # STARTUP: Inicializar banco de dados
    print("🚀 Iniciando aplicação...")
    
    try:
        init_database()
        print("✅ Banco de dados pronto!")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        sys.exit(1)
    
    yield
    
    # SHUTDOWN
    print("👋 Encerrando aplicação...")

# Criar aplicação FastAPI
app = FastAPI(
    title="AI Agent Backend",
    description="Sistema de Agentes Conversacionais Inteligentes",
    version="2.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(health.router, tags=["Health"])
app.include_router(agents.router, prefix="/api", tags=["Agents"])
app.include_router(conversations.router, prefix="/api", tags=["Conversations"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Agent Backend API",
        "version": "2.0.0",
        "status": "online",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
