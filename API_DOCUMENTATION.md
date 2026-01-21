# 📚 DOCUMENTAÇÃO DA API - Backend Dual-Frontend

**Versão:** 4.0.0  
**Base URL:** `https://web-production-9a8a1.up.railway.app`  
**Documentação Interativa:** `/docs`

---

## 🎯 Visão Geral

Backend para sistema de agentes conversacionais com **duas interfaces**:

1. **Admin API** - CRUD completo de agentes (futuro: autenticado)
2. **Public API** - Chat público via slug único (SEM autenticação)

---

## 🔐 Admin API

### **GET /api/agents**
Lista todos os agentes do sistema.

**Response:**
```json
[
  {
    "id": "uuid",
    "slug": "vendedor-dux",
    "name": "Vendedor Dux",
    "description": "Agente especializado em vendas",
    "system_prompt": "Você é um vendedor...",
    "model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
    "brand_color": "#4F46E5",
    "welcome_message": "Olá! Como posso ajudar?",
    "input_placeholder": "Digite sua mensagem...",
    "is_active": true,
    "allow_public_access": true,
    "rag_enabled": false,
    "created_at": "2025-01-21T00:00:00Z",
    "updated_at": "2025-01-21T00:00:00Z"
  }
]
```

---

### **GET /api/agents/{agent_id}**
Retorna detalhes de um agente específico.

**Parameters:**
- `agent_id` (UUID) - ID do agente

**Response:** Mesmo formato do GET /api/agents

---

### **POST /api/agents**
Cria novo agente. **Gera slug automaticamente**.

**Request Body:**
```json
{
  "name": "Vendedor Dux",
  "system_prompt": "Você é um vendedor especializado...",
  "model": "gpt-4o-mini",
  "temperature": 0.7,
  "max_tokens": 1000,
  "top_p": 1.0,
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0,
  "description": "Agente de vendas",
  "avatar_url": "https://...",
  "brand_color": "#4F46E5",
  "welcome_message": "Olá! Como posso ajudar?",
  "input_placeholder": "Digite sua mensagem..."
}
```

**Response:**
```json
{
  "id": "uuid",
  "slug": "vendedor-dux",  // ⬅️ Gerado automaticamente
  "name": "Vendedor Dux",
  "public_url": "https://chat.dominio.com/vendedor-dux",
  ...
}
```

**Notas:**
- Slug é gerado a partir do `name`
- Se slug já existe, adiciona contador: `vendedor-dux-2`
- Campos opcionais têm defaults seguros

---

### **PUT /api/agents/{agent_id}**
Atualiza agente existente.

**Parameters:**
- `agent_id` (UUID) - ID do agente

**Request Body:** (todos os campos opcionais)
```json
{
  "name": "Novo Nome",
  "system_prompt": "Novo prompt...",
  "temperature": 0.8,
  "is_active": false
}
```

**Response:** Agente atualizado

**Notas:**
- Se `name` muda, slug é regenerado
- Apenas campos enviados são atualizados

---

### **DELETE /api/agents/{agent_id}**
Desativa agente (**soft delete**).

**Parameters:**
- `agent_id` (UUID) - ID do agente

**Response:**
```json
{
  "message": "Agente desativado com sucesso",
  "agent_id": "uuid"
}
```

**Notas:**
- Define `is_active = false` e `status = archived`
- Não deleta do banco (reversível)
- Chat público retorna 404 para agentes inativos

---

## 🌐 Public API (SEM Autenticação)

### **GET /api/public/agents/{slug}**
Retorna configuração pública do agente.

**Parameters:**
- `slug` (string) - Identificador único do agente

**Response:**
```json
{
  "slug": "vendedor-dux",
  "name": "Vendedor Dux",
  "description": "Agente especializado em vendas",
  "avatar_url": "https://...",
  "brand_color": "#4F46E5",
  "welcome_message": "Olá! Como posso ajudar?",
  "input_placeholder": "Digite sua mensagem...",
  "meta_title": "Chat com Vendedor Dux",
  "meta_description": "Converse com nosso vendedor especializado",
  "og_image_url": "https://..."
}
```

**Segurança:**
- ❌ NÃO retorna `system_prompt`
- ❌ NÃO retorna parâmetros LLM
- ❌ NÃO retorna dados sensíveis
- ✅ Apenas dados necessários para UI

**Erros:**
- `404` - Agente não encontrado ou inativo

---

### **POST /api/public/agents/{slug}/chat**
Envia mensagem para o agente (chat público).

**Parameters:**
- `slug` (string) - Identificador único do agente

**Request Body:**
```json
{
  "message": "Olá, preciso de informações sobre produtos",
  "session_id": "optional-uuid-from-frontend"
}
```

**Response:**
```json
{
  "conversation_id": "uuid",
  "session_id": "uuid",
  "response": "Olá! Posso ajudar. Qual produto você procura?",
  "tokens": 45,
  "cost": 0.00001035,
  "processing_time": 1.52
}
```

