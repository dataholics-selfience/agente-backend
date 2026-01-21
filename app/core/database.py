"""
Database - Inicialização AUTOMÁTICA e ROBUSTA
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL não configurada!")
    sys.exit(1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def run_migration_v4(conn):
    """Migration v4.0.0 - Adiciona campos para Dual-Frontend"""
    
    print("  📦 Adicionando colunas novas...")
    
    # Adicionar todas as colunas novas
    migrations = [
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS slug VARCHAR(100)",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS description TEXT",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS avatar_url VARCHAR(500)",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS max_tokens INTEGER DEFAULT 1000",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS top_p FLOAT DEFAULT 1.0",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS frequency_penalty FLOAT DEFAULT 0.0",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS presence_penalty FLOAT DEFAULT 0.0",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS function_calling_enabled BOOLEAN DEFAULT FALSE",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS whatsapp_number VARCHAR(20)",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS email_address VARCHAR(200)",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS web_enabled BOOLEAN DEFAULT TRUE",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS allow_public_access BOOLEAN DEFAULT TRUE",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS brand_color VARCHAR(7) DEFAULT '#4F46E5'",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS welcome_message TEXT DEFAULT 'Olá! Como posso ajudar?'",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS input_placeholder VARCHAR(100) DEFAULT 'Digite sua mensagem...'",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS meta_title VARCHAR(200)",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS meta_description VARCHAR(500)",
        "ALTER TABLE agents ADD COLUMN IF NOT EXISTS og_image_url VARCHAR(500)",
        "ALTER TABLE conversations ADD COLUMN IF NOT EXISTS session_id UUID",
    ]
    
    for sql in migrations:
        try:
            conn.execute(text(sql))
        except Exception as e:
            print(f"    ⚠️ Erro (não crítico): {e}")
    
    print("  🔧 Gerando slugs para agentes existentes...")
    
    # Gerar slugs
    conn.execute(text("""
        UPDATE agents 
        SET slug = LOWER(
            REGEXP_REPLACE(
                REGEXP_REPLACE(name, '[^a-zA-Z0-9\\s-]', '', 'g'), 
                '\\s+', 
                '-', 
                'g'
            )
        )
        WHERE slug IS NULL
    """))
    
    print("  🔍 Garantindo slugs únicos...")
    
    # Garantir slugs únicos
    conn.execute(text("""
        WITH ranked AS (
            SELECT 
                id, 
                slug,
                ROW_NUMBER() OVER (PARTITION BY slug ORDER BY created_at) as rn
            FROM agents
            WHERE slug IS NOT NULL
        )
        UPDATE agents
        SET slug = ranked.slug || '-' || ranked.rn
        FROM ranked
        WHERE agents.id = ranked.id 
        AND ranked.rn > 1
    """))
    
    print("  📊 Criando índices...")
    
    # Criar índices
    indices = [
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_agents_slug_unique ON agents(slug)",
        "CREATE INDEX IF NOT EXISTS idx_agents_is_active ON agents(is_active)",
        "CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id)",
    ]
    
    for sql in indices:
        try:
            conn.execute(text(sql))
        except Exception as e:
            print(f"    ⚠️ Erro (não crítico): {e}")
    
    print("  🎨 Preenchendo valores padrão...")
    
    # Preencher defaults
    defaults = [
        "UPDATE agents SET is_active = TRUE WHERE is_active IS NULL",
        "UPDATE agents SET allow_public_access = TRUE WHERE allow_public_access IS NULL",
        "UPDATE agents SET web_enabled = TRUE WHERE web_enabled IS NULL",
        "UPDATE agents SET brand_color = '#4F46E5' WHERE brand_color IS NULL",
        "UPDATE agents SET welcome_message = 'Olá! Como posso ajudar?' WHERE welcome_message IS NULL",
        "UPDATE agents SET input_placeholder = 'Digite sua mensagem...' WHERE input_placeholder IS NULL",
        "UPDATE agents SET max_tokens = 1000 WHERE max_tokens IS NULL",
        "UPDATE agents SET top_p = 1.0 WHERE top_p IS NULL",
        "UPDATE agents SET frequency_penalty = 0.0 WHERE frequency_penalty IS NULL",
        "UPDATE agents SET presence_penalty = 0.0 WHERE presence_penalty IS NULL",
    ]
    
    for sql in defaults:
        try:
            conn.execute(text(sql))
        except Exception as e:
            print(f"    ⚠️ Erro (não crítico): {e}")
    
    conn.commit()
    
    print("  ✅ Migration v4.0.0 concluída!")

def init_database():
    """Inicializa banco de dados com SQL inline"""
    
    print("🔍 Verificando banco de dados...")
    
    try:
        with engine.connect() as conn:
            # Verificar se já foi inicializado
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'agents'
                );
            """))
            
            table_exists = result.fetchone()[0]
            
            if table_exists:
                print("✅ Banco já inicializado")
                
                # 🆕 MIGRATION AUTOMÁTICA v4.0.0
                print("🔄 Verificando se migration v4 é necessária...")
                
                # Verificar se coluna slug existe
                result = conn.execute(text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.columns 
                        WHERE table_name = 'agents' 
                        AND column_name = 'slug'
                    );
                """))
                
                slug_exists = result.fetchone()[0]
                
                if not slug_exists:
                    print("🚀 Executando migration v4.0.0...")
                    run_migration_v4(conn)
                else:
                    print("✅ Migration v4 já aplicada")
                
                result = conn.execute(text("SELECT COUNT(*) FROM agents"))
                print(f"🤖 {result.fetchone()[0]} agente(s) no banco")
                return
            
            print("🚀 Criando schema do banco de dados...")
            
            # Criar tipos ENUM
            conn.execute(text("""
                DO $$ BEGIN
                    CREATE TYPE agentstatus AS ENUM ('active', 'inactive', 'archived');
                EXCEPTION WHEN duplicate_object THEN null;
                END $$;
            """))
            
            conn.execute(text("""
                DO $$ BEGIN
                    CREATE TYPE conversationstatus AS ENUM ('active', 'paused', 'closed');
                EXCEPTION WHEN duplicate_object THEN null;
                END $$;
            """))
            
            conn.execute(text("""
                DO $$ BEGIN
                    CREATE TYPE messagerole AS ENUM ('user', 'assistant', 'system');
                EXCEPTION WHEN duplicate_object THEN null;
                END $$;
            """))
            
            # Criar tabela agents
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS agents (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    slug VARCHAR(100) UNIQUE,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    avatar_url VARCHAR(500),
                    system_prompt TEXT NOT NULL,
                    model VARCHAR(100) NOT NULL DEFAULT 'gpt-4o-mini',
                    temperature FLOAT NOT NULL DEFAULT 0.7,
                    max_tokens INTEGER NOT NULL DEFAULT 1000,
                    top_p FLOAT NOT NULL DEFAULT 1.0,
                    frequency_penalty FLOAT NOT NULL DEFAULT 0.0,
                    presence_penalty FLOAT NOT NULL DEFAULT 0.0,
                    rag_enabled BOOLEAN NOT NULL DEFAULT FALSE,
                    function_calling_enabled BOOLEAN NOT NULL DEFAULT FALSE,
                    whatsapp_enabled BOOLEAN NOT NULL DEFAULT FALSE,
                    whatsapp_number VARCHAR(20),
                    email_enabled BOOLEAN NOT NULL DEFAULT FALSE,
                    email_address VARCHAR(200),
                    web_enabled BOOLEAN NOT NULL DEFAULT TRUE,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    allow_public_access BOOLEAN NOT NULL DEFAULT TRUE,
                    brand_color VARCHAR(7) NOT NULL DEFAULT '#4F46E5',
                    welcome_message TEXT NOT NULL DEFAULT 'Olá! Como posso ajudar?',
                    input_placeholder VARCHAR(100) NOT NULL DEFAULT 'Digite sua mensagem...',
                    meta_title VARCHAR(200),
                    meta_description VARCHAR(500),
                    og_image_url VARCHAR(500),
                    status agentstatus NOT NULL DEFAULT 'active',
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Criar tabela conversations
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
                    user_identifier VARCHAR(255) NOT NULL,
                    session_id UUID,
                    channel VARCHAR(50) NOT NULL DEFAULT 'web',
                    status conversationstatus NOT NULL DEFAULT 'active',
                    extra_data JSONB DEFAULT '{}'::jsonb,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Criar tabela messages
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS messages (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
                    role messagerole NOT NULL,
                    content TEXT NOT NULL,
                    tokens INTEGER DEFAULT 0,
                    cost FLOAT DEFAULT 0.0,
                    processing_time FLOAT DEFAULT 0.0,
                    extra_data JSONB DEFAULT '{}'::jsonb,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Criar tabela documents
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS documents (
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
                )
            """))
            
            # Criar tabela channel_configs
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS channel_configs (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
                    channel VARCHAR(50) NOT NULL,
                    config JSONB DEFAULT '{}'::jsonb,
                    enabled BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Criar índices
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_conversations_agent_id ON conversations(agent_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_identifier)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_documents_agent_id ON documents(agent_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_channel_configs_agent_id ON channel_configs(agent_id)"))
            conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS idx_agents_slug_unique ON agents(slug)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_agents_is_active ON agents(is_active)"))
            
            # Inserir agentes de exemplo
            conn.execute(text("""
                INSERT INTO agents (
                    id, slug, name, system_prompt, model, temperature, 
                    rag_enabled, whatsapp_enabled, email_enabled, status,
                    is_active, allow_public_access, brand_color, 
                    welcome_message, input_placeholder
                )
                SELECT 
                    '00000000-0000-0000-0000-000000000001'::UUID,
                    'vendedor-inteligente',
                    'Vendedor Inteligente',
                    'Você é um assistente de vendas profissional e educado.',
                    'gpt-4o-mini',
                    0.7,
                    FALSE,
                    FALSE,
                    FALSE,
                    'active',
                    TRUE,
                    TRUE,
                    '#4F46E5',
                    'Olá! Como posso ajudar com suas vendas?',
                    'Digite sua pergunta...'
                WHERE NOT EXISTS (SELECT 1 FROM agents WHERE id = '00000000-0000-0000-0000-000000000001'::UUID)
            """))
            
            conn.execute(text("""
                INSERT INTO agents (
                    id, slug, name, system_prompt, model, temperature, 
                    rag_enabled, whatsapp_enabled, email_enabled, status,
                    is_active, allow_public_access, brand_color,
                    welcome_message, input_placeholder
                )
                SELECT 
                    '00000000-0000-0000-0000-000000000002'::UUID,
                    'suporte-tecnico',
                    'Suporte Técnico',
                    'Você é um assistente de suporte técnico prestativo.',
                    'gpt-4o-mini',
                    0.5,
                    FALSE,
                    FALSE,
                    FALSE,
                    'active',
                    TRUE,
                    TRUE,
                    '#10B981',
                    'Olá! Como posso ajudar com suporte?',
                    'Descreva seu problema...'
                WHERE NOT EXISTS (SELECT 1 FROM agents WHERE id = '00000000-0000-0000-0000-000000000002'::UUID)
            """))
            
            conn.commit()
            
            print("✅ Schema criado com sucesso!")
            
            result = conn.execute(text("SELECT COUNT(*) FROM agents"))
            print(f"🤖 {result.fetchone()[0]} agente(s) criado(s)")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
