# 23
import threading
import queue
import logging
from src.detector import detectar_ia
from src.reprocessor import reprocessar_texto
from src.naturalness_evaluator import avaliar_naturalidade

class ProcessingThread(threading.Thread):
    def __init__(self, app_core, text, criatividade, intensidade, ui_queue, style_key="default"):
        # 23
        super().__init__(daemon=True)
        self.core = app_core
        self.text_original = text
        self.criatividade = criatividade
        self.intensidade = intensidade
        self.ui_queue = ui_queue
        self.style_key = style_key
        self.stop_event = threading.Event()

    # 24
    def run(self):
        try:
            # 25. Análise Inicial
            self.emit_status("Analisando texto original...")
            prob_ia_original, _ = detectar_ia(self.text_original, self.core.detector)
            naturalidade_original = avaliar_naturalidade(self.text_original, self.core.naturalness_evaluator)
            self.emit_initial_stats(prob_ia_original, naturalidade_original)

            # 26. Reprocessamento
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
                prompt_info=prompt_info
            )

            # 27. Enviar resultados finais ou status de interrupção
            if self.stop_event.is_set():
                self.emit_status("Processamento interrompido.")
            else:
                self.emit_final_result(prob_ia_final, naturalidade_final)
                self.emit_status("Processo concluído.")

        except Exception as e:
            logging.error(f"Erro na thread de processamento: {e}", exc_info=True)
            self.emit_status(f"Erro: {e}")
        finally:
            # Sinaliza que a thread terminou
            self.ui_queue.put({"type": "finished"})

    # 28
    def emit(self, data):
        self.ui_queue.put(data)

    # 28
    def emit_status(self, message):
        self.emit({"type": "status", "value": message})

    # 29
    def emit_initial_stats(self, prob_ia, naturalidade):
        self.emit({"type": "initial_stats", "prob_ia": prob_ia, "naturalidade": naturalidade})

    # 30
    def emit_progress_update(self, progress, text_chunk):
        self.emit({"type": "progress", "progress": progress, "chunk": text_chunk})
    
    # 31
    def emit_final_result(self, prob_ia, naturalidade):
        self.emit({"type": "final_result", "prob_ia": prob_ia, "naturalidade": naturalidade})

    # 31
    def stop(self):
        self.stop_event.set()
