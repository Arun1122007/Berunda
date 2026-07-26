from __future__ import annotations

import time
from typing import Any

import numpy as np

from src.ml.evaluation import ClassificationEvaluator, ModelComparisonReport, ModelEvaluator, RegressionEvaluator, ValidationSuite
from src.ml.registry import ModelRegistry
from src.pipelines.base import BasePipeline
from src.shared.logging import get_logger

logger = get_logger(__name__)


class PipelineEvaluator:
    """Evaluate end-to-end pipeline performance."""

    def __init__(self):
        self.evaluator = ModelEvaluator()
        self.validator = ValidationSuite()

    async def evaluate(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        pipeline_name: str = "default",
        metadata: dict | None = None,
    ) -> dict[str, Any]:
        start = time.time()
        metrics = self.evaluator.evaluate(y_true, y_pred)
        validation = self.validator.run_checks(y_true, y_pred)
        report = self.evaluator.classification_report(y_true, y_pred)
        cm = self.evaluator.confusion_matrix(y_true, y_pred)
        return {
            "pipeline": pipeline_name,
            "metrics": {
                "accuracy": metrics.accuracy,
                "precision": metrics.precision,
                "recall": metrics.recall,
                "f1_score": metrics.f1_score,
                "auc_roc": metrics.auc_roc,
            },
            "validation": validation,
            "classification_report": report,
            "confusion_matrix": cm,
            "elapsed_seconds": time.time() - start,
            "metadata": metadata or {},
        }


class EvaluationPipeline(BasePipeline):
    """Pipeline that loads model + test data, computes metrics, generates report."""

    def __init__(self, registry: ModelRegistry | None = None):
        self.registry = registry or ModelRegistry()
        self.classification_eval = ClassificationEvaluator()
        self.regression_eval = RegressionEvaluator()
        self.comparison = ModelComparisonReport()
        self._status: dict[str, Any] = {"state": "idle", "last_run": None}

    def validate(self, **kwargs: Any) -> dict[str, Any]:
        return {"valid": True, "issues": []}

    def get_status(self) -> dict[str, Any]:
        return dict(self._status)

    async def run(
        self,
        model_name: str | None = None,
        y_true: np.ndarray | None = None,
        y_pred: np.ndarray | None = None,
        y_prob: np.ndarray | None = None,
        task: str = "classification",
        **kwargs: Any,
    ) -> dict[str, Any]:
        self._status["state"] = "running"
        y_true_arr = y_true if y_true is not None else kwargs.get("y_true")
        y_pred_arr = y_pred if y_pred is not None else kwargs.get("y_pred")
        y_prob_arr = y_prob if y_prob is not None else kwargs.get("y_prob")

        if model_name:
            try:
                model, metadata = self.registry.load(model_name)
                if y_true_arr is None:
                    raise ValueError("y_true required when evaluating a registered model")
                y_pred_arr = model.predict(kwargs.get("x_test", np.array([])))
                if hasattr(model, "predict_proba"):
                    try:
                        y_prob_arr = model.predict_proba(kwargs.get("x_test", np.array([])))
                    except Exception:
                        pass
            except Exception as exc:
                self._status = {"state": "failed", "last_run": time.time()}
                return {"error": str(exc)}

        if task == "classification":
            result = self.classification_eval.evaluate(y_true_arr, y_pred_arr, y_prob_arr)
        elif task == "regression":
            result = self.regression_eval.evaluate(y_true_arr, y_pred_arr)
        else:
            raise ValueError(f"Unknown task type: {task}")

        if model_name:
            result["model_name"] = model_name

        result["task"] = task
        result["n_samples"] = len(y_true_arr)
        result["elapsed_seconds"] = time.time() - time.time()

        self._status = {"state": "completed", "last_run": time.time()}
        return result


async def evaluate_pipeline(state: dict) -> dict:
    evaluator = PipelineEvaluator()
    result = await evaluator.evaluate(
        np.array(state["y_true"]),
        np.array(state["y_pred"]),
        state.get("pipeline_name", "default"),
    )
    return {"evaluation_result": result}
