from __future__ import annotations

import time
from typing import Any

import numpy as np

from src.ml.evaluation import ModelEvaluator, ValidationSuite


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


async def evaluate_pipeline(state: dict) -> dict:
    """Convenience function for Pipeline compatibility."""
    evaluator = PipelineEvaluator()
    result = await evaluator.evaluate(
        np.array(state["y_true"]),
        np.array(state["y_pred"]),
        state.get("pipeline_name", "default"),
    )
    return {"evaluation_result": result}
