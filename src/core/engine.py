from __future__ import annotations

import logging
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import config
from src.core.detector_api import detectar_ia_api
from src.core.detector_local import detectar_ia_local
from src.core.humanizador_api import humanizar_api
from src.core.humanizador_local import humanizar_local

logger = logging.getLogger(__name__)


@dataclass
class IterationResult:
    texto: str
    score_ia: float
    label: str
    iteracao: int


@dataclass
class ProcessResult:
    texto_original: str
    texto_final: str
    score_inicial: float
    score_final: float
    iteracoes: list[IterationResult]
    sucesso: bool
    mensagem: str


class DoppelgangerEngine:
    def __init__(
        self,
        detector_mode: str = "local",
        humanizer_mode: str = "api",
        api_provider: str = "groq",
        max_iterations: int = 5,
        target_score: float = 0.3,
        progress_callback: Callable[[str, float], None] | None = None,
    ) -> None:
        self.detector_mode = detector_mode
        self.humanizer_mode = humanizer_mode
        self.api_provider = api_provider
        self.max_iterations = max_iterations
        self.target_score = target_score
        self.progress_callback = progress_callback

        logger.info(
            f"Engine inicializado: detector={detector_mode}, humanizer={humanizer_mode}, "
            f"provider={api_provider}, max_iter={max_iterations}, target={target_score}"
        )

    def _report_progress(self, message: str, progress: float) -> None:
        if self.progress_callback:
            self.progress_callback(message, progress)
        logger.info(message)

    def detect(self, texto: str) -> tuple[float, str]:
        if self.detector_mode == "api":
            return detectar_ia_api(texto, self.api_provider)
        return detectar_ia_local(texto)

    def humanize(self, texto: str, style: str = "casual") -> str:
        if self.humanizer_mode == "api":
            return humanizar_api(texto, style, self.api_provider)
        return humanizar_local(texto)

    def process(self, texto: str, style: str = "casual") -> ProcessResult:
        if not texto.strip():
            return ProcessResult(
                texto_original=texto,
                texto_final=texto,
                score_inicial=0.0,
                score_final=0.0,
                iteracoes=[],
                sucesso=False,
                mensagem="Texto vazio",
            )

        self._report_progress("Analisando texto original...", 0.1)
        score_inicial, label_inicial = self.detect(texto)

        logger.info(f"Score inicial: {score_inicial:.2%} ({label_inicial})")

        if score_inicial < self.target_score:
            self._report_progress("Texto ja parece humano!", 1.0)
            return ProcessResult(
                texto_original=texto,
                texto_final=texto,
                score_inicial=score_inicial,
                score_final=score_inicial,
                iteracoes=[],
                sucesso=True,
                mensagem=f"Texto ja possui score baixo: {score_inicial:.2%}",
            )

        iteracoes: list[IterationResult] = []
        texto_atual = texto
        score_atual = score_inicial

        for i in range(self.max_iterations):
            progress = 0.1 + (0.8 * (i + 1) / self.max_iterations)
            self._report_progress(f"Iteracao {i + 1}/{self.max_iterations}...", progress)

            texto_humanizado = self.humanize(texto_atual, style)
            novo_score, novo_label = self.detect(texto_humanizado)

            iteracao = IterationResult(
                texto=texto_humanizado,
                score_ia=novo_score,
                label=novo_label,
                iteracao=i + 1,
            )
            iteracoes.append(iteracao)

            logger.info(
                f"Iteracao {i + 1}: score {score_atual:.2%} -> {novo_score:.2%} "
                f"(delta: {(score_atual - novo_score):.2%})"
            )

            if novo_score < self.target_score:
                self._report_progress("Meta alcancada!", 1.0)
                return ProcessResult(
                    texto_original=texto,
                    texto_final=texto_humanizado,
                    score_inicial=score_inicial,
                    score_final=novo_score,
                    iteracoes=iteracoes,
                    sucesso=True,
                    mensagem=f"Score reduzido para {novo_score:.2%} em {i + 1} iteracao(oes)",
                )

            if novo_score >= score_atual:
                logger.warning(f"Score nao reduziu na iteracao {i + 1}. Tentando novamente...")

            texto_atual = texto_humanizado
            score_atual = novo_score

        self._report_progress("Processamento concluido", 1.0)

        melhor_iteracao = min(iteracoes, key=lambda x: x.score_ia) if iteracoes else None
        texto_final = melhor_iteracao.texto if melhor_iteracao else texto
        score_final = melhor_iteracao.score_ia if melhor_iteracao else score_inicial

        sucesso = score_final < score_inicial * 0.7

        return ProcessResult(
            texto_original=texto,
            texto_final=texto_final,
            score_inicial=score_inicial,
            score_final=score_final,
            iteracoes=iteracoes,
            sucesso=sucesso,
            mensagem=f"Score reduzido de {score_inicial:.2%} para {score_final:.2%} ({len(iteracoes)} iteracoes)",
        )


def create_engine(
    progress_callback: Callable[[str, float], None] | None = None,
) -> DoppelgangerEngine:
    return DoppelgangerEngine(
        detector_mode=config.DETECTOR_MODE,
        humanizer_mode=config.HUMANIZER_MODE,
        api_provider="groq" if config.GROQ_API_KEY else "gemini",
        max_iterations=config.MAX_ITERATIONS,
        target_score=config.TARGET_SCORE,
        progress_callback=progress_callback,
    )


# "A persistencia e o caminho do exito." - Charles Chaplin
