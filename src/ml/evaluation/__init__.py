"""ML model evaluation utilities."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class EvalMetrics:
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    auc_roc: float | None = None


class ModelEvaluator:
    """Evaluate model performance with standard metrics."""

    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray) -> EvalMetrics:
        from sklearn.metrics import (
            accuracy_score,
            f1_score,
            precision_score,
            recall_score,
            roc_auc_score,
        )

        metrics = EvalMetrics(
            accuracy=float(accuracy_score(y_true, y_pred)),
            precision=float(precision_score(y_true, y_pred, average="weighted", zero_division=0)),
            recall=float(recall_score(y_true, y_pred, average="weighted", zero_division=0)),
            f1_score=float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
        )

        try:
            if len(np.unique(y_true)) == 2:
                metrics.auc_roc = float(roc_auc_score(y_true, y_pred))
        except (ValueError, IndexError):
            pass

        return metrics

    def classification_report(self, y_true: np.ndarray, y_pred: np.ndarray) -> dict:
        from sklearn.metrics import classification_report

        report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
        return report

    def confusion_matrix(self, y_true: np.ndarray, y_pred: np.ndarray) -> list[list[int]]:
        from sklearn.metrics import confusion_matrix

        return confusion_matrix(y_true, y_pred).tolist()


class ValidationSuite:
    """Run multiple validation checks on model performance."""

    def __init__(self):
        self.evaluator = ModelEvaluator()
        self.checks: list[dict] = []

    def run_checks(
        self, y_true: np.ndarray, y_pred: np.ndarray, thresholds: dict | None = None
    ) -> list[dict]:
        thresholds = thresholds or {"accuracy": 0.7, "f1": 0.6}
        metrics = self.evaluator.evaluate(y_true, y_pred)
        results = []

        for metric_name, threshold in thresholds.items():
            value = getattr(metrics, metric_name, 0)
            results.append(
                {
                    "metric": metric_name,
                    "value": value,
                    "threshold": threshold,
                    "passed": value >= threshold,
                }
            )

        return results
