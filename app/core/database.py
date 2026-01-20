"""
Database connection and initialization
"""
import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Database URL do Railway
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL não configurada!")
    sys.exit(1)

# Criar engine SQLAlchemy
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

@contextmanager
def get_db():
    """Context manager para sessões do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """
    Inicializa o banco de dados na primeira execução
    Cria tabelas e insere dados iniciais (seed)
    """
    
    print("🔍 Verificando estado do banco de dados...")
    
    try:
        with engine.connect() as conn:
            # Verificar se tabela agents existe
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'agents'
                );
            """))
            
            already_initialized = result.fetchone()[0]
            
            if already_initialized:
                print("✅ Banco de dados já inicializado")
                return
            
            print("🚀 Primeira execução detectada. Criando schema...")
            
            # Ler e executar script SQL
            sql_file = Path(__file__).parent.parent.parent / "init_database.sql"
            
            if not sql_file.exists():
                print(f"❌ Script SQL não encontrado: {sql_file}")
                raise FileNotFoundError(f"init_database.sql não encontrado em {sql_file}")
            
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            # Executar script (dividir por comandos individuais)
            statements = [s.strip() for s in sql_script.split(';') if s.strip()]
            
            for statement in statements:
                if statement:
                    try:
                        conn.execute(text(statement))
                    except Exception as e:
                        # Ignorar erros de "já existe" mas logar outros
                        if "already exists" not in str(e):
                            print(f"⚠️  Aviso ao executar SQL: {e}")
            
            conn.commit()
            
            print("✅ Schema criado com sucesso!")
            
            # Verificar agentes criados
            result = conn.execute(text("SELECT COUNT(*) FROM agents"))
            agent_count = result.fetchone()[0]
            print(f"🤖 {agent_count} agente(s) criado(s)")
            
    except Exception as e:
        print(f"❌ Erro fatal na inicialização: {e}")
        import traceback
        traceback.print_exc()
        raise

def get_db_dependency():
    """Dependency para FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
