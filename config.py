from __future__ import annotations

import os
import pathlib

from dotenv import load_dotenv

_env_path = pathlib.Path(__file__).parent / ".env"
load_dotenv(_env_path, override=True)

APP_DIR = pathlib.Path(__file__).parent.resolve()
SRC_DIR = APP_DIR / "src"
ASSETS_DIR = APP_DIR / "assets"
LOGS_DIR = SRC_DIR / "logs"
DATA_DIR = APP_DIR / "data"
TEMP_DIR = SRC_DIR / "temp"
MODELS_DIR = APP_DIR / "models"

HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_HOME = MODELS_DIR / "cache"

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 1100
WINDOW_MIN_HEIGHT = 700

DETECTOR_MODEL_BASE = "roberta-base-openai-detector"
DETECTOR_MODEL_LARGE = "roberta-large-openai-detector"
DETECTOR_MODEL = DETECTOR_MODEL_LARGE

HUMANIZADOR_LEVE = "unicamp-dl/ptt5-small-portuguese-vocab"
HUMANIZADOR_EQUILIBRADO = "unicamp-dl/ptt5-base-portuguese-vocab"
HUMANIZADOR_PROFUNDO = "unicamp-dl/ptt5-large-portuguese-vocab"
HALLUCINATION_EVALUATION_MODEL = "roberta-base-openai-detector"

HUMANIZADOR_MAP = {
    "Leve (CPU)": HUMANIZADOR_LEVE,
    "Equilibrado (CPU)": HUMANIZADOR_EQUILIBRADO,
    "Profundo (CPU)": HUMANIZADOR_PROFUNDO,
}

DETECTOR_MODE = os.getenv("DETECTOR_MODE", "local")
HUMANIZER_MODE = os.getenv("HUMANIZER_MODE", "api")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_RATE_LIMIT = 14400

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.0-flash"

MAX_ITERATIONS = 5
TARGET_SCORE = 0.3
EPSILON = 0.001
DEFAULT_NUM_BEAMS = 5
DEFAULT_TEMPERATURE = 0.9

ADVERSARIAL_SYNONYM_RATE = 0.30
ADVERSARIAL_ENTROPY_FACTOR = 1.2

COLORS = {
    "background": "#181825",
    "bg": "#282A36",
    "frame": "#44475A",
    "green": "#50FA7B",
    "pink": "#FF79C6",
    "purple": "#BD93F9",
    "cyan": "#8BE9FD",
    "orange": "#FFB86C",
    "yellow": "#F1FA8C",
    "red": "#FF5555",
    "text": "#F8F8F2",
    "placeholder": "#6272A4",
    "input_bg": "#1e1e2e",
    "input_border": "#6272A4",
    "output_bg": "#1a1a2e",
    "output_border": "#50FA7B",
}

BG_COLOR = COLORS["bg"]
FRAME_COLOR = COLORS["frame"]
ACCENT_GREEN = COLORS["green"]
ACCENT_PINK = COLORS["pink"]
ACCENT_PURPLE = COLORS["purple"]
ACCENT_CYAN = COLORS["cyan"]
ACCENT_ORANGE = COLORS["orange"]
TEXT_COLOR = COLORS["text"]
PLACEHOLDER_TEXT_COLOR = COLORS["placeholder"]

INPUT_BG = COLORS["input_bg"]
INPUT_BORDER = COLORS["input_border"]
OUTPUT_BG = COLORS["output_bg"]
OUTPUT_BORDER = COLORS["output_border"]

THEME_PATH = SRC_DIR / "utils" / "ctk_theme.json"
PROMPTS_PATH = APP_DIR / "prompts.json"

os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(DATA_DIR / "input", exist_ok=True)
os.makedirs(DATA_DIR / "output", exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(HF_HOME, exist_ok=True)


def get_model_path(model_key: str) -> str | None:
    return HUMANIZADOR_MAP.get(model_key)


def get_assets_path(filename: str) -> pathlib.Path:
    return ASSETS_DIR / filename


# "Simplicidade e a sofisticacao suprema." - Leonardo da Vinci
