import logging
import json
import random
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from .base import SupermarketConnector

logger = logging.getLogger(__name__)

class ExtraConnector(SupermarketConnector):
    def __init__(self):
        super().__init__(
            name="Extra",
            base_url="https://www.extramercado.com.br"
        )
        self.use_mock = True # Extra ainda requer mock devido a proteções
        
    async def search(self, product_name: str, cep: Optional[str] = None) -> List[Dict]:
        if self.use_mock:
            return self._search_mock(product_name)
            
        try:
            search_url = f"{self.base_url}/busca?terms={product_name.replace(' ', '%20')}"
            response = await self.make_request(search_url)
            if not response: return self._search_mock(product_name)
                
            soup = BeautifulSoup(response.text, 'html.parser')
            next_data = soup.find('script', id='__NEXT_DATA__')
            if next_data:
                data = json.loads(next_data.string)
                products_data = data.get('props', {}).get('pageProps', {}).get('initialData', {}).get('products', [])
                results = []
                for p in products_data:
                    results.append({
                        "name": p.get('name', ''),
                        "price": float(p.get('price', 0)),
                        "url": f"{self.base_url}/produto/{p.get('id')}",
                        "store": self.name,
                        "mock": False
                    })
                if results: return results
            return self._search_mock(product_name)
        except Exception as e:
            logger.error(f"Erro no Extra assíncrono: {e}")
            return self._search_mock(product_name)

    async def get_product_details(self, product_url: str) -> Dict:
        return {"url": product_url, "store": self.name}

    def _search_mock(self, product_name: str) -> List[Dict]:
        seed = sum(ord(c) for c in product_name.lower())
        random.seed(seed + 4)
        base_price = random.uniform(4.5, 20.0)
        return [{
            "name": f"{product_name.capitalize()} - Extra",
            "price": round(base_price, 2),
            "url": self.base_url,
            "store": self.name,
            "mock": True
        }]
