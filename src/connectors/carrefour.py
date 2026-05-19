import logging
import random
import re
from typing import List, Dict, Optional
from urllib.parse import quote
from bs4 import BeautifulSoup
from .base import SupermarketConnector

logger = logging.getLogger(__name__)

class CarrefourConnector(SupermarketConnector):
    def __init__(self):
        super().__init__(
            name="Carrefour",
            base_url="https://mercado.carrefour.com.br"
        )
        self.use_mock = False
    
    async def search(self, product_name: str, cep: Optional[str] = None) -> List[Dict]:
        if self.use_mock:
            return self._search_mock(product_name)
        
        try:
            search_url = f"{self.base_url}/busca/{quote(product_name)}"
            response = await self.make_request(search_url)
            if not response:
                return self._search_mock(product_name)
                
            soup = BeautifulSoup(response.text, 'html.parser')
            products = []
            product_links = soup.select('a[href*="/p"]')
            
            seen_urls = set()
            for link in product_links:
                url = link.get('href', '')
                if not url or '/p' not in url or url in seen_urls: continue
                seen_urls.add(url)
                
                if not url.startswith('http'): url = self.base_url + url
                
                img = link.select_one('img[alt]')
                name = img.get('alt', '') if img else link.get_text(strip=True)
                
                if not name or len(name) < 5: continue
                
                # Tentar encontrar preço no texto ao redor
                price_text = link.parent.get_text() if link.parent else ""
                price_match = re.search(r'R\$\s*([\d,]+)', price_text)
                
                if price_match:
                    price = self.normalize_price(price_match.group(0))
                    if price > 0:
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
                
                if len(products) >= 10: break
                
            return products if products else self._search_mock(product_name)
        except Exception as e:
            logger.error(f"Erro no Carrefour assíncrono: {e}")
            return self._search_mock(product_name)

    async def get_product_details(self, product_url: str) -> Dict:
        return {"url": product_url, "store": self.name}

    def _search_mock(self, product_name: str) -> List[Dict]:
        seed = sum(ord(c) for c in product_name.lower())
        random.seed(seed + 1)
        base_price = random.uniform(3.0, 15.0)
        size_value, size_unit = self.extract_size(product_name)
        return [{
            'name': f"{product_name.title()} - Carrefour",
            'price': round(base_price, 2),
            'url': self.base_url,
            'store': self.name,
            'size_value': size_value,
            'size_unit': size_unit,
            'mock': True
        }]
