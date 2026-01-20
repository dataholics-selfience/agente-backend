# 🚀 GUIA DE DEPLOY - RAILWAY

Este guia detalha o processo completo de deploy do AI Agent Backend no Railway.

## ✅ Checklist Pré-Deploy

Antes de fazer deploy, certifique-se de:

- [ ] Código está em repositório Git (GitHub/GitLab)
- [ ] Arquivo `.env.example` está atualizado
- [ ] Requirements.txt correto (mailersend==2.0.0)
- [ ] Migrations criadas e testadas localmente
- [ ] OpenAI API Key válida
- [ ] Todos testes passando (`pytest`)

## 📋 PASSO A PASSO

### 1. Preparar Repositório Git

```bash
# Inicializar git (se ainda não tiver)
git init

# Adicionar arquivos
git add .
git commit -m "Initial commit - AI Agent Backend v1.0.0"

# Criar repositório no GitHub
# Vá em: https://github.com/new

# Adicionar remote
git remote add origin https://github.com/SEU-USUARIO/ai-agent-backend.git
git branch -M main
git push -u origin main
```

### 2. Criar Conta Railway

1. Acesse: https://railway.app
2. Clique em "Start a New Project"
3. Login com GitHub
4. Autorize Railway

### 3. Criar Novo Projeto

**Opção A: Deploy from GitHub (Recomendado)**

1. Dashboard > "New Project"
2. Escolha "Deploy from GitHub repo"
3. Selecione o repositório: `ai-agent-backend`
4. Railway detectará automaticamente Python/FastAPI
5. Clique em "Deploy Now"

**Opção B: Deploy via CLI**

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Inicializar projeto
railway init

# Fazer deploy
railway up
```

### 4. Adicionar PostgreSQL Database

1. No seu projeto Railway, clique em "+ New"
2. Selecione "Database"
3. Escolha "PostgreSQL"
4. Railway criará automaticamente
5. Copie a `DATABASE_URL` das variáveis

### 5. Adicionar Redis

1. Clique em "+ New" novamente
2. Selecione "Database"
3. Escolha "Redis"
4. Railway criará automaticamente
5. Copie a `REDIS_URL` das variáveis

### 6. Configurar Variáveis de Ambiente

No painel do seu serviço FastAPI:

1. Clique na aba "Variables"
2. Clique em "RAW Editor"
3. Cole as variáveis:

```env
# Database (copiado do PostgreSQL service)
DATABASE_URL=postgresql://postgres:...@...railway.app:5432/railway

# Redis (copiado do Redis service)
REDIS_URL=redis://default:...@...railway.app:6379

# OpenAI (sua API key)
OPENAI_API_KEY=sk-proj-...

# Auth
SECRET_KEY=gere-uma-string-aleatoria-segura-aqui-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=sua-senha-segura-aqui

# Environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# CORS (adicione seu frontend depois)
ALLOWED_ORIGINS=http://localhost:3000,https://seu-frontend.netlify.app

# Opcional - Twilio WhatsApp
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_FROM=

# Opcional - MailerSend
MAILERSEND_API_KEY=
MAILERSEND_FROM_EMAIL=noreply@yourdomain.com
MAILERSEND_FROM_NAME=AI Agent
```

**Como gerar SECRET_KEY:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

Ou via CLI:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 7. Configurar Settings do Serviço

1. Clique na aba "Settings"
2. Verifique:
   - **Root Directory**: `/` (deixe vazio)
   - **Build Command**: Detectado automaticamente
   - **Start Command**: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. **Health Check**:
   - Path: `/health`
   - Timeout: 100

### 8. Deploy!

1. Railway iniciará build automaticamente
2. Acompanhe logs na aba "Deployments"
3. Aguarde ~3-5 minutos
4. Quando status = "Active" ✅, deploy concluído!

### 9. Verificar Deploy

Copie a URL gerada (formato: `https://ai-agent-backend-production-xxxx.up.railway.app`)

**Teste via curl:**
```bash
# Health check
curl https://sua-app.railway.app/health

# Deve retornar:
{
  "status": "ok",
  "version": "1.0.0",
  "environment": "production"
}
```

**Teste via navegador:**
```
https://sua-app.railway.app/docs
```

Você verá a documentação Swagger se DEBUG=true (não recomendado em produção).

### 10. Configurar Custom Domain (Opcional)

1. Settings > Networking
2. Custom Domain > Generate Domain
3. Ou adicione seu próprio domínio
4. Configure DNS (CNAME)

## 🔧 CONFIGURAÇÕES AVANÇADAS

