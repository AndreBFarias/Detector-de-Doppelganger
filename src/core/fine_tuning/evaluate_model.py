from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

MODEL_PATH = config.MODELS_DIR / "detector_pt_finetuned"
DATASET_DIR = config.DATA_DIR / "fine_tuning"


def load_model() -> tuple[Any, Any]:
    logger.info(f"Carregando modelo de {MODEL_PATH}")

    tokenizer = AutoTokenizer.from_pretrained(str(MODEL_PATH))
    model = AutoModelForSequenceClassification.from_pretrained(str(MODEL_PATH))
    model.eval()

    return model, tokenizer


def predict(model: Any, tokenizer: Any, text: str) -> tuple[Any, float]:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True,
    )

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)
        predicted_class = torch.argmax(probs, dim=1).item()
        ai_probability = probs[0][1].item()

    return predicted_class, ai_probability


def evaluate_dataset() -> dict[str, float]:
    model, tokenizer = load_model()

    test_path = DATASET_DIR / "test.json"
    with open(test_path, encoding="utf-8") as f:
        test_data = json.load(f)

    logger.info(f"Avaliando {len(test_data)} amostras do conjunto de teste")

    correct_human = 0
    total_human = 0
    correct_ai = 0
    total_ai = 0

    results = []

    for sample in test_data:
        text = sample["text"]
        true_label = sample["label"]
        source = sample.get("source", "unknown")

        predicted_label, ai_prob = predict(model, tokenizer, text)

        is_correct = predicted_label == true_label

        if true_label == 0:
            total_human += 1
            if is_correct:
                correct_human += 1
        else:
            total_ai += 1
            if is_correct:
                correct_ai += 1

        results.append(
            {
                "text": text[:60] + "..." if len(text) > 60 else text,
                "true": "IA" if true_label == 1 else "Humano",
                "pred": "IA" if predicted_label == 1 else "Humano",
                "ai_prob": f"{ai_prob * 100:.1f}%",
                "correct": is_correct,
                "source": source,
            }
        )

    logger.info("\n" + "=" * 60)
    logger.info("RESULTADOS DA AVALIACAO")
    logger.info("=" * 60)

    human_acc = (correct_human / total_human * 100) if total_human > 0 else 0
    ai_acc = (correct_ai / total_ai * 100) if total_ai > 0 else 0
    total_acc = ((correct_human + correct_ai) / len(test_data) * 100) if test_data else 0

    logger.info(f"\nHumanos: {correct_human}/{total_human} = {human_acc:.1f}%")
    logger.info(f"IA: {correct_ai}/{total_ai} = {ai_acc:.1f}%")
    logger.info(f"Total: {correct_human + correct_ai}/{len(test_data)} = {total_acc:.1f}%")

    logger.info("\n" + "-" * 60)
    logger.info("DETALHES POR AMOSTRA")
    logger.info("-" * 60)

    for r in results:
        status = "OK" if r["correct"] else "ERRO"
        logger.info(f"[{status}] Real: {r['true']:6s} | Pred: {r['pred']:6s} | P(IA): {r['ai_prob']:6s} | {r['text']}")

    return {
        "human_accuracy": human_acc,
        "ai_accuracy": ai_acc,
        "total_accuracy": total_acc,
    }


def test_custom_texts() -> None:
    model, tokenizer = load_model()

    human_texts = [
        "Ontem fui ao mercado comprar frutas. O dia estava ensolarado.",
        "Meu filho tirou nota boa na escola. Ficamos orgulhosos.",
        "O cachorro latiu a noite toda e ninguém dormiu direito.",
        "A vizinha pediu açúcar emprestado e esqueceu de devolver.",
        "Fiz uma receita nova da internet e ficou uma delícia.",
    ]

    ai_texts = [
        "A inteligência artificial está revolucionando diversos setores da economia, desde a saúde até o entretenimento.",
        "Redes sociais desempenham um papel fundamental na sociedade contemporânea, impactando a forma como nos comunicamos.",
        "A educação no Brasil enfrenta desafios significativos que precisam ser abordados de forma estruturada.",
        "O aquecimento global representa uma das maiores ameaças ao meio ambiente e requer ação coordenada globalmente.",
        "Tecnologia moderna tem transformado a maneira como trabalhamos, estudamos e nos relacionamos socialmente.",
    ]

    logger.info("\n" + "=" * 60)
    logger.info("TESTE COM TEXTOS CUSTOMIZADOS")
    logger.info("=" * 60)

    logger.info("\n--- Textos Humanos ---")
    correct = 0
    for text in human_texts:
        pred, prob = predict(model, tokenizer, text)
        status = "OK" if pred == 0 else "ERRO"
        if pred == 0:
            correct += 1
        logger.info(f"[{status}] P(IA): {prob*100:5.1f}% | {text[:50]}...")
    logger.info(f"Acuracia Humanos: {correct}/{len(human_texts)} = {correct/len(human_texts)*100:.1f}%")

    logger.info("\n--- Textos IA ---")
    correct = 0
    for text in ai_texts:
        pred, prob = predict(model, tokenizer, text)
        status = "OK" if pred == 1 else "ERRO"
        if pred == 1:
            correct += 1
        logger.info(f"[{status}] P(IA): {prob*100:5.1f}% | {text[:50]}...")
    logger.info(f"Acuracia IA: {correct}/{len(ai_texts)} = {correct/len(ai_texts)*100:.1f}%")


if __name__ == "__main__":
    evaluate_dataset()
    test_custom_texts()


# "Medir e gerenciar." - Peter Drucker
