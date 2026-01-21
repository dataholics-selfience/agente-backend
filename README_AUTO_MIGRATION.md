# 🚀 DEPLOY AUTOMÁTICO - Backend v4.0.0

## ✨ ZERO CONFIGURAÇÃO MANUAL

Este backend foi projetado para fazer **tudo automaticamente** no primeiro deploy:

1. ✅ Cria tabelas do zero (se não existirem)
2. ✅ Detecta versão antiga e faz migration automática
3. ✅ Adiciona todas as colunas novas
4. ✅ Gera slugs para agentes existentes
5. ✅ Cria índices
6. ✅ Insere agentes de exemplo

**Você só precisa fazer deploy. O resto é automático!**

---

## 📦 Deploy no Railway

### Opção 1: Via Git (Recomendado)

```bash
# 1. Extrair arquivos
tar -xzf backend-v4-auto-migration.tar.gz
cd backend-railway-final-corrigido

# 2. Inicializar Git (se ainda não tem)
git init
git add .
git commit -m "feat: backend v4 com migration automática"

# 3. Conectar com Railway
railway link

# 4. Deploy (migration roda automaticamente)
git push railway main
```

### Opção 2: Via Railway CLI

```bash
# 1. Extrair arquivos
tar -xzf backend-v4-auto-migration.tar.gz
cd backend-railway-final-corrigido

# 2. Deploy direto
railway up
```

---

## 🔍 Verificar Deploy

```bash
# Ver logs (deve mostrar "Migration v4.0.0 concluída")
railway logs --tail 50

# Testar
curl https://web-production-9a8a1.up.railway.app/health
```

**Logs esperados:**
```
🚀 Iniciando aplicação...
🔍 Verificando banco de dados...
✅ Banco já inicializado
🔄 Verificando se migration v4 é necessária...
🚀 Executando migration v4.0.0...
  📦 Adicionando colunas novas...
  🔧 Gerando slugs para agentes existentes...
  🔍 Garantindo slugs únicos...
  📊 Criando índices...
  🎨 Preenchendo valores padrão...
  ✅ Migration v4.0.0 concluída!
🤖 3 agente(s) no banco
✅ Sistema pronto!
```

---

## 🧪 Testar Endpoints

```bash
# 1. Health check
curl https://web-production-9a8a1.up.railway.app/health

# 2. Listar agentes (deve mostrar slugs)
curl https://web-production-9a8a1.up.railway.app/api/agents

# 3. Criar novo agente
curl -X POST https://web-production-9a8a1.up.railway.app/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Agent",
    "system_prompt": "You are helpful"
  }'

# Resposta esperada:
# {
#   "id": "...",
#   "slug": "test-agent",  ✅ Gerado automaticamente
#   "name": "Test Agent",
#   ...
# }

# 4. Testar endpoint público
curl https://web-production-9a8a1.up.railway.app/api/public/agents/test-agent

# 5. Chat público
curl -X POST https://web-production-9a8a1.up.railway.app/api/public/agents/test-agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

---

## 🔄 Como Funciona a Migration Automática

### 1. Primeira Instalação (Banco Vazio)
- Cria todas as tabelas **já com campos v4**
- Insere 2 agentes de exemplo com slugs

### 2. Update (v3 → v4)
- Detecta que tabela `agents` existe
- Verifica se coluna `slug` existe
- Se NÃO existe → Executa migration automática
- Se existe → Pula migration

### 3. Segurança
- Usa `IF NOT EXISTS` em tudo
- Commits automáticos
- Erros não críticos são ignorados
- Logs detalhados para debug

---

## 📊 O que Muda no Banco

### Tabela `agents` - Novos campos:
```sql
slug                    VARCHAR(100) UNIQUE
description             TEXT
avatar_url              VARCHAR(500)
max_tokens              INTEGER DEFAULT 1000
top_p                   FLOAT DEFAULT 1.0
frequency_penalty       FLOAT DEFAULT 0.0
presence_penalty        FLOAT DEFAULT 0.0
function_calling_enabled BOOLEAN DEFAULT FALSE
whatsapp_number         VARCHAR(20)
email_address           VARCHAR(200)
web_enabled             BOOLEAN DEFAULT TRUE
is_active               BOOLEAN DEFAULT TRUE
allow_public_access     BOOLEAN DEFAULT TRUE
brand_color             VARCHAR(7) DEFAULT '#4F46E5'
welcome_message         TEXT DEFAULT 'Olá! Como posso ajudar?'
input_placeholder       VARCHAR(100) DEFAULT 'Digite sua mensagem...'
meta_title              VARCHAR(200)
meta_description        VARCHAR(500)
og_image_url            VARCHAR(500)
```

### Tabela `conversations` - Novo campo:
```sql
session_id              UUID
```

### Novos índices:
```sql
CREATE UNIQUE INDEX idx_agents_slug_unique ON agents(slug)
CREATE INDEX idx_agents_is_active ON agents(is_active)
CREATE INDEX idx_conversations_session_id ON conversations(session_id)
```

---

## ✅ Checklist Pós-Deploy

- [ ] Deploy completo sem erros
- [ ] Logs mostram "Migration v4.0.0 concluída"
- [ ] `/health` retorna 200
- [ ] `GET /api/agents` mostra agentes com `slug`
- [ ] `POST /api/agents` funciona
- [ ] `GET /api/public/agents/{slug}` funciona
- [ ] `POST /api/public/agents/{slug}/chat` funciona
- [ ] Docs acessíveis em `/docs`

---

## 🐛 Troubleshooting

### Erro: "column agents.slug does not exist"

**Causa:** Migration não rodou (raro)

**Solução:**
```bash
# Ver logs completos
railway logs --tail 100 | grep -i migration

# Forçar restart
railway restart
```

### Logs não mostram migration

**Causa:** Banco foi criado direto na v4 (normal)

**Solução:** Nenhuma, está funcionando!

### Agentes antigos sem slug

**Causa:** Impossível se migration rodou

**Verificar:**
```bash
railway run psql $DATABASE_URL -c "SELECT id, name, slug FROM agents;"
```

Todos devem ter slug.

---

## 📈 Próximos Passos

Após deploy bem-sucedido:

1. ✅ Backend funcionando com URLs públicas
2. ✅ Pronto para frontend admin
3. ✅ Pronto para frontend público
4. ✅ Docs em `/docs`

---

## 🎯 Vantagens da Migration Automática

✅ **Zero comandos SQL manuais**  
✅ **Idempotente** - Pode rodar várias vezes sem problemas  
✅ **Logs detalhados** - Vê exatamente o que acontece  
✅ **Seguro** - Não quebra instalações existentes  
✅ **Rápido** - Tudo em segundos no startup  

---

## 📞 Suporte

**Logs:**
```bash
railway logs --tail 100
```

**Database:**
```bash
railway run psql $DATABASE_URL
```

**Restart:**
```bash
railway restart
```

---

**Versão:** 4.0.0  
**Status:** ✅ 100% Automático  
**Última atualização:** 2025-01-21

---

# 🎉 JUST DEPLOY IT!

Literalmente, só fazer `railway up` ou `git push` e tudo funciona.
