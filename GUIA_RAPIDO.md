# ⚡ GUIA RÁPIDO - DEPLOYMENT EM 5 MINUTOS

## 📦 O QUE VOCÊ TEM

Um backend completo de agentes de IA que:
- ✅ Cria tabelas automaticamente no primeiro uso
- ✅ Já vem com 2 agentes pré-configurados
- ✅ Calcula custos automaticamente
- ✅ Funciona direto no Railway SEM Railway CLI

---

## 🚀 PASSO A PASSO

### 1️⃣ PREPARAR CÓDIGO (SEU COMPUTADOR)

```bash
# Extrair o arquivo
tar -xzf ai-agent-backend-v2.tar.gz
cd ai-agent-backend-v2

# Inicializar Git
git init
git add .
git commit -m "Backend AI Agent v2"

# Conectar ao GitHub (crie um repositório novo no GitHub primeiro)
git remote add origin https://github.com/SEU_USUARIO/ai-agent-backend.git
git branch -M main
git push -u origin main
```

---

### 2️⃣ CRIAR PROJETO NO RAILWAY

1. Acesse: https://railway.app
2. Faça login (pode usar GitHub)
3. Clique **"New Project"**
4. Selecione **"Deploy from GitHub repo"**
5. Escolha o repositório `ai-agent-backend`

**Railway começa a fazer deploy automaticamente!**

---

### 3️⃣ ADICIONAR POSTGRESQL

1. Dentro do projeto no Railway, clique **"+ New"**
2. Selecione **"Database"**
3. Clique **"Add PostgreSQL"**

**Railway conecta automaticamente o banco ao backend!**

---

### 4️⃣ ADICIONAR OPENAI API KEY

1. Clique no **serviço do backend** (não no PostgreSQL)
2. Vá na aba **"Variables"**
3. Clique **"+ New Variable"**
4. Adicione:

```
OPENAI_API_KEY = sk-proj-xxxxxxxxxxxxxxx
```

(Pegue sua key em: https://platform.openai.com/api-keys)

---

### 5️⃣ AGUARDAR DEPLOY

Railway vai:
1. ✅ Instalar Python e dependências
2. ✅ Conectar ao PostgreSQL
3. ✅ Criar todas as tabelas automaticamente
4. ✅ Inserir 2 agentes de exemplo
5. ✅ Disponibilizar a API

**Tempo total: ~2 minutos**

---

### 6️⃣ TESTAR

Railway gera uma URL automática. Exemplo:
```
https://ai-agent-backend-production-xxxx.up.railway.app
```

**Teste 1: Health Check**
```bash
curl https://SUA_URL.railway.app/health
```

Resposta esperada:
```json
{
  "status": "online",
  "database": "healthy",
  "openai_configured": true,
  "version": "2.0.0"
}
```

**Teste 2: Listar Agentes**
```bash
curl https://SUA_URL.railway.app/api/agents
```

Deve retornar 2 agentes.

**Teste 3: Conversar com Agente**
```bash
curl -X POST https://SUA_URL.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "00000000-0000-0000-0000-000000000001",
    "user_identifier": "test@email.com",
    "message": "Olá!"
  }'
```

Resposta esperada:
```json
{
  "conversation_id": "uuid...",
  "response": "Olá! Como posso ajudar você hoje?",
  "tokens": 45,
  "cost": 0.000123,
  "processing_time": 0.89
}
```

---

## ✅ PRONTO!

Se os 3 testes funcionaram, seu backend está 100% operacional!

---

## 🔍 ONDE VER OS LOGS

1. No Railway, clique no serviço do backend
2. Aba **"Deployments"**
3. Clique no deployment ativo
4. Veja **"Deploy Logs"**

Você deve ver:
```
🚀 Iniciando aplicação...
🔍 Verificando estado do banco de dados...
🚀 Primeira execução detectada. Criando schema...
✅ Schema criado com sucesso!
🤖 2 agente(s) criado(s)
✅ Banco de dados pronto!
```

---

## 🐛 SE ALGO DER ERRADO

### Erro: "Internal Server Error 500"

**Causa**: OpenAI key inválida ou DATABASE_URL não configurada

**Solução**:
1. Verifique logs no Railway
2. Confirme que há uma variável `DATABASE_URL` (criada automaticamente ao conectar PostgreSQL)
3. Confirme que `OPENAI_API_KEY` está correta
4. Na aba "Deployments", clique em "Redeploy"

### Erro: "Database connection failed"

**Causa**: PostgreSQL não conectado

**Solução**:
1. No projeto Railway, clique "+ New"
2. Adicione PostgreSQL
3. Railway reconectará automaticamente
4. Force redeploy do backend

### Erro: Tabelas não foram criadas

**Causa**: Script de inicialização não rodou

**Solução manual**:
1. No Railway, abra o PostgreSQL
2. Clique em "Data" → "Query"
3. Cole o conteúdo de `init_database.sql`
4. Execute
5. Force redeploy do backend

---

## 📚 DOCUMENTAÇÃO COMPLETA

Acesse: `https://SUA_URL.railway.app/docs`

Swagger UI interativo com todos os endpoints!

---

## 💰 CUSTOS

- **Railway**: €5/mês (Starter Plan) ou grátis (trial de €5)
- **OpenAI**: ~€0.10 por 1000 mensagens (GPT-4o-mini)
- **Total**: ~€10-20/mês para uso moderado

---

## 📞 PRÓXIMOS PASSOS

1. ✅ Anote a URL do Railway
2. ✅ Teste todos os endpoints em `/docs`
3. ✅ Configure frontend para usar essa URL
4. ✅ Comece a desenvolver features avançadas (WhatsApp, Email, RAG)

**Tudo funcionando? Parabéns! 🎉**
