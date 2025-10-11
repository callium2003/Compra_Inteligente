"""
Classe base para conectores de supermercados
"""
import re
import time
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
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.last_request_time = 0
        self.min_interval = 1.0  # 1 segundo entre requisições
    
    @abstractmethod
    def search(self, product_name: str, cep: Optional[str] = None) -> List[Dict]:
        """
        Busca produto no supermercado
        
        Args:
            product_name: Nome do produto a buscar
            cep: CEP para filtrar disponibilidade (opcional)
        
        Returns:
            Lista de dicionários com informações dos produtos encontrados
        """
        pass
    
    @abstractmethod
    def get_product_details(self, product_url: str) -> Dict:
        """
        Obtém detalhes completos de um produto
        
        Args:
            product_url: URL do produto
        
        Returns:
            Dicionário com detalhes do produto
        """
        pass
    
    def normalize_price(self, price_string: str) -> float:
        """
        Normaliza string de preço para float
        
        Args:
            price_string: String com preço (ex: "R$ 4,69")
        
        Returns:
            Preço como float (ex: 4.69)
        """
        try:
            # Remove tudo exceto números, vírgula e ponto
            price_clean = re.sub(r'[^\d,.]', '', price_string)
            # Substitui vírgula por ponto
            price_clean = price_clean.replace(',', '.')
            # Remove pontos extras (separadores de milhar)
            parts = price_clean.split('.')
            if len(parts) > 2:
                price_clean = ''.join(parts[:-1]) + '.' + parts[-1]
            return float(price_clean)
        except (ValueError, AttributeError) as e:
            logger.error(f"Erro ao normalizar preço '{price_string}': {e}")
            return 0.0
    
    def extract_size(self, product_name: str) -> tuple:
        """
        Extrai tamanho do nome do produto
        
        Args:
            product_name: Nome do produto
        
        Returns:
            Tupla (valor, unidade) ou (None, None) se não encontrar
        """
        # Padrões comuns: "1L", "1 L", "500ml", "500 ml", "1kg", "1 kg"
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
                # Normalizar unidades
                unit_map = {
                    'litro': 'l', 'litros': 'l',
                    'mililitro': 'ml', 'mililitros': 'ml',
                    'kilo': 'kg', 'kilos': 'kg', 'quilograma': 'kg', 'quilogramas': 'kg',
                    'grama': 'g', 'gramas': 'g',
                    'unidade': 'un', 'unidades': 'un'
                }
                unit = unit_map.get(unit, unit)
                return (value, unit)
        
        return (None, None)
    
    def rate_limit(self):
        """Implementa rate limiting para evitar sobrecarga"""
        now = time.time()
        elapsed = now - self.last_request_time
        
        if elapsed < self.min_interval:
            sleep_time = self.min_interval - elapsed
            logger.debug(f"Rate limiting: aguardando {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def make_request(self, url: str, method: str = 'GET', **kwargs) -> requests.Response:
        """
        Faz requisição HTTP com rate limiting
        
        Args:
            url: URL para requisição
            method: Método HTTP (GET, POST, etc)
            **kwargs: Argumentos adicionais para requests
        
        Returns:
            Response object
        """
        self.rate_limit()
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=10, **kwargs)
            elif method.upper() == 'POST':
                response = self.session.post(url, timeout=10, **kwargs)
            else:
                raise ValueError(f"Método HTTP não suportado: {method}")
            
            response.raise_for_status()
            return response
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao fazer requisição para {url}: {e}")
            raise
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML usando BeautifulSoup
        
        Args:
            html: String HTML
        
        Returns:
            Objeto BeautifulSoup
        """
        return BeautifulSoup(html, 'lxml')
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}', base_url='{self.base_url}')>"
