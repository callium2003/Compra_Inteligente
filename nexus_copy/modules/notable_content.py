from __future__ import annotations

from typing import Dict


class NotableContentGenerator:
    """Gera o corpo central com valor prático em 3 blocos."""

    def generate(self, contexto: Dict[str, str]) -> str:
        promessa = contexto.get("promessa") or "um ganho claro para o público"
        dor = contexto.get("dor", "a dor principal do nicho")
        return (
            "Bloco 1 — Diagnóstico rápido: "
            f"Mostre por que '{dor}' acontece quando não há estrutura de narrativa.\n"
            "Bloco 2 — Método prático: "
            f"Apresente um micro framework de 3 passos para entregar {promessa}.\n"
            "Bloco 3 — Aplicação imediata: "
            "Dê um exemplo real de frase, cena e sequência para o público copiar hoje."
        )
