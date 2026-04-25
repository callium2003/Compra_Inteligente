from __future__ import annotations

import random
from typing import Dict, List


class MysteryIntensifierGenerator:
    """Cria frases para aumentar retenção com base no tipo emocional do hook."""

    STRUCTURES_BY_EMOTION = {
        "medo": [
            "Se você ignorar isso, o problema tende a piorar nos próximos dias.",
            "A maioria só percebe esse erro quando já perdeu resultado.",
            "O detalhe mais perigoso aparece no próximo passo.",
            "Não cometa o mesmo erro que atrasa 90% das pessoas.",
        ],
        "curiosidade": [
            "A parte que ninguém comenta vem agora.",
            "Tem um detalhe contraintuitivo que muda tudo.",
            "Nos próximos segundos, você vai entender o motivo real.",
            "Guarda isso porque o final conecta toda a lógica.",
        ],
        "ganho": [
            "Agora vou te mostrar o passo com maior impacto imediato.",
            "Esse ponto sozinho já melhora seu resultado hoje.",
            "A próxima etapa é a mais simples e a mais lucrativa.",
            "Em 10 segundos você já consegue aplicar.",
        ],
        "urgencia": [
            "Isso precisa ser aplicado hoje para você não ficar para trás.",
            "A janela de oportunidade é curta, presta atenção agora.",
            "Se você adiar esse passo, perde tração esta semana.",
            "Vai rápido: esse ajuste define seu resultado imediato.",
        ],
    }

    def generate_for_hook(
        self,
        hook: str,
        contexto: Dict[str, str],
        quantidade: int = 3,
        tipo_emocional: str = "curiosidade",
    ) -> List[str]:
        emotion_pool = self.STRUCTURES_BY_EMOTION.get(tipo_emocional, self.STRUCTURES_BY_EMOTION["curiosidade"])
        amostras = random.sample(emotion_pool, k=min(quantidade, len(emotion_pool)))
        return [f"{frase} ({hook[:45]}... → {contexto['objetivo']})" for frase in amostras]
