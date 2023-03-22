from __future__ import annotations

import logging
import os
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import config
from src.core.logging_config import get_logger, setup_logging


def _suppress_library_warnings() -> None:
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"


def _setup_environment() -> None:
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    os.environ["HF_HOME"] = str(config.HF_HOME)

    if config.HF_TOKEN:
        os.environ["HF_TOKEN"] = config.HF_TOKEN


def _verify_assets(logger: logging.Logger) -> str | None:
    icon_path = config.ASSETS_DIR / "icon.png"
    if not icon_path.exists():
        return f"Asset nao encontrado: {icon_path}"

    theme_path = config.THEME_PATH
    if not theme_path.exists():
        return f"Tema nao encontrado: {theme_path}"

    return None


def _setup_customtkinter(logger: logging.Logger) -> None:
    import customtkinter

    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme(str(config.THEME_PATH))
    logger.info("CustomTkinter configurado com tema Dark")


def initialize_application() -> tuple[logging.Logger, str | None]:
    _suppress_library_warnings()
    _setup_environment()

    setup_logging(level="INFO", log_to_file=True, log_to_console=True)
    logger = get_logger("doppelganger")

    logger.info("=" * 60)
    logger.info("Inicializando Detector de Doppelganger...")
    logger.info(f"Diretorio: {config.APP_DIR}")
    logger.info(f"Logs: {config.LOGS_DIR}")
    logger.info("=" * 60)

    error = _verify_assets(logger)
    if error:
        return logger, error

    _setup_customtkinter(logger)

    return logger, None
