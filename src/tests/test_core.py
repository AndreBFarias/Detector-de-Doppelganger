from __future__ import annotations

import json
import os
import tempfile

from src.core.checkpoint import load_checkpoint, save_checkpoint
from src.core.config_loader import load_config
from src.core.naturalness_evaluator import avaliar_naturalidade
from src.core.output_formatter import save_output


class TestNaturalnessEvaluator:
    def test_avaliar_texto_vazio(self) -> None:
        resultado = avaliar_naturalidade("", None)
        assert resultado == 0.0

    def test_avaliar_sem_avaliador(self) -> None:
        resultado = avaliar_naturalidade("Texto de teste", None)
        assert resultado == 0.0


class TestCheckpoint:
    def test_load_checkpoint_arquivo_inexistente(self) -> None:
        resultado = load_checkpoint("/caminho/inexistente/arquivo.json")
        assert resultado == {}

    def test_save_and_load_checkpoint(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            data = {"key": "value", "number": 42}
            save_checkpoint(temp_path, data)
            loaded = load_checkpoint(temp_path)
            assert loaded == data
        finally:
            os.unlink(temp_path)


class TestOutputFormatter:
    def test_save_txt(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            temp_path = f.name

        try:
            save_output("Texto de teste", temp_path)
            with open(temp_path) as f:
                content = f.read()
            assert content == "Texto de teste"
        finally:
            os.unlink(temp_path)

    def test_save_json(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            save_output("Texto de teste", temp_path, style="formal")
            with open(temp_path) as f:
                data = json.load(f)
            assert data["content"] == "Texto de teste"
            assert data["style"] == "formal"
        finally:
            os.unlink(temp_path)

    def test_save_md(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            temp_path = f.name

        try:
            save_output("Texto de teste", temp_path)
            with open(temp_path) as f:
                content = f.read()
            assert content == "Texto de teste"
        finally:
            os.unlink(temp_path)

    def test_save_md_bullets(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            temp_path = f.name

        try:
            save_output("Linha 1\nLinha 2", temp_path, style="bullets")
            with open(temp_path) as f:
                content = f.read()
            assert "- Linha 1" in content
            assert "- Linha 2" in content
        finally:
            os.unlink(temp_path)


class TestConfigLoader:
    def test_load_config_retorna_dict(self) -> None:
        config = load_config()
        assert isinstance(config, dict)
        assert "styles" in config or "hf_key" in config


# "Teste cedo, teste frequentemente." - Kent Beck
