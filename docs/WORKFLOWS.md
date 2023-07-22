# Sistema de Workflows e Skills

Sistema hibrido de governanca para o projeto Detector de Doppelganger.

---

## Arquitetura

```
scripts/
└── run_agents.sh              # Rotina automatica de validacao

dev-templates/
├── PROJECT_RULES.md           # Regras base
├── RULES_MAP.md               # Hierarquia de regras
├── SPRINT_TEMPLATE.md         # Template de sprint
├── QA_MANUAL_TEMPLATE.md      # QA manual
├── COMMERCIAL_REPORT_TEMPLATE.md
├── hooks/                     # Scripts de validacao
└── workflows/                 # Prompts de automacao
```

---

## Script de Automacao

### Uso

```bash
./scripts/run_agents.sh all        # Roda tudo
./scripts/run_agents.sh qa         # Apenas QA
./scripts/run_agents.sh audit      # Apenas auditoria
./scripts/run_agents.sh compliance # Apenas compliance
./scripts/run_agents.sh scorecard  # Apenas scorecard
./scripts/run_agents.sh build      # Apenas builds
```

---

## Comandos Disponiveis

### /qa - Quality Assurance

Executa analise completa de qualidade:
- Testes automatizados (pytest)
- Cobertura de codigo
- Linter (ruff)
- Scorecard de qualidade

**Output:** `docs/QA_REPORT.md`

---

### /audit - Auditoria de Codigo

Auditoria profunda de seguranca e arquitetura:
- Credenciais expostas
- Hardcoded paths
- Silent exceptions
- God classes

**Output:** `docs/AUDIT_REPORT.md`

---

### /compliance - Verificacao de Regras

Verifica conformidade com PROJECT_RULES.md:
- Regra -1: Anonimato
- Regra 0: Estrutura
- Regra 1: Codigo
- Regra 5: Git

**Output:** `docs/COMPLIANCE_REPORT.md`

---

### /scorecard - Pontuacao do Projeto

Gera scorecard visual com notas 0-10:
- Testes (20%)
- Qualidade (25%)
- Seguranca (15%)
- Performance (15%)
- Arquitetura (10%)
- Documentacao (15%)

**Output:** `docs/SCORECARD.md`

---

### /sprint - Execucao de Tarefas

Workflow completo de sprint com 7 fases:
1. Setup (branch, metricas ANTES)
2. Implementacao
3. Testes
4. Validacao
5. Commit
6. PR
7. Metricas POS

**Uso:** `/sprint 42`

**Output:** `docs/SPRINT_ISSUE_42.md`

---

### /build - Gerar Pacotes

Gera pacotes de distribuicao:
- .deb para Debian/Ubuntu
- .flatpak para Linux universal

**Output:** `dist/*.deb`, `dist/*.flatpak`

---

## Workflow Recomendado

### Para Desenvolvimento

```
1. /sprint 42        # Executa tarefa
2. /compliance       # Verifica regras
3. /qa               # Valida qualidade
4. /scorecard        # Gera pontuacao
```

### Para Auditoria

```
1. /audit            # Audita codigo
2. /compliance       # Verifica regras
3. /scorecard        # Gera pontuacao
4. /commercial       # Gera relatorio
```

### Para Release

```
1. /qa               # Valida qualidade
2. /scorecard        # Pontuacao final
3. /build            # Gera pacotes
```

---

*Sistema de governanca para projetos anonimos e comunitarios.*
