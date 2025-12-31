from __future__ import annotations

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.humanizador import HumanizadorCache, humanizar_texto


class TestHumanizarTexto:
    def test_humanizar_texto_vazio(self, empty_text: str) -> None:
        result = humanizar_texto(empty_text, None, None)
        assert "vazio" in result.lower()

    def test_humanizar_texto_apenas_espacos(self) -> None:
        result = humanizar_texto("   ", None, None)
        assert "vazio" in result.lower()

    def test_humanizar_sem_modelo(self, sample_text_human: str) -> None:
        result = humanizar_texto(sample_text_human, None, None)
        assert "Erro" in result or "nao carregado" in result.lower()


class TestHumanizadorCache:
    def test_cache_singleton(self) -> None:
        cache1 = HumanizadorCache()
        cache2 = HumanizadorCache()
        assert cache1 is cache2

    def test_cache_clear(self) -> None:
        cache = HumanizadorCache()
        cache.clear()
        model, tokenizer, name = cache.get()
        assert model is None
        assert tokenizer is None
        assert name is None


# "A simplicidade e o ultimo grau de sofisticacao." - Leonardo da Vinci
