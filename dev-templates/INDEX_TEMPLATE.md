# INDEX.md - Navegacao Rapida

```
PROJETO: [NOME_DO_PROJETO]
VERSAO: [X.Y.Z]
ATUALIZADO: [YYYY-MM-DD]
```

> **Para automacoes:** Este arquivo e seu mapa do projeto. Use-o antes de qualquer modificacao.
> **Para Devs:** Consulte antes de criar novos arquivos ou refatorar.

---

## QUICK LINKS

| Precisa de... | Va para... |
|---------------|------------|
| Entender o projeto | [README.md](README.md) |
| Regras de desenvolvimento | [PROJECT_RULES.md](PROJECT_RULES.md) |
| Conformidade legal | [COMPLIANCE.md](COMPLIANCE.md) |
| Arquitetura tecnica | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Historico de versoes | [docs/CHANGELOG.md](docs/CHANGELOG.md) |
| Contribuir | [CONTRIBUTING.md](CONTRIBUTING.md) |

---

## ESTRUTURA DO PROJETO

```
projeto/
├── [ENTRY POINTS]
│   ├── main.py              # Orquestrador principal
│   └── config.py            # Configuracoes centralizadas
│
├── [CODIGO FONTE]
│   └── src/
│       ├── core/            # Infraestrutura base
│       ├── services/        # Logica de negocio
│       ├── ui/              # Interface
│       └── tests/           # Testes unitarios
│
├── [DOCUMENTACAO]
│   ├── docs/                # Documentacao tecnica
│   └── dev-journey/         # Memoria do projeto
│
├── [SCRIPTS]
│   ├── install.sh           # Instalacao
│   └── scripts/             # Automacao
│
└── [ASSETS]
    └── assets/              # Recursos estaticos
```

---

## MAPA DE MODULOS

### Core (`src/core/`)

| Arquivo | Responsabilidade | Dependencias |
|---------|------------------|--------------|
| `logging_config.py` | Logging centralizado | - |
| `file_lock.py` | Lock para arquivos JSON | - |
| `config_loader.py` | Carregamento de configs | `logging_config` |
| `[adicionar]` | | |

### Services (`src/services/`)

| Arquivo | Responsabilidade | Dependencias |
|---------|------------------|--------------|
| `[nome].py` | [descricao] | [deps] |

### UI (`src/ui/`)

| Arquivo | Responsabilidade | Dependencias |
|---------|------------------|--------------|
| `[nome].py` | [descricao] | [deps] |

---

## FLUXO DE DADOS

```
[INPUT]
   │
   ▼
┌──────────────┐
│   main.py    │  ← Entry point
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   config.py  │  ← Configuracoes
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────┐
│          src/services/           │
│  ┌────────┐  ┌────────┐          │
│  │Service1│→→│Service2│→→ ...    │
│  └────────┘  └────────┘          │
└──────────────────────────────────┘
       │
       ▼
[OUTPUT]
```

---

## IMPORTS CRITICOS

### Como importar corretamente

```python
# CORE
from src.core.logging_config import get_logger
from src.core.file_lock import read_json_safe, write_json_safe

# SERVICES
from src.services.main_service import MainService

# CONFIG
import config
```

### Ordem de imports

```python
# 1. Stdlib
import os
import sys
from pathlib import Path

# 2. Third-party
import requests
import numpy as np

# 3. Local
from src.core import get_logger
from src.services import MainService
```

---

## PADROES DO PROJETO

### Logging

```python
from src.core.logging_config import get_logger
logger = get_logger(__name__)

logger.info("Operacao iniciada")
logger.error(f"Falha: {e}")
```

### File Operations

```python
from src.core.file_lock import read_json_safe, write_json_safe

data = read_json_safe(Path("config.json"))
write_json_safe(Path("config.json"), data)
```

### Error Handling

```python
try:
    resultado = operacao_arriscada()
except SpecificError as e:
    logger.error(f"Erro especifico: {e}")
    raise
except Exception as e:
    logger.error(f"Erro inesperado: {e}")
    raise
```

---

## ONDE ADICIONAR CODIGO NOVO

| Tipo de Codigo | Local | Exemplo |
|----------------|-------|---------|
| Nova feature | `src/services/` | `src/services/nova_feature.py` |
| Utilitario | `src/core/` | `src/core/helper.py` |
| Componente UI | `src/ui/` | `src/ui/novo_widget.py` |
| Teste | `src/tests/` | `src/tests/test_nova_feature.py` |
| Script de automacao | `scripts/` | `scripts/novo_script.sh` |

---

## COMANDOS FREQUENTES

```bash
# Iniciar aplicacao
python main.py

# Rodar testes
pytest src/tests/ -v

# Verificar codigo
ruff check src/ --fix
ruff format src/

# Validar imports
python -c "from src.services import MainService; print('OK')"

# Ver logs
tail -f logs/app.log
```

---

## TROUBLESHOOTING

### Problema: Import nao encontrado

```bash
# Verificar PYTHONPATH
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Verificar estrutura
ls -la src/
```

### Problema: Erro de permissao

```bash
# Verificar permissoes
chmod +x scripts/*.sh
```

### Problema: Dependencia faltando

```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

---

## GLOSSARIO

| Termo | Significado |
|-------|-------------|
| Core | Modulos de infraestrutura base |
| Service | Modulos de logica de negocio |
| Handler | Funcao que responde a eventos |
| Provider | Classe que fornece recursos |
| Manager | Classe que gerencia ciclo de vida |

---

## HISTORICO DE MUDANCAS DO INDEX

| Data | Mudanca |
|------|---------|
| YYYY-MM-DD | Criacao inicial |
| | |

---

## NOTAS PARA automacoes

1. **Antes de modificar**, leia `PROJECT_RULES.md`
2. **Antes de criar arquivo**, verifique se ja existe similar
3. **Sempre atualize** este INDEX apos criar novos modulos
4. **Use os padroes** documentados acima
5. **Nunca quebre** imports existentes sem migracao

---

*Mantenha este arquivo atualizado. E a bussola do projeto.*
