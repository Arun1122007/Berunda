from __future__ import annotations

import threading
from typing import Any

import numpy as np
import pandas as pd

from src.ml.features import build_features, get_feature_names
from src.ml.preprocessing import clean_dataframe
from src.ml.registry import ModelRegistry as _ModelRegistryPersistent
from src.shared.logging import get_logger

logger = get_logger(__name__)

try:
    import shap
    _SHAP_AVAILABLE = True
except ImportError:
    _SHAP_AVAILABLE = False
    shap = None


class ModelRegistry:
    """Thread-safe singleton model registry (in-memory)."""

    _instance: ModelRegistry | None = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._models: dict[str, dict[str, Any]] = {}
        return cls._instance

    def register(self, name: str, model: Any, metadata: dict | None = None) -> None:
        self._models[name] = {"model": model, "metadata": metadata or {}}

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
            raise ValueError(f"Model '{model_name}' not found in registry")
        return model.predict(data.values)


class CrimePredictor:
    """End-to-end predictor: load -> preprocess -> predict -> explain."""

    def __init__(
        self,
        model_name: str,
        registry: _ModelRegistryPersistent | None = None,
    ):
        self.model_name = model_name
        self.registry = registry or _ModelRegistryPersistent()
        self._model: Any = None
        self._metadata: dict[str, Any] = {}
        self._loaded = False

    def load(self, version: str | None = None) -> None:
        self._model, self._metadata = self.registry.load(self.model_name, version)
        self._loaded = True
        logger.info("Model loaded for inference", extra={"model": self.model_name})

    def predict(self, df: pd.DataFrame, return_proba: bool = True) -> dict[str, Any]:
        if not self._loaded:
            self.load()
        preprocessed = self._preprocess(df)
        x = preprocessed.values
        predictions = self._model.predict(x)
        result: dict[str, Any] = {
            "predictions": predictions.tolist(),
            "n_records": len(predictions),
        }
        if return_proba and hasattr(self._model, "predict_proba"):
            try:
                proba = self._model.predict_proba(x)
                result["probabilities"] = proba.tolist()
                result["confidence_scores"] = [
                    float(max(p)) for p in proba
                ]
            except Exception as exc:
                logger.warning("Probability prediction failed", exc_info=exc)
        return result

    def predict_single(self, record: dict[str, Any]) -> dict[str, Any]:
        df = pd.DataFrame([record])
        result = self.predict(df)
        return {k: v[0] if isinstance(v, list) and v else v for k, v in result.items()}

    def _preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        cleaned = clean_dataframe(df)
        features = build_features(cleaned)
        numeric_cols = features.select_dtypes(include=[np.number]).columns.tolist()
        expected = get_feature_names()
        for col in expected:
            if col not in numeric_cols:
                features[col] = 0.0
        feature_cols = [c for c in expected if c in features.columns]
        return features[feature_cols].fillna(0)


class PredictionExplanation:
    """Explain model predictions using SHAP or fallback methods."""

    def __init__(self, model: Any, feature_names: list[str] | None = None):
        self.model = model
        self.feature_names = feature_names or []
        self._explainer: Any = None
        self._method: str = "unknown"

    def fit(self, background_data: np.ndarray | None = None) -> PredictionExplanation:
        if _SHAP_AVAILABLE:
            try:
                if hasattr(self.model, "predict_proba"):
                    self._explainer = shap.TreeExplainer(self.model) if "Tree" in type(self.model).__name__ else shap.KernelExplainer(self.model.predict_proba, background_data or np.zeros((100, len(self.feature_names) or 10)))
                else:
                    self._explainer = shap.TreeExplainer(self.model) if "Tree" in type(self.model).__name__ else shap.KernelExplainer(self.model.predict, background_data or np.zeros((100, len(self.feature_names) or 10)))
                self._method = "shap"
                logger.info("SHAP explainer initialized")
            except Exception as exc:
                logger.warning("SHAP explainer init failed, using fallback", exc_info=exc)
                self._method = "coefficient"
        else:
            self._method = self._detect_fallback_method()
        return self

    def explain(self, x: np.ndarray) -> dict[str, Any]:
        if self._method == "shap" and self._explainer is not None:
            return self._shap_explain(x)
        elif self._method == "coefficient":
            return self._coeff_explain(x)
        elif self._method == "permutation":
            return self._permutation_explain(x)
        return {"method": "none", "error": "No explanation method available", "feature_importance": {}}

    def _shap_explain(self, x: np.ndarray) -> dict[str, Any]:
        shap_values = self._explainer.shap_values(x)
        if isinstance(shap_values, list):
            shap_values = shap_values[0]
        if shap_values.ndim > 2:
            shap_values = shap_values[:, :, 0]
        feature_importance = {}
        for i in range(min(shap_values.shape[1], len(self.feature_names or []))):
            feature_importance[self.feature_names[i]] = float(np.abs(shap_values[:, i]).mean())
        return {
            "method": "shap",
            "shap_values": shap_values.tolist() if hasattr(shap_values, "tolist") else shap_values,
                "feature_importance": feature_importance,
        }

    def _coeff_explain(self, x: np.ndarray) -> dict[str, Any]:
        if hasattr(self.model, "coef_"):
            coefs = self.model.coef_
            if coefs.ndim > 1:
                coefs = coefs[0]
            feature_importance = {}
            for i in range(min(len(coefs), len(self.feature_names or []))):
                feature_importance[self.feature_names[i]] = float(abs(coefs[i]))
            return {"method": "coefficient", "feature_importance": feature_importance}
        return self._permutation_explain(x)

    def _permutation_explain(self, x: np.ndarray) -> dict[str, Any]:
        from sklearn.inspection import permutation_importance
        result = permutation_importance(self.model, x, np.zeros(x.shape[0]), n_repeats=5, random_state=42)
        feature_importance = {}
        for i in range(min(len(result.importances_mean), len(self.feature_names or []))):
            feature_importance[self.feature_names[i]] = float(result.importances_mean[i])
        return {"method": "permutation", "feature_importance": feature_importance}

    def _detect_fallback_method(self) -> str:
        if hasattr(self.model, "coef_") or hasattr(self.model, "feature_importances_"):
            return "coefficient"
        return "permutation"


def predict_model(model_name: str, data: pd.DataFrame) -> np.ndarray:
    """Convenience function for prediction."""
    registry = ModelRegistry()
    predictor = BatchPredictor(registry)
    return predictor.predict(model_name, data)
