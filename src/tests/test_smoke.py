"""Smoke tests adicionais para elevar cobertura alem dos 6 testes existentes."""

from pathlib import Path


def test_license_gpl3_presente():
    license_path = Path(__file__).resolve().parent.parent.parent / "LICENSE"
    texto = license_path.read_text(encoding="utf-8")
    assert "GNU GENERAL PUBLIC LICENSE" in texto
    assert "Version 3" in texto


def test_pyproject_existente_e_nao_vazio():
    pyproject = Path(__file__).resolve().parent.parent.parent / "pyproject.toml"
    assert pyproject.exists()
    conteudo = pyproject.read_text(encoding="utf-8")
    assert len(conteudo) > 100


def test_gitignore_exclui_env_e_venv():
    gitignore = Path(__file__).resolve().parent.parent.parent / ".gitignore"
    conteudo = gitignore.read_text(encoding="utf-8")
    assert ".env" in conteudo
    assert ".venv" in conteudo or "venv" in conteudo


def test_env_example_presente():
    env_example = Path(__file__).resolve().parent.parent.parent / ".env.example"
    assert env_example.exists()


def test_estrutura_src_core_existe():
    core_dir = Path(__file__).resolve().parent.parent / "core"
    assert core_dir.is_dir()
    assert (core_dir / "__init__.py").exists()
