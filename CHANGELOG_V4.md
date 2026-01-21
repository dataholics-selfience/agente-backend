# 📝 CHANGELOG

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

---

## [4.0.0] - 2025-01-21

### 🎯 DUAL-FRONTEND ARCHITECTURE

Implementação completa da arquitetura dual-frontend conforme especificação do projeto.

### ✨ Adicionado

#### Modelo de Dados
- **Agent**:
  - `slug` (string, unique) - Identificador público único para URLs
  - `description` (text) - Descrição do agente
  - `avatar_url` (string) - URL do avatar
  - `max_tokens` (int) - Limite de tokens por resposta
  - `top_p` (float) - Parâmetro top_p do LLM
  - `frequency_penalty` (float) - Penalidade de frequência
  - `presence_penalty` (float) - Penalidade de presença
  - `function_calling_enabled` (bool) - Ativa function calling
  - `whatsapp_number` (string) - Número WhatsApp configurado
  - `email_address` (string) - Email configurado
  - `web_enabled` (bool) - Ativa canal web
  - `is_active` (bool) - Controla se agente está ativo
  - `allow_public_access` (bool) - Permite acesso público
  - `brand_color` (string) - Cor da marca (hex)
  - `welcome_message` (text) - Mensagem de boas-vindas
  - `input_placeholder` (string) - Placeholder do input
  - `meta_title` (string) - Título SEO
  - `meta_description` (string) - Descrição SEO
  - `og_image_url` (string) - Imagem Open Graph

- **Conversation**:
  - `session_id` (UUID) - ID de sessão para chat público

#### Endpoints Admin (Privados)
- `PUT /api/agents/{id}` - Atualizar agente
- `DELETE /api/agents/{id}` - Soft delete de agente

#### Endpoints Públicos (SEM Autenticação)
- `GET /api/public/agents/{slug}` - Obter dados públicos do agente
- `POST /api/public/agents/{slug}/chat` - Enviar mensagem
- `GET /api/public/agents/{slug}/history/{session_id}` - Histórico da conversa

#### Funcionalidades
- **Auto-geração de slug** a partir do nome do agente
- **Slug único** com contador automático (ex: `vendedor-dux-2`)
- **Soft delete** para agentes (reversível)
- **Session tracking** para chat público sem autenticação
- **Segurança** - Endpoint público NÃO expõe `system_prompt`
- **White-label** - Customização por agente (cores, mensagens)
- **SEO-ready** - Meta tags para cada agente

#### Documentação
- `API_DOCUMENTATION.md` - Documentação completa da API
- `DEPLOY_V4.md` - Guia de deploy com migration
- `migration_v4.sql` - Migration SQL completa

### 🔄 Modificado

#### Endpoints Existentes
- `POST /api/agents` agora:
  - Gera `slug` automaticamente
  - Aceita novos campos opcionais
  - Retorna `slug` na resposta
  
- `GET /api/agents` agora retorna:
  - Todos os novos campos
  - Dados completos de customização
  - Parâmetros LLM adicionais

#### Modelos Pydantic
- `AgentCreate` - Expandido com 15+ novos campos opcionais
- `AgentResponse` - Inclui todos os campos novos
- Adicionado `AgentUpdate` - Modelo para updates parciais
- Adicionado `PublicAgentResponse` - Modelo público (sem dados sensíveis)

#### Documentação FastAPI
- Título atualizado: "AI Agent Backend - Dual Frontend"
- Descrição expandida com endpoints principais
- Versão: 3.0.0 → 4.0.0
- Tags organizadas: "Public Chat", "Agents", "Conversations"

### 🛡️ Segurança

- ✅ Endpoint público NÃO retorna `system_prompt`
- ✅ Endpoint público NÃO retorna parâmetros LLM
- ✅ Validação de `is_active` antes de permitir chat
- ✅ Validação de `allow_public_access`
- ✅ Session ID gerado no frontend (não trusted no backend)

### 📊 Migration

**IMPORTANTE**: Execute `migration_v4.sql` ANTES do deploy.

```bash
psql $DATABASE_URL -f migration_v4.sql
```

### 🔧 Breaking Changes

⚠️ **Atenção**: Esta versão adiciona campos obrigatórios com defaults.

1. **Novos campos obrigatórios**:
   - `brand_color` (default: `#4F46E5`)
   - `welcome_message` (default: `"Olá! Como posso ajudar?"`)
   - `input_placeholder` (default: `"Digite sua mensagem..."`)
   - `is_active` (default: `true`)
   - `allow_public_access` (default: `true`)

2. **Schema changes**:
   - `agents.slug` adicionado (unique index)
   - `conversations.session_id` adicionado

3. **Comportamento**:
   - Agentes criados antes da v4 receberão slug automático na migration
   - `DELETE /api/agents/{id}` agora é soft delete (antes era hard delete)

### 📈 Performance

- ✅ Índice em `agents.slug` para queries rápidas
- ✅ Índice em `agents.is_active` para filtros
- ✅ Índice em `conversations.session_id` para chat público

### 🧪 Testes Recomendados

```bash
# 1. Health check
curl /health

# 2. Criar agente
curl -X POST /api/agents -d '{"name":"Test","system_prompt":"Hi"}'

# 3. Testar público
curl /api/public/agents/test

# 4. Chat público
curl -X POST /api/public/agents/test/chat -d '{"message":"Hi"}'
```

---

## [3.0.0] - 2025-01-20

### Versão Estável Anterior

- ✅ CRUD básico de agentes
- ✅ Endpoint de chat funcional
- ✅ Integração OpenAI
- ✅ Database PostgreSQL
- ✅ Deploy Railway configurado

---

## [2.0.0] - 2025-01-19

### Inicial

- Setup FastAPI
- Modelos SQLAlchemy
- Endpoints básicos
- Health check

---

## Formato do Changelog

Este changelog segue [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### Tipos de Mudanças

- **Adicionado** - Novas funcionalidades
- **Modificado** - Mudanças em funcionalidades existentes
- **Depreciado** - Funcionalidades que serão removidas
- **Removido** - Funcionalidades removidas
- **Corrigido** - Bug fixes
- **Segurança** - Vulnerabilidades corrigidas
