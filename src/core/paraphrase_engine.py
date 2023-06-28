from __future__ import annotations

import logging
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, MarianMTModel, MarianTokenizer

import config

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434"
OLLAMA_DEFAULT_MODEL = "llama3.2:3b"

TRANSLATION_MODELS = {
    "pt_en": "Helsinki-NLP/opus-mt-roa-en",
    "en_pt": "Helsinki-NLP/opus-mt-tc-big-en-pt",
}

PARAPHRASE_MODELS = {
    "quora_small": "mrm8488/t5-small-finetuned-quora-for-paraphrasing",
    "paws": "Vamsi/T5_Paraphrase_Paws",
    "chatgpt_style": "humarin/chatgpt_paraphraser_on_T5_base",
}

DEFAULT_MODEL = "quora_small"


@dataclass
class ParaphraseCandidate:
    text: str
    score: float = 0.0
    model_name: str = ""


class BackTranslationEngine:
    _instance: BackTranslationEngine | None = None
    _pt_en_model: MarianMTModel | None = None
    _pt_en_tokenizer: MarianTokenizer | None = None
    _en_pt_model: MarianMTModel | None = None
    _en_pt_tokenizer: MarianTokenizer | None = None
    _device: torch.device | None = None
    _loaded: bool = False

    def __new__(cls) -> BackTranslationEngine:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._device is None:
            self._device = torch.device("cpu")
            logger.info("BackTranslationEngine inicializado (CPU only para economia de memoria)")

    def load_models(self) -> bool:
        if self._loaded:
            return True

        logger.info("Carregando modelos de traducao para back-translation...")

        try:
            self._pt_en_tokenizer = MarianTokenizer.from_pretrained(
                TRANSLATION_MODELS["pt_en"],
                cache_dir=str(config.HF_HOME),
            )
            self._pt_en_model = MarianMTModel.from_pretrained(
                TRANSLATION_MODELS["pt_en"],
                cache_dir=str(config.HF_HOME),
            ).to(self._device)

            self._en_pt_tokenizer = MarianTokenizer.from_pretrained(
                TRANSLATION_MODELS["en_pt"],
                cache_dir=str(config.HF_HOME),
            )
            self._en_pt_model = MarianMTModel.from_pretrained(
                TRANSLATION_MODELS["en_pt"],
                cache_dir=str(config.HF_HOME),
            ).to(self._device)

            self._loaded = True
            logger.info("Modelos de traducao carregados com sucesso.")
            return True

        except Exception as e:
            logger.error(f"Falha ao carregar modelos de traducao: {e}")
            return False

    def unload_models(self) -> None:
        if self._pt_en_model is not None:
            del self._pt_en_model
            self._pt_en_model = None
        if self._pt_en_tokenizer is not None:
            del self._pt_en_tokenizer
            self._pt_en_tokenizer = None
        if self._en_pt_model is not None:
            del self._en_pt_model
            self._en_pt_model = None
        if self._en_pt_tokenizer is not None:
            del self._en_pt_tokenizer
            self._en_pt_tokenizer = None

        self._loaded = False

        import gc

        gc.collect()
        logger.info("Modelos de traducao descarregados.")

    def _translate(
        self,
        text: str,
        model: MarianMTModel,
        tokenizer: MarianTokenizer,
        num_beams: int = 4,
        num_return: int = 1,
        target_lang_prefix: str = "",
    ) -> list[str]:
        if target_lang_prefix:
            text = f"{target_lang_prefix} {text}"

        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        inputs = {k: v.to(self._device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                num_beams=num_beams,
                num_return_sequences=num_return,
                max_length=512,
                early_stopping=True,
            )

        return [tokenizer.decode(out, skip_special_tokens=True) for out in outputs]

    def back_translate(
        self,
        texto: str,
        num_candidates: int = 3,
    ) -> list[ParaphraseCandidate]:
        if not texto.strip():
            return [ParaphraseCandidate(text=texto)]

        if not self._loaded:
            if not self.load_models():
                return [ParaphraseCandidate(text=texto)]

        try:
            en_versions = self._translate(
                texto,
                self._pt_en_model,
                self._pt_en_tokenizer,
                num_beams=num_candidates * 2,
                num_return=num_candidates,
            )

            candidates = []
            seen = set()

            for en_text in en_versions:
                pt_versions = self._translate(
                    en_text,
                    self._en_pt_model,
                    self._en_pt_tokenizer,
                    num_beams=4,
                    num_return=2,
                    target_lang_prefix=">>por<<",
                )

                for pt_text in pt_versions:
                    pt_text = pt_text.strip()
                    if pt_text.lower() not in seen and pt_text.lower() != texto.lower():
                        seen.add(pt_text.lower())
                        candidates.append(
                            ParaphraseCandidate(
                                text=pt_text,
                                model_name="back_translation",
                            )
                        )

            if not candidates:
                candidates.append(ParaphraseCandidate(text=texto))

            return candidates[:num_candidates]

        except Exception as e:
            logger.error(f"Falha no back-translation: {e}", exc_info=True)
            return [ParaphraseCandidate(text=texto)]


class OllamaParaphraseEngine:
    _instance: OllamaParaphraseEngine | None = None

    def __new__(cls) -> OllamaParaphraseEngine:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._model = OLLAMA_DEFAULT_MODEL
        self._available: bool | None = None

    def is_available(self) -> bool:
        if self._available is not None:
            return self._available

        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
            self._available = response.status_code == 200
            if self._available:
                models = response.json().get("models", [])
                model_names = [m.get("name", "") for m in models]
                logger.info(f"Ollama disponivel. Modelos: {model_names}")
            return self._available
        except Exception as e:
            logger.warning(f"Ollama nao disponivel: {e}")
            self._available = False
            return False

    def set_model(self, model_name: str) -> None:
        self._model = model_name
        logger.info(f"Ollama model definido: {model_name}")

    def _build_prompt(self, texto: str, num_variants: int = 3, style: str = "default") -> str:
        if style == "casual":
            return f"""Reescreva o texto como se fosse uma pessoa normal falando. Seja informal, direto, use gírias se fizer sentido. Faça {num_variants} versões diferentes.

REGRAS:
- Escreva como gente de verdade escreve
- Frases curtas e longas misturadas
- Pode começar frase com "E", "Mas", "Aí"
- Menos palavras difíceis
- Numere: 1. 2. 3.
- SÓ as versões, nada mais

TEXTO:
{texto}

VERSOES:"""
        elif style == "humanize":
            return f"""Você é um escritor humano. Reescreva este texto de {num_variants} formas diferentes para parecer escrito por uma pessoa real, não por IA.

CARACTERÍSTICAS DE TEXTO HUMANO:
- Imperfeições naturais na estrutura
- Variação no tamanho das frases (algumas curtas, outras longas)
- Menos conectivos formais (evite "além disso", "portanto", "consequentemente")
- Repetições ocasionais são OK
- Comece algumas frases de forma inesperada
- Use voz ativa quando possível

IMPORTANTE:
- Numere cada versão (1., 2., 3.)
- Apenas as versões, sem explicações

TEXTO:
{texto}

VERSOES HUMANIZADAS:"""
        else:
            return f"""Reescreva o texto abaixo de {num_variants} formas diferentes, mantendo o mesmo significado.

REGRAS IMPORTANTES:
- Mude a estrutura das frases
- Use sinônimos naturais
- Varie o comprimento das frases
- Mantenha o tom e significado original
- Escreva APENAS as versões reescritas, uma por linha
- Numere cada versão (1., 2., 3.)
- NAO inclua explicações ou comentários

TEXTO ORIGINAL:
{texto}

VERSOES REESCRITAS:"""

    def _parse_response(self, response_text: str, original: str) -> list[str]:
        lines = response_text.strip().split("\n")
        candidates = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line[0].isdigit() and len(line) > 2 and line[1] in ".):":
                line = line[2:].strip()
            elif line.startswith("-"):
                line = line[1:].strip()

            if len(line) < 10:
                continue
            if line.lower() == original.lower():
                continue
            if "reescr" in line.lower() or "versão" in line.lower() or "texto" in line.lower():
                continue

            candidates.append(line)

        return candidates

    def generate_paraphrases(
        self,
        texto: str,
        num_candidates: int = 3,
        temperature: float = 0.8,
        style: str = "default",
    ) -> list[ParaphraseCandidate]:
        if not texto.strip():
            return [ParaphraseCandidate(text=texto)]

        if not self.is_available():
            logger.error("Ollama nao esta disponivel.")
            return [ParaphraseCandidate(text=texto)]

        prompt = self._build_prompt(texto, num_candidates, style=style)

        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": self._model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": 1024,
                    },
                },
                timeout=120,
            )

            if response.status_code != 200:
                logger.error(f"Ollama retornou status {response.status_code}")
                return [ParaphraseCandidate(text=texto)]

            result = response.json()
            response_text = result.get("response", "")

            logger.debug(f"Ollama response:\n{response_text}")

            parsed = self._parse_response(response_text, texto)

            candidates = []
            for text in parsed[:num_candidates]:
                candidates.append(
                    ParaphraseCandidate(
                        text=text,
                        model_name=f"ollama:{self._model}",
                    )
                )

            if not candidates:
                logger.warning("Ollama nao gerou candidatos validos.")
                candidates.append(ParaphraseCandidate(text=texto))

            return candidates

        except requests.exceptions.Timeout:
            logger.error("Timeout ao chamar Ollama.")
            return [ParaphraseCandidate(text=texto)]
        except Exception as e:
            logger.error(f"Falha na geracao via Ollama: {e}", exc_info=True)
            return [ParaphraseCandidate(text=texto)]

    def paraphrase_with_selection(
        self,
        texto: str,
        detector_fn: Callable[[str], tuple[float, str]],
        num_candidates: int = 5,
    ) -> tuple[str, float]:
        candidates = self.generate_paraphrases(texto, num_candidates=num_candidates)

        if len(candidates) == 1 and candidates[0].text == texto:
            score, _ = detector_fn(texto)
            return texto, score

        best_candidate = candidates[0]
        best_score = float("inf")

        for candidate in candidates:
            score, _ = detector_fn(candidate.text)
            candidate.score = score

            logger.debug(f"Candidato Ollama: score={score:.2%}, texto={candidate.text[:50]}...")

            if score < best_score:
                best_score = score
                best_candidate = candidate

        logger.info(f"Melhor parafrase Ollama: score={best_score:.2%} (de {len(candidates)} candidatos)")

        return best_candidate.text, best_score

    def iterative_paraphrase(
        self,
        texto: str,
        detector_fn: Callable[[str], tuple[float, str]],
        max_iterations: int = 3,
        num_candidates: int = 5,
        min_length_ratio: float = 0.5,
    ) -> tuple[str, float, int]:
        current_text = texto
        original_len = len(texto)
        score_orig, _ = detector_fn(texto)
        best_score = score_orig
        best_text = texto

        for iteration in range(max_iterations):
            candidates = self.generate_paraphrases(
                current_text,
                num_candidates=num_candidates,
                temperature=0.85,
                style="default",
            )

            improved = False
            for candidate in candidates:
                if len(candidate.text) < original_len * min_length_ratio:
                    continue

                score, _ = detector_fn(candidate.text)

                if score < best_score:
                    best_score = score
                    best_text = candidate.text
                    current_text = candidate.text
                    improved = True
                    logger.info(
                        f"Iteracao {iteration + 1}: score {score:.1%} " f"(len: {len(candidate.text)}/{original_len})"
                    )

            if not improved:
                logger.info(f"Sem melhoria na iteracao {iteration + 1}, parando.")
                break

        reducao = score_orig - best_score
        logger.info(
            f"Resultado iterativo: {score_orig:.1%} -> {best_score:.1%} "
            f"(reducao: {reducao:.1%}, {iteration + 1} iteracoes)"
        )

        return best_text, best_score, iteration + 1

    def aggressive_humanize(
        self,
        texto: str,
        detector_fn: Callable[[str], tuple[float, str]],
        target_reduction: float = 0.5,
        max_attempts: int = 20,
        min_length_ratio: float = 0.4,
        priority: str = "balanced",
    ) -> tuple[str, float, dict]:
        from src.core.adversarial import humanizar_adversarial

        if priority == "max_reduction":
            min_length_ratio = 0.2
            max_attempts = 30
        elif priority == "preserve_content":
            min_length_ratio = 0.6
            max_attempts = 15

        original_len = len(texto)
        score_orig, _ = detector_fn(texto)
        target_score = score_orig * (1 - target_reduction)

        stats: dict[str, Any] = {
            "attempts": 0,
            "candidates_tested": 0,
            "best_per_round": [],
            "priority": priority,
        }

        best_score = score_orig
        best_text = texto

        texto_adv = humanizar_adversarial(texto)
        score_adv, _ = detector_fn(texto_adv)
        if score_adv < best_score:
            best_score = score_adv
            best_text = texto_adv

        for attempt in range(max_attempts):
            stats["attempts"] = attempt + 1

            temp = 0.7 + (attempt % 5) * 0.1
            current = best_text if attempt % 2 == 0 else texto_adv

            candidates = self.generate_paraphrases(
                current,
                num_candidates=5,
                temperature=temp,
                style="default",
            )

            for c in candidates:
                stats["candidates_tested"] += 1

                if len(c.text) < original_len * min_length_ratio:
                    continue

                c_clean = humanizar_adversarial(c.text)
                score, _ = detector_fn(c_clean)

                if score < best_score:
                    best_score = score
                    best_text = c_clean
                    stats["best_per_round"].append({"attempt": attempt + 1, "score": score})

                    if score <= target_score:
                        logger.info(f"Meta atingida: {score:.1%} <= {target_score:.1%}")
                        return best_text, best_score, stats

        reducao = (score_orig - best_score) / score_orig
        logger.info(
            f"Humanizacao agressiva: {score_orig:.1%} -> {best_score:.1%} "
            f"({reducao:.1%} reducao, {stats['attempts']} tentativas)"
        )

        return best_text, best_score, stats


