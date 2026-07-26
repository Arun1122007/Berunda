"""Tests for ml.inference module."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.ml.inference import (
    BatchPredictor,
    CrimePredictor,
    ModelRegistry,
    PredictionExplanation,
    predict_model,
)


class TestModelRegistry:
    def test_singleton(self):
        r1 = ModelRegistry()
        r2 = ModelRegistry()
        assert r1 is r2

    def test_register_and_get(self):
        registry = ModelRegistry()
        registry.register("test", {"dummy": True})
        model = registry.get("test")
        assert model is not None

    def test_get_missing_returns_none(self):
        registry = ModelRegistry()
        assert registry.get("missing") is None

    def test_list_models(self):
        registry = ModelRegistry()
        registry.register("a", {"x": 1})
        models = registry.list_models()
        assert "a" in models

    def test_deregister(self):
        registry = ModelRegistry()
        registry.register("a", {})
        assert registry.deregister("a") is True
        assert registry.deregister("a") is False


class TestBatchPredictor:
    def test_predict(self):
        class DummyModel:
            def predict(self, data):
                return np.array([1, 0])

        registry = ModelRegistry()
        registry.register("dummy", DummyModel())
        predictor = BatchPredictor(registry)
        result = predictor.predict("dummy", pd.DataFrame({"a": [1, 2]}))
        assert len(result) == 2

    def test_predict_missing_model_raises(self):
        predictor = BatchPredictor()
        with pytest.raises(ValueError, match="not found"):
            predictor.predict("missing", pd.DataFrame())


class TestCrimePredictor:
    def test_load_and_predict_with_persistent_registry(self, tmp_path):
        from src.ml.registry import ModelRegistry as PersistentRegistry
        from sklearn.dummy import DummyClassifier

        p_registry = PersistentRegistry(str(tmp_path / "reg"))
        dummy = DummyClassifier(strategy="most_frequent")
        dummy.fit(np.array([[1, 2], [3, 4]]), np.array([0, 1]))
        p_registry.register("crime_model", model=dummy)

        predictor = CrimePredictor("crime_model", registry=p_registry)
        predictor.load()
        df = pd.DataFrame({"feat1": [1, 3], "feat2": [2, 4]})
        result = predictor.predict(df, return_proba=True)
        assert "predictions" in result
        assert "confidence_scores" in result

    def test_predict_single(self, tmp_path):
        from src.ml.registry import ModelRegistry as PersistentRegistry
        from sklearn.dummy import DummyClassifier

        p_registry = PersistentRegistry(str(tmp_path / "reg2"))
        dummy = DummyClassifier(strategy="most_frequent")
        dummy.fit(np.array([[1, 2], [3, 4]]), np.array([0, 1]))
        p_registry.register("crime_model", model=dummy)

        predictor = CrimePredictor("crime_model", registry=p_registry)
        predictor.load()
        result = predictor.predict_single({"feat1": 1, "feat2": 2})
        assert "predictions" in result


class TestPredictionExplanation:
    def test_coefficient_fallback(self):
        from sklearn.linear_model import LogisticRegression
        model = LogisticRegression()
        rng = np.random.RandomState(42)
        x = rng.rand(50, 3)
        model.fit(x, (x[:, 0] > 0.5).astype(int))
        explainer = PredictionExplanation(model, feature_names=["a", "b", "c"])
        explainer.fit()
        result = explainer.explain(x[:5])
        assert "method" in result
        assert "feature_importance" in result

    def test_permutation_fallback(self):
        from sklearn.svm import SVC
        model = SVC(kernel="linear", random_state=42)
        rng = np.random.RandomState(42)
        x = rng.rand(50, 3)
        model.fit(x, (x[:, 0] > 0.5).astype(int))
        explainer = PredictionExplanation(model, feature_names=["a", "b", "c"])
        explainer.fit()
        result = explainer.explain(x[:5])
        assert "feature_importance" in result


class TestPredictModel:
    def test_convenience_function(self):
        class DummyModel:
            def predict(self, data):
                return np.array([1])

        registry = ModelRegistry()
        registry.register("test", DummyModel())
        result = predict_model("test", pd.DataFrame({"a": [1]}))
        assert result[0] == 1
