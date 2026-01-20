# 📋 GUIA DE DEPLOY - PASSO A PASSO

## 1️⃣ EXTRAIR E PREPARAR

```bash
# Extrair
tar -xzf backend-railway-final-corrigido.tar.gz
cd backend-railway-final-corrigido

# Verificar arquivos
ls -la
# Deve mostrar: main.py, requirements.txt, Procfile, app/, etc.
```

---

## 2️⃣ GIT

```bash
# Inicializar
git init
git add .
git commit -m "AI Agent Backend - v3.1"

# Criar repositório no GitHub
# Vá em: https://github.com/new
# Nome: ai-agent-backend
# Público ou Privado
# NÃO adicione README, .gitignore ou license

# Conectar
git remote add origin https://github.com/SEU_USUARIO/ai-agent-backend.git
git branch -M main
git push -u origin main
```

**✓ Checkpoint:** Código no GitHub

---

## 3️⃣ RAILWAY - CRIAR PROJETO

1. Abra: https://railway.app
2. Login (GitHub recomendado)
3. Clique: **"New Project"**
4. Selecione: **"Deploy from GitHub repo"**
5. Autorize Railway (se primeira vez)
6. Escolha: `ai-agent-backend`
7. Aguarde build (~2 min)

**✓ Checkpoint:** Build completo

---

## 4️⃣ RAILWAY - ADICIONAR POSTGRESQL

1. No projeto, clique: **"+ New"**
2. Selecione: **"Database"**
3. Clique: **"Add PostgreSQL"**
4. Aguarde ~30 segundos

**Railway conecta automaticamente!**

**✓ Checkpoint:** PostgreSQL online (ícone verde)

---

## 5️⃣ RAILWAY - CONFIGURAR API KEY

1. Clique no serviço **BACKEND** (não PostgreSQL)
2. Aba: **"Variables"**
3. Clique: **"+ New Variable"**
4. Preencha:
   - **Variable Name:** `OPENAI_API_KEY`
   - **Value:** `sk-proj-xxxxxxxxx` (sua key)
5. Clique: **"Add"**

**Railway faz redeploy automático!**

**✓ Checkpoint:** 2 variáveis visíveis (DATABASE_URL e OPENAI_API_KEY)

---

## 6️⃣ AGUARDAR DEPLOY

1. Aba: **"Deployments"**
2. Aguarde deploy ativo (~2 min)
3. Status deve ficar: **"Success"**

---

## 7️⃣ VERIFICAR LOGS

1. Deployments → Deploy ativo
2. Aba: **"Deploy Logs"**
3. Procure por:

```
🚀 Iniciando aplicação...
🔍 Verificando banco de dados...
🚀 Criando schema do banco de dados...
✅ Schema criado com sucesso!
🤖 2 agente(s) criado(s)
✅ Sistema pronto!
INFO: Application startup complete.
```

**Se ver isso → FUNCIONOU!** ✅

---

## 8️⃣ PEGAR URL

1. Serviço backend
2. Aba: **"Settings"**
3. Seção: **"Domains"**
4. Copie a URL (ex: `https://web-production-xxxx.up.railway.app`)

---

## 9️⃣ TESTAR API

Use a URL copiada:

```bash
# Substitua SUA_URL pela URL do Railway

# Teste 1: Health
curl https://SUA_URL/health

# Teste 2: Agentes
curl https://SUA_URL/api/agents

# Teste 3: Criar Agente
curl -X POST https://SUA_URL/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vendedor IA",
    "system_prompt": "Você é um vendedor educado.",
    "model": "gpt-4o-mini",
    "temperature": 0.7
  }'

# Teste 4: Chat
curl -X POST https://SUA_URL/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "00000000-0000-0000-0000-000000000001",
    "user_identifier": "test@email.com",
    "message": "Olá!"
  }'
```

**Se todos os 4 testes passarem → SUCESSO TOTAL!** 🎉

---

## 🔟 VERIFICAR POSTGRESQL

1. Railway → PostgreSQL
2. Aba: **"Data"**
3. Deve ter **5 tabelas:**
   - agents
   - conversations
   - messages
   - documents
   - channel_configs

4. Clique em **"agents"**
5. Deve ter **2 registros**

---

## ✅ CHECKLIST FINAL

- [ ] Código no GitHub
- [ ] Projeto criado no Railway
- [ ] PostgreSQL adicionado
- [ ] OPENAI_API_KEY configurada
- [ ] Build completo (Success)
- [ ] Logs mostram "✅ Sistema pronto!"
- [ ] PostgreSQL tem 5 tabelas
- [ ] agents tem 2 registros
- [ ] GET /health funciona
- [ ] GET /api/agents funciona
- [ ] POST /api/agents funciona
- [ ] POST /api/chat funciona

---

## 🎯 PRÓXIMOS PASSOS

Agora que está funcionando:

1. **Documentação:** Acesse `https://SUA_URL/docs` (Swagger UI)
2. **Testar mais:** Crie agentes, converse, veja custos
3. **Frontend:** Desenvolva interface conectada à API
4. **Features:** WhatsApp, Email, RAG (Fase 2)

---

## 🆘 SE DER ERRO

### Build falha
- Verifique que todos os arquivos foram commitados
- Force rebuild: Deployments → ... → Rebuild

### Sem variável DATABASE_URL
- Delete PostgreSQL
- Adicione novamente (+ New → Database → PostgreSQL)

### Erro 500
- Veja logs completos
- Confirme que logs mostram "✅ Sistema pronto!"
- Force redeploy

### Tabelas não criadas
- Veja logs do primeiro deploy
- Deve mostrar "✅ Schema criado"
- Se não, force redeploy

---

**Tempo total:** ~10 minutos  
**Custo:** €0 (trial) ou €5/mês  
**Sucesso:** 100% se seguir os passos 🎯
