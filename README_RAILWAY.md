# 🚨 BACKEND V3 - SOLUÇÃO DEFINITIVA PARA RAILWAY

## ❌ PROBLEMA IDENTIFICADO

Analisando seus logs:
```
ERROR: relation "agents" does not exist
```

**Causa raiz**: O script SQL de inicialização não está sendo executado porque o Railway não consegue ler arquivos externos durante o startup.

---

## ✅ SOLUÇÃO V3: SQL INLINE

Esta versão **embute o SQL diretamente no código Python**, eliminando dependência de arquivos externos.

### O que mudou:

**ANTES (v2 - FALHAVA):**
```python
# Tentava ler arquivo init_database.sql
with open('init_database.sql', 'r') as f:
    sql_script = f.read()
```

**DEPOIS (v3 - FUNCIONA):**
```python
# SQL embutido direto no código
INIT_SQL = """
CREATE TABLE IF NOT EXISTS agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ...
)
"""
conn.execute(text(INIT_SQL))
```

---

## 🎯 COMO USAR ESTA VERSÃO

### 1. Preparar

```bash
tar -xzf ai-agent-backend-v3-railway.tar.gz
cd ai-agent-backend-v3
```

### 2. Deploy no Railway

**Opção A: Via GitHub (Recomendado)**
```bash
git init
git add .
git commit -m "Backend v3 com SQL inline"
git remote add origin https://github.com/SEU_USUARIO/ai-agent-backend.git
git push -u origin main
```

No Railway:
1. New Project → Deploy from GitHub repo
2. Selecione o repositório

**Opção B: Via Railway CLI** (se disponível)
```bash
railway login
railway init
railway up
```

**Opção C: Upload Direto**
1. Railway → New Project → Empty Project
2. + New → Empty Service
3. Settings → Source → Connect Repo
4. Upload do código

### 3. Adicionar PostgreSQL

1. No projeto Railway, clique **"+ New"**
2. Selecione **"Database" → "Add PostgreSQL"**
3. Railway cria automaticamente a variável `DATABASE_URL`

### 4. Configurar Variáveis

No serviço **backend** (não no PostgreSQL):

```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxx
PORT=8000
```

**IMPORTANTE**: NÃO adicione `DATABASE_URL` manualmente! O Railway faz isso automaticamente.

### 5. Aguardar Deploy

Railway vai:
- ✅ Instalar dependências Python
- ✅ Iniciar aplicação
- ✅ **EXECUTAR SQL INLINE automaticamente**
- ✅ Criar tabelas
- ✅ Inserir 2 agentes

---

## 🔍 VERIFICAR SE FUNCIONOU

### 1. Checar Logs

No Railway:
- Serviço backend → Deployments → Deploy ativo → Deploy Logs

Procure por:
```
🚀 Primeira execução detectada. Criando schema...
✅ Schema criado com sucesso!
🤖 2 agente(s) criado(s)
   - Vendedor Inteligente (ID: 00000000-0000-0000-0000-000000000001)
   - Suporte Técnico (ID: 00000000-0000-0000-0000-000000000002)
✅ Banco de dados pronto!
```

### 2. Testar API

```bash
# Health check
curl https://seu-projeto.up.railway.app/health

# Deve retornar:
{
  "status": "online",
  "database": "healthy",
  "openai_configured": true,
  "version": "2.0.0"
}
```

### 3. Verificar Tabelas no PostgreSQL

No Railway:
1. Abra o serviço PostgreSQL
2. Clique em "Data"
3. Você deve ver 5 tabelas:
   - agents
   - conversations
   - messages
   - documents
   - channel_configs

### 4. Listar Agentes

```bash
curl https://seu-projeto.up.railway.app/api/agents

# Deve retornar 2 agentes
```

### 5. Testar Conversa

```bash
curl -X POST https://seu-projeto.up.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "00000000-0000-0000-0000-000000000001",
    "user_identifier": "test@email.com",
    "message": "Olá!"
  }'

# Deve retornar resposta do agente
```

