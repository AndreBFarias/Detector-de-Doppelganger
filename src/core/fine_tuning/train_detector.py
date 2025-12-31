from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import torch
from torch.utils.data import Dataset
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments,
)

import config

logger = logging.getLogger(__name__)

DATASET_DIR = config.DATA_DIR / "fine_tuning"
MODEL_OUTPUT_DIR = config.MODELS_DIR / "detector_pt_finetuned"


class AIDetectorDataset(Dataset):
    def __init__(
        self,
        samples: list[dict[str, Any]],
        tokenizer: Any,
        max_length: int = 512,
    ) -> None:
        self.samples = samples
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        sample = self.samples[idx]
        text = sample["text"]
        label = sample["label"]

        encoding = self.tokenizer(
            text,
            truncation=True,
            max_length=self.max_length,
            padding="max_length",
            return_tensors="pt",
        )

        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels": torch.tensor(label, dtype=torch.long),
        }


class DetectorTrainer:
    def __init__(
        self,
        base_model: str = "xlm-roberta-large",
        learning_rate: float = 2e-5,
        batch_size: int = 8,
        epochs: int = 3,
        warmup_steps: int = 500,
        weight_decay: float = 0.01,
        fp16: bool = True,
        gradient_accumulation_steps: int = 4,
    ) -> None:
        self.base_model = base_model
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.epochs = epochs
        self.warmup_steps = warmup_steps
        self.weight_decay = weight_decay
        self.fp16 = False
        self.gradient_accumulation_steps = gradient_accumulation_steps

        self.tokenizer: Any = None
        self.model: Any = None
        self.device = torch.device("cpu")

        logger.info(f"Trainer inicializado. Device: {self.device}")

    def load_base_model(self) -> bool:
        logger.info(f"Carregando modelo base: {self.base_model}")

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.base_model,
                cache_dir=str(config.HF_HOME),
            )

            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.base_model,
                num_labels=2,
                cache_dir=str(config.HF_HOME),
            )

            logger.info("Modelo base carregado com sucesso.")
            return True

        except Exception as e:
            logger.error(f"Falha ao carregar modelo base: {e}")
            return False

    def load_dataset(self) -> tuple[list[dict], list[dict], list[dict]] | None:
        logger.info("Carregando dataset...")

        try:
            train_path = DATASET_DIR / "train.json"
            val_path = DATASET_DIR / "validation.json"
            test_path = DATASET_DIR / "test.json"

            with open(train_path, encoding="utf-8") as f:
                train_data = json.load(f)
            with open(val_path, encoding="utf-8") as f:
                val_data = json.load(f)
            with open(test_path, encoding="utf-8") as f:
                test_data = json.load(f)

            logger.info(
                f"Dataset carregado: train={len(train_data)}, "
                f"val={len(val_data)}, test={len(test_data)}"
            )

            return train_data, val_data, test_data

        except Exception as e:
            logger.error(f"Falha ao carregar dataset: {e}")
            return None

    def train(self) -> bool:
        if not self.load_base_model():
            return False

        dataset_result = self.load_dataset()
        if dataset_result is None:
            return False

        train_data, val_data, _ = dataset_result

        train_dataset = AIDetectorDataset(train_data, self.tokenizer)
        val_dataset = AIDetectorDataset(val_data, self.tokenizer)

        os.makedirs(MODEL_OUTPUT_DIR, exist_ok=True)

        training_args = TrainingArguments(
            output_dir=str(MODEL_OUTPUT_DIR),
            num_train_epochs=self.epochs,
            per_device_train_batch_size=self.batch_size,
            per_device_eval_batch_size=self.batch_size,
            gradient_accumulation_steps=self.gradient_accumulation_steps,
            learning_rate=self.learning_rate,
            warmup_steps=self.warmup_steps,
            weight_decay=self.weight_decay,
            fp16=self.fp16,
            use_cpu=True,
            eval_strategy="steps",
            eval_steps=50,
            save_strategy="steps",
            save_steps=50,
            save_total_limit=2,
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            greater_is_better=False,
            logging_dir=str(config.LOGS_DIR / "training"),
            logging_steps=25,
            report_to="none",
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
        )

        logger.info("Iniciando treinamento...")

        try:
            trainer.train()

            logger.info(f"Salvando modelo em {MODEL_OUTPUT_DIR}...")
            trainer.save_model(str(MODEL_OUTPUT_DIR))
            self.tokenizer.save_pretrained(str(MODEL_OUTPUT_DIR))

            logger.info("Treinamento concluido com sucesso!")
            return True

        except Exception as e:
            logger.error(f"Falha no treinamento: {e}")
            return False


def train_detector() -> None:
    trainer = DetectorTrainer(
        base_model="distilbert-base-multilingual-cased",
        learning_rate=3e-5,
        batch_size=16,
        epochs=5,
        warmup_steps=100,
        weight_decay=0.05,
        gradient_accumulation_steps=2,
    )

    trainer.train()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    train_detector()


# "A pratica leva a perfeicao." - Proverbio
