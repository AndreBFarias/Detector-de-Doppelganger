from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import config

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s"
LOG_DIR = config.LOGS_DIR

_initialized = False


def setup_logging(level: str = "INFO", log_to_file: bool = True, log_to_console: bool = True) -> None:
    global _initialized
    if _initialized:
        return

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    if root.hasHandlers():
        root.handlers.clear()

    formatter = logging.Formatter(LOG_FORMAT)

    if log_to_console:
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(getattr(logging, level))
        console.setFormatter(formatter)
        root.addHandler(console)

    if log_to_file:
        LOG_DIR.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            LOG_DIR / "doppelganger.log", maxBytes=10_000_000, backupCount=5, encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

        error_handler = RotatingFileHandler(
            LOG_DIR / "doppelganger_errors.log", maxBytes=5_000_000, backupCount=3, encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        root.addHandler(error_handler)

    _silence_noisy_loggers()
    _initialized = True

    logging.info(f"Logger inicializado. Logs em: {LOG_DIR}")


def _silence_noisy_loggers() -> None:
    noisy = [
        "PIL.PngImagePlugin",
        "PIL.Image",
        "urllib3",
        "transformers",
        "torch",
        "filelock",
        "huggingface_hub",
        "httpx",
        "httpcore",
    ]
    for name in noisy:
        logging.getLogger(name).setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
