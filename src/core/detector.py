from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def detectar_ia(texto, detector_pipeline):
    """
    Analisa o texto e retorna a probabilidade de ser gerado por IA.
    """
    if not texto.strip():
        logging.warning("detectar_ia chamado com texto vazio.")
        return 0.0, "Texto vazio"

    if detector_pipeline is None:
        logging.error("Falha crítica: detectar_ia foi chamado com um pipeline NULO.")
        return 0.0, "Erro: Detector não carregado"

    try:
        resultados = detector_pipeline(texto, truncation=True, max_length=512)

        # A saída padrão do 'openai-detector' é 'Real' (LABEL_0) ou 'Fake' (LABEL_1)
        for resultado in resultados:
            if resultado["label"] == "Real" or resultado["label"] == "LABEL_0":
                # Score é a confiança no 'Real'. Invertemos para obter a prob. de IA.
                prob_ia = 1.0 - resultado["score"]
                label = f"Humano ({100 - prob_ia*100:.1f}%)"
                return prob_ia, label
            elif resultado["label"] == "Fake" or resultado["label"] == "LABEL_1":
                # Score é a confiança no 'Fake' (IA).
                prob_ia = resultado["score"]
                label = f"IA ({prob_ia*100:.1f}%)"
                return prob_ia, label

        logging.warning(f"Nenhum label 'Real' ou 'Fake' encontrado na saída do detector: {resultados}")
        return 0.0, "Erro: Label desconhecido"

    except Exception as e:
        logging.error(f"Falha ao executar pipeline de detecção: {e}", exc_info=True)
        return 0.0, "Erro na análise"