def get_ollama_engine() -> OllamaParaphraseEngine:
    return OllamaParaphraseEngine()


def ollama_paraphrase_text(
    texto: str,
    detector_fn: Callable[[str], tuple[float, str]] | None = None,
    num_candidates: int = 5,
    model: str = OLLAMA_DEFAULT_MODEL,
) -> str:
    engine = get_ollama_engine()
    engine.set_model(model)

    if detector_fn is not None:
        result, _ = engine.paraphrase_with_selection(texto, detector_fn, num_candidates)
        return result

    candidates = engine.generate_paraphrases(texto, num_candidates=1)
    return candidates[0].text if candidates else texto


class ParaphraseEngine:
    _instance: ParaphraseEngine | None = None
    _model: Any = None
    _tokenizer: Any = None
    _model_key: str | None = None
    _device: torch.device | None = None

    def __new__(cls) -> ParaphraseEngine:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._device is None:
            self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"ParaphraseEngine usando device: {self._device}")

    def unload_model(self) -> None:
        if self._model is not None:
            del self._model
            self._model = None
        if self._tokenizer is not None:
            del self._tokenizer
            self._tokenizer = None
        self._model_key = None

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

        import gc

        gc.collect()
        logger.info("Modelo de parafrase descarregado e memoria liberada.")

    def load_model(self, model_key: str = DEFAULT_MODEL, force_cpu: bool = False) -> bool:
        if self._model_key == model_key and self._model is not None:
            logger.info(f"Modelo {model_key} ja carregado.")
            return True

        self.unload_model()

        model_name = PARAPHRASE_MODELS.get(model_key, PARAPHRASE_MODELS[DEFAULT_MODEL])
        logger.info(f"Carregando modelo de parafrase: {model_name}")

        device = torch.device("cpu") if force_cpu else self._device

        try:
            self._tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                cache_dir=str(config.HF_HOME),
            )
            self._model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name,
                cache_dir=str(config.HF_HOME),
            ).to(device)
            self._model_key = model_key
            self._device = device
            logger.info(f"Modelo {model_name} carregado em {device}.")
            return True

        except torch.cuda.OutOfMemoryError:
            logger.warning(f"CUDA OOM ao carregar {model_name}, tentando CPU...")
            return self.load_model(model_key, force_cpu=True)

        except Exception as e:
            logger.error(f"Falha ao carregar modelo {model_name}: {e}")
            self._model = None
            self._tokenizer = None
            return False

    def generate_paraphrases(
        self,
        texto: str,
        num_candidates: int = 5,
        num_beams: int = 10,
        temperature: float = 1.5,
        max_length: int = 256,
    ) -> list[ParaphraseCandidate]:
        if not texto.strip():
            return [ParaphraseCandidate(text=texto)]

        if self._model is None or self._tokenizer is None:
            if not self.load_model():
                return [ParaphraseCandidate(text=texto)]

        try:
            input_text = f"paraphrase: {texto} </s>"

            inputs = self._tokenizer(
                input_text,
                return_tensors="pt",
                max_length=max_length,
                truncation=True,
                padding=True,
            ).to(self._device)

            with torch.no_grad():
                outputs = self._model.generate(
                    **inputs,
                    max_length=max_length,
                    num_beams=num_beams,
                    num_return_sequences=num_candidates,
                    temperature=temperature,
                    do_sample=True,
                    top_k=120,
                    top_p=0.95,
                    repetition_penalty=1.2,
                    length_penalty=1.0,
                    early_stopping=True,
                    no_repeat_ngram_size=2,
                )

            candidates = []
            for output in outputs:
                decoded = self._tokenizer.decode(output, skip_special_tokens=True)
                decoded = decoded.strip()

                if len(decoded) < len(texto) * 0.3:
                    continue

                if decoded.lower() == texto.lower():
                    continue

                candidates.append(
                    ParaphraseCandidate(
                        text=decoded,
                        model_name=self._model_key or DEFAULT_MODEL,
                    )
                )

            if not candidates:
                candidates.append(ParaphraseCandidate(text=texto))

            return candidates

        except Exception as e:
            logger.error(f"Falha na geracao de parafrases: {e}", exc_info=True)
            return [ParaphraseCandidate(text=texto)]

    def paraphrase_with_selection(
        self,
        texto: str,
        detector_fn: Callable[[str], tuple[float, str]],
        num_candidates: int = 5,
    ) -> tuple[str, float]:
        candidates = self.generate_paraphrases(texto, num_candidates=num_candidates)

        if len(candidates) == 1 and candidates[0].text == texto:
            score, _ = detector_fn(texto)
            return texto, score

        best_candidate = candidates[0]
        best_score = float("inf")

        for candidate in candidates:
            score, _ = detector_fn(candidate.text)
            candidate.score = score

            logger.debug(f"Candidato: score={score:.2%}, texto={candidate.text[:50]}...")

            if score < best_score:
                best_score = score
                best_candidate = candidate

        logger.info(f"Melhor parafrase: score={best_score:.2%} (de {len(candidates)} candidatos)")

        return best_candidate.text, best_score


