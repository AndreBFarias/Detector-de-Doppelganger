import logging
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
# 3
from src.utils.config import Config
from src.config_loader import load_config

class AppCore:
    """
    Gerencia o carregamento e o acesso aos modelos e configurações de IA.
    """
    def __init__(self):
        # 4
        self.detector = None
        self.naturalness_evaluator = None
        self.humanizer_tokenizer = None
        self.humanizer_model = None
        self.current_humanizer_name = None
        self.styles = {}
        # 4
        self.modelos = {
            "Leve (CPU)": Config.HUMANIZADOR_LEVE,
            "Equilibrado (CPU)": Config.HUMANIZADOR_EQUILIBRADO,
            "Profundo (CPU)": Config.HUMANIZADOR_PROFUNDO,
        }

    # 4
    def load_styles(self):
        """Carrega os estilos de prompts do prompts.json."""
        try:
            config = load_config()
            self.styles = config.get("styles", {})
            logging.info(f"Estilos de saída carregados: {list(self.styles.keys())}")
            return list(self.styles.keys())
        except Exception as e:
            logging.error(f"Falha ao carregar estilos do prompts.json: {e}", exc_info=True)
            self.styles = {"default": {"style": "informal"}} # Fallback
            return ["default"]

    def get_style_info(self, style_key):
        """Retorna as informações do prompt para o estilo selecionado."""
        return self.styles.get(style_key, {})

    # 4
    def load_detector_models(self):
        """Carrega os modelos de detecção e avaliação."""
        try:
            # 4
            logging.info(f"Carregando modelo detector: {Config.DETECTOR_MODEL}")
            # Força o CPU (-1)
            self.detector = pipeline("text-classification", model=Config.DETECTOR_MODEL, device=-1)
            logging.info("Modelo detector carregado com sucesso.")

            # Carrega o avaliador de naturalidade (que pode ser o mesmo ou outro)
            # 4
            logging.info(f"Carregando modelo avaliador: {Config.HALLUCINATION_EVALUATION_MODEL}")
            self.naturalness_evaluator = pipeline("text-classification", model=Config.HALLUCINATION_EVALUATION_MODEL, device=-1)
            logging.info("Modelo avaliador carregado com sucesso.")
            
            return True
        except Exception as e:
            logging.error(f"Falha ao carregar modelos de detecção/avaliação: {e}", exc_info=True)
            return False

    # 4
    def load_humanizer_model(self, model_key="Equilibrado (CPU)"):
        """Carrega um modelo de humanização específico com base na chave do menu."""
        model_name = self.modelos.get(model_key)
        if not model_name:
             logging.error(f"Chave de modelo inválida: {model_key}")
             return False
        
        if self.current_humanizer_name == model_name and self.humanizer_model is not None:
            logging.info(f"Modelo humanizador '{model_name}' já está carregado.")
            return True

        # 4
        try:
            logging.info(f"Carregando modelo humanizador: {model_name}")
            logging.debug(f"Tentando carregar tokenizer e model de: {model_name}")
            
            self.humanizer_tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            if "gpt" in model_name.lower():
                self.humanizer_model = AutoModelForCausalLM.from_pretrained(model_name, device_map="cpu")
            else:
                self.humanizer_model = AutoModelForSeq2SeqLM.from_pretrained(model_name, device_map="cpu")
            
            self.humanizer_model.eval()
            self.current_humanizer_name = model_name
            logging.info(f"Modelo humanizador '{model_name}' carregado com sucesso.")
            logging.debug(f"Modelo atual definido como: {self.current_humanizer_name}")
            return True
        except Exception as e:
            logging.error(f"Falha ao carregar modelo humanizador '{model_name}': {e}", exc_info=True)
            return False
