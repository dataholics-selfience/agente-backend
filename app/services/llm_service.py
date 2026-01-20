"""
LLM Service - Wrapper para OpenAI e outros LLMs
"""
from openai import OpenAI, AsyncOpenAI
from typing import List, Dict, Optional, AsyncGenerator
import time
from app.core.config import settings
from loguru import logger

# Preços por 1M tokens (em USD)
PRICING = {
    "gpt-4o-mini": {
        "input": 0.15 / 1_000_000,
        "output": 0.60 / 1_000_000,
    },
    "gpt-4o": {
        "input": 2.50 / 1_000_000,
        "output": 10.00 / 1_000_000,
    },
    "gpt-4-turbo": {
        "input": 10.00 / 1_000_000,
        "output": 30.00 / 1_000_000,
    },
}


class LLMService:
    """Serviço para interagir com LLMs"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.async_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    def calculate_cost(
        self, 
        model: str, 
        input_tokens: int, 
        output_tokens: int
    ) -> float:
        """Calcula custo em USD baseado em tokens"""
        pricing = PRICING.get(model, PRICING["gpt-4o-mini"])
        input_cost = input_tokens * pricing["input"]
        output_cost = output_tokens * pricing["output"]
        return input_cost + output_cost
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        stream: bool = False,
    ) -> Dict:
        """
        Chama LLM de forma assíncrona
        
        Args:
            messages: Lista de mensagens [{role: str, content: str}]
            model: Modelo a usar (default: settings.OPENAI_MODEL)
            temperature: Criatividade (0-2)
            max_tokens: Máximo de tokens na resposta
            stream: Se True, retorna generator
        
        Returns:
            {
                "content": str,
                "tokens_used": int,
                "cost": float,
                "model": str,
                "time": float
            }
        """
        if model is None:
            model = settings.OPENAI_MODEL
        
        start_time = time.time()
        
        try:
            logger.info(f"Calling {model} with {len(messages)} messages")
            
            response = await self.async_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
            )
            
            if stream:
                # Se stream, retornar generator
                return self._handle_stream(response, model, start_time)
            
            # Extrair dados
            content = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            
            # Calcular custo
            cost = self.calculate_cost(model, input_tokens, output_tokens)
            
            elapsed_time = time.time() - start_time
            
            logger.info(
                f"LLM response: {total_tokens} tokens, "
                f"${cost:.4f}, {elapsed_time:.2f}s"
            )
            
            return {
                "content": content,
                "tokens_used": total_tokens,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
                "model": model,
                "time": elapsed_time,
            }
            
        except Exception as e:
            logger.error(f"LLM error: {e}")
            
            # TODO: Implementar fallback para Groq se OpenAI falhar
            raise
    
    async def _handle_stream(
        self, 
        stream, 
        model: str, 
        start_time: float
    ) -> AsyncGenerator:
        """Handle streaming responses"""
        full_content = ""
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_content += content
                yield {
                    "content": content,
                    "done": False,
                }
        
        # Final chunk com metadata
        elapsed_time = time.time() - start_time
        yield {
            "content": "",
            "done": True,
            "full_content": full_content,
            "time": elapsed_time,
        }
    
    async def generate_embedding(
        self, 
        text: str,
        model: str = None
    ) -> List[float]:
        """
        Gera embedding de texto
        
        Args:
            text: Texto para embedar
            model: Modelo (default: settings.OPENAI_EMBEDDING_MODEL)
        
        Returns:
            Lista de floats (embedding vector)
        """
        if model is None:
            model = settings.OPENAI_EMBEDDING_MODEL
        
        try:
            response = await self.async_client.embeddings.create(
                model=model,
                input=text,
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            raise


# Instância global
llm_service = LLMService()
