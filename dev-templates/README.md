# DEV TEMPLATES - Sistema Universal de Governanca

```
VERSAO: 1.0
AUTOR: Comunidade (Anonimo)
LICENCA: GPLv3
```

---

## O QUE E ISSO?

Um sistema completo de templates e workflowes para governanca de projetos de software. Pode ser copiado para qualquer projeto para estabelecer:

- Padroes de codigo
- Workflow de desenvolvimento
- Sistema de qualidade
- Workflowes autonomos de validacao

---

## ESTRUTURA

```
dev-templates/
├── README.md                      # Este arquivo
│
├── [TEMPLATES DE PROJETO]
│   ├── PROJECT_RULES.md           # Regras base para qualquer projeto
│   ├── INDEX_TEMPLATE.md          # Template de navegacao
│   ├── RULES_MAP.md               # Mapa de precedencia de regras
│   ├── SPRINT_TEMPLATE.md         # Workflow de sprint
│   ├── QA_MANUAL_TEMPLATE.md      # Testes manuais humanos
│   └── COMMERCIAL_REPORT_TEMPLATE.md # Relatorio comercial
│
├── [HOOKS]
│   └── hooks/
│       ├── check_acentuacao.py    # Detecta palavras sem acento
│       └── fix_acentuacao.py      # Corrige automaticamente
│
└── [WORKFLOWES AUTONOMOS]
    └── workflows/
        ├── WORKFLOW_00_MASTER.md     # Visao geral dos workflowes
        ├── WORKFLOW_01_QA.md         # Quality Assurance
        ├── WORKFLOW_02_AUDITOR.md    # Auditoria de codigo
        ├── WORKFLOW_03_COMPLIANCE.md # Verificacao de regras
        ├── WORKFLOW_04_COMMERCIAL.md # Relatorios comerciais
        ├── WORKFLOW_05_SCORECARD.md  # Geracao de scorecard
        ├── WORKFLOW_06_INTEGRATION.md # Verificacao de integracao
        └── WORKFLOW_07_SPRINT.md     # Execucao de sprints
```

---

## COMO USAR

### 1. Copiar para Novo Projeto

```bash
# Copiar templates para novo projeto
cp -r .llm-templates /path/to/novo-projeto/

# Copiar PROJECT_RULES.md base
cp .dev-templates/PROJECT_RULES.md /path/to/novo-projeto/PROJECT_RULES.md

# Editar para personalizar
nano /path/to/novo-projeto/PROJECT_RULES.md
```

### 2. Instalar Hooks

```bash
# Copiar hooks para scripts/hooks/
mkdir -p scripts/hooks
cp dev-templates/hooks/*.py scripts/hooks/

# Adicionar ao pre-commit
cat >> .pre-commit-config.yaml << 'EOF'
  - repo: local
    hooks:
      - id: check-acentuacao
        name: Verificar acentuacao PT-BR
        entry: python scripts/hooks/check_acentuacao.py
        language: python
        types: [python]
EOF
```

### 3. Usar Workflowes

```bash
# Copiar prompt do workflowe desejado
cat dev-templates/workflows/WORKFLOW_01_QA.md

# Usar como system prompt em:
# - LLM CLI
# - ChatLLM
# - Outro LLM

# Resultado esperado: arquivo de report gerado
```

---

## FLUXO RECOMENDADO

### Para Desenvolvimento

```
1. WORKFLOW_07_SPRINT     → Executa tarefa com workflow
2. WORKFLOW_06_INTEGRATION → Verifica integracao
3. WORKFLOW_01_QA         → Valida qualidade
4. WORKFLOW_05_SCORECARD  → Gera pontuacao
```

### Para Auditoria

```
1. WORKFLOW_02_AUDITOR    → Audita codigo
2. WORKFLOW_03_COMPLIANCE → Verifica regras
3. WORKFLOW_05_SCORECARD  → Gera pontuacao
4. WORKFLOW_04_COMMERCIAL → Gera relatorio
```

### Para Release

```
1. WORKFLOW_06_INTEGRATION → Verifica tudo
2. WORKFLOW_01_QA         → Valida qualidade
3. WORKFLOW_05_SCORECARD  → Gera pontuacao final
4. WORKFLOW_04_COMMERCIAL → Gera release notes
```

---

## ARQUIVOS POR PROPOSITO

| Voce quer... | Use... |
|--------------|--------|
| Padronizar projeto | `PROJECT_RULES.md` |
| Criar navegacao | `INDEX_TEMPLATE.md` |
| Entender precedencia de regras | `RULES_MAP.md` |
| Executar sprint | `SPRINT_TEMPLATE.md` |
| Fazer QA manual | `QA_MANUAL_TEMPLATE.md` |
| Gerar release notes | `COMMERCIAL_REPORT_TEMPLATE.md` |
| Detectar acentuacao | `hooks/check_acentuacao.py` |
| Rodar QA automatizado | `workflows/WORKFLOW_01_QA.md` |
| Auditar codigo | `workflows/WORKFLOW_02_AUDITOR.md` |
| Verificar regras | `workflows/WORKFLOW_03_COMPLIANCE.md` |
| Criar relatorio comercial | `workflows/WORKFLOW_04_COMMERCIAL.md` |
| Gerar scorecard | `workflows/WORKFLOW_05_SCORECARD.md` |
| Verificar integracao | `workflows/WORKFLOW_06_INTEGRATION.md` |
| Executar tarefa completa | `workflows/WORKFLOW_07_SPRINT.md` |

---

## PERSONALIZACAO

### Adicionar Regras

Edite `PROJECT_RULES.md` e adicione novas regras seguindo o padrao:

```markdown
# REGRA X: [NOME]

## O que e

[Descricao]

## Exemplos

```python
# CORRETO
...

# PROIBIDO
...
```

## Validacao

```bash
# Comando para verificar
```
```

### Adicionar Workflowe

1. Copie um workflowe existente como base
2. Renomeie para `WORKFLOW_XX_[NOME].md`
3. Edite as tarefas especificas
4. Adicione ao `WORKFLOW_00_MASTER.md`

---

## CONTRIBUIR

Este e um projeto anonimo e comunitario. Para contribuir:

1. Nunca adicione nomes, emails ou creditos pessoais
2. Mantenha linguagem tecnica e direta
3. Inclua exemplos praticos
4. Teste os templates antes de submeter

---

## LICENCA

GPLv3 - Uso livre, modificacao livre, distribuicao livre.
Creditos pessoais proibidos por design.

---

*"Templates sao a memoria coletiva de boas praticas."*
