"""
LLM Service - OpenAI com LAZY LOADING
"""
import os
import time
from typing import List, Dict

_client = None

def get_openai_client():
    """Lazy loading do cliente OpenAI"""
    global _client
    if _client is None:
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não configurada!")
        _client = OpenAI(api_key=api_key)
    return _client

class LLMService:
    
    @staticmethod
    def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
        pricing = {
            "gpt-4o-mini": {"input": 0.150, "output": 0.600},
            "gpt-4o": {"input": 2.50, "output": 10.00},
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
        start_time = time.time()
        
        try:
            client = get_openai_client()
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            processing_time = time.time() - start_time
            
            content = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            
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
            raise Exception(f"Erro OpenAI: {str(e)}")
