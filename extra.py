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
        self.use_mock = True  # Usar mock (site com proteção anti-bot)
    
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
            # URL de busca
            search_url = f"{self.base_url}/busca?terms={quote(product_name)}"
            logger.info(f"Buscando '{product_name}' no Extra: {search_url}")
            
            # Fazer requisição
            response = self.make_request(search_url)
            soup = self.parse_html(response.text)
            
            products = []
            
            # Buscar produtos usando seletores identificados
            # Seletor: div com classe CardStyled
            product_cards = soup.select('div[class*="CardStyled"]')
            
            if not product_cards:
                logger.warning(f"Nenhum card encontrado para '{product_name}' no Extra")
                # Tentar seletor alternativo
                product_cards = soup.select('div[class*="Card-sc"]')
            
            if not product_cards:
                logger.warning(f"Nenhum produto encontrado para '{product_name}' no Extra, usando mock")
                return self._search_mock(product_name)
            
            logger.info(f"Extra: {len(product_cards)} cards encontrados")
            
            for card in product_cards[:10]:  # Limitar a 10 resultados
                try:
                    # Extrair nome usando seletor identificado
                    # Nome está em: a[class*="Title"]
                    name_elem = card.select_one('a[class*="Title"]')
                    if not name_elem:
                        # Fallback: buscar qualquer link com texto
                        name_elem = card.select_one('a[href*="/produto/"]')
                    
                    if not name_elem:
                        continue
                    
                    name = name_elem.get_text(strip=True)
                    if not name:
                        # Tentar pegar do alt da imagem
                        img = card.select_one('img[alt]')
                        name = img.get('alt', '') if img else ''
                    
                    if not name:
                        continue
                    
                    # Extrair preço usando seletor identificado
                    # Preço está em: p[class*="PriceValue"]
                    price_elem = card.select_one('p[class*="PriceValue"]')
                    if not price_elem:
                        # Fallback: buscar qualquer elemento com "R$"
                        price_elem = card.find(string=re.compile(r'R\$\s*[\d,]+'))
                        if price_elem:
                            price_text = price_elem
                        else:
                            continue
                    else:
                        price_text = price_elem.get_text(strip=True)
                    
                    price = self.normalize_price(price_text)
                    
                    if price == 0:
                        logger.debug(f"Preço zero para '{name}', ignorando")
                        continue
                    
                    # Extrair URL
                    link_elem = card.select_one('a[href*="/produto/"]')
                    url = link_elem.get('href', '') if link_elem else ''
                    
                    if url and not url.startswith('http'):
                        url = self.base_url + url
                    
                    # Extrair tamanho do nome
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
        
        # Gerar preço mock baseado em hash do nome
        seed = sum(ord(c) for c in product_name.lower())
        random.seed(seed)
        
        # Preço base entre 3 e 15 reais
        base_price = random.uniform(3.0, 15.0)
        
        # Extrair tamanho
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
            
            # Nome
            name_elem = soup.select_one('h1, [class*="ProductName"]')
            if name_elem:
                details['name'] = name_elem.get_text(strip=True)
            
            # Preço
            price_elem = soup.select_one('p[class*="PriceValue"]')
            if price_elem:
                details['price'] = self.normalize_price(price_elem.get_text(strip=True))
            
            # Marca
            brand_elem = soup.select_one('[class*="brand"], [class*="Brand"]')
            if brand_elem:
                details['brand'] = brand_elem.get_text(strip=True)
            
            return details
        
        except Exception as e:
            logger.error(f"Erro ao obter detalhes do produto no Extra: {e}")
            return {'url': product_url, 'store': self.name, 'error': str(e)}
