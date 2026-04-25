# NEXUS COPY - Gerador de Hooks Virais
# 16 formatos com exemplos praticos reais e tipo emocional

from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class HookFormat:
    nome: str
    template: str
    exemplo: str
    tipo_emocional: str
    exemplo_pratico_real: str


FORMATOS: List[HookFormat] = [
    HookFormat("Como Eu", "Como eu {resultado} sem {objecao}", "Como eu fiz minha primeira venda em 24h", "curiosidade", "Como eu fiz R$200 por dia sem aparecer usando so o celular"),
    HookFormat("Como Fazer X Sem Y", "Como {resultado} sem {esforco}", "Como vender sem gastar com trafego", "ganho", "Como vender todos os dias sem gastar 1 real com ads"),
    HookFormat("Velocidade", "Como conseguir {resultado} em {tempo}", "Como conseguir clientes em 7 dias", "urgencia", "Como fazer 10 vendas em 3 dias sem aparecer"),
    HookFormat("Uma Coisa So", "{coisa} me trouxe {resultado}", "Esse habito me fez faturar todos os dias", "curiosidade", "Esse unico erro me custou R$5000 mas me ensinou a vender"),
    HookFormat("Comando Direto", "Faca isso e {resultado}", "Faca isso e aumente suas vendas hoje", "ganho", "Faca isso e dobre seus seguidores em 7 dias"),
    HookFormat("Lista Magnetica", "{numero} coisas que {acao}", "3 erros que te impedem de vender", "medo", "3 coisas que estao destruindo seu engajamento sem voce perceber"),
    HookFormat("Quebra de Crenca", "A verdade sobre {topico}", "A verdade sobre ganhar dinheiro online", "curiosidade", "A verdade sobre reels virais que ninguem te conta"),
    HookFormat("Medo Oculto", "O perigo de {acao}", "O perigo de anunciar sem estrategia", "medo", "O perigo de postar todo dia sem uma estrategia de hook"),
    HookFormat("Correcao", "Voce esta fazendo {acao} errado", "Voce esta perdendo vendas por causa disso", "medo", "Voce esta criando conteudo errado se ninguem assiste ate o final"),
    HookFormat("Identificacao", "{numero} sinais de que {situacao}", "3 sinais de que seu negocio vai crescer", "curiosidade", "3 sinais de que seu proximo video vai viralizar"),
    HookFormat("Hack de Especialista", "O truque que {profissao} usa para {resultado}", "O truque que copywriters usam pra vender mais", "ganho", "O truque que criadores virais usam para prender atencao nos 3 primeiros segundos"),
    HookFormat("Reviravolta", "Depois que vi isso, nunca mais {acao}", "Depois que vi isso, nunca mais anunciei igual", "curiosidade", "Depois que descobri isso, parei de postar sem estrategia"),
    HookFormat("Libertacao de Dor", "Nunca mais {problema}", "Nunca mais perca dinheiro com anuncios", "medo", "Nunca mais tenha um video com menos de 100 views"),
    HookFormat("Exclusividade", "O segredo de {resultado}", "O segredo das campanhas que vendem todo dia", "curiosidade", "O segredo dos reels que chegam a 1M de views sem trafego pago"),
    HookFormat("Valor Alto", "Guia completo para {objetivo}", "Guia completo para comecar no digital", "ganho", "Guia completo para criar hooks virais que prendem atencao"),
    HookFormat("Identidade", "So quem {acao} entende isso", "So quem tenta vender todo dia entende isso", "curiosidade", "So quem ja tentou viralizar sabe como e frustrante ter 10 views"),
]

TIPOS_EMOCIONAIS = ["curiosidade", "ganho", "medo", "urgencia"]


class HookGenerator:
    """Gera hooks virais usando 16 formatos classicos de atencao."""

    @staticmethod
    def get_all() -> List[HookFormat]:
        return FORMATOS

    @staticmethod
    def generate_hook(produto: str, dor: str, objetivo: str) -> Dict[str, str]:
        formato = random.choice(FORMATOS)
        hook = formato.template.format(
            resultado=f"vender mais com {produto}",
            objecao="aparecer",
            esforco="gastar com trafego",
            tempo="7 dias",
            coisa="esse metodo",
            acao="fazer hooks",
            numero="3",
            topico=dor,
            profissao="copywriters",
            problema="ter poucos views",
            profissao="criadores virais",
            objetivo="viralizar",
        )
        return {
            "formato": formato.nome,
            "hook": hook,
            "overlay": f"{objetivo.upper()}?",
            "cena": f"Mostre {produto} em acao nos primeiros 2s",
            "tipo_emocional": formato.tipo_emocional,
        }

    @staticmethod
    def generate_variations(n: int, produto: str, dor: str, objetivo: str) -> List[Dict[str, str]]:
        return [HookGenerator.generate_hook(produto, dor, objetivo) for _ in range(n)]