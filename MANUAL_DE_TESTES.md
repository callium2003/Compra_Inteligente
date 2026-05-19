# Manual de Testes — Compra Inteligente 🧪

Este guia orienta como testar todas as funcionalidades implementadas do MVP (Sprints 1 a 7).

## 1. Preparação
1. Acesse o link do aplicativo: [https://60h5imcl15vw.manus.space](https://60h5imcl15vw.manus.space)
2. Crie uma nova conta ou faça login.
3. **Importante**: Certifique-se de que o script `supabase_setup.sql` foi executado no seu projeto Supabase.

## 2. Fluxo de Endereço (Sprint 1)
- Vá em "Meus Endereços".
- Adicione um novo endereço com um CEP válido (Ex: 01310-100).
- Marque-o como "Endereço Ativo".
- **O que observar**: O sistema deve salvar e listar o endereço corretamente.

## 3. Normalização de Lista (Sprint 2)
- Vá em "Nova Cotação".
- Cole a seguinte lista no campo de texto:
  ```text
  2 leite integral 1l
  arroz 5kg
  feijão preto 1kg
  ```
- Clique em "Validar & Normalizar".
- **O que observar**: O sistema deve transformar o texto em uma tabela com colunas de Quantidade, Produto, Tamanho e Unidade.

## 4. Filtros Avançados e Gráficos (Sprint 7)
- Na tela de revisão da lista (após normalizar):
- Clique em **"Filtros Avançados"**.
- Digite uma marca (Ex: "Nestlé") e aplique.
- Clique em **"Ver Gráfico"**.
- **O que observar**: O gráfico de evolução de preços deve aparecer para o primeiro item da lista. Os filtros devem ser aplicados na cotação final.

## 5. Cotação em Tempo Real (Sprints 3, 4, 5 e 6)
- Com a lista revisada, clique em **"Fazer Cotação"**.
- Aguarde de 5 a 10 segundos.
- **O que observar**:
  - O sistema deve mostrar os resultados do **Carrefour (Preços Reais)**.
  - Deve exibir a comparação entre **Cesta Única** e **Cesta Mista**.
  - Deve destacar a economia gerada pela Cesta Mista.

## 6. Histórico (Sprint 1)
- Vá na aba "Histórico".
- **O que observar**: Sua cotação recém-realizada deve aparecer na lista com data, valor e economia.

---

## 🛠️ Troubleshooting (Resolução de Problemas)
- **Erro ao salvar lista**: Verifique se você está logado e se as tabelas do Supabase foram criadas.
- **Cotação demorada**: O sistema busca em 4 lojas simultaneamente; em horários de pico dos sites dos supermercados, pode levar até 15 segundos.
- **Preços Mock**: Lembre-se que Extra, Mambo e Mercado Livre podem retornar preços simulados se o scraping direto for bloqueado pelos sites.
