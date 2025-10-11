# 🧪 Guia de Teste do MVP - Compra Inteligente

## 🌐 URL do Aplicativo
**https://60h5imcl15vw.manus.space**

---

## ⚠️ IMPORTANTE: Configuração Inicial do Banco de Dados

**ANTES DE TESTAR**, você precisa executar o script SQL no Supabase:

### Passo a Passo:

1. **Acesse o Supabase Dashboard**
   - URL: https://supabase.com/dashboard
   - Faça login com suas credenciais

2. **Selecione o Projeto**
   - Nome: `wrzuwwvnyzflsohrgyin`
   - URL: https://wrzuwwvnyzflsohrgyin.supabase.co

3. **Abra o SQL Editor**
   - No menu lateral, clique em **SQL Editor**
   - Clique em **+ New query**

4. **Execute o Script**
   - Copie todo o conteúdo do arquivo `/home/ubuntu/supabase_setup.sql`
   - Cole no editor SQL
   - Clique em **Run** ou pressione `Ctrl+Enter`

5. **Verifique a Criação**
   - Vá em **Table Editor** no menu lateral
   - Você deve ver 4 tabelas:
     - `user_addresses`
     - `shopping_lists`
     - `shopping_items`
     - `quotes`

---

## 📋 Roteiro de Teste Completo

### Teste 1: Autenticação ✅

#### 1.1 Cadastro de Nova Conta
1. Acesse https://60h5imcl15vw.manus.space
2. Clique em **"Não tem conta? Cadastre-se"**
3. Preencha:
   - **Email**: `teste@compra.com`
   - **Senha**: `teste123` (mínimo 6 caracteres)
4. Clique em **"Cadastrar"**
5. ✅ **Resultado esperado**: Mensagem "Verifique seu email para confirmar o cadastro!"

#### 1.2 Confirmação de Email
1. Acesse o email cadastrado
2. Abra o email de confirmação do Supabase
3. Clique no link de confirmação
4. ✅ **Resultado esperado**: Email confirmado

#### 1.3 Login
1. Volte para https://60h5imcl15vw.manus.space
2. Se estiver na tela de cadastro, clique em **"Já tem conta? Entre"**
3. Preencha:
   - **Email**: `teste@compra.com`
   - **Senha**: `teste123`
4. Clique em **"Entrar"**
5. ✅ **Resultado esperado**: Redirecionamento para tela principal com 3 abas

---

### Teste 2: Gerenciamento de Endereços ✅

#### 2.1 Acessar Tela de Endereços
1. Após login, clique na aba **"Endereços"**
2. ✅ **Resultado esperado**: Tela vazia com botão "Novo Endereço"

#### 2.2 Cadastrar Primeiro Endereço
1. Clique em **"Novo Endereço"**
2. Preencha o formulário:
   - **Nome do Endereço**: `Casa`
   - **CEP**: `01310-100`
   - **Número**: `1000`
   - **Rua**: `Av. Paulista`
   - **Complemento**: `Apto 101` (opcional)
   - **Bairro**: `Bela Vista`
   - **Cidade**: `São Paulo`
   - **Estado**: `SP`
3. Clique em **"Salvar"**
4. ✅ **Resultado esperado**: 
   - Formulário fecha
   - Endereço aparece na lista
   - Card com borda azul e badge "Ativo"

#### 2.3 Cadastrar Segundo Endereço
1. Clique em **"Novo Endereço"** novamente
2. Preencha:
   - **Nome do Endereço**: `Trabalho`
   - **CEP**: `04543-011`
   - **Número**: `500`
   - **Rua**: `Av. Brigadeiro Faria Lima`
   - **Bairro**: `Itaim Bibi`
   - **Cidade**: `São Paulo`
   - **Estado**: `SP`
3. Clique em **"Salvar"**
4. ✅ **Resultado esperado**: Dois endereços na lista, "Casa" ainda como ativo

#### 2.4 Trocar Endereço Ativo
1. No card do endereço "Trabalho", clique no botão **✓** (check)
2. ✅ **Resultado esperado**: 
   - "Trabalho" agora tem borda azul e badge "Ativo"
   - "Casa" perde o badge "Ativo"

