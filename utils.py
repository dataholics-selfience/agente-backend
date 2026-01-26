from slugify import slugify
import re

def normalize_slug(slug: str) -> str:
    if not slug:
        return ""
    normalized = slugify(slug, separator='-', lowercase=True)
    normalized = re.sub(r'-+', '-', normalized)
    return normalized.strip('-')

def validate_slug(slug: str):
    if not slug:
        return False, "Slug cannot be empty"
    if not re.match(r'^[a-z0-9-]+$', slug):
        return False, "Slug can only contain lowercase letters, numbers, and hyphens"
    if slug.startswith('-') or slug.endswith('-'):
        return False, "Slug cannot start or end with hyphen"
    return True, None

def calculate_token_cost(tokens: int, model: str = "gpt-4o-mini") -> float:
    prices = {
        "gpt-4o-mini": 0.15 / 1_000_000,
        "gpt-4o": 5.00 / 1_000_000,
    }
    return tokens * prices.get(model.lower(), prices["gpt-4o-mini"])
