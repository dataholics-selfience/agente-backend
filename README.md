# 🤖 AI Agent Backend v2.0

Sistema de Agentes Conversacionais Inteligentes com inicialização automática de banco de dados.

## ✨ Novidades da Versão 2.0

- ✅ **Inicialização automática do banco de dados** (sem necessidade de Railway CLI)
- ✅ **Deploy simplificado** (apenas conectar PostgreSQL e configurar variáveis)
- ✅ **2 agentes pré-configurados** (Vendedor Inteligente e Suporte Técnico)
- ✅ **API REST completa** com documentação Swagger automática
- ✅ **Cálculo automático de custos** por conversa
- ✅ **Health checks** para monitoramento

## 🚀 Deploy Rápido (5 minutos)

### 1. Criar conta no Railway
https://railway.app (grátis)

### 2. Criar novo projeto
- Clique em "New Project"
- Selecione "Deploy from GitHub repo"
- Conecte este repositório

### 3. Adicionar PostgreSQL
- No projeto, clique "+ New"
- Selecione "Database" → "Add PostgreSQL"

### 4. Configurar variáveis
Na aba "Variables" do serviço backend, adicione:

```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxx
PORT=8000
```

### 5. Deploy automático!
Railway fará deploy automaticamente. Aguarde ~2 minutos.

### 6. Testar
```bash
curl https://seu-projeto.up.railway.app/health
```

## 📚 Documentação Completa

Veja [RAILWAY_DEPLOY_GUIDE.md](RAILWAY_DEPLOY_GUIDE.md) para instruções detalhadas.

## 🔌 API Endpoints

### Health
- `GET /health` - Status geral
- `GET /health/db` - Status do banco de dados

### Agentes
- `GET /api/agents` - Listar todos
- `GET /api/agents/{id}` - Buscar por ID
- `POST /api/agents` - Criar novo
- `PUT /api/agents/{id}` - Atualizar
- `DELETE /api/agents/{id}` - Deletar

### Conversas
- `POST /api/chat` - Enviar mensagem
- `GET /api/conversations` - Listar conversas
- `GET /api/conversations/{id}` - Detalhes
- `GET /api/conversations/{id}/messages` - Histórico

## 💬 Exemplo de Uso

```bash
# Enviar mensagem para o agente
curl -X POST https://seu-projeto.up.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "00000000-0000-0000-0000-000000000001",
    "user_identifier": "cliente@email.com",
    "message": "Preciso de informações sobre produtos"
  }'
```

Resposta:
```json
{
  "conversation_id": "uuid-da-conversa",
  "response": "Olá! Fico feliz em ajudar com informações sobre nossos produtos...",
  "tokens": 45,
  "cost": 0.000123,
  "processing_time": 0.89
}
```

## 🏗️ Arquitetura

```
ai-agent-backend-v2/
├── main.py                          # Aplicação FastAPI
├── init_database.sql                # Script de inicialização do banco
├── app/
│   ├── api/
│   │   ├── health.py               # Health checks
│   │   ├── agents.py               # CRUD de agentes
│   │   └── conversations.py        # Gestão de conversas
│   ├── core/
│   │   └── database.py             # Conexão + Inicialização automática
│   ├── models/
│   │   └── __init__.py             # SQLAlchemy models
│   └── services/
│       ├── llm_service.py          # Integração OpenAI
│       └── conversation_service.py # Lógica de conversação
├── requirements.txt                # Dependências Python
├── Procfile                        # Comando de start
└── railway.json                    # Configuração Railway
```

## 🛠️ Stack Tecnológico

- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **LLM**: OpenAI GPT-4o-mini
- **Hosting**: Railway

## 💰 Custos Estimados

- **Railway**: €5-20/mês (database + hosting)
- **OpenAI API**: €0.15 por 1M tokens input (GPT-4o-mini)
- **Total para ~5.000 mensagens/mês**: €10-30/mês

## 📊 Features

- [x] API REST completa
- [x] Inicialização automática do banco
- [x] Múltiplos agentes
- [x] Histórico de conversas
- [x] Cálculo de custos
- [x] Health checks
- [x] Documentação Swagger
- [ ] RAG (Fase 2)
- [ ] WhatsApp (Fase 2)
- [ ] Email (Fase 2)

## 🐛 Troubleshooting

### Erro 500 ao chamar agente

1. Verifique logs no Railway
2. Confirme `DATABASE_URL` existe
3. Confirme `OPENAI_API_KEY` está correta
4. Teste: `curl https://seu-projeto.up.railway.app/health`

### Banco não inicializa

1. Veja logs do primeiro deploy
2. Procure por "🚀 Primeira execução detectada"
3. Se necessário, execute `init_database.sql` manualmente no Railway

## 📝 Changelog

### v2.0.0 (Janeiro 2025)
- Inicialização automática do banco de dados
- Removida dependência de Railway CLI
- Adicionados 2 agentes pré-configurados
- Melhorado sistema de health checks
- Simplificado processo de deployment

### v1.0.0
- Release inicial

## 📄 Licença

Propriedade do cliente. Código não pode ser reutilizado ou comercializado sem autorização.

## 👨‍💻 Suporte

Para suporte técnico, verifique:
1. Logs no Railway
2. Documentação Swagger: `/docs`
3. Health checks: `/health` e `/health/db`
