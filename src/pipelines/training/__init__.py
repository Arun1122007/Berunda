"""Pipeline training utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from src.ml.training import ModelTrainer, TrainConfig


@dataclass
class TrainingPipelineConfig:
    """Configuration for training pipeline."""

    model_type: str = "linear"
    test_size: float = 0.2
    cv_folds: int = 5
    random_state: int = 42


class TrainingPipeline:
    """End-to-end model training pipeline."""

    def __init__(self, config: TrainingPipelineConfig | None = None):
        self.config = config or TrainingPipelineConfig()
        self.trainer = ModelTrainer(
            TrainConfig(
                test_size=self.config.test_size,
                random_state=self.config.random_state,
                cv_folds=self.config.cv_folds,
                model_type=self.config.model_type,
            )
        )

    async def run(
        self, x: np.ndarray, y: np.ndarray, model_name: str | None = None
    ) -> dict[str, Any]:
        metrics = self.trainer.train(x, y, model_name)
        cv_results = self.trainer.cross_validate(x, y)

        return {
            "train_metrics": metrics,
            "cross_validation": cv_results,
            "model_type": self.config.model_type,
        }


async def train_model(state: dict) -> dict:
    config = TrainingPipelineConfig(**state.get("training_config", {}))
    pipeline = TrainingPipeline(config)
    x = state.get("X")
    y = state.get("y")
    if x is None or y is None:
        return {"error": "Missing X or y in state"}
    return {"training_result": await pipeline.run(np.array(x), np.array(y))}
