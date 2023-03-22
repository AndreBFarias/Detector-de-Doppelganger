# Arquitetura - Detector de Doppelganger

## TL;DR

Aplicacao desktop (customtkinter) que detecta textos gerados por IA e os humaniza usando modelos T5.

---

## Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────────────┐
│                           main.py                                    │
│                      (Orquestrador Puro)                            │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      src/app/bootstrap.py                           │
│            (Inicializacao, Logging, Environment)                    │
└─────────────────────────────────────────────────────────────────────┘
                                │
            ┌───────────────────┼───────────────────┐
            ▼                   ▼                   ▼
┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
│    src/ui/        │ │   src/core/       │ │   src/utils/      │
│  Interface GUI    │ │  Logica IA        │ │   Helpers         │
└───────────────────┘ └───────────────────┘ └───────────────────┘
         │                     │
         │                     ▼
         │           ┌───────────────────┐
         │           │ HuggingFace       │
         │           │ Transformers      │
         │           └───────────────────┘
         │                     │
         ▼                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    CustomTkinter (GUI Framework)                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Fluxo de Dados

```
[Texto Input]
      │
      ▼
[Detector IA] ──────────────────┐
      │                         │
      ▼                         │
[Humanizador T5]                │
      │                         │
      ▼                         │
[Avaliador Naturalidade]        │
      │                         │
      ├── Score < Threshold? ───┘
      │         │
      │         ▼
      │   [Reprocessador]
      │         │
      │         ▼
      │   [Loop ate 3x]
      │
      ▼
[Texto Humanizado]
```

---

## Componentes Principais

### 1. main.py (Orquestrador)
- Entry point da aplicacao
- < 80 linhas
- Apenas orquestracao, sem logica

### 2. config.py (Configuracoes)
- Todas as constantes centralizadas
- Carrega .env com python-dotenv
- Define paths, modelos, cores

### 3. src/app/bootstrap.py (Inicializacao)
- Setup de logging rotacionado
- Verificacao de assets
- Configuracao do CustomTkinter

### 4. src/core/ (Logica de Negocio)
- `detector.py` - Deteccao de texto IA
- `humanizador.py` - Humanizacao com T5
- `reprocessor.py` - Loop iterativo
- `models.py` - Carregamento de modelos
- `logging_config.py` - Logging rotacionado

### 5. src/ui/ (Interface)
- `main_window.py` - Janela principal
- `left_menu.py` - Menu lateral
- `splash_screen.py` - Tela de carregamento
- `text_input_frame.py` - Area de entrada
- `text_output_frame.py` - Area de saida

---

## Modelos de IA

| Modelo | Uso | Origem |
|--------|-----|--------|
| roberta-base-openai-detector | Deteccao IA | HuggingFace |
| ptt5-small-portuguese-vocab | Humanizacao Leve | Unicamp |
| ptt5-base-portuguese-vocab | Humanizacao Equilibrada | Unicamp |
| ptt5-large-portuguese-vocab | Humanizacao Profunda | Unicamp |

---

## Stack Tecnologico

- **Linguagem**: Python 3.10+
- **GUI**: CustomTkinter
- **IA**: Transformers, PyTorch
- **Logging**: RotatingFileHandler
- **Config**: python-dotenv

---

*Documento atualizado em: 2024-12-31*
