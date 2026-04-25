# NEXUS COPY - Motor de Roteiros Virais

Assistente CLI em Python para geração de copy e roteiros virais para **TikTok, Reels e Shorts**.

## Estrutura de pastas

```text
nexus_copy/
├── README.md
├── __init__.py
├── main.py
└── modules/
    ├── __init__.py
    ├── authority.py
    ├── cta.py
    ├── hooks.py
    ├── mystery.py
    ├── niche_adapter.py
    ├── notable_content.py
    ├── platform_adapter.py
    └── script_builder.py
```

## Módulos implementados

1. **Gerador de Hooks**
   - 16 formatos virais
   - exemplos por formato
   - geração de variações dinâmicas
2. **Gerador de Intensificadores de Mistério**
   - 10 estruturas de retenção
   - 3 saídas por hook
3. **Gerador de Posicionamento de Autoridade**
   - frases de prova social + domínio de método
4. **Gerador de Conteúdo Notável**
   - corpo em 3 blocos práticos
5. **Gerador de CTA**
   - tipos: venda, lead, engajamento (atrair), autoridade
   - adaptação por estágio de funil
6. **Montador de Roteiro Completo**
   - junta todos os módulos em sequência final
7. **Adaptador por Plataforma**
   - TikTok: agressivo/nativo
   - Reels: clean/aspiracional
   - Shorts: direto/educativo
8. **Adaptador por Nicho**
   - emagrecimento, ganhar dinheiro, relacionamento, saúde

## Como usar

No diretório raiz do repositório:

```bash
python nexus_copy/main.py
```

O assistente fará 5 perguntas:
1. Produto/serviço/ideia
2. Objetivo do vídeo
3. Plataforma principal
4. Público-alvo (nicho + dor)
5. Ângulo/promessa

Depois ele gera:
- 3 hooks virais com overlay e cena
- 3 intensificadores por hook
- posicionamento de autoridade
- conteúdo notável
- CTA adaptado ao objetivo

## Exemplo de uso rápido

```bash
python nexus_copy/main.py
```

Exemplo de entrada:
- Produto: Mentoria para creators
- Objetivo: vender
- Plataforma: TikTok
- Público: ganhar dinheiro + baixa conversão
- Ângulo: transformar views em clientes

