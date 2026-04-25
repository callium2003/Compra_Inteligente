from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class HookFormat:
    nome: str
    template: str
    exemplo: str
    tipo_emocional: str
    exemplo_pratico_real: str


class HookGenerator:
    """Gera hooks virais usando 16 formatos clássicos de atenção."""

    FORMATS: List[HookFormat] = [
        HookFormat("Quebra de padrão", "Pare de {erro}. Faça isso: {solucao}.", "Pare de postar sem gancho. Faça isso: comece com um choque visual.", "urgencia", "Ex.: 'Pare de tentar emagrecer cortando tudo. Faça isso: monte 2 refeições com alta saciedade por dia.'"),
        HookFormat("Segredo revelado", "Ninguém fala isso sobre {tema}...", "Ninguém fala isso sobre perder peso sem dieta maluca...", "curiosidade", "Ex.: 'Ninguém fala isso sobre ganhar dinheiro: oferta clara converte mais que postar todo dia.'"),
        HookFormat("Erro comum", "Se você ainda {erro}, está travando {resultado}.", "Se você ainda grava sem roteiro, está travando seu alcance.", "medo", "Ex.: 'Se você ainda responde no impulso no relacionamento, está travando sua conexão emocional.'"),
        HookFormat("Lista curta", "{quantidade} passos para {resultado} ainda hoje.", "3 passos para vender mais com vídeos ainda hoje.", "ganho", "Ex.: '3 passos para aumentar sua energia ainda hoje: água, luz solar e caminhada pós-almoço.'"),
        HookFormat("Contrarian", "Esqueça {crenca}. O que funciona é {nova_abordagem}.", "Esqueça consistência sem estratégia. O que funciona é consistência com estrutura.", "curiosidade", "Ex.: 'Esqueça cardio infinito. O que funciona é treino de força + déficit moderado.'"),
        HookFormat("Dor específica", "Você sente {dor}? Isso está custando {prejuizo}.", "Você sente vergonha de aparecer? Isso está custando clientes.", "medo", "Ex.: 'Você sente cansaço todo dia? Isso está custando sua produtividade e foco.'"),
        HookFormat("Prova rápida", "Eu fiz {resultado} em {tempo} e vou te mostrar como.", "Eu fiz 40 vendas em 7 dias e vou te mostrar como.", "ganho", "Ex.: 'Eu recuperei minha rotina de sono em 14 dias e vou te mostrar o protocolo.'"),
        HookFormat("Pergunta provocativa", "Você realmente sabe {tema}?", "Você realmente sabe por que seus vídeos não retêm?", "curiosidade", "Ex.: 'Você realmente sabe por que seu perfil tem visualização, mas não tem cliente?'"),
        HookFormat("Antes x depois", "Antes: {antes}. Depois: {depois}.", "Antes: 500 views. Depois: 50k views em 1 semana.", "ganho", "Ex.: 'Antes: discussões diárias. Depois: comunicação respeitosa em 2 semanas.'"),
        HookFormat("Desafio", "Te desafio a testar isso por {tempo}.", "Te desafio a testar esse roteiro por 3 dias.", "urgencia", "Ex.: 'Te desafio a aplicar esse roteiro de oferta por 72h e medir seus leads.'"),
        HookFormat("Mito vs verdade", "Mito: {mito}. Verdade: {verdade}.", "Mito: precisa viralizar para vender. Verdade: precisa converter.", "curiosidade", "Ex.: 'Mito: cortar carboidrato emagrece. Verdade: o que emagrece é consistência no déficit.'"),
        HookFormat("Ameaça de perda", "Se ignorar isso, você perde {beneficio}.", "Se ignorar isso, você perde leads todos os dias.", "medo", "Ex.: 'Se ignorar esse check-up, você perde chance de prevenir problemas silenciosos.'"),
        HookFormat("Tutorial relâmpago", "Em {tempo}, você vai aprender {habilidade}.", "Em 30 segundos, você vai aprender um hook que prende.", "ganho", "Ex.: 'Em 20 segundos, você vai aprender a abrir um vídeo com retenção alta.'"),
        HookFormat("Confissão", "Eu também {falha}, até descobrir {virada}.", "Eu também travava na câmera, até descobrir esse script.", "curiosidade", "Ex.: 'Eu também falhava nas vendas por DM, até descobrir um script de 4 mensagens.'"),
        HookFormat("Alvo específico", "Se você é {publico}, isso é para você.", "Se você é nutricionista iniciando no digital, isso é para você.", "ganho", "Ex.: 'Se você é mãe sem tempo e quer emagrecer, isso é para você.'"),
        HookFormat("Alerta urgente", "Urgente: {mudanca} já está afetando {publico}.", "Urgente: o algoritmo já está punindo vídeos sem retenção inicial.", "urgencia", "Ex.: 'Urgente: novos padrões de retenção já estão reduzindo alcance de vídeos longos sem gancho.'"),
    ]

    def generate_variations(self, contexto: Dict[str, str], quantidade: int = 3) -> List[Dict[str, str]]:
        pool = self.FORMATS.copy()
        random.shuffle(pool)
        hooks = []
        for formato in pool[:quantidade]:
            hook_text = formato.template.format(
                tema=contexto["produto"],
                erro=contexto.get("erro", "fazendo o básico"),
                solucao=contexto.get("promessa", "usar um roteiro em blocos"),
                resultado=contexto.get("objetivo", "resultado"),
                quantidade=contexto.get("quantidade", "3"),
                crenca=contexto.get("crenca", "seguir dicas genéricas"),
                nova_abordagem=contexto.get("nova_abordagem", "usar dados de retenção"),
                dor=contexto.get("dor", "estagnação"),
                prejuizo=contexto.get("prejuizo", "tempo e oportunidade"),
                tempo=contexto.get("tempo", "7 dias"),
                antes=contexto.get("antes", "pouco alcance"),
                depois=contexto.get("depois", "alta retenção"),
                mito=contexto.get("mito", "mais conteúdo = mais vendas"),
                verdade=contexto.get("verdade", "mais clareza = mais vendas"),
                beneficio=contexto.get("beneficio", "crescimento"),
                habilidade=contexto.get("habilidade", "abrir vídeos com impacto"),
                falha=contexto.get("falha", "fazia vídeos longos demais"),
                virada=contexto.get("virada", "o framework NEXUS"),
                publico=contexto["publico"],
                mudanca=contexto.get("mudanca", "uma nova tendência de consumo"),
            )
            hooks.append(
                {
                    "formato": formato.nome,
                    "tipo_emocional": formato.tipo_emocional,
                    "hook": hook_text,
                    "overlay": f"Overlay: {hook_text}",
                    "cena": f"Cena sugerida: close rápido + texto em tela para {contexto['plataforma']}",
                    "exemplo_formato": formato.exemplo,
                    "exemplo_pratico_real": formato.exemplo_pratico_real,
                }
            )
        return hooks
