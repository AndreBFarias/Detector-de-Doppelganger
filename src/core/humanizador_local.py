from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import torch
from transformers import AutoTokenizer, PreTrainedModel, PreTrainedTokenizer, T5ForConditionalGeneration

import config
from src.core.adversarial import humanizar_adversarial

logger = logging.getLogger(__name__)


class HumanizerLocal:
    _instance: HumanizerLocal | None = None
    _model: PreTrainedModel | None = None
    _tokenizer: PreTrainedTokenizer | None = None
    _model_name: str | None = None
    _device: torch.device | None = None

    def __new__(cls) -> HumanizerLocal:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._device is None:
            self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"HumanizerLocal usando device: {self._device}")

    def load_model(self, model_name: str) -> bool:
        if self._model_name == model_name and self._model is not None:
            logger.info(f"Modelo {model_name} ja carregado.")
            return True

        logger.info(f"Carregando modelo humanizador: {model_name}")

        try:
            self._tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                cache_dir=str(config.HF_HOME),
            )
            self._model = T5ForConditionalGeneration.from_pretrained(
                model_name,
                cache_dir=str(config.HF_HOME),
            ).to(self._device)
            self._model_name = model_name
            logger.info(f"Modelo {model_name} carregado com sucesso.")
            return True

        except Exception as e:
            logger.error(f"Falha ao carregar modelo {model_name}: {e}")
            self._model = None
            self._tokenizer = None
            return False

    def humanize(
        self,
        texto: str,
        num_beams: int = 5,
        temperature: float = 0.9,
        use_adversarial: bool = True,
    ) -> str:
        if not texto.strip():
            return texto

        resultado = texto

        if self._model is not None and self._tokenizer is not None:
            resultado = self._paraphrase(resultado, num_beams, temperature)

        if use_adversarial:
            resultado = humanizar_adversarial(resultado)

        return resultado

    def _paraphrase(self, texto: str, num_beams: int, temperature: float) -> str:
        try:
            input_text = f"paraphrase: {texto}"

            inputs = self._tokenizer(  # type: ignore[misc]
                input_text,
                return_tensors="pt",
                max_length=512,
                truncation=True,
                padding=True,
            ).to(self._device)

            with torch.no_grad():
                outputs = self._model.generate(  # type: ignore[union-attr]
                    **inputs,
                    max_length=512,
                    num_beams=num_beams,
                    temperature=temperature,
                    do_sample=True,
                    top_k=50,
                    top_p=0.95,
                    early_stopping=True,
                )

            resultado = self._tokenizer.decode(outputs[0], skip_special_tokens=True)  # type: ignore[union-attr]

            if len(resultado.strip()) < len(texto.strip()) * 0.3:
                logger.warning("Saida do modelo muito curta, retornando original.")
                return texto

            return resultado

        except Exception as e:
            logger.error(f"Falha na parafrase: {e}")
            return texto

    def get_model_name(self) -> str:
        return self._model_name or "Nao carregado"


def get_humanizer() -> HumanizerLocal:
    return HumanizerLocal()


def humanizar_local(
    texto: str,
    model_name: str | None = None,
    num_beams: int = 5,
    temperature: float = 0.9,
    use_adversarial: bool = True,
) -> str:
    humanizer = get_humanizer()

    if model_name:
        humanizer.load_model(model_name)
    elif humanizer._model is None:
        humanizer.load_model(config.HUMANIZADOR_EQUILIBRADO)

    return humanizer.humanize(texto, num_beams, temperature, use_adversarial)


# "A perfeicao nao e alcancavel, mas se perseguirmos a perfeicao, podemos alcancar a excelencia." - Vince Lombardi