#### 2.5 Excluir Endereço
1. No card do endereço "Casa", clique no botão **🗑️** (lixeira)
2. Confirme a exclusão
3. ✅ **Resultado esperado**: Endereço "Casa" removido da lista

---

### Teste 3: Nova Cotação ✅

#### 3.1 Acessar Tela de Nova Cotação
1. Clique na aba **"Nova Cotação"**
2. ✅ **Resultado esperado**: 
   - Card com textarea para lista
   - Placeholder com exemplos
   - Botão "Validar & Normalizar"

#### 3.2 Digitar Lista de Compras
1. No textarea, digite a seguinte lista:

```
2 leite integral 1l
arroz tipo 1 5kg
3 ovos brancos
feijão preto 1kg
café 500g
açúcar cristal 2kg
óleo de soja 900ml
macarrão 500g
```

2. Clique em **"Validar & Normalizar"**
3. ✅ **Resultado esperado**: 
   - Tela muda para prévia
   - Tabela com 8 itens normalizados
   - Campos editáveis (quantidade, nome, tamanho, unidade, marca)

#### 3.3 Editar Item Normalizado
1. Na tabela, localize o item "leite integral"
2. Altere o campo **Marca** para `Italac`
3. ✅ **Resultado esperado**: Campo atualizado

#### 3.4 Remover Item
1. Clique no botão **✕** no último item (macarrão)
2. ✅ **Resultado esperado**: Item removido da tabela (7 itens restantes)

#### 3.5 Adicionar Título da Lista
1. No campo "Título da Lista", digite: `Compras de Outubro`
2. ✅ **Resultado esperado**: Título preenchido

#### 3.6 Fazer Cotação
1. Clique em **"Fazer Cotação"**
2. Aguarde processamento (2-3 segundos)
3. ✅ **Resultado esperado**: 
   - Tela muda para resultados
   - Card verde com economia destacada
   - Dois cards lado a lado: "Cesta Única" e "Cesta Mista"

---

### Teste 4: Resultados da Cotação ✅

#### 4.1 Verificar Cesta Única
1. Observe o card **"Cesta Única"**
2. ✅ **Resultado esperado**:
   - Nome da loja (ex: Carrefour)
   - Subtotal calculado
   - Valor do frete
   - Total = Subtotal + Frete
   - Lista de todos os itens com preços

#### 4.2 Verificar Cesta Mista
1. Observe o card **"Cesta Mista Otimizada"**
2. ✅ **Resultado esperado**:
   - Múltiplas lojas (1-2 lojas)
   - Cada loja com seus itens
   - Subtotal e frete por loja
   - Total geral menor que Cesta Única

#### 4.3 Verificar Economia
1. Observe o card verde no topo
2. ✅ **Resultado esperado**:
   - Valor em R$ da economia
   - Percentual de economia
   - Economia > 0 (cesta mista mais barata)

#### 4.4 Nova Cotação
1. Clique em **"Nova Cotação"**
2. ✅ **Resultado esperado**: Volta para tela de entrada de lista

---

### Teste 5: Histórico ✅

#### 5.1 Acessar Histórico
1. Clique na aba **"Histórico"**
2. ✅ **Resultado esperado**: 
   - Seção "Cotações Recentes" com 1 cotação
   - Seção "Listas Salvas" com 1 lista

#### 5.2 Verificar Cotação Salva
1. Observe o card da cotação
2. ✅ **Resultado esperado**:
   - Data e hora da cotação
   - Lojas consultadas
   - Valores: Cesta Única, Cesta Mista, Economia
   - Percentual de desconto

#### 5.3 Verificar Lista Salva
1. Observe o card da lista
2. ✅ **Resultado esperado**:
   - Título: "Compras de Outubro"
   - Data de criação
   - Número de itens (7 itens)
   - Primeiros 5 itens listados

---

### Teste 6: Segurança (RLS) ✅

#### 6.1 Criar Segunda Conta
1. Clique em **"Sair"** no canto superior direito
2. Cadastre nova conta:
   - **Email**: `teste2@compra.com`
   - **Senha**: `teste456`
3. Faça login com a nova conta

