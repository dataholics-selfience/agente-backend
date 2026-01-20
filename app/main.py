from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api import api_router
from app import __version__


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"Starting AI Agent Backend v{__version__}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug mode: {settings.DEBUG}")
    
    yield
    
    # Shutdown
    print("Shutting down AI Agent Backend")


app = FastAPI(
    title="AI Agent Backend",
    description="Sistema de agentes conversacionais inteligentes",
    version=__version__,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router)


# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "version": __version__,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/")
async def root():
    return {
        "message": "AI Agent Backend API",
        "version": __version__,
        "docs": "/docs" if settings.DEBUG else "disabled",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
