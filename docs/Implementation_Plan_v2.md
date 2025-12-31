# Implementation Plan v2 - Arquitetura Dual

## Visao Geral

Substituicao do motor de deteccao/humanizacao por uma arquitetura que oferece:
1. **Modo Open-Source**: Modelos locais, sem dependencia externa
2. **Modo API**: Groq/Gemini free tier para melhor qualidade

---

## Arquitetura Nova

```
┌─────────────────────────────────────────────────────────────┐
│                      ENTRADA DE TEXTO                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    DETECTOR (Modular)                        │
│  ├── OpenSource: roberta-large-openai-detector               │
│  │               ou XLM-RoBERTa fine-tuned PT                │
│  └── API: Groq (meta-llama/llama-guard) [opcional]           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   HUMANIZADOR (Modular)                      │
│  ├── OpenSource: Tecnicas adversariais locais                │
│  │               - Substituicao sinonimos contextual         │
│  │               - Perturbacao de entropia                   │
│  │               - Variacao de estrutura sintatica           │
│  └── API: Groq (llama-3.3-70b-versatile)                     │
│           Prompt especializado anti-detector                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   LOOP DE ITERACAO                           │
│  while score_ia >= threshold AND iteracoes < max:            │
│      texto = humanizar(texto)                                │
│      score_ia = detectar(texto)                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      SAIDA HUMANIZADA                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Estrategia de Fine-Tuning (Detector PT-BR)

### Problema
- roberta-base-openai-detector treinado em GPT-2 (2019)
- Nao detecta bem GPT-3.5/4/Claude/Gemini
- Detectores multilíngues existem mas nao focados em PT-BR

### Solucao: Fine-tuning XLM-RoBERTa

#### Modelo Base
- `xlm-roberta-large` (550M params)
- Pre-treinado em 100 linguas incluindo PT-BR
- Excelente transferencia cross-lingual

#### Dataset para Fine-Tuning

```python
# Fontes de dados humanos (PT-BR)
HUMAN_SOURCES = [
    "wikipedia-pt",           # Artigos Wikipedia
    "oscar-pt",               # Common Crawl filtrado
    "brwac",                  # Brazilian Web as Corpus
    "news-pt",                # Noticias brasileiras
]

# Fontes de dados IA (gerar com APIs gratuitas)
AI_SOURCES = [
    "gemini-generated",       # Gemini 1.5 Flash (6M tokens/dia gratis)
    "groq-generated",         # Llama 3.3 70B (14k req/dia gratis)
    "gpt2-generated",         # GPT-2 local (baseline)
]
```

#### Pipeline de Geracao de Dataset

```python
# 1. Coletar textos humanos (10k-50k amostras)
# 2. Para cada texto humano, gerar versao IA:
#    - Reescrever com Gemini
#    - Reescrever com Groq/Llama
#    - Gerar texto similar com mesmo tema
# 3. Balancear: 50% humano, 50% IA
# 4. Split: 80% treino, 10% validacao, 10% teste
```

#### Configuracao de Treino

```python
training_args = {
    "model": "xlm-roberta-large",
    "learning_rate": 2e-5,
    "batch_size": 16,
    "epochs": 3,
    "warmup_steps": 500,
    "weight_decay": 0.01,
    "max_length": 512,
    "fp16": True,  # RTX 3050 suporta
}
```

#### Estimativa de Recursos
- GPU: RTX 3050 (4GB VRAM) - Suficiente com gradient accumulation
- Tempo: ~4-8 horas para 50k amostras
- Storage: ~2GB para modelo + ~500MB dataset

---

## Implementacao Open-Source (Humanizador Local)

### Tecnicas Adversariais

#### 1. Substituicao de Sinonimos Contextual
```python
# Usar modelo de embeddings para encontrar sinonimos
# que mantenham semantica mas alterem "fingerprint"
from sentence_transformers import SentenceTransformer

def substituir_sinonimos(texto: str, taxa: float = 0.15) -> str:
    # Selecionar 15% das palavras para substituicao
    # Usar embeddings para encontrar sinonimos contextuais
    # Priorizar palavras que modelos IA usam com frequencia
    pass
```

#### 2. Perturbacao de Entropia
```python
# Modelos IA tem entropia mais baixa (previsivel)
# Adicionar variacao para aumentar entropia

def perturbar_entropia(texto: str) -> str:
    # Inserir palavras menos comuns
    # Variar comprimento de sentencas
    # Adicionar conectivos menos padronizados
    pass
```

#### 3. Variacao Sintatica
```python
# Alterar estrutura sem mudar significado

