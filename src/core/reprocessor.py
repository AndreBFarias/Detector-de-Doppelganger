from __future__ import annotations

import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.detector import detectar_ia
from src.core.humanizador import humanizar_texto
from src.core.naturalness_evaluator import avaliar_naturalidade


def reprocessar_texto(
    texto_original,
    tokenizer,
    model,
    detector,
    evaluator,
    num_beams,
    temperature,
    progress_callback,
    stop_event,
    threshold_improvement=0.60,
    prompt_info=None,
):
    prob_original, _ = detectar_ia(texto_original, detector)
    max_iterations = 3
    current_text = texto_original
    current_prob = prob_original

    best_text = texto_original
    best_prob = prob_original
    best_naturalness = 0.0  # Inicializa

    # Avaliação inicial de naturalidade para baseline
    best_naturalness = avaliar_naturalidade(texto_original, evaluator)

    for iteration in range(max_iterations):
        if stop_event.is_set():
            break

        logging.info(f"Iniciando iteração {iteration + 1} de {max_iterations}...")

        # Quebra o texto em frases para processamento incremental
        frases = re.split(r"(?<=[.!?])\s+", current_text.strip())
        logging.debug(f"Texto quebrado em {len(frases)} frases: {frases}")

        texto_final_completo = ""
        total_frases = len(frases) if frases else 1

        for i, frase in enumerate(frases):
            if stop_event.is_set():
                break

            if not frase.strip():
                continue

            # Humaniza a frase e a anexa ao resultado
            frase_humanizada = humanizar_texto(
                frase, model, tokenizer, num_beams=num_beams, temperature=temperature, prompt_info=prompt_info
            )
            texto_final_completo += frase_humanizada + " "

            # Emite o progresso de forma incremental (ajustado para iterações)
            # Progresso total = (iteração_atual + progresso_na_iteração) / max_iterations
            progresso_iteracao = (i + 1) / total_frases
            progresso_total = (iteration + progresso_iteracao) / max_iterations
            progress_callback(progresso_total, frase_humanizada + " ")

        if stop_event.is_set():
            break

        # Análise final da iteração
        prob_final, _ = detectar_ia(texto_final_completo, detector)
        naturalidade_final = avaliar_naturalidade(texto_final_completo, evaluator)

        logging.info(
            f"Iteração {iteration + 1} concluída. Prob IA: {prob_final:.2f}, Naturalidade: {naturalidade_final:.2f}"
        )

        # Verifica se houve melhora em relação à iteração ANTERIOR (ou original na primeira)
        # Se a probabilidade de IA aumentou significativamente, degradou.
        # Usa uma tolerância (epsilon) para evitar paradas por flutuações minúsculas
        epsilon = 0.001
        if prob_final > (current_prob + epsilon):
            logging.warning(
                f"A humanização degradou o score (Atual: {prob_final:.2f} > Anterior: {current_prob:.2f}). Revertendo para o melhor resultado."
            )
            break  # Para o loop, mantendo o best_text atualizado até agora

        # Se melhorou ou manteve, atualiza o atual e verifica se é o melhor global
        current_text = texto_final_completo
        current_prob = prob_final

        if prob_final < best_prob:
            best_prob = prob_final
            best_text = texto_final_completo
            best_naturalness = naturalidade_final
            logging.info(f"Novo melhor resultado encontrado: Prob IA {best_prob:.2f}")

        # Verifica se atingiu a meta de 60% de melhoria em relação ao ORIGINAL
        target_prob = prob_original * (1 - threshold_improvement)

        if prob_final <= target_prob:
            logging.info(f"Meta de melhoria atingida ({prob_final:.2f} <= {target_prob:.2f}). Parando reprocessamento.")
            break

    logging.info(f"Reprocessamento finalizado. Melhor Prob IA: {best_prob:.2f}")

    return best_text, best_prob, best_naturalness
