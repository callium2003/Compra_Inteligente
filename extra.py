"""
Conector para Extra Mercado (scraping real)
"""
import logging
import random
import re
from typing import List, Dict, Optional
from urllib.parse import quote
from .base import SupermarketConnector

logger = logging.getLogger(__name__)


class ExtraConnector(SupermarketConnector):
    """Conector para buscar produtos no Extra Mercado"""
    
    def __init__(self):
        super().__init__(
            name="Extra",
            base_url="https://www.extramercado.com.br"
        )
        self.use_mock = False  # Usar scraping real
    
    def search(self, product_name: str, cep: Optional[str] = None) -> List[Dict]:
        """
        Busca produto no Extra Mercado
        
        Args:
            product_name: Nome do produto
            cep: CEP (não utilizado por enquanto)
        
        Returns:
            Lista de produtos encontrados
        """
        if self.use_mock:
            return self._search_mock(product_name)
        
        try:
            search_url = f"{self.base_url}/busca?terms={quote(product_name)}"
            logger.info(f"Buscando '{product_name}' no Extra: {search_url}")
            
            response = self.make_request(search_url)
            soup = self.parse_html(response.text)
            
            products = []
            
            product_cards = soup.select('div[class*="CardStyled__Card-"]')
            
            if not product_cards:
                logger.warning(f"Nenhum produto encontrado para '{product_name}' no Extra, usando mock")
                return self._search_mock(product_name)
            
            logger.info(f"Extra: {len(product_cards)} cards encontrados")
            
            for card in product_cards[:10]:
                try:
                    name_elem = card.select_one('a[class*="ProductTitle__Name-"]')
                    name = name_elem.get_text(strip=True) if name_elem else ''

                    if not name:
                        continue

                    price_elem = card.select_one('p[class*="PriceUI__Price-sc"]')
                    price_text = price_elem.get_text(strip=True) if price_elem else ''
                    
                    price = self.normalize_price(price_text)
                    
                    if price == 0:
                        continue

                    link_elem = card.select_one('a[href*="/produto/"]')
                    url = self.base_url + link_elem['href'] if link_elem else ''

                    size_value, size_unit = self.extract_size(name)

                    products.append({
                        'name': name,
                        'price': price,
                        'url': url,
                        'store': self.name,
                        'size_value': size_value,
                        'size_unit': size_unit,
                        'mock': False
                    })

                    logger.debug(f"Extra: {name} - R$ {price:.2f}")
                
                except Exception as e:
                    logger.error(f"Erro ao processar card no Extra: {e}")
                    continue
            
            if not products:
                logger.warning(f"Nenhum produto válido encontrado para '{product_name}' no Extra, usando mock")
                return self._search_mock(product_name)
            
            logger.info(f"Extra: {len(products)} produtos válidos encontrados para '{product_name}'")
            return products
        
        except Exception as e:
            logger.error(f"Erro ao buscar no Extra: {e}", exc_info=True)
            return self._search_mock(product_name)
    
    def _search_mock(self, product_name: str) -> List[Dict]:
        """Busca mock com preços realistas"""
        logger.info(f"Extra (mock): Buscando '{product_name}'")
        
        seed = sum(ord(c) for c in product_name.lower())
        random.seed(seed)
        
        base_price = random.uniform(3.0, 15.0)
        size_value, size_unit = self.extract_size(product_name)
        
        return [{
            'name': f"{product_name.title()} - Extra",
            'price': round(base_price, 2),
            'url': f"{self.base_url}/produto/{product_name.lower().replace(' ', '-')}",
            'store': self.name,
            'size_value': size_value,
            'size_unit': size_unit,
            'mock': True
        }]
    
    def get_product_details(self, product_url: str) -> Dict:
        """Obtém detalhes de um produto específico"""
        try:
            response = self.make_request(product_url)
            soup = self.parse_html(response.text)
            
            details = {'url': product_url, 'store': self.name}
            
            name_elem = soup.select_one('h1[class*="ProductName"]')
            if name_elem:
                details['name'] = name_elem.get_text(strip=True)
            
            price_elem = soup.select_one('p[class*="PriceValue"]')
            if price_elem:
                details['price'] = self.normalize_price(price_elem.get_text(strip=True))
            
            return details
        
        except Exception as e:
            logger.error(f"Erro ao obter detalhes do produto no Extra: {e}")
            return {'url': product_url, 'store': self.name, 'error': str(e)}
