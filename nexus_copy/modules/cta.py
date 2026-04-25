# NEXUS COPY - Gerador de CTA
# Matriz completa: 4 objetivos x 3 estagios de funil = 12 CTAs

CTA_MAP = {
    "vender": {
        "topo": "Quer acelerar seu resultado? Comenta 'NEXUS' que eu te envio o proximo passo.",
        "meio": "Se isso fez sentido, me chama no direct para ver como aplica no seu caso.",
        "fundo": "Clique no link e entre agora no NEXUS COPY para implementar hoje mesmo.",
    },
    "lead": {
        "topo": "Comenta 'GUIA' para receber o checklist gratuito de roteiro viral.",
        "meio": "Baixe o material no link do perfil e aplique no proximo video.",
        "fundo": "Preencha o formulario e receba um plano personalizado no seu nicho.",
    },
    "engajamento": {
        "topo": "Curtiu? Segue o perfil para receber novos scripts curtos todos os dias.",
        "meio": "Salva este video e marca alguem que precisa aplicar isso hoje.",
        "fundo": "Comenta sua maior dificuldade que eu te respondo com um roteiro pratico.",
    },
    "autoridade": {
        "topo": "Compartilha esse video para fortalecer sua referencia no tema.",
        "meio": "Comenta seu nicho e eu te devolvo um hook estrategico personalizado.",
        "fundo": "Veja os estudos de caso nos destaques e valide o metodo completo.",
    },
}


def gerar_cta(objetivo: str, funil: str) -> str:
    """Gera CTA por tipo e estagio de funil."""
    return CTA_MAP.get(objetivo, CTA_MAP["engajamento"]).get(funil, CTA_MAP["engajamento"]["topo"])


class CTAGenerator:
    """Gerador de CTA com matriz completa."""

    @staticmethod
    def get_all() -> dict:
        return CTA_MAP

    @staticmethod
    def generate(objetivo: str, funil: str, produto: str = "") -> str:
        base = gerar_cta(objetivo, funil)
        if produto:
            return f"{base} Nao perca tempo - comece agora no {produto}."
        return base

    @staticmethod
    def generate_matriz() -> list:
        """Retorna todos os 12 CTAs da matriz."""
        matriz = []
        for obj in CTA_MAP:
            for fun in ["topo", "meio", "fundo"]:
                matriz.append({
                    "objetivo": obj,
                    "funil": fun,
                    "cta": CTA_MAP[obj][fun],
                })
        return matriz