"""
LLM Service (OpenAI)
"""
import os
from openai import OpenAI
from typing import List, Dict
import logging

from utils import calculate_token_cost

logger = logging.getLogger(__name__)


class LLMService:
    """
    Serviço para interagir com OpenAI API
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 1500
    ) -> Dict:
        """
        Gerar resposta do LLM
        
        Returns:
            {
                "content": str,
                "tokens": int,
                "cost": float
            }
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            content = response.choices[0].message.content
            tokens = response.usage.total_tokens
            cost = calculate_token_cost(tokens, model)
            
            logger.info(f"LLM response: {tokens} tokens, €{cost:.4f}")
            
            return {
                "content": content,
                "tokens": tokens,
                "cost": cost
            }
            
        except Exception as e:
            logger.error(f"LLM error: {str(e)}")
            raise Exception(f"Erro ao chamar OpenAI API: {str(e)}")