def variar_sintaxe(texto: str) -> str:
    # Converter voz ativa <-> passiva
    # Reordenar clausulas
    # Fragmentar/combinar sentencas
    pass
```

#### 4. Injecao de Imperfeicoes Humanas
```python
# Humanos cometem "erros" que IA evita

def humanizar_imperfeicoes(texto: str) -> str:
    # Variar pontuacao (... vs .)
    # Adicionar hesitacoes ocasionais
    # Usar contrações e coloquialismos
    pass
```

---

## Implementacao API (Groq Free Tier)

### Configuracao
```python
GROQ_CONFIG = {
    "api_key": "env:GROQ_API_KEY",
    "model": "llama-3.3-70b-versatile",
    "rate_limit": 14400,  # requests/dia
    "tokens_per_request": 8000,
}
```

### Prompt Anti-Detector
```python
HUMANIZER_PROMPT = '''
Voce e um especialista em reescrita de textos.
Sua tarefa: reescrever o texto abaixo de forma que pareca
escrito por um humano brasileiro nativo.

REGRAS:
1. Mantenha TODO o significado original
2. Use linguagem natural e coloquial brasileira
3. Varie o comprimento das frases
4. Evite estruturas muito formais ou padronizadas
5. Adicione pequenas imperfeicoes naturais
6. Use conectivos variados (porem, entretanto, contudo, mas)
7. Evite repeticao de palavras
8. Inclua expressoes idiomaticas quando apropriado

TEXTO ORIGINAL:
{texto}

TEXTO REESCRITO:
'''
```

### Fallback para Gemini
```python
GEMINI_CONFIG = {
    "api_key": "env:GEMINI_API_KEY",
    "model": "gemini-1.5-flash",
    "rate_limit": 6_000_000,  # tokens/dia
    "tokens_per_request": 32000,
}
```

---

## Estrutura de Arquivos Nova

```
src/
├── core/
│   ├── detector.py           # Refatorar para modular
│   ├── detector_local.py     # NEW: roberta-large ou fine-tuned
│   ├── detector_api.py       # NEW: Groq/Gemini detector
│   ├── humanizador.py        # Refatorar para modular
│   ├── humanizador_local.py  # NEW: tecnicas adversariais
│   ├── humanizador_api.py    # NEW: Groq/Gemini API
│   ├── adversarial.py        # NEW: tecnicas de perturbacao
│   └── fine_tuning/          # NEW: scripts de fine-tuning
│       ├── dataset_builder.py
│       ├── train_detector.py
│       └── evaluate.py
```

---

## Fases de Implementacao

### Fase 1: Infraestrutura (Atual)
- [x] Refatoracao Luna
- [x] CI/CD, testes, linting
- [x] Score 98/100

### Fase 2: Detector Melhorado
- [ ] Trocar para roberta-large-openai-detector
- [ ] Implementar detector_local.py
- [ ] Implementar detector_api.py (opcional)
- [ ] Criar interface modular

### Fase 3: Humanizador Novo
- [ ] Implementar tecnicas adversariais locais
- [ ] Integrar Groq API
- [ ] Criar prompt especializado
- [ ] Implementar fallback Gemini

### Fase 4: Fine-Tuning (Opcional)
- [ ] Coletar dataset PT-BR
- [ ] Gerar dados IA com APIs gratuitas
- [ ] Treinar XLM-RoBERTa
- [ ] Avaliar e iterar

### Fase 5: Integracao
- [ ] Refatorar UI para suportar modo dual
- [ ] Adicionar configuracao de modo (local/api)
- [ ] Testes end-to-end
- [ ] Documentacao

---

## Configuracao Usuario Final

```ini
# config.ini
[detector]
mode = local  # local | api | hybrid
local_model = roberta-large-openai-detector
api_provider = groq  # groq | gemini

[humanizer]
mode = api  # local | api | hybrid
local_techniques = synonyms,entropy,syntax,imperfections
api_provider = groq
api_model = llama-3.3-70b-versatile

[iteration]
max_iterations = 5
target_score = 0.3  # Score IA abaixo de 30%
```

---

## Metricas de Sucesso

1. **Detector**: Acuracia >= 85% em textos GPT-3.5/4/Claude
2. **Humanizador**: Reducao de score IA em >= 50% por iteracao
3. **Loop**: Convergencia para score < 30% em <= 5 iteracoes
4. **Latencia**: < 5s por iteracao (modo API)
5. **Custo**: $0 (free tier apenas)

---

"A simplicidade e a sofisticacao suprema." - Leonardo da Vinci
