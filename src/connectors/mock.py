"""
Conectores mock para Mambo e Mercado Livre
(até que possamos implementar scraping real com autenticação)
"""
import logging
import random
from typing import List, Dict, Optional
from .base import SupermarketConnector

logger = logging.getLogger(__name__)


class MamboConnector(SupermarketConnector):
    """Conector mock para Mambo (requer seleção de loja)"""
    
    def __init__(self):
        super().__init__(
            name="Mambo",
            base_url="https://www.mambo.com.br"
        )
    
    def search(self, product_name: str, cep: Optional[str] = None) -> List[Dict]:
        """
        Busca mock no Mambo
        
        Nota: O site Mambo requer seleção de loja antes de buscar produtos.
        Por enquanto, retornamos preços mock baseados em variação realista.
        """
        logger.info(f"Mambo (mock): Buscando '{product_name}'")
        
        # Gerar preço mock baseado em hash do nome do produto
        # Isso garante consistência entre buscas
        seed = sum(ord(c) for c in product_name.lower())
        random.seed(seed + 2)  # +2 para diferenciar do Extra
        
        # Preço base entre 3 e 15 reais
        base_price = random.uniform(3.0, 15.0)
        
        # Extrair tamanho do nome
        size_value, size_unit = self.extract_size(product_name)
        
        return [{
            'name': f"{product_name.title()} - Mambo",
            'price': round(base_price, 2),
            'url': f"{self.base_url}/produto/{product_name.lower().replace(' ', '-')}",
            'store': self.name,
            'size_value': size_value,
            'size_unit': size_unit,
            'mock': True
        }]
    
    def get_product_details(self, product_url: str) -> Dict:
        """Retorna detalhes mock"""
        return {
            'url': product_url,
            'store': self.name,
            'mock': True
        }


class MercadoLivreConnector(SupermarketConnector):
    """Conector mock para Mercado Livre (requer login)"""
    
    def __init__(self):
        super().__init__(
            name="Mercado Livre",
            base_url="https://www.mercadolivre.com.br"
        )
    
    def search(self, product_name: str, cep: Optional[str] = None) -> List[Dict]:
        """
        Busca mock no Mercado Livre
        
        Nota: O site requer login para acessar o supermercado.
        Por enquanto, retornamos preços mock baseados em variação realista.
        """
        logger.info(f"Mercado Livre (mock): Buscando '{product_name}'")
        
        # Gerar preço mock baseado em hash do nome do produto
        seed = sum(ord(c) for c in product_name.lower())
        random.seed(seed + 3)  # +3 para diferenciar dos outros
        
        # Mercado Livre tende a ter preços um pouco mais altos
        base_price = random.uniform(4.0, 16.0)
        
        # Extrair tamanho do nome
        size_value, size_unit = self.extract_size(product_name)
        
        return [{
            'name': f"{product_name.title()} - ML",
            'price': round(base_price, 2),
            'url': f"{self.base_url}/supermercado/market/{product_name.lower().replace(' ', '-')}",
            'store': self.name,
            'size_value': size_value,
            'size_unit': size_unit,
            'mock': True
        }]
    
    def get_product_details(self, product_url: str) -> Dict:
        """Retorna detalhes mock"""
        return {
            'url': product_url,
            'store': self.name,
            'mock': True
        }
