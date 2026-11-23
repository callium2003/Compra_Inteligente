import pytest

from src.main import app
from src.routes import quote as quote_module
from src.routes.quote import calculate_baskets
from src.utils.matching import get_best_match


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    return app.test_client()


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'


def test_normalize_list(client):
    response = client.post('/api/normalize', json={'raw_text': '2 leite integral 1l\narroz 5kg'})
    assert response.status_code == 200
    assert response.json['items'] == [
        {'brand': None, 'notes': None, 'preference': 'any', 'product_name': 'leite integral', 'qty': 2.0, 'size_unit': 'l', 'size_value': 1.0},
        {'brand': None, 'notes': None, 'preference': 'any', 'product_name': 'arroz', 'qty': 1.0, 'size_unit': 'kg', 'size_value': 5.0},
    ]


def test_explicit_matching_filter_does_not_fallback():
    products = [{'name': 'Leite comum', 'price': 4.0}]
    assert get_best_match('leite', products, filters={'organic': True}) is None


def test_calculate_baskets_includes_quantity_and_freight():
    priced = [
        {'product_name': 'leite', 'qty': 2, 'prices': {'A': {'name': 'Leite', 'price': 5}, 'B': {'name': 'Leite', 'price': 4}}},
        {'product_name': 'arroz', 'qty': 1, 'prices': {'A': {'name': 'Arroz', 'price': 20}, 'B': {'name': 'Arroz', 'price': 25}}},
    ]
    single, mixed, unavailable = calculate_baskets(priced, ['A', 'B'])
    assert single['store'] == 'A'
    assert single['subtotal'] == 30
    assert single['total'] == 39.9
    # Dois fretes deixariam a divisão mais cara; a otimização mantém a loja única.
    assert mixed['total'] == 39.9
    assert [store['store'] for store in mixed['stores']] == ['A']
    assert unavailable == []


def test_quote_uses_requested_stores_and_qty(client, monkeypatch):
    async def fake_fetch(items, cep, selected_connectors, filters=None):
        assert list(selected_connectors) == ['Extra']
        return [{'product_name': 'leite', 'qty': 2, 'size_value': 1, 'size_unit': 'l', 'prices': {'Extra': {'name': 'Leite', 'price': 5, 'mock': True}}}]

    monkeypatch.setattr(quote_module, 'fetch_all_prices', fake_fetch)
    response = client.post('/api/quote', json={'items': [{'product_name': 'leite', 'qty': 2}], 'stores': ['Extra']})
    assert response.status_code == 200
    assert response.json['single_store']['subtotal'] == 10
    assert response.json['single_store']['items'][0]['qty'] == 2
    assert response.json['savings'] == {'amount': 0.0, 'percentage': 0.0}


def test_quote_rejects_unknown_store(client):
    response = client.post('/api/quote', json={'items': [{'product_name': 'leite', 'qty': 1}], 'stores': ['Inexistente']})
    assert response.status_code == 400
    assert 'Lojas desconhecidas' in response.json['error']


def test_quote_rejects_invalid_quantity(client):
    response = client.post('/api/quote', json={'items': [{'product_name': 'leite', 'qty': 'muitos'}]})
    assert response.status_code == 400
    assert 'quantidade positiva' in response.json['error']
