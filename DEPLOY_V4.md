# 🚀 GUIA DE DEPLOY - Backend v4.0.0

## ⚠️ IMPORTANTE - BREAKING CHANGES

Esta versão adiciona novos campos ao banco de dados. **EXECUTE A MIGRATION ANTES DO DEPLOY**.

---

## 📋 Pré-requisitos

- Railway CLI instalado
- Acesso ao projeto Railway
- Backup do banco de dados (recomendado)

---

## 🔄 Processo de Deploy

### 1. Backup (Recomendado)

```bash
# Via Railway
railway run pg_dump $DATABASE_URL > backup_v3.sql

# Ou conecte manualmente
psql $DATABASE_URL -c "\copy (SELECT * FROM agents) TO 'agents_backup.csv' CSV HEADER"
```

---

### 2. Execute Migration

**Opção A: Via Railway Dashboard**
1. Acesse Railway Dashboard
2. Vá em PostgreSQL → Query
3. Cole o conteúdo de `migration_v4.sql`
4. Execute

**Opção B: Via CLI**
```bash
# Upload do arquivo
railway run bash -c "cat > /tmp/migration.sql << 'EOF'
$(cat migration_v4.sql)
EOF
psql \$DATABASE_URL -f /tmp/migration.sql"

# Ou direto
psql $DATABASE_URL -f migration_v4.sql
```

---

### 3. Verifique Migration

```bash
railway run psql $DATABASE_URL -c "
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'agents' 
AND column_name IN ('slug', 'brand_color', 'is_active')
ORDER BY column_name;
"
```

Deve retornar:
```
 column_name  | data_type
--------------+------------
 brand_color  | character varying
 is_active    | boolean
 slug         | character varying
```

---

### 4. Deploy do Código

```bash
# Via Git (recomendado)
git add .
git commit -m "feat: adicionar dual-frontend v4.0.0"
git push railway main

# Ou via Railway CLI
railway up
```

---

### 5. Teste os Endpoints

```bash
# Health check
curl https://web-production-9a8a1.up.railway.app/health

# Criar agente de teste
curl -X POST https://web-production-9a8a1.up.railway.app/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Agent",
    "system_prompt": "You are a helpful assistant"
  }'

# Copie o slug retornado (ex: test-agent)

# Testar endpoint público
curl https://web-production-9a8a1.up.railway.app/api/public/agents/test-agent

# Testar chat público
curl -X POST https://web-production-9a8a1.up.railway.app/api/public/agents/test-agent/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello",
    "session_id": "test-session-123"
  }'
```

---

## 🔍 Verificação Pós-Deploy

### Checklist Completo

- [ ] Migration executada com sucesso
- [ ] `/health` retorna status 200
- [ ] `/docs` carrega documentação atualizada
- [ ] `GET /api/agents` funciona
- [ ] `POST /api/agents` cria agente e gera slug
- [ ] `GET /api/public/agents/{slug}` retorna dados públicos
- [ ] `POST /api/public/agents/{slug}/chat` funciona
- [ ] Agentes antigos têm slug gerado automaticamente
- [ ] Logs não mostram erros críticos

---

## 🐛 Troubleshooting

### Erro: "column 'slug' does not exist"
**Causa:** Migration não foi executada  
**Solução:**
```bash
railway run psql $DATABASE_URL -f migration_v4.sql
railway restart
```

### Erro: "duplicate key value violates unique constraint"
**Causa:** Slugs duplicados na migration  
**Solução:**
```bash
# Limpar slugs duplicados
railway run psql $DATABASE_URL -c "
UPDATE agents 
SET slug = CONCAT(slug, '-', id::text) 
WHERE slug IN (
  SELECT slug FROM agents 
  GROUP BY slug HAVING COUNT(*) > 1
);"
```

### Erro: Build falha no Railway
**Causa:** Dependências não instaladas  
**Solução:**
```bash
# Verificar requirements.txt
cat requirements.txt

# Forçar rebuild
railway redeploy
```

### Erro 500 em `/api/agents`
**Causa:** Campos obrigatórios com NULL  
**Solução:**
```bash
# Preencher valores default
railway run psql $DATABASE_URL -c "
UPDATE agents 
SET 
  brand_color = '#4F46E5',
  welcome_message = 'Olá! Como posso ajudar?',
  input_placeholder = 'Digite sua mensagem...',
  is_active = TRUE,
  allow_public_access = TRUE
WHERE brand_color IS NULL OR is_active IS NULL;"
```

---

## 📊 Monitoramento

### Logs Importantes

```bash
# Acompanhar logs em tempo real
railway logs --tail 100

# Buscar erros
railway logs | grep ERROR

# Verificar inicialização
railway logs | grep "Sistema pronto"
```

### Queries Úteis

```bash
# Quantos agentes ativos
railway run psql $DATABASE_URL -c "
SELECT 
  COUNT(*) FILTER (WHERE is_active = true) as ativos,
  COUNT(*) FILTER (WHERE is_active = false) as inativos,
  COUNT(*) as total
FROM agents;"

# Agentes sem slug (não deveria existir)
railway run psql $DATABASE_URL -c "
SELECT id, name FROM agents WHERE slug IS NULL;"

# Conversas públicas hoje
railway run psql $DATABASE_URL -c "
SELECT COUNT(*) FROM conversations 
WHERE user_identifier LIKE 'public_%' 
AND created_at > CURRENT_DATE;"
```

---

## 🔄 Rollback (Se Necessário)

### Reverter para v3.0.0

```bash
# 1. Fazer checkout do commit anterior
git checkout <commit-hash-v3>

# 2. Deploy
git push railway main --force

# 3. Reverter migration (CUIDADO!)
railway run psql $DATABASE_URL -f rollback_v4.sql
```

**rollback_v4.sql:**
```sql
-- CUIDADO: Isso remove colunas e dados
ALTER TABLE agents DROP COLUMN IF EXISTS slug;
ALTER TABLE agents DROP COLUMN IF EXISTS brand_color;
-- ... (adicione todos os campos novos)
```

---

## 🎯 Próximos Passos

Após deploy bem-sucedido:

1. ✅ Testar no frontend público
2. ✅ Criar documentação de integração
3. ✅ Configurar monitoring/alertas
4. ✅ Configurar CORS para domínios corretos
5. ✅ Implementar rate limiting

---

## 📞 Suporte

**Problemas críticos:**
1. Verifique logs: `railway logs`
2. Verifique database: `railway run psql $DATABASE_URL`
3. Rollback se necessário (instruções acima)

**Railway específico:**
- Dashboard: https://railway.app
- Docs: https://docs.railway.app

---

**Versão:** 4.0.0  
**Data:** 2025-01-21  
**Status:** ✅ Pronto para deploy
