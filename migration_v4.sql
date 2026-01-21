-- Migration: Adicionar campos Dual-Frontend
-- Versão: 4.0.0
-- Data: 2025-01-21

-- ============================================
-- AGENTS TABLE - Novos campos
-- ============================================

-- Campos de identificação pública
ALTER TABLE agents ADD COLUMN IF NOT EXISTS slug VARCHAR(100) UNIQUE;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS avatar_url VARCHAR(500);

-- Parâmetros LLM adicionais
ALTER TABLE agents ADD COLUMN IF NOT EXISTS max_tokens INTEGER NOT NULL DEFAULT 1000;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS top_p FLOAT NOT NULL DEFAULT 1.0;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS frequency_penalty FLOAT NOT NULL DEFAULT 0.0;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS presence_penalty FLOAT NOT NULL DEFAULT 0.0;

-- Features
ALTER TABLE agents ADD COLUMN IF NOT EXISTS function_calling_enabled BOOLEAN NOT NULL DEFAULT FALSE;

-- Channels - campos adicionais
ALTER TABLE agents ADD COLUMN IF NOT EXISTS whatsapp_number VARCHAR(20);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS email_address VARCHAR(200);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS web_enabled BOOLEAN NOT NULL DEFAULT TRUE;

-- Public Access Control
ALTER TABLE agents ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS allow_public_access BOOLEAN NOT NULL DEFAULT TRUE;

-- Customização White-label
ALTER TABLE agents ADD COLUMN IF NOT EXISTS brand_color VARCHAR(7) NOT NULL DEFAULT '#4F46E5';
ALTER TABLE agents ADD COLUMN IF NOT EXISTS welcome_message TEXT NOT NULL DEFAULT 'Olá! Como posso ajudar?';
ALTER TABLE agents ADD COLUMN IF NOT EXISTS input_placeholder VARCHAR(100) NOT NULL DEFAULT 'Digite sua mensagem...';

-- SEO
ALTER TABLE agents ADD COLUMN IF NOT EXISTS meta_title VARCHAR(200);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS meta_description VARCHAR(500);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS og_image_url VARCHAR(500);

-- ============================================
-- CONVERSATIONS TABLE
-- ============================================

-- Session ID para chat público
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS session_id UUID;

-- ============================================
-- INDICES para performance
-- ============================================

CREATE INDEX IF NOT EXISTS idx_agents_slug ON agents(slug);
CREATE INDEX IF NOT EXISTS idx_agents_is_active ON agents(is_active);
CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id);

-- ============================================
-- MIGRATION de dados existentes
-- ============================================

-- Gera slug para agentes existentes que não têm
UPDATE agents 
SET slug = LOWER(REGEXP_REPLACE(name, '[^a-zA-Z0-9\s-]', '', 'g'))
WHERE slug IS NULL;

-- Garante slugs únicos
WITH numbered_agents AS (
    SELECT 
        id,
        slug,
        ROW_NUMBER() OVER (PARTITION BY slug ORDER BY created_at) as rn
    FROM agents
    WHERE slug IS NOT NULL
)
UPDATE agents a
SET slug = CONCAT(na.slug, '-', na.rn)
FROM numbered_agents na
WHERE a.id = na.id AND na.rn > 1;

-- Ativa novos campos booleanos para agentes existentes
UPDATE agents 
SET 
    is_active = TRUE,
    allow_public_access = TRUE,
    web_enabled = TRUE
WHERE is_active IS NULL;

COMMIT;
