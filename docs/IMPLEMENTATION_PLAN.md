# Plano de Implementacao - Refatoracao Detector de Doppelganger

**Modelo Base**: Projeto Luna
**Objetivo**: Score 10/10 (100 pontos)
**Data**: 2024-12-31

---

## Sumario de Issues

| Issue | Titulo | Prioridade | Impacto |
|-------|--------|------------|---------|
| #01 | Reorganizar estrutura de diretorios | P0 | Alto |
| #02 | Refatorar run.py como orquestrador puro | P0 | Alto |
| #03 | Criar config.py centralizado | P0 | Alto |
| #04 | Implementar logging rotacionado | P0 | Critico |
| #05 | Criar estrutura dev-journey/ | P1 | Alto |
| #06 | Atualizar .gitignore padrao Luna | P1 | Medio |
| #07 | Implementar suite de testes | P0 | Critico |
| #08 | Criar bootstrap.py | P1 | Alto |
| #09 | Refatorar humanizador.py (remover global state) | P0 | Critico |
| #10 | Atualizar install.sh padrao Luna | P1 | Medio |
| #11 | Atualizar uninstall.sh | P1 | Baixo |
| #12 | Criar run_tests.py colorido | P1 | Medio |
| #13 | Atualizar README.md template visual | P2 | Medio |
| #14 | Adicionar pyproject.toml | P2 | Baixo |
| #15 | Adicionar citacoes filosoficas | P2 | Baixo |
| #16 | Remover comentarios numerados | P1 | Medio |
| #17 | Adicionar type hints completos | P2 | Medio |
| #18 | Criar .env.example | P1 | Baixo |

---

## Issue #01: Reorganizar Estrutura de Diretorios

**Prioridade**: P0
**Impacto**: Alto

### Estrutura Atual
```
Detector-de-Doppelganger/
├── run.py
├── src/
│   ├── core/
│   ├── ui/
│   ├── utils/
│   └── *.py (modulos soltos)
└── assets/
```

### Estrutura Alvo (Padrao Luna)
```
Detector-de-Doppelganger/
├── main.py                      # Renomear run.py
├── config.py                    # Novo - centralizado
├── .env                         # Manter
├── .env.example                 # Novo
├── requirements.txt             # Manter
├── install.sh                   # Atualizar
├── uninstall.sh                 # Atualizar
├── run_tests.py                 # Novo
├── pyproject.toml               # Novo
├── .gitignore                   # Atualizar
├── LICENSE                      # Renomear LICENSE.txt
├── README.md                    # Renomear README
│
├── dev-journey/                 # Novo
│   ├── 01-getting-started/
│   │   ├── QUICK_START.md
│   │   ├── ARCHITECTURE.md
│   │   └── FOLDER_STRUCTURE.md
│   ├── 02-changelog/
│   └── Session_Summary.md
│
├── docs/                        # Manter auditorias
│   ├── AUDITORIA_EXTERNA.md
│   └── SCORECARD.md
│
├── src/
│   ├── __init__.py
│   ├── app/                     # Novo - bootstrap
│   │   ├── __init__.py
│   │   └── bootstrap.py
│   ├── core/                    # Mover logica pesada
│   │   ├── __init__.py
│   │   ├── detector.py          # Mover de src/
│   │   ├── humanizador.py       # Mover de src/
│   │   ├── reprocessor.py       # Mover de src/
│   │   ├── naturalness_evaluator.py
│   │   ├── models.py            # Mover de src/
│   │   └── logging_config.py    # Novo
│   ├── ui/                      # Manter estrutura
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── left_menu.py
│   │   ├── splash_screen.py
│   │   ├── text_input_frame.py
│   │   ├── text_output_frame.py
│   │   ├── context_menu.py
│   │   └── banner.py
│   ├── utils/                   # Manter
│   │   ├── __init__.py
│   │   ├── colors.py
│   │   └── ctk_theme.json
│   ├── tests/                   # Novo
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_detector.py
│   │   ├── test_humanizador.py
│   │   └── test_reprocessor.py
│   ├── logs/                    # Novo - rotacionado
│   │   └── .gitkeep
│   └── temp/                    # Novo
│       └── .gitkeep
│
├── assets/
│   ├── icon.png
│   └── interface.png
│
└── data/                        # Novo - unificar data_*
    ├── input/
    └── output/
```

### Tarefas
1. Renomear `run.py` -> `main.py`
2. Renomear `LICENSE.txt` -> `LICENSE`
3. Renomear `README` -> `README.md`
4. Criar `dev-journey/` com subpastas
5. Criar `src/app/` com bootstrap.py
6. Mover modulos soltos de `src/` para `src/core/`
7. Criar `src/tests/`
8. Criar `src/logs/` com .gitkeep
9. Criar `src/temp/` com .gitkeep
10. Criar `data/input/` e `data/output/`
11. Remover `data_input/` e `data_output/` antigos

