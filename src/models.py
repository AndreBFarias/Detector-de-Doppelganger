# 1
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, T5ForConditionalGeneration
import os

# 2
def load_model_and_tokenizer(model_name_or_path, model_class, tokenizer_class, device, hf_home, task_name="Modelo"):
    """
    Carrega um modelo e tokenizador da Hugging Face, com cache local.
    """
    print(f"Iniciando carregamento: {task_name} ({model_name_or_path})")
    try:
        # Define o caminho do cache local
        local_cache_path = os.path.join(hf_home, model_name_or_path.replace('/', '_'))
        
        # Tenta carregar do cache local primeiro
        try:
            if os.path.exists(local_cache_path):
                print(f"Carregando {task_name} do cache local: {local_cache_path}")
                model = model_class.from_pretrained(local_cache_path, local_files_only=True).to(device)
                tokenizer = tokenizer_class.from_pretrained(local_cache_path, local_files_only=True)
                print(f"{task_name} carregado com sucesso do cache.")
                return model, tokenizer
        except Exception as e:
            print(f"Falha ao carregar {task_name} do cache local ({e}). Tentando baixar...")

        # Se falhar ou não existir, baixa e salva no cache
        print(f"Baixando e salvando {task_name} em: {local_cache_path}")
        model = model_class.from_pretrained(model_name_or_path, cache_dir=hf_home).to(device)
        tokenizer = tokenizer_class.from_pretrained(model_name_or_path, cache_dir=hf_home)
        
        # Salva no cache local para uso futuro
        model.save_pretrained(local_cache_path)
        tokenizer.save_pretrained(local_cache_path)
        
        print(f"{task_name} baixado e salvo com sucesso.")
        return model, tokenizer

    except Exception as e:
        print(f"Erro crítico ao carregar {task_name} ({model_name_or_path}): {e}")
        return None, None

# 3
class ModelLoader:
    """
    Gerencia o carregamento de todos os modelos necessários para a aplicação,
    reportando o progresso através de um callback.
    """
    
    # 4
    def __init__(self, status_callback=None):
        """
        Inicializa o loader.
        :param status_callback: Função para onde enviar atualizações (texto, valor_progresso)
        """
        self.status_callback = status_callback
        
        # Define o dispositivo
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Device set to use {self.device}")
        
        # Define o diretório de cache
        self.hf_home = os.environ.get('HF_HOME', os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'cache'))
        os.makedirs(self.hf_home, exist_ok=True)

    def _report_status(self, text, value):
        """Helper para chamar o callback de status se ele existir."""
        if self.status_callback:
            # Garante que a atualização da UI seja feita na thread principal
            self.status_callback(text, value)
        print(text)

    # 5
    def load_models(self):
        """
        Carrega todos os modelos definidos na configuração.
        """
        try:
            # Importa a configuração dentro do método
            from src.utils.config import Config
            
            # Lista de modelos a carregar
            models_to_load = [
                {"name": "Detector", "path": Config.DETECTOR_MODEL, "model_class": AutoModelForSequenceClassification, "tokenizer_class": AutoTokenizer},
                {"name": "Humanizador Leve", "path": Config.HUMANIZADOR_LEVE, "model_class": T5ForConditionalGeneration, "tokenizer_class": AutoTokenizer},
                {"name": "Humanizador Equilibrado", "path": Config.HUMANIZADOR_EQUILIBRADO, "model_class": T5ForConditionalGeneration, "tokenizer_class": AutoTokenizer},
                {"name": "Humanizador Profundo", "path": Config.HUMANIZADOR_PROFUNDO, "model_class": T5ForConditionalGeneration, "tokenizer_class": AutoTokenizer},
                {"name": "Avaliador de Alucinação", "path": Config.HALLUCINATION_EVALUATION_MODEL, "model_class": AutoModelForSequenceClassification, "tokenizer_class": AutoTokenizer},
            ]
            
            total_models = len(models_to_load)
            
            for i, model_info in enumerate(models_to_load):
                progress = (i + 1) / total_models
                self._report_status(f"Carregando {model_info['name']}...", progress)
                
                load_model_and_tokenizer(
                    model_name_or_path=model_info["path"],
                    model_class=model_info["model_class"],
                    tokenizer_class=model_info["tokenizer_class"],
                    device=self.device,
                    hf_home=self.hf_home,
                    task_name=model_info["name"]
                )
                
            self._report_status("Todos os modelos carregados.", 1.0)
            
        except ImportError:
            self._report_status("Erro: Não foi possível encontrar o arquivo de configuração.", 0.9)
        except Exception as e:
            self._report_status(f"Erro inesperado no ModelLoader: {e}", 0.9)
