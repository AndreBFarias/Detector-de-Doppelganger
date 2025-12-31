from __future__ import annotations

import logging
import os
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, T5ForConditionalGeneration

import config

logger = logging.getLogger(__name__)


def load_model_and_tokenizer(
    model_name_or_path: str,
    model_class: Any,
    tokenizer_class: Any,
    device: torch.device,
    hf_home: str,
    task_name: str = "Modelo",
) -> tuple[Any, Any]:
    logger.info(f"Iniciando carregamento: {task_name} ({model_name_or_path})")
    try:
        local_cache_path = os.path.join(hf_home, model_name_or_path.replace("/", "_"))

        try:
            if os.path.exists(local_cache_path):
                logger.info(f"Carregando {task_name} do cache local: {local_cache_path}")
                model = model_class.from_pretrained(local_cache_path, local_files_only=True).to(device)
                tokenizer = tokenizer_class.from_pretrained(local_cache_path, local_files_only=True)
                logger.info(f"{task_name} carregado com sucesso do cache.")
                return model, tokenizer
        except Exception as e:
            logger.warning(f"Falha ao carregar {task_name} do cache local ({e}). Tentando baixar...")

        logger.info(f"Baixando e salvando {task_name} em: {local_cache_path}")
        model = model_class.from_pretrained(model_name_or_path, cache_dir=hf_home).to(device)
        tokenizer = tokenizer_class.from_pretrained(model_name_or_path, cache_dir=hf_home)

        model.save_pretrained(local_cache_path)
        tokenizer.save_pretrained(local_cache_path)

        logger.info(f"{task_name} baixado e salvo com sucesso.")
        return model, tokenizer

    except Exception as e:
        logger.error(f"Erro critico ao carregar {task_name} ({model_name_or_path}): {e}")
        return None, None


class ModelLoader:
    def __init__(self, status_callback: Callable[[str, float], None] | None = None) -> None:
        self.status_callback = status_callback
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Device set to use {self.device}")

        self.hf_home = str(config.HF_HOME)
        os.makedirs(self.hf_home, exist_ok=True)

    def _report_status(self, text: str, value: float) -> None:
        if self.status_callback:
            self.status_callback(text, value)
        logger.info(text)

    def load_models(self) -> None:
        try:
            models_to_load = [
                {
                    "name": "Detector",
                    "path": config.DETECTOR_MODEL,
                    "model_class": AutoModelForSequenceClassification,
                    "tokenizer_class": AutoTokenizer,
                },
                {
                    "name": "Humanizador Leve",
                    "path": config.HUMANIZADOR_LEVE,
                    "model_class": T5ForConditionalGeneration,
                    "tokenizer_class": AutoTokenizer,
                },
                {
                    "name": "Humanizador Equilibrado",
                    "path": config.HUMANIZADOR_EQUILIBRADO,
                    "model_class": T5ForConditionalGeneration,
                    "tokenizer_class": AutoTokenizer,
                },
                {
                    "name": "Humanizador Profundo",
                    "path": config.HUMANIZADOR_PROFUNDO,
                    "model_class": T5ForConditionalGeneration,
                    "tokenizer_class": AutoTokenizer,
                },
                {
                    "name": "Avaliador de Alucinacao",
                    "path": config.HALLUCINATION_EVALUATION_MODEL,
                    "model_class": AutoModelForSequenceClassification,
                    "tokenizer_class": AutoTokenizer,
                },
            ]

            total_models = len(models_to_load)

            for i, model_info in enumerate(models_to_load):
                progress = (i + 1) / total_models
                self._report_status(f"Carregando {model_info['name']}...", progress)

                load_model_and_tokenizer(
                    model_name_or_path=str(model_info["path"]),
                    model_class=model_info["model_class"],
                    tokenizer_class=model_info["tokenizer_class"],
                    device=self.device,
                    hf_home=self.hf_home,
                    task_name=str(model_info["name"]),
                )

            self._report_status("Todos os modelos carregados.", 1.0)

        except Exception as e:
            self._report_status(f"Erro inesperado no ModelLoader: {e}", 0.9)


# "A excelencia nao e um ato, mas um habito." - Aristoteles
