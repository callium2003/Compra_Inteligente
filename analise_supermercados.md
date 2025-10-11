# Análise dos Supermercados - Conectores Reais

## 1. Extra Mercado ✅

**URL**: https://www.extramercado.com.br

### Estrutura Identificada:

#### Busca de Produtos
- **URL de busca**: `https://www.extramercado.com.br/busca?terms={produto}`
- **Exemplo**: `https://www.extramercado.com.br/busca?terms=leite`

#### Página de Produto
- **URL**: `https://www.extramercado.com.br/produto/{id}/{slug}`
- **Exemplo**: `https://www.extramercado.com.br/produto/5729/leite-longa-vida-integral-dalia-1-litro`

#### Dados Extraídos:
- ✅ **Nome do produto**: "Leite Longa Vida Integral DÁLIA 1 Litro"
- ✅ **Preço atual**: R$ 4,69
- ✅ **Preço anterior**: R$ 5,39
- ✅ **Desconto**: -12%
- ✅ **Código**: 6017309
- ✅ **Marca**: Dália
- ✅ **Tamanho**: 1 Litro
- ✅ **Categoria**: Alimentos > Básico da Despensa > Leites > Leite Integral

#### Método de Scraping:
- **Busca**: Fazer GET em `/busca?terms={produto}`
- **Parsing**: Extrair lista de produtos do HTML
- **Detalhes**: Acessar página individual do produto
- **Preço**: Extrair do elemento com preço atual

#### Limitações:
- ⚠️ Requer CEP para calcular frete
- ⚠️ Preços podem variar por região
- ⚠️ Necessário respeitar rate limiting

---

## 2. Carrefour

**URL**: https://mercado.carrefour.com.br

### A Analisar:
- [ ] Estrutura de busca
- [ ] API endpoints
- [ ] Formato de dados
- [ ] Requisitos de autenticação

---

## 3. Mambo

**URL**: https://www.mambo.com.br

### A Analisar:
- [ ] Estrutura de busca
- [ ] API endpoints
- [ ] Formato de dados
- [ ] Requisitos de autenticação

---

## 4. Mercado Livre

**URL**: https://www.mercadolivre.com.br/ofertas/supermercado

### A Analisar:
- [ ] Estrutura de busca
- [ ] API pública disponível
- [ ] Formato de dados
- [ ] Requisitos de autenticação

---

## Estratégia de Implementação

### Fase 1: Análise Completa
1. ✅ Extra - Concluído
2. ⏳ Carrefour - Em andamento
3. ⏳ Mambo - Pendente
4. ⏳ Mercado Livre - Pendente

### Fase 2: Desenvolvimento dos Conectores
- Criar classe base `SupermarketConnector`
- Implementar conectores específicos para cada loja
- Sistema de cache Redis/arquivo
- Rate limiting por loja

### Fase 3: Integração
- Substituir preços mock por preços reais
- Manter fallback para mock em caso de erro
- Logging de requisições

### Fase 4: Testes
- Testar cada conector individualmente
- Testar cotação completa
- Validar preços e disponibilidade

---

## Notas Técnicas

### Extra Mercado

**Estrutura HTML observada:**
```html
<!-- Lista de produtos -->
<div class="product-card">
  <img alt="Nome do Produto"/>
  <a>Nome do Produto</a>
  <span>R$ 4,69</span>
  <span>R$ 5,39</span>
  <span>-12%</span>
</div>

<!-- Página de produto -->
<h1>Leite Longa Vida Integral DÁLIA 1 Litro</h1>
<span>Cód.: 6017309</span>
<span>R$ 4,69</span>
<span>R$ 5,39</span>
<span>-12%</span>
```

**Possível API (a investigar):**
- Pode haver endpoints JSON para busca
- Verificar Network tab para chamadas XHR/Fetch
- Possível uso de GraphQL ou REST API

---

## Próximos Passos

1. ✅ Analisar Extra Mercado
2. 🔄 Analisar Carrefour
3. ⏳ Analisar Mambo
4. ⏳ Analisar Mercado Livre
5. ⏳ Implementar conectores
6. ⏳ Integrar com sistema de cotação
7. ⏳ Testar e validar