### Auto-Deploy via Git

Railway faz auto-deploy quando você faz push:

```bash
# Fazer mudança
git add .
git commit -m "feat: nova funcionalidade"
git push

# Railway detecta e faz redeploy automaticamente
```

### Rollback

1. Vá em "Deployments"
2. Encontre deploy anterior
3. Clique em "⋮" > "Redeploy"

### Ver Logs em Tempo Real

```bash
# Via CLI
railway logs --follow

# Ou no dashboard: Aba "Deployments" > Clique no deploy > View Logs
```

### Configurar Alerts

1. Settings > Notifications
2. Adicione email ou webhook Discord/Slack
3. Configure eventos (deploy failed, service down, etc)

## 🐛 TROUBLESHOOTING

### Build Falha

**Erro: `mailersend==0.5.2 not found`**
```
Solução: Já corrigido no requirements.txt (versão 2.0.0)
```

**Erro: `No module named 'app'`**
```
Solução: Verifique Root Directory está "/" e não "/app"
```

**Erro: `DATABASE_URL not set`**
```
Solução: 
1. Verifique se PostgreSQL está rodando
2. Copie DATABASE_URL do service PostgreSQL
3. Cole nas variáveis do serviço FastAPI
```

### Runtime Errors

**Erro: `connection refused` PostgreSQL**
```
Solução:
1. Verifique se PostgreSQL service está "Active"
2. Verifique variável DATABASE_URL
3. Teste conexão: railway run python -c "from app.core.config import settings; print(settings.DATABASE_URL)"
```

**Erro: `OpenAI API key invalid`**
```
Solução:
1. Verifique OPENAI_API_KEY nas variáveis
2. Teste no OpenAI playground
3. Gere nova key se necessário
```

### Migration Issues

**Erro: `alembic upgrade head` failed**
```
Solução:
# Via Railway CLI
railway run alembic upgrade head

# Se der erro de revisão
railway run alembic stamp head
railway run alembic upgrade head
```

## 📊 MONITORAMENTO

### Métricas Railway

Railway oferece métricas built-in:
- CPU Usage
- Memory Usage
- Network I/O
- HTTP requests

Acesse: Service > Metrics

### Logs Estruturados

Ver logs:
```bash
railway logs --follow
railway logs --deployment [deployment-id]
```

### Health Checks

Railway checa `/health` automaticamente a cada 60s.

Se falhar 3x consecutivas, reinicia o serviço.

## 💰 CUSTOS RAILWAY

### Plano Developer (Grátis)
- $5 créditos/mês
- 512MB RAM
- 1GB storage
- **Suficiente para testes**

### Plano Hobby ($5/mês)
- $5 créditos inclusos
- Pay as you go
- 8GB RAM
- 100GB storage
- **Recomendado para produção pequena**

### Estimativa Mensal
```
Backend FastAPI: ~$10-15
PostgreSQL: ~$5-10
Redis: ~$3-5
---
Total: ~$18-30/mês
```

## 🔄 CI/CD AUTOMÁTICO

Railway já vem com CI/CD configurado!

**Workflow:**
1. Push para branch `main`
2. Railway detecta mudança
3. Build automático
4. Testa build
5. Se sucesso → Deploy
6. Se falha → Mantém versão anterior

**Configurar branch:**
```
Settings > Service > Branch: main
```

## ✅ CHECKLIST PÓS-DEPLOY

Após deploy bem-sucedido:

- [ ] Health check retorna `ok`
- [ ] Swagger docs acessível (se DEBUG=true)
- [ ] Criar primeiro agente via API
- [ ] Testar chat endpoint
- [ ] Verificar logs sem erros
- [ ] Configurar domínio customizado
- [ ] Adicionar frontend nas ALLOWED_ORIGINS
- [ ] Configurar WhatsApp webhook (se aplicável)
- [ ] Configurar Email (se aplicável)
- [ ] Backup database configurado
- [ ] Alerts configurados

## 🎯 PRÓXIMOS PASSOS

1. **Deploy Frontend** (Next.js no Netlify)
2. **Conectar Frontend ao Backend**
3. **Configurar integrações** (WhatsApp/Email)
4. **Testes end-to-end**
5. **Monitoramento em produção**
6. **Otimizar custos**

## 📞 SUPORTE

**Problemas com Railway:**
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway
- Twitter: @railway

**Problemas com o código:**
- GitHub Issues
- Email: dev@yourdomain.com

---

**Última atualização:** 2025-01-20  
**Versão do guia:** 1.0  
✅ **Testado e aprovado**