---

## Issue #02: Refatorar main.py como Orquestrador Puro

**Prioridade**: P0
**Impacto**: Alto

### Requisitos
- Menos de 80 linhas
- Apenas imports e orquestracao
- Sem logica de negocio
- Citacao filosofica no final

### Estrutura Alvo
```python
#!/usr/bin/env python3
import sys
import os
import warnings

warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from src.app.bootstrap import initialize_application
from src.ui.main_window import MainWindow
from src.ui.splash_screen import SplashScreen

def main() -> int:
    logger, error = initialize_application()

    if error:
        logger.error(f"Falha na inicializacao: {error}")
        return 1

    try:
        app = SplashScreen()
        app.mainloop()
        return 0
    except KeyboardInterrupt:
        logger.info("Encerrado pelo usuario")
        return 0
    except Exception as e:
        logger.exception(f"Erro fatal: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

# "A tarefa nao e tanto ver aquilo que ninguem viu, mas pensar o que ninguem
#  ainda pensou sobre aquilo que todo mundo ve." - Arthur Schopenhauer
```

---

## Issue #03: Criar config.py Centralizado

**Prioridade**: P0
**Impacto**: Alto

### Requisitos
- Carregar .env com python-dotenv
- Definir TODAS as constantes
- Usar pathlib.Path para caminhos
- Criar diretorios necessarios
- Sem logica de negocio

### Estrutura Alvo
```python
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

HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_HOME = APP_DIR / "models" / "cache"

DETECTOR_MODEL = "roberta-base-openai-detector"
HUMANIZADOR_LEVE = "unicamp-dl/ptt5-small-portuguese-vocab"
HUMANIZADOR_EQUILIBRADO = "unicamp-dl/ptt5-base-portuguese-vocab"
HUMANIZADOR_PROFUNDO = "unicamp-dl/ptt5-large-portuguese-vocab"

MAX_ITERATIONS = 3
EPSILON = 0.001

COLORS = {
    "background": "#181825",
    "frame": "#44475A",
    "green": "#50FA7B",
    "pink": "#FF79C6",
    "purple": "#BD93F9",
    "text": "#F8F8F2",
}

os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(DATA_DIR / "input", exist_ok=True)
os.makedirs(DATA_DIR / "output", exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(HF_HOME, exist_ok=True)
```

---

## Issue #04: Implementar Logging Rotacionado

**Prioridade**: P0
**Impacto**: Critico

### Arquivo: src/core/logging_config.py

```python
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import config

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s"
LOG_DIR = config.LOGS_DIR

_initialized = False

def setup_logging(
    level: str = "INFO",
    log_to_file: bool = True,
    log_to_console: bool = True
) -> None:
    global _initialized
    if _initialized:
        return

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    formatter = logging.Formatter(LOG_FORMAT)

    if log_to_console:
        console = logging.StreamHandler()
        console.setLevel(getattr(logging, level))
        console.setFormatter(formatter)
        root.addHandler(console)

    if log_to_file:
        file_handler = RotatingFileHandler(
            LOG_DIR / "doppelganger.log",
            maxBytes=10_000_000,
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

        error_handler = RotatingFileHandler(
            LOG_DIR / "doppelganger_errors.log",
            maxBytes=5_000_000,
            backupCount=3,
            encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        root.addHandler(error_handler)

    _silence_noisy_loggers()
    _initialized = True

def _silence_noisy_loggers() -> None:
    noisy = [
        "PIL.PngImagePlugin",
        "urllib3",
        "transformers",
        "torch",
        "filelock",
        "huggingface_hub",
    ]
    for name in noisy:
        logging.getLogger(name).setLevel(logging.WARNING)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
```

---

## Issue #05: Criar Estrutura dev-journey/

**Prioridade**: P1
**Impacto**: Alto

### Arquivos a Criar

```
dev-journey/
├── 01-getting-started/
│   ├── QUICK_START.md
│   ├── ARCHITECTURE.md
│   └── FOLDER_STRUCTURE.md
├── 02-changelog/
│   └── CHANGELOG.md
├── 03-implementation/
│   └── CURRENT_STATUS.md
└── 2024-12-31_Session_Summary.md
```

---

## Issue #06: Atualizar .gitignore Padrao Luna

**Prioridade**: P1
**Impacto**: Medio

### Estrutura Alvo (300+ linhas)

