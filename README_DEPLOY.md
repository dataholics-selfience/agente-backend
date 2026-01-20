# 🚂 Backend - Guia de Deploy no Railway

## ✅ Pré-requisitos
- Conta Railway criada
- Chave OpenAI configurada

## 📦 Deploy Automático

### 1. Criar Novo Projeto
1. Aceda a https://railway.app
2. Clique em "New Project"
3. Escolha "Deploy from GitHub repo"

### 2. Adicionar Serviços

**A) PostgreSQL:**
- New → Database → PostgreSQL
- Copiar `DATABASE_URL`

**B) Redis:**
- New → Database → Redis
- Copiar `REDIS_URL`

**C) Qdrant:**
- New → Empty Service
- Nome: `qdrant`
- Docker Image: `qdrant/qdrant:latest`
- Port: `6333`

**D) Backend:**
- New → GitHub Repo
- **Root Directory:** `backend`
- Railway detecta Python automaticamente

### 3. Configurar Variáveis de Ambiente

No serviço Backend, adicionar:

```
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
QDRANT_URL=http://qdrant.railway.internal:6333
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
SECRET_KEY=sua-chave-secreta-min-32-chars
DEBUG=False
```

### 4. Configurar Build

**Build Command:**
```bash
pip install -r requirements.txt && alembic upgrade head
```

**Start Command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 5. Deploy!
- Clique em "Deploy"
- Aguarde 3-5 minutos
- Copie a URL pública

## ✅ Verificar

1. Aceda: `https://seu-app.railway.app/health`
2. Deve retornar: `{"status":"healthy"}`
3. Docs: `https://seu-app.railway.app/docs`

## 🆘 Problemas?

**Build falha:**
- Verifique se Root Directory = `backend`
- Veja os logs do build

**Erro 500:**
- Verifique variáveis de ambiente
- Veja logs: Serviço → View Logs
