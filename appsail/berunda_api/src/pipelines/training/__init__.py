from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from src.ml.evaluation import ClassificationEvaluator
from src.ml.features import build_features, get_feature_names
from src.ml.preprocessing import clean_dataframe
from src.ml.registry import ModelRegistry
from src.ml.training import CrimePatternTrainer, HyperparamConfig, ModelTrainer, TrainConfig
from src.pipelines.base import BasePipeline
from src.shared.logging import get_logger

logger = get_logger(__name__)


@dataclass
class TrainingPipelineConfig:
    """Configuration for training pipeline."""

    model_type: str = "random_forest"
    test_size: float = 0.2
    cv_folds: int = 5
    random_state: int = 42
    target_column: str = "CrimeMajorHeadID"
    hyperparameter_tuning: bool = False
    model_name: str = "crime_pattern_model"


class TrainingPipeline(BasePipeline):
    """End-to-end model training pipeline orchestrating all steps."""

    def __init__(self, config: TrainingPipelineConfig | None = None):
        self.config = config or TrainingPipelineConfig()
        self._status: dict[str, Any] = {"state": "idle", "last_run": None}
        self.trainer: CrimePatternTrainer | None = None
        self.evaluator = ClassificationEvaluator()
        self.registry = ModelRegistry()

    def validate(self, **kwargs: Any) -> dict[str, Any]:
        issues = []
        if self.config.model_type not in ("random_forest", "gradient_boosting", "logistic_regression", "svm"):
            issues.append(f"Unknown model type: {self.config.model_type}")
        return {"valid": len(issues) == 0, "issues": issues}

    def get_status(self) -> dict[str, Any]:
        return dict(self._status)

    async def run(self, df: pd.DataFrame | None = None, **kwargs: Any) -> dict[str, Any]:
        self._status["state"] = "running"
        data = df if df is not None else kwargs.get("data", pd.DataFrame())
        if isinstance(data, dict):
            data = pd.DataFrame(data)

        logger.info("Training pipeline started", extra={"rows": len(data)})

        cleaned = clean_dataframe(data)
        features = build_features(cleaned)

        target = self.config.target_column
        if target in features.columns:
            y = features[target].values
            x = features.drop(columns=[target]).select_dtypes(include=[np.number]).values
            feature_names = features.drop(columns=[target]).select_dtypes(include=[np.number]).columns.tolist()
        elif target in cleaned.columns:
            y = cleaned[target].values
            x = features.select_dtypes(include=[np.number]).values
            feature_names = features.select_dtypes(include=[np.number]).columns.tolist()
        else:
            raise ValueError(f"Target column '{target}' not found in data")

        hyperparam_config = HyperparamConfig(enabled=self.config.hyperparameter_tuning)
        self.trainer = CrimePatternTrainer(
            model_type=self.config.model_type,
            hyperparam_config=hyperparam_config,
            random_state=self.config.random_state,
        )

        train_result = self.trainer.train(
            x, y,
            feature_names=feature_names,
            model_name=self.config.model_name,
        )

        self.registry.register(
            name=self.config.model_name,
            model=self.trainer.get_model(),
            metrics=self.trainer.get_metrics(),
            params=self.trainer.get_params(),
            model_type=self.config.model_type,
        )

        from sklearn.model_selection import train_test_split
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=self.config.test_size, random_state=self.config.random_state
        )
        y_pred = self.trainer.get_model().predict(x_test)
        y_prob = None
        if hasattr(self.trainer.get_model(), "predict_proba"):
            try:
                y_prob = self.trainer.get_model().predict_proba(x_test)
            except Exception:
                pass

        eval_result = self.evaluator.evaluate(y_test, y_pred, y_prob)

        self._status = {"state": "completed", "last_run": __import__("time").time()}
        return {
            "training_metrics": train_result,
            "evaluation": eval_result,
            "feature_importance": self.trainer.get_feature_importance(),
            "feature_names": feature_names,
            "model_name": self.config.model_name,
            "model_type": self.config.model_type,
            "n_samples": x.shape[0],
            "n_features": x.shape[1],
        }


async def train_model(state: dict) -> dict:
    config = TrainingPipelineConfig(**state.get("training_config", {}))
    pipeline = TrainingPipeline(config)
    x = np.asarray(state.get("X", []))
    y = np.asarray(state.get("y", []))
    if x.size == 0 or y.size == 0:
        return {"error": "Missing X or y in state"}
    cols = [f"feat_{i}" for i in range(x.shape[1])] + ["CrimeMajorHeadID"]
    df = pd.DataFrame(np.column_stack([x, y]), columns=cols)
    return {"training_result": await pipeline.run(df)}
