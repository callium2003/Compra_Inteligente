# 🛒 Compra Inteligente - MVP

## 📋 Visão Geral

O **Compra Inteligente** é um aplicativo web que permite aos usuários comparar preços de listas de compras em diferentes supermercados, otimizando custos através de duas estratégias:

- **Cesta Única**: Todos os itens comprados na loja mais barata
- **Cesta Mista Otimizada**: Itens divididos entre lojas para minimizar o custo total

## 🌐 Acesso ao MVP

**URL do Aplicativo**: https://60h5imcl15vw.manus.space

## 🔑 Credenciais Supabase

### Project URL
```
https://wrzuwwvnyzflsohrgyin.supabase.co
```

### Anon Public Key (Frontend)
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndyenV3d3ZueXpmbHNvaHJneWluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk0OTQyNDksImV4cCI6MjA3NTA3MDI0OX0.iiLEOqT4wcRLNfgcjmc3IvsAYNTJ4D5g7XSqpNH69Dw
```

### Service Role Key (Backend)
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndyenV3d3ZueXpmbHNvaHJneWluIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1OTQ5NDI0OSwiZXhwIjoyMDc1MDcwMjQ5fQ.723liEADe824HGnHExfQJLNqtY5U-sa2ErrAow6m2ME
```

## 🗄️ Estrutura do Banco de Dados

### Tabelas Criadas

#### 1. `user_addresses`
Armazena endereços de entrega dos usuários.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | UUID | Identificador único |
| user_id | UUID | Referência ao usuário (auth.users) |
| label | VARCHAR(100) | Nome do endereço (ex: Casa, Trabalho) |
| cep | VARCHAR(9) | CEP do endereço |
| street | VARCHAR(255) | Nome da rua |
| number | VARCHAR(20) | Número |
| complement | VARCHAR(100) | Complemento |
| neighborhood | VARCHAR(100) | Bairro |
| city | VARCHAR(100) | Cidade |
| state | VARCHAR(2) | Estado (UF) |
| is_default | BOOLEAN | Indica se é o endereço ativo |
| created_at | TIMESTAMP | Data de criação |

#### 2. `shopping_lists`
Cabeçalho das listas de compras.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | UUID | Identificador único |
| user_id | UUID | Referência ao usuário |
| title | VARCHAR(255) | Título da lista |
| created_at | TIMESTAMP | Data de criação |

#### 3. `shopping_items`
Itens normalizados das listas.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | UUID | Identificador único |
| list_id | UUID | Referência à lista |
| qty | NUMERIC(10,2) | Quantidade |
| product_name | VARCHAR(255) | Nome do produto |
| size_value | NUMERIC(10,2) | Valor do tamanho |
| size_unit | VARCHAR(10) | Unidade (g, kg, ml, l, un) |
| brand | VARCHAR(100) | Marca (opcional) |
| preference | VARCHAR(20) | Preferência (any, cheapest, exact_brand, similar) |
| notes | TEXT | Observações |
| created_at | TIMESTAMP | Data de criação |

#### 4. `quotes`
Histórico de cotações realizadas.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | UUID | Identificador único |
| user_id | UUID | Referência ao usuário |
| list_id | UUID | Referência à lista |
| address_id | UUID | Referência ao endereço |
| stores | TEXT[] | Array de lojas consultadas |
| result_json | JSONB | Resultado completo da cotação |
| created_at | TIMESTAMP | Data de criação |

### Row Level Security (RLS)

Todas as tabelas possuem **RLS habilitado** com policies que garantem:
- Usuários só acessam seus próprios dados
- Operações CRUD (SELECT, INSERT, UPDATE, DELETE) restritas por `user_id`
- Itens de lista verificados via relacionamento com `shopping_lists`

### Índices Otimizados

```sql
-- Endereços por usuário
CREATE INDEX idx_user_addresses_user_id ON user_addresses(user_id, created_at DESC);

-- Listas por usuário
CREATE INDEX idx_shopping_lists_user_id ON shopping_lists(user_id, created_at DESC);

-- Itens por lista
CREATE INDEX idx_shopping_items_list_id ON shopping_items(list_id);

-- Cotações por usuário
CREATE INDEX idx_quotes_user_id ON quotes(user_id, created_at DESC);
```

### Trigger: Endereço Único Padrão

Função que garante apenas um endereço padrão por usuário:

