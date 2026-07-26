from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd

from src.ml.features import build_features
from src.ml.preprocessing import clean_dataframe
from src.ml.registry import ModelRegistry
from src.shared.logging import get_logger

logger = get_logger(__name__)


@dataclass
class TrainConfig:
    """Training configuration."""

    test_size: float = 0.2
    random_state: int = 42
    cv_folds: int = 5
    model_type: str = "linear"


@dataclass
class HyperparamConfig:
    """Hyperparameter search configuration."""

    enabled: bool = False
    method: str = "grid"  # grid, random
    n_iter: int = 10
    cv: int = 5
    scoring: str = "f1_weighted"
    param_grid: dict[str, list[Any]] = field(default_factory=lambda: {
        "n_estimators": [50, 100, 200],
        "max_depth": [5, 10, 20, None],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
    })


class BaseTrainer(ABC):
    """Abstract base class for all model trainers."""

    @abstractmethod
    def train(self, x: np.ndarray, y: np.ndarray, **kwargs: Any) -> dict[str, Any]:
        ...

    @abstractmethod
    def get_model(self) -> Any:
        ...

    @abstractmethod
    def get_params(self) -> dict[str, Any]:
        ...


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

    def cross_validate(self, x: np.ndarray, y: np.ndarray, model_name: str = "cv_model") -> dict[str, float]:
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


