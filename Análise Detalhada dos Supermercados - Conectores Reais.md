# Análise Detalhada dos Supermercados - Conectores Reais

## 1. Extra Mercado ✅ ANALISADO

**URL Base**: https://www.extramercado.com.br

### Estrutura de URLs

#### Busca
- **Padrão**: `https://www.extramercado.com.br/busca?terms={produto}`
- **Exemplo**: `https://www.extramercado.com.br/busca?terms=leite`

#### Produto Individual
- **Padrão**: `https://www.extramercado.com.br/produto/{id}/{slug}`
- **Exemplo**: `https://www.extramercado.com.br/produto/5729/leite-longa-vida-integral-dalia-1-litro`

### Dados Disponíveis

**Na Página de Busca:**
- Nome do produto
- Preço atual (com desconto)
- Preço anterior (riscado)
- Percentual de desconto
- Imagem do produto
- Link para página do produto

**Na Página do Produto:**
```
Nome: Leite Longa Vida Integral DÁLIA 1 Litro
Código: 6017309
Preço Atual: R$ 4,69
Preço Anterior: R$ 5,39
Desconto: -12%
Marca: Dália
Tamanho: 1 Litro
Categoria: Alimentos > Básico da Despensa > Leites > Leite Integral
Ingredientes: Leite integral e estabilizante: citrato de sódio INS 331iii
Glúten: Não Contém
Lactose: Contém
```

### Método de Extração

**Scraping HTML:**
```python
# Busca
GET /busca?terms=leite
# Parse HTML para extrair:
# - Lista de produtos
# - Preços
# - Links

# Produto
GET /produto/{id}/{slug}
# Parse HTML para extrair:
# - Nome completo
# - Preço atual
# - Marca
# - Tamanho
# - Código
```

### Limitações
- ⚠️ Requer CEP para cálculo de frete
- ⚠️ Preços podem variar por região
- ⚠️ Rate limiting necessário
- ⚠️ Sem API pública identificada (scraping HTML)

---

## 2. Carrefour ✅ ANALISADO

**URL Base**: https://mercado.carrefour.com.br

### Estrutura de URLs

#### Busca
- **Padrão**: `https://mercado.carrefour.com.br/busca/{produto}`
- **Exemplo**: `https://mercado.carrefour.com.br/busca/leite`

#### Produto Individual
- **Padrão**: `https://mercado.carrefour.com.br/{slug}/p`
- **Exemplo**: `https://mercado.carrefour.com.br/leite-integral-uht-tipo-a-parmalat-1-litro-147540/p`

### Dados Disponíveis

**Na Página de Busca:**
- Nome do produto
- Preço atual (com desconto)
- Preço anterior (riscado)
- Percentual de desconto
- Imagem do produto
- Botão "Adicionar"
- Filtros (Marca, Categoria, Subcategoria, etc.)

**Na Página do Produto:**
```
Nome: Leite Integral UHT Tipo A Parmalat 1 Litro
Marca: Parmalat
Código: 2051
Preço Atual: R$ 4,49
Preço Anterior: R$ 4,99
Desconto: -10%
Conteúdo: 1 L
País: Brasil
Tipo: Leite
Apresentação: Líquido
Embalagem: Caixa
Fabricante: Lactalis
Glúten: Não Contém
Lactose: Contém
Ingredientes: Leite integral e estabilizantes (citrato de sódio, trifosfato de sódio, monofosfato de sódio e difosfato de sódio)
Categoria: Padaria e Matinais > Leites > Leite UHT > Parmalat
```

**Informações Nutricionais Completas:**
- Calorias: 113 kcal por porção (200ml)
- Carboidratos: 8,8g
- Proteínas: 6,0g
- Gorduras Totais: 6,0g
- Gorduras Saturadas: 4,0g
- Sódio: 138mg
- Cálcio: 230mg

### Método de Extração

**Scraping HTML:**
```python
# Busca
GET /busca/{produto}
# Parse HTML para extrair:
# - Grid de produtos
# - Preços
# - Links
# - Filtros disponíveis

# Produto
GET /{slug}/p
# Parse HTML para extrair:
# - Dados completos do produto
# - Especificações técnicas
# - Informações nutricionais
```

### Filtros Disponíveis
- Departamento (Padaria e Matinais, Bebê e Infantil, etc.)
- Categoria (Leites, Alimentação Infantil, etc.)
- Subcategoria (Leite UHT, Leite Pasteurizado, etc.)
- Marca (Parmalat, Piracanjuba, Goiasminas, Ninho, etc.)
- Preferência de Consumo (Zero Lactose, etc.)
- Ordenação (Relevância, Mais vendidos, Menor preço, etc.)

