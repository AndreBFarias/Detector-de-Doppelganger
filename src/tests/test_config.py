from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import config


class TestConfig:
    def test_app_dir_exists(self) -> None:
        assert config.APP_DIR.exists()

    def test_src_dir_exists(self) -> None:
        assert config.SRC_DIR.exists()

    def test_assets_dir_exists(self) -> None:
        assert config.ASSETS_DIR.exists()

    def test_detector_model_defined(self) -> None:
        assert config.DETECTOR_MODEL is not None
        assert isinstance(config.DETECTOR_MODEL, str)

    def test_humanizador_map_has_keys(self) -> None:
        assert "Leve (CPU)" in config.HUMANIZADOR_MAP
        assert "Equilibrado (CPU)" in config.HUMANIZADOR_MAP
        assert "Profundo (CPU)" in config.HUMANIZADOR_MAP

    def test_get_model_path_valid(self) -> None:
        path = config.get_model_path("Equilibrado (CPU)")
        assert path is not None
        assert "ptt5" in path.lower()

    def test_get_model_path_invalid(self) -> None:
        path = config.get_model_path("Modelo Inexistente")
        assert path is None

    def test_colors_defined(self) -> None:
        assert config.BG_COLOR is not None
        assert config.ACCENT_GREEN is not None
        assert config.ACCENT_PURPLE is not None
        assert config.ACCENT_PINK is not None


# "A configuracao e a base de todo sistema robusto." - Desconhecido
