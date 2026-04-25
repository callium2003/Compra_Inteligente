from __future__ import annotations

from typing import Dict, List

from .authority import AuthorityPositioningGenerator
from .cta import CTAGenerator
from .hooks import HookGenerator
from .mystery import MysteryIntensifierGenerator
from .notable_content import NotableContentGenerator
from .platform_adapter import PlatformAdapter


class CompleteScriptBuilder:
    """Orquestra todos os módulos para gerar roteiro final."""

    def __init__(self) -> None:
        self.hooks = HookGenerator()
        self.mystery = MysteryIntensifierGenerator()
        self.authority = AuthorityPositioningGenerator()
        self.content = NotableContentGenerator()
        self.cta = CTAGenerator()
        self.platform = PlatformAdapter()

    def build(self, contexto: Dict[str, str]) -> Dict[str, object]:
        hooks = self.hooks.generate_variations(contexto, quantidade=3)
        intensificadores: List[Dict[str, object]] = []
        for item in hooks:
            intensificadores.append(
                {
                    "hook": item["hook"],
                    "tipo_emocional": item["tipo_emocional"],
                    "frases": self.mystery.generate_for_hook(
                        item["hook"],
                        contexto,
                        quantidade=3,
                        tipo_emocional=item["tipo_emocional"],
                    ),
                }
            )

        autoridade = self.authority.generate(contexto)
        conteudo = self.content.generate(contexto)
        cta = self.cta.generate(contexto)

        return {
            "hooks": hooks,
            "intensificadores": intensificadores,
            "autoridade": self.platform.adapt(contexto["plataforma"], autoridade),
            "conteudo_notavel": self.platform.adapt(contexto["plataforma"], conteudo),
            "cta": self.platform.adapt(contexto["plataforma"], cta),
            "niche_keywords": contexto.get("niche_keywords", ""),
            "recommended_hook_structures": contexto.get("recommended_hook_structures", []),
            "recommended_ctas": contexto.get("recommended_ctas", []),
        }

    def to_markdown(self, resultado: Dict[str, object]) -> str:
        lines = [
            "# 🚀 NEXUS COPY — Roteiro Viral Completo",
            "",
            "## 🎣 1) Hooks virais (com overlay, cena e exemplo prático)",
        ]

        for idx, hook in enumerate(resultado["hooks"], start=1):
            lines.extend(
                [
                    f"### Hook {idx} — {hook['formato']} ({hook['tipo_emocional']})",
                    f"- **Hook:** {hook['hook']}",
                    f"- **Overlay:** {hook['overlay']}",
                    f"- **Cena:** {hook['cena']}",
                    f"- **Exemplo base:** {hook['exemplo_formato']}",
                    f"- **Exemplo prático real:** {hook['exemplo_pratico_real']}",
                    "",
                ]
            )

        lines.append("## 🧠 2) Intensificadores de mistério (3 por hook)")
        for bloco in resultado["intensificadores"]:
            lines.append(f"### Para: _{bloco['hook']}_")
            for frase in bloco["frases"]:
                lines.append(f"- {frase}")
            lines.append("")

        lines.extend(
            [
                "## 🏅 3) Posicionamento de autoridade",
                f"- {resultado['autoridade']}",
                "",
                "## 💡 4) Conteúdo notável",
                f"- {resultado['conteudo_notavel']}",
                "",
                "## 📣 5) CTA adaptado ao objetivo",
                f"- {resultado['cta']}",
                "",
                "## 🧬 6) Ajuste por nicho",
                f"- **Palavras-chave do nicho:** {resultado.get('niche_keywords', 'N/A')}",
                "- **Estruturas de hook recomendadas:**",
            ]
        )

        for estrutura in resultado.get("recommended_hook_structures", []):
            lines.append(f"  - {estrutura}")

        lines.append("- **CTAs recomendados para o nicho:**")
        for cta in resultado.get("recommended_ctas", []):
            lines.append(f"  - {cta}")

        return "\n".join(lines)
