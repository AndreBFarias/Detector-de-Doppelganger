from __future__ import annotations

import sys
from pathlib import Path

import pytest

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_text_human() -> str:
    return "Este e um texto escrito por um humano com algumas imperfeicoess e erros de digitacao."


@pytest.fixture
def sample_text_ai() -> str:
    return (
        "A inteligencia artificial e uma area da ciencia da computacao que se dedica "
        "ao desenvolvimento de sistemas capazes de realizar tarefas que normalmente "
        "requerem inteligencia humana."
    )


@pytest.fixture
def empty_text() -> str:
    return ""


@pytest.fixture
def short_text() -> str:
    return "Ola mundo"


# "O teste de uma inteligencia de primeira classe e a capacidade de manter duas
#  ideias opostas na mente ao mesmo tempo." - F. Scott Fitzgerald
