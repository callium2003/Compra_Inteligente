from __future__ import annotations

from textwrap import indent
from typing import Dict

from modules.niche_adapter import NicheAdapter
from modules.script_builder import CompleteScriptBuilder


def coletar_briefing() -> Dict[str, str]:
    print("=== NEXUS COPY - Motor de Roteiros Virais ===")
    produto = input("1) Qual é o produto/serviço/ideia? ").strip()
    objetivo = input("2) Objetivo do vídeo? (vender, atrair, lead, autoridade) ").strip().lower()
    plataforma = input("3) Plataforma principal? (TikTok, Reels, Shorts) ").strip()
    publico = input("4) Público-alvo? (nicho + dor principal) ").strip()
    angulo = input("5) Tem algum ângulo ou promessa já definida? ").strip()

    nicho = publico.split("+")[0].strip() if "+" in publico else publico.split()[0]
    dor = publico.split("+")[1].strip() if "+" in publico else ""

    return {
        "produto": produto,
        "objetivo": objetivo,
        "plataforma": plataforma,
        "publico": publico,
        "nicho": nicho,
        "dor": dor,
        "promessa": angulo,
    }


def formatar_saida(resultado: Dict[str, object]) -> str:
    linhas = ["\n=== SAÍDA COMPLETA NEXUS COPY ==="]
    linhas.append("\n1) Hooks virais (3 opções com overlay e cena):")
    for idx, hook in enumerate(resultado["hooks"], start=1):
        linhas.append(f"\nHook {idx} [{hook['formato']}]: {hook['hook']}")
        linhas.append(f"- {hook['overlay']}")
        linhas.append(f"- {hook['cena']}")

    linhas.append("\n2) Intensificadores de mistério (3 por hook):")
    for bloco in resultado["intensificadores"]:
        linhas.append(f"\nPara hook: {bloco['hook']}")
        for frase in bloco["frases"]:
            linhas.append(f"- {frase}")

    linhas.append("\n3) Posicionamento de autoridade:")
    linhas.append(indent(resultado["autoridade"], prefix="- "))

    linhas.append("\n4) Conteúdo notável:")
    linhas.append(indent(resultado["conteudo_notavel"], prefix="- "))

    linhas.append("\n5) CTA adaptado ao objetivo:")
    linhas.append(indent(resultado["cta"], prefix="- "))

    return "\n".join(linhas)


def main() -> None:
    briefing = coletar_briefing()
    briefing_adaptado = NicheAdapter().adapt_context(briefing)
    resultado = CompleteScriptBuilder().build(briefing_adaptado)
    print(formatar_saida(resultado))


if __name__ == "__main__":
    main()
