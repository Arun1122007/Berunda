"""ML model training utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass
class TrainConfig:
    """Training configuration."""

    test_size: float = 0.2
    random_state: int = 42
    cv_folds: int = 5
    model_type: str = "linear"  # baseline, linear, ensemble


class ModelTrainer:
    """Train ML models with validation and evaluation."""

    def __init__(self, config: TrainConfig | None = None):
        self.config = config or TrainConfig()
        self.models: dict[str, Any] = {}

    def train_test_split(self, x: np.ndarray, y: np.ndarray) -> tuple:
        from sklearn.model_selection import train_test_split as tts

        return tts(x, y, test_size=self.config.test_size, random_state=self.config.random_state)

    def train(self, x: np.ndarray, y: np.ndarray, model_name: str | None = None) -> dict[str, Any]:
        name = model_name or f"model_{len(self.models)}"
        x_train, x_test, y_train, y_test = self.train_test_split(x, y)

        model = self._create_model()
        model.fit(x_train, y_train)

        train_score = model.score(x_train, y_train)
        test_score = model.score(x_test, y_test)

        metrics = {
            "train_score": float(train_score),
            "test_score": float(test_score),
            "overfit_gap": float(train_score - test_score),
        }

        self.models[name] = {"model": model, "metrics": metrics}
        return metrics

    def cross_validate(
        self,
        x: np.ndarray,
        y: np.ndarray,
        model_name: str = "cv_model",
    ) -> dict[str, float]:
        from sklearn.model_selection import cross_val_score

        model = self._create_model()
        scores = cross_val_score(model, x, y, cv=self.config.cv_folds)
        return {
            "mean_score": float(scores.mean()),
            "std_score": float(scores.std()),
            "scores": scores.tolist(),
        }

    def _create_model(self):
        if self.config.model_type == "baseline":
            from sklearn.dummy import DummyClassifier

            return DummyClassifier(strategy="most_frequent")
        elif self.config.model_type == "linear":
            from sklearn.linear_model import LogisticRegression

            return LogisticRegression(random_state=self.config.random_state)
        elif self.config.model_type == "ensemble":
            from sklearn.ensemble import RandomForestClassifier

            return RandomForestClassifier(n_estimators=100, random_state=self.config.random_state)
        else:
            raise ValueError(f"Unknown model type: {self.config.model_type}")

    def get_model(self, name: str) -> Any | None:
        entry = self.models.get(name)
        return entry["model"] if entry else None


def train_model_async(x, y, config: TrainConfig | None = None) -> dict[str, Any]:
    trainer = ModelTrainer(config)
    return trainer.train(x, y)
