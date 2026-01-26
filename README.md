# Sistema de Agentes IA - Backend (CORRIGIDO)

Backend FastAPI para plataforma de agentes conversacionais inteligentes.

## ✅ BUGS CORRIGIDOS

### 1. DELETE não removia da lista
**Problema:** Soft delete sem filtro no GET  
**Solução:** Hard delete ou filtro de `deleted_at.is_(None)`

### 2. PUT quebrava agente ao editar slug
**Problema:** Slug com espaços salvo literalmente  
**Solução:** `normalize_slug()` automático usando `python-slugify`

### 3. Endpoint público retornava 404
**Problema:** Case-sensitive search, sem fallback  
**Solução:** Case-insensitive + fallback + logs detalhados

---

## 🚀 DEPLOY NO RAILWAY

### 1. Criar Novo Projeto Railway

```bash
# Descompactar o arquivo
unzip agentes-ia-backend-fixed.zip
cd agentes-ia-backend-fixed

# Inicializar Git
git init
git add .
git commit -m "Backend corrigido - DELETE e PUT funcionando"

# Conectar com Railway
railway link

# Deploy
railway up
```

### 2. Configurar Variáveis de Ambiente

No painel Railway, adicionar:

```env
DATABASE_URL=<postgresql-url-from-railway>
REDIS_URL=<redis-url-from-railway>
OPENAI_API_KEY=sk-...
JWT_SECRET_KEY=<gerar-chave-segura>
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<senha-forte>
CORS_ORIGINS=https://agentes.genoibot.com,http://localhost:3000
PORT=8080
```

### 3. Limpar Database (Opcional)

Se houver agentes órfãos no database:

```bash
railway connect postgres
```

```sql
-- Remover agentes deletados
DELETE FROM agents WHERE deleted_at IS NOT NULL;

-- Normalizar slugs
UPDATE agents
SET slug = LOWER(
    REGEXP_REPLACE(
        REGEXP_REPLACE(slug, '[^a-z0-9-]+', '-', 'g'),
        '-+', '-', 'g'
    )
);

-- Ativar todos
UPDATE agents
SET is_active = true, allow_public_access = true;

-- Verificar
SELECT id, name, slug, is_active, allow_public_access FROM agents;
```

---

## 📁 ESTRUTURA DO PROJETO

```
agentes-ia-backend-fixed/
├── main.py                 # Aplicação FastAPI principal
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── database.py            # Database config
├── auth.py                # JWT authentication
├── utils.py               # normalize_slug() e helpers
├── requirements.txt       # Dependências
├── Procfile              # Railway config
├── runtime.txt           # Python version
├── .env.example          # Template de env vars
├── routes/
│   ├── agents.py         # CRUD agentes (CORRIGIDO)
│   ├── public.py         # Endpoints públicos (CORRIGIDO)
│   └── auth.py           # Login
└── services/
    └── llm.py            # OpenAI integration
```

---

## 🧪 TESTAR APÓS DEPLOY

### 1. Health Check
```bash
curl https://seu-backend.up.railway.app/health
```

### 2. Login
```bash
curl -X POST https://seu-backend.up.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"sua-senha"}'
```

### 3. Criar Agente
```bash
curl -X POST https://seu-backend.up.railway.app/api/agents \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -d '{
    "name": "Test Agent",
    "slug": "test agent with spaces",
    "system_prompt": "You are a helpful assistant",
    "model": "gpt-4o-mini"
  }'

# Deve normalizar slug para "test-agent-with-spaces"
```

### 4. Listar Agentes
```bash
curl https://seu-backend.up.railway.app/api/agents \
  -H "Authorization: Bearer SEU_TOKEN"
```

### 5. Deletar Agente
```bash
curl -X DELETE https://seu-backend.up.railway.app/api/agents/UUID \
  -H "Authorization: Bearer SEU_TOKEN"

# Verificar que sumiu da lista
curl https://seu-backend.up.railway.app/api/agents \
  -H "Authorization: Bearer SEU_TOKEN"
```

### 6. Editar Slug
```bash
curl -X PUT https://seu-backend.up.railway.app/api/agents/UUID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -d '{"slug": "novo slug com espaços"}'

# Deve normalizar e agente continuar acessível
curl https://seu-backend.up.railway.app/api/public/agents/novo-slug-com-espacos
```

### 7. Chat Público
```bash
curl -X POST https://seu-backend.up.railway.app/api/public/agents/test-agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá!"}'
```

---

## 🔧 DESENVOLVIMENTO LOCAL

### 1. Instalar Dependências
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar .env
```bash
cp .env.example .env
# Editar .env com suas credenciais
```

### 3. Rodar
```bash
python main.py
```

Acessar: http://localhost:8080/docs

---

## 📝 CHANGELOG

### v1.0.0 (2025-01-26)
- ✅ BUG FIX: DELETE agora remove da lista
- ✅ BUG FIX: PUT normaliza slug automaticamente
- ✅ BUG FIX: Endpoint público com case-insensitive + fallback
- ✅ Validação de slug em tempo real
- ✅ Logs detalhados para debug
- ✅ Hard delete (simplificado)
- ✅ `normalize_slug()` com `python-slugify`

---

## 🆘 TROUBLESHOOTING

### "Agente não encontrado" após editar
**Causa:** Slug no DB diferente do esperado  
**Solução:** Rodar SQL de normalização acima

### "DELETE retorna 200 mas agente continua"
**Causa:** Versão antiga do código  
**Solução:** Fazer deploy desta versão corrigida

### "500 Internal Server Error"
**Causa:** Variáveis de ambiente faltando  
**Solução:** Verificar todas as env vars no Railway

---

## 📞 SUPORTE

Este backend resolve definitivamente os bugs:
1. ✅ DELETE funciona
2. ✅ PUT não quebra agente
3. ✅ Slugs normalizados automaticamente

Qualquer problema, verificar os logs do Railway! 🔍
