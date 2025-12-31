from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

import config
from src.core.config_loader import load_config


class AppCore:
    detector: Any
    naturalness_evaluator: Any
    humanizer_tokenizer: Any
    humanizer_model: Any
    current_humanizer_name: str | None
    styles: dict[str, Any]
    modelos: dict[str, str]

    def __init__(self) -> None:
        self.detector = None
        self.naturalness_evaluator = None
        self.humanizer_tokenizer = None
        self.humanizer_model = None
        self.current_humanizer_name = None
        self.styles = {}
        self.modelos = config.HUMANIZADOR_MAP

    def load_styles(self) -> list[str]:
        try:
            cfg = load_config()
            self.styles = cfg.get("styles", {})
            logging.info(f"Estilos de saida carregados: {list(self.styles.keys())}")
            return list(self.styles.keys())
        except Exception as e:
            logging.error(f"Falha ao carregar estilos do prompts.json: {e}", exc_info=True)
            self.styles = {"default": {"style": "informal"}}
            return ["default"]

    def get_style_info(self, style_key: str) -> dict[str, Any]:
        return self.styles.get(style_key, {})

    def load_detector_models(self) -> bool:
        try:
            logging.info(f"Carregando modelo detector: {config.DETECTOR_MODEL}")
            self.detector = pipeline("text-classification", model=config.DETECTOR_MODEL, device=-1)
            logging.info("Modelo detector carregado com sucesso.")

            logging.info(f"Carregando modelo avaliador: {config.HALLUCINATION_EVALUATION_MODEL}")
            self.naturalness_evaluator = pipeline(
                "text-classification", model=config.HALLUCINATION_EVALUATION_MODEL, device=-1
            )
            logging.info("Modelo avaliador carregado com sucesso.")

            return True
        except Exception as e:
            logging.error(f"Falha ao carregar modelos de deteccao/avaliacao: {e}", exc_info=True)
            return False

    def load_humanizer_model(self, model_key: str = "Equilibrado (CPU)") -> bool:
        model_name = self.modelos.get(model_key)
        if not model_name:
            logging.error(f"Chave de modelo invalida: {model_key}")
            return False

        if self.current_humanizer_name == model_name and self.humanizer_model is not None:
            logging.info(f"Modelo humanizador '{model_name}' ja esta carregado.")
            return True

        try:
            logging.info(f"Carregando modelo humanizador: {model_name}")
            logging.debug(f"Tentando carregar tokenizer e model de: {model_name}")

            self.humanizer_tokenizer = AutoTokenizer.from_pretrained(model_name)

            if "gpt" in model_name.lower():
                self.humanizer_model = AutoModelForCausalLM.from_pretrained(model_name, device_map="cpu")
            else:
                self.humanizer_model = AutoModelForSeq2SeqLM.from_pretrained(model_name, device_map="cpu")

            self.humanizer_model.eval()
            self.current_humanizer_name = model_name
            logging.info(f"Modelo humanizador '{model_name}' carregado com sucesso.")
            logging.debug(f"Modelo atual definido como: {self.current_humanizer_name}")
            return True
        except Exception as e:
            logging.error(f"Falha ao carregar modelo humanizador '{model_name}': {e}", exc_info=True)
            return False


# "A simplicidade e a sofisticacao suprema." - Leonardo da Vinci
