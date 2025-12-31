from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import re

from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer

import config

if TYPE_CHECKING:
    from transformers import PreTrainedModel, PreTrainedTokenizer


@dataclass
class HumanizadorConfig:
    modelo: str
    temperatura: float = 0.8
    num_beams: int = 5
    max_length_mult: float = 1.8
    min_length_mult: float = 0.8


class HumanizadorCache:
    _instance: HumanizadorCache | None = None
    tokenizer: PreTrainedTokenizer | None
    model: PreTrainedModel | None
    current_name: str | None

    def __new__(cls) -> HumanizadorCache:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.tokenizer = None
            cls._instance.model = None
            cls._instance.current_name = None
        return cls._instance

    def get(self) -> tuple[PreTrainedModel | None, PreTrainedTokenizer | None, str | None]:
        return self.model, self.tokenizer, self.current_name

    def set(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer, name: str) -> None:
        self.model = model
        self.tokenizer = tokenizer
        self.current_name = name

    def clear(self) -> None:
        self.tokenizer = None
        self.model = None
        self.current_name = None


_cache = HumanizadorCache()


def carregar_modelo_humanizador(model_key: str = "Equilibrado (CPU)") -> tuple:
    model_name = config.get_model_path(model_key)
    if not model_name:
        logging.error(f"Chave de modelo humanizador invalida: {model_key}")
        return None, None

    cached_model, cached_tokenizer, cached_name = _cache.get()
    if cached_name == model_name and cached_model is not None:
        logging.info(f"Usando modelo humanizador '{model_name}' do cache.")
        return cached_model, cached_tokenizer

    logging.info(f"Carregando novo modelo humanizador: {model_name}")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        if "gpt" in model_name.lower():
            model = AutoModelForCausalLM.from_pretrained(model_name, device_map="cpu")
        else:
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name, device_map="cpu")

        model.eval()
        _cache.set(model, tokenizer, model_name)

        logging.info(f"Modelo humanizador '{model_name}' carregado com sucesso.")
        return model, tokenizer

    except Exception as e:
        logging.error(f"Falha ao carregar modelo humanizador '{model_name}': {e}", exc_info=True)
        _cache.clear()
        return None, None


def humanizar_texto(
    texto: str,
    model: PreTrainedModel | None,
    tokenizer: PreTrainedTokenizer | None,
    device: str = "cpu",
    prompt_info: dict | None = None,
    num_beams: int = 5,
    temperature: float = 0.9,
) -> str:
    if not texto.strip():
        logging.warning("humanizar_texto chamado com texto vazio.")
        return "Texto vazio"

    if model is None or tokenizer is None:
        logging.error("Modelo ou Tokenizer de humanizacao nao fornecidos.")
        return "Erro: Humanizador nao carregado"

    try:
        if prompt_info is None:
            prompt_info = {}

        max_length_mult = prompt_info.get("max_length_multiplier", 1.8)
        min_length_mult = prompt_info.get("min_length_multiplier", 0.8)

        prompt_final = f"Parafrase: {texto}"
        inputs = tokenizer(prompt_final, return_tensors="pt", truncation=True, max_length=1024).to(device)

        input_length = inputs.input_ids.shape[1]
        max_len = max(50, int(input_length * max_length_mult))
        min_len = max(20, int(input_length * min_length_mult))

        logging.info(
            f"Gerando texto humanizado (PTT5). Input_len: {input_length}, Min_len: {min_len}, Max_len: {max_len}"
        )

        outputs = model.generate(
            **inputs,
            max_length=max_len,
            min_length=min_len,
            num_beams=num_beams,
            early_stopping=True,
            temperature=0.8,
            top_k=50,
            top_p=0.95,
            no_repeat_ngram_size=3,
            repetition_penalty=1.2,
        )

        texto_humanizado = tokenizer.decode(outputs[0], skip_special_tokens=True)
        logging.info(f"RAW OUTPUT: {texto_humanizado}")

        pattern = r"(?:Parafrase|Paráfrase|Reescreva).*?[:\s]*"
        texto_humanizado = re.sub(pattern, "", texto_humanizado, flags=re.IGNORECASE).strip()
        texto_humanizado = texto_humanizado.lstrip(": ")
        texto_humanizado = texto_humanizado.strip("\"' ")

        logging.info("Texto humanizado gerado com sucesso.")
        return texto_humanizado

    except Exception as e:
        logging.error(f"Falha ao gerar texto humanizado: {e}", exc_info=True)
        return f"Erro durante a humanizacao: {e}"


# "O homem que move montanhas comeca carregando pequenas pedras." - Confucio
