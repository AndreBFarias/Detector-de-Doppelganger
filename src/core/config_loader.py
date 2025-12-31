from __future__ import annotations

import json
import logging
import os
from typing import Any

from dotenv import load_dotenv


def load_config() -> dict[str, Any]:
    project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    env_path = os.path.join(project_root, ".env")
    prompts_path = os.path.join(project_root, "prompts.json")

    if os.path.exists(env_path):
        load_dotenv(env_path)
        hf_key = os.getenv("HF_KEY")
        logging.info("Chave HF carregada do .env.")
    else:
        hf_key = None
        logging.warning("Arquivo .env não encontrado.")

    styles = {}
    if os.path.exists(prompts_path):
        with open(prompts_path) as f:
            styles = json.load(f)
        logging.info("Estilos carregados de prompts.json.")
    else:
        styles = {"default": {"style": "informal", "example": "Fala aí, bicho!"}}
        logging.warning("prompts.json não encontrado. Usando estilo padrão.")

    return {"hf_key": hf_key, "styles": styles}


if __name__ == "__main__":
    config = load_config()
    print(config)


# "Conhece-te a ti mesmo." - Oraculo de Delfos
