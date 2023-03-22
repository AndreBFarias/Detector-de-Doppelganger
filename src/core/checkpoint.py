from __future__ import annotations

import json
import logging
import os
from typing import Any


def load_checkpoint(file_path: str) -> dict[str, Any]:
    if os.path.exists(file_path):
        try:
            with open(file_path) as f:
                data = json.load(f)
            logging.info(f"Checkpoint carregado de {file_path}.")
            return data
        except Exception as e:
            logging.error(f"Erro ao carregar checkpoint: {e}")
    return {}


def save_checkpoint(file_path: str, data: dict[str, Any]) -> None:
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f)
        logging.info(f"Checkpoint salvo em {file_path}.")
    except Exception as e:
        logging.error(f"Erro ao salvar checkpoint: {e}")


# "A persistencia e o caminho do exito." - Charles Chaplin
