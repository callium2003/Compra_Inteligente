from __future__ import annotations

from typing import Dict


class AuthorityPositioningGenerator:
    """Gera posicionamento de autoridade e prova social."""

    def generate(self, contexto: Dict[str, str]) -> str:
        publico = contexto["publico"]
        produto = contexto["produto"]
        return (
            f"Eu venho testando scripts para {publico} com foco em {produto}. "
            "Esse método combina padrões de retenção, gatilhos de narrativa "
            "e estrutura de conversão usada por criadores de alta performance."
        )