def get_paraphrase_engine() -> ParaphraseEngine:
    return ParaphraseEngine()


def get_back_translation_engine() -> BackTranslationEngine:
    return BackTranslationEngine()


def paraphrase_text(
    texto: str,
    detector_fn: Callable[[str], tuple[float, str]] | None = None,
    num_candidates: int = 5,
    model_key: str = DEFAULT_MODEL,
) -> str:
    engine = get_paraphrase_engine()
    engine.load_model(model_key)

    if detector_fn is not None:
        result, _ = engine.paraphrase_with_selection(texto, detector_fn, num_candidates)
        return result

    candidates = engine.generate_paraphrases(texto, num_candidates=1)
    return candidates[0].text if candidates else texto


def back_translate_text(
    texto: str,
    num_candidates: int = 3,
) -> list[ParaphraseCandidate]:
    engine = get_back_translation_engine()
    return engine.back_translate(texto, num_candidates)


def back_translate_with_selection(
    texto: str,
    detector_fn: Callable[[str], tuple[float, str]],
    num_candidates: int = 3,
) -> tuple[str, float]:
    candidates = back_translate_text(texto, num_candidates)

    if len(candidates) == 1 and candidates[0].text == texto:
        score, _ = detector_fn(texto)
        return texto, score

    best_candidate = candidates[0]
    best_score = float("inf")

    for candidate in candidates:
        score, _ = detector_fn(candidate.text)
        candidate.score = score

        logger.debug(f"Candidato BT: score={score:.2%}, texto={candidate.text[:50]}...")

        if score < best_score:
            best_score = score
            best_candidate = candidate

    logger.info(f"Melhor back-translation: score={best_score:.2%} (de {len(candidates)} candidatos)")

    return best_candidate.text, best_score


# "A arte de escrever e reescrever ate que as palavras dancem." - Autor Desconhecido
