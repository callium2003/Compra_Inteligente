# NEXUS COPY - Gerador de Intensificadores de Misterio
# Selecao por tipo emocional: medo, curiosidade, ganho, urgencia

import random
from typing import Dict, List


STRUCTURES_BY_EMOTION = {
    "curiosidade": [
        "Mas tem um detalhe que ninguem percebe...",
        "E isso e o que ninguem te conta sobre...",
        "Mas o que acontece depois e o mais interessante...",
        "Existe um padrao por tras disso que pouca gente percebe...",
        "A parte mais importante vem agora...",
    ],
    "medo": [
        "Se voce fizer isso do jeito errado, pode dar o efeito contrario...",
        "E eu quase cometi um erro que ia estragar tudo...",
        "O perigo e que ninguem fala sobre isso...",
        "Se voce ignorar isso, pode perder tudo...",
        "A maioria das pessoas faz exatamente o oposto...",
    ],
    "ganho": [
        "So comecou a funcionar depois que eu...",
        "E foi aqui que tudo virou pra mim...",
        "E quase ninguem faz isso - e por isso que funciona...",
        "O segredo que mudou tudo foi...",
        "Depois que descobri isso, nunca mais...",
    ],
    "urgencia": [
        "Mas isso aqui so funciona agora...",
        "E se voce nao agir hoje, pode perder a chance...",
        "A janela de oportunidade esta fechando...",
        "So tenho tempo de mostrar isso hoje...",
        "Isso aqui vai sair do ar em breve...",
    ],
}


def generate_for_hook(
    hook: str,
    contexto: Dict[str, str],
    quantidade: int = 3,
    tipo_emocional: str = "curiosidade",
) -> List[str]:
    """Gera intensificadores selecionando pelo tipo emocional do hook."""
    emotion_pool = STRUCTURES_BY_EMOTION.get(tipo_emocional, STRUCTURES_BY_EMOTION["curiosidade"])
    amostras = random.sample(emotion_pool, k=min(quantidade, len(emotion_pool)))
    return [f"({frase}) ({contexto.get('objetivo', '')})" for frase in amostras]


class MysteryIntensifier:
    """Gerador de intensificadores de misterio por emocao."""

    def __init__(self):
        self.STRUCTURES_BY_EMOTION = STRUCTURES_BY_EMOTION

    def generate(self, hook: str, tipo_emocional: str = "curiosidade", quantidade: int = 3) -> List[str]:
        return generate_for_hook(hook, {}, quantidade, tipo_emocional)

    def generate_by_context(self, contexto: Dict[str, str]) -> List[str]:
        """Gera baseado no contexto completo do briefing."""
        tipo = contexto.get("tipo_emocional", "curiosidade")
        hook = contexto.get("hook", "")
        return generate_for_hook(hook, contexto, 3, tipo)