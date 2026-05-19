import asyncio
import logging
from flask import Blueprint, request, jsonify
from ..connectors import (
    ExtraConnector,
    CarrefourConnector,
    MamboConnector,
    MercadoLivreConnector
)
from ..cache import PriceCache
from ..utils.matching import get_best_match

logger = logging.getLogger(__name__)
quote_bp = Blueprint('quote', __name__)

# Inicializar conectores
connectors = {
    'Extra': ExtraConnector(),
    'Carrefour': CarrefourConnector(),
    'Mambo': MamboConnector(),
    'Mercado Livre': MercadoLivreConnector()
}

# Inicializar cache
cache = PriceCache(ttl=3600)

async def search_in_store_async(store_name, connector, product_name, cep, filters=None):
    """Busca assíncrona em uma única loja com cache e filtros"""
    try:
        # Cache é por nome do produto, mas filtros mudam o resultado. 
        # Para simplificar, não usaremos cache se houver filtros específicos.
        if not filters:
            cached = cache.get(store_name, product_name)
            if cached:
                return store_name, cached

        # Buscar real
        results = await connector.search(product_name, cep)
        if results:
            # Usar Matching Inteligente com filtros
            best_match = get_best_match(product_name, results, filters=filters)
            result_data = {
                'price': best_match['price'],
                'name': best_match['name'],
                'url': best_match.get('url', ''),
                'mock': best_match.get('mock', False)
            }
            if not filters:
                cache.set(store_name, product_name, result_data)
            return store_name, result_data
        return store_name, None
    except Exception as e:
        logger.error(f"Erro ao buscar {product_name} em {store_name}: {e}")
        return store_name, None

async def fetch_all_prices(items, cep, filters=None):
    """Busca todos os itens em todas as lojas em paralelo com filtros"""
    all_tasks = []
    for item in items:
        product_name = item.get('product_name')
        for store_name, connector in connectors.items():
            all_tasks.append(search_in_store_async(store_name, connector, product_name, cep, filters))
    
    # Executar tudo em paralelo
    results = await asyncio.gather(*all_tasks)
    
    # Organizar resultados por item
    organized = []
    idx = 0
    for item in items:
        item_prices = {}
        for _ in range(len(connectors)):
            store_name, data = results[idx]
            item_prices[store_name] = data
            idx += 1
        organized.append({
            'product_name': item.get('product_name'),
            'quantity': item.get('quantity', 1),
            'prices': item_prices
        })
    return organized

@quote_bp.route('/quote', methods=['POST'])
def quote():
    data = request.json
    items = data.get('items', [])
    cep = data.get('cep')
    filters = data.get('filters', {}) # { brand: "Nestlé", organic: true }
    
    if not items:
        return jsonify({'success': False, 'error': 'Nenhum item'}), 400

    # Executar loop assíncrono
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        items_with_prices = loop.run_until_complete(fetch_all_prices(items, cep, filters))
    finally:
        loop.close()

    # Cálculo de Cestas (Lógica simplificada para MVP)
    # 1. Cesta Única
    best_single_store = None
    min_total = float('inf')
    
    for store in connectors.keys():
        total = 0
        store_items = []
        possible = True
        for item in items_with_prices:
            p_data = item['prices'].get(store)
            if not p_data:
                possible = False
                break
            subtotal = p_data['price'] * item['quantity']
            total += subtotal
            store_items.append({
                'product_name': item['product_name'],
                'unit_price': p_data['price'],
                'subtotal': subtotal,
                'store': store
            })
        
        if possible and total < min_total:
            min_total = total
            best_single_store = {'store': store, 'total': round(total, 2), 'items': store_items}

    # 2. Cesta Mista
    mixed_total = 0
    mixed_items = []
    for item in items_with_prices:
        valid_prices = {s: p for s, p in item['prices'].items() if p}
        if valid_prices:
            best_store = min(valid_prices, key=lambda s: valid_prices[s]['price'])
            p_data = valid_prices[best_store]
            subtotal = p_data['price'] * item['quantity']
            mixed_total += subtotal
            mixed_items.append({
                'product_name': item['product_name'],
                'unit_price': p_data['price'],
                'subtotal': subtotal,
                'store': best_store
            })

    return jsonify({
        'success': True,
        'single_basket': best_single_store,
        'mixed_basket': {'total': round(mixed_total, 2), 'items': mixed_items},
        'savings': {
            'value': round((best_single_store['total'] - mixed_total) if best_single_store else 0, 2),
            'percent': round(((best_single_store['total'] - mixed_total) / best_single_store['total'] * 100) if best_single_store and best_single_store['total'] > 0 else 0, 1)
        }
    })
