"""
Conector para Carrefour (API VTEX)
"""
import logging
from typing import List, Dict, Optional
from .base import SupermarketConnector

logger = logging.getLogger(__name__)


class CarrefourConnector(SupermarketConnector):
    """Conector para buscar produtos no Carrefour usando a API VTEX"""
    
    def __init__(self):
        super().__init__(
            name="Carrefour",
            base_url="https://mercado.carrefour.com.br"
        )
        self.api_url = "https://carrefourbrfood.vtexcommercestable.com.br/api/catalog_system/pub/products/search"

    def search(self, product_name: str, cep: Optional[str] = None) -> List[Dict]:
        """
        Busca produto no Carrefour usando a API VTEX

        Args:
            product_name: Nome do produto
            cep: CEP (não utilizado por enquanto)
        
        Returns:
            Lista de produtos encontrados
        """
        try:
            params = {
                'ft': product_name,
                '_from': 0,
                '_to': 9  # 10 primeiros resultados
            }
            
            response = self.make_request(self.api_url, params=params)
            products_data = response.json()
            
            results = []
            for product in products_data:
                item = product.get('items', [])[0]
                seller = item.get('sellers', [])[0]
                offer = seller.get('commertialOffer', {})
                
                price = offer.get('Price')
                if not price:
                    continue

                results.append({
                    'name': product.get('productName'),
                    'price': price,
                    'url': f"{self.base_url}{product.get('link')}",
                    'store': self.name,
                    'brand': product.get('brand'),
                    'available': offer.get('AvailableQuantity', 0) > 0,
                    'mock': False
                })
            
            logger.info(f"Carrefour API: {len(results)} produtos encontrados para '{product_name}'")
            return results

        except Exception as e:
            logger.error(f"Erro ao buscar na API do Carrefour: {e}", exc_info=True)
            return []

    def get_product_details(self, product_url: str) -> Dict:
        """
        Obtém detalhes de um produto específico (simplificado, pois a busca já traz tudo)
        """
        logger.warning("get_product_details não é necessário com a API do Carrefour, pois a busca já retorna todos os dados.")
        return {
            'url': product_url,
            'store': self.name,
            'error': "Use o método search para obter os detalhes do produto."
        }