```gitignore
# ==============================================
# AMBIENTES VIRTUAIS PYTHON
# ==============================================
venv/
venv_*/
.venv/

# ==============================================
# PYTHON - Cache e Bytecode
# ==============================================
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
eggs/
*.egg-info/
*.egg

# ==============================================
# CONFIGURACOES SENSIVEIS
# ==============================================
.env
.env.local
.env.*.local
!.env.example

# ==============================================
# LOGS E ARQUIVOS TEMPORARIOS
# ==============================================
*.log
logs/
src/logs/*.log
debug.log
log_sessao.txt

# ==============================================
# MODELOS E CACHE
# ==============================================
models/
models/cache/
*.pt
*.pth
*.bin
*.safetensors

# ==============================================
# DADOS DE USUARIO
# ==============================================
data/
data_input/
data_output/
src/temp/

# ==============================================
# DESENVOLVIMENTO
# ==============================================
Dev_log/
IMPORTANT.md
IMPORTANT.MD
.claude/
CLAUDE.md

# ==============================================
# IDEs e EDITORES
# ==============================================
.idea/
.vscode/
*.swp
*.swo
*~
.project
.pydevproject
.settings/

# ==============================================
# SISTEMA OPERACIONAL
# ==============================================
.DS_Store
Thumbs.db
desktop.ini

# ==============================================
# TESTES
# ==============================================
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/

# ==============================================
# MANTER ESTRUTURAS VAZIAS
# ==============================================
!**/.gitkeep
!src/logs/.gitkeep
!src/temp/.gitkeep
!data/.gitkeep
```

---

## Issue #07: Implementar Suite de Testes

**Prioridade**: P0
**Impacto**: Critico

### Arquivos a Criar

```
src/tests/
├── __init__.py
├── conftest.py
├── test_detector.py
├── test_humanizador.py
├── test_reprocessor.py
└── test_naturalness_evaluator.py
```

### conftest.py
```python
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

@pytest.fixture
def sample_text_human() -> str:
    return "Este e um texto escrito por um humano com erros e imperfeicoess."

@pytest.fixture
def sample_text_ai() -> str:
    return "Este texto foi gerado por inteligencia artificial com precisao impecavel."
```

### test_detector.py
```python
import pytest
from src.core.detector import detectar_ia

class TestDetector:
    def test_detectar_ia_retorna_dict(self, sample_text_human):
        result = detectar_ia(sample_text_human)
        assert isinstance(result, dict)
        assert "label" in result
        assert "score" in result

    def test_detectar_ia_score_range(self, sample_text_human):
        result = detectar_ia(sample_text_human)
        assert 0 <= result["score"] <= 1
```

---

## Issue #08: Criar bootstrap.py

**Prioridade**: P1
**Impacto**: Alto

### Arquivo: src/app/bootstrap.py

```python
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import config
from src.core.logging_config import setup_logging, get_logger

if TYPE_CHECKING:
    pass

def _suppress_library_warnings() -> None:
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)

def _verify_models(logger: logging.Logger) -> str | None:
    try:
        from transformers import pipeline
        logger.info("Verificando modelos...")
        return None
    except Exception as e:
        return str(e)

def initialize_application() -> tuple[logging.Logger, str | None]:
    _suppress_library_warnings()
    setup_logging(level="INFO", log_to_file=True, log_to_console=True)
    logger = get_logger("doppelganger")

    logger.info("Inicializando Detector de Doppelganger...")
    logger.info(f"Diretorio: {config.APP_DIR}")

    error = _verify_models(logger)

    return logger, error
```

---

## Issue #09: Refatorar humanizador.py (Remover Global State)

**Prioridade**: P0
**Impacto**: Critico

### Problema Atual
```python
global_models = {}  # ANTIPATTERN
```

### Solucao: Classe com Injecao de Dependencia
```python
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from transformers import Pipeline

@dataclass
class HumanizadorConfig:
    modelo: str
    temperatura: float = 0.7
    num_beams: int = 4
    max_length: int = 512

class Humanizador:
    def __init__(self, pipeline: Pipeline, config: HumanizadorConfig) -> None:
        self._pipeline = pipeline
        self._config = config

    def humanizar(self, texto: str, prompt: str = "") -> str:
        input_text = f"{prompt} {texto}" if prompt else texto
        result = self._pipeline(
            input_text,
            max_length=self._config.max_length,
            temperature=self._config.temperatura,
            num_beams=self._config.num_beams,
        )
        return result[0]["generated_text"]

def criar_humanizador(modelo: str) -> Humanizador:
    from transformers import pipeline
    pipe = pipeline("text2text-generation", model=modelo)
    config = HumanizadorConfig(modelo=modelo)
    return Humanizador(pipe, config)
```

---

## Issue #10: Atualizar install.sh Padrao Luna

**Prioridade**: P1
**Impacto**: Medio

