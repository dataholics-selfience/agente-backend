# 🚀 Backend Agentes IA - v3.0.0-FIXED

## ✅ O Que Foi Corrigido

- ✅ Model `Agent` **inclui** campo `deleted_at`
- ✅ Database schema **cria** coluna `deleted_at` automaticamente
- ✅ Soft delete funcionando
- ✅ CORS configurado
- ✅ Auth admin/admin123

## 🔧 Deploy no Railway

### 1. Criar Novo Projeto

Railway → **New Project** → **Deploy from GitHub** (ou arrastar pasta)

### 2. Adicionar PostgreSQL

**+ New** → **Database** → **Add PostgreSQL**

### 3. Configurar Variáveis

```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
JWT_SECRET_KEY=a7f9d8c3b2e1f4a6d9c8b7e6f5a4d3c2b1e9f8a7d6c5b4e3f2a1d9c8b7e6f5a4d3
OPENAI_API_KEY=sk-proj-SUA_CHAVE_AQUI
CORS_ORIGINS=https://agentes.genoibot.com,http://localhost:3000
```

### 4. Deploy Automático

Railway detecta `Procfile` e faz deploy (~2min)

### 5. Verificar Logs

Deve aparecer:
```
🚀 Sistema de Agentes IA - Build v3.0.0-FIXED
✅ Database tables created WITH deleted_at column
✅ Ready!
```

## 🧪 Testar

```bash
curl https://SEU-DOMINIO.railway.app/health
# {"status":"ok","version":"3.0.0-FIXED"}
```

## 📦 Estrutura

```
backend/
├── main.py           # FastAPI app
├── database.py       # SQLAlchemy
├── models.py         # Agent (COM deleted_at!)
├── routes/
│   ├── auth.py       # Login
│   └── agents.py     # CRUD (soft delete)
├── requirements.txt
├── Procfile
├── runtime.txt
└── README.md
```
