# Seletores CSS - Carrefour

## Análise do HTML

### Produtos Encontrados

A busca por "leite" retornou **62 produtos** no Carrefour.

Exemplos de produtos visíveis:
- Fórmula Infantil Ninho: R$ 39,99 (-20%)
- Leite Desnatado UHT Tipo A Parmalat 1L: R$ 4,29 (-10%)
- Leite UHT Semi Desnatado Carrefour Classic 1L: R$ 4,49 (-10%)
- Leite Semidesnatado UHT Ninho Levinho 1L: R$ 5,39 (-10%)

### Estrutura do HTML

O Carrefour usa **VTEX** como plataforma de e-commerce.

**Padrão de URLs:**
```
https://mercado.carrefour.com.br/[produto-slug]/p
```

Exemplo:
```
/leite-desnatado-uht-tipo-a-parmalat-1-litro-147516/p
```

### Seletores Identificados

| Elemento | Seletor CSS | Observação |
|----------|-------------|------------|
| **Link do Produto** | `a[href*="/p"]` | Todos os produtos terminam com `/p` |
| **Nome do Produto** | `img[alt]` dentro do link | Alt da imagem contém o nome |
| **Preço** | Classe com `price` ou `Price` | Texto: "R$ 4,29" |
| **Desconto** | Classe com `discount` | Percentual: "-10%" |
| **Imagem** | `img[src*="vtexassets"]` | CDN da VTEX |

### Seletores Sugeridos

```python
# Buscar todos os links de produtos
product_links = soup.select('a[href*="/p"]')

for link in product_links:
    # URL
    url = link.get('href')
    if not url.startswith('http'):
        url = 'https://mercado.carrefour.com.br' + url
    
    # Nome (via alt da imagem)
    img = link.select_one('img[alt]')
    name = img.get('alt') if img else None
    
    # Preço (buscar no texto do link)
    price_text = link.get_text()
    # Extrair "R$ X,XX" do texto
    import re
    price_match = re.search(r'R\$\s*([\d,]+)', price_text)
    price = price_match.group(1) if price_match else None
```

### Desafios

1. **JavaScript Pesado**: Carrefour usa React/VTEX que carrega produtos dinamicamente
2. **Seletores Dinâmicos**: Classes geradas automaticamente
3. **Paginação**: Produtos carregam via scroll infinito
4. **CEP Obrigatório**: Alguns produtos só aparecem com CEP

### Solução Alternativa: API VTEX

O Carrefour usa a API da VTEX para buscar produtos:

```
GET https://carrefourbrfood.vtexcommercestable.com.br/api/catalog_system/pub/products/search?ft=leite
```

**Vantagens:**
- ✅ Retorna JSON estruturado
- ✅ Mais rápido que scraping
- ✅ Mais confiável
- ✅ Sem necessidade de parsing HTML

**Estrutura da Resposta:**
```json
[
  {
    "productId": "147516",
    "productName": "Leite Desnatado UHT Tipo A Parmalat 1 Litro",
    "brand": "Parmalat",
    "link": "/leite-desnatado-uht-tipo-a-parmalat-1-litro-147516/p",
    "items": [
      {
        "itemId": "147516",
        "sellers": [
          {
            "sellerId": "1",
            "sellerName": "Carrefour",
            "commertialOffer": {
              "Price": 4.29,
              "ListPrice": 4.79,
              "AvailableQuantity": 100
            }
          }
        ]
      }
    ]
  }
]
```

### Recomendação

**Usar API VTEX** em vez de scraping HTML:

```python
import requests

def search_carrefour_api(query):
    url = f"https://carrefourbrfood.vtexcommercestable.com.br/api/catalog_system/pub/products/search"
    params = {
        'ft': query,
        '_from': 0,
        '_to': 9  # 10 primeiros resultados
    }
    
    response = requests.get(url, params=params)
    products = response.json()
    
    results = []
    for product in products:
        item = product['items'][0]
        seller = item['sellers'][0]
        offer = seller['commertialOffer']
        
        results.append({
            'name': product['productName'],
            'price': offer['Price'],
            'url': 'https://mercado.carrefour.com.br' + product['link'],
            'brand': product.get('brand'),
            'available': offer['AvailableQuantity'] > 0
        })
    
    return results
```

✅ **Método mais confiável e eficiente!**
