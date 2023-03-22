from __future__ import annotations

import json
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import config

logger = logging.getLogger(__name__)

DETECTION_PROMPT = """Analise o texto abaixo e determine se foi escrito por um humano ou por uma IA.

CRITERIOS DE ANALISE:
1. Variacao lexical e escolha de palavras
2. Estrutura de frases (uniformidade vs variacao)
3. Presenca de imperfeicoes naturais humanas
4. Coerencia e fluidez do texto
5. Padroes tipicos de modelos de linguagem

TEXTO PARA ANALISE:
{texto}

RESPOSTA (JSON):
{{
    "classificacao": "humano" ou "ia",
    "confianca": 0.0 a 1.0,
    "razoes": ["razao1", "razao2", "razao3"]
}}
"""


class DetectorAPI:
    def __init__(self, provider: str = "groq") -> None:
        self.provider = provider
        self._client: object | None = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        if self.provider == "groq":
            self._initialize_groq()
        elif self.provider == "gemini":
            self._initialize_gemini()
        else:
            logger.error(f"Provider desconhecido: {self.provider}")

    def _initialize_groq(self) -> None:
        if not config.GROQ_API_KEY:
            logger.warning("GROQ_API_KEY nao configurada. Detector API indisponivel.")
            return

        try:
            from groq import Groq
            self._client = Groq(api_key=config.GROQ_API_KEY)
            logger.info("Cliente Groq inicializado com sucesso.")
        except ImportError:
            logger.error("Pacote 'groq' nao instalado. Execute: pip install groq")
        except Exception as e:
            logger.error(f"Falha ao inicializar Groq: {e}")

    def _initialize_gemini(self) -> None:
        if not config.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY nao configurada. Detector API indisponivel.")
            return

        try:
            import google.generativeai as genai
            genai.configure(api_key=config.GEMINI_API_KEY)
            self._client = genai.GenerativeModel(config.GEMINI_MODEL)
            logger.info("Cliente Gemini inicializado com sucesso.")
        except ImportError:
            logger.error("Pacote 'google-generativeai' nao instalado.")
        except Exception as e:
            logger.error(f"Falha ao inicializar Gemini: {e}")

    def detect(self, texto: str) -> tuple[float, str]:
        if not texto.strip():
            return 0.0, "Texto vazio"

        if self._client is None:
            logger.error("Cliente API nao inicializado.")
            return 0.0, "Erro: API nao configurada"

        try:
            prompt = DETECTION_PROMPT.format(texto=texto[:2000])

            if self.provider == "groq":
                return self._detect_groq(prompt)
            elif self.provider == "gemini":
                return self._detect_gemini(prompt)

            return 0.0, "Erro: Provider desconhecido"

        except Exception as e:
            logger.error(f"Falha na deteccao via API: {e}", exc_info=True)
            return 0.0, "Erro na analise"

    def _detect_groq(self, prompt: str) -> tuple[float, str]:
        response = self._client.chat.completions.create(  # type: ignore[union-attr]
            model=config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": "Voce e um especialista em detectar textos gerados por IA."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=500,
        )

        content = response.choices[0].message.content
        return self._parse_response(content)

    def _detect_gemini(self, prompt: str) -> tuple[float, str]:
        response = self._client.generate_content(prompt)  # type: ignore[union-attr]
        content = response.text
        return self._parse_response(content)

    def _parse_response(self, content: str) -> tuple[float, str]:
        try:
            json_match = re.search(r"\{[^}]+\}", content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                classificacao = data.get("classificacao", "").lower()
                confianca = float(data.get("confianca", 0.5))

                if classificacao == "ia":
                    return confianca, f"IA ({confianca * 100:.1f}%)"
                else:
                    return 1 - confianca, f"Humano ({confianca * 100:.1f}%)"

        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Falha ao parsear resposta: {e}")

        if "ia" in content.lower() or "artificial" in content.lower():
            return 0.7, "IA (estimado)"
        return 0.3, "Humano (estimado)"


def detectar_ia_api(texto: str, provider: str = "groq") -> tuple[float, str]:
    detector = DetectorAPI(provider)
    return detector.detect(texto)


# "O conhecimento fala, mas a sabedoria escuta." - Jimi Hendrix
