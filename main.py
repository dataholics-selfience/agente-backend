from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes import auth, agents
import os

app = FastAPI(title="Agentes IA API", version="2.0.2")

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

# Routes
app.include_router(auth.router)
app.include_router(agents.router)

@app.on_event("startup")
async def startup():
    print("=" * 80)
    print("🚀 Sistema de Agentes IA - Build v2.0.2 CLEAN")
    print("=" * 80)
    print(f"🔐 Admin: {os.getenv('ADMIN_USERNAME', 'admin')}")
    print(f"🌐 CORS: {', '.join(CORS_ORIGINS)}")
    print("=" * 80)
    init_db()
    print("✅ Ready!")
    print("=" * 80)

@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.0.2"}