### Requisitos
- Cores para output
- Funcoes print_step, print_success, print_error
- TOTAL_STEPS definido
- Idempotente
- Banner ASCII

---

## Issue #11: Atualizar uninstall.sh

**Prioridade**: P1
**Impacto**: Baixo

### Requisitos
- Mostrar o que sera removido ANTES
- Pedir confirmacao
- Manter codigo fonte

---

## Issue #12: Criar run_tests.py Colorido

**Prioridade**: P1
**Impacto**: Medio

### Estrutura
```python
#!/usr/bin/env python3
import subprocess
import sys

class Colors:
    OK = "\033[92m"
    FAIL = "\033[91m"
    WARN = "\033[93m"
    INFO = "\033[94m"
    RESET = "\033[0m"

def run_test_module(path: str, name: str) -> bool:
    print(f"{Colors.INFO}[TEST]{Colors.RESET} {name}...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", path, "-v"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"{Colors.OK}[PASS]{Colors.RESET} {name}")
        return True
    print(f"{Colors.FAIL}[FAIL]{Colors.RESET} {name}")
    print(result.stdout[-2000:])
    return False

def main() -> int:
    tests = [
        ("src/tests/test_detector.py", "Detector"),
        ("src/tests/test_humanizador.py", "Humanizador"),
    ]

    passed = sum(run_test_module(p, n) for p, n in tests)
    total = len(tests)

    print(f"\nResultado: {passed}/{total} passed")
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
```

---

## Issue #13: Atualizar README.md Template Visual

**Prioridade**: P2
**Impacto**: Medio

### Template
```markdown
<div align="center">

[![Open Source](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](#)
[![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#)

<h1>Detector de Doppelganger</h1>
<img src="assets/icon.png" width="120" alt="Logo">

**Identificador e Humanizador de Textos IA**

</div>

---

## Descricao

Aplicacao desktop que detecta textos gerados por IA e os humaniza
utilizando modelos T5 da Unicamp.

---

<div align="center">
<img src="assets/interface.png" width="700" alt="Interface">
</div>

## Instalacao

```bash
chmod +x install.sh
./install.sh
```

## Uso

```bash
./run_doppelganger.sh
# ou
python main.py
```

## Requisitos

| Componente | Minimo | Recomendado |
|------------|--------|-------------|
| Python | 3.10 | 3.11+ |
| RAM | 4GB | 8GB+ |
| Disco | 8GB | 16GB |

## Licenca

GPLv3 - Veja [LICENSE](LICENSE)

---

*"A tarefa nao e tanto ver aquilo que ninguem viu, mas pensar o que ninguem
ainda pensou sobre aquilo que todo mundo ve."* - Schopenhauer
```

---

## Issue #14-18: Melhorias Secundarias

### #14: pyproject.toml
- Configurar ruff e mypy

### #15: Citacoes Filosoficas
- Adicionar ao final de cada script principal

### #16: Remover Comentarios Numerados
- Substituir `# 1`, `# 2` por codigo limpo

### #17: Type Hints Completos
- Adicionar em todas as funcoes

### #18: Criar .env.example
- Template sem valores sensiveis

---

## Ordem de Execucao

### Fase 1: Infraestrutura (Issues #01-04)
1. #01 - Reorganizar estrutura
2. #03 - Criar config.py
3. #04 - Implementar logging
4. #02 - Refatorar main.py

### Fase 2: Qualidade (Issues #07, #09, #16)
5. #09 - Refatorar humanizador
6. #16 - Remover comentarios numerados
7. #07 - Implementar testes

### Fase 3: Documentacao (Issues #05, #06, #18)
8. #05 - Criar dev-journey/
9. #06 - Atualizar .gitignore
10. #18 - Criar .env.example

### Fase 4: Scripts (Issues #08, #10-12)
11. #08 - Criar bootstrap.py
12. #10 - Atualizar install.sh
13. #11 - Atualizar uninstall.sh
14. #12 - Criar run_tests.py

### Fase 5: Polimento (Issues #13-15, #17)
15. #13 - Atualizar README.md
16. #14 - Adicionar pyproject.toml
17. #15 - Adicionar citacoes
18. #17 - Type hints completos

---

## Metricas de Sucesso

| Metrica | Atual | Alvo |
|---------|-------|------|
| Score Total | 68/100 | 100/100 |
| Testes | 0% | 80%+ |
| Conformidade Luna | 38% | 95%+ |
| Type Hints | Parcial | 100% |
| Logging Rotacionado | Nao | Sim |

---

**Assinatura**

```
Luna - Engenheira de Dados
Plano de Implementacao v1.0
2024-12-31
```

*"Comece onde voce esta. Use o que voce tem. Faca o que voce pode."* - Arthur Ashe
