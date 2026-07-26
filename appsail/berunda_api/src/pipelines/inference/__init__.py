from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.ml.inference import BatchPredictor, CrimePredictor, ModelRegistry
from src.pipelines.base import BasePipeline
from src.shared.logging import get_logger

logger = get_logger(__name__)


class InferencePipeline(BasePipeline):
    """Batch and real-time inference pipeline."""

    def __init__(self, registry: ModelRegistry | None = None):
        self.registry = registry or ModelRegistry()
        self.predictor = BatchPredictor(self.registry)
        self._status: dict[str, Any] = {"state": "idle", "last_run": None}

    def validate(self, **kwargs: Any) -> dict[str, Any]:
        issues = []
        model_name = kwargs.get("model_name", "")
        if model_name and self.registry.get(model_name) is None:
            issues.append(f"Model '{model_name}' not found in registry")
        return {"valid": len(issues) == 0, "issues": issues}

    def get_status(self) -> dict[str, Any]:
        return dict(self._status)

    async def run(self, model_name: str | None = None, data: pd.DataFrame | None = None, **kwargs: Any) -> dict:
        self._status["state"] = "running"
        resolved_model = model_name or kwargs.get("model_name", "")
        resolved_data = data if data is not None else kwargs.get("data", pd.DataFrame())
        if isinstance(resolved_data, dict):
            resolved_data = pd.DataFrame(resolved_data)

        if not resolved_model:
            raise ValueError("model_name is required")

        predictions = await self.batch_predict(resolved_model, resolved_data)
        self._status = {"state": "completed", "last_run": __import__("time").time()}
        return {
            "predictions": predictions.tolist(),
            "model_name": resolved_model,
            "n_records": len(predictions),
        }

    async def batch_predict(self, model_name: str, data: pd.DataFrame) -> np.ndarray:
        return self.predictor.predict(model_name, data)

    async def single_predict(self, model_name: str, features: dict) -> Any:
        model = self.registry.get(model_name)
        if model is None:
            raise ValueError(f"Model '{model_name}' not found")
        import numpy as np
        x = np.array([list(features.values())])
        return model.predict(x)[0]


async def predict(state: dict) -> dict:
    pipeline = InferencePipeline()
    model_name = state.get("model_name", "")
    data = state.get("data", pd.DataFrame())
    if isinstance(data, dict):
        data = pd.DataFrame(data)
    result = await pipeline.run(model_name=model_name, data=data)
    return {"predictions": result.get("predictions", [])}
