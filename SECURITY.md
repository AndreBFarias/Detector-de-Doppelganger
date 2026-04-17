# Política de Segurança -- Detector-de-Doppelganger

## Versões Suportadas

| Versão | Suportada |
| ------ | --------- |
| 2.0.x  | sim       |

## Credenciais

O `.env` armazena chaves de API (OpenAI, Anthropic, outros). Nunca commite. Use `.env.example` como template.

## Reportando

1. **Não** abra issue pública
2. Email ao mantenedor
3. Tempo: 48h recepção / 7d avaliação / 30d correção

## Escopo

- `src/core/` e módulos associados
- Pipelines de fine-tuning e avaliação
- CI/CD

## Fora do Escopo

- `transformers`, `torch`, `openai` (reporte upstream)
- APIs externas
