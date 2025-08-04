# 1
import torch
from transformers import pipeline

# 2
device = "cuda" if torch.cuda.is_available() else "cpu"

# 3
def carregar_detector():
    return pipeline("text-classification", model="openai-community/roberta-base-openai-detector", device=device if device == "cuda" else -1)

# 4
def detectar_ia(texto, detector):
    resultado = detector(texto)
    label = resultado[0]['label']
    score = resultado[0]['score']
    if label == 'Fake' and score > 0.5:
        return True, score
    else:
        return False, score# 1
import torch
from transformers import pipeline

# 2
device = "cuda" if torch.cuda.is_available() else "cpu"

# 3
def carregar_detector():
    return pipeline("text-classification", model="openai-community/roberta-base-openai-detector", device=device if device == "cuda" else -1)

# 4
def detectar_ia(texto, detector):
    resultado = detector(texto)
    label = resultado[0]['label']
    score = resultado[0]['score']
    if label == 'Fake' and score > 0.5:
        return True, score
    else:
        return False, score