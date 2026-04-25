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
                    "frases": self.mystery.generate_for_hook(item["hook"], contexto, quantidade=3),
                }
            )

        autoridade = self.authority.generate(contexto)
        conteudo = self.content.generate(contexto)
        cta = self.cta.generate(contexto)

        roteiro = {
            "hooks": hooks,
            "intensificadores": intensificadores,
            "autoridade": self.platform.adapt(contexto["plataforma"], autoridade),
            "conteudo_notavel": self.platform.adapt(contexto["plataforma"], conteudo),
            "cta": self.platform.adapt(contexto["plataforma"], cta),
        }
        return roteiro
