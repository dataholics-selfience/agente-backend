# 🚀 GUIA DE DEPLOYMENT NO RAILWAY
## Backend AI Agent - Versão 2.0 (Com Inicialização Automática)

---

## 📋 PRÉ-REQUISITOS

1. **Conta no Railway**: https://railway.app (grátis)
2. **OpenAI API Key**: https://platform.openai.com/api-keys
3. **Repositório Git** (opcional, mas recomendado)

---

## 🎯 MÉTODO 1: DEPLOYMENT VIA GITHUB (RECOMENDADO)

### Passo 1: Preparar Repositório Git

```bash
# No seu computador, dentro da pasta ai-agent-backend-v2/

# Inicializar Git
git init

# Adicionar arquivos
git add .

# Commit inicial
git commit -m "Initial commit - AI Agent Backend v2"

# Criar repositório no GitHub e conectar
git remote add origin https://github.com/SEU_USUARIO/ai-agent-backend.git
git branch -M main
git push -u origin main
```

### Passo 2: Criar Projeto no Railway

1. Acesse https://railway.app
2. Clique em **"New Project"**
3. Selecione **"Deploy from GitHub repo"**
4. Autorize Railway a acessar seu GitHub
5. Selecione o repositório `ai-agent-backend`

### Passo 3: Adicionar PostgreSQL

1. No projeto Railway, clique em **"+ New"**
2. Selecione **"Database"** → **"Add PostgreSQL"**
3. Railway criará automaticamente a variável `DATABASE_URL`

### Passo 4: Configurar Variáveis de Ambiente

No serviço do backend (não no PostgreSQL):

1. Clique na aba **"Variables"**
2. Adicione as seguintes variáveis:

```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxx
PORT=8000
```

**IMPORTANTE**: Não adicione `DATABASE_URL` manualmente! O Railway faz isso automaticamente quando você conecta o PostgreSQL.

### Passo 5: Deploy Automático

O Railway detectará automaticamente:
- `requirements.txt` (instalará dependências)
- `Procfile` (comando de inicialização)
- `railway.json` (configurações)

O deploy começará automaticamente!

### Passo 6: Verificar Logs

1. Clique na aba **"Deployments"**
2. Clique no deployment ativo
3. Veja os logs em **"Build Logs"** e **"Deploy Logs"**

Você deve ver:

```
🚀 Iniciando aplicação...
🔍 Verificando estado do banco de dados...
🚀 Primeira execução detectada. Criando schema...
✅ Schema criado com sucesso!
🤖 2 agente(s) criado(s)
✅ Banco de dados pronto!
```

### Passo 7: Testar API

Railway gera uma URL automática: `https://seu-projeto.up.railway.app`

Teste endpoints:

```bash
# Health check
curl https://seu-projeto.up.railway.app/health

# Listar agentes
curl https://seu-projeto.up.railway.app/api/agents

# Enviar mensagem
curl -X POST https://seu-projeto.up.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "00000000-0000-0000-0000-000000000001",
    "user_identifier": "test@email.com",
    "message": "Olá, preciso de ajuda"
  }'
```

---

## 🎯 MÉTODO 2: DEPLOYMENT VIA ARQUIVO ZIP

Se não quiser usar Git:

### Passo 1: Preparar Arquivos

1. Compacte a pasta `ai-agent-backend-v2/` em um arquivo ZIP
2. Faça upload para Google Drive, Dropbox, ou qualquer lugar

### Passo 2: Deploy Manual

1. No Railway, clique em **"New Project"**
2. Selecione **"Empty Project"**
3. Clique em **"+ New"** → **"Empty Service"**
4. Na aba **"Settings"**, role até **"Source"**
5. Clique em **"Connect Repo"** e faça upload dos arquivos

### Passo 3: Siga Passos 3-7 do Método 1

---

## 🔧 SOLUÇÃO DE PROBLEMAS

### ❌ Erro: "Internal Server Error 500"

**Causa**: Banco não inicializado ou OpenAI key inválida

**Solução**:

1. Verifique logs no Railway
2. Confirme que `DATABASE_URL` existe (aba Variables)
3. Confirme que `OPENAI_API_KEY` está correta
4. Force re-deploy: aba "Deployments" → "Redeploy"

### ❌ Erro: "syntax error at or near 'gpt'"

**Causa**: Usando o script SQL antigo

**Solução**: Use o novo `init_database.sql` incluído neste pacote

### ❌ Agente não responde

**Verifique**:

```bash
# 1. Health check
curl https://seu-projeto.up.railway.app/health

# Deve retornar:
{
  "status": "online",
  "database": "healthy",
  "openai_configured": true,
  "version": "2.0.0"
}

# 2. Detalhes do banco
curl https://seu-projeto.up.railway.app/health/db

# Deve retornar:
{
  "status": "healthy",
  "agents": 2,
  "conversations": 0,
  "messages": 0
}
```

### ❌ Banco não cria tabelas

**Solução manual** (último recurso):

1. No Railway, abra o PostgreSQL
2. Clique em **"Data"** → **"Query"**
3. Cole o conteúdo de `init_database.sql`
4. Execute
5. Force re-deploy do backend

---

## 📊 VERIFICAÇÃO PÓS-DEPLOY

### 1. Testar Health Check

```bash
curl https://seu-projeto.up.railway.app/health
```

Esperado:
```json
{
  "status": "online",
  "database": "healthy",
  "openai_configured": true,
  "version": "2.0.0"
}
```

### 2. Listar Agentes Criados

```bash
curl https://seu-projeto.up.railway.app/api/agents
```

Esperado: Array com 2 agentes (Vendedor Inteligente, Suporte Técnico)

### 3. Testar Conversa

```bash
curl -X POST https://seu-projeto.up.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "00000000-0000-0000-0000-000000000001",
    "user_identifier": "teste@email.com",
    "message": "Olá!"
  }'
```

Esperado:
```json
{
  "conversation_id": "uuid-da-conversa",
  "response": "Olá! Como posso ajudar você hoje?",
  "tokens": 45,
  "cost": 0.000123,
  "processing_time": 0.89
}
```

---

## 🎉 PRONTO!

Se todos os testes acima passarem, seu backend está funcionando perfeitamente!

**Próximos passos**:
1. Anotar a URL do Railway
2. Usar essa URL no frontend
3. Começar a desenvolver funcionalidades avançadas

---

## 📞 SUPORTE

Se tiver problemas:
1. Verifique logs no Railway (aba "Deployments")
2. Teste health check endpoints
3. Confirme variáveis de ambiente
4. Force re-deploy se necessário

**URL da documentação automática**: `https://seu-projeto.up.railway.app/docs`
