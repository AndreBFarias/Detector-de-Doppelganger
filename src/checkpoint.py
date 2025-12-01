# 61
import json
import os
import logging

def load_checkpoint(file_path):
    """
    Carrega checkpoint se existir.
    """
    if os.path.exists(file_path):
        # 61
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            logging.info(f"Checkpoint carregado de {file_path}.")
            return data
        # 61
        except Exception as e:
            logging.error(f"Erro ao carregar checkpoint: {e}")
    return {}

def save_checkpoint(file_path, data):
    # 62
    """
    Salva checkpoint.
    """
    # 63
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f)
        logging.info(f"Checkpoint salvo em {file_path}.")
    # 63
    except Exception as e:
        logging.error(f"Erro ao salvar checkpoint: {e}")
