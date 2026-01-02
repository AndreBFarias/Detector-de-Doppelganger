# QA MANUAL - Template de Testes Humanos

```
PROJETO: [NOME_DO_PROJETO]
VERSAO: [X.Y.Z]
DATA: [YYYY-MM-DD]
TESTADOR: [NOME_OU_ALIAS]
```

---

## INSTRUCOES GERAIS

1. Execute cada teste na ordem listada
2. Marque [OK] ou [FALHA] em cada item
3. Capture screenshots/prints quando indicado
4. Anote observacoes relevantes
5. Ao finalizar, submeta este documento preenchido

---

## PRE-REQUISITOS

- [ ] Ambiente limpo (sem cache anterior)
- [ ] Dependencias instaladas (`./install.sh`)
- [ ] Variaveis de ambiente configuradas (`.env`)
- [ ] Aplicacao iniciada sem erros

---

## SUITE 1: INICIALIZACAO

### T1.1 - Startup da Aplicacao

| Campo | Valor |
|-------|-------|
| **Acao** | Executar `./run.sh` ou `python main.py` |
| **Esperado** | Aplicacao inicia sem erros em < 5s |
| **Resultado** | [ ] OK / [ ] FALHA |
| **Tempo real** | ___s |
| **Observacoes** | |

### T1.2 - Interface Principal

| Campo | Valor |
|-------|-------|
| **Acao** | Observar tela inicial |
| **Esperado** | Todos elementos visiveis, sem quebra de layout |
| **Resultado** | [ ] OK / [ ] FALHA |
| **Screenshot** | [Anexar se FALHA] |
| **Observacoes** | |

### T1.3 - Logs de Inicializacao

| Campo | Valor |
|-------|-------|
| **Acao** | Verificar `logs/app.log` |
| **Esperado** | Sem ERRORs ou WARNINGs criticos |
| **Resultado** | [ ] OK / [ ] FALHA |
| **Erros encontrados** | |

---

## SUITE 2: FUNCIONALIDADES CORE

### T2.1 - [NOME_DA_FEATURE_1]

**Contexto:** [Descrever o que esta feature faz]

| Passo | Acao | Esperado | OK? |
|-------|------|----------|-----|
| 1 | [Ir em Menu > Opcao X] | [Menu abre] | [ ] |
| 2 | [Clicar em Botao Y] | [Modal aparece] | [ ] |
| 3 | [Preencher campo Z com "teste"] | [Campo aceita input] | [ ] |
| 4 | [Clicar em Confirmar] | [Mensagem de sucesso] | [ ] |
| 5 | [Verificar resultado] | [Dados salvos corretamente] | [ ] |

**Resultado Final:** [ ] OK / [ ] FALHA

**Screenshot de Evidencia:**
```
[Cole aqui o caminho ou anexe]
```

**Observacoes:**
```
[Anote comportamentos inesperados]
```

---

### T2.2 - [NOME_DA_FEATURE_2]

**Contexto:** [Descrever]

| Passo | Acao | Esperado | OK? |
|-------|------|----------|-----|
| 1 | | | [ ] |
| 2 | | | [ ] |
| 3 | | | [ ] |

**Resultado Final:** [ ] OK / [ ] FALHA

---

## SUITE 3: FLUXOS DE ERRO

### T3.1 - Input Invalido

| Campo | Valor |
|-------|-------|
| **Acao** | Inserir dados invalidos no campo X |
| **Input** | `"!@#$%^&*()"` |
| **Esperado** | Mensagem de erro amigavel, sem crash |
| **Resultado** | [ ] OK / [ ] FALHA |
| **Mensagem exibida** | |

### T3.2 - Conexao Perdida (se aplicavel)

| Campo | Valor |
|-------|-------|
| **Acao** | Desconectar rede durante operacao |
| **Esperado** | Timeout gracioso, mensagem de erro, retry opcional |
| **Resultado** | [ ] OK / [ ] FALHA |
| **Comportamento real** | |

### T3.3 - Arquivo Corrompido

| Campo | Valor |
|-------|-------|
| **Acao** | Editar manualmente arquivo de config com JSON invalido |
| **Esperado** | App detecta erro, usa defaults ou pede reconfiguracao |
| **Resultado** | [ ] OK / [ ] FALHA |

---

## SUITE 4: PERFORMANCE

### T4.1 - Tempo de Resposta

| Operacao | Tempo Maximo | Tempo Real | OK? |
|----------|--------------|------------|-----|
| Startup | 5s | ___s | [ ] |
| Abrir tela X | 1s | ___s | [ ] |
| Salvar dados | 2s | ___s | [ ] |
| Busca com 1000 itens | 3s | ___s | [ ] |

### T4.2 - Uso de Recursos

| Recurso | Limite | Valor Real | OK? |
|---------|--------|------------|-----|
| RAM (idle) | 500MB | ___MB | [ ] |
| RAM (uso intenso) | 2GB | ___MB | [ ] |
| CPU (idle) | 5% | ___% | [ ] |
| CPU (uso intenso) | 80% | ___% | [ ] |

---

## SUITE 5: INTEGRACAO (se aplicavel)

### T5.1 - API Externa

| Campo | Valor |
|-------|-------|
| **Acao** | Realizar chamada para API [NOME] |
| **Esperado** | Resposta em < 3s, dados corretos |
| **Resultado** | [ ] OK / [ ] FALHA |
| **Status Code** | |
| **Tempo** | |

### T5.2 - Banco de Dados

| Campo | Valor |
|-------|-------|
| **Acao** | CRUD completo em tabela X |
| **Esperado** | Create, Read, Update, Delete funcionam |
| **Resultado** | [ ] OK / [ ] FALHA |

---

## SUITE 6: REGRESSAO

### T6.1 - Features Anteriores

Verifique que features da versao anterior ainda funcionam:

| Feature | Versao Anterior | Status |
|---------|-----------------|--------|
| [Feature A] | vX.Y.Z | [ ] OK / [ ] FALHA |
| [Feature B] | vX.Y.Z | [ ] OK / [ ] FALHA |
| [Feature C] | vX.Y.Z | [ ] OK / [ ] FALHA |

---

## RESUMO EXECUTIVO

### Estatisticas

| Categoria | Total | Passou | Falhou | % |
|-----------|-------|--------|--------|---|
| Inicializacao | | | | |
| Core | | | | |
| Erros | | | | |
| Performance | | | | |
| Integracao | | | | |
| Regressao | | | | |
| **TOTAL** | | | | |

### Bugs Encontrados

| ID | Severidade | Descricao | Steps to Reproduce |
|----|------------|-----------|-------------------|
| B001 | [CRITICO/ALTO/MEDIO/BAIXO] | | |
| B002 | | | |

### Recomendacoes

```
[ ] Aprovar para producao
[ ] Aprovar com ressalvas (listar abaixo)
[ ] Reprovar - requer correcoes

Ressalvas/Motivos:
1.
2.
```

---

## ASSINATURA

```
Testador: _______________
Data: _______________
Tempo total de teste: _____ horas
Ambiente: [Desktop/Mobile/Web] - [OS] - [Browser se aplicavel]
```

---

## ANEXOS

### Screenshots

```
[Liste os arquivos de screenshot anexados]
1. screenshot_t2_1_sucesso.png
2. screenshot_bug_001.png
```

### Logs Relevantes

```
[Cole trechos de log importantes]
```

### Notas Adicionais

```
[Qualquer informacao extra]
```
