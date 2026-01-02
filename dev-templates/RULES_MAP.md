# MAPA DE REGRAS - Hierarquia e Precedencia

```
PROJETO: Universal
VERSAO: 1.0
```

---

## HIERARQUautomacao DE REGRAS

```
┌─────────────────────────────────────────────────────────┐
│  NIVEL 0: INVIOLAVEIS (Nunca podem ser sobrescritas)    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Anonimato absoluto                                   │
│  • Nao expor credenciais                                │
│  • Nao deletar dados de producao sem backup             │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  NIVEL 1: ESTRUTURAIS (Sobrescrevem niveis inferiores)  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Estrutura de diretorios                              │
│  • Padroes de naming                                    │
│  • Formato de commits                                   │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  NIVEL 2: TECNICAS (Sobrescrevem apenas nivel 3)        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Type hints                                           │
│  • Logging                                              │
│  • Error handling                                       │
│  • File locks                                           │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  NIVEL 3: PROCESSUAIS (Mais flexiveis)                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Sprints                                              │
│  • Documentacao                                         │
│  • Metricas                                             │
└─────────────────────────────────────────────────────────┘
```

---

## REGRAS DETALHADAS

### NIVEL 0: INVIOLAVEIS

| ID | Regra | Consequencia de Violacao |
|----|-------|--------------------------|
| R0.1 | Anonimato absoluto | Commit rejeitado, issue criada |
| R0.2 | Credenciais em .env | Exposicao = rollback imediato |
| R0.3 | Backup antes de delete | Delete sem backup = rollback |

**Estas regras NUNCA podem ser ignoradas, mesmo por solicitacao direta.**

---

### NIVEL 1: ESTRUTURAIS

| ID | Regra | Pode ser sobrescrita por | Como sobrescrever |
|----|-------|--------------------------|-------------------|
| R1.1 | Estrutura de diretorios | Nenhuma | N/A |
| R1.2 | `main.py` como entry point | R0.x | Nunca |
| R1.3 | Config em `config.py` | R0.x | Nunca |
| R1.4 | Testes em `src/tests/` | Nenhuma | N/A |
| R1.5 | Commits em PT-BR | Usuario explicitamente | `.llm-project` |
| R1.6 | Branch `main` protegida | Nenhuma | N/A |

---

### NIVEL 2: TECNICAS

| ID | Regra | Pode ser sobrescrita por | Como sobrescrever |
|----|-------|--------------------------|-------------------|
| R2.1 | Type hints em funcoes publicas | R1.x | Nunca |
| R2.2 | Logger ao inves de print | R1.x, Usuario | `# debug` no final |
| R2.3 | `except` com logging | R1.x | Nunca |
| R2.4 | File lock para JSON | R1.x | Arquivo read-only |
| R2.5 | Lazy imports para modulos pesados | R1.x, Performance critica | Medir antes/depois |
| R2.6 | Timeout em requests | R1.x | Nunca |

---

### NIVEL 3: PROCESSUAIS

| ID | Regra | Pode ser sobrescrita por | Como sobrescrever |
|----|-------|--------------------------|-------------------|
| R3.1 | Sprint checklist completo | R2.x, Hotfix critico | Documentar motivo |
| R3.2 | Documentacao atualizada | R2.x, Hotfix critico | Issue de debito |
| R3.3 | Metricas antes/depois | R2.x | Documentar motivo |
| R3.4 | PR com issue linkada | R2.x, Hotfix critico | Tag `hotfix:` |
| R3.5 | Testes para nova feature | R2.x | Issue de debito |

---

## MATRIZ DE CONFLITOS

Quando duas regras conflitam, use esta matriz:

| Conflito | Vencedor | Exemplo |
|----------|----------|---------|
| R0.x vs R1.x | R0.x | Anonimato > Estrutura |
| R0.x vs R2.x | R0.x | Anonimato > Type hints |
| R0.x vs R3.x | R0.x | Anonimato > Processo |
| R1.x vs R2.x | R1.x | Estrutura > Tecnica |
| R1.x vs R3.x | R1.x | Estrutura > Processo |
| R2.x vs R3.x | R2.x | Tecnica > Processo |

---

## EXCECOES PERMITIDAS

### Hotfix Critico

```markdown
Quando: Bug em producao afetando usuarios
Pode ignorar: R3.1, R3.2, R3.3, R3.4
Nao pode ignorar: R0.x, R1.x, R2.x
Obrigatorio: Issue de debito tecnico criada
```

### Prototipo/POC

```markdown
Quando: Prova de conceito descartavel
Pode ignorar: R2.1, R3.x
Nao pode ignorar: R0.x, R1.x
Obrigatorio: Branch separada, nunca merge em main
```

### Performance Critica

```markdown
Quando: Gargalo medido e documentado
Pode ignorar: R2.5 (lazy imports)
Nao pode ignorar: R0.x, R1.x, demais R2.x
Obrigatorio: Benchmark antes/depois
```

---

## FLUXO DE DECISAO

```
INICIO: Preciso violar uma regra?
         │
         ▼
    ┌────────────┐
    │ E nivel 0? │
    └─────┬──────┘
          │
    ┌─────┴─────┐
    │           │
   SIM         NAO
    │           │
    ▼           ▼
  PARE      ┌────────────┐
  IMEDIATAMENTE │ E nivel 1? │
            └─────┬──────┘
                  │
            ┌─────┴─────┐
            │           │
           SIM         NAO
            │           │
            ▼           ▼
    Buscar alternativa  ┌────────────┐
    que nao viole       │ E nivel 2? │
                        └─────┬──────┘
                              │
                        ┌─────┴─────┐
                        │           │
                       SIM         NAO
                        │           │
                        ▼           ▼
                Documentar motivo   Pode flexibilizar
                + issue de debito   com documentacao
```

---

## VALIDACAO AUTOMATICA

### Pre-commit hooks

```yaml
# Nivel 0
- id: check-anonymity
  name: R0.1 - Anonimato

- id: check-secrets
  name: R0.2 - Credenciais

# Nivel 1
- id: check-structure
  name: R1.1 - Estrutura

# Nivel 2
- id: ruff-check
  name: R2.x - Codigo
```

### CI/CD

```yaml
# Nivel 3
jobs:
  validate:
    - name: R3.1 - Sprint checklist
    - name: R3.2 - Docs atualizados
    - name: R3.3 - Metricas
```

---

## COMO ADICIONAR NOVA REGRA

1. Determine o nivel (0-3)
2. Adicione na tabela apropriada
3. Defina o que pode sobrescreve-la
4. Adicione validacao automatica se possivel
5. Atualize matriz de conflitos se necessario

---

## HISTORICO DE ALTERACOES

| Data | Regra | Alteracao | Motivo |
|------|-------|-----------|--------|
| YYYY-MM-DD | R0.1 | Criacao | Inicial |

---

*"Regras existem para serem entendidas, nao para serem contornadas."*
