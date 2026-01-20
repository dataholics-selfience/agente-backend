# 🚀 Backend AI Agent - PRONTO PARA DEPLOY

**Versão Final Corrigida - 100% Funcional no Railway**

---

## ✅ O QUE FOI CORRIGIDO

Este projeto inclui TODAS as correções:

1. ✅ OpenAI 1.59.8 (compatível com Railway)
2. ✅ Lazy loading do client OpenAI
3. ✅ SQL inline (não depende de arquivos)
4. ✅ Inicialização automática do banco
5. ✅ **Pydantic v2 schemas** (correção do datetime)

---

## 🎯 DEPLOY EM 3 PASSOS

### 1️⃣ PREPARAR GIT

```bash
# Extrair o projeto
tar -xzf backend-railway-final-corrigido.tar.gz
cd backend-railway-final-corrigido

# Inicializar Git
git init
git add .
git commit -m "Initial commit - AI Agent Backend"

# Criar repositório no GitHub e conectar
git remote add origin https://github.com/SEU_USUARIO/ai-agent-backend.git
git branch -M main
git push -u origin main
```

### 2️⃣ DEPLOY NO RAILWAY

1. https://railway.app → "New Project"
2. "Deploy from GitHub repo"
3. Selecione: `ai-agent-backend`

### 3️⃣ CONFIGURAR

**A. PostgreSQL:**
- + New → Database → Add PostgreSQL

**B. OpenAI:**
- Backend → Variables → + New Variable
- Name: `OPENAI_API_KEY`
- Value: `sk-proj-xxx`

**PRONTO!** Railway faz deploy automático.

---

## ✅ TESTAR

```bash
# Health Check
curl https://SUA_URL/health

# Listar Agentes
curl https://SUA_URL/api/agents

# Criar Agente
curl -X POST https://SUA_URL/api/agents \
  -H "Content-Type: application/json" \
  -d '{"name":"Vendedor","system_prompt":"Você é vendedor.","model":"gpt-4o-mini","temperature":0.7}'

# Chat
curl -X POST https://SUA_URL/api/chat \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"00000000-0000-0000-0000-000000000001","user_identifier":"test@email.com","message":"Olá!"}'
```

---

## 📊 VERIFICAR LOGS

Railway → Backend → Deployments → Logs

Deve mostrar:
```
✅ Schema criado com sucesso!
🤖 2 agente(s) criado(s)
✅ Sistema pronto!
```

---

## 🐛 TROUBLESHOOTING

**Erro: "relation 'agents' does not exist"**
→ Force redeploy (Deployments → Redeploy)

**Erro: Build falha**
→ Verifique `openai==1.59.8` em requirements.txt

**Erro: Variáveis não configuradas**
→ Backend → Variables → Adicione OPENAI_API_KEY

---

**Versão:** 3.1.0  
**Status:** ✅ Pronto para produção  
**Documentação:** /docs
