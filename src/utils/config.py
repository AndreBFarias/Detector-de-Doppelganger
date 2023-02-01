# 64
import os

class Config:
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ASSETS_DIR = os.path.join(BASE_DIR, "assets")
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    BG_COLOR = "#282A36"
    FRAME_COLOR = "#44475A"
    ACCENT_GREEN = "#50FA7B"
    ACCENT_PINK = "#FF79C6"
    ACCENT_PURPLE = "#BD93F9"
    TEXT_COLOR = "#F8F8F2"
    PLACEHOLDER_TEXT_COLOR = "#6272A4"

    # Modelos de Humanização (PTT5 - Unicamp)
    HUMANIZADOR_LEVE = "unicamp-dl/ptt5-small-portuguese-vocab"
    HUMANIZADOR_EQUILIBRADO = "unicamp-dl/ptt5-base-portuguese-vocab"
    HUMANIZADOR_PROFUNDO = "unicamp-dl/ptt5-large-portuguese-vocab"
    DETECTOR_MODEL = "roberta-base-openai-detector"
    HALLUCINATION_EVALUATION_MODEL = "roberta-base-openai-detector"
