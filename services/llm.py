import os
from openai import OpenAI
from utils import calculate_token_cost

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate(self, messages, model="gpt-4o-mini", temperature=0.7, max_tokens=1500):
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        content = response.choices[0].message.content
        tokens = response.usage.total_tokens
        cost = calculate_token_cost(tokens, model)
        return {"content": content, "tokens": tokens, "cost": cost}
