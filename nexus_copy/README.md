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
   - exemplos base + exemplos práticos reais em cada formato
   - classificação por tipo emocional (medo, curiosidade, ganho, urgência)
2. **Gerador de Intensificadores de Mistério**
   - seleção baseada no tipo emocional do hook
   - 3 intensificadores por hook
3. **Gerador de Posicionamento de Autoridade**
4. **Gerador de Conteúdo Notável**
5. **Gerador de CTA**
   - matriz completa por objetivo x funil (12 CTAs no mínimo)
6. **Montador de Roteiro Completo**
   - saída estruturada e também formatada em Markdown com emojis
7. **Adaptador por Plataforma**
   - TikTok: agressivo/nativo
   - Reels: clean/aspiracional
   - Shorts: direto/educativo
8. **Adaptador por Nicho**
   - emagrecimento, ganhar dinheiro, relacionamento, saúde
   - cada nicho com 10+ palavras-chave, 3 estruturas de hook e 3 CTAs recomendados

## Como usar

No diretório raiz do repositório:

```bash
python nexus_copy/main.py
```

O assistente faz 5 perguntas do briefing e, se algo não for respondido, aplica valores padrão inteligentes.

Saída gerada:
- 3 hooks virais com overlay e cena
- 3 intensificadores por hook
- posicionamento de autoridade
- conteúdo notável
- CTA adaptado ao objetivo/funil
- recomendações por nicho

