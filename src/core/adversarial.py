from __future__ import annotations

import logging
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import config

logger = logging.getLogger(__name__)

SINONIMOS_PT = {
    "entretanto": ["porém", "contudo", "todavia", "no entanto", "mas"],
    "portanto": ["logo", "assim", "por isso", "então", "consequentemente"],
    "além disso": ["ademais", "também", "igualmente", "outrossim"],
    "importante": ["relevante", "significativo", "essencial", "crucial"],
    "realizar": ["fazer", "executar", "efetuar", "concretizar"],
    "utilizar": ["usar", "empregar", "aplicar"],
    "demonstrar": ["mostrar", "evidenciar", "revelar", "indicar"],
    "considerar": ["pensar", "ponderar", "refletir", "avaliar"],
    "apresentar": ["expor", "mostrar", "exibir", "revelar"],
    "possibilitar": ["permitir", "viabilizar", "propiciar"],
    "compreender": ["entender", "assimilar", "perceber", "captar"],
    "estabelecer": ["definir", "fixar", "determinar", "instituir"],
    "desenvolver": ["criar", "elaborar", "construir", "produzir"],
    "necessário": ["preciso", "indispensável", "essencial", "obrigatório"],
    "fundamental": ["básico", "essencial", "primordial", "crucial"],
    "significativo": ["expressivo", "relevante", "notável", "considerável"],
    "frequentemente": ["muitas vezes", "com frequência", "amiúde", "seguidamente"],
    "especificamente": ["particularmente", "em especial", "notadamente"],
    "inicialmente": ["primeiramente", "a princípio", "no início", "primeiro"],
    "finalmente": ["por fim", "enfim", "ao final", "em conclusão"],
    "atualmente": ["hoje em dia", "nos dias de hoje", "presentemente"],
    "geralmente": ["normalmente", "em geral", "usualmente", "via de regra"],
    "basicamente": ["essencialmente", "fundamentalmente", "em essência"],
    "obviamente": ["claramente", "evidentemente", "naturalmente"],
}

CONECTIVOS_HUMANOS = [
    "bom,",
    "olha,",
    "veja bem,",
    "tipo assim,",
    "sabe,",
    "na real,",
    "pra ser sincero,",
    "falando nisso,",
    "a propósito,",
    "enfim,",
    "de qualquer forma,",
    "seja como for,",
]

EXPRESSOES_IDIOMATICAS = [
    "dar uma mãozinha",
    "fazer das tripas coração",
    "quebrar um galho",
    "tirar de letra",
    "pegar o jeito",
    "dar conta do recado",
    "colocar a mão na massa",
]


class AdversarialHumanizer:
    def __init__(self, synonym_rate: float = 0.15, entropy_factor: float = 1.2) -> None:
        self.synonym_rate = synonym_rate
        self.entropy_factor = entropy_factor

    def humanize(self, texto: str) -> str:
        if not texto.strip():
            return texto

        resultado = texto
        resultado = self._substituir_sinonimos(resultado)
        resultado = self._variar_pontuacao(resultado)
        resultado = self._variar_estrutura(resultado)
        resultado = self._adicionar_imperfeicoes(resultado)

        return resultado

    def _substituir_sinonimos(self, texto: str) -> str:
        palavras = texto.split()
        total_palavras = len(palavras)
        num_substituicoes = int(total_palavras * self.synonym_rate)

        indices_candidatos = []
        for i, palavra in enumerate(palavras):
            palavra_limpa = re.sub(r"[^\w]", "", palavra.lower())
            if palavra_limpa in SINONIMOS_PT:
                indices_candidatos.append(i)

        if not indices_candidatos:
            return texto

        indices_selecionados = random.sample(indices_candidatos, min(num_substituicoes, len(indices_candidatos)))

        for idx in indices_selecionados:
            palavra_original = palavras[idx]
            palavra_limpa = re.sub(r"[^\w]", "", palavra_original.lower())

            if palavra_limpa in SINONIMOS_PT:
                sinonimo = random.choice(SINONIMOS_PT[palavra_limpa])

                if palavra_original[0].isupper():
                    sinonimo = sinonimo.capitalize()

                sufixo = ""
                for char in reversed(palavra_original):
                    if not char.isalnum():
                        sufixo = char + sufixo
                    else:
                        break

                palavras[idx] = sinonimo + sufixo

        return " ".join(palavras)

    def _variar_pontuacao(self, texto: str) -> str:
        texto = re.sub(r"\.{3,}", "...", texto)

        if random.random() < 0.1:
            texto = texto.replace(". ", "... ", 1)

        if random.random() < 0.15:
            texto = re.sub(r"([a-záéíóú]),", r"\1 –", texto, count=1)

        return texto

    def _variar_estrutura(self, texto: str) -> str:
        sentencas = re.split(r"(?<=[.!?])\s+", texto)

        if len(sentencas) >= 3 and random.random() < 0.2:
            idx = random.randint(1, len(sentencas) - 1)
            if len(sentencas[idx]) > 50 and ", " in sentencas[idx]:
                partes = sentencas[idx].split(", ", 1)
                if len(partes) == 2:
                    sentencas[idx] = partes[0] + ". " + partes[1].capitalize()

        if len(sentencas) >= 2 and random.random() < 0.15:
            for i in range(len(sentencas) - 1):
                if len(sentencas[i]) < 40 and len(sentencas[i + 1]) < 40:
                    if sentencas[i].endswith("."):
                        conectivo = random.choice(["e", "mas", "porém"])
                        sentencas[i] = sentencas[i][:-1] + ", " + conectivo + " " + sentencas[i + 1].lower()
                        sentencas[i + 1] = ""
                        break

        return " ".join(s for s in sentencas if s.strip())

    def _adicionar_imperfeicoes(self, texto: str) -> str:
        if random.random() < 0.1:
            sentencas = re.split(r"(?<=[.!?])\s+", texto)
            if sentencas:
                conectivo = random.choice(CONECTIVOS_HUMANOS)
                primeira = sentencas[0]
                if primeira and primeira[0].isupper():
                    primeira = primeira[0].lower() + primeira[1:]
                sentencas[0] = conectivo.capitalize() + " " + primeira
                texto = " ".join(sentencas)

        texto = re.sub(
            r"\bvocê\b", lambda m: random.choice(["você", "vc"]) if random.random() < 0.05 else m.group(), texto
        )
        texto = re.sub(r"\bporque\b", lambda m: "pq" if random.random() < 0.03 else m.group(), texto)
        texto = re.sub(
            r"\bmuito\b", lambda m: random.choice(["muito", "mt"]) if random.random() < 0.03 else m.group(), texto
        )

        return texto


def humanizar_adversarial(texto: str) -> str:
    humanizer = AdversarialHumanizer(
        synonym_rate=config.ADVERSARIAL_SYNONYM_RATE,
        entropy_factor=config.ADVERSARIAL_ENTROPY_FACTOR,
    )
    return humanizer.humanize(texto)


# "A imperfeicao e a beleza da humanidade." - Nietzsche