**Como funciona:**
1. Frontend gera `session_id` (UUID) na primeira mensagem
2. Backend usa `public_{session_id}` como identificador
3. Todas as mensagens com mesmo `session_id` mantêm contexto
4. Frontend armazena `session_id` em localStorage

**Erros:**
- `404` - Agente não encontrado
- `403` - Agente não está ativo
- `500` - Erro ao processar mensagem

---

### **GET /api/public/agents/{slug}/history/{session_id}**
Retorna histórico da conversa.

**Parameters:**
- `slug` (string) - Identificador do agente
- `session_id` (UUID) - ID da sessão

**Response:**
```json
{
  "conversation_id": "uuid",
  "messages": [
    {
      "role": "user",
      "content": "Olá",
      "created_at": "2025-01-21T10:00:00Z"
    },
    {
      "role": "assistant",
      "content": "Olá! Como posso ajudar?",
      "created_at": "2025-01-21T10:00:01Z"
    }
  ]
}
```

---

## 💬 Chat API (Original - Ambos)

### **POST /api/chat**
Endpoint original de chat (mantido para compatibilidade).

**Request Body:**
```json
{
  "agent_id": "uuid",
  "user_identifier": "user@email.com",
  "message": "Olá",
  "channel": "web"
}
```

**Response:**
```json
{
  "conversation_id": "uuid",
  "response": "Olá! Como posso ajudar?",
  "tokens": 45,
  "cost": 0.00001035,
  "processing_time": 1.52
}
```

---

## 🏥 Health Check

### **GET /health**
Verifica status do sistema.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-01-21T10:00:00Z"
}
```

---

## 📊 Modelo de Dados

### Agent
```typescript
{
  id: UUID,
  slug: string,                    // URL pública única
  name: string,
  description?: string,
  avatar_url?: string,
  
  // Configuração LLM
  system_prompt: string,
  model: string,
  temperature: number,             // 0.0 - 2.0
  max_tokens: number,              // 1 - 4096
  top_p: number,                   // 0.0 - 1.0
  frequency_penalty: number,       // -2.0 - 2.0
  presence_penalty: number,        // -2.0 - 2.0
  
  // Features
  rag_enabled: boolean,
  function_calling_enabled: boolean,
  
  // Channels
  whatsapp_enabled: boolean,
  email_enabled: boolean,
  web_enabled: boolean,
  
  // Access Control
  is_active: boolean,
  allow_public_access: boolean,
  
  // Branding
  brand_color: string,             // Hex color
  welcome_message: string,
  input_placeholder: string,
  
  // SEO
  meta_title?: string,
  meta_description?: string,
  og_image_url?: string,
  
  // Timestamps
  created_at: DateTime,
  updated_at: DateTime
}
```

---

## 🔧 Exemplos de Uso

### Criar Agente e Obter URL Pública

```bash
# 1. Criar agente
curl -X POST https://api.seudominio.com/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vendedor Dux",
    "system_prompt": "Você é um vendedor especializado...",
    "temperature": 0.7
  }'

# Response:
# {
#   "id": "abc123",
#   "slug": "vendedor-dux",
#   ...
# }

# 2. URL pública gerada:
# https://chat.seudominio.com/vendedor-dux
```

### Chat Público (Frontend)

```typescript
// Frontend - Primeira mensagem
const sessionId = localStorage.getItem('session_id') || uuid();
localStorage.setItem('session_id', sessionId);

const response = await fetch(
  'https://api.seudominio.com/api/public/agents/vendedor-dux/chat',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: 'Olá, preciso de ajuda',
      session_id: sessionId
    })
  }
);

const data = await response.json();
// {
//   conversation_id: "...",
//   session_id: "...",
//   response: "Olá! Como posso ajudar?",
//   ...
// }
```

---

## 🚀 Migration

Execute antes de fazer deploy:

```bash
# Railway
psql $DATABASE_URL -f migration_v4.sql

# Local
psql -h localhost -U postgres -d agentes -f migration_v4.sql
```

---

## 🐛 Troubleshooting

### Erro: "Agente não encontrado" no chat público
- Verifique se `slug` está correto
- Confirme que `is_active = true`
- Confirme que `allow_public_access = true`

### Erro: "Slug já existe" ao criar agente
- Sistema adiciona contador automaticamente
- Ex: `vendedor-dux-2`, `vendedor-dux-3`

### Erro ao fazer migration
- Execute em ordem: adicionar colunas → índices → dados

---

## 📈 Próximos Passos

- [ ] Implementar autenticação JWT no Admin
- [ ] Adicionar rate limiting no Public
- [ ] Implementar RAG (upload de documentos)
- [ ] Analytics por agente
- [ ] Webhooks para clientes

---

**Última atualização:** 2025-01-21  
**Versão:** 4.0.0
