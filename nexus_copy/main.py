from __future__ import annotations

from typing import Dict

from modules.niche_adapter import NicheAdapter
from modules.script_builder import CompleteScriptBuilder


DEFAULTS = {
    "produto": "mentoria de criação de conteúdo",
    "objetivo": "engajamento",
    "plataforma": "TikTok",
    "publico": "ganhar dinheiro + baixa conversão",
    "promessa": "transformar views em clientes",
}

VALID_OBJECTIVES = {"vender", "lead", "engajamento", "autoridade", "atrair"}
VALID_PLATFORMS = {"TikTok", "Reels", "Shorts"}


def sanitize_answer(value: str, default: str) -> str:
    clean_value = value.strip()
    return clean_value if clean_value else default


def coletar_briefing() -> Dict[str, str]:
    print("=== NEXUS COPY - Motor de Roteiros Virais ===")

    produto = sanitize_answer(input("1) Qual é o produto/serviço/ideia? "), DEFAULTS["produto"])

    objetivo_raw = sanitize_answer(
        input("2) Objetivo do vídeo? (vender, lead, engajamento, autoridade) "),
        DEFAULTS["objetivo"],
    ).lower()
    objetivo = objetivo_raw if objetivo_raw in VALID_OBJECTIVES else DEFAULTS["objetivo"]

    plataforma_raw = sanitize_answer(
        input("3) Plataforma principal? (TikTok, Reels, Shorts) "),
        DEFAULTS["plataforma"],
    )
    plataforma = plataforma_raw if plataforma_raw in VALID_PLATFORMS else DEFAULTS["plataforma"]

    publico = sanitize_answer(input("4) Público-alvo? (nicho + dor principal) "), DEFAULTS["publico"])
    promessa = sanitize_answer(
        input("5) Tem algum ângulo ou promessa já definida? "),
        DEFAULTS["promessa"],
    )

    if "+" in publico:
        nicho, dor = [p.strip() for p in publico.split("+", maxsplit=1)]
    else:
        nicho = publico.split()[0] if publico.split() else "ganhar dinheiro"
        dor = ""

    return {
        "produto": produto,
        "objetivo": objetivo,
        "plataforma": plataforma,
        "publico": publico,
        "nicho": nicho,
        "dor": dor,
        "promessa": promessa,
    }


def main() -> None:
    briefing = coletar_briefing()
    briefing_adaptado = NicheAdapter().adapt_context(briefing)
    builder = CompleteScriptBuilder()
    resultado = builder.build(briefing_adaptado)
    print(builder.to_markdown(resultado))


if __name__ == "__main__":
    main()
