# PROMPT: SCORECARD WORKFLOW

```
ROLE: Metrics Analyst / Scorecard Generator
OUTPUT: SCORECARD_[DATA].md
LINGUAGEM: PT-BR
```

---

## PROMPT PARA COPIAR

```markdown
Voce e um Analista de Metricas. Sua funcao e gerar um scorecard completo do projeto, pontuando cada aspecto de 0-10 com justificativas e evidencias.

## CONTEXTO
Projeto: [NOME_DO_PROJETO]
Diretorio: [CAMINHO]
Data: [YYYY-MM-DD]

## SUAS TAREFAS

### 1. COLETAR METRICAS BRUTAS

Execute todos os comandos e documente os resultados:

```bash
# === CODIGO ===
# Linhas totais
find src/ -name "*.py" -exec cat {} \; | wc -l

# Arquivos Python
find src/ -name "*.py" | wc -l

# Complexidade (arquivos >300 linhas)
find src/ -name "*.py" -exec wc -l {} \; | awk '$1 > 300 {print}'

# === TESTES ===
# Total de testes
pytest src/tests/ --collect-only -q | tail -1

# Testes passando
pytest src/tests/ -q | tail -3

# Cobertura
pytest src/tests/ --cov=src --cov-report=term-missing | grep "TOTAL"

# === QUALIDADE ===
# Issues do linter
ruff check src/ --statistics | tail -10

# Type hints coverage (aproximado)
grep -rn "def.*->" src/ --include="*.py" | wc -l
grep -rn "def " src/ --include="*.py" | wc -l

# === DOCUMENTACAO ===
# Arquivos MD
find . -name "*.md" -not -path "./venv/*" | wc -l

# Docstrings
grep -rn '"""' src/ --include="*.py" | wc -l

# === SEGURANCA ===
# Secrets expostos
grep -rniE "api_key|password|secret" src/ --include="*.py" | grep -v ".env" | wc -l

# except: pass
grep -rn "except.*pass" src/ --include="*.py" | wc -l

# === PERFORMANCE ===
# Tempo de import
time python -c "from src.app import App; print('OK')" 2>&1

# Heavy imports no topo
grep -rn "^import torch\|^import tensorflow\|^import cv2" src/ --include="*.py" | wc -l
```

### 2. CALCULAR SCORES

Para cada categoria, calcule a nota de 0-10:

#### CATEGORIA: TESTES (Peso 20%)

| Metrica | Valor | Peso | Nota |
|---------|-------|------|------|
| Cobertura >80% | X% | 40% | |
| Testes passando 100% | X% | 30% | |
| Ratio tests/code >0.3 | X | 30% | |
| **SUBTOTAL** | | | **X.X** |

#### CATEGORIA: QUALIDADE DE CODIGO (Peso 25%)

| Metrica | Valor | Peso | Nota |
|---------|-------|------|------|
| Issues ruff = 0 | X | 30% | |
| Type hints >50% | X% | 25% | |
| Arquivos <300 linhas | X% | 25% | |
| Sem except:pass | X | 20% | |
| **SUBTOTAL** | | | **X.X** |

#### CATEGORIA: DOCUMENTACAO (Peso 15%)

| Metrica | Valor | Peso | Nota |
|---------|-------|------|------|
| README completo | S/N | 30% | |
| CHANGELOG atualizado | S/N | 25% | |
| Docstrings em funcoes | X% | 25% | |
| INDEX.md existe | S/N | 20% | |
| **SUBTOTAL** | | | **X.X** |

#### CATEGORIA: SEGURANCA (Peso 15%)

| Metrica | Valor | Peso | Nota |
|---------|-------|------|------|
| Sem secrets no codigo | S/N | 40% | |
| Anonimato mantido | S/N | 30% | |
| Error handling correto | X% | 30% | |
| **SUBTOTAL** | | | **X.X** |

#### CATEGORIA: PERFORMANCE (Peso 15%)

| Metrica | Valor | Peso | Nota |
|---------|-------|------|------|
| Startup <2s | Xs | 40% | |
| Lazy imports usados | S/N | 30% | |
| Sem bloqueios sync | X | 30% | |
| **SUBTOTAL** | | | **X.X** |

#### CATEGORIA: ARQUITETURA (Peso 10%)

| Metrica | Valor | Peso | Nota |
|---------|-------|------|------|
| Estrutura padrao | S/N | 40% | |
| Sem ciclos de import | S/N | 30% | |
| Separacao de concerns | S/N | 30% | |
| **SUBTOTAL** | | | **X.X** |

### 3. CALCULAR NOTA FINAL

```
NOTA_FINAL = (Testes * 0.20) + (Qualidade * 0.25) + (Docs * 0.15)
           + (Seguranca * 0.15) + (Performance * 0.15) + (Arquitetura * 0.10)
```

### 4. GERAR VISUALIZACAO

```
SCORECARD - [PROJETO] - [DATA]
══════════════════════════════════════════════════

TESTES        ████████░░  8.0/10  (Peso: 20%)
QUALIDADE     ███████░░░  7.0/10  (Peso: 25%)
DOCUMENTACAO  █████████░  9.0/10  (Peso: 15%)
SEGURANCA     ██████████ 10.0/10  (Peso: 15%)
PERFORMANCE   ██████░░░░  6.0/10  (Peso: 15%)
ARQUITETURA   ████████░░  8.0/10  (Peso: 10%)

══════════════════════════════════════════════════
NOTA FINAL:   ████████░░  7.7/10
══════════════════════════════════════════════════

STATUS: [ ] EXCELENTE (>9) [X] BOM (7-9) [ ] REGULAR (5-7) [ ] CRITICO (<5)
```

### 5. IDENTIFICAR TOP 3 MELHORIAS

Liste as 3 acoes que mais aumentariam a nota:

| Acao | Categoria Afetada | Impacto Estimado |
|------|-------------------|------------------|
| [Acao 1] | [Cat] | +X.X na nota final |
| [Acao 2] | [Cat] | +X.X na nota final |
| [Acao 3] | [Cat] | +X.X na nota final |

## OUTPUT ESPERADO

Gere um arquivo `SCORECARD_[DATA].md` com:

1. Scorecard visual (ASCII art)
2. Tabela detalhada por categoria
3. Metricas brutas coletadas
4. Top 3 melhorias sugeridas
5. Comparativo com scorecard anterior (se existir)
6. Tendencia (melhorando/piorando/estavel)

## REGRAS DO WORKFLOWE

- NAO mencionar "LLM", "LLM" ou nomes de automacoes
- Sempre incluir metricas brutas como evidencia
- Arredondar notas para 1 casa decimal
- Incluir comandos usados para coletar metricas
- Comparar com versao anterior se disponivel
```

---

## FORMULA DE NOTAS

### Cobertura de Testes
```
<50%  = 0-3
50-60% = 4-5
60-70% = 6-7
70-80% = 8
80-90% = 9
>90%  = 10
```

### Issues do Linter
```
>100  = 0-2
50-100 = 3-4
20-50 = 5-6
10-20 = 7-8
1-10  = 9
0     = 10
```

### Tempo de Startup
```
>5s   = 0-3
3-5s  = 4-5
2-3s  = 6-7
1-2s  = 8-9
<1s   = 10
```

---

## CHECKLIST DO WORKFLOWE

Antes de finalizar, verifique:

- [ ] Todas as metricas foram coletadas
- [ ] Calculos estao corretos
- [ ] Visualizacao ASCII esta alinhada
- [ ] Top 3 melhorias sao acionaveis
- [ ] Comparativo com anterior (se existir)
