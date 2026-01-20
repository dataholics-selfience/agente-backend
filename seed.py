"""
Seed script - Criar agente inicial
"""
import sys
import uuid
from sqlalchemy.orm import Session

# Adicionar path
sys.path.insert(0, '/home/claude/agent-platform/backend')

from app.core.database import SessionLocal
from app.models import Agent


def seed_initial_agent():
    """Cria agente inicial para testes"""
    
    db: Session = SessionLocal()
    
    try:
        # Verificar se já existe algum agente
        existing = db.query(Agent).first()
        if existing:
            print(f"✅ Agente já existe: {existing.name} ({existing.id})")
            return
        
        # Criar agente de vendas
        agent = Agent(
            id=uuid.uuid4(),
            name="Assistente de Vendas",
            system_prompt="""Você é um assistente de vendas inteligente e prestável.

Seu objetivo é:
1. Cumprimentar o cliente de forma calorosa
2. Entender as necessidades dele
3. Fazer perguntas relevantes para qualificar o lead
4. Sugerir produtos/serviços adequados
5. Responder dúvidas com clareza
6. Incentivar o próximo passo (agendar reunião, fazer pedido, etc)

Sempre:
- Seja educado e profissional
- Use português de Portugal
- Seja conciso mas completo
- Demonstre entusiasmo genuíno
- Personalize as respostas

Nunca:
- Seja insistente demais
- Faça promessas que não pode cumprir
- Use linguagem técnica sem explicar
- Ignore as preocupações do cliente""",
            model="gpt-4o-mini",
            temperature=0.7,
            rag_enabled=False,
            whatsapp_enabled=False,
            email_enabled=False,
            is_active=True,
        )
        
        db.add(agent)
        db.commit()
        db.refresh(agent)
        
        print(f"✅ Agente criado com sucesso!")
        print(f"   ID: {agent.id}")
        print(f"   Nome: {agent.name}")
        print(f"   Modelo: {agent.model}")
        print(f"\n📋 Use este ID nos testes:")
        print(f"   {agent.id}")
        
    except Exception as e:
        print(f"❌ Erro ao criar agente: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_initial_agent()
