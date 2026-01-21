-- Quick Migration v4.0.0
-- Execute ESTE arquivo primeiro!

-- Adicionar coluna slug (pode ser NULL temporariamente)
ALTER TABLE agents ADD COLUMN IF NOT EXISTS slug VARCHAR(100);

-- Adicionar outros campos essenciais
ALTER TABLE agents ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS avatar_url VARCHAR(500);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS max_tokens INTEGER DEFAULT 1000;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS top_p FLOAT DEFAULT 1.0;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS frequency_penalty FLOAT DEFAULT 0.0;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS presence_penalty FLOAT DEFAULT 0.0;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS function_calling_enabled BOOLEAN DEFAULT FALSE;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS whatsapp_number VARCHAR(20);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS email_address VARCHAR(200);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS web_enabled BOOLEAN DEFAULT TRUE;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS allow_public_access BOOLEAN DEFAULT TRUE;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS brand_color VARCHAR(7) DEFAULT '#4F46E5';
ALTER TABLE agents ADD COLUMN IF NOT EXISTS welcome_message TEXT DEFAULT 'Olá! Como posso ajudar?';
ALTER TABLE agents ADD COLUMN IF NOT EXISTS input_placeholder VARCHAR(100) DEFAULT 'Digite sua mensagem...';
ALTER TABLE agents ADD COLUMN IF NOT EXISTS meta_title VARCHAR(200);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS meta_description VARCHAR(500);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS og_image_url VARCHAR(500);

-- Adicionar session_id em conversations
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS session_id UUID;

-- Gerar slugs para agentes existentes
UPDATE agents 
SET slug = LOWER(REGEXP_REPLACE(REGEXP_REPLACE(name, '[^a-zA-Z0-9\s-]', '', 'g'), '\s+', '-', 'g'))
WHERE slug IS NULL;

-- Garantir slugs únicos
DO $$
DECLARE
    rec RECORD;
    new_slug TEXT;
    counter INT;
BEGIN
    FOR rec IN 
        SELECT id, slug, ROW_NUMBER() OVER (PARTITION BY slug ORDER BY created_at) as rn
        FROM agents
        WHERE slug IS NOT NULL
    LOOP
        IF rec.rn > 1 THEN
            counter := rec.rn;
            new_slug := rec.slug || '-' || counter::TEXT;
            UPDATE agents SET slug = new_slug WHERE id = rec.id;
        END IF;
    END LOOP;
END $$;

-- Criar índice único em slug
CREATE UNIQUE INDEX IF NOT EXISTS idx_agents_slug_unique ON agents(slug);
CREATE INDEX IF NOT EXISTS idx_agents_is_active ON agents(is_active);
CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id);

-- Preencher valores padrão para campos obrigatórios
UPDATE agents SET is_active = TRUE WHERE is_active IS NULL;
UPDATE agents SET allow_public_access = TRUE WHERE allow_public_access IS NULL;
UPDATE agents SET web_enabled = TRUE WHERE web_enabled IS NULL;
UPDATE agents SET brand_color = '#4F46E5' WHERE brand_color IS NULL;
UPDATE agents SET welcome_message = 'Olá! Como posso ajudar?' WHERE welcome_message IS NULL;
UPDATE agents SET input_placeholder = 'Digite sua mensagem...' WHERE input_placeholder IS NULL;
UPDATE agents SET max_tokens = 1000 WHERE max_tokens IS NULL;
UPDATE agents SET top_p = 1.0 WHERE top_p IS NULL;
UPDATE agents SET frequency_penalty = 0.0 WHERE frequency_penalty IS NULL;
UPDATE agents SET presence_penalty = 0.0 WHERE presence_penalty IS NULL;

COMMIT;

-- Verificação
SELECT 
    COUNT(*) as total_agents,
    COUNT(DISTINCT slug) as unique_slugs,
    COUNT(*) FILTER (WHERE slug IS NULL) as null_slugs
FROM agents;
