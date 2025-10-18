"""
Conector para Mercado Livre (API)
"""
import logging
from typing import List, Dict, Optional
from .base import SupermarketConnector

logger = logging.getLogger(__name__)


class MercadoLivreConnector(SupermarketConnector):
    """Conector para buscar produtos no Mercado Livre"""

    def __init__(self):
        super().__init__(
            name="Mercado Livre",
            # A URL base da API é diferente do site principal
            base_url="https://api.mercadolibre.com"
        )
        self.use_mock = False

    def search(self, product_name: str, cep: Optional[str] = None) -> List[Dict]:
        """
        Busca um produto na API do Mercado Livre.

        Args:
            product_name: Nome do produto a ser buscado.
            cep: CEP (não utilizado no momento).

        Returns:
            Lista de produtos encontrados.
        """
        if self.use_mock:
            return self._search_mock(product_name)

        try:
            # O endpoint de busca do Mercado Livre para o Brasil (MLB)
            search_url = f"{self.base_url}/sites/MLB/search?q={product_name}&category=MLB1459"
            logger.info(f"Buscando '{product_name}' no Mercado Livre: {search_url}")

            response = self.make_request(search_url)
            data = response.json()

            products = []
            for item in data.get('results', [])[:10]: # Limitar aos 10 primeiros
                try:
                    price = item.get('price')
                    if not price:
                        continue

                    name = item.get('title', '')
                    url = item.get('permalink', '')
                    size_value, size_unit = self.extract_size(name)

                    products.append({
                        'name': name,
                        'price': float(price),
                        'url': url,
                        'store': self.name,
                        'size_value': size_value,
                        'size_unit': size_unit,
                        'mock': False
                    })
                except Exception as e:
                    logger.error(f"Erro processando item do Mercado Livre: {e}")
                    continue
            
            logger.info(f"Mercado Livre: {len(products)} produtos encontrados para '{product_name}'")
            return products

        except Exception as e:
            logger.error(f"Erro ao buscar no Mercado Livre: {e}", exc_info=True)
            return []

    def _search_mock(self, product_name: str) -> List[Dict]:
        """Mock para busca no Mercado Livre."""
        return [{
            'name': f"{product_name.title()} - Mercado Livre",
            'price': 10.99,
            'url': f"https://lista.mercadolivre.com.br/{product_name}",
            'store': self.name,
            'mock': True
        }]
