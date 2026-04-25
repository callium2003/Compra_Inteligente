from __future__ import annotations

import random
from typing import Dict, List


class MysteryIntensifierGenerator:
    """Cria frases para aumentar retenção logo após o hook."""

    STRUCTURES = [
        "E o detalhe que muda tudo vem agora.",
        "O maior erro aparece no próximo passo.",
        "Se você pular essa parte, perde o resultado.",
        "Foi aqui que eu quase desisti, até perceber isso.",
        "Nos próximos 10 segundos, você vai entender o motivo real.",
        "Quase ninguém aplica esse ponto, e é ele que converte.",
        "A parte mais contraintuitiva é justamente a que funciona.",
        "Guarda isso porque o final conecta tudo.",
        "Agora vem a peça que destrava {objetivo}.",
        "Não parece importante, mas isso define o sucesso do vídeo.",
    ]

    def generate_for_hook(self, hook: str, contexto: Dict[str, str], quantidade: int = 3) -> List[str]:
        amostras = random.sample(self.STRUCTURES, k=min(quantidade, len(self.STRUCTURES)))
        return [f"{frase.format(objetivo=contexto['objetivo'])} ({hook[:45]}...)" for frase in amostras]
