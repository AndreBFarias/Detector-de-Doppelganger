import logging
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import re
from src.utils.config import Config
# 3
# A importação 'load_model_at_checkpoint' foi removida.

# Dicionário global para cachear modelos carregados
global_models = {
    "tokenizer": None,
    "model": None,
    "current_name": None
}

def carregar_modelo_humanizador(model_key="Equilibrado (CPU)"):
    """
    Carrega um modelo de humanização sob demanda e o mantém em cache global.
    """
    modelos = {
        "Leve (CPU)": Config.HUMANIZADOR_LEVE,
        "Equilibrado (CPU)": Config.HUMANIZADOR_EQUILIBRADO,
        "Profundo (CPU)": Config.HUMANIZADOR_PROFUNDO,
    }
    
    model_name = modelos.get(model_key)
    if not model_name:
        logging.error(f"Chave de modelo humanizador inválida: {model_key}")
        return None, None

    # Verifica se o modelo solicitado já está no cache global
    if global_models["current_name"] == model_name and global_models["model"] is not None:
        logging.info(f"Usando modelo humanizador '{model_name}' do cache.")
        return global_models["model"], global_models["tokenizer"]

    # Se não, carrega o novo modelo
    logging.info(f"Carregando novo modelo humanizador: {model_name}")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        if "gpt" in model_name.lower():
            model = AutoModelForCausalLM.from_pretrained(model_name, device_map="cpu")
        else:
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name, device_map="cpu")
        
        model.eval()
        
        # Atualiza o cache global
        global_models["tokenizer"] = tokenizer
        global_models["model"] = model
        global_models["current_name"] = model_name
        
        logging.info(f"Modelo humanizador '{model_name}' carregado com sucesso.")
        return model, tokenizer
        
    except Exception as e:
        logging.error(f"Falha ao carregar modelo humanizador '{model_name}': {e}", exc_info=True)
        # Limpa o cache em caso de falha
        global_models.update({"tokenizer": None, "model": None, "current_name": None})
        return None, None

def humanizar_texto(texto, model, tokenizer, device="cpu", prompt_info=None, num_beams=5, temperature=0.9):
    """
    Aplica o prompt de humanização e gera o texto.
    """
    if not texto.strip():
        logging.warning("humanizar_texto chamado com texto vazio.")
        return "Texto vazio"
    
    if model is None or tokenizer is None:
        logging.error("Modelo ou Tokenizer de humanização não fornecidos.")
        return "Erro: Humanizador não carregado"

    try:
        # Extrai informações do prompt
        if prompt_info is None:
            prompt_info = {}
            
        style_prompt = prompt_info.get("style", "reescreva este texto de forma mais natural:")
        max_length_mult = prompt_info.get("max_length_multiplier", 1.8)
        min_length_mult = prompt_info.get("min_length_multiplier", 0.8)

        # Monta o prompt final para PTT5
        # PTT5 foi treinado com tarefas prefixadas. "Paráfrase: " é um bom gatilho.
        prompt_final = f"Paráfrase: {texto}"
        
        # Tokeniza o prompt
        inputs = tokenizer(prompt_final, return_tensors="pt", truncation=True, max_length=1024).to(device)
        
        # Calcula comprimentos com base no input
        input_length = inputs.input_ids.shape[1]
        max_len = max(50, int(input_length * max_length_mult))
        min_len = max(20, int(input_length * min_length_mult))
        
        logging.info(f"Gerando texto humanizado (PTT5). Input_len: {input_length}, Min_len: {min_len}, Max_len: {max_len}")

        # Gera a saída
        outputs = model.generate(
            **inputs,
            max_length=max_len,
            min_length=min_len,
            num_beams=num_beams,
            early_stopping=True,
            temperature=0.8, # PTT5 aguenta um pouco mais de temperatura
            top_k=50,
            top_p=0.95,
            no_repeat_ngram_size=3,
            repetition_penalty=1.2
        )
        
        # Decodifica o texto gerado
        texto_humanizado = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        logging.info(f"RAW OUTPUT: {texto_humanizado}")

        # Limpa saídas comuns
        
        # 0. Remove a instrução do prompt se ela aparecer no texto (Case Insensitive)
        pattern = r"(?:Paráfrase|Parafrase|Reescreva).*?[:\s]*"
        texto_humanizado = re.sub(pattern, "", texto_humanizado, flags=re.IGNORECASE).strip()
        
        # Remove também dois pontos extras que podem sobrar
        texto_humanizado = texto_humanizado.lstrip(': ')

        # 1. Remove repetição do texto original se o modelo apenas copiar o input
        # Isso é difícil de garantir 100% sem comparar strings, mas vamos assumir que se o modelo
        # devolve algo muito similar ao input, falhou. O loop de reprocessamento vai pegar isso na métrica.
        
        # 2. Limpeza final de aspas ou espaços extras
        texto_humanizado = texto_humanizado.strip('"\' ')

        logging.info("Texto humanizado gerado com sucesso.")
        return texto_humanizado

    except Exception as e:
        logging.error(f"Falha ao gerar texto humanizado: {e}", exc_info=True)
        return f"Erro durante a humanização: {e}"
