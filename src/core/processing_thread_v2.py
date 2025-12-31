from __future__ import annotations

import logging
import queue
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import config
from src.core.engine import DoppelgangerEngine

logger = logging.getLogger(__name__)


class ProcessingThreadV2(threading.Thread):
    def __init__(
        self,
        text: str,
        criatividade: float,
        intensidade: int,
        ui_queue: queue.Queue,
        style_key: str = "casual",
        detector_mode: str = "local",
        humanizer_mode: str = "local",
    ) -> None:
        super().__init__(daemon=True)
        self.text_original = text
        self.criatividade = criatividade
        self.intensidade = int(intensidade)
        self.ui_queue = ui_queue
        self.style_key = style_key
        self.detector_mode = detector_mode
        self.humanizer_mode = humanizer_mode
        self.stop_event = threading.Event()

        self.engine: DoppelgangerEngine | None = None

    def run(self) -> None:
        try:
            self.emit_status("Inicializando engine...")

            self.engine = DoppelgangerEngine(
                detector_mode=self.detector_mode,
                humanizer_mode=self.humanizer_mode,
                api_provider="groq" if config.GROQ_API_KEY else "gemini",
                max_iterations=config.MAX_ITERATIONS,
                target_score=config.TARGET_SCORE,
                progress_callback=self._on_progress,
            )

            self.emit_status("Analisando texto original...")
            score_inicial, label_inicial = self.engine.detect(self.text_original)

            naturalidade_inicial = 1.0 - score_inicial

            self.emit_initial_stats(score_inicial, naturalidade_inicial)

            if self.stop_event.is_set():
                self.emit_status("Processamento interrompido.")
                return

            self.emit_status("Processando texto...")

            result = self._process_with_progress()

            if self.stop_event.is_set():
                self.emit_status("Processamento interrompido.")
            else:
                naturalidade_final = 1.0 - result.score_final
                self.emit_final_result(result.score_final, naturalidade_final)
                self.emit_status(result.mensagem)

        except Exception as e:
            logger.error(f"Erro na thread de processamento: {e}", exc_info=True)
            self.emit_status(f"Erro: {e}")
        finally:
            self.ui_queue.put({"type": "finished"})

    def _process_with_progress(self):
        if self.engine is None:
            raise RuntimeError("Engine nao inicializado")

        from src.core.engine import IterationResult, ProcessResult

        score_inicial, _ = self.engine.detect(self.text_original)

        if score_inicial < self.engine.target_score:
            self.emit_progress_update(1.0, self.text_original)
            return ProcessResult(
                texto_original=self.text_original,
                texto_final=self.text_original,
                score_inicial=score_inicial,
                score_final=score_inicial,
                iteracoes=[],
                sucesso=True,
                mensagem=f"Texto ja possui score baixo: {score_inicial:.2%}",
            )

        iteracoes: list[IterationResult] = []
        texto_atual = self.text_original
        score_atual = score_inicial
        melhor_texto = self.text_original
        melhor_score = score_inicial

        for i in range(self.engine.max_iterations):
            if self.stop_event.is_set():
                break

            progress = (i + 0.5) / self.engine.max_iterations
            self._on_progress(f"Iteracao {i + 1}/{self.engine.max_iterations}...", progress)

            texto_humanizado = self.engine.humanize(texto_atual, self.style_key)

            self.emit_progress_update((i + 0.7) / self.engine.max_iterations, texto_humanizado if i == 0 else "")

            novo_score, novo_label = self.engine.detect(texto_humanizado)

            iteracao = IterationResult(
                texto=texto_humanizado,
                score_ia=novo_score,
                label=novo_label,
                iteracao=i + 1,
            )
            iteracoes.append(iteracao)

            logger.info(
                f"Iteracao {i + 1}: score {score_atual:.2%} -> {novo_score:.2%} "
                f"(delta: {(score_atual - novo_score):.2%})"
            )

            if novo_score < melhor_score:
                melhor_score = novo_score
                melhor_texto = texto_humanizado

            if novo_score < self.engine.target_score:
                self._on_progress("Meta alcancada!", 1.0)
                self.emit_progress_update(1.0, "")
                return ProcessResult(
                    texto_original=self.text_original,
                    texto_final=texto_humanizado,
                    score_inicial=score_inicial,
                    score_final=novo_score,
                    iteracoes=iteracoes,
                    sucesso=True,
                    mensagem=f"Score reduzido para {novo_score:.2%} em {i + 1} iteracao(oes)",
                )

            if novo_score >= score_atual:
                logger.warning(f"Score nao reduziu na iteracao {i + 1}.")

            texto_atual = texto_humanizado
            score_atual = novo_score

        self._on_progress("Processamento concluido", 1.0)
        self.emit_progress_update(1.0, "")

        sucesso = melhor_score < score_inicial * 0.7

        return ProcessResult(
            texto_original=self.text_original,
            texto_final=melhor_texto,
            score_inicial=score_inicial,
            score_final=melhor_score,
            iteracoes=iteracoes,
            sucesso=sucesso,
            mensagem=f"Score: {score_inicial:.2%} -> {melhor_score:.2%} ({len(iteracoes)} iteracoes)",
        )

    def _on_progress(self, message: str, progress: float) -> None:
        self.emit_status(message)

    def emit(self, data: dict) -> None:
        self.ui_queue.put(data)

    def emit_status(self, message: str) -> None:
        self.emit({"type": "status", "value": message})

    def emit_initial_stats(self, prob_ia: float, naturalidade: float) -> None:
        self.emit({"type": "initial_stats", "prob_ia": prob_ia, "naturalidade": naturalidade})

    def emit_progress_update(self, progress: float, text_chunk: str) -> None:
        self.emit({"type": "progress", "progress": progress, "chunk": text_chunk})

    def emit_final_result(self, prob_ia: float, naturalidade: float) -> None:
        self.emit({"type": "final_result", "prob_ia": prob_ia, "naturalidade": naturalidade})

    def stop(self) -> None:
        self.stop_event.set()


# "A evolucao nao e uma forca, mas um processo." - Ernst Mayr
