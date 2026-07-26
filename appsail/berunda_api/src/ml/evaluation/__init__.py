from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from src.shared.logging import get_logger

logger = get_logger(__name__)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import seaborn as sns
    _PLOTTING_AVAILABLE = True
except ImportError:
    _PLOTTING_AVAILABLE = False
    plt = None
    sns = None


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
        from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
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
            results.append({
                "metric": metric_name,
                "value": value,
                "threshold": threshold,
                "passed": value >= threshold,
            })
        return results


class ClassificationEvaluator:
    """Detailed classification evaluation with ROC AUC, per-class metrics."""

    def evaluate(
        self, y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray | None = None
    ) -> dict[str, Any]:
        from sklearn.metrics import (
            accuracy_score,
            classification_report,
            confusion_matrix,
            f1_score,
            precision_score,
            recall_score,
        )

        results: dict[str, Any] = {
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "precision_macro": float(precision_score(y_true, y_pred, average="macro", zero_division=0)),
            "precision_weighted": float(precision_score(y_true, y_pred, average="weighted", zero_division=0)),
            "recall_macro": float(recall_score(y_true, y_pred, average="macro", zero_division=0)),
            "recall_weighted": float(recall_score(y_true, y_pred, average="weighted", zero_division=0)),
            "f1_macro": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
            "f1_weighted": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
            "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
            "classification_report": classification_report(y_true, y_pred, output_dict=True, zero_division=0),
        }

        n_classes = len(np.unique(y_true))
        if y_prob is not None and n_classes == 2:
            from sklearn.metrics import roc_auc_score
            try:
                results["roc_auc"] = float(roc_auc_score(y_true, y_prob[:, 1]))
            except (ValueError, IndexError):
                pass
        elif y_prob is not None and n_classes > 2:
            from sklearn.metrics import roc_auc_score
            try:
                results["roc_auc_ovr"] = float(
                    roc_auc_score(y_true, y_prob, multi_class="ovr")
                )
            except (ValueError, IndexError):
                pass

        logger.info("Classification evaluation complete", extra={"accuracy": results["accuracy"]})
        return results

    def plot_confusion_matrix(
        self, y_true: np.ndarray, y_pred: np.ndarray, save_path: str | None = None
    ) -> str | None:
        if not _PLOTTING_AVAILABLE:
            logger.warning("matplotlib/seaborn not available, skipping plot")
            return None
        from sklearn.metrics import confusion_matrix
        cm = confusion_matrix(y_true, y_pred)
        _, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("True")
        ax.set_title("Confusion Matrix")
        if save_path:
            plt.savefig(save_path, bbox_inches="tight", dpi=100)
            plt.close()
            return save_path
        return None

    def plot_roc_curve(
        self, y_true: np.ndarray, y_prob: np.ndarray, save_path: str | None = None
    ) -> str | None:
        if not _PLOTTING_AVAILABLE:
            logger.warning("matplotlib/seaborn not available, skipping plot")
            return None
        from sklearn.metrics import auc, roc_curve
        fpr, tpr, _ = roc_curve(y_true, y_prob[:, 1] if y_prob.ndim > 1 else y_prob)
        roc_auc = auc(fpr, tpr)
        _, ax = plt.subplots(figsize=(8, 6))
        ax.plot(fpr, tpr, label=f"ROC (AUC = {roc_auc:.3f})")
        ax.plot([0, 1], [0, 1], "k--")
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.set_title("ROC Curve")
        ax.legend(loc="lower right")
        if save_path:
            plt.savefig(save_path, bbox_inches="tight", dpi=100)
            plt.close()
            return save_path
        return None

    def plot_feature_importance(
        self, importance: dict[str, float], top_n: int = 20, save_path: str | None = None
    ) -> str | None:
        if not _PLOTTING_AVAILABLE:
            logger.warning("matplotlib/seaborn not available, skipping plot")
            return None
        sorted_items = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:top_n]
        names, values = zip(*sorted_items) if sorted_items else ([], [])
        _, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=list(values), y=list(names), ax=ax)
        ax.set_xlabel("Importance")
        ax.set_ylabel("Feature")
        ax.set_title(f"Top {len(names)} Feature Importance")
        if save_path:
            plt.savefig(save_path, bbox_inches="tight", dpi=100)
            plt.close()
            return save_path
        return None


class RegressionEvaluator:
    """Regression evaluation metrics."""

    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        mse = float(mean_squared_error(y_true, y_pred))
        rmse = float(np.sqrt(mse))
        mae = float(mean_absolute_error(y_true, y_pred))
        r2 = float(r2_score(y_true, y_pred))
        mape = float(
            np.mean(np.abs((y_true - y_pred) / np.maximum(np.abs(y_true), 1e-10))) * 100
        )
        results = {
            "mse": mse,
            "rmse": rmse,
            "mae": mae,
            "r2": r2,
            "mape": mape,
            "adj_r2": float(1 - (1 - r2) * (len(y_true) - 1) / (len(y_true) - 1 - 1))
            if len(y_true) > 2
            else r2,
        }
        logger.info("Regression evaluation complete", extra={"r2": r2, "rmse": rmse})
        return results


class ModelComparisonReport:
    """Compare multiple models and generate a ranking report."""

    def __init__(self):
        self.results: dict[str, dict[str, Any]] = {}

    def add_model(self, name: str, metrics: dict[str, Any]) -> None:
        self.results[name] = metrics

    def compare(self, metric: str = "f1_weighted", higher_is_better: bool = True) -> dict[str, Any]:
        if not self.results:
            return {"models": [], "ranking": [], "best_model": None}
        sorted_models = sorted(
            self.results.items(),
            key=lambda x: x[1].get(metric, 0),
            reverse=higher_is_better,
        )
        ranking = [
            {"rank": i + 1, "name": name, metric: metrics.get(metric, 0)}
            for i, (name, metrics) in enumerate(sorted_models)
        ]
        return {
            "models": list(self.results.keys()),
            "ranking": ranking,
            "best_model": sorted_models[0][0] if sorted_models else None,
            "comparison_metric": metric,
        }

    def to_dataframe(self) -> "pd.DataFrame":
        import pandas as pd
        rows = []
        for name, metrics in self.results.items():
            row = {"model": name}
            row.update(metrics)
            rows.append(row)
        return pd.DataFrame(rows)

    def summary(self) -> dict[str, Any]:
        return {
            "n_models": len(self.results),
            "models": list(self.results.keys()),
        }
