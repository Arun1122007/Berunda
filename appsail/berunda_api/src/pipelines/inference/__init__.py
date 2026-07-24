from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.ml.inference import BatchPredictor, ModelRegistry


class InferencePipeline:
    """Batch and real-time inference pipeline."""

    def __init__(self):
        self.registry = ModelRegistry()
        self.predictor = BatchPredictor(self.registry)

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
    """Convenience function for Pipeline compatibility."""
    pipeline = InferencePipeline()
    model_name = state.get("model_name", "")
    data = state.get("data", pd.DataFrame())
    if isinstance(data, dict):
        data = pd.DataFrame(data)
    predictions = await pipeline.batch_predict(model_name, data)
    return {"predictions": predictions.tolist()}
