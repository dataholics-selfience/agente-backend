"""
FastAPI Application - AI Agent Backend
Versão FINAL para Railway
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import sys

from app.api import agents, conversations, health
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
    title="AI Agent Backend",
    version="3.0.0",
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
app.include_router(agents.router, prefix="/api", tags=["Agents"])
app.include_router(conversations.router, prefix="/api", tags=["Conversations"])

@app.get("/")
async def root():
    return {
        "message": "AI Agent Backend",
        "version": "3.0.0",
        "status": "online",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
