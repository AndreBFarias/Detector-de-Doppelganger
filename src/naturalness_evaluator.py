# 4
import logging

def avaliar_naturalidade(texto, avaliador):
    """
    Avalia a naturalidade do texto.
    Para o roberta-base-openai-detector, a naturalidade é o inverso da probabilidade de ser IA.
    LABEL_1 = Real (humano)
    """
    if not texto or not avaliador:
        return 0.0
    try:
        # Trunca para os primeiros 512 tokens para eficiência
        resultado = avaliador(texto[:512])[0]
        
        # CORREÇÃO LÓGICA: Se o resultado for LABEL_1 (Humano), o score é direto. 
        # Se for LABEL_0 (IA), a naturalidade é 1 - score.
        # NOTA: O modelo 'roberta-base-openai-detector' usa:
        # LABEL_0 -> Real (Humano)
        # LABEL_1 -> Fake (IA)
        # Portanto:
        # Se LABEL_0 (Real): Naturalidade = score (confiança de ser Real)
        # Se LABEL_1 (Fake): Naturalidade = 1 - score (confiança de ser Real é o inverso de ser Fake)
        
        label = resultado['label']
        score = resultado['score']
        
        if label == 'Real' or label == 'LABEL_0':
            naturalidade = score
        else:
            naturalidade = 1.0 - score
        
        logging.info(f"Avaliação de naturalidade concluída. Label: {label}, Score Original: {score:.4f}, Naturalidade Calc: {naturalidade:.4f}")
        return naturalidade
    
    except Exception as e:
        logging.error(f"Erro durante a avaliação de naturalidade: {e}", exc_info=True)
        return 0.0
