"""Rotas e regras de cálculo da cotação de compras."""
import asyncio
import logging

from flask import Blueprint, jsonify, request

from ..cache import PriceCache
from ..connectors import CarrefourConnector, ExtraConnector, MamboConnector, MercadoLivreConnector
from ..utils.matching import get_best_match

logger = logging.getLogger(__name__)
quote_bp = Blueprint("quote", __name__)

connectors = {
    "Extra": ExtraConnector(),
    "Carrefour": CarrefourConnector(),
    "Mambo": MamboConnector(),
    "Mercado Livre": MercadoLivreConnector(),
}
cache = PriceCache(ttl=3600)


def _quantity(item):
    """Aceita tanto o contrato do normalizador (qty) quanto o legado (quantity)."""
    return float(item.get("qty", item.get("quantity", 1)))


async def search_in_store_async(store_name, connector, product_name, cep, filters=None):
    """Busca um item em uma loja, aplicando cache e restrições de produto."""
    try:
        if not filters:
            cached = cache.get(store_name, product_name)
            if cached:
                return store_name, cached

        results = await connector.search(product_name, cep)
        best_match = get_best_match(product_name, results, filters=filters) if results else None
        if not best_match:
            return store_name, None

        result_data = {
            "price": float(best_match["price"]),
            "name": best_match["name"],
            "url": best_match.get("url", ""),
            "mock": best_match.get("mock", False),
        }
        if not filters:
            cache.set(store_name, product_name, result_data)
        return store_name, result_data
    except Exception:
        logger.exception("Erro ao buscar %s em %s", product_name, store_name)
        return store_name, None


async def fetch_all_prices(items, cep, selected_connectors, filters=None):
    """Busca todos os itens nas lojas selecionadas em paralelo."""
    tasks = [
        search_in_store_async(store_name, connector, item["product_name"], cep, filters)
        for item in items
        for store_name, connector in selected_connectors.items()
    ]
    results = await asyncio.gather(*tasks)

    organized = []
    result_index = 0
    for item in items:
        prices = {}
        for _ in selected_connectors:
            store_name, price = results[result_index]
            prices[store_name] = price
            result_index += 1
        organized.append({
            "product_name": item["product_name"],
            "qty": _quantity(item),
            "size_value": item.get("size_value"),
            "size_unit": item.get("size_unit"),
            "prices": prices,
        })
    return organized


def _basket_item(item, price_data):
    subtotal = round(price_data["price"] * item["qty"], 2)
    return {
        "product_name": item["product_name"],
        "qty": item["qty"],
        "size_value": item.get("size_value"),
        "size_unit": item.get("size_unit"),
        "unit_price": price_data["price"],
        "total": subtotal,
        "url": price_data.get("url", ""),
        "mock": price_data.get("mock", False),
    }


def calculate_baskets(items_with_prices, store_names):
    """Calcula cestas única e mista usando o mesmo formato consumido pelo frontend."""
    single_candidates = []
    for store_name in store_names:
        if all(item["prices"].get(store_name) for item in items_with_prices):
            basket_items = [_basket_item(item, item["prices"][store_name]) for item in items_with_prices]
            subtotal = round(sum(item["total"] for item in basket_items), 2)
            frete = 0.0 if subtotal >= 50 else 9.9
            single_candidates.append({
                "store": store_name,
                "items": basket_items,
                "subtotal": subtotal,
                "frete": frete,
                "minimo": 50.0,
                "meets_minimum": subtotal >= 50,
                "total": round(subtotal + frete, 2),
            })

    single_store = min(single_candidates, key=lambda basket: basket["total"]) if single_candidates else None

    grouped = {}
    unavailable_items = []
    for item in items_with_prices:
        available = {name: value for name, value in item["prices"].items() if value}
        if not available:
            unavailable_items.append(item["product_name"])
            continue
        store_name, price_data = min(available.items(), key=lambda pair: pair[1]["price"])
        grouped.setdefault(store_name, []).append(_basket_item(item, price_data))

    mixed_stores = []
    for store_name, basket_items in grouped.items():
        subtotal = round(sum(item["total"] for item in basket_items), 2)
        frete = 0.0 if subtotal >= 50 else 9.9
        mixed_stores.append({
            "store": store_name,
            "items": basket_items,
            "subtotal": subtotal,
            "frete": frete,
            "minimo": 50.0,
            "meets_minimum": subtotal >= 50,
            "total": round(subtotal + frete, 2),
        })

    total_frete = round(sum(store["frete"] for store in mixed_stores), 2)
    mixed_total = round(sum(store["total"] for store in mixed_stores), 2)

    # Comprar cada item pelo menor preço pode gerar vários fretes. A cesta
    # apresentada como "otimizada" nunca deve ser mais cara que a melhor loja única.
    if single_store and single_store["total"] < mixed_total:
        mixed_stores = [{**single_store}]
        total_frete = single_store["frete"]
        mixed_total = single_store["total"]
    mixed_basket = {"stores": mixed_stores, "total_frete": total_frete, "total": mixed_total}
    return single_store, mixed_basket, unavailable_items


@quote_bp.route("/quote", methods=["POST"])
def quote():
    data = request.get_json(silent=True) or {}
    items = data.get("items") or []
    if not items:
        return jsonify({"success": False, "error": "Nenhum item fornecido"}), 400
    try:
        invalid_items = [item for item in items if not item.get("product_name") or _quantity(item) <= 0]
    except (TypeError, ValueError):
        invalid_items = items
    if invalid_items:
        return jsonify({"success": False, "error": "Todos os itens precisam de nome e quantidade positiva"}), 400

    requested_stores = data.get("stores") or list(connectors)
    unknown_stores = sorted(set(requested_stores) - set(connectors))
    if unknown_stores:
        return jsonify({"success": False, "error": f"Lojas desconhecidas: {', '.join(unknown_stores)}"}), 400
    selected_connectors = {name: connectors[name] for name in requested_stores}

    items_with_prices = asyncio.run(
        fetch_all_prices(items, data.get("cep"), selected_connectors, data.get("filters") or None)
    )
    single_store, mixed_basket, unavailable_items = calculate_baskets(items_with_prices, requested_stores)

    if single_store:
        amount = max(round(single_store["total"] - mixed_basket["total"], 2), 0)
        percentage = round(amount / single_store["total"] * 100, 1) if single_store["total"] else 0
    else:
        amount = percentage = 0

    return jsonify({
        "success": True,
        "single_store": single_store,
        "mixed_basket": mixed_basket,
        "savings": {"amount": amount, "percentage": percentage},
        "unavailable_items": unavailable_items,
    })