### Limitações
- ⚠️ Requer CEP para disponibilidade e frete
- ⚠️ Preços podem variar por região
- ⚠️ Rate limiting necessário
- ⚠️ Sem API pública identificada (scraping HTML)
- ⚠️ Pode requerer cookies/sessão

---

## 3. Mambo ⏳ PENDENTE

**URL Base**: https://www.mambo.com.br

### A Analisar:
- [ ] Estrutura de busca
- [ ] Formato de URLs
- [ ] Dados disponíveis
- [ ] Método de extração
- [ ] Limitações

---

## 4. Mercado Livre ⏳ PENDENTE

**URL Base**: https://www.mercadolivre.com.br/ofertas/supermercado

### A Analisar:
- [ ] Estrutura de busca
- [ ] API pública (ML tem API oficial)
- [ ] Formato de dados
- [ ] Autenticação necessária
- [ ] Limitações

### Nota:
Mercado Livre possui **API oficial** documentada:
- https://developers.mercadolivre.com.br/
- Pode ser mais confiável que scraping
- Requer cadastro de aplicação

---

## Comparação dos Supermercados

| Característica | Extra | Carrefour | Mambo | Mercado Livre |
|----------------|-------|-----------|-------|---------------|
| **Análise** | ✅ | ✅ | ⏳ | ⏳ |
| **URL de Busca** | `/busca?terms=` | `/busca/` | ? | ? |
| **Preços Visíveis** | ✅ | ✅ | ? | ? |
| **Marca Visível** | ✅ | ✅ | ? | ? |
| **Tamanho Visível** | ✅ | ✅ | ? | ? |
| **API Pública** | ❌ | ❌ | ? | ✅ (provável) |
| **Requer CEP** | ✅ | ✅ | ? | ? |
| **Filtros** | Básicos | Avançados | ? | ? |

---

## Estratégia de Implementação

### Arquitetura Proposta

```
SupermarketConnector (Base Class)
├── ExtraConnector
├── CarrefourConnector
├── MamboConnector
└── MercadoLivreConnector
```

### Classe Base

```python
class SupermarketConnector:
    def __init__(self, name, base_url):
        self.name = name
        self.base_url = base_url
        self.session = requests.Session()
        self.cache = {}
    
    def search(self, product_name, cep=None):
        """Busca produto e retorna lista de resultados"""
        pass
    
    def get_product_details(self, product_url):
        """Obtém detalhes completos do produto"""
        pass
    
    def normalize_price(self, price_string):
        """Normaliza string de preço para float"""
        # "R$ 4,69" -> 4.69
        pass
    
    def extract_size(self, product_name):
        """Extrai tamanho do nome do produto"""
        # "Leite 1L" -> (1.0, "l")
        pass
    
    def rate_limit(self):
        """Implementa rate limiting"""
        time.sleep(1)  # 1 segundo entre requisições
```

### Implementação Extra

```python
class ExtraConnector(SupermarketConnector):
    def __init__(self):
        super().__init__("Extra", "https://www.extramercado.com.br")
    
    def search(self, product_name, cep=None):
        url = f"{self.base_url}/busca?terms={product_name}"
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        products = []
        # Parse HTML para extrair produtos
        for item in soup.select('.product-card'):
            products.append({
                'name': item.select_one('a').text,
                'price': self.normalize_price(item.select_one('.price').text),
                'url': item.select_one('a')['href']
            })
        
        return products
```

### Implementação Carrefour

```python
class CarrefourConnector(SupermarketConnector):
    def __init__(self):
        super().__init__("Carrefour", "https://mercado.carrefour.com.br")
    
    def search(self, product_name, cep=None):
        url = f"{self.base_url}/busca/{product_name}"
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        products = []
        # Parse HTML para extrair produtos
        # Estrutura específica do Carrefour
        
        return products
```

### Sistema de Cache

```python
import hashlib
import json
import time
from pathlib import Path

class PriceCache:
    def __init__(self, cache_dir="/tmp/price_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = 3600  # 1 hora
    
    def get_cache_key(self, store, product):
        key = f"{store}_{product}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, store, product):
        cache_file = self.cache_dir / f"{self.get_cache_key(store, product)}.json"
        if cache_file.exists():
            data = json.loads(cache_file.read_text())
            if time.time() - data['timestamp'] < self.ttl:
                return data['result']
        return None
    
    def set(self, store, product, result):
        cache_file = self.cache_dir / f"{self.get_cache_key(store, product)}.json"
        data = {
            'timestamp': time.time(),
            'result': result
        }
        cache_file.write_text(json.dumps(data))
```

### Rate Limiting

