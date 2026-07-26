"""Tests for ml.evaluation module."""

from __future__ import annotations

import numpy as np
import pytest

from src.ml.evaluation import (
    ClassificationEvaluator,
    EvalMetrics,
    ModelComparisonReport,
    ModelEvaluator,
    RegressionEvaluator,
    ValidationSuite,
)


class TestEvalMetrics:
    def test_default_values(self):
        m = EvalMetrics()
        assert m.accuracy == 0.0
        assert m.auc_roc is None


class TestModelEvaluator:
    def test_evaluate_binary(self):
        y_true = np.array([0, 1, 0, 1, 0])
        y_pred = np.array([0, 1, 0, 1, 1])
        evaluator = ModelEvaluator()
        metrics = evaluator.evaluate(y_true, y_pred)
        assert 0 <= metrics.accuracy <= 1
        assert metrics.auc_roc is not None

    def test_classification_report(self):
        evaluator = ModelEvaluator()
        report = evaluator.classification_report(
            np.array([0, 1, 0]), np.array([0, 1, 1])
        )
        assert "0" in report or "1" in report

    def test_confusion_matrix_shape(self):
        evaluator = ModelEvaluator()
        cm = evaluator.confusion_matrix(np.array([0, 1, 0, 1]), np.array([0, 1, 0, 0]))
        assert len(cm) == 2


class TestClassificationEvaluator:
    def test_evaluate_binary(self):
        y_true = np.array([0, 1, 0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 1, 1, 1])
        y_prob = np.array([[0.9, 0.1], [0.2, 0.8], [0.8, 0.2], [0.3, 0.7], [0.4, 0.6], [0.1, 0.9]])
        evaluator = ClassificationEvaluator()
        result = evaluator.evaluate(y_true, y_pred, y_prob)
        assert result["accuracy"] > 0
        assert "roc_auc" in result
        assert "confusion_matrix" in result

    def test_evaluate_multiclass(self):
        y_true = np.array([0, 1, 2, 0, 1, 2])
        y_pred = np.array([0, 1, 2, 0, 0, 2])
        evaluator = ClassificationEvaluator()
        result = evaluator.evaluate(y_true, y_pred)
        assert result["accuracy"] > 0

    def test_plot_methods_return_none_without_matplotlib(self):
        evaluator = ClassificationEvaluator()
        result = evaluator.plot_confusion_matrix(
            np.array([0, 1]), np.array([0, 1])
        )
        assert result is None


class TestRegressionEvaluator:
    def test_evaluate(self):
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.1, 2.1, 2.9, 4.2, 4.8])
        evaluator = RegressionEvaluator()
        result = evaluator.evaluate(y_true, y_pred)
        assert "mse" in result
        assert "rmse" in result
        assert "mae" in result
        assert "r2" in result
        assert "mape" in result
        assert result["r2"] > 0.9

    def test_perfect_prediction(self):
        y_true = np.array([1.0, 2.0, 3.0])
        evaluator = RegressionEvaluator()
        result = evaluator.evaluate(y_true, y_true)
        assert result["r2"] == 1.0
        assert result["mse"] == 0.0


class TestValidationSuite:
    def test_run_checks_passes(self):
        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 1])
        suite = ValidationSuite()
        results = suite.run_checks(y_true, y_pred, thresholds={"accuracy": 0.5})
        assert all(r["passed"] for r in results)


class TestModelComparisonReport:
    def test_add_and_compare(self):
        report = ModelComparisonReport()
        report.add_model("A", {"f1_weighted": 0.9, "accuracy": 0.95})
        report.add_model("B", {"f1_weighted": 0.8, "accuracy": 0.85})
        result = report.compare(metric="f1_weighted")
        assert result["best_model"] == "A"
        assert len(result["ranking"]) == 2

    def test_empty_report(self):
        report = ModelComparisonReport()
        result = report.compare()
        assert result["best_model"] is None

    def test_summary(self):
        report = ModelComparisonReport()
        report.add_model("X", {"acc": 1.0})
        summary = report.summary()
        assert summary["n_models"] == 1

    def test_to_dataframe(self):
        import pandas as pd
        report = ModelComparisonReport()
        report.add_model("A", {"score": 0.9})
        df = report.to_dataframe()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
