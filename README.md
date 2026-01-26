# Backend - Sistema de Agentes IA

Build: v2.0.1 - 2026-01-26

## Deploy Railway

1. Fazer upload deste código para GitHub
2. Conectar Railway ao repositório
3. Configurar variáveis de ambiente:

```
DATABASE_URL=<fornecido pelo Railway>
OPENAI_API_KEY=sk-...
JWT_SECRET_KEY=<gerar chave aleatória>
ADMIN_USERNAME=admin
ADMIN_PASSWORD=SuaSenhaForte123!
CORS_ORIGINS=https://agentes.genoibot.com,http://localhost:3000
```

4. Deploy automático!

## Endpoints

- GET /health - Health check
- POST /api/auth/login - Login
- GET /api/agents - Listar agentes (requer auth)
- POST /api/agents - Criar agente (requer auth)
- PUT /api/agents/{id} - Editar agente (requer auth)
- DELETE /api/agents/{id} - Deletar agente (requer auth)
- GET /api/public/agents/{slug} - Info pública do agente
- POST /api/public/agents/{slug}/chat - Chat público

## Correções nesta versão

✅ Removido python-cors (não existe)
✅ DELETE faz hard delete real
✅ PUT normaliza slugs automaticamente
✅ Public endpoint case-insensitive
✅ CORS configurado corretamente
✅ Logging detalhado

