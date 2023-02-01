# 32
from dotenv import load_dotenv
import os
import json
import logging

def load_config():
    """
    Carrega chaves do .env e estilos de prompts.json.
    """
    config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    env_path = os.path.join(config_dir, '.env')
    prompts_path = os.path.join(config_dir, 'prompts.json')

    # 33
    # Carrega .env
    if os.path.exists(env_path):
        load_dotenv(env_path)
        hf_key = os.getenv("HF_KEY")
        logging.info("Chave HF carregada do .env.")
    else:
        hf_key = None
        logging.warning("Arquivo .env não encontrado.")

    # 34
    # Carrega prompts.json
    styles = {}
    if os.path.exists(prompts_path):
        with open(prompts_path, 'r') as f:
            styles = json.load(f)
        logging.info("Estilos carregados de prompts.json.")
    else:
        styles = {"default": {"style": "informal", "example": "Fala aí, bicho!"}}  # Fallback
        logging.warning("prompts.json não encontrado. Usando estilo padrão.")

    # 35
    return {"hf_key": hf_key, "styles": styles}

if __name__ == "__main__":
    config = load_config()
    print(config)
