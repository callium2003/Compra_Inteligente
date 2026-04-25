# NEXUS COPY - Montador de Roteiro Completo
# Junta hook + intensificador + posicionamento + conteudo + CTA

from typing import Dict, List, Any
from .hooks import HookGenerator
from .mystery import MysteryIntensifier
from .authority import AuthorityGenerator
from .notable_content import NotableContentGenerator
from .cta import CTAGenerator
from .niche_adapter import NicheAdapter
from .platform_adapter import PlatformAdapter


class CompleteScriptBuilder:
    """Montador de roteiro viral completo em blocos modulares."""

    def __init__(self):
        self.hooks = HookGenerator()
        self.mystery = MysteryIntensifier()
        self.authority = AuthorityGenerator()
        self.notable = NotableContentGenerator()
        self.cta = CTAGenerator()
        self.niche = NicheAdapter()
        self.platform = PlatformAdapter()

    def build(self, contexto: Dict[str, str]) -> Dict[str, Any]:
        """Gera roteiro completo a partir do contexto."""
        hooks_data = self.hooks.generate_variations(contexto=contexto, n=3)
        intensificadores = []
        for item in hooks_data:
            tipo_emocional = item.get("tipo_emocional", "curiosidade")
            frases = self.mystery.generate(hook=item["hook"], tipo_emocional=tipo_emocional, quantidade=3)
            intensificadores.append({"hook": item["hook"], "frases": frases})

        return {
            "hooks": hooks_data,
            "intensificadores": intensificadores,
            "autoridade": self.authority.generate(contexto),
            "conteudo_notavel": self.notable.generate(contexto),
            "cta": self.cta.generate(
                contexto.get("objetivo", "engajamento"),
                contexto.get("funil", "topo"),
                contexto.get("produto", "")
            ),
            "rota": {
                "bloco1": f"HOOK (0-3s): {hooks_data[0]['hook']}",
                "bloco2": f"INTENSIFICADOR (3-6s): {intensificadores[0]['frases'][0]}",
                "bloco3": f"POSICIONAMENTO (6-10s): {self.authority.generate(contexto)}",
                "bloco4": f"CONTEUDO (10-25s): {self.notable.generate(contexto)[0]}",
                "bloco5": f"CTA (final): {self.cta.generate(contexto.get('objetivo', 'engajamento'), contexto.get('funil', 'topo'))}",
            }
        }

    def to_markdown(self, resultado: Dict[str, Any]) -> str:
        """Formata a saida como markdown com emojis e secoes claras."""
        linhas = []
        linhas.append("\n" + "="*50)
        linhas.append("  NEXUS COPY - Roteiro Viral")
        linhas.append("="*50 + "\n")

        linhas.append("## 1) Hooks Virais (3 opcoes com overlay e cena)\n")
        for idx, hook in enumerate(resultado["hooks"], start=1):
            linhas.append(f"### Hook {idx} - {hook['formato']}")
            linhas.append(f"**Fala:** {hook['hook']}")
            linhas.append(f"**Overlay:** {hook['overlay']}")
            linhas.append(f"**Cena:** {hook['cena']}\n")

        linhas.append("## 2) Intensificadores de Misterio (3 por hook)\n")
        for bloco in resultado["intensificadores"]:
            linhas.append(f"Para hook: **{bloco['hook']}**")
            for frase in bloco["frases"]:
                linhas.append(f"- {frase}")
            linhas.append("")

        linhas.append("## 3) Posicionamento de Autoridade\n")
        linhas.append(f"- {resultado['autoridade']}\n")

        linhas.append("## 4) Conteudo Notavel\n")
        for bloco in resultado["conteudo_notavel"]:
            linhas.append(f"- {bloco}")
        linhas.append("")

        linhas.append("## 5) CTA Adaptado\n")
        linhas.append(f"- {resultado['cta']}\n")

        linhas.append("## 6) Rota do Video\n")
        for bloco, descricao in resultado["rota"].items():
            linhas.append(f"- {bloco}: {descricao}")

        return "\n".join(linhas)