# PROJECT_RULES.md - Template Universal v1.0

```
STATUS: PRODUCAO | LANG: PT-BR | ANONIMATO: OBRIGATORIO
```

---

# REGRA -1: ANONIMATO ABSOLUTO

## PALAVRAS BLOQUEADAS EM QUALQUER ARQUIVO

```
PROIBIDO:
├── "LLM" / "LLM" / "provider" / "tool"
├── "provider" / "provider" / "Google AI"
├── "by LLM" / "automatizado" / "automatizado"
├── "Feito por" / "Criado por" / "Autor:"
├── Nomes de pessoas (exceto em LICENSE se exigido)
├── Emails pessoais
├── @usernames
└── Assinaturas em comentarios
```

### VALIDACAO PRE-COMMIT

```bash
grep -rniE "llm|provider|provider|llm-[0-9]|provider" src/ --include="*.py" | grep -viE "api_key|provider|model|config|client|engine"
# DEVE RETORNAR VAZIO
```

---

# REGRA 0: ESTRUTURA OBRIGATORIA

## Arquitetura Base

```
projeto/
├── main.py                 # Entry point (orquestrador)
├── config.py               # Configuracoes centralizadas
├── requirements.txt        # Dependencias
├── .env.example            # Template de variaveis
├── .gitignore              # Padrao robusto
├── LICENSE                 # GPLv3 ou MIT
├── README.md               # Face do projeto
├── INDEX.md                # Navegacao para automacao e devs
├── PROJECT_RULES.md               # Este arquivo
├── COMPLIANCE.md           # Conformidade legal
│
├── install.sh              # Setup Linux
├── uninstall.sh            # Remocao limpa
│
├── src/
│   ├── __init__.py
│   ├── core/               # Infraestrutura base
│   ├── services/           # Logica de negocio
│   ├── ui/                 # Interface (se houver)
│   ├── tests/              # Testes unitarios
│   └── tools/              # Scripts auxiliares
│
├── docs/
│   ├── ARCHITECTURE.md     # Arquitetura tecnica
│   ├── API.md              # Documentacao de API
│   └── CHANGELOG.md        # Historico de versoes
│
├── dev-journey/            # Memoria do projeto
│   ├── 01-getting-started/
│   ├── 02-implementation/
│   ├── 03-changelog/
│   ├── 04-sprints/
│   └── 05-commercial/
│
├── scripts/                # Automacao
│   ├── validate.sh
│   ├── deploy.sh
│   └── hooks/
│
└── assets/                 # Recursos estaticos
```

---

# REGRA 1: CODIGO

## Padrao Python

```python
# CORRETO
from src.core.logging_config import get_logger
logger = get_logger(__name__)

def process_data(input: str) -> dict:
    try:
        result = heavy_operation(input)
        return {"status": "ok", "data": result}
    except Exception as e:
        logger.error(f"Falha em process_data: {e}")
        raise

# PROIBIDO
print("debug")           # Usar logger
except: pass             # Sempre logar erros
import *                 # Imports explicitos
"/home/user/path"        # Usar config.APP_DIR
```

## Imports

```python
# LAZY LOADING - Dentro da funcao quando pesado
def heavy_function():
    import heavy_module  # Carrega apenas quando necessario
    return heavy_module.process()

# EAGER LOADING - Topo do arquivo quando leve
from typing import Optional, List
from pathlib import Path
```

## Type Hints

```python
# Funcoes publicas DEVEM ter type hints
def calculate_score(items: List[dict], threshold: float = 0.5) -> Optional[float]:
    ...

# Funcoes privadas podem omitir
def _internal_helper(x):
    ...
```

---

# REGRA 2: LOGGING

## Configuracao Centralizada

```python
# src/core/logging_config.py
import logging
from logging.handlers import RotatingFileHandler

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = RotatingFileHandler(
            "logs/app.log",
            maxBytes=10_000_000,
            backupCount=5
        )
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
```

## Uso

```python
from src.core.logging_config import get_logger
logger = get_logger(__name__)

logger.info("Operacao iniciada")
logger.warning("Recurso escasso")
logger.error(f"Falha: {e}")
logger.debug("Dados internos")  # Apenas em dev
```

---

# REGRA 3: FILE LOCKS

## Para Arquivos JSON Compartilhados

```python
# src/core/file_lock.py
import fcntl
import json
from pathlib import Path

def read_json_safe(path: Path) -> dict:
    with open(path, "r") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_SH)
        try:
            return json.load(f)
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

def write_json_safe(path: Path, data: dict) -> None:
    with open(path, "w") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            json.dump(data, f, indent=2, ensure_ascii=False)
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
```

---

# REGRA 4: TESTES

## Estrutura

```
src/tests/
├── conftest.py           # Fixtures globais
├── fixtures/             # Dados de teste
├── test_core.py
├── test_services.py
└── test_integration.py
```

## Dados Anonimos

```python
# CORRETO
test_user = "test_user_001"
test_email = "test@example.com"
test_path = tempfile.mkdtemp()

# PROIBIDO
user = "Andre"
email = "andre@gmail.com"
path = "/home/andre/projeto"
```

## Padrao de Teste

```python
import pytest

class TestFeatureX:
    def test_caso_sucesso(self):
        result = feature_x("input_valido")
        assert result is not None
        assert result["status"] == "ok"

    def test_caso_falha(self):
        with pytest.raises(ValueError):
            feature_x("input_invalido")
```

---

# REGRA 5: GIT WORKFLOW

## Branches

```
main        # Producao estavel
dev         # Desenvolvimento ativo
feat/xxx    # Nova feature
fix/xxx     # Correcao de bug
refactor/xxx # Refatoracao
```

## Commits

```bash
# FORMATO
tipo: descricao imperativa em pt-br

# TIPOS
feat:     Nova funcionalidade
fix:      Correcao de bug
refactor: Refatoracao sem mudanca funcional
docs:     Documentacao
test:     Testes
ci:       CI/CD
perf:     Performance
style:    Formatacao

# EXEMPLO
git commit -m "feat: adicionar cache L2 com TTL"
```

## Workflow com Issues

```bash
# 1. Pegar issue
gh issue list --label "status:ready"
gh issue edit N --add-label "status:in-progress"

# 2. Criar branch
gh issue develop N --checkout

# 3. Trabalhar e commitar
git add .
git commit -m "feat: descricao"

# 4. Validar
./scripts/validate.sh

# 5. PR
gh pr create --body "Closes #N"

# 6. Merge
gh pr merge --squash --delete-branch
```

---

# REGRA 6: DOCUMENTACAO

## README.md Obrigatorio

```markdown
<div align="center">

# Nome do Projeto

[![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#)

**Descricao curta e impactante do projeto.**

</div>

## Instalacao

## Uso

## Contribuir
```

## Changelog

```markdown
# CHANGELOG

## [X.Y.Z] - YYYY-MM-DD

### Adicionado
- Feature nova

### Corrigido
- Bug X

### Alterado
- Comportamento Y

### Removido
- Feature obsoleta
```

---

# REGRA 7: SPRINTS

## Checklist Obrigatorio

Toda tarefa DEVE seguir:

```markdown
## Sprint: [NOME]

### Pre-Implementacao
- [ ] Issue criada e assignada
- [ ] Branch criada a partir de dev
- [ ] Metricas "antes" coletadas

### Implementacao
- [ ] Codigo escrito
- [ ] Type hints adicionados
- [ ] Logging implementado
- [ ] Testes unitarios criados

### Validacao
- [ ] Testes passando (pytest)
- [ ] Linter passando (ruff)
- [ ] Imports validados
- [ ] Anonimato verificado

### Documentacao
- [ ] CHANGELOG atualizado
- [ ] INDEX.md atualizado (se necessario)
- [ ] Docstrings em funcoes publicas

### Integracao
- [ ] PR criado com "Closes #N"
- [ ] Metricas "depois" coletadas
- [ ] Relatorio de impacto gerado

### Pos-Merge
- [ ] Branch deletada
- [ ] Issue fechada automaticamente
```

---

# REGRA 8: METRICAS

## Coleta Obrigatoria

```python
# Antes de implementacao
time python -c "from src.app import App; print('OK')"
pytest src/tests/ --tb=short | tail -5
wc -l src/**/*.py | tail -1

# Depois de implementacao
# Mesmos comandos - comparar resultados
```

## Formato de Relatorio

```markdown
## Metricas: Feature X

| Metrica | Antes | Depois | Delta |
|---------|-------|--------|-------|
| Tempo startup | 2.3s | 0.8s | -65% |
| Testes | 150 | 165 | +15 |
| Linhas | 5000 | 5200 | +200 |
| Cobertura | 60% | 62% | +2% |
```

---

# REGRA 9: HIERARQUautomacao DE REGRAS

## Ordem de Precedencia

```
1. REGRA -1 (Anonimato)     # INVIOLAVEL
2. REGRA 0 (Estrutura)      # Base do projeto
3. REGRA 1-4 (Codigo)       # Padroes tecnicos
4. REGRA 5-6 (Git/Docs)     # Workflow
5. REGRA 7-8 (Sprints)      # Processo
```

## Conflitos

Se duas regras conflitarem, a de menor numero vence.

Exemplo: Se uma feature exige commit sem issue (violando REGRA 5), mas e necessaria para manter anonimato (REGRA -1), a REGRA -1 prevalece.

---

# REGRA 10: PRE-COMMIT HOOKS

## .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: local
    hooks:
      - id: check-anonymity
        name: Verificar Anonimato
        entry: bash -c 'grep -rniE "llm|provider|provider" src/ --include="*.py" | grep -viE "api|config" && exit 1 || exit 0'
        language: system
        types: [python]

      - id: check-print
        name: Verificar prints
        entry: bash -c 'grep -rn "print(" src/ --include="*.py" | grep -v "# debug" && exit 1 || exit 0'
        language: system
        types: [python]

      - id: check-test-quality
        name: Verificar qualidade de testes
        entry: bash scripts/hooks/check_test_quality.sh
        language: system
        pass_filenames: false
```

---

# COMANDOS RAPIDOS

```bash
# Validacao completa
./scripts/validate.sh

# Testes
pytest src/tests/ -v

# Linter
ruff check src/ --fix
ruff format src/

# Imports
python -c "from src.app import App; print('OK')"

# Anonimato
grep -rniE "llm|provider" src/ --include="*.py" | grep -viE "api|config"

# Metricas
wc -l src/**/*.py | tail -1
```

---

*"O codigo e propriedade de quem o executa, nao de quem o escreve."*
