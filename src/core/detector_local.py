from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import torch
from transformers import pipeline

import config

logger = logging.getLogger(__name__)


FINETUNED_MODEL_PATH = config.MODELS_DIR / "detector_pt_finetuned"


class DetectorLocal:
    _instance: DetectorLocal | None = None
    _pipeline: Any = None
    _model_name: str | None = None

    def __new__(cls) -> DetectorLocal:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._pipeline is None:
            self._load_model()

    def _load_model(self) -> None:
        finetuned_exists = FINETUNED_MODEL_PATH.exists() and (FINETUNED_MODEL_PATH / "model.safetensors").exists()

        if finetuned_exists:
            model_path = str(FINETUNED_MODEL_PATH)
            logger.info(f"Carregando detector fine-tuned PT-BR: {model_path}")
        else:
            model_path = config.DETECTOR_MODEL
            logger.info(f"Carregando detector base: {model_path}")

        try:
            from transformers import AutoModelForSequenceClassification, AutoTokenizer

            device = 0 if torch.cuda.is_available() else -1

            model = AutoModelForSequenceClassification.from_pretrained(
                model_path,
                cache_dir=str(config.HF_HOME) if not finetuned_exists else None,
            )
            tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                cache_dir=str(config.HF_HOME) if not finetuned_exists else None,
            )

            self._pipeline = pipeline(
                "text-classification",
                model=model,
                tokenizer=tokenizer,
                device=device,
            )
            self._model_name = "detector_pt_finetuned" if finetuned_exists else model_path
            logger.info(f"Detector carregado com sucesso. Device: {'GPU' if device == 0 else 'CPU'}")
        except Exception as e:
            logger.error(f"Falha ao carregar detector: {e}")
            self._pipeline = None

    def detect(self, texto: str) -> tuple[float, str]:
        if not texto.strip():
            logger.warning("detect chamado com texto vazio.")
            return 0.0, "Texto vazio"

        if self._pipeline is None:
            logger.error("Pipeline de deteccao nao carregado.")
            return 0.0, "Erro: Detector nao carregado"

        try:
            resultados = self._pipeline(texto, truncation=True, max_length=512)

            for resultado in resultados:
                label = resultado["label"]
                score = resultado["score"]

                if label in ("Real", "LABEL_0"):
                    prob_ia = 1.0 - score
                    return prob_ia, f"Humano ({(1 - prob_ia) * 100:.1f}%)"
                elif label in ("Fake", "LABEL_1"):
                    prob_ia = score
                    return prob_ia, f"IA ({prob_ia * 100:.1f}%)"

            logger.warning(f"Label desconhecido na saida do detector: {resultados}")
            return 0.0, "Erro: Label desconhecido"

        except Exception as e:
            logger.error(f"Falha na deteccao: {e}", exc_info=True)
            return 0.0, "Erro na analise"

    def get_model_name(self) -> str:
        return self._model_name or "Nao carregado"

    def unload(self) -> None:
        if self._pipeline is not None:
            del self._pipeline
            self._pipeline = None
        self._model_name = None

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

        import gc

        gc.collect()
        logger.info("Detector descarregado e memoria liberada.")


def get_detector() -> DetectorLocal:
    return DetectorLocal()


def detectar_ia_local(texto: str) -> tuple[float, str]:
    detector = get_detector()
    return detector.detect(texto)


# "A duvida e a origem da sabedoria." - Rene Descartes
