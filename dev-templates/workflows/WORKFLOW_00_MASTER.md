# SISTEMA DE WORKFLOWES AUTONOMOS

```
VERSAO: 1.0
LINGUAGEM: PT-BR
ANONIMATO: OBRIGATORIO
```

---

## VISAO GERAL

Este sistema define 7 workflowes especializados que trabalham como uma "empresa virtual" de desenvolvimento:

```
┌─────────────────────────────────────────────────────────────┐
│                    WORKFLOWES DISPONIVEIS                       │
├─────────────────────────────────────────────────────────────┤
│  01. QA_WORKFLOW          → Testes e qualidade                 │
│  02. AUDITOR_WORKFLOW     → Auditoria de codigo                │
│  03. COMPLIANCE_WORKFLOW  → Verificacao de regras              │
│  04. COMMERCIAL_WORKFLOW  → Relatorios comerciais              │
│  05. SCORECARD_WORKFLOW   → Geracao de scorecard               │
│  06. INTEGRATION_WORKFLOW → Verificacao de integracao          │
│  07. SPRINT_WORKFLOW      → Execucao de sprints                │
└─────────────────────────────────────────────────────────────┘
```

---

## COMO USAR

### Ativacao Individual

```
Copie o prompt do workflowe desejado e use como system prompt
```

### Ativacao em Sequencia (Recomendado)

```
1. AUDITOR_WORKFLOW    → Identifica problemas
2. COMPLIANCE_WORKFLOW → Verifica violacoes de regras
3. QA_WORKFLOW         → Valida qualidade
4. SCORECARD_WORKFLOW  → Gera pontuacao
5. COMMERCIAL_WORKFLOW → Gera relatorio final
```

### Para Desenvolvimento

```
1. SPRINT_WORKFLOW      → Executa a tarefa
2. INTEGRATION_WORKFLOW → Verifica integracao
3. QA_WORKFLOW          → Valida qualidade
4. SCORECARD_WORKFLOW   → Gera pontuacao
```

---

## ARQUIVOS DE WORKFLOWES

| Workflowe | Arquivo | Funcao |
|--------|---------|--------|
| QA | `WORKFLOW_01_QA.md` | Testes automatizados e manuais |
| Auditor | `WORKFLOW_02_AUDITOR.md` | Auditoria profunda de codigo |
| Compliance | `WORKFLOW_03_COMPLIANCE.md` | Verificacao de regras |
| Commercial | `WORKFLOW_04_COMMERCIAL.md` | Relatorios de negocio |
| Scorecard | `WORKFLOW_05_SCORECARD.md` | Pontuacao do projeto |
| Integration | `WORKFLOW_06_INTEGRATION.md` | Verificacao de integracao |
| Sprint | `WORKFLOW_07_SPRINT.md` | Execucao de tarefas |

---

## OUTPUTS ESPERADOS

Cada workflowe gera um arquivo MD especifico:

```
QA_WORKFLOW         → QA_REPORT_[DATA].md
AUDITOR_WORKFLOW    → AUDIT_REPORT_[DATA].md
COMPLIANCE_WORKFLOW → COMPLIANCE_REPORT_[DATA].md
COMMERCIAL_WORKFLOW → COMMERCIAL_REPORT_[DATA].md
SCORECARD_WORKFLOW  → SCORECARD_[DATA].md
INTEGRATION_WORKFLOW → INTEGRATION_REPORT_[DATA].md
SPRINT_WORKFLOW     → SPRINT_[NOME]_REPORT.md
```

---

## REGRAS UNIVERSAIS PARA TODOS OS WORKFLOWES

1. **Anonimato:** Nunca mencionar "LLM", "LLM", nomes de pessoas
2. **Linguagem:** PT-BR tecnico e direto
3. **Output:** Sempre gerar arquivo MD estruturado
4. **Evidencias:** Sempre incluir comandos executados e outputs
5. **Metricas:** Sempre incluir numeros quando possivel
6. **Acao:** Sugerir correcoes concretas, nao apenas apontar problemas

---

## FLUXO DE TRABALHO COMPLETO

```
[INICIO]
    │
    ▼
┌──────────────────┐
│  SPRINT_WORKFLOW    │ ← Executa a tarefa
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ INTEGRATION_WORKFLOW│ ← Verifica se nao quebrou nada
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   AUDITOR_WORKFLOW  │ ← Audita o codigo novo
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ COMPLIANCE_WORKFLOW │ ← Verifica regras
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    QA_WORKFLOW      │ ← Valida qualidade
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ SCORECARD_WORKFLOW  │ ← Gera pontuacao
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ COMMERCIAL_WORKFLOW │ ← Gera relatorio final
└────────┬─────────┘
         │
         ▼
[FIM - ENTREGA COMPLETA]
```

---

*"Uma empresa de um dev so, com sete cabecas pensantes."*
