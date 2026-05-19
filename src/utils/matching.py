import re
from difflib import SequenceMatcher

def calculate_similarity(a: str, b: str) -> float:
    """Calcula a similaridade entre duas strings (0 a 1)"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def clean_name(name: str) -> str:
    """Limpa o nome do produto para melhor comparação"""
    # Remove termos genéricos e unidades
    name = name.lower()
    name = re.sub(r'\d+\s*(l|ml|kg|g|un|unidade|litro|grama)', '', name)
    name = re.sub(r'[^\w\s]', '', name)
    return name.strip()

def get_best_match(target_name: str, products: list, threshold: float = 0.3, filters: dict = None):
    """
    Encontra o melhor produto em uma lista baseado em similaridade, preço e filtros.
    """
    if not products:
        return None
        
    filters = filters or {}
    brand_filter = filters.get('brand', '').lower()
    organic_only = filters.get('organic', False)
    
    target_clean = clean_name(target_name)
    target_keywords = set(target_clean.split())
    
    scored_products = []
    for p in products:
        p_name = p.get('name', '').lower()
        
        # Aplicar Filtro Orgânico
        if organic_only and 'orgânico' not in p_name and 'organico' not in p_name:
            continue
            
        # Aplicar Filtro de Marca
        if brand_filter and brand_filter not in p_name:
            continue
            
        p_clean = clean_name(p_name)
        p_keywords = set(p_clean.split())
        
        # Score de palavras-chave
        matches = target_keywords.intersection(p_keywords)
        keyword_score = len(matches) / len(target_keywords) if target_keywords else 0
        
        # Score de similaridade
        string_score = calculate_similarity(target_clean, p_clean)
        
        # Score final
        final_score = (keyword_score * 0.7) + (string_score * 0.3)
        
        if final_score >= threshold:
            scored_products.append((final_score, p))
            
    if not scored_products:
        # Se os filtros forem muito restritivos, tentamos sem filtros como fallback
        # ou retornamos o mais barato dos que sobraram
        if not products: return None
        return min(products, key=lambda x: x['price'])
        
    scored_products.sort(key=lambda x: (-x[0], x[1]['price']))
    return scored_products[0][1]
