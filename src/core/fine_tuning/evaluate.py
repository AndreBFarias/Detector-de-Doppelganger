from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import torch
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from transformers import pipeline

import config

logger = logging.getLogger(__name__)

DATASET_DIR = config.DATA_DIR / "fine_tuning"
MODEL_OUTPUT_DIR = config.MODELS_DIR / "detector_pt_finetuned"


class DetectorEvaluator:
    def __init__(self, model_path: str | None = None) -> None:
        self.model_path = model_path or str(MODEL_OUTPUT_DIR)
        self.pipeline: Any = None
        self.device = 0 if torch.cuda.is_available() else -1

    def load_model(self) -> bool:
        logger.info(f"Carregando modelo de {self.model_path}...")

        try:
            self.pipeline = pipeline(
                "text-classification",
                model=self.model_path,
                tokenizer=self.model_path,
                device=self.device,
            )
            logger.info("Modelo carregado com sucesso.")
            return True

        except Exception as e:
            logger.error(f"Falha ao carregar modelo: {e}")
            return False

    def load_test_data(self) -> list[dict[str, Any]] | None:
        test_path = DATASET_DIR / "test.json"

        try:
            with open(test_path, encoding="utf-8") as f:
                data = json.load(f)
            logger.info(f"Carregadas {len(data)} amostras de teste.")
            return data

        except Exception as e:
            logger.error(f"Falha ao carregar dados de teste: {e}")
            return None

    def predict(self, text: str) -> int:
        if self.pipeline is None:
            return -1

        try:
            result = self.pipeline(text, truncation=True, max_length=512)[0]
            label = result["label"]

            if label in ("LABEL_1", "Fake", "AI"):
                return 1
            return 0

        except Exception as e:
            logger.warning(f"Falha na predicao: {e}")
            return -1

    def evaluate(self) -> dict[str, float] | None:
        if not self.load_model():
            return None

        test_data = self.load_test_data()
        if test_data is None:
            return None

        y_true = []
        y_pred = []

        logger.info("Executando predicoes...")

        for i, sample in enumerate(test_data):
            text = sample["text"]
            true_label = sample["label"]

            pred_label = self.predict(text)

            if pred_label != -1:
                y_true.append(true_label)
                y_pred.append(pred_label)

            if (i + 1) % 100 == 0:
                logger.info(f"Processadas {i + 1}/{len(test_data)} amostras...")

        if not y_true:
            logger.error("Nenhuma predicao valida.")
            return None

        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1": f1_score(y_true, y_pred, zero_division=0),
        }

        cm = confusion_matrix(y_true, y_pred)
        metrics["confusion_matrix"] = cm.tolist()

        logger.info("=" * 50)
        logger.info("RESULTADOS DA AVALIACAO")
        logger.info("=" * 50)
        logger.info(f"Accuracy:  {metrics['accuracy']:.4f}")
        logger.info(f"Precision: {metrics['precision']:.4f}")
        logger.info(f"Recall:    {metrics['recall']:.4f}")
        logger.info(f"F1-Score:  {metrics['f1']:.4f}")
        logger.info("=" * 50)
        logger.info("Matriz de Confusao:")
        logger.info(f"  TN={cm[0][0]} FP={cm[0][1]}")
        logger.info(f"  FN={cm[1][0]} TP={cm[1][1]}")
        logger.info("=" * 50)

        results_path = MODEL_OUTPUT_DIR / "evaluation_results.json"
        with open(results_path, "w") as f:
            json.dump(metrics, f, indent=2)
        logger.info(f"Resultados salvos em {results_path}")

        return metrics

    def compare_models(self, models: list[str]) -> dict[str, dict[str, float]]:
        results = {}

        for model_path in models:
            logger.info(f"\nAvaliando modelo: {model_path}")
            self.model_path = model_path

            metrics = self.evaluate()
            if metrics:
                results[model_path] = metrics

        logger.info("\n" + "=" * 60)
        logger.info("COMPARACAO DE MODELOS")
        logger.info("=" * 60)

        for model_name, metrics in results.items():
            logger.info(f"\n{model_name}:")
            logger.info(f"  Accuracy: {metrics['accuracy']:.4f}")
            logger.info(f"  F1-Score: {metrics['f1']:.4f}")

        return results


def evaluate_detector() -> None:
    evaluator = DetectorEvaluator()
    evaluator.evaluate()


def compare_detectors() -> None:
    models = [
        "roberta-base-openai-detector",
        "roberta-large-openai-detector",
        str(MODEL_OUTPUT_DIR),
    ]

    evaluator = DetectorEvaluator()
    evaluator.compare_models(models)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    evaluate_detector()


# "A medida de inteligencia e a habilidade de mudar." - Albert Einstein
