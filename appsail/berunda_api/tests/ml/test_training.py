"""Tests for ml.training module."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.ml.training import (
    BaseTrainer,
    CrimePatternTrainer,
    HyperparamConfig,
    ModelTrainer,
    TrainConfig,
    train_model_async,
)


class TestModelTrainer:
    def test_train_returns_metrics(self):
        rng = np.random.RandomState(42)
        x = rng.rand(100, 4)
        y = (x[:, 0] > 0.5).astype(int)
        trainer = ModelTrainer(TrainConfig(model_type="baseline"))
        metrics = trainer.train(x, y)
        assert "train_score" in metrics
        assert "test_score" in metrics

    def test_cross_validate(self):
        rng = np.random.RandomState(42)
        x = rng.rand(50, 4)
        y = (x[:, 0] > 0.5).astype(int)
        trainer = ModelTrainer(TrainConfig(model_type="baseline"))
        cv = trainer.cross_validate(x, y)
        assert "mean_score" in cv

    def test_get_model(self):
        rng = np.random.RandomState(42)
        x = rng.rand(20, 4)
        y = (x[:, 0] > 0.5).astype(int)
        trainer = ModelTrainer()
        trainer.train(x, y, "test_model")
        model = trainer.get_model("test_model")
        assert model is not None

    def test_create_model(self):
        trainer = ModelTrainer(TrainConfig(model_type="ensemble"))
        model = trainer._create_model()
        from sklearn.ensemble import RandomForestClassifier
        assert isinstance(model, RandomForestClassifier)


class TestBaseTrainer:
    def test_abstract_cannot_instantiate(self):
        with pytest.raises(TypeError):
            BaseTrainer()  # type: ignore


class TestCrimePatternTrainer:
    def test_train_returns_metrics(self):
        rng = np.random.RandomState(42)
        x = rng.rand(100, 4)
        y = (x[:, 0] > 0.5).astype(int)
        trainer = CrimePatternTrainer(model_type="random_forest")
        metrics = trainer.train(x, y)
        assert "accuracy" in metrics
        assert "f1_weighted" in metrics

    def test_train_with_feature_names(self):
        rng = np.random.RandomState(42)
        x = rng.rand(100, 4)
        y = (x[:, 0] > 0.5).astype(int)
        trainer = CrimePatternTrainer()
        metrics = trainer.train(x, y, feature_names=["a", "b", "c", "d"])
        assert "accuracy" in metrics

    def test_get_model_after_train(self):
        rng = np.random.RandomState(42)
        x = rng.rand(50, 4)
        y = (x[:, 0] > 0.5).astype(int)
        trainer = CrimePatternTrainer()
        trainer.train(x, y)
        model = trainer.get_model()
        assert model is not None

    def test_get_params(self):
        trainer = CrimePatternTrainer(random_state=99)
        params = trainer.get_params()
        assert params["random_state"] == 99

    def test_feature_importance(self):
        rng = np.random.RandomState(42)
        x = rng.rand(100, 4)
        y = (x[:, 0] > 0.5).astype(int)
        trainer = CrimePatternTrainer(model_type="random_forest")
        trainer.train(x, y, feature_names=["f1", "f2", "f3", "f4"])
        importance = trainer.get_feature_importance()
        assert isinstance(importance, dict)

    def test_train_from_dataframe(self):
        df = pd.DataFrame({
            "CrimeMajorHeadID": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            "IncidentFromDate": pd.date_range("2024-01-01", periods=15),
            "BriefFacts": ["theft", "assault", "theft", "robbery", "assault"] * 3,
        })
        trainer = CrimePatternTrainer()
        result = trainer.train_from_dataframe(df, register=False)
        assert "metrics" in result
        assert "feature_importance" in result

    def test_hyperparameter_tuning(self):
        rng = np.random.RandomState(42)
        x = rng.rand(200, 4)
        y = (x[:, 0] > 0.5).astype(int)
        hpc = HyperparamConfig(enabled=True, param_grid={"n_estimators": [10, 20]})
        trainer = CrimePatternTrainer(model_type="random_forest", hyperparam_config=hpc)
        metrics = trainer.train(x, y)
        assert "accuracy" in metrics


class TestTrainModelAsync:
    def test_convenience_function(self):
        rng = np.random.RandomState(42)
        x = rng.rand(30, 4)
        y = (x[:, 0] > 0.5).astype(int)
        result = train_model_async(x, y)
        assert "train_score" in result
