# PCI — Compra Inteligente (MVP) 🛒⚡

O **Compra Inteligente** é um aplicativo web projetado para otimizar suas compras de supermercado, comparando preços em tempo real entre os principais estabelecimentos e sugerindo a melhor combinação de itens para o menor custo total.

## 🚀 Funcionalidades Principais

### 1. Comparação em Tempo Real
- **Conectores Reais**: Integração com Carrefour (Scraping Real), Mambo (API VTEX), Mercado Livre e Extra.
- **Busca Paralela**: Utiliza `asyncio` e `httpx` para consultar todas as lojas simultaneamente, reduzindo o tempo de resposta em 75%.

### 2. Inteligência de Compra
- **Matching Inteligente**: Algoritmo baseado em similaridade de string (Levenshtein) para garantir que os produtos comparados sejam idênticos.
- **Cesta Mista Ótima**: O sistema divide sua lista entre os supermercados para garantir o menor preço total possível.
- **Filtros Avançados**: Priorização de marcas específicas e opção exclusiva para produtos orgânicos.

### 3. Visualização e Histórico
- **Gráficos de Evolução**: Acompanhe a variação de preços dos produtos nos últimos 7, 30 ou 90 dias.
- **Histórico Completo**: Todas as suas listas e cotações ficam salvas com segurança no Supabase.

## 🛠️ Arquitetura Técnica

- **Frontend**: React 18, Tailwind CSS, Shadcn/UI, Recharts.
- **Backend**: Flask (Python), Asyncio, HTTPX, BeautifulSoup4.
- **Banco de Dados & Auth**: Supabase (PostgreSQL com RLS).
- **Infraestrutura**: Deploy unificado (Frontend estático servido pelo Flask).

## 📋 Estrutura do Projeto

```text
/src
  /connectors    # Scrapers e APIs dos supermercados
  /routes        # Endpoints da API (Normalize, Quote, History)
  /utils         # Algoritmos de Matching e Processamento
  /static        # Build do Frontend React
```

## 🔧 Configuração do Banco de Dados

Para que o aplicativo funcione corretamente, você deve executar o script `supabase_setup.sql` no seu painel do Supabase. Ele criará as tabelas:
- `user_addresses`: Gerenciamento de CEPs de entrega.
- `shopping_lists`: Cabeçalhos das listas de compras.
- `shopping_items`: Itens normalizados.
- `quotes`: Histórico de resultados de cotações.

## 🔮 Roadmap Futuro

- [ ] Entrada de lista por Voz (STT).
- [ ] Finalização automática de carrinhos nos sites dos supermercados.
- [ ] Aplicativo Mobile (React Native).
- [ ] Alertas de queda de preço para itens favoritos.

---
Desenvolvido como parte do projeto PCI - MVP Sprint 1-7.
