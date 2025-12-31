from __future__ import annotations

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.detector import detectar_ia


class TestDetectarIA:
    def test_detectar_ia_com_pipeline_nulo(self, sample_text_human: str) -> None:
        prob, label = detectar_ia(sample_text_human, None)
        assert prob == 0.0
        assert "Erro" in label or "nao carregado" in label.lower()

    def test_detectar_ia_texto_vazio(self, empty_text: str) -> None:
        prob, label = detectar_ia(empty_text, None)
        assert prob == 0.0
        assert "vazio" in label.lower()

    def test_detectar_ia_texto_apenas_espacos(self) -> None:
        prob, label = detectar_ia("   ", None)
        assert prob == 0.0
        assert "vazio" in label.lower()


# "A duvida e o principio da sabedoria." - Aristoteles
