"""ML inference engine."""

from __future__ import annotations

import threading
from typing import Any

import numpy as np
import pandas as pd


class ModelRegistry:
    """Thread-safe singleton model registry."""

    _instance: ModelRegistry | None = None
    _lock = threading.Lock()
    _models: dict[str, dict[str, Any]]

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._models: dict[str, dict[str, Any]] = {}
        return cls._instance

    def register(self, name: str, model: Any, metadata: dict | None = None) -> None:
        self._models[name] = {
            "model": model,
            "metadata": metadata or {},
        }

    def get(self, name: str) -> Any | None:
        entry = self._models.get(name)
        return entry["model"] if entry else None

    def list_models(self) -> dict[str, dict]:
        return {name: {"name": name, **entry["metadata"]} for name, entry in self._models.items()}

    def deregister(self, name: str) -> bool:
        return bool(self._models.pop(name, None))


class BatchPredictor:
    """Run batch predictions on DataFrames."""

    def __init__(self, registry: ModelRegistry | None = None):
        self.registry = registry or ModelRegistry()

    def predict(self, model_name: str, data: pd.DataFrame) -> np.ndarray:
        model = self.registry.get(model_name)
        if model is None:
            raise ValueError(f"Model '{model_name}' not found")
        return model.predict(data.values)


def predict_model(model_name: str, data: pd.DataFrame) -> np.ndarray:
    """Convenience function for prediction."""
    registry = ModelRegistry()
    predictor = BatchPredictor(registry)
    return predictor.predict(model_name, data)
