"""
LLM Service - OpenAI Integration
"""
import os
import time
from openai import OpenAI
from typing import List, Dict

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LLMService:
    """Serviço para interação com modelos de linguagem"""
    
    @staticmethod
    def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
        """Calcula custo da chamada baseado no modelo"""
        
        # Preços por 1M tokens (Janeiro 2025)
        pricing = {
            "gpt-4o-mini": {"input": 0.150, "output": 0.600},
            "gpt-4o": {"input": 2.50, "output": 10.00},
            "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        }
        
        model_pricing = pricing.get(model, pricing["gpt-4o-mini"])
        
        input_cost = (input_tokens / 1_000_000) * model_pricing["input"]
        output_cost = (output_tokens / 1_000_000) * model_pricing["output"]
        
        return input_cost + output_cost
    
    @staticmethod
    async def generate_response(
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict:
        """
        Gera resposta usando OpenAI
        
        Returns:
            {
                "content": str,
                "tokens": int,
                "cost": float,
                "processing_time": float
            }
        """
        
        start_time = time.time()
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            processing_time = time.time() - start_time
            
            # Extrair dados da resposta
            content = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            
            # Calcular custo
            cost = LLMService.calculate_cost(model, input_tokens, output_tokens)
            
            return {
                "content": content,
                "tokens": total_tokens,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
                "processing_time": processing_time,
                "model": model
            }
            
        except Exception as e:
            raise Exception(f"Erro ao chamar OpenAI: {str(e)}")
