from __future__ import annotations

from typing import Dict


class NicheAdapter:
    """Ajusta vocabulário e ênfases por nicho."""

    NICHE_WORDS = {
        "emagrecimento": ["metabolismo", "consistência", "hábitos"],
        "ganhar dinheiro": ["escala", "oferta", "conversão"],
        "relacionamento": ["conexão", "comunicação", "confiança"],
        "saude": ["prevenção", "bem-estar", "rotina"],
    }

    def adapt_context(self, contexto: Dict[str, str]) -> Dict[str, str]:
        contexto = contexto.copy()
        nicho = contexto["nicho"].lower()
        palavras = self.NICHE_WORDS.get(nicho, ["clareza", "resultado", "consistência"])
        contexto["promessa"] = contexto.get("promessa") or f"mais {palavras[0]} e {palavras[1]}"
        contexto["dor"] = contexto.get("dor") or f"falta de {palavras[2]}"
        contexto["erro"] = f"ignora {palavras[1]} no conteúdo"
        contexto["beneficio"] = f"{palavras[0]} e crescimento"
        return contexto
