# Estrutura de Pastas - Detector de Doppelganger

## TL;DR

Projeto organizado em camadas: raiz (config/scripts), src/ (codigo), docs/ (documentacao), dev-journey/ (memoria).

---

## Arvore Completa

```
Detector-de-Doppelganger/
│
├── main.py                      # Entry point (orquestrador puro)
├── config.py                    # Configuracoes centralizadas
├── .env                         # Variaveis de ambiente (ignorado)
├── .env.example                 # Template de configuracao
├── requirements.txt             # Dependencias Python
├── install.sh                   # Script de instalacao
├── uninstall.sh                 # Script de desinstalacao
├── run_tests.py                 # Executor de testes
├── .gitignore                   # Exclusoes de versionamento
├── LICENSE                      # GPLv3
├── README.md                    # Documentacao principal
├── prompts.json                 # Estilos de output
│
├── assets/                      # Recursos estaticos
│   ├── icon.png                 # Icone da aplicacao
│   └── interface.png            # Screenshot da UI
│
├── data/                        # Dados de usuario (ignorado)
│   ├── input/                   # Arquivos de entrada
│   └── output/                  # Arquivos processados
│
├── dev-journey/                 # Memoria do projeto
│   ├── 01-getting-started/      # Quick start, arquitetura
│   ├── 02-changelog/            # Historico de versoes
│   ├── 03-implementation/       # Status atual
│   └── Session_Summary.md       # Resumo de sessao
│
├── docs/                        # Documentacao adicional
│   ├── AUDITORIA_EXTERNA.md     # Analise tecnica
│   ├── SCORECARD.md             # Metricas de qualidade
│   └── IMPLEMENTATION_PLAN.md   # Plano de refatoracao
│
├── src/                         # Codigo fonte
│   ├── __init__.py
│   │
│   ├── app/                     # Bootstrap e inicializacao
│   │   ├── __init__.py
│   │   └── bootstrap.py         # Setup da aplicacao
│   │
│   ├── core/                    # Logica de negocio
│   │   ├── __init__.py
│   │   ├── app_core.py          # Gerenciador de modelos
│   │   ├── detector.py          # Deteccao de IA
│   │   ├── humanizador.py       # Humanizacao de texto
│   │   ├── reprocessor.py       # Loop iterativo
│   │   ├── naturalness_evaluator.py
│   │   ├── models.py            # Carregador de modelos
│   │   ├── config_loader.py     # Loader de prompts
│   │   ├── output_formatter.py  # Formatador de saida
│   │   ├── checkpoint.py        # Sistema de checkpoint
│   │   ├── logging_config.py    # Logging rotacionado
│   │   └── processing_thread.py # Thread de processamento
│   │
│   ├── ui/                      # Interface grafica
│   │   ├── __init__.py
│   │   ├── main_window.py       # Janela principal
│   │   ├── left_menu.py         # Menu lateral
│   │   ├── splash_screen.py     # Tela de carregamento
│   │   ├── text_input_frame.py  # Area de entrada
│   │   ├── text_output_frame.py # Area de saida
│   │   ├── context_menu.py      # Menu de contexto
│   │   └── banner.py            # Banner da aplicacao
│   │
│   ├── utils/                   # Utilitarios
│   │   ├── __init__.py
│   │   ├── colors.py            # Helpers de cor
│   │   └── ctk_theme.json       # Tema CustomTkinter
│   │
│   ├── tests/                   # Testes automatizados
│   │   ├── __init__.py
│   │   ├── conftest.py          # Fixtures pytest
│   │   ├── test_detector.py
│   │   ├── test_humanizador.py
│   │   └── test_reprocessor.py
│   │
│   ├── logs/                    # Logs rotacionados (ignorado)
│   │   └── .gitkeep
│   │
│   └── temp/                    # Arquivos temporarios (ignorado)
│       └── .gitkeep
│
└── venv/                        # Virtual environment (ignorado)
```

---

## Descricao por Diretorio

### Raiz
Arquivos de configuracao, scripts de instalacao e entry point.

### src/app/
Bootstrap e inicializacao da aplicacao.

### src/core/
Toda a logica de negocio: deteccao, humanizacao, reprocessamento.

### src/ui/
Componentes da interface grafica (CustomTkinter).

### src/utils/
Utilitarios e helpers compartilhados.

### src/tests/
Suite de testes automatizados (pytest).

### dev-journey/
Documentacao de desenvolvimento e memoria do projeto.

### docs/
Documentacao tecnica adicional.

---

*Documento atualizado em: 2024-12-31*
