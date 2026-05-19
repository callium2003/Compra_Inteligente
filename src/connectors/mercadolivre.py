import logging
import random
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from .base import SupermarketConnector

logger = logging.getLogger(__name__)

class MercadoLivreConnector(SupermarketConnector):
    def __init__(self):
        super().__init__(
            name="Mercado Livre",
            base_url="https://api.mercadolibre.com"
        )
        self.use_mock = False
        
    async def search(self, product_name: str, cep: Optional[str] = None) -> List[Dict]:
        if self.use_mock:
            return self._search_mock(product_name)
            
        try:
            # Tentar busca HTML direta (mais estável para supermercado)
            search_url = f"https://lista.mercadolivre.com.br/supermercado/{product_name.replace(' ', '-')}"
            response = await self.make_request(search_url)
            if not response:
                return self._search_mock(product_name)
                
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            items = soup.select('.ui-search-result__wrapper')
            
            for item in items:
                name_tag = item.select_one('.ui-search-item__title')
                price_tag = item.select_one('.poly-price__current .andes-money-amount__fraction')
                link_tag = item.select_one('.ui-search-link')
                
                if name_tag and price_tag:
                    name = name_tag.get_text(strip=True)
                    price = float(price_tag.get_text(strip=True).replace('.', '').replace(',', '.'))
                    results.append({
                        "name": name,
                        "price": price,
                        "url": link_tag['href'] if link_tag else "",
                        "store": self.name,
                        "mock": False
                    })
                if len(results) >= 10: break
            
            return results if results else self._search_mock(product_name)
        except Exception as e:
            logger.error(f"Erro no ML assíncrono: {e}")
            return self._search_mock(product_name)

    async def get_product_details(self, product_url: str) -> Dict:
        return {"url": product_url, "store": self.name}

    def _search_mock(self, product_name: str) -> List[Dict]:
        seed = sum(ord(c) for c in product_name.lower())
        random.seed(seed + 3)
        base_price = random.uniform(3.5, 16.0)
        return [{
            "name": f"{product_name.capitalize()} - Mercado Livre",
            "price": round(base_price, 2),
            "url": "https://www.mercadolivre.com.br",
            "store": self.name,
            "mock": True
        }]
