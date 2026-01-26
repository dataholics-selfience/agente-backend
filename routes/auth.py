"""
Authentication Routes
"""
from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
import logging

from schemas import LoginRequest, Token
from auth import authenticate_user, create_access_token, JWT_ACCESS_TOKEN_EXPIRE_MINUTES

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """
    Login com username/password
    
    Retorna JWT token válido por 7 dias
    """
    user = authenticate_user(login_data.username, login_data.password)
    
    if not user:
        logger.warning(f"Failed login attempt: {login_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Criar token
    access_token_expires = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in: {user['username']}")
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60  # segundos
    )