```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self):
        self.last_request = defaultdict(float)
        self.min_interval = {
            'Extra': 1.0,      # 1 req/segundo
            'Carrefour': 1.0,  # 1 req/segundo
            'Mambo': 1.0,
            'MercadoLivre': 0.5  # API pode ser mais rápida
        }
    
    def wait(self, store):
        now = time.time()
        elapsed = now - self.last_request[store]
        min_interval = self.min_interval.get(store, 1.0)
        
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        
        self.last_request[store] = time.time()
```

---

## Integração com Sistema de Cotação

### Fluxo Atual (Mock)

```
1. Usuário envia lista de itens
2. Para cada item:
   - Gera preço aleatório para cada loja
3. Calcula cesta única e cesta mista
4. Retorna resultado
```

### Fluxo Novo (Real)

```
1. Usuário envia lista de itens
2. Para cada item:
   a. Verifica cache
   b. Se não houver cache:
      - Busca em cada loja (Extra, Carrefour, Mambo, ML)
      - Extrai preços reais
      - Salva no cache
   c. Se houver erro:
      - Fallback para preço mock
      - Log do erro
3. Calcula cesta única e cesta mista com preços reais
4. Retorna resultado
```

### Endpoint Atualizado

```python
@app.route('/api/quote', methods=['POST'])
def quote():
    data = request.json
    items = data.get('items', [])
    cep = data.get('cep')  # Novo: CEP para busca
    
    # Conectores
    connectors = [
        ExtraConnector(),
        CarrefourConnector(),
        MamboConnector(),
        MercadoLivreConnector()
    ]
    
    # Cache e rate limiter
    cache = PriceCache()
    rate_limiter = RateLimiter()
    
    results = []
    for item in items:
        product_name = item['product_name']
        item_results = {}
        
        for connector in connectors:
            # Verificar cache
            cached = cache.get(connector.name, product_name)
            if cached:
                item_results[connector.name] = cached
                continue
            
            # Rate limiting
            rate_limiter.wait(connector.name)
            
            # Buscar preço real
            try:
                search_results = connector.search(product_name, cep)
                if search_results:
                    best_match = search_results[0]  # Primeiro resultado
                    item_results[connector.name] = {
                        'price': best_match['price'],
                        'name': best_match['name'],
                        'url': best_match['url']
                    }
                    cache.set(connector.name, product_name, item_results[connector.name])
                else:
                    # Fallback para mock
                    item_results[connector.name] = generate_mock_price(item)
            except Exception as e:
                logger.error(f"Erro ao buscar {product_name} em {connector.name}: {e}")
                item_results[connector.name] = generate_mock_price(item)
        
        results.append({
            'item': item,
            'prices': item_results
        })
    
    # Calcular cestas
    single_basket = calculate_single_basket(results)
    mixed_basket = calculate_mixed_basket(results)
    
    return jsonify({
        'success': True,
        'single_basket': single_basket,
        'mixed_basket': mixed_basket,
        'savings': calculate_savings(single_basket, mixed_basket)
    })
```

---

## Próximos Passos

### Fase 1: Completar Análise ⏳
- [x] Extra - Concluído
- [x] Carrefour - Concluído
- [ ] Mambo - Analisar estrutura
- [ ] Mercado Livre - Verificar API oficial

### Fase 2: Implementar Conectores
- [ ] Criar classe base `SupermarketConnector`
- [ ] Implementar `ExtraConnector`
- [ ] Implementar `CarrefourConnector`
- [ ] Implementar `MamboConnector`
- [ ] Implementar `MercadoLivreConnector`

### Fase 3: Sistema de Suporte
- [ ] Implementar `PriceCache`
- [ ] Implementar `RateLimiter`
- [ ] Sistema de logging
- [ ] Tratamento de erros

### Fase 4: Integração
- [ ] Atualizar endpoint `/api/quote`
- [ ] Adicionar campo CEP no frontend
- [ ] Manter fallback para mock
- [ ] Testes unitários

### Fase 5: Deploy e Testes
- [ ] Testar cada conector individualmente
- [ ] Testar cotação completa
- [ ] Validar preços reais vs mock
- [ ] Deploy da atualização

---

## Considerações Finais

### Vantagens
- ✅ Preços reais e atualizados
- ✅ Comparação precisa entre lojas
- ✅ Economia real calculada
- ✅ Links diretos para produtos

### Desafios
- ⚠️ Scraping pode quebrar se sites mudarem
- ⚠️ Rate limiting necessário para evitar bloqueio
- ⚠️ Necessidade de CEP para preços regionais
- ⚠️ Produtos podem não estar disponíveis em todas as lojas

### Mitigações
- ✅ Cache para reduzir requisições
- ✅ Fallback para preços mock em caso de erro
- ✅ Logging detalhado para debug
- ✅ Retry logic com backoff exponencial

---

*Última atualização: 03/10/2025*
