import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import init_db
from routes import agents, public, auth

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("="*80)
    logger.info("🚀 Sistema de Agentes IA - Build v2.0.1")
    logger.info("="*80)
    try:
        init_db()
        logger.info("✅ Database OK")
    except Exception as e:
        logger.error(f"❌ Database error: {e}")
        raise
    
    cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000")
    logger.info(f"🌐 CORS: {cors_origins}")
    logger.info("✅ Ready!")
    logger.info("="*80)
    yield
    logger.info("👋 Shutdown")

app = FastAPI(
    title="Agentes IA API",
    version="2.0.1",
    lifespan=lifespan
)

cors_str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
cors_origins = [o.strip() for o in cors_str.split(",")]

logger.info(f"🔐 CORS Origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/")
async def root():
    return {"service": "Agentes IA API", "version": "2.0.1", "status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "2.0.1"}

app.include_router(auth.router)
app.include_router(agents.router)
app.include_router(public.router)
