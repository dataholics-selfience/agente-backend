# Backend Agentes IA - Build v2.0.2 CLEAN

## ✅ O Que Foi Corrigido

- ❌ REMOVIDO: Campo `deleted_at` que causava erro
- ✅ CORS configurado corretamente
- ✅ Auth admin/admin123 funcionando
- ✅ Models simplificados

## 🚀 Deploy no Railway

### 1. Criar Novo Projeto

Railway → New Project → Deploy from GitHub

### 2. Configurar Variáveis

```
DATABASE_URL=<Railway PostgreSQL URL>
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
JWT_SECRET_KEY=<gerar chave aleatória de 64 chars>
OPENAI_API_KEY=sk-...
CORS_ORIGINS=https://agentes.genoibot.com,http://localhost:3000
```

### 3. Deploy Automático

Railway detecta automaticamente:
- `requirements.txt` → instala dependências
- `Procfile` → roda `uvicorn main:app`
- `runtime.txt` → Python 3.11

### 4. Verificar Logs

Deve aparecer:
```
🚀 Sistema de Agentes IA - Build v2.0.2 CLEAN
🔐 Admin: admin
🌐 CORS: https://agentes.genoibot.com,http://localhost:3000
✅ Database tables created
✅ Ready!
```

## 🧪 Testar

```bash
# Health check
curl https://SEU-DOMINIO.railway.app/health

# Login
curl -X POST https://SEU-DOMINIO.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Listar agentes
curl https://SEU-DOMINIO.railway.app/api/agents \
  -H "Authorization: Bearer SEU_TOKEN"
```

## 📦 Arquivos

```
backend/
├── main.py              # FastAPI app
├── database.py          # SQLAlchemy setup
├── models.py            # Agent model (SEM deleted_at!)
├── routes/
│   ├── auth.py          # Login JWT
│   └── agents.py        # CRUD agentes
├── requirements.txt     # Dependências
├── Procfile             # Railway start command
├── runtime.txt          # Python 3.11
└── .env.example         # Template de variáveis
```

## ⚠️ Importante

- **NÃO tem** campo `deleted_at` → sem erros de coluna!
- **CORS** já configurado para `agentes.genoibot.com`
- **Auth** simples com JWT
- **Database** criado automaticamente no startup