class CrimePatternTrainer(BaseTrainer):
    """Trainer for crime category prediction using scikit-learn with hyperparameter tuning."""

    def __init__(
        self,
        model_type: str = "random_forest",
        hyperparam_config: HyperparamConfig | None = None,
        registry: ModelRegistry | None = None,
        random_state: int = 42,
    ):
        self.model_type = model_type
        self.hyperparam_config = hyperparam_config or HyperparamConfig()
        self.registry = registry or ModelRegistry()
        self.random_state = random_state
        self._model: Any = None
        self._metrics: dict[str, Any] = {}
        self._params: dict[str, Any] = {}
        self._feature_importance: dict[str, float] = {}
        self._training_time: float = 0.0

    def train(
        self,
        x: np.ndarray,
        y: np.ndarray,
        feature_names: list[str] | None = None,
        model_name: str = "crime_pattern_model",
        **kwargs: Any,
    ) -> dict[str, Any]:
        from sklearn.model_selection import train_test_split

        self._params = {
            "model_type": self.model_type,
            "random_state": self.random_state,
            "hyperparam_tuning": self.hyperparam_config.enabled,
        }

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=self.random_state, stratify=y
        )

        start_time = time.time()

        if self.hyperparam_config.enabled:
            best_estimator = self._tune_hyperparameters(x_train, y_train)
            self._model = best_estimator
        else:
            self._model = self._build_model()
            self._model.fit(x_train, y_train)

        self._training_time = time.time() - start_time

        from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

        y_pred = self._model.predict(x_test)
        y_prob = None
        if hasattr(self._model, "predict_proba"):
            try:
                y_prob = self._model.predict_proba(x_test)
            except Exception:
                pass

        self._metrics = {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "precision_weighted": float(precision_score(y_test, y_pred, average="weighted", zero_division=0)),
            "recall_weighted": float(recall_score(y_test, y_pred, average="weighted", zero_division=0)),
            "f1_weighted": float(f1_score(y_test, y_pred, average="weighted", zero_division=0)),
            "training_time_seconds": round(self._training_time, 4),
            "n_features": x.shape[1],
            "n_samples": x.shape[0],
        }

        if len(np.unique(y)) == 2 and y_prob is not None:
            from sklearn.metrics import roc_auc_score
            try:
                self._metrics["roc_auc"] = float(roc_auc_score(y_test, y_prob[:, 1]))
            except (ValueError, IndexError):
                pass

        if hasattr(self._model, "feature_importances_"):
            importances = self._model.feature_importances_
            names = feature_names or [f"feature_{i}" for i in range(len(importances))]
            self._feature_importance = dict(zip(names[: len(importances)], importances.tolist()))
            self._metrics["top_features"] = sorted(
                self._feature_importance.items(), key=lambda x: x[1], reverse=True
            )[:10]
        elif hasattr(self._model, "coef_"):
            coefs = self._model.coef_
            if coefs.ndim > 1:
                coefs = coefs[0]
            names = feature_names or [f"feature_{i}" for i in range(len(coefs))]
            self._feature_importance = dict(zip(names[: len(coefs)], np.abs(coefs).tolist()))

        logger.info(
            "Training complete",
            extra={"model_name": model_name, "accuracy": self._metrics["accuracy"]},
        )
        return self._metrics

    def _build_model(self) -> Any:
        if self.model_type == "random_forest":
            from sklearn.ensemble import RandomForestClassifier
            return RandomForestClassifier(n_estimators=100, random_state=self.random_state, n_jobs=-1)
        elif self.model_type == "gradient_boosting":
            from sklearn.ensemble import GradientBoostingClassifier
            return GradientBoostingClassifier(n_estimators=100, random_state=self.random_state)
        elif self.model_type == "logistic_regression":
            from sklearn.linear_model import LogisticRegression
            return LogisticRegression(random_state=self.random_state, max_iter=1000, n_jobs=-1)
        elif self.model_type == "svm":
            from sklearn.svm import SVC
            return SVC(kernel="rbf", random_state=self.random_state, probability=True)
        elif self.model_type == "xgboost":
            try:
                from xgboost import XGBClassifier
                return XGBClassifier(n_estimators=100, random_state=self.random_state, n_jobs=-1)
            except ImportError:
                logger.warning("XGBoost not installed, falling back to RandomForest")
                from sklearn.ensemble import RandomForestClassifier
                return RandomForestClassifier(n_estimators=100, random_state=self.random_state, n_jobs=-1)
        else:
            from sklearn.ensemble import RandomForestClassifier
            return RandomForestClassifier(n_estimators=100, random_state=self.random_state, n_jobs=-1)

    def _tune_hyperparameters(self, x_train: np.ndarray, y_train: np.ndarray) -> Any:
        base_model = self._build_model()
        param_grid = self.hyperparam_config.param_grid

        if self.hyperparam_config.method == "random":
            from sklearn.model_selection import RandomizedSearchCV
            searcher = RandomizedSearchCV(
                base_model,
                param_grid,
                n_iter=self.hyperparam_config.n_iter,
                cv=self.hyperparam_config.cv,
                scoring=self.hyperparam_config.scoring,
                random_state=self.random_state,
                n_jobs=-1,
                verbose=0,
            )
        else:
            from sklearn.model_selection import GridSearchCV
            searcher = GridSearchCV(
                base_model,
                param_grid,
                cv=self.hyperparam_config.cv,
                scoring=self.hyperparam_config.scoring,
                n_jobs=-1,
                verbose=0,
            )

        searcher.fit(x_train, y_train)
        self._params["best_params"] = searcher.best_params_
        self._params["best_score"] = float(searcher.best_score_)
        logger.info("Hyperparameter tuning complete", extra={"best_params": searcher.best_params_})
        return searcher.best_estimator_

    def train_from_dataframe(
        self,
        df: pd.DataFrame,
        target_column: str = "CrimeMajorHeadID",
        feature_columns: list[str] | None = None,
        model_name: str = "crime_pattern_model",
        register: bool = True,
    ) -> dict[str, Any]:
        cleaned = clean_dataframe(df)
        features = build_features(cleaned)
        if target_column in features.columns:
            y = features[target_column].values
            x = features.drop(columns=[target_column]).select_dtypes(include=[np.number]).values
            feature_names = features.drop(columns=[target_column]).select_dtypes(include=[np.number]).columns.tolist()
        else:
            y = cleaned[target_column].values
            x = features.select_dtypes(include=[np.number]).values
            feature_names = features.select_dtypes(include=[np.number]).columns.tolist()

        metrics = self.train(x, y, feature_names=feature_names, model_name=model_name)

        if register:
            self.registry.register(
                name=model_name,
                model=self._model,
                metrics=self._metrics,
                params=self._params,
                model_type=self.model_type,
            )

        return {
            "metrics": metrics,
            "model_name": model_name,
            "n_features": x.shape[1],
            "n_samples": x.shape[0],
            "feature_importance": self._feature_importance,
        }

    def get_model(self) -> Any:
        return self._model

    def get_params(self) -> dict[str, Any]:
        return self._params

    def get_metrics(self) -> dict[str, Any]:
        return self._metrics

    def get_feature_importance(self) -> dict[str, float]:
        return self._feature_importance


def train_model_async(x, y, config: TrainConfig | None = None) -> dict[str, Any]:
    trainer = ModelTrainer(config)
    return trainer.train(x, y)
