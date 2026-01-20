# 🤖 AI Agent Backend v3.0 - RAILWAY EDITION

**Backend de agentes de IA com SQL inline para funcionamento garantido no Railway**

## 🆕 Novidade v3.0

✅ **SQL embutido no código** - Não depende de arquivos externos  
✅ **Funciona 100% no Railway** - Testado e validado  
✅ **Inicialização automática** - Cria tabelas no primeiro uso  
✅ **2 agentes pré-configurados** - Prontos para usar  

---

## 🚀 DEPLOY RÁPIDO

```bash
# 1. Extrair
tar -xzf ai-agent-backend-v3.tar.gz
cd ai-agent-backend-v3

# 2. Git
git init && git add . && git commit -m "v3"

# 3. Railway
railway init
railway up

# 4. Adicionar PostgreSQL
railway add postgresql

# 5. Configurar
railway variables set OPENAI_API_KEY=sk-proj-xxx

# 6. Pronto!
```

---

## 📖 DOCUMENTAÇÃO

Leia o **README_RAILWAY.md** para:
- Guia passo a passo detalhado
- Solução de problemas
- Validação de funcionamento
- Alternativas de banco de dados

---

## 🔧 MUDANÇAS TÉCNICAS (v2 → v3)

### Problema Identificado
```
ERROR: relation "agents" does not exist
```

### Causa
Railway não conseguia ler arquivo `init_database.sql` externo durante startup.

### Solução
SQL agora está embutido direto em `app/core/database.py`:

```python
INIT_SQL = """
CREATE TABLE IF NOT EXISTS agents (...)
CREATE TABLE IF NOT EXISTS conversations (...)
...
"""

def init_database():
    conn.execute(text(INIT_SQL))  # ← Executa SQL inline
```

---

## ✅ VALIDAÇÃO

Após deploy, rode:

```bash
# 1. Health check
curl https://seu-projeto.up.railway.app/health

# 2. Listar agentes
curl https://seu-projeto.up.railway.app/api/agents

# 3. Conversar
curl -X POST https://seu-projeto.up.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "00000000-0000-0000-0000-000000000001",
    "user_identifier": "test@email.com",
    "message": "Olá!"
  }'
```

---

## 🛠️ Stack

- Python 3.11
- FastAPI 0.109
- PostgreSQL 15
- SQLAlchemy 2.0
- OpenAI GPT-4o-mini

---

## 📊 API Endpoints

- `GET /health` - Status do sistema
- `GET /api/agents` - Listar agentes
- `POST /api/agents` - Criar agente
- `POST /api/chat` - Enviar mensagem
- `GET /api/conversations` - Listar conversas
- Documentação completa: `/docs`

---

## 💰 Custos

- Railway: €5/mês (Starter)
- OpenAI: ~€0.10 por 1000 mensagens
- **Total**: ~€10-20/mês

---

## 🆘 Suporte

Se algo der errado, consulte **README_RAILWAY.md** seção "Solução de Problemas".

---

**Versão**: 3.0.0  
**Data**: 20/01/2025  
**Status**: ✅ Testado no Railway
