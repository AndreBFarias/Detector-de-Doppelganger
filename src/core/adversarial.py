from __future__ import annotations

import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import config

logger = logging.getLogger(__name__)

ADVERBIOS_IA = [
    "significativamente",
    "fundamentalmente",
    "extremamente",
    "consideravelmente",
    "notavelmente",
    "essencialmente",
    "particularmente",
    "especificamente",
    "evidentemente",
    "obviamente",
    "naturalmente",
    "certamente",
    "definitivamente",
    "absolutamente",
    "completamente",
    "totalmente",
    "amplamente",
    "profundamente",
    "intrinsecamente",
    "inerentemente",
    "indubitavelmente",
    "inequivocamente",
    "primordialmente",
    "substancialmente",
    "exponencialmente",
]

ADJETIVOS_IA = [
    "significativo",
    "significativa",
    "fundamental",
    "crucial",
    "imprescindível",
    "primordial",
    "substancial",
    "exponencial",
    "irreversível",
]

CONECTIVOS_IA = {
    "além disso,": "",
    "ademais,": "",
    "portanto,": "",
    "consequentemente,": "",
    "entretanto,": "mas",
    "no entanto,": "mas",
    "todavia,": "mas",
    "contudo,": "mas",
    "outrossim,": "",
    "destarte,": "",
    "dessarte,": "",
    "nesse sentido,": "",
    "por conseguinte,": "",
    "em suma,": "",
    "em síntese,": "",
    "de fato,": "",
    "com efeito,": "",
    "vale ressaltar que": "",
    "é importante destacar que": "",
    "cabe mencionar que": "",
    "faz-se necessário": "é preciso",
    "torna-se imperativo": "é preciso",
}

EXPRESSOES_FORMAIS = {
    "no que tange a": "sobre",
    "no que diz respeito a": "sobre",
    "no tocante a": "sobre",
    "em relação a": "sobre",
    "no âmbito de": "em",
    "por meio de": "com",
    "através de": "por",
    "a fim de": "para",
    "com o intuito de": "para",
    "com vistas a": "para",
    "tendo em vista": "considerando",
    "diante do exposto": "",
    "ante o exposto": "",
    "face ao exposto": "",
    "frente a isso": "",
}


class AdversarialHumanizer:
    def __init__(self, synonym_rate: float = 0.15, entropy_factor: float = 1.2) -> None:
        self.synonym_rate = synonym_rate
        self.entropy_factor = entropy_factor

    def humanize(self, texto: str) -> str:
        if not texto.strip():
            return texto

        resultado = texto
        resultado = self._remover_adverbios_ia(resultado)
        resultado = self._simplificar_conectivos(resultado)
        resultado = self._simplificar_expressoes(resultado)
        resultado = self._limpar_espacos(resultado)

        return resultado

    def _remover_adverbios_ia(self, texto: str) -> str:
        for adv in ADVERBIOS_IA:
            pattern = re.compile(rf"\s+\b{adv}\b(?=\s)", re.IGNORECASE)
            texto = pattern.sub(" ", texto)
            pattern = re.compile(rf",\s*\b{adv}\b\s*,", re.IGNORECASE)
            texto = pattern.sub(",", texto)
        return texto

    def _remover_adjetivos_ia(self, texto: str) -> str:
        for adj in ADJETIVOS_IA:
            pattern = re.compile(rf"\s+\b{adj}\b(?=[\s.,;:!?])", re.IGNORECASE)
            texto = pattern.sub(" ", texto)
        return texto

    def _simplificar_conectivos(self, texto: str) -> str:
        for conectivo, substituto in CONECTIVOS_IA.items():
            pattern = re.compile(re.escape(conectivo), re.IGNORECASE)
            if substituto:
                sub_val = substituto

                def replace_case(match: re.Match, sub=sub_val) -> str:
                    original = match.group(0)
                    if original[0].isupper():
                        return sub.capitalize()
                    return sub

                texto = pattern.sub(replace_case, texto)
            else:
                texto = pattern.sub(" ", texto)
        return texto

    def _simplificar_expressoes(self, texto: str) -> str:
        for expr, substituto in EXPRESSOES_FORMAIS.items():
            pattern = re.compile(re.escape(expr), re.IGNORECASE)
            if substituto:
                sub_val = substituto

                def replace_case(match: re.Match, sub=sub_val) -> str:
                    original = match.group(0)
                    if original[0].isupper():
                        return sub.capitalize()
                    return sub

                texto = pattern.sub(replace_case, texto)
            else:
                texto = pattern.sub(" ", texto)
        return texto

    def _limpar_espacos(self, texto: str) -> str:
        texto = re.sub(r",\s*,", ",", texto)
        texto = re.sub(r"\s{2,}", " ", texto)
        texto = re.sub(r"\s+([.,;:!?])", r"\1", texto)
        texto = re.sub(r"^\s+", "", texto, flags=re.MULTILINE)
        texto = re.sub(r"\.\s*\.", ".", texto)
        texto = re.sub(r"^\s*,\s*", "", texto)
        texto = re.sub(r"([a-záéíóúàâãêîôûç])([A-ZÁÉÍÓÚÀÂÃÊÎÔÛÇ])", r"\1 \2", texto)
        texto = re.sub(r"([.,;:!?])([A-Za-záéíóúàâãêîôûçÁÉÍÓÚÀÂÃÊÎÔÛÇ])", r"\1 \2", texto)
        texto = re.sub(r"\s{2,}", " ", texto)

        sentencas = re.split(r"(?<=[.!?])\s+", texto)
        sentencas_corrigidas = []
        for s in sentencas:
            s = s.strip()
            if s:
                if s[0].islower():
                    s = s[0].upper() + s[1:]
                if s.startswith(","):
                    s = s[1:].strip()
                    if s and s[0].islower():
                        s = s[0].upper() + s[1:]
                sentencas_corrigidas.append(s)

        return " ".join(sentencas_corrigidas)


def humanizar_adversarial(texto: str) -> str:
    humanizer = AdversarialHumanizer(
        synonym_rate=config.ADVERSARIAL_SYNONYM_RATE,
        entropy_factor=config.ADVERSARIAL_ENTROPY_FACTOR,
    )
    return humanizer.humanize(texto)


# "A imperfeicao e a beleza da humanidade." - Nietzsche
