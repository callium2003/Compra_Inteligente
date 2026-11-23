# PCI — Compra Inteligente (MVP) 🛒⚡

O **Compra Inteligente** é um aplicativo web projetado para otimizar suas compras de supermercado, comparando preços em tempo real entre os principais estabelecimentos e sugerindo a melhor combinação de itens para o menor custo total.

## Estado atual

O repositório contém um **MVP executável**, mas ainda não um comparador pronto para
produção. A API normaliza listas, consulta conectores em paralelo e calcula as
cestas. Carrefour e Extra dependem da estrutura atual dos sites; Mambo e Mercado
Livre podem recorrer a dados simulados quando a consulta externa falha. O histórico
de preços também é demonstrativo. Essas respostas são identificadas pelo campo
`mock`, para não serem confundidas com preços confirmados.

## 🚀 Funcionalidades Principais

### 1. Comparação em Tempo Real
- **Conectores Reais**: Integração com Carrefour (Scraping Real), Mambo (API VTEX), Mercado Livre e Extra.
- **Busca Paralela**: Utiliza `asyncio` para consultar as lojas sem bloquear as demais buscas.

### 2. Inteligência de Compra
- **Matching Inteligente**: Algoritmo baseado em palavras-chave e similaridade de strings para classificar os resultados.
- **Cesta Mista**: O sistema divide a lista pelo menor preço e considera o impacto dos fretes na comparação com a cesta única.
- **Filtros Avançados**: Priorização de marcas específicas e opção exclusiva para produtos orgânicos.

### 3. Visualização e Histórico
- **Gráficos de Evolução**: Acompanhe a variação de preços dos produtos nos últimos 7, 30 ou 90 dias.
- **Histórico demonstrativo**: A tela existente permite validar o fluxo enquanto a persistência real é concluída.

## 🛠️ Arquitetura Técnica

- **Frontend**: React 18, Tailwind CSS, Shadcn/UI, Recharts.
- **Backend**: Flask (Python), Asyncio, Requests, BeautifulSoup4.
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

## ▶️ Executar e validar

Requer Python 3.11 ou mais recente. O build atual do frontend já está em
`src/static` e é servido pela aplicação Flask.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.main
```

A aplicação fica disponível em `http://localhost:5000` e o health check em
`http://localhost:5000/health`. Para executar a suíte automatizada:

```bash
python -m pytest -q
```

## Próximas prioridades

1. Recriar a estrutura-fonte do frontend (os componentes JSX na raiz dependem de
   aliases e componentes UI que não estão versionados) e gerar o build de forma
   reproduzível.
2. Substituir os fallbacks simulados por integrações autorizadas e observáveis,
   com testes de contrato para cada loja.
3. Persistir cotações e evolução de preços no Supabase em vez de gerar histórico
   demonstrativo.
4. Adicionar autenticação da API, limitar CORS por ambiente e validar CEP antes de
   uma implantação pública.
5. Consolidar os módulos duplicados entre a raiz e `src/`, mantendo uma única
   implementação da aplicação.

## 🔮 Roadmap Futuro

- [ ] Entrada de lista por Voz (STT).
- [ ] Finalização automática de carrinhos nos sites dos supermercados.
- [ ] Aplicativo Mobile (React Native).
- [ ] Alertas de queda de preço para itens favoritos.

---
Desenvolvido como parte do projeto PCI - MVP Sprint 1-7.
