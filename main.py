"""
Main FastAPI Application - Sistema de Agentes IA
"""
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import init_db
from routes import agents, public, auth

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events
    """
    # Startup
    logger.info("🚀 Iniciando aplicação...")
    logger.info("🔍 Verificando banco de dados...")
    
    try:
        init_db()
        logger.info("✅ Database inicializado")
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar database: {e}")
        raise
    
    logger.info("✅ Sistema pronto!")
    
    yield
    
    # Shutdown
    logger.info("👋 Encerrando aplicação...")


# Create FastAPI app
app = FastAPI(
    title="Sistema de Agentes IA",
    description="Plataforma de agentes conversacionais inteligentes",
    version="1.0.0",
    lifespan=lifespan
)


# CORS Configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health Check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "agentes-ia-backend",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sistema de Agentes IA - API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Include routers
app.include_router(auth.router)      # /api/auth
app.include_router(agents.router)    # /api/agents
app.include_router(public.router)    # /api/public


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
