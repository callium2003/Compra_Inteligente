"""
Classe base para conectores de supermercados (Versão Assíncrona)
"""
import re
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class SupermarketConnector(ABC):
    """Classe base abstrata para conectores de supermercados"""
    
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.min_interval = 0.5  # Reduzido para 0.5s em modo assíncrono
    
    @abstractmethod
    async def search(self, product_name: str, cep: Optional[str] = None) -> List[Dict]:
        """Busca produto no supermercado (Assíncrono)"""
        pass
    
    @abstractmethod
    async def get_product_details(self, product_url: str) -> Dict:
        """Obtém detalhes completos de um produto (Assíncrono)"""
        pass
    
    async def make_request(self, url: str, method: str = 'GET', **kwargs) -> requests.Response:
        """Faz a requisição sem bloquear as demais buscas do loop assíncrono."""
        try:
            response = await asyncio.to_thread(
                requests.request,
                method.upper(),
                url,
                headers=self.headers,
                timeout=15,
                allow_redirects=True,
                **kwargs,
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Erro na requisição assíncrona para {url}: {e}")
            return None

    def normalize_price(self, price_string: str) -> float:
        try:
            price_clean = re.sub(r'[^\d,.]', '', price_string)
            price_clean = price_clean.replace(',', '.')
            parts = price_clean.split('.')
            if len(parts) > 2:
                price_clean = ''.join(parts[:-1]) + '.' + parts[-1]
            return float(price_clean)
        except (ValueError, AttributeError):
            return 0.0
    
    def extract_size(self, product_name: str) -> tuple:
        patterns = [
            r'(\d+(?:[.,]\d+)?)\s*(l|litro|litros)',
            r'(\d+(?:[.,]\d+)?)\s*(ml|mililitro|mililitros)',
            r'(\d+(?:[.,]\d+)?)\s*(kg|kilo|kilos|quilograma|quilogramas)',
            r'(\d+(?:[.,]\d+)?)\s*(g|grama|gramas)',
            r'(\d+(?:[.,]\d+)?)\s*(un|unidade|unidades)',
        ]
        product_lower = product_name.lower()
        for pattern in patterns:
            match = re.search(pattern, product_lower)
            if match:
                value = float(match.group(1).replace(',', '.'))
                unit = match.group(2)
                unit_map = {
                    'litro': 'l', 'litros': 'l', 'mililitro': 'ml', 'mililitros': 'ml',
                    'kilo': 'kg', 'kilos': 'kg', 'quilograma': 'kg', 'quilogramas': 'kg',
                    'grama': 'g', 'gramas': 'g', 'unidade': 'un', 'unidades': 'un'
                }
                unit = unit_map.get(unit, unit)
                return (value, unit)
        return (None, None)
