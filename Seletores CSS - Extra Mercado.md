# Seletores CSS - Extra Mercado

## Análise Completa do HTML

### Estrutura do Card de Produto

```
div.Card-sc-yvvqkp-0.bUWsSi.CardStyled-sc-20azeh-0.kFyEoJ
├── div.TopSection-sc-20azeh-1 (imagem)
│   └── a[href*="/produto/"]
│       └── img (imagem do produto)
├── div.PriceContainer-sc-20azeh-3
│   └── p.PriceValue-sc-20azeh-4 (preço: "R$ 13,90")
└── div.DescriptionContainer-sc-20azeh-8
    └── div.TitleContainer-sc-20azeh-9
        └── a.Title-sc-20azeh-10 (nome do produto)
```

### Seletores Identificados

| Elemento | Seletor CSS | Exemplo |
|----------|-------------|---------|
| **Card Principal** | `.Card-sc-yvvqkp-0` ou `.CardStyled-sc-20azeh-0` | Container do produto |
| **Nome do Produto** | `.Title-sc-20azeh-10` ou `a[href*="/produto/"]` | "Pack Leite Fermentado..." |
| **Preço** | `.PriceValue-sc-20azeh-4` | "R$ 13,90" |
| **Link do Produto** | `a[href*="/produto/"]` | "/produto/106572/..." |
| **Imagem** | `.Image-sc-20azeh-2` | URL da imagem |

### Observações

1. **Classes Dinâmicas**: O Extra usa styled-components com hashes (sc-yvvqkp-0, sc-20azeh-0)
   - Essas classes podem mudar entre deploys
   - Melhor usar seletores mais estáveis

2. **Seletores Mais Estáveis**:
   ```css
   /* Card */
   div[class*="CardStyled"]
   
   /* Preço */
   p[class*="PriceValue"]
   
   /* Título */
   a[class*="Title"]
   
   /* Link */
   a[href*="/produto/"]
   ```

3. **Estrutura de Preço**:
   - Preço atual: `p[class*="PriceValue"]`
   - Formato: "R$ 13,90 " (com espaço no final)

4. **Produtos Patrocinados**:
   - Têm tag "Patrocinado" em `.SponsoredLabel-sc-20azeh-15`
   - Podem ser filtrados ou incluídos

### Código de Extração Sugerido

```python
# Buscar todos os cards
cards = soup.select('div[class*="CardStyled"]')

for card in cards:
    # Nome
    title_elem = card.select_one('a[class*="Title"]')
    name = title_elem.get_text(strip=True) if title_elem else None
    
    # Preço
    price_elem = card.select_one('p[class*="PriceValue"]')
    price_text = price_elem.get_text(strip=True) if price_elem else None
    
    # URL
    link_elem = card.select_one('a[href*="/produto/"]')
    url = link_elem.get('href') if link_elem else None
    
    # Processar
    if name and price_text:
        price = normalize_price(price_text)  # "R$ 13,90" -> 13.90
        full_url = f"https://www.extramercado.com.br{url}"
```

### Teste Manual

URL de teste: https://www.extramercado.com.br/busca?terms=leite

Produtos encontrados: 527
Primeiros resultados:
- Pack Leite Fermentado Desnatado Yakult: R$ 13,90
- Bebida Láctea UHT Chocolate Zero Lactose Nescau: R$ 3,99
- Leite UHT Integral Qualitá: R$ 4,29

✅ Seletores validados e funcionais!
