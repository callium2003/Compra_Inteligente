# NEXUS COPY - Motor de Roteiros Virais
# Assistente CLI para criativos de TikTok, Reels e Shorts

from modules.hooks import HookGenerator
from modules.mystery import MysteryIntensifier
from modules.authority import AuthorityGenerator
from modules.notable_content import NotableContentGenerator
from modules.cta import CTAGenerator
from modules.niche_adapter import NicheAdapter
from modules.script_builder import CompleteScriptBuilder

DEFAULTS = {
    "produto": "Mentoria para criadores de conteudo",
    "objetivo": "vender",
    "plataforma": "TikTok",
    "nicho": "ganhar dinheiro",
    "dor": "baixa conversao",
    "promessa": "views -> clientes",
}

VALID_OBJECTIVES = ["vender", "atrair", "lead", "autoridade"]
VALID_PLATFORMS = ["TikTok", "Reels", "Shorts"]


def sanitize_answer(answer: str) -> str:
    return answer.strip() if answer.strip() else ""


def coletar_briefing() -> dict:
    print("\n=== NEXUS COPY - Motor de Roteiros Virais ===")
    produto = sanitize_answer(input("(1) Qual e o produto/servico/ideia? ")) or DEFAULTS["produto"]
    objetivo = sanitize_answer(input("(2) Objetivo do video? (vender, atrair, lead, autoridade) ")) or DEFAULTS["objetivo"]
    if objetivo not in VALID_OBJECTIVES:
        objetivo = DEFAULTS["objetivo"]
    plataforma = sanitize_answer(input("(3) Plataforma principal? (TikTok, Reels, Shorts) ")) or DEFAULTS["plataforma"]
    if plataforma not in VALID_PLATFORMS:
        plataforma = DEFAULTS["plataforma"]
    publico = sanitize_answer(input("(4) Publico-alvo? (nicho + dor principal) ")) or DEFAULTS["nicho"]
    promessa = sanitize_answer(input("(5) Tem algum angulo ou promessa ja definida? ")) or DEFAULTS["promessa"]

    if "+" in publico:
        nicho, dor = [p.strip() for p in publico.split("+", maxsplit=1)]
    else:
        nicho = publico.split()[0] if publico.split() else DEFAULTS["nicho"]
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


def formatar_saida(resultado: dict) -> str:
    linhas = ["\n=== SAIDA COMPLETA NEXUS COPY ==="]
    linhas.append("\n1) Hooks virais (3 opcoes com overlay e cena):")
    for idx, hook in enumerate(resultado["hooks"], start=1):
        linhas.append(f"\nHook {idx} [{hook['formato']}]: {hook['hook']}")
        linhas.append(f"  - {hook['overlay']}")
        linhas.append(f"  - Cena: {hook['cena']}")

    linhas.append("\n2) Intensificadores de misterio (3 por hook):")
    for bloco in resultado["intensificadores"]:
        linhas.append(f"\nPara hook: {bloco['hook']}")
        for frase in bloco["frases"]:
            linhas.append(f"  - {frase}")

    linhas.append("\n3) Posicionamento de autoridade:")
    linhas.append(f"  - {resultado['autoridade']}")

    linhas.append("\n4) Conteudo notavel:")
    for bloco in resultado["conteudo_notavel"]:
        linhas.append(f"  - {bloco}")

    linhas.append("\n5) CTA adaptado ao objetivo:")
    linhas.append(f"  - {resultado['cta']}")

    return "\n".join(linhas)


def main() -> None:
    briefing = coletar_briefing()
    briefing_adaptado = NicheAdapter().adapt_context(briefing)
    resultado = CompleteScriptBuilder().build(briefing_adaptado)
    print(formatar_saida(resultado))


if __name__ == "__main__":
    main()