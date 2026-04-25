from __future__ import annotations

from typing import Dict, List


class NicheAdapter:
    """Ajusta vocabulário e recomendações por nicho."""

    NICHE_LIBRARY: Dict[str, Dict[str, List[str]]] = {
        "emagrecimento": {
            "keywords": [
                "déficit calórico",
                "saciedade",
                "termogênico natural",
                "metabolismo",
                "reeducação alimentar",
                "retenção de líquido",
                "treino de força",
                "constância",
                "sono regulado",
                "progresso semanal",
                "foco",
                "composição corporal",
            ],
            "hook_structures": [
                "Se você quer emagrecer sem sofrer, pare de {erro}.",
                "O erro que trava seu metabolismo em 7 dias é {erro}.",
                "Em {tempo}, você pode ver diferença no espelho com este passo.",
            ],
            "cta_recommended": [
                "Comenta 'SECAR' para receber o protocolo inicial.",
                "Salva este vídeo para montar sua rotina da semana.",
                "Clique no link e entre no plano guiado hoje.",
            ],
        },
        "ganhar dinheiro": {
            "keywords": [
                "oferta",
                "ticket médio",
                "escala",
                "margem",
                "conversão",
                "funil",
                "copy de vendas",
                "aquisição",
                "ROI",
                "recorrência",
                "caixa",
                "autoridade digital",
            ],
            "hook_structures": [
                "Se você ainda {erro}, está deixando dinheiro na mesa.",
                "A estratégia que me fez aumentar {resultado} sem anúncio caro.",
                "3 ajustes de funil para vender mais em {tempo}.",
            ],
            "cta_recommended": [
                "Comenta 'LUCRO' para receber o modelo de oferta.",
                "Me chama no direct para revisar seu funil em 2 minutos.",
                "Entre no programa e implemente a estratégia ainda hoje.",
            ],
        },
        "relacionamento": {
            "keywords": [
                "conexão emocional",
                "comunicação assertiva",
                "limites",
                "confiança",
                "linguagem do amor",
                "vulnerabilidade",
                "respeito mútuo",
                "escuta ativa",
                "intimidade",
                "autoconhecimento",
                "alinhamento de valores",
                "segurança afetiva",
            ],
            "hook_structures": [
                "Se você sente {dor}, este ajuste muda tudo.",
                "O comportamento silencioso que destrói relacionamentos é {erro}.",
                "Em {tempo}, você pode melhorar a conexão com este método.",
            ],
            "cta_recommended": [
                "Comenta 'CONEXÃO' para receber o roteiro de conversa.",
                "Compartilha com quem precisa ouvir isso hoje.",
                "Entre no treinamento para aplicar com acompanhamento.",
            ],
        },
        "saude": {
            "keywords": [
                "prevenção",
                "bem-estar",
                "rotina saudável",
                "check-up",
                "inflamação",
                "energia",
                "imunidade",
                "hábito diário",
                "hidratação",
                "qualidade do sono",
                "longevidade",
                "equilíbrio hormonal",
            ],
            "hook_structures": [
                "Se você quer mais energia, pare de {erro} agora.",
                "O hábito simples que melhora sua saúde em {tempo}.",
                "Ninguém te contou isso sobre prevenção e rotina.",
            ],
            "cta_recommended": [
                "Comenta 'SAÚDE' para receber o checklist diário.",
                "Salva para revisar na sua próxima rotina.",
                "Clique no link para acessar o protocolo completo.",
            ],
        },
    }

    DEFAULT_NICHE = {
        "keywords": ["clareza", "resultado", "consistência", "crescimento", "estratégia", "narrativa", "valor", "retenção", "conversão", "autoridade"],
        "hook_structures": [
            "Se você ainda {erro}, está travando {resultado}.",
            "Em {tempo}, você pode melhorar seu resultado com este ajuste.",
            "Ninguém fala isso sobre {tema}.",
        ],
        "cta_recommended": [
            "Comenta 'NEXUS' para receber o próximo passo.",
            "Salva este vídeo para aplicar depois.",
            "Acesse o link para ver o método completo.",
        ],
    }

    def get_niche_profile(self, nicho: str) -> Dict[str, List[str]]:
        return self.NICHE_LIBRARY.get(nicho.lower(), self.DEFAULT_NICHE)

    def adapt_context(self, contexto: Dict[str, str]) -> Dict[str, str]:
        contexto = contexto.copy()
        profile = self.get_niche_profile(contexto["nicho"])
        keywords = profile["keywords"]

        contexto["niche_keywords"] = ", ".join(keywords)
        contexto["recommended_hook_structures"] = profile["hook_structures"]
        contexto["recommended_ctas"] = profile["cta_recommended"]

        contexto["promessa"] = contexto.get("promessa") or f"mais {keywords[0]} e {keywords[1]}"
        contexto["dor"] = contexto.get("dor") or f"falta de {keywords[2]}"
        contexto["erro"] = f"ignora {keywords[4]} no conteúdo"
        contexto["beneficio"] = f"{keywords[0]} com {keywords[3]}"
        contexto["mito"] = contexto.get("mito") or f"focar só em {keywords[6]} resolve tudo"
        contexto["verdade"] = contexto.get("verdade") or f"combinar {keywords[5]} + {keywords[7]} aumenta {keywords[8]}"

        return contexto
