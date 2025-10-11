"""
Conector para Carrefour (scraping HTML)
"""
import logging
import random
import re
from typing import List, Dict, Optional
from urllib.parse import quote
from .base import SupermarketConnector

logger = logging.getLogger(__name__)


class CarrefourConnector(SupermarketConnector):
    """Conector para buscar produtos no Carrefour"""
    
    def __init__(self):
        super().__init__(
            name="Carrefour",
            base_url="https://mercado.carrefour.com.br"
        )
        self.use_mock = False  # Ativar scraping real
    
    def search(self, product_name: str, cep: Optional[str] = None) -> List[Dict]:
        """
        Busca produto no Carrefour
        
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
            search_url = f"{self.base_url}/busca/{quote(product_name)}"
            logger.info(f"Buscando '{product_name}' no Carrefour: {search_url}")
            
            # Fazer requisição
            response = self.make_request(search_url)
            soup = self.parse_html(response.text)
            
            products = []
            
            # Buscar produtos - links terminam com /p
            product_links = soup.select('a[href*="/p"]')
            
            if not product_links:
                logger.warning(f"Nenhum produto encontrado para '{product_name}' no Carrefour, usando mock")
                return self._search_mock(product_name)
            
            logger.info(f"Carrefour: {len(product_links)} links encontrados")
            
            # Processar produtos únicos (evitar duplicatas)
            seen_urls = set()
            
            for link in product_links:
                try:
                    url = link.get('href', '')
                    
                    # Filtrar apenas URLs de produtos
                    if not url or '/p' not in url or url in seen_urls:
                        continue
                    
                    seen_urls.add(url)
                    
                    # Montar URL completa
                    if not url.startswith('http'):
                        url = self.base_url + url
                    
                    # Extrair nome da imagem (alt)
                    img = link.select_one('img[alt]')
                    name = img.get('alt', '') if img else ''
                    
                    if not name:
                        # Tentar pegar do texto do link
                        name = link.get_text(strip=True)
                    
                    if not name or len(name) < 5:
                        continue
                    
                    # Buscar preço no contexto do link (parent)
                    parent = link.parent
                    for _ in range(3):  # Subir até 3 níveis
                        if parent is None:
                            break
                        
                        # Procurar preço
                        price_text = parent.get_text()
                        price_match = re.search(r'R\$\s*([\d,]+)', price_text)
                        
                        if price_match:
                            price = self.normalize_price(price_match.group(0))
                            
                            if price > 0:
                                # Extrair tamanho
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
                                
                                logger.debug(f"Carrefour: {name} - R$ {price:.2f}")
                                break
                        
                        parent = parent.parent
                    
                    # Limitar a 10 produtos
                    if len(products) >= 10:
                        break
                
                except Exception as e:
                    logger.error(f"Erro ao processar link no Carrefour: {e}")
                    continue
            
            if not products:
                logger.warning(f"Nenhum produto válido encontrado para '{product_name}' no Carrefour, usando mock")
                return self._search_mock(product_name)
            
            logger.info(f"Carrefour: {len(products)} produtos válidos encontrados para '{product_name}'")
            return products
        
        except Exception as e:
            logger.error(f"Erro ao buscar no Carrefour: {e}", exc_info=True)
            return self._search_mock(product_name)
    
    def _search_mock(self, product_name: str) -> List[Dict]:
        """Busca mock com preços realistas"""
        logger.info(f"Carrefour (mock): Buscando '{product_name}'")
        
        # Gerar preço mock baseado em hash do nome
        seed = sum(ord(c) for c in product_name.lower())
        random.seed(seed + 1)  # +1 para diferenciar do Extra
        
        # Preço base entre 3 e 15 reais
        base_price = random.uniform(3.0, 15.0)
        
        # Extrair tamanho
        size_value, size_unit = self.extract_size(product_name)
        
        return [{
            'name': f"{product_name.title()} - Carrefour",
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
            name_elem = soup.select_one('h1, [class*="productName"]')
            if name_elem:
                details['name'] = name_elem.get_text(strip=True)
            
            # Preço
            price_text = soup.get_text()
            price_match = re.search(r'R\$\s*([\d,]+)', price_text)
            if price_match:
                details['price'] = self.normalize_price(price_match.group(0))
            
            # Marca
            brand_elem = soup.select_one('[class*="brand"]')
            if brand_elem:
                details['brand'] = brand_elem.get_text(strip=True)
            
            return details
        
        except Exception as e:
            logger.error(f"Erro ao obter detalhes do produto no Carrefour: {e}")
            return {'url': product_url, 'store': self.name, 'error': str(e)}
