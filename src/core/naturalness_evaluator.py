from __future__ import annotations

import logging
from typing import Any


def avaliar_naturalidade(texto: str, avaliador: Any) -> float:
    if not texto or not avaliador:
        return 0.0
    try:
        resultado = avaliador(texto[:512])[0]

        label = resultado['label']
        score = resultado['score']

        if label == 'Real' or label == 'LABEL_0':
            naturalidade = score
        else:
            naturalidade = 1.0 - score

        logging.info(f"Avaliação de naturalidade concluída. Label: {label}, Score Original: {score:.4f}, Naturalidade Calc: {naturalidade:.4f}")
        return naturalidade

    except Exception as e:
        logging.error(f"Erro durante a avaliação de naturalidade: {e}", exc_info=True)
        return 0.0


# "A natureza nao faz nada em vao." - Aristoteles
