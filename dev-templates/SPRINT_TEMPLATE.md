# SPRINT TEMPLATE - Workflow Completo

```
SPRINT: [NOME/NUMERO]
PERIODO: [DATA_INICIO] - [DATA_FIM]
RESPONSAVEL: [IA/DEV]
STATUS: [ ] Planejada | [ ] Em Andamento | [ ] Concluida
```

---

## OBJETIVO DA SPRINT

> [Descreva em 1-2 frases o que esta sprint entrega]

---

## CHECKLIST OBRIGATORIO

### FASE 1: PLANEJAMENTO

- [ ] **1.1** Issue criada no GitHub
  - [ ] Titulo descritivo
  - [ ] Labels apropriadas (P0/P1/P2, type:feature/fix/refactor)
  - [ ] Assignee definido

- [ ] **1.2** Branch criada
  ```bash
  gh issue develop [NUMERO] --checkout
  # ou
  git checkout -b feat/[nome-curto]
  ```

- [ ] **1.3** Metricas "ANTES" coletadas
  ```bash
  # Copie e execute, salve os resultados
  time python -c "from src.app import App; print('OK')"
  pytest src/tests/ -q | tail -3
  wc -l src/**/*.py | tail -1
  ruff check src/ --statistics | tail -5
  ```

  | Metrica | Valor ANTES |
  |---------|-------------|
  | Tempo import | |
  | Testes passando | |
  | Linhas de codigo | |
  | Issues ruff | |

---

### FASE 2: IMPLEMENTACAO

- [ ] **2.1** Codigo escrito
  - [ ] Funcionalidade principal implementada
  - [ ] Edge cases tratados

- [ ] **2.2** Padroes seguidos
  - [ ] Type hints em funcoes publicas
  - [ ] Logger ao inves de print
  - [ ] Error handling com logging
  - [ ] File locks quando necessario

- [ ] **2.3** Testes escritos
  - [ ] Teste de sucesso
  - [ ] Teste de falha esperada
  - [ ] Teste de edge cases

---

### FASE 3: VALIDACAO

- [ ] **3.1** Testes passando
  ```bash
  pytest src/tests/ -v --tb=short
  ```
  Resultado: [ ] OK | [ ] FALHA

- [ ] **3.2** Linter passando
  ```bash
  ruff check src/ --fix
  ruff format src/
  ```
  Resultado: [ ] OK | [ ] FALHA

- [ ] **3.3** Imports validados
  ```bash
  python -c "from src.app import App; print('OK')"
  ```
  Resultado: [ ] OK | [ ] FALHA

- [ ] **3.4** Anonimato verificado
  ```bash
  grep -rniE "llm|provider|provider" src/ --include="*.py" | grep -viE "api|config"
  ```
  Resultado: [ ] VAZIO (OK) | [ ] ENCONTROU (FALHA)

- [ ] **3.5** Pre-commit passou
  ```bash
  pre-commit run --all-files
  ```
  Resultado: [ ] OK | [ ] FALHA

---

### FASE 4: DOCUMENTACAO

- [ ] **4.1** CHANGELOG atualizado
  ```markdown
  ## [X.Y.Z] - YYYY-MM-DD
  ### Adicionado/Corrigido/Alterado
  - [Descricao da mudanca]
  ```

- [ ] **4.2** INDEX.md atualizado (se criou novo modulo)

- [ ] **4.3** Docstrings em funcoes publicas novas

- [ ] **4.4** README atualizado (se feature visivel ao usuario)

---

### FASE 5: INTEGRACAO

- [ ] **5.1** Commit realizado
  ```bash
  git add .
  git commit -m "feat: [descricao imperativa]"
  ```

- [ ] **5.2** Metricas "DEPOIS" coletadas

  | Metrica | ANTES | DEPOIS | DELTA |
  |---------|-------|--------|-------|
  | Tempo import | | | |
  | Testes passando | | | |
  | Linhas de codigo | | | |
  | Issues ruff | | | |

- [ ] **5.3** PR criado
  ```bash
  gh pr create --title "feat: [titulo]" --body "Closes #[NUMERO]"
  ```

- [ ] **5.4** Screenshots/evidencias anexadas (se UI)

---

### FASE 6: POS-MERGE

- [ ] **6.1** PR mergeado
  ```bash
  gh pr merge --squash --delete-branch
  ```

- [ ] **6.2** Issue fechada automaticamente

- [ ] **6.3** Branch local deletada
  ```bash
  git checkout main
  git pull
  git branch -d feat/[nome]
  ```

- [ ] **6.4** Relatorio comercial gerado (se feature significativa)

---

## EVIDENCIAS

### Screenshots

```
[Anexar screenshots da feature funcionando]
```

### Logs Relevantes

```
[Colar logs de sucesso/erro tratado]
```

### Metricas Finais

```
ANTES -> DEPOIS

Tempo startup: Xs -> Ys (-Z%)
Testes: X -> Y (+Z)
Cobertura: X% -> Y% (+Z%)
```

---

## BLOQUEIOS/RISCOS

| Bloqueio | Impacto | Mitigacao | Status |
|----------|---------|-----------|--------|
| | | | |

---

## DEBITO TECNICO CRIADO

| Item | Prioridade | Issue |
|------|------------|-------|
| | | #X |

---

## RETROSPECTIVA

### O que funcionou bem

```
1.
2.
3.
```

### O que pode melhorar

```
1.
2.
3.
```

### Licoes aprendidas

```
1.
2.
```

---

## ASSINATURA

```
Desenvolvedor: _______________
Data conclusao: _______________
Tempo total: _____ horas
Commits: _____
Arquivos alterados: _____
```

---

## CHECKLIST FINAL

```
[ ] Todas as fases completas (1-6)
[ ] Metricas antes/depois documentadas
[ ] Issue fechada
[ ] Branch deletada
[ ] Sem debito tecnico critico
```

**STATUS FINAL:** [ ] APROVADO | [ ] REPROVADO

---

*"Uma sprint bem documentada e uma sprint replicavel."*
