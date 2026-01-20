from fastapi import APIRouter
from .agents import router as agents_router
from .chat import router as chat_router

api_router = APIRouter(prefix="/api")

api_router.include_router(agents_router)
api_router.include_router(chat_router)

__all__ = ["api_router"]
