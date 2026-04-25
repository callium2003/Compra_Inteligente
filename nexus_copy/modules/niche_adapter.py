# NEXUS COPY - Adaptador por Nicho
# Palavras, hooks e CTAs especificos por nicho

from typing import Dict, List


NICHE_LIBRARY = {
    "emagrecimento": {
        "keywords": ["secar", "derreter gordura", "barriga", "em X dias", "sem dieta", "celulite", "metabolismo", "gordura abdominal", "perder peso", "emagrecer rapido"],
        "hook_structures": [
            "Como perder X kg em X dias sem dieta",
            "Isso te impede de emagrecer",
            "Erro que trava sua perda de peso",
        ],
        "cta_recommended": [
            "Comenta 'SECAR' que te envio o plano",
            "Salva esse video para nao esquecer",
            "Me chama no direct se quer o metodo",
        ],
    },
    "ganhar dinheiro": {
        "keywords": ["ganhar", "vender", "todos os dias", "automatico", "sem aparecer", "faturar", "lucro", "renda extra", "liberdade financeira", "dinheiro online"],
        "hook_structures": [
            "Como fiz X dinheiro em X dias",
            "Metodo simples para ganhar sem aparecer",
            "Segredo que ninguem conta sobre",
        ],
        "cta_recommended": [
            "Comenta 'DINHEIRO' para receber o guia",
            "Clica no link da bio agora",
            "Me segue para parte 2",
        ],
    },
    "relacionamento": {
        "keywords": ["atrair", "fazer ele correr atras", "mensagem", "erro", "interesse", "seducao", "rejeicao", "inseguranca", "paquera", "conquista"],
        "hook_structures": [
            "Envie isso e veja o que acontece",
            "Nunca diga isso se quer que ele",
            "3 sinais de que ele esta interessado",
        ],
        "cta_recommended": [
            "Comenta 'AMOR' que te envio mais",
            "Salva para consultar depois",
            "Manda para uma amiga que precisa",
        ],
    },
    "saude": {
        "keywords": ["perigo", "sinais", "alerta", "isso te afeta", "doenca", "prevencao", "sintomas", "risco", "longevidade", "bem estar"],
        "hook_structures": [
            "O perigo de ignorar isso",
            "3 sinais de que algo esta errado",
            "Isso destrói sua saude sem voce perceber",
        ],
        "cta_recommended": [
            "Compartilha com quem precisa saber",
            "Comenta sua duvida que respondo",
            "Segue para mais dicas de saude",
        ],
    },
}

DEFAULT_NICHE = {
    "keywords": ["resultado", "transformacao", "metodo", "estrategia", "pratico"],
    "hook_structures": [
        "Como conseguir {resultado} sem {esforco}",
        "Isso vai mudar sua forma de ver",
        "O erro que todo mundo comete",
    ],
    "cta_recommended": [
        "Comenta para receber mais",
        "Salva esse conteudo",
        "Segue para proximas dicas",
    ],
}


class NicheAdapter:
    """Ajusta vocabulario e enfases por nicho."""

    def __init__(self):
        self.NICHE_LIBRARY = NICHE_LIBRARY
        self.DEFAULT_NICHE = DEFAULT_NICHE

    def get_niche_profile(self, nicho: str) -> Dict:
        return self.NICHE_LIBRARY.get(nicho.lower(), self.DEFAULT_NICHE)

    def adapt_keywords(self, texto: str, nicho: str) -> str:
        """Substitui palavras genericas por palavras do nicho."""
        perfil = self.get_niche_profile(nicho)
        for palavra in perfil["keywords"][:3]:
            texto = texto.replace("resultado", palavra)
        return texto

    def adapt_context(self, contexto: Dict[str, str]) -> Dict[str, str]:
        """Adapta o contexto completo com dados do nicho."""
        contexto = contexto.copy()
        perfil = self.get_niche_profile(contexto["nicho"])
        keywords = perfil["keywords"]

        contexto["niche_keywords"] = ", ".join(keywords)
        contexto["recommended_hook_structures"] = perfil["hook_structures"]
        contexto["recommended_ctas"] = perfil["cta_recommended"]

        contexto["promessa"] = contexto.get("promessa") or f"mais {keywords[0]} e {keywords[1]}"
        contexto["dor"] = contexto.get("dor") or f"falta de {keywords[2]}"
        contexto["erro"] = f"ignora {keywords[4]} no conteudo"
        contexto["beneficio"] = f"{keywords[0]} com {keywords[3]}"
        contexto["mito"] = contexto.get("mito") or f"focar so em {keywords[6]} resolve tudo"
        contexto["verdade"] = contexto.get("verdade") or f"combinar {keywords[5]} + {keywords[7]}"

        return contexto

    def generate_niche_hook(self, nicho: str, dor: str) -> str:
        perfil = self.get_niche_profile(nicho)
        estrutura = perfil["hook_structures"][0]
        palavra = perfil["keywords"][0]
        return estrutura.format(resultado=palavra, esforco="esforco", X="3", dias="7")