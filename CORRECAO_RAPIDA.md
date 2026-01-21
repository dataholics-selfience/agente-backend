# ⚡ CORREÇÃO RÁPIDA - Execute Isto AGORA

## 🚨 Problema Identificado

O erro acontece porque **a migration não foi executada**. O banco não tem as colunas novas.

```
psycopg2.errors.UndefinedColumn: column agents.slug does not exist
```

---

## ✅ Solução (2 minutos)

### 1. Execute a Migration

```bash
# Conectar ao Railway e executar migration
railway run psql $DATABASE_URL < quick_migration.sql
```

**OU via Railway Dashboard:**
1. Acesse Railway Dashboard
2. Vá em PostgreSQL → Query
3. Cole o conteúdo de `quick_migration.sql`
4. Execute

---

### 2. Reinicie o Serviço

```bash
railway restart
```

---

### 3. Teste Novamente

```bash
# Health check
curl https://web-production-9a8a1.up.railway.app/health

# Criar agente
curl -X POST https://web-production-9a8a1.up.railway.app/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Agent",
    "system_prompt": "You are helpful"
  }'

# Deve retornar:
# {
#   "id": "...",
#   "slug": "test-agent",  ⬅️ AGORA VAI FUNCIONAR
#   ...
# }
```

---

## 🔍 Verificar se Migration Funcionou

```bash
railway run psql $DATABASE_URL -c "
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'agents' 
AND column_name IN ('slug', 'brand_color', 'is_active', 'max_tokens')
ORDER BY column_name;
"
```

**Deve retornar:**
```
   column_name  |     data_type
----------------+--------------------
 brand_color    | character varying
 is_active      | boolean
 max_tokens     | integer
 slug           | character varying
```

Se aparecer vazio, a migration não rodou. Execute novamente.

---

## 📝 O que a Migration Faz

1. ✅ Adiciona coluna `slug` e todos os campos novos
2. ✅ Gera slugs para agentes existentes
3. ✅ Garante slugs únicos (adiciona contador se duplicado)
4. ✅ Cria índices para performance
5. ✅ Preenche valores padrão

---

## 🐛 Se Ainda Não Funcionar

### Verificar logs:
```bash
railway logs --tail 50
```

### Procurar por erros de sintaxe SQL:
```bash
railway run psql $DATABASE_URL -c "SELECT * FROM agents LIMIT 1;"
```

### Rollback (se necessário):
```bash
# Remover colunas adicionadas
railway run psql $DATABASE_URL -c "
ALTER TABLE agents DROP COLUMN IF EXISTS slug;
ALTER TABLE agents DROP COLUMN IF EXISTS brand_color;
-- (adicione todas as colunas novas)
"
```

---

## ✅ Checklist Pós-Migration

- [ ] Migration executada com sucesso
- [ ] Serviço reiniciado
- [ ] `/health` retorna 200
- [ ] `POST /api/agents` funciona
- [ ] Agente criado tem `slug` gerado
- [ ] `GET /api/public/agents/{slug}` funciona
- [ ] Logs não mostram erros

---

## 💡 Por Que Aconteceu?

O código novo usa colunas que ainda não existiam no banco. É **obrigatório** executar a migration antes do deploy do código novo.

**Ordem correta:**
1. Migration SQL
2. Deploy código
3. Teste

---

**Execute `quick_migration.sql` AGORA e tudo vai funcionar!** 🚀
