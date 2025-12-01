import logging
import os
import sys

def setup_logger(log_file="debug.log", level=logging.DEBUG):
    """
    Configura um logger robusto que grava em arquivo e console.
    """
    # Cria o formatador
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Handler de Arquivo
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    
    # Handler de Console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO) # Console menos verboso
    
    # Configuração do Root Logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Limpa handlers anteriores para evitar duplicidade
    if logger.hasHandlers():
        logger.handlers.clear()
        
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logging.info(f"Logger inicializado. Gravando em: {os.path.abspath(log_file)}")
