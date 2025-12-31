from __future__ import annotations

from src.utils.colors import get_color_for_percentage


class TestColors:
    def test_color_baixo(self) -> None:
        color = get_color_for_percentage(0.2)
        assert color is not None
        assert isinstance(color, str)

    def test_color_medio(self) -> None:
        color = get_color_for_percentage(0.5)
        assert color is not None

    def test_color_alto(self) -> None:
        color = get_color_for_percentage(0.9)
        assert color is not None

    def test_color_inverse_baixo(self) -> None:
        color = get_color_for_percentage(0.2, inverse=True)
        assert color is not None

    def test_color_inverse_alto(self) -> None:
        color = get_color_for_percentage(0.9, inverse=True)
        assert color is not None

    def test_color_limite_zero(self) -> None:
        color = get_color_for_percentage(0.0)
        assert color is not None

    def test_color_limite_um(self) -> None:
        color = get_color_for_percentage(1.0)
        assert color is not None


# "As cores sao o sorriso da natureza." - Leigh Hunt
