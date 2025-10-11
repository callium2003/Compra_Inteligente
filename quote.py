"""
Rota de cotação com conectores reais
"""
import logging
from flask import Blueprint, request, jsonify
from ..connectors import (
    ExtraConnector,
    CarrefourConnector,
    MamboConnector,
    MercadoLivreConnector
)
from ..cache import PriceCache

logger = logging.getLogger(__name__)

quote_bp = Blueprint('quote', __name__)

# Inicializar conectores
connectors = {
    'Extra': ExtraConnector(),
    'Carrefour': CarrefourConnector(),
    'Mambo': MamboConnector(),
    'Mercado Livre': MercadoLivreConnector()
}

# Inicializar cache (1 hora de TTL)
cache = PriceCache(ttl=3600)


def search_product_in_stores(product_name: str, cep: str = None):
    """
    Busca produto em todas as lojas
    
    Args:
        product_name: Nome do produto
        cep: CEP para filtrar disponibilidade
    
    Returns:
        Dicionário com preços por loja
    """
    results = {}
    
    for store_name, connector in connectors.items():
        try:
            # Verificar cache primeiro
            cached = cache.get(store_name, product_name)
            if cached:
                results[store_name] = cached
                logger.info(f"Cache hit: {store_name} - {product_name}")
                continue
            
            # Buscar preço real
            logger.info(f"Buscando {product_name} em {store_name}...")
            search_results = connector.search(product_name, cep)
            
            if search_results and len(search_results) > 0:
                # Pegar o primeiro resultado (melhor match)
                best_match = search_results[0]
                
                result_data = {
                    'price': best_match['price'],
                    'name': best_match['name'],
                    'url': best_match.get('url', ''),
                    'size_value': best_match.get('size_value'),
                    'size_unit': best_match.get('size_unit'),
                    'mock': best_match.get('mock', False)
                }
                
                results[store_name] = result_data
                
                # Salvar no cache
                cache.set(store_name, product_name, result_data)
            else:
                # Nenhum resultado encontrado
                logger.warning(f"Nenhum resultado para {product_name} em {store_name}")
                results[store_name] = None
        
        except Exception as e:
            logger.error(f"Erro ao buscar {product_name} em {store_name}: {e}")
            results[store_name] = None
    
    return results


def calculate_single_basket(items_with_prices):
    """
    Calcula cesta única (tudo em uma loja)
    
    Args:
        items_with_prices: Lista de itens com preços por loja
    
    Returns:
        Dicionário com resultado da cesta única
    """
    stores = list(connectors.keys())
    best_store = None
    best_total = float('inf')
    best_items = []
    
    for store in stores:
        total = 0
        items = []
        all_available = True
        
        for item in items_with_prices:
            product_name = item['product_name']
            quantity = item.get('quantity', 1)
            prices = item['prices']
            
            if store not in prices or prices[store] is None:
                all_available = False
                break
            
            price = prices[store]['price']
            subtotal = price * quantity
            total += subtotal
            
            items.append({
                'product_name': product_name,
                'quantity': quantity,
                'unit_price': price,
                'subtotal': subtotal,
                'url': prices[store].get('url', '')
            })
        
        if all_available and total < best_total:
            best_total = total
            best_store = store
            best_items = items
    
    # Adicionar frete (simulado)
    freight = 0 if best_total >= 50 else 9.90
    
    return {
        'store': best_store,
        'items': best_items,
        'subtotal': round(best_total, 2),
        'freight': freight,
        'total': round(best_total + freight, 2)
    }


def calculate_mixed_basket(items_with_prices):
    """
    Calcula cesta mista (item mais barato de cada loja)
    
    Args:
        items_with_prices: Lista de itens com preços por loja
    
    Returns:
        Dicionário com resultado da cesta mista
    """
    items_by_store = {}
    total = 0
    
    for item in items_with_prices:
        product_name = item['product_name']
        quantity = item.get('quantity', 1)
        prices = item['prices']
        
        # Encontrar loja com menor preço
        best_store = None
        best_price = float('inf')
        best_url = ''
        
        for store, price_data in prices.items():
            if price_data and price_data['price'] < best_price:
                best_price = price_data['price']
                best_store = store
                best_url = price_data.get('url', '')
        
        if best_store:
            subtotal = best_price * quantity
            total += subtotal
            
            if best_store not in items_by_store:
                items_by_store[best_store] = []
            
            items_by_store[best_store].append({
                'product_name': product_name,
                'quantity': quantity,
                'unit_price': best_price,
                'subtotal': subtotal,
                'url': best_url
            })
    
    # Calcular frete por loja
    freight_by_store = {}
    total_freight = 0
    
    for store, items in items_by_store.items():
        store_subtotal = sum(item['subtotal'] for item in items)
        freight = 0 if store_subtotal >= 50 else 9.90
        freight_by_store[store] = freight
        total_freight += freight
    
    return {
        'items_by_store': items_by_store,
        'freight_by_store': freight_by_store,
        'subtotal': round(total, 2),
        'total_freight': round(total_freight, 2),
        'total': round(total + total_freight, 2)
    }


@quote_bp.route('/quote', methods=['POST'])
def quote():
    """
    Endpoint para gerar cotação com preços reais
    
    Body:
        {
            "items": [
                {"product_name": "leite", "quantity": 2},
                {"product_name": "arroz", "quantity": 1}
            ],
            "cep": "01310-100"  # opcional
        }
    
    Returns:
        {
            "success": true,
            "single_basket": {...},
            "mixed_basket": {...},
            "savings": {...}
        }
    """
    try:
        data = request.json
        items = data.get('items', [])
        cep = data.get('cep')
        
        if not items:
            return jsonify({
                'success': False,
                'error': 'Nenhum item fornecido'
            }), 400
        
        logger.info(f"Cotação solicitada: {len(items)} itens")
        
        # Buscar preços para cada item
        items_with_prices = []
        
        for item in items:
            product_name = item.get('product_name', '')
            quantity = item.get('quantity', 1)
            
            if not product_name:
                continue
            
            # Buscar em todas as lojas
            prices = search_product_in_stores(product_name, cep)
            
            items_with_prices.append({
                'product_name': product_name,
                'quantity': quantity,
                'prices': prices
            })
        
        # Calcular cestas
        single_basket = calculate_single_basket(items_with_prices)
        mixed_basket = calculate_mixed_basket(items_with_prices)
        
        # Calcular economia
        savings_value = single_basket['total'] - mixed_basket['total']
        savings_percent = (savings_value / single_basket['total'] * 100) if single_basket['total'] > 0 else 0
        
        return jsonify({
            'success': True,
            'single_basket': single_basket,
            'mixed_basket': mixed_basket,
            'savings': {
                'value': round(savings_value, 2),
                'percent': round(savings_percent, 1)
            },
            'items_searched': len(items_with_prices)
        })
    
    except Exception as e:
        logger.error(f"Erro ao gerar cotação: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@quote_bp.route('/cache/stats', methods=['GET'])
def cache_stats():
    """Retorna estatísticas do cache"""
    try:
        stats = cache.get_stats()
        return jsonify({
            'success': True,
            'cache': stats
        })
    except Exception as e:
        logger.error(f"Erro ao obter stats do cache: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@quote_bp.route('/cache/clear', methods=['POST'])
def clear_cache():
    """Limpa o cache"""
    try:
        data = request.json or {}
        store = data.get('store')
        
        cache.clear(store)
        
        return jsonify({
            'success': True,
            'message': f"Cache limpo{' para ' + store if store else ''}"
        })
    except Exception as e:
        logger.error(f"Erro ao limpar cache: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
