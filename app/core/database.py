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
            
            if result.fetchone()[0]:
                print("✅ Banco já inicializado")
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
                )
            """))
            
            # Criar tabela conversations
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
                    user_identifier VARCHAR(255) NOT NULL,
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
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_documents_agent_id ON documents(agent_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_channel_configs_agent_id ON channel_configs(agent_id)"))
            
            # Inserir agentes de exemplo
            conn.execute(text("""
                INSERT INTO agents (id, name, system_prompt, model, temperature, rag_enabled, whatsapp_enabled, email_enabled, status)
                SELECT 
                    '00000000-0000-0000-0000-000000000001'::UUID,
                    'Vendedor Inteligente',
                    'Você é um assistente de vendas profissional e educado.',
                    'gpt-4o-mini',
                    0.7,
                    FALSE,
                    FALSE,
                    FALSE,
                    'active'
                WHERE NOT EXISTS (SELECT 1 FROM agents WHERE id = '00000000-0000-0000-0000-000000000001'::UUID)
            """))
            
            conn.execute(text("""
                INSERT INTO agents (id, name, system_prompt, model, temperature, rag_enabled, whatsapp_enabled, email_enabled, status)
                SELECT 
                    '00000000-0000-0000-0000-000000000002'::UUID,
                    'Suporte Técnico',
                    'Você é um assistente de suporte técnico prestativo.',
                    'gpt-4o-mini',
                    0.5,
                    FALSE,
                    FALSE,
                    FALSE,
                    'active'
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
