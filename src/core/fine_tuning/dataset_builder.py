from __future__ import annotations

import json
import logging
import os
import random
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import config

logger = logging.getLogger(__name__)

DATASET_DIR = config.DATA_DIR / "fine_tuning"


class DatasetBuilder:
    def __init__(self) -> None:
        os.makedirs(DATASET_DIR, exist_ok=True)
        self.human_samples: list[dict[str, Any]] = []
        self.ai_samples: list[dict[str, Any]] = []

    def collect_human_samples_wikipedia(self, num_samples: int = 1000) -> int:
        logger.info(f"Coletando {num_samples} amostras da Wikipedia PT...")

        try:
            from datasets import load_dataset

            dataset = load_dataset(
                "wikipedia",
                "20220301.pt",
                split=f"train[:{num_samples}]",
                cache_dir=str(config.HF_HOME),
            )

            count = 0
            for item in dataset:
                text = item.get("text", "")
                if len(text) > 200:
                    paragraphs = text.split("\n\n")
                    for para in paragraphs[:2]:
                        if 100 < len(para) < 2000:
                            self.human_samples.append({
                                "text": para.strip(),
                                "label": 0,
                                "source": "wikipedia-pt",
                            })
                            count += 1

            logger.info(f"Coletadas {count} amostras da Wikipedia.")
            return count

        except Exception as e:
            logger.error(f"Falha ao coletar Wikipedia: {e}")
            return 0

    def collect_human_samples_news(self, num_samples: int = 500) -> int:
        logger.info(f"Coletando {num_samples} amostras de noticias PT...")

        try:
            from datasets import load_dataset

            dataset = load_dataset(
                "cnn_dailymail",
                "3.0.0",
                split=f"train[:{num_samples}]",
                cache_dir=str(config.HF_HOME),
            )

            count = 0
            for item in dataset:
                text = item.get("article", "")
                if 200 < len(text) < 3000:
                    self.human_samples.append({
                        "text": text[:2000].strip(),
                        "label": 0,
                        "source": "news",
                    })
                    count += 1

            logger.info(f"Coletadas {count} amostras de noticias.")
            return count

        except Exception as e:
            logger.error(f"Falha ao coletar noticias: {e}")
            return 0

    def generate_ai_samples_groq(self, num_samples: int = 500) -> int:
        if not config.GROQ_API_KEY:
            logger.warning("GROQ_API_KEY nao configurada.")
            return 0

        logger.info(f"Gerando {num_samples} amostras com Groq...")

        try:
            from groq import Groq
            client = Groq(api_key=config.GROQ_API_KEY)

            prompts = [
                "Escreva um paragrafo sobre a importancia da educacao no Brasil.",
                "Explique como funciona o sistema de saude publico brasileiro.",
                "Descreva os principais pontos turisticos do Rio de Janeiro.",
                "Fale sobre a historia do futebol brasileiro.",
                "Explique o que e inteligencia artificial e suas aplicacoes.",
                "Descreva o processo de reciclagem e sua importancia ambiental.",
                "Fale sobre a culinaria tipica do Nordeste brasileiro.",
                "Explique como funciona o mercado financeiro.",
                "Descreva as principais caracteristicas da Amazonia.",
                "Fale sobre a importancia da leitura para o desenvolvimento pessoal.",
            ]

            count = 0
            samples_per_prompt = num_samples // len(prompts)

            for prompt in prompts:
                for _ in range(samples_per_prompt):
                    try:
                        response = client.chat.completions.create(
                            model=config.GROQ_MODEL,
                            messages=[
                                {"role": "user", "content": prompt},
                            ],
                            temperature=0.9,
                            max_tokens=500,
                        )

                        text = response.choices[0].message.content
                        if text and len(text) > 100:
                            self.ai_samples.append({
                                "text": text.strip(),
                                "label": 1,
                                "source": "groq-llama",
                            })
                            count += 1

                    except Exception as e:
                        logger.warning(f"Falha ao gerar amostra Groq: {e}")
                        continue

            logger.info(f"Geradas {count} amostras com Groq.")
            return count

        except ImportError:
            logger.error("Pacote 'groq' nao instalado.")
            return 0

    def generate_ai_samples_gemini(self, num_samples: int = 500) -> int:
        if not config.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY nao configurada.")
            return 0

        logger.info(f"Gerando {num_samples} amostras com Gemini...")

        try:
            import google.generativeai as genai
            genai.configure(api_key=config.GEMINI_API_KEY)
            model = genai.GenerativeModel(config.GEMINI_MODEL)

            prompts = [
                "Escreva sobre tecnologia e inovacao no Brasil.",
                "Fale sobre mudancas climaticas e seus impactos.",
                "Explique a importancia da preservacao cultural.",
                "Descreva o cenario economico atual do pais.",
                "Fale sobre avancos na medicina moderna.",
            ]

            count = 0
            samples_per_prompt = num_samples // len(prompts)

            for prompt in prompts:
                for _ in range(samples_per_prompt):
                    try:
                        response = model.generate_content(prompt)
                        text = response.text

                        if text and len(text) > 100:
                            self.ai_samples.append({
                                "text": text.strip(),
                                "label": 1,
                                "source": "gemini",
                            })
                            count += 1

                    except Exception as e:
                        logger.warning(f"Falha ao gerar amostra Gemini: {e}")
                        continue

            logger.info(f"Geradas {count} amostras com Gemini.")
            return count

        except ImportError:
            logger.error("Pacote 'google-generativeai' nao instalado.")
            return 0

    def build_dataset(
        self,
        train_ratio: float = 0.8,
        val_ratio: float = 0.1,
    ) -> dict[str, list[dict[str, Any]]]:
        all_samples = self.human_samples + self.ai_samples
        random.shuffle(all_samples)

        total = len(all_samples)
        train_end = int(total * train_ratio)
        val_end = int(total * (train_ratio + val_ratio))

        dataset = {
            "train": all_samples[:train_end],
            "validation": all_samples[train_end:val_end],
            "test": all_samples[val_end:],
        }

        for split_name, samples in dataset.items():
            path = DATASET_DIR / f"{split_name}.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(samples, f, ensure_ascii=False, indent=2)
            logger.info(f"Salvo {split_name}: {len(samples)} amostras em {path}")

        stats = {
            "total": total,
            "human": len(self.human_samples),
            "ai": len(self.ai_samples),
            "train": len(dataset["train"]),
            "validation": len(dataset["validation"]),
            "test": len(dataset["test"]),
        }

        with open(DATASET_DIR / "stats.json", "w") as f:
            json.dump(stats, f, indent=2)

        logger.info(f"Dataset criado: {stats}")
        return dataset

    def load_dataset(self) -> dict[str, list[dict[str, Any]]]:
        dataset = {}
        for split in ["train", "validation", "test"]:
            path = DATASET_DIR / f"{split}.json"
            if path.exists():
                with open(path, encoding="utf-8") as f:
                    dataset[split] = json.load(f)
        return dataset


def build_fine_tuning_dataset() -> None:
    builder = DatasetBuilder()

    builder.collect_human_samples_wikipedia(1000)
    builder.generate_ai_samples_groq(500)
    builder.generate_ai_samples_gemini(500)

    builder.build_dataset()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    build_fine_tuning_dataset()


# "Dados sao o novo petroleo." - Clive Humby
