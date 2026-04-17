# Sprint: Isolamento de Modelos Ollama

```
STATUS: PLANEJADA
PRIORIDADE: MEDIA
TIPO: Refactor + Infra
```

---

## Problema

O Detector-de-Doppelganger usa Ollama opcionalmente para parafraseamento (via `OllamaParaphraseEngine`). Os modelos sao buscados no cache global `~/.ollama/models/`. Embora o Ollama seja opcional (HuggingFace e o engine principal), a dependencia de cache global viola o principio de isolamento.

**Modelo utilizado:**
- `llama3.2:3b` (hardcoded em `src/core/paraphrase_engine.py`)

**Impacto:** BAIXO -- Ollama e opcional, projeto funciona sem ele via HuggingFace.

> **ATENCAO:** O cache global `~/.ollama/models/` ja foi removido em 2026-04-01 durante limpeza de disco. Os modelos devem ser baixados e usados exclusivamente dentro da pasta do projeto (`models/ollama/`). Todos os paths no codigo que apontem para `~/.ollama/` devem ser corrigidos para usar o diretorio local do projeto.

---

## Solucao

### Fase 1: Criar diretorio local de modelos Ollama

```bash
mkdir -p models/ollama
```

### Fase 2: Configurar OLLAMA_MODELS

1. Em `.env`, adicionar:
   ```
   OLLAMA_MODELS=./models/ollama
   ```

2. Em `src/core/paraphrase_engine.py`:
   - Remover OLLAMA_URL hardcoded
   - Carregar configuracao do .env
   - Definir `os.environ["OLLAMA_MODELS"]` antes de usar

### Fase 3: Tornar modelo configuravel

Substituir hardcode `llama3.2:3b` por variavel de ambiente:
```
OLLAMA_PARAPHRASE_MODEL=llama3.2:3b
```

### Fase 4: Atualizar .gitignore

```gitignore
models/ollama/
```

---

## Arquivos a modificar

| Arquivo | Alteracao |
|---------|----------|
| .env | Adicionar OLLAMA_MODELS e OLLAMA_PARAPHRASE_MODEL |
| .gitignore | Adicionar models/ollama/ |
| src/core/paraphrase_engine.py | Remover hardcodes, usar .env |

---

*"Dependencia implicita e divida tecnica invisivel."*
