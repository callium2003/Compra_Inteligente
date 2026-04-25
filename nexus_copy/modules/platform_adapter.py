from __future__ import annotations


class PlatformAdapter:
    """Adapta estilo por plataforma."""

    STYLES = {
        "TikTok": "Tom agressivo/nativo, frases curtas, ritmo acelerado e cortes visuais fortes.",
        "Reels": "Tom clean/aspiracional, linguagem elegante e foco em transformação percebida.",
        "Shorts": "Tom direto/educativo, didático e objetivo com promessa clara em poucos segundos.",
    }

    def adapt(self, plataforma: str, texto: str) -> str:
        style = self.STYLES.get(plataforma, self.STYLES["Shorts"])
        return f"[{plataforma}] {style}\n{texto}"
