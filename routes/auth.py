from fastapi import APIRouter, HTTPException
from schemas import LoginRequest, Token
from auth import authenticate_user, create_access_token, JWT_EXPIRE_MINUTES

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(data: LoginRequest):
    user = authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({"sub": user["username"]})
    return Token(access_token=token, expires_in=JWT_EXPIRE_MINUTES * 60)
