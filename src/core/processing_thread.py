from __future__ import annotations

import logging
import queue
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.detector import detectar_ia
from src.core.naturalness_evaluator import avaliar_naturalidade
from src.core.reprocessor import reprocessar_texto


class ProcessingThread(threading.Thread):
    def __init__(
        self,
        app_core,
        text: str,
        criatividade: float,
        intensidade: int,
        ui_queue: queue.Queue,
        style_key: str = "default",
    ) -> None:
        super().__init__(daemon=True)
        self.core = app_core
        self.text_original = text
        self.criatividade = criatividade
        self.intensidade = intensidade
        self.ui_queue = ui_queue
        self.style_key = style_key
        self.stop_event = threading.Event()

    def run(self) -> None:
        try:
            self.emit_status("Analisando texto original...")
            prob_ia_original, _ = detectar_ia(self.text_original, self.core.detector)
            naturalidade_original = avaliar_naturalidade(self.text_original, self.core.naturalness_evaluator)
            self.emit_initial_stats(prob_ia_original, naturalidade_original)

            self.emit_status("Humanizando e reprocessando...")

            prompt_info = self.core.get_style_info(self.style_key)

            texto_final, prob_ia_final, naturalidade_final = reprocessar_texto(
                texto_original=self.text_original,
                tokenizer=self.core.humanizer_tokenizer,
                model=self.core.humanizer_model,
                detector=self.core.detector,
                evaluator=self.core.naturalness_evaluator,
                num_beams=int(self.intensidade),
                temperature=self.criatividade,
                progress_callback=self.emit_progress_update,
                stop_event=self.stop_event,
                prompt_info=prompt_info,
            )

            if self.stop_event.is_set():
                self.emit_status("Processamento interrompido.")
            else:
                self.emit_final_result(prob_ia_final, naturalidade_final)
                self.emit_status("Processo concluido.")

        except Exception as e:
            logging.error(f"Erro na thread de processamento: {e}", exc_info=True)
            self.emit_status(f"Erro: {e}")
        finally:
            self.ui_queue.put({"type": "finished"})

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


# "O tempo e o melhor professor, infelizmente ele mata todos os seus alunos." - Robin Williams
