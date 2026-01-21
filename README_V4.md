# 🤖 AI Agent Backend - Dual Frontend

**Versão:** 4.0.0  
**Status:** ✅ Pronto para deploy  
**URL Produção:** https://web-production-9a8a1.up.railway.app

---

## 🎯 O que é?

Backend FastAPI para sistema de agentes conversacionais com **arquitetura dual-frontend**:

1. **Admin Panel** (Privado) - CRUD completo de agentes
2. **Public Chat** (Público) - URLs únicas por agente, sem autenticação

---

## ✨ Features v4.0.0

### 🆕 Novidades

- ✅ **URLs públicas únicas** - Cada agente tem sua URL compartilhável
- ✅ **Auto-geração de slug** - Cria automaticamente: `vendedor-dux`
- ✅ **Chat público** - SEM autenticação, via session ID
- ✅ **White-label** - Customização por agente (cores, mensagens)
- ✅ **SEO-ready** - Meta tags para cada agente
- ✅ **Soft delete** - Desativa agentes sem perder dados
- ✅ **15+ parâmetros LLM** - Controle total sobre comportamento

### 🔐 Segurança

- ✅ Endpoint público NÃO expõe `system_prompt`
- ✅ Validação de `is_active` e `allow_public_access`
- ✅ Session tracking sem trusted data

---

## 📁 Estrutura do Projeto

```
backend-railway-final-corrigido/
├── main.py                    # FastAPI app principal
├── requirements.txt           # Dependências Python
├── runtime.txt                # Python 3.11
├── Procfile                   # Railway start command
├── railway.json               # Railway config
│
├── app/
│   ├── api/
│   │   ├── agents.py         # CRUD de agentes (admin)
│   │   ├── public.py         # ⭐ NOVO - Chat público
│   │   ├── conversations.py  # Endpoint /chat original
│   │   └── health.py         # Health check
│   │
│   ├── core/
│   │   └── database.py       # SQLAlchemy setup
│   │
│   ├── models/
│   │   └── __init__.py       # Agent, Conversation, Message, Document
│   │
│   └── services/
│       ├── llm_service.py    # OpenAI wrapper
│       └── conversation_service.py  # Lógica de conversação
│
├── migration_v4.sql          # ⭐ NOVO - Migration obrigatória
├── API_DOCUMENTATION.md      # ⭐ NOVO - Docs completa
├── DEPLOY_V4.md              # ⭐ NOVO - Guia de deploy
└── CHANGELOG_V4.md           # ⭐ NOVO - Histórico de mudanças
```

---

## 🚀 Quick Start

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

```bash
# .env
DATABASE_URL=postgresql://user:pass@host:5432/db
OPENAI_API_KEY=sk-...
PORT=8000
```

### 3. Executar Migration

```bash
psql $DATABASE_URL -f migration_v4.sql
```

### 4. Rodar Localmente

```bash
python main.py
```

Acesse: http://localhost:8000/docs

---

## 📊 Endpoints Principais

### Admin API

```bash
# Listar agentes
GET /api/agents

# Criar agente (gera slug automático)
POST /api/agents
{
  "name": "Vendedor Dux",
  "system_prompt": "Você é um vendedor...",
  "temperature": 0.7
}

# Atualizar agente
PUT /api/agents/{id}

# Desativar agente (soft delete)
DELETE /api/agents/{id}
```

### Public API

```bash
# Obter dados públicos (SEM system_prompt)
GET /api/public/agents/{slug}

# Enviar mensagem
POST /api/public/agents/{slug}/chat
{
  "message": "Olá",
  "session_id": "optional-uuid"
}

# Histórico
GET /api/public/agents/{slug}/history/{session_id}
```

---

## 🧪 Testar

```bash
# Health check
curl https://web-production-9a8a1.up.railway.app/health

# Criar agente
curl -X POST https://web-production-9a8a1.up.railway.app/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Agent",
    "system_prompt": "You are helpful"
  }'

# Copie o slug retornado (ex: test-agent)

# Testar público
curl https://web-production-9a8a1.up.railway.app/api/public/agents/test-agent

# Chat público
curl -X POST https://web-production-9a8a1.up.railway.app/api/public/agents/test-agent/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello",
    "session_id": "test-123"
  }'
```

---

## 🚢 Deploy Railway

### Primeira vez

```bash
# 1. Login Railway
railway login

# 2. Link projeto
railway link

# 3. Configurar variáveis
railway variables set OPENAI_API_KEY=sk-...

# 4. Deploy
railway up
```

### Update (v3 → v4)

```bash
# 1. EXECUTE MIGRATION PRIMEIRO
railway run psql $DATABASE_URL -f migration_v4.sql

# 2. Deploy código
git add .
git commit -m "feat: dual-frontend v4.0.0"
git push railway main

# 3. Verificar
railway logs --tail 100
```

📖 **Guia completo:** [DEPLOY_V4.md](DEPLOY_V4.md)

---

## 📚 Documentação

### Completa
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Todos os endpoints com exemplos
- **[DEPLOY_V4.md](DEPLOY_V4.md)** - Guia de deploy e troubleshooting
- **[CHANGELOG_V4.md](CHANGELOG_V4.md)** - Histórico de mudanças

### Interativa
- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`

---

## 🔧 Stack Técnico

- **Framework:** FastAPI 0.115.6
- **Database:** PostgreSQL 15 (via Railway)
- **ORM:** SQLAlchemy 2.0.36
- **LLM:** OpenAI GPT-4o-mini
- **Hosting:** Railway
- **Python:** 3.11

---

## 📈 Próximos Passos

Após este deploy:

1. ✅ **Frontend Admin** - Criar interface de gerenciamento
2. ✅ **Frontend Public** - Criar interface de chat público
3. 🔜 **Autenticação JWT** - Proteger endpoints admin
4. 🔜 **Rate Limiting** - Limitar requisições públicas
5. 🔜 **RAG** - Upload de documentos
6. 🔜 **Analytics** - Métricas por agente

---

## 🐛 Troubleshooting

### Migration não funcionou
```bash
# Verificar colunas
railway run psql $DATABASE_URL -c "
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'agents' AND column_name = 'slug';"

# Se vazio, executar migration novamente
railway run psql $DATABASE_URL -f migration_v4.sql
```

### Erro 500 em /api/agents
```bash
# Preencher valores default para agentes antigos
railway run psql $DATABASE_URL -c "
UPDATE agents SET 
  brand_color = '#4F46E5',
  welcome_message = 'Olá! Como posso ajudar?',
  is_active = TRUE
WHERE brand_color IS NULL;"
```

### Build falha
```bash
# Limpar cache e rebuild
railway redeploy
```

---

## 📞 Suporte

**Problemas?**
1. Verifique logs: `railway logs`
2. Consulte [DEPLOY_V4.md](DEPLOY_V4.md)
3. Rollback se necessário (instruções no DEPLOY_V4.md)

---

## 📄 Licença

Propriedade exclusiva do cliente conforme especificação do projeto.

---

**🎉 v4.0.0 pronto para deploy!**  
Última atualização: 2025-01-21
