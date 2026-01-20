# ⚡ QUICK START - AI Agent Backend

Guia rápido para ter o sistema funcionando em **10 minutos**.

## 🎯 Opção 1: Deploy Direto no Railway (Recomendado)

### 1. Preparar GitHub (2 min)

```bash
# Extrair projeto
tar -xzf ai-agent-backend.tar.gz
cd ai-agent-backend

# Criar repo GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main

# Criar repo em: https://github.com/new
# Depois:
git remote add origin https://github.com/SEU-USUARIO/ai-agent-backend.git
git push -u origin main
```

### 2. Deploy Railway (5 min)

1. **Acesse**: https://railway.app
2. **Login** com GitHub
3. **New Project** > Deploy from GitHub
4. Selecione `ai-agent-backend`
5. **Add PostgreSQL**: New > Database > PostgreSQL
6. **Add Redis**: New > Database > Redis

### 3. Configurar Variáveis (2 min)

No serviço FastAPI, adicione:

```env
# Copiado do PostgreSQL service
DATABASE_URL=postgresql://postgres:...

# Copiado do Redis service  
REDIS_URL=redis://default:...

# Sua OpenAI key
OPENAI_API_KEY=sk-proj-...

# Gere: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=sua-chave-aleatoria-32-chars

# Defina senha admin
ADMIN_PASSWORD=senha-segura-123

# Produção
ENVIRONMENT=production
DEBUG=false
ALLOWED_ORIGINS=*
```

### 4. Verificar (1 min)

```bash
# Health check
curl https://sua-app.railway.app/health

# Deve retornar: {"status":"ok"}
```

✅ **Pronto! Sistema funcionando em produção**

---

## 🖥️ Opção 2: Rodar Local (Desenvolvimento)

### 1. Setup (3 min)

```bash
# Extrair
tar -xzf ai-agent-backend.tar.gz
cd ai-agent-backend

# Criar venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

# Instalar
pip install -r requirements.txt
```

### 2. Database Local (2 min)

**Opção A: PostgreSQL + Redis local**
```bash
# Instale PostgreSQL e Redis
# Linux: sudo apt install postgresql redis-server
# Mac: brew install postgresql redis

# Crie database
createdb ai_agents
```

**Opção B: Use serviços Railway** (mais fácil)
- Crie PostgreSQL + Redis no Railway
- Use as URLs fornecidas

### 3. Configurar .env (1 min)

```bash
cp .env.example .env
nano .env  # ou code .env
```

Mínimo necessário:
```env
DATABASE_URL=postgresql://user:pass@localhost/ai_agents
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=sk-...
SECRET_KEY=qualquer-string-aqui
ADMIN_PASSWORD=admin123
```

### 4. Migrations e Run (2 min)

```bash
# Migrations
alembic upgrade head

# Iniciar
uvicorn app.main:app --reload
```

Acesse: http://localhost:8000/docs

---

## 🧪 Testar API

### 1. Criar Agente

```bash
curl -X POST http://localhost:8000/api/agents/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vendedor Bot",
    "system_prompt": "Você é um vendedor experiente e educado.",
    "model": "gpt-4o-mini",
    "temperature": 0.7
  }'
```

Copie o `id` retornado.

### 2. Enviar Mensagem

```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "COLE-O-ID-AQUI",
    "user_identifier": "teste@email.com",
    "message": "Olá! Preciso de ajuda."
  }'
```

Você receberá a resposta do agente! 🎉

---

## 📱 Próximos Passos

Agora que está funcionando:

1. **Frontend**: Deploy Next.js no Netlify
2. **WhatsApp**: Configure Twilio webhook
3. **Email**: Configure MailerSend
4. **Produção**: Ajuste variáveis de ambiente

## 🆘 Problemas?

### Build falha
- Verifique `requirements.txt` tem `mailersend==2.0.0`

### Database error
- Verifique `DATABASE_URL` está correto
- Teste: `railway run alembic upgrade head`

### OpenAI error
- Verifique `OPENAI_API_KEY` válida
- Teste em: https://platform.openai.com/playground

### Precisa ajuda?
- Leia `DEPLOY.md` para guia completo
- Leia `README.md` para documentação
- Abra issue no GitHub

---

**Tempo total**: ~10 minutos ⚡  
**Custo inicial**: $0 (Railway tem plano grátis)  
**Dificuldade**: ⭐⭐☆☆☆ (Fácil)
