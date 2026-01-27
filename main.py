from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes import auth, agents
import os

app = FastAPI(title="Agentes IA API", version="3.0.0-FIXED")

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "https://agentes.genoibot.com,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(auth.router)
app.include_router(agents.router)

@app.on_event("startup")
async def startup():
    print("=" * 80)
    print("🚀 Sistema de Agentes IA - Build v3.0.0-FIXED")
    print("=" * 80)
    print(f"🔐 Admin: {os.getenv('ADMIN_USERNAME', 'admin')}")
    print(f"🌐 CORS: {', '.join(CORS_ORIGINS)}")
    print("=" * 80)
    init_db()
    print("✅ Ready! (with deleted_at column)")
    print("=" * 80)

@app.get("/health")
async def health():
    return {"status": "ok", "version": "3.0.0-FIXED"}
