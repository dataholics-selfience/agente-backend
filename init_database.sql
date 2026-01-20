-- ================================================================
-- SCRIPT DE INICIALIZAÇÃO DO BANCO DE DADOS
-- Railway PostgreSQL - Execução Direta
-- ================================================================

-- Limpar tabelas existentes (se existirem)
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
DROP TABLE IF EXISTS documents CASCADE;
DROP TABLE IF EXISTS channel_configs CASCADE;
DROP TABLE IF EXISTS agents CASCADE;
DROP TABLE IF EXISTS alembic_version CASCADE;

-- Limpar tipos ENUM (se existirem)
DROP TYPE IF EXISTS agentstatus CASCADE;
DROP TYPE IF EXISTS conversationstatus CASCADE;
DROP TYPE IF EXISTS messagerole CASCADE;

-- ================================================================
-- CRIAR TIPOS ENUM
-- ================================================================

CREATE TYPE agentstatus AS ENUM ('active', 'inactive', 'archived');
CREATE TYPE conversationstatus AS ENUM ('active', 'paused', 'closed');
CREATE TYPE messagerole AS ENUM ('user', 'assistant', 'system');

-- ================================================================
-- CRIAR TABELAS
-- ================================================================

-- Tabela: agents
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    system_prompt TEXT NOT NULL,
    model VARCHAR(100) NOT NULL DEFAULT 'gpt-4o-mini',
    temperature FLOAT NOT NULL DEFAULT 0.7,
    rag_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    whatsapp_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    email_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    status agentstatus NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: conversations
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    user_identifier VARCHAR(255) NOT NULL,
    channel VARCHAR(50) NOT NULL DEFAULT 'web',
    status conversationstatus NOT NULL DEFAULT 'active',
    extra_data JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: messages
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role messagerole NOT NULL,
    content TEXT NOT NULL,
    tokens INTEGER DEFAULT 0,
    cost FLOAT DEFAULT 0.0,
    processing_time FLOAT DEFAULT 0.0,
    extra_data JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: documents
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    file_size INTEGER,
    status VARCHAR(50) NOT NULL DEFAULT 'processing',
    chunks_count INTEGER DEFAULT 0,
    extra_data JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: channel_configs
CREATE TABLE channel_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    channel VARCHAR(50) NOT NULL,
    config JSONB DEFAULT '{}'::jsonb,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ================================================================
-- CRIAR ÍNDICES PARA PERFORMANCE
-- ================================================================

CREATE INDEX idx_conversations_agent_id ON conversations(agent_id);
CREATE INDEX idx_conversations_user_identifier ON conversations(user_identifier);
CREATE INDEX idx_conversations_status ON conversations(status);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_documents_agent_id ON documents(agent_id);
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_channel_configs_agent_id ON channel_configs(agent_id);
CREATE INDEX idx_channel_configs_channel ON channel_configs(channel);

-- ================================================================
-- TABELA ALEMBIC (para controle de migrations)
-- ================================================================

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL PRIMARY KEY
);

INSERT INTO alembic_version (version_num) VALUES ('001_initial_schema');

-- ================================================================
-- INSERIR DADOS INICIAIS (SEED)
-- ================================================================

-- Inserir agente de exemplo
INSERT INTO agents (id, name, system_prompt, model, temperature, rag_enabled, whatsapp_enabled, email_enabled, status)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'Vendedor Inteligente',
    'Você é um assistente de vendas profissional e educado. Seu objetivo é qualificar leads, entender necessidades do cliente e conduzir conversas comerciais de forma natural. Seja objetivo, faça perguntas relevantes e sempre mantenha um tom amigável.',
    'gpt-4o-mini',
    0.7,
    FALSE,
    FALSE,
    FALSE,
    'active'
);

-- Inserir agente de suporte
INSERT INTO agents (id, name, system_prompt, model, temperature, rag_enabled, whatsapp_enabled, email_enabled, status)
VALUES (
    '00000000-0000-0000-0000-000000000002',
    'Suporte Técnico',
    'Você é um assistente de suporte técnico prestativo e paciente. Seu objetivo é resolver problemas dos clientes de forma clara e eficiente. Faça perguntas para entender o problema, forneça soluções passo a passo e sempre confirme se a solução funcionou.',
    'gpt-4o-mini',
    0.5,
    FALSE,
    FALSE,
    FALSE,
    'active'
);

-- ================================================================
-- VERIFICAÇÃO FINAL
-- ================================================================

-- Mostrar todas as tabelas criadas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Mostrar contagem de agentes criados
SELECT COUNT(*) as total_agents FROM agents;

-- ================================================================
-- FIM DO SCRIPT
-- ================================================================
