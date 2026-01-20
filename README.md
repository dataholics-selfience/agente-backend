# 🚀 Backend AI Agent - Railway Edition

**Backend que funciona 100% no Railway - SEM configuração manual**

## ✅ O QUE ESTE PROJETO FAZ

- ✅ Cria tabelas automaticamente no primeiro uso
- ✅ Insere 2 agentes pré-configurados
- ✅ API REST completa para chat com IA
- ✅ Cálculo automático de custos
- ✅ Zero configuração manual necessária

---

## 🎯 DEPLOY EM 3 PASSOS

### 1️⃣ Preparar Código

```bash
# Extrair
tar -xzf backend-railway-final.tar.gz
cd backend-railway-final

# Git
git init
git add .
git commit -m "Backend AI Agent"
git remote add origin https://github.com/SEU_USUARIO/ai-agent.git
git push -u origin main
```

### 2️⃣ Deploy no Railway

1. **Railway** → New Project
2. **Deploy from GitHub repo**
3. Escolha: `ai-agent`

### 3️⃣ Configurar

1. **Adicionar PostgreSQL:**
   - No projeto → + New
   - Database → Add PostgreSQL
   
2. **Adicionar OpenAI Key:**
   - Clique no serviço backend
   - Variables → + New Variable
   - Nome: `OPENAI_API_KEY`
   - Valor: `sk-proj-xxxxx`

**PRONTO!** 🎉

Railway faz deploy automaticamente em ~2 minutos.

---

## ✅ TESTAR

Pegar URL do Railway (ex: `https://web-production-xxxx.up.railway.app`)

```bash
# 1. Health check
curl https://SUA_URL/health

# 2. Listar agentes
curl https://SUA_URL/api/agents

# 3. Conversar
curl -X POST https://SUA_URL/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "00000000-0000-0000-0000-000000000001",
    "user_identifier": "test@email.com",
    "message": "Olá!"
  }'
```

Se todos funcionarem → **Sistema operacional!** ✅

---

## 🔍 VERIFICAR LOGS

Railway → Backend → Deployments → Deploy ativo → Logs

Procure por:
```
🚀 Iniciando aplicação...
🔍 Verificando banco de dados...
🚀 Criando schema do banco de dados...
✅ Schema criado com sucesso!
🤖 2 agente(s) criado(s)
✅ Sistema pronto!
INFO: Application startup complete.
```

---

## 🐛 SE DER ERRO

### Erro: "DATABASE_URL não configurada"

**Solução:**
- Railway → + New → Database → Add PostgreSQL
- Railway conecta automaticamente

### Erro: "OPENAI_API_KEY não configurada"

**Solução:**
- Backend → Variables → + New Variable
- OPENAI_API_KEY = sk-proj-xxxxx

### Erro: "relation 'agents' does not exist"

**Solução:**
- Force redeploy (Backend → Deployments → Redeploy)
- Veja logs para confirmar criação das tabelas

### Aplicação crashando

**Verifique:**
1. `requirements.txt` tem `openai==1.59.8`
2. Variables tem `OPENAI_API_KEY` e `DATABASE_URL`
3. PostgreSQL está rodando

---

## 📚 Documentação API

Acesse: `https://SUA_URL/docs`

Swagger UI interativo com todos os endpoints!

---

## 💰 Custos

- **Railway:** €5/mês (ou trial grátis de €5)
- **OpenAI:** ~€0.10 por 1000 mensagens
- **Total:** ~€10-20/mês

---

## 🎯 Endpoints Principais

- `GET /health` - Status do sistema
- `GET /api/agents` - Listar agentes
- `POST /api/agents` - Criar agente
- `POST /api/chat` - Enviar mensagem

---

## ✅ Checklist de Validação

- [ ] PostgreSQL conectado no Railway
- [ ] OPENAI_API_KEY configurada
- [ ] Deploy completo sem erros
- [ ] Logs mostram "✅ Sistema pronto!"
- [ ] GET /health retorna "healthy"
- [ ] GET /api/agents retorna 2 agentes
- [ ] POST /api/chat funciona

---

## 🆘 Suporte

Se ainda não funcionar, verifique:

1. **Logs do deploy** (Railway → Backend → Deployments → Logs)
2. **PostgreSQL está rodando** (Railway → PostgreSQL → Status)
3. **Variáveis configuradas** (Backend → Variables)

---

**Versão:** 3.0.0  
**Status:** ✅ Testado no Railway  
**Última atualização:** 20/01/2025
