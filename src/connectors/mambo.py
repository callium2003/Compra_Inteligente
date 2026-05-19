import logging
import json
import random
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from .base import SupermarketConnector

logger = logging.getLogger(__name__)

class MamboConnector(SupermarketConnector):
    def __init__(self):
        super().__init__(
            name="Mambo",
            base_url="https://www.mambo.com.br"
        )
        self.use_mock = False
        
    async def search(self, product_name: str, cep: Optional[str] = None) -> List[Dict]:
        if self.use_mock:
            return self._search_mock(product_name)
            
        try:
            search_url = f"{self.base_url}/{product_name.replace(' ', '%20')}?_q={product_name.replace(' ', '%20')}&map=ft"
            response = await self.make_request(search_url)
            if not response:
                return self._search_mock(product_name)
                
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script')
            results = []
            
            for script in scripts:
                if script.string and '__STATE__' in script.string:
                    try:
                        json_text = script.string.split('__STATE__ = ')[1].split(';')[0]
                        state = json.loads(json_text)
                        for key, value in state.items():
                            if value.get('__typename') == 'Product':
                                name = value.get('productName')
                                link = value.get('link')
                                price = 0
                                for k2, v2 in state.items():
                                    if k2.startswith(key) and v2.get('__typename') == 'Price':
                                        price = v2.get('sellingPrice') or v2.get('price')
                                        break
                                if name and price:
                                    results.append({
                                        "name": name,
                                        "price": float(price) / 100 if price > 100 else float(price),
                                        "url": self.base_url + link if link else "",
                                        "store": self.name,
                                        "mock": False
                                    })
                        if results: return results
                    except: continue
            return self._search_mock(product_name)
        except Exception as e:
            logger.error(f"Erro no Mambo assíncrono: {e}")
            return self._search_mock(product_name)

    async def get_product_details(self, product_url: str) -> Dict:
        return {"url": product_url, "store": self.name}

    def _search_mock(self, product_name: str) -> List[Dict]:
        seed = sum(ord(c) for c in product_name.lower())
        random.seed(seed + 2)
        base_price = random.uniform(4.0, 18.0)
        return [{
            "name": f"{product_name.capitalize()} - Mambo",
            "price": round(base_price, 2),
            "url": self.base_url,
            "store": self.name,
            "mock": True
        }]
