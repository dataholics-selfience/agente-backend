from openai import OpenAI
from typing import List, Dict, Optional, Generator
import time
from app.core.config import settings


class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Custos por 1M tokens (aproximado)
        self.pricing = {
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "gpt-4o": {"input": 2.50, "output": 10.00},
            "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        }
    
    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calcula custo em USD"""
        if model not in self.pricing:
            return 0.0
        
        input_cost = (input_tokens / 1_000_000) * self.pricing[model]["input"]
        output_cost = (output_tokens / 1_000_000) * self.pricing[model]["output"]
        
        return input_cost + output_cost
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
    ) -> Dict:
        """
        Envia mensagens para o LLM e retorna resposta com metadata
        
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
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
            )
            
            if stream:
                return self._handle_stream(response, model, start_time)
            
            # Extrai dados
            content = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            
            # Calcula custo
            cost = self.calculate_cost(model, input_tokens, output_tokens)
            
            # Tempo de processamento
            processing_time = time.time() - start_time
            
            return {
                "content": content,
                "tokens": total_tokens,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
                "processing_time": processing_time,
                "model": model,
            }
        
        except Exception as e:
            print(f"LLM Error: {e}")
            raise
    
    def _handle_stream(self, response, model: str, start_time: float) -> Generator:
        """Handle streaming response"""
        # TODO: Implementar streaming se necessário
        pass
    
    def create_embeddings(self, texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
        """
        Cria embeddings para RAG
        
        Args:
            texts: Lista de textos para embeddings
            model: Modelo de embeddings
        
        Returns:
            Lista de vetores de embeddings
        """
        try:
            response = self.client.embeddings.create(
                model=model,
                input=texts
            )
            
            return [item.embedding for item in response.data]
        
        except Exception as e:
            print(f"Embedding Error: {e}")
            raise


# Singleton
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
