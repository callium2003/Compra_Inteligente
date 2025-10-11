"""
Normalizador de Lista de Compras
Converte texto livre em itens estruturados
"""
import re
from typing import List, Dict, Any

# Unidades conhecidas
UNITS = {
    'kg': 'kg', 'kilo': 'kg', 'kilos': 'kg', 'quilos': 'kg', 'quilo': 'kg',
    'g': 'g', 'grama': 'g', 'gramas': 'g',
    'l': 'l', 'litro': 'l', 'litros': 'l',
    'ml': 'ml', 'mililitro': 'ml', 'mililitros': 'ml',
    'un': 'un', 'unidade': 'un', 'unidades': 'un', 'und': 'un',
    'pc': 'un', 'pç': 'un', 'peça': 'un', 'peças': 'un',
    'cx': 'un', 'caixa': 'un', 'caixas': 'un',
    'pct': 'un', 'pacote': 'un', 'pacotes': 'un',
}

# Padrões de preferência
PREFERENCES = {
    'qualquer': 'any',
    'mais barato': 'cheapest',
    'barato': 'cheapest',
    'marca': 'exact_brand',
    'similar': 'similar',
}


def normalize_unit(unit_str: str) -> str:
    """Normaliza string de unidade para formato padrão"""
    unit_lower = unit_str.lower().strip()
    return UNITS.get(unit_lower, 'un')


def parse_quantity_and_size(text: str) -> tuple:
    """
    Extrai quantidade e tamanho do texto
    Exemplos:
    - "2 leite 1l" -> qty=2, size_value=1, size_unit='l'
    - "arroz 5kg" -> qty=1, size_value=5, size_unit='kg'
    - "3 ovos" -> qty=3, size_value=None, size_unit='un'
    """
    # Padrão: [quantidade] produto [tamanho][unidade]
    pattern = r'^(\d+(?:[.,]\d+)?)\s*(.+?)(?:\s+(\d+(?:[.,]\d+)?)\s*([a-zA-Zç]+))?$'
    match = re.match(pattern, text.strip())
    
    if match:
        qty_str, product, size_str, unit_str = match.groups()
        qty = float(qty_str.replace(',', '.'))
        
        if size_str and unit_str:
            size_value = float(size_str.replace(',', '.'))
            size_unit = normalize_unit(unit_str)
            return qty, product.strip(), size_value, size_unit
        else:
            return qty, product.strip(), None, 'un'
    
    # Padrão alternativo: produto [tamanho][unidade]
    pattern2 = r'^(.+?)\s+(\d+(?:[.,]\d+)?)\s*([a-zA-Zç]+)$'
    match2 = re.match(pattern2, text.strip())
    
    if match2:
        product, size_str, unit_str = match2.groups()
        size_value = float(size_str.replace(',', '.'))
        size_unit = normalize_unit(unit_str)
        return 1.0, product.strip(), size_value, size_unit
    
    # Sem tamanho especificado
    return 1.0, text.strip(), None, 'un'


def normalize_item(line: str) -> Dict[str, Any]:
    """
    Normaliza uma linha de texto em item estruturado
    """
    line = line.strip()
    
    if not line or line.startswith('#'):
        return None
    
    # Remover marcadores de lista
    line = re.sub(r'^[-*•]\s*', '', line)
    
    # Extrair notas entre parênteses
    notes = None
    notes_match = re.search(r'\(([^)]+)\)', line)
    if notes_match:
        notes = notes_match.group(1)
        line = line.replace(notes_match.group(0), '').strip()
    
    # Extrair marca se houver
    brand = None
    brand_match = re.search(r'\b(marca|marca:)\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$)', line, re.IGNORECASE)
    if brand_match:
        brand = brand_match.group(2).strip()
        line = line.replace(brand_match.group(0), '').strip()
    
    # Extrair preferência
    preference = 'any'
    for key, value in PREFERENCES.items():
        if key in line.lower():
            preference = value
            line = re.sub(rf'\b{key}\b', '', line, flags=re.IGNORECASE).strip()
            break
    
    # Parse quantidade e tamanho
    qty, product_name, size_value, size_unit = parse_quantity_and_size(line)
    
    return {
        'qty': qty,
        'product_name': product_name,
        'size_value': size_value,
        'size_unit': size_unit,
        'brand': brand,
        'preference': preference,
        'notes': notes
    }


def normalize_shopping_list(raw_text: str) -> List[Dict[str, Any]]:
    """
    Normaliza texto completo da lista de compras
    """
    lines = raw_text.split('\n')
    items = []
    
    for line in lines:
        item = normalize_item(line)
        if item:
            items.append(item)
    
    return items


# Exemplos de uso para testes
if __name__ == '__main__':
    test_text = """
    2 leite integral 1l
    arroz tipo 1 5kg
    3 ovos brancos
    feijão preto 1kg (marca Camil)
    café mais barato 500g
    açúcar cristal 2kg
    """
    
    result = normalize_shopping_list(test_text)
    for item in result:
        print(item)
