from __future__ import annotations

from typing import Dict


class CTAGenerator:
    """Gera CTA por objetivo x etapa de funil (matriz completa 4x3)."""

    CTA_MATRIX = {
        "vender": {
            "topo": "Se quer acelerar seu resultado, comenta 'NEXUS' que eu te envio o passo inicial.",
            "meio": "Se isso fez sentido, me chama no direct para eu te mostrar a aplicação no seu caso.",
            "fundo": "Clique no link e entre agora no NEXUS COPY para implementar hoje mesmo.",
        },
        "lead": {
            "topo": "Comenta 'GUIA' para receber o checklist gratuito de roteiro viral.",
            "meio": "Baixe o material no link do perfil e aplique no próximo vídeo.",
            "fundo": "Preencha o formulário e receba um plano personalizado no seu nicho.",
        },
        "engajamento": {
            "topo": "Curtiu? Segue o perfil para receber novos scripts curtos todos os dias.",
            "meio": "Salva este vídeo e marca alguém que precisa aplicar isso hoje.",
            "fundo": "Comenta sua maior dificuldade que eu te respondo com um roteiro pronto.",
        },
        "autoridade": {
            "topo": "Compartilha esse vídeo para fortalecer sua referência no tema.",
            "meio": "Comenta seu nicho e eu te devolvo um hook estratégico personalizado.",
            "fundo": "Veja os estudos de caso nos destaques e valide o método completo.",
        },
    }

    FUNIL_HINT = {
        "TikTok": "topo",
        "Reels": "meio",
        "Shorts": "topo",
    }

    GOAL_ALIASES = {
        "atrair": "engajamento",
    }

    def normalize_goal(self, objetivo: str) -> str:
        objetivo = objetivo.lower().strip()
        objetivo = self.GOAL_ALIASES.get(objetivo, objetivo)
        return objetivo if objetivo in self.CTA_MATRIX else "engajamento"

    def generate(self, contexto: Dict[str, str]) -> str:
        objetivo = self.normalize_goal(contexto.get("objetivo", "engajamento"))
        funil = self.FUNIL_HINT.get(contexto.get("plataforma", "Reels"), "meio")
        return self.CTA_MATRIX[objetivo][funil]