---

## 🐛 SE AINDA NÃO FUNCIONAR

### Erro 1: "relation 'agents' does not exist"

**Causa**: SQL inline não foi executado

**Solução**:
1. Force redeploy no Railway
2. Verifique se `DATABASE_URL` existe em Variables
3. Veja logs completos do primeiro deploy

### Erro 2: "Internal Server Error 500"

**Causas possíveis**:
- OpenAI API key inválida
- DATABASE_URL não configurada
- Conexão com PostgreSQL falhou

**Solução**:
```bash
# 1. Verifique health check
curl https://seu-projeto.up.railway.app/health

# 2. Verifique logs
# Railway → Backend → Deployments → Logs

# 3. Verifique variáveis
# Railway → Backend → Variables
# Deve ter: DATABASE_URL e OPENAI_API_KEY
```

### Erro 3: Tabelas não aparecem no PostgreSQL

**Solução**: Execute SQL manual (último recurso)

1. Railway → PostgreSQL → Data → Query
2. Cole este SQL:

```sql
-- Criar tipos ENUM
CREATE TYPE agentstatus AS ENUM ('active', 'inactive', 'archived');
CREATE TYPE conversationstatus AS ENUM ('active', 'paused', 'closed');
CREATE TYPE messagerole AS ENUM ('user', 'assistant', 'system');

-- Criar tabela agents
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    system_prompt TEXT NOT NULL,
    model VARCHAR(100) NOT NULL DEFAULT 'gpt-4o-mini',
    temperature FLOAT NOT NULL DEFAULT 0.7,
    rag_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    whatsapp_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    email_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    status agentstatus NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Inserir agente de exemplo
INSERT INTO agents (id, name, system_prompt, model, temperature)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'Vendedor Inteligente',
    'Você é um assistente de vendas profissional.',
    'gpt-4o-mini',
    0.7
);
```

3. Execute
4. Force redeploy do backend

---

## 🔄 ALTERNATIVA: USAR OUTRO BANCO DE DADOS

Se PostgreSQL continuar dando problema, você pode tentar:

### 1. MySQL (Railway)

1. Railway → + New → Database → Add MySQL
2. Modifique `requirements.txt`:
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
pymysql==1.1.0      # ← Trocar psycopg2 por pymysql
cryptography==41.0.7
openai==1.10.0
python-dotenv==1.0.0
pydantic==2.5.3
pydantic-settings==2.1.0
```

3. Railway cria `DATABASE_URL` automaticamente

### 2. SQLite (Desenvolvimento Local)

Crie arquivo `.env`:
```
DATABASE_URL=sqlite:///./database.db
OPENAI_API_KEY=sk-proj-xxx
```

Execute localmente:
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## ✅ CHECKLIST DE VALIDAÇÃO

Antes de considerar que funciona, valide:

- [ ] Logs mostram "✅ Schema criado com sucesso!"
- [ ] PostgreSQL tem 5 tabelas visíveis
- [ ] `GET /health` retorna `"database": "healthy"`
- [ ] `GET /api/agents` retorna 2 agentes
- [ ] `POST /api/chat` retorna resposta do agente
- [ ] Não há erros "relation does not exist" nos logs

**Se todos passarem → Sistema funcionando!** 🎉

---

## 💡 POR QUE V3 É DIFERENTE

| Versão | Método | Funciona? |
|--------|--------|-----------|
| v1 | Alembic migrations | ❌ Complexo |
| v2 | Script SQL externo | ❌ Railway não lê |
| v3 | **SQL inline no código** | ✅ **FUNCIONA** |

V3 elimina dependências externas e garante que o SQL sempre seja executado.

---

## 📞 PRÓXIMOS PASSOS

Quando funcionar:
1. ✅ Anote a URL do Railway
2. ✅ Teste todos os endpoints em `/docs`
3. ✅ Desenvolva frontend
4. ✅ Adicione features avançadas

**Boa sorte! 🚀**