#### 6.2 Verificar Isolamento de Dados
1. Vá para **"Endereços"**
2. ✅ **Resultado esperado**: Lista vazia (não vê endereços da conta anterior)

3. Vá para **"Histórico"**
4. ✅ **Resultado esperado**: Sem cotações ou listas (não vê dados da conta anterior)

---

## 🐛 Problemas Conhecidos e Soluções

### Problema 1: "Erro ao salvar lista"
**Causa**: Banco de dados não configurado  
**Solução**: Execute o script SQL no Supabase (ver seção inicial)

### Problema 2: "Você precisa cadastrar um endereço"
**Causa**: Nenhum endereço cadastrado  
**Solução**: Vá para aba "Endereços" e cadastre um endereço

### Problema 3: Email de confirmação não chega
**Causa**: Configuração de email do Supabase  
**Solução**: 
- Verifique spam/lixo eletrônico
- Ou desabilite confirmação de email no Supabase:
  1. Dashboard > Authentication > Settings
  2. Desmarque "Enable email confirmations"

### Problema 4: Erro 500 ao fazer cotação
**Causa**: Backend não consegue salvar no banco  
**Solução**: Verifique se as tabelas foram criadas corretamente

---

## 📊 Métricas de Sucesso do MVP

### Funcionalidades Essenciais
- ✅ Cadastro e login funcionando
- ✅ CRUD de endereços completo
- ✅ Normalização de lista por texto
- ✅ Geração de cotação mock
- ✅ Comparação de cestas
- ✅ Cálculo de economia
- ✅ Salvamento no histórico
- ✅ RLS funcionando (isolamento de usuários)

### Performance
- ⚡ Normalização: < 1 segundo
- ⚡ Cotação: < 3 segundos
- ⚡ Carregamento de histórico: < 2 segundos

### UX
- 🎨 Design moderno e responsivo
- 🎨 Feedback visual em todas as ações
- 🎨 Navegação intuitiva por abas
- 🎨 Formulários com validação

---

## 🎯 Casos de Teste Adicionais

### Teste de Normalização Avançada

Digite esta lista para testar casos especiais:

```
leite (qualquer marca)
2kg arroz
500g café mais barato
3 ovos
óleo 900ml marca Liza
feijão 1 kilo
macarrão 500 gramas
```

✅ **Resultado esperado**:
- "qualquer marca" → notes
- "mais barato" → preference = "cheapest"
- "marca Liza" → brand = "Liza"
- "kilo" → normalizado para "kg"
- "gramas" → normalizado para "g"

### Teste de Múltiplos Endereços

Cadastre 5 endereços diferentes e verifique:
- ✅ Apenas um pode ser ativo por vez
- ✅ Ao definir novo ativo, anterior perde o status
- ✅ Pode excluir endereços não ativos
- ✅ Pode excluir endereço ativo (se houver outros)

### Teste de Lista Grande

Digite uma lista com 20+ itens e verifique:
- ✅ Normalização funciona
- ✅ Tabela tem scroll
- ✅ Cotação processa todos os itens
- ✅ Resultados exibem todos os itens

---

## 📝 Checklist Final de Validação

Antes de considerar o MVP aprovado, verifique:

- [ ] Script SQL executado no Supabase
- [ ] Cadastro de conta funciona
- [ ] Login funciona
- [ ] Logout funciona
- [ ] Cadastro de endereço funciona
- [ ] Definir endereço ativo funciona
- [ ] Excluir endereço funciona
- [ ] Entrada de lista funciona
- [ ] Normalização funciona
- [ ] Edição de itens funciona
- [ ] Salvamento de lista funciona
- [ ] Geração de cotação funciona
- [ ] Cesta única calcula corretamente
- [ ] Cesta mista calcula corretamente
- [ ] Economia é calculada
- [ ] Histórico mostra listas
- [ ] Histórico mostra cotações
- [ ] RLS isola usuários
- [ ] Design está responsivo
- [ ] Não há erros no console

---

## 🚀 Pronto para Produção!

Se todos os testes passarem, o MVP está **pronto para uso**!

**URL Final**: https://60h5imcl15vw.manus.space

---

*Última atualização: 03/10/2025*
