from __future__ import annotations

from typing import Dict


class CTAGenerator:
    """Gera CTA por tipo e estágio de funil."""

    CTA_MAP = {
        "vender": {
            "topo": "Quer acelerar seu resultado? Comenta 'NEXUS' que eu te envio o próximo passo.",
            "meio": "Se isso fez sentido, me chama no direct para ver como aplico no seu caso.",
            "fundo": "Clique no link e entre agora no NEXUS COPY para implementar hoje.",
        },
        "lead": {
            "topo": "Comenta 'GUIA' e eu libero um checklist de roteiro viral.",
            "meio": "Baixe o material gratuito no link do perfil e aplique no próximo vídeo.",
            "fundo": "Preencha o formulário e receba o plano personalizado no seu nicho.",
        },
        "atrair": {
            "topo": "Segue o perfil para receber scripts curtos todos os dias.",
            "meio": "Salva este vídeo para usar como modelo na próxima gravação.",
            "fundo": "Se quiser acompanhamento, entre para a comunidade fechada do perfil.",
        },
        "autoridade": {
            "topo": "Se isso te ajudou, compartilha com alguém que grava conteúdo.",
            "meio": "Comenta seu nicho que eu respondo com um hook personalizado.",
            "fundo": "Assista os destaques e veja os estudos de caso completos.",
        },
    }

    FUNIL_HINT = {
        "TikTok": "topo",
        "Reels": "meio",
        "Shorts": "topo",
    }

    def generate(self, contexto: Dict[str, str]) -> str:
        objetivo = contexto["objetivo"].lower()
        plataforma = contexto["plataforma"]
        funil = self.FUNIL_HINT.get(plataforma, "meio")
        return self.CTA_MAP.get(objetivo, self.CTA_MAP["atrair"])[funil]