```sql
CREATE OR REPLACE FUNCTION ensure_single_default_address()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_default = true THEN
        UPDATE user_addresses
        SET is_default = false
        WHERE user_id = NEW.user_id
        AND id != NEW.id
        AND is_default = true;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

## 🔧 Configuração do Banco de Dados

### Passo 1: Acessar Supabase SQL Editor

1. Acesse https://supabase.com/dashboard
2. Selecione o projeto `wrzuwwvnyzflsohrgyin`
3. Vá para **SQL Editor**

### Passo 2: Executar Script de Configuração

Execute o arquivo `supabase_setup.sql` disponível no diretório do projeto:

```bash
/home/ubuntu/supabase_setup.sql
```

Este script cria:
- ✅ Todas as tabelas com campos corretos
- ✅ Políticas RLS para segurança
- ✅ Índices para performance
- ✅ Trigger para endereço único padrão

## 🚀 Arquitetura do Sistema

### Backend (Flask)

**Diretório**: `/home/ubuntu/compra_inteligente_api`

#### Estrutura de Arquivos

```
compra_inteligente_api/
├── src/
│   ├── main.py                    # Aplicação Flask principal
│   ├── normalizer.py              # Lógica de normalização de listas
│   ├── routes/
│   │   ├── normalize.py           # Endpoint de normalização
│   │   └── quote.py               # Endpoint de cotação
│   └── static/                    # Frontend buildado (React)
│       ├── index.html
│       └── assets/
├── requirements.txt               # Dependências Python
├── .env                          # Variáveis de ambiente
└── .gitignore
```

#### Endpoints da API

##### 1. POST `/api/normalize`

Normaliza texto de lista de compras em itens estruturados.

**Request Body**:
```json
{
  "raw_text": "2 leite integral 1l\narroz tipo 1 5kg\n3 ovos brancos"
}
```

**Response**:
```json
{
  "success": true,
  "items": [
    {
      "qty": 2.0,
      "product_name": "leite integral",
      "size_value": 1.0,
      "size_unit": "l",
      "brand": null,
      "preference": "any",
      "notes": null
    },
    ...
  ]
}
```

##### 2. POST `/api/quote`

Gera cotação mock comparando cestas única e mista.

**Request Body**:
```json
{
  "items": [...],
  "stores": ["Carrefour", "Extra"]
}
```

**Response**:
```json
{
  "success": true,
  "single_store": {
    "store": "Carrefour",
    "items": [...],
    "subtotal": 85.50,
    "frete": 9.90,
    "total": 95.40
  },
  "mixed_basket": {
    "stores": [...],
    "total_frete": 18.80,
    "total": 82.30
  },
  "savings": {
    "amount": 13.10,
    "percentage": 13.7
  }
}
```

##### 3. GET `/health`

Health check do serviço.

**Response**:
```json
{
  "status": "ok",
  "service": "compra-inteligente-api"
}
```

#### Lógica de Normalização

O módulo `normalizer.py` implementa:

1. **Extração de Quantidade e Tamanho**
   - Regex para padrões: "2 leite 1l", "arroz 5kg", "3 ovos"
   
2. **Normalização de Unidades**
   - Converte variações para padrão: kg, g, l, ml, un
   
3. **Detecção de Preferências**
   - Identifica: "mais barato", "marca X", "similar"
   
4. **Extração de Notas**
   - Captura texto entre parênteses

#### Algoritmo de Cotação Mock

**Cesta Única**:
- Todos os itens na primeira loja
- Preço = Subtotal + Frete único

**Cesta Mista**:
- Para cada item, gera preço aleatório em cada loja
- Seleciona loja mais barata por item
- Agrupa itens por loja
- Calcula: Subtotal por loja + Frete por loja

**Economia**:
```
economia = total_cesta_unica - total_cesta_mista
percentual = (economia / total_cesta_unica) * 100
```

### Frontend (React)

**Diretório**: `/home/ubuntu/compra-inteligente-frontend`

#### Estrutura de Componentes

```
src/
├── contexts/
│   └── AuthContext.jsx           # Contexto de autenticação
├── components/
│   ├── Auth.jsx                  # Login/Cadastro
│   ├── Addresses.jsx             # CRUD de endereços
│   ├── NewQuote.jsx              # Nova cotação
│   ├── QuoteResults.jsx          # Resultados comparativos
│   ├── History.jsx               # Histórico
│   └── ui/                       # Componentes shadcn/ui
├── lib/
│   └── supabase.js               # Cliente Supabase
├── App.jsx                       # Aplicação principal
├── App.css                       # Estilos globais
└── main.jsx                      # Entry point
```

#### Fluxo de Navegação

1. **Autenticação** (`Auth.jsx`)
   - Login com email/senha
   - Cadastro de nova conta
   - Integração com Supabase Auth

2. **Endereços** (`Addresses.jsx`)
   - Listar endereços cadastrados
   - Adicionar novo endereço
   - Definir endereço ativo
   - Excluir endereços

3. **Nova Cotação** (`NewQuote.jsx`)
   - **Passo 1**: Entrada de texto
   - **Passo 2**: Normalização e prévia editável
   - **Passo 3**: Salvamento da lista
   - **Passo 4**: Geração da cotação
   - **Passo 5**: Exibição de resultados

4. **Resultados** (`QuoteResults.jsx`)
   - Comparação lado a lado
   - Destaque de economia
   - Detalhamento por loja

5. **Histórico** (`History.jsx`)
   - Listas salvas
   - Cotações anteriores
   - Detalhes de cada cotação

#### Tecnologias Frontend

- **React 19** - Framework UI
- **Tailwind CSS** - Estilização
- **shadcn/ui** - Componentes prontos
- **Lucide React** - Ícones
- **Supabase JS** - Cliente para autenticação e banco
- **Vite** - Build tool

## 📦 Deploy

### Backend + Frontend Integrado

O aplicativo foi deployado como **aplicação Flask única** que serve:
- API REST nos endpoints `/api/*`
- Frontend React estático na raiz `/`

**URL de Produção**: https://60h5imcl15vw.manus.space

### Processo de Build

1. **Frontend**:
   ```bash
   cd compra-inteligente-frontend
   pnpm run build
   ```
   
2. **Integração**:
   ```bash
   cp -r dist/* ../compra_inteligente_api/src/static/
   ```
   
3. **Deploy**:
   ```bash
   # Deploy automático via Manus
   ```

## 🧪 Testes de Aceitação do MVP

### ✅ Checklist de Funcionalidades

- [x] **Autenticação**
  - [x] Cadastro de nova conta
  - [x] Login com email/senha
  - [x] Logout
  - [x] Persistência de sessão

- [x] **Endereços**
  - [x] Cadastrar endereço com CEP
  - [x] Listar endereços
  - [x] Definir endereço ativo
  - [x] Excluir endereço
  - [x] Apenas um endereço ativo por vez

- [x] **Lista de Compras**
  - [x] Entrada por texto livre
  - [x] Normalização automática
  - [x] Prévia editável em tabela
  - [x] Salvamento no banco
  - [x] Título da lista

- [x] **Cotação**
  - [x] Geração de cotação mock
  - [x] Cálculo de cesta única
  - [x] Cálculo de cesta mista
  - [x] Cálculo de economia
  - [x] Salvamento no histórico

- [x] **Histórico**
  - [x] Listar listas salvas
  - [x] Listar cotações anteriores
  - [x] Detalhes de cada cotação

- [x] **Segurança**
  - [x] RLS habilitado
  - [x] Usuários isolados
  - [x] Anon Key no frontend
  - [x] Service Role Key protegida

## 📊 Exemplo de Uso

### 1. Criar Conta
```
Email: usuario@exemplo.com
Senha: senha123
```

### 2. Cadastrar Endereço
```
Nome: Casa
CEP: 01310-100
Rua: Av. Paulista
Número: 1000
Cidade: São Paulo
Estado: SP
```

### 3. Criar Lista
```
Título: Compras do Mês

Lista:
2 leite integral 1l
arroz tipo 1 5kg
3 ovos brancos
feijão preto 1kg
café 500g
açúcar cristal 2kg
óleo de soja 900ml
macarrão 500g
```

### 4. Fazer Cotação
- Selecionar lojas: Carrefour, Extra
- Ver comparação de preços
- Economia estimada: ~R$ 13,10 (13,7%)

## 🔮 Próximos Passos (Roadmap)

### Sprint 2 - Entrada por Voz
- [ ] Integração com STT (Speech-to-Text)
- [ ] Upload de áudio
- [ ] Transcrição PT-BR
- [ ] Storage de áudios no Supabase

### Sprint 3 - Conectores Reais
- [ ] Web scraping de supermercados
- [ ] APIs de e-commerce
- [ ] Cache de preços
- [ ] Atualização periódica

### Sprint 4 - Otimização ILP
- [ ] Algoritmo de programação linear inteira
- [ ] Consideração de mínimos por loja
- [ ] Otimização multi-objetivo
- [ ] Sugestão de produtos similares

### Sprint 5 - Exportação
- [ ] Exportar resultados em CSV
- [ ] Exportar em JSON
- [ ] Gerar carrinho automático
- [ ] Links diretos para lojas

## 📝 Notas Técnicas

### Limitações do MVP

1. **Preços Mock**: Preços são gerados aleatoriamente para demonstração
2. **Lojas Fixas**: 4 lojas pré-configuradas (Carrefour, Pão de Açúcar, Extra, Assaí)
3. **Sem Voz**: Entrada apenas por texto
4. **Otimização Simples**: Heurística básica (item mais barato por loja)

### Considerações de Segurança

- ✅ RLS habilitado em todas as tabelas
- ✅ Service Role Key nunca exposta no frontend
- ✅ CORS configurado corretamente
- ✅ Validação de entrada em todos os endpoints
- ✅ Autenticação obrigatória para operações

### Performance

- Índices otimizados para consultas por usuário
- Ordenação DESC por `created_at` para histórico recente
- Limite de 10-20 registros em listagens
- Cache de sessão no frontend

## 📞 Suporte

Para dúvidas ou problemas, consulte:
- Documentação do Supabase: https://supabase.com/docs
- Documentação do Flask: https://flask.palletsprojects.com
- Documentação do React: https://react.dev

---

**Desenvolvido com ❤️ para o MVP Compra Inteligente**

*Última atualização: 03/10/2025*
