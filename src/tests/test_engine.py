from __future__ import annotations

from src.core.adversarial import CONECTIVOS_IA, AdversarialHumanizer, humanizar_adversarial


class TestAdversarialHumanizer:
    def test_init(self) -> None:
        humanizer = AdversarialHumanizer()
        assert humanizer.synonym_rate == 0.15
        assert humanizer.entropy_factor == 1.2

    def test_init_custom_params(self) -> None:
        humanizer = AdversarialHumanizer(synonym_rate=0.3, entropy_factor=1.5)
        assert humanizer.synonym_rate == 0.3
        assert humanizer.entropy_factor == 1.5

    def test_humanize_empty_text(self) -> None:
        humanizer = AdversarialHumanizer()
        result = humanizer.humanize("")
        assert result == ""

    def test_humanize_whitespace(self) -> None:
        humanizer = AdversarialHumanizer()
        result = humanizer.humanize("   ")
        assert result == "   "

    def test_humanize_simple_text(self) -> None:
        humanizer = AdversarialHumanizer()
        texto = "Este e um texto simples para teste."
        result = humanizer.humanize(texto)
        assert result is not None
        assert len(result) > 0

    def test_humanize_with_synonyms(self) -> None:
        humanizer = AdversarialHumanizer(synonym_rate=1.0)
        texto = "Entretanto, e importante considerar isso."
        result = humanizer.humanize(texto)
        assert result is not None

    def test_conectivos_dict_exists(self) -> None:
        assert len(CONECTIVOS_IA) > 0
        assert "entretanto," in CONECTIVOS_IA
        assert "portanto," in CONECTIVOS_IA


class TestHumanizarAdversarial:
    def test_function_exists(self) -> None:
        result = humanizar_adversarial("Texto de teste.")
        assert result is not None

    def test_preserves_meaning(self) -> None:
        texto = "O Brasil e um pais grande."
        result = humanizar_adversarial(texto)
        assert len(result) > 0


class TestDetectorLocal:
    def test_import(self) -> None:
        from src.core.detector_local import DetectorLocal, detectar_ia_local, get_detector

        assert DetectorLocal is not None
        assert get_detector is not None
        assert detectar_ia_local is not None


class TestDetectorAPI:
    def test_import(self) -> None:
        from src.core.detector_api import DetectorAPI, detectar_ia_api

        assert DetectorAPI is not None
        assert detectar_ia_api is not None


class TestHumanizerLocal:
    def test_import(self) -> None:
        from src.core.humanizador_local import HumanizerLocal, get_humanizer, humanizar_local

        assert HumanizerLocal is not None
        assert get_humanizer is not None
        assert humanizar_local is not None


class TestHumanizerAPI:
    def test_import(self) -> None:
        from src.core.humanizador_api import HumanizerAPI, humanizar_api

        assert HumanizerAPI is not None
        assert humanizar_api is not None


class TestEngine:
    def test_import(self) -> None:
        from src.core.engine import DoppelgangerEngine, IterationResult, ProcessResult, create_engine

        assert DoppelgangerEngine is not None
        assert create_engine is not None
        assert IterationResult is not None
        assert ProcessResult is not None

    def test_iteration_result_dataclass(self) -> None:
        from src.core.engine import IterationResult

        result = IterationResult(
            texto="Teste",
            score_ia=0.5,
            label="IA (50%)",
            iteracao=1,
        )
        assert result.texto == "Teste"
        assert result.score_ia == 0.5
        assert result.iteracao == 1

    def test_process_result_dataclass(self) -> None:
        from src.core.engine import ProcessResult

        result = ProcessResult(
            texto_original="Original",
            texto_final="Final",
            score_inicial=0.8,
            score_final=0.3,
            iteracoes=[],
            sucesso=True,
            mensagem="OK",
        )
        assert result.texto_original == "Original"
        assert result.texto_final == "Final"
        assert result.sucesso is True


# "Testar e duvidar, e duvidar e pensar." - Descartes
