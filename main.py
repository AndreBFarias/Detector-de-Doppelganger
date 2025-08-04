# 1
import torch
from detector import carregar_detector, detectar_ia
from humanizador import carregar_humanizador, humanizar_texto

# 2
device = "cuda" if torch.cuda.is_available() else "cpu"

# 3
if __name__ == "__main__":
    detector = carregar_detector()
    tokenizer, model = carregar_humanizador(device)
    
# 4
    texto = input("Digite o texto para análise: ")
# 5
    eh_ia, score = detectar_ia(texto, detector)
    if eh_ia:
        print(f"Detectado como IA com confiança {score:.2f}. Humanizando...")
        texto_humanizado = humanizar_texto(texto, tokenizer, model, device)
        print("Texto humanizado:", texto_humanizado)
    else:
        print(f"Parece humano com confiança {score:.2f}. Sem necessidade de humanização.")

# "A virtude é suficiente para a felicidade." – Aristóteles, nos alertando que open source virtude liberta das ilusões proprietárias.