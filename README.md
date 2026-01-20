# 🤖 AI Agent Backend

Sistema backend de agentes conversacionais inteligentes com suporte a WhatsApp, Email e interface web.

## 📋 Features

- ✅ **Multi-agente**: Crie e gerencie múltiplos agentes de IA
- ✅ **Multi-canal**: WhatsApp, Email e Web Chat
- ✅ **LLM Integration**: OpenAI GPT-4o-mini (otimizado para custos)
- ✅ **RAG Support**: Sistema de documentos e busca semântica (Fase 2)
- ✅ **Conversas persistentes**: Histórico completo no PostgreSQL
- ✅ **Analytics**: Métricas de uso, custos e performance
- ✅ **API REST**: Totalmente documentada com FastAPI

## 🏗️ Stack Técnico

### Backend
- **FastAPI** - Framework web assíncrono
- **PostgreSQL** - Database principal
- **Redis** - Cache e filas
- **SQLAlchemy** - ORM
- **Alembic** - Migrations

### AI/ML
- **OpenAI GPT-4o-mini** - Modelo principal
- **OpenAI Embeddings** - Para RAG (Fase 2)
- **Qdrant** - Vector database (Fase 2)

### Integrações
- **Twilio** - WhatsApp Business API
- **MailerSend** - Envio de emails

### Deploy
- **Railway** - Hosting + CI/CD

## 📦 Instalação Local

### Pré-requisitos
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Git

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/ai-agent-backend.git
cd ai-agent-backend
```

### 2. Crie ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale dependências
```bash
pip install -r requirements.txt
```

### 4. Configure variáveis de ambiente
```bash
cp .env.example .env
# Edite .env com suas credenciais
```

**Variáveis obrigatórias:**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=sk-...
SECRET_KEY=seu-secret-key-aqui
ADMIN_PASSWORD=senha-segura-aqui
```

### 5. Execute migrations
```bash
alembic upgrade head
```

### 6. Inicie o servidor
```bash
uvicorn app.main:app --reload
```

Acesse: http://localhost:8000/docs

## 🚀 Deploy no Railway

### Preparação

1. **Crie repositório no GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/seu-usuario/ai-agent-backend.git
git push -u origin main
```

2. **Crie conta no Railway**: https://railway.app

### Deploy Automático

1. **Novo Projeto Railway**
   - Dashboard > New Project > Deploy from GitHub
   - Selecione seu repositório
   - Railway detectará automaticamente FastAPI

2. **Adicione PostgreSQL**
   - New > Database > PostgreSQL
   - Copie `DATABASE_URL` das variáveis

3. **Adicione Redis**
   - New > Database > Redis
   - Copie `REDIS_URL` das variáveis

4. **Configure Variáveis de Ambiente**
   
   No painel do serviço FastAPI, adicione:
   ```
   OPENAI_API_KEY=sk-...
   SECRET_KEY=generate-random-string-here
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=senha-segura
   ENVIRONMENT=production
   DEBUG=false
   ALLOWED_ORIGINS=https://seu-frontend.netlify.app
   ```

5. **Deploy**
   - Railway fará deploy automaticamente
   - Aguarde build concluir (~3-5 min)
   - Acesse URL gerada

### Verificar Deploy

```bash
# Health check
curl https://seu-app.railway.app/health

# Deve retornar:
{
  "status": "ok",
  "version": "1.0.0",
  "environment": "production"
}
```

## 📚 API Documentation

Após iniciar, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principais

#### Agents
```bash
# Criar agente
POST /api/agents/
{
  "name": "Vendedor Bot",
  "system_prompt": "Você é um vendedor...",
  "model": "gpt-4o-mini",
  "temperature": 0.7
}

# Listar agentes
GET /api/agents/

# Buscar agente
GET /api/agents/{agent_id}

# Atualizar agente
PUT /api/agents/{agent_id}

# Deletar agente
DELETE /api/agents/{agent_id}
```

#### Chat
```bash
# Enviar mensagem
POST /api/chat/
{
  "agent_id": "uuid",
  "user_identifier": "user@email.com",
  "message": "Olá!",
  "channel": "web"
}

# Listar conversas
GET /api/chat/conversations

# Buscar conversa com mensagens
GET /api/chat/conversations/{conversation_id}
```

## 🔧 Configuração Avançada

### Custos OpenAI

O sistema calcula automaticamente custos:

```python
# GPT-4o-mini (default)
Input: $0.15 / 1M tokens
Output: $0.60 / 1M tokens

# Custo médio por conversa: ~$0.001-0.005
```

### WhatsApp (Twilio)

1. Crie conta: https://www.twilio.com
2. Configure WhatsApp Sandbox
3. Adicione variáveis:
```env
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```
4. Configure webhook: `https://seu-app.railway.app/api/webhooks/whatsapp`

### Email (MailerSend)

1. Crie conta: https://www.mailersend.com
2. Verifique domínio
3. Adicione variáveis:
```env
MAILERSEND_API_KEY=...
MAILERSEND_FROM_EMAIL=noreply@yourdomain.com
```

## 🧪 Testes

```bash
# Executar testes
pytest

# Com coverage
pytest --cov=app tests/

# Apenas unitários
pytest tests/unit/
```

## 📊 Monitoramento

### Logs
```bash
# Railway
railway logs

# Local
tail -f logs/app.log
```

### Métricas

Acesse `/health` para status:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "environment": "production"
}
```

## 🔐 Segurança

- ✅ JWT para autenticação
- ✅ Variáveis sensíveis em .env
- ✅ CORS configurado
- ✅ Rate limiting (Railway)
- ✅ SQL injection protection (SQLAlchemy)

## 🛠️ Troubleshooting

### Build falha no Railway
```bash
# Erro: mailersend version not found
# Solução: requirements.txt já corrigido (2.0.0)
```

### Database connection error
```bash
# Verifique DATABASE_URL no Railway
# Deve ser: postgresql://...
```

### OpenAI API timeout
```bash
# Aumente timeout ou use modelo mais rápido
# gpt-4o-mini é o mais rápido
```

## 📈 Roadmap

### ✅ Fase 1 (2 semanas) - ATUAL
- [x] Core API
- [x] Sistema de agentes
- [x] Conversas persistentes
- [x] Integração OpenAI
- [x] Deploy Railway

### 🚧 Fase 2 (3-4 semanas)
- [ ] Sistema RAG (Qdrant)
- [ ] Upload de documentos
- [ ] WhatsApp webhook
- [ ] Email send/receive
- [ ] Analytics dashboard
- [ ] CRM integration

### 🔮 Fase 3 (6-8 semanas)
- [ ] Multi-tenancy
- [ ] Billing system
- [ ] White-label
- [ ] Marketplace
- [ ] Advanced analytics

## 💰 Custos Estimados

### Desenvolvimento (One-time)
- Setup: €1.800

### Operacional (Mensal - 5k msgs)
| Serviço | Custo |
|---------|-------|
| Railway Hosting | €20-40 |
| OpenAI API | €30-80 |
| Twilio WhatsApp | €20-50 |
| MailerSend | €0-25 |
| **Total** | **€70-195/mês** |

## 🤝 Contribuindo

1. Fork o projeto
2. Crie branch (`git checkout -b feature/amazing`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Pull Request

## 📄 Licença

Propriedade intelectual exclusiva do cliente.

## 📞 Suporte

- **Issues**: GitHub Issues
- **Email**: support@yourdomain.com
- **Docs**: https://docs.yourdomain.com

---

**Versão:** 1.0.0  
**Última atualização:** 2025-01-20  
**Status:** ✅ Production Ready
