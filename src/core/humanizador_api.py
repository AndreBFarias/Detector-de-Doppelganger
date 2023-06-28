from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import config

logger = logging.getLogger(__name__)

HUMANIZER_PROMPT = """Edite o texto abaixo fazendo APENAS estas mudancas:

1. Escolha UMA frase e reordene as palavras (ex: "A IA transforma setores" -> "Setores sao transformados pela IA")
2. Substitua UM adjetivo por outro equivalente
3. Remova UM advérbio se houver (significativamente, extremamente, etc)
4. Se houver lista com virgulas, mude a ordem dos itens

IMPORTANTE:
- Mantenha 80% do texto EXATAMENTE igual
- Nao adicione palavras novas
- Nao mude o tom
- Responda APENAS com o texto editado

TEXTO: {texto}

EDITADO:"""

HUMANIZER_PROMPT_STYLE = {
    "casual": """Tom: neutro e natural, como alguem digitando normalmente.""",
    "formal": """Tom: profissional mas fluido, como um email de trabalho bem escrito.""",
    "academico": """Tom: tecnico mas legivel, como um artigo bem redigido.""",
}


class HumanizerAPI:
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
            logger.warning("GROQ_API_KEY nao configurada.")
            return

        try:
            from groq import Groq

            self._client = Groq(api_key=config.GROQ_API_KEY)
            logger.info("Cliente Groq inicializado para humanizacao.")
        except ImportError:
            logger.error("Pacote 'groq' nao instalado. Execute: pip install groq")
        except Exception as e:
            logger.error(f"Falha ao inicializar Groq: {e}")

    def _initialize_gemini(self) -> None:
        if not config.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY nao configurada.")
            return

        try:
            import google.generativeai as genai

            genai.configure(api_key=config.GEMINI_API_KEY)
            self._client = genai.GenerativeModel(config.GEMINI_MODEL)
            logger.info("Cliente Gemini inicializado para humanizacao.")
        except ImportError:
            logger.error("Pacote 'google-generativeai' nao instalado.")
        except Exception as e:
            logger.error(f"Falha ao inicializar Gemini: {e}")

    def humanize(self, texto: str, style: str = "casual") -> str:
        if not texto.strip():
            return texto

        if self._client is None:
            logger.error("Cliente API nao inicializado.")
            return texto

        try:
            style_instruction = HUMANIZER_PROMPT_STYLE.get(style, HUMANIZER_PROMPT_STYLE["casual"])
            prompt = HUMANIZER_PROMPT.format(texto=texto)
            full_prompt = f"{style_instruction}\n\n{prompt}"

            if self.provider == "groq":
                return self._humanize_groq(full_prompt)
            elif self.provider == "gemini":
                return self._humanize_gemini(full_prompt)

            return texto

        except Exception as e:
            logger.error(f"Falha na humanizacao via API: {e}", exc_info=True)
            return texto

    def _humanize_groq(self, prompt: str) -> str:
        response = self._client.chat.completions.create(  # type: ignore[union-attr]
            model=config.GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Voce e um especialista em reescrita de textos. Responda APENAS com o texto reescrito, sem explicacoes ou comentarios adicionais.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
            max_tokens=4000,
        )

        content = response.choices[0].message.content
        return self._clean_response(content)

    def _humanize_gemini(self, prompt: str) -> str:
        response = self._client.generate_content(prompt)  # type: ignore[union-attr]
        content = response.text
        return self._clean_response(content)

    def _clean_response(self, content: str) -> str:
        content = content.strip()

        prefixes_to_remove = [
            "Aqui esta o texto reescrito:",
            "Texto reescrito:",
            "Segue o texto:",
            "Claro!",
            "Certo!",
        ]

        for prefix in prefixes_to_remove:
            if content.lower().startswith(prefix.lower()):
                content = content[len(prefix) :].strip()

        if content.startswith('"') and content.endswith('"'):
            content = content[1:-1]

        return content


def humanizar_api(texto: str, style: str = "casual", provider: str = "groq") -> str:
    humanizer = HumanizerAPI(provider)
    return humanizer.humanize(texto, style)


# "A arte de escrever e a arte de descobrir o que voce acredita." - Gustave Flaubert
