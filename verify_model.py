#!/usr/bin/env python3
from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from transformers import pipeline

import config

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def test_detector_model() -> bool:
    logger.info(f"Testando modelo detector: {config.DETECTOR_MODEL}")
    try:
        pipe = pipeline("text-classification", model=config.DETECTOR_MODEL, device=-1)

        human_text = "O sol brilha forte nesta manha de verao."
        ai_text = "Como um modelo de linguagem, eu nao tenho capacidade de sentir emocoes."

        res_human = pipe(human_text)[0]
        res_ai = pipe(ai_text)[0]

        logger.info(f"Texto humano: {res_human}")
        logger.info(f"Texto IA: {res_ai}")

        return True
    except Exception as e:
        logger.error(f"Falha ao testar detector: {e}")
        return False


def test_humanizer_models() -> bool:
    logger.info("Testando modelos humanizadores...")
    try:
        from transformers import AutoTokenizer

        for name, path in config.HUMANIZADOR_MAP.items():
            logger.info(f"Verificando {name}: {path}")
            tokenizer = AutoTokenizer.from_pretrained(path)
            logger.info(f"  Tokenizer OK: {tokenizer.__class__.__name__}")

        return True
    except Exception as e:
        logger.error(f"Falha ao testar humanizadores: {e}")
        return False


def main() -> int:
    logger.info("=" * 60)
    logger.info("Verificacao de Modelos - Detector de Doppelganger")
    logger.info("=" * 60)

    results = []

    results.append(("Detector", test_detector_model()))
    results.append(("Humanizadores", test_humanizer_models()))

    logger.info("=" * 60)
    logger.info("Resultados:")
    for name, passed in results:
        status = "OK" if passed else "FALHOU"
        logger.info(f"  {name}: {status}")

    all_passed = all(r[1] for r in results)
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())


# "Confie, mas verifique." - Proverbio Russo
