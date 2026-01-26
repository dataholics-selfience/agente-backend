"""
Utility Functions
"""
from slugify import slugify
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def normalize_slug(slug: str) -> str:
    """
    Normaliza slug para formato válido:
    - Remove espaços
    - Remove acentos
    - Lowercase
    - Apenas: a-z, 0-9, hífen
    
    Examples:
        normalize_slug("Vendedor DUX") → "vendedor-dux"
        normalize_slug("vendedor dux 2- teste") → "vendedor-dux-2-teste"
        normalize_slug("  test  ") → "test"
        normalize_slug("açúcar") → "acucar"
    """
    if not slug:
        return ""
    
    # Usar slugify para limpar
    normalized = slugify(
        slug,
        separator='-',
        lowercase=True,
        replacements=[
            (' ', '-'),    # Espaços → hífens
            ('_', '-'),    # Underscores → hífens
        ]
    )
    
    # Remove hífens duplicados
    while '--' in normalized:
        normalized = normalized.replace('--', '-')
    
    # Remove hífens no início/fim
    normalized = normalized.strip('-')
    
    return normalized


def generate_unique_slug(base_slug: str, existing_slugs: list[str]) -> str:
    """
    Gera slug único adicionando sufixo numérico se necessário
    
    Args:
        base_slug: Slug base
        existing_slugs: Lista de slugs já existentes
        
    Returns:
        Slug único
    """
    normalized = normalize_slug(base_slug)
    
    if normalized not in existing_slugs:
        return normalized
    
    # Adicionar sufixo numérico
    counter = 1
    while f"{normalized}-{counter}" in existing_slugs:
        counter += 1
    
    return f"{normalized}-{counter}"


def calculate_token_cost(tokens: int, model: str = "gpt-4o-mini") -> float:
    """
    Calcula custo aproximado baseado em tokens
    
    Args:
        tokens: Número de tokens
        model: Modelo usado
        
    Returns:
        Custo em euros
    """
    # Preços por 1M tokens (ajustar conforme OpenAI pricing)
    prices = {
        "gpt-4o-mini": {
            "input": 0.15 / 1_000_000,   # $0.15 per 1M tokens
            "output": 0.60 / 1_000_000    # $0.60 per 1M tokens
        },
        "gpt-4o": {
            "input": 2.50 / 1_000_000,
            "output": 10.00 / 1_000_000
        },
        "gpt-4": {
            "input": 30.00 / 1_000_000,
            "output": 60.00 / 1_000_000
        }
    }
    
    model_key = model.lower()
    if model_key not in prices:
        model_key = "gpt-4o-mini"  # Default
    
    # Assumindo metade input, metade output (aproximado)
    avg_price = (prices[model_key]["input"] + prices[model_key]["output"]) / 2
    
    return tokens * avg_price


def validate_slug(slug: str) -> tuple[bool, Optional[str]]:
    """
    Valida se slug está no formato correto
    
    Returns:
        (is_valid, error_message)
    """
    if not slug:
        return False, "Slug não pode ser vazio"
    
    if len(slug) < 3:
        return False, "Slug deve ter pelo menos 3 caracteres"
    
    if len(slug) > 100:
        return False, "Slug não pode ter mais de 100 caracteres"
    
    # Regex: apenas letras minúsculas, números e hífens
    import re
    if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', slug):
        return False, "Slug inválido. Use apenas letras minúsculas, números e hífens"
    
    return True, None
