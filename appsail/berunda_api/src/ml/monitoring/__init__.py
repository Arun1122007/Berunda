from __future__ import annotations

import numpy as np


class DriftDetector:
    """Detect data drift between training and serving distributions."""

    def detect(self, reference: np.ndarray, current: np.ndarray, threshold: float = 0.05) -> dict:
        """Detect drift using Kolmogorov-Smirnov test."""
        from scipy.stats import ks_2samp

        if reference.shape[1] != current.shape[1]:
            return {"drift_detected": True, "reason": "Feature dimension mismatch"}

        drifted_features = []
        for i in range(reference.shape[1]):
            stat, p_value = ks_2samp(reference[:, i], current[:, i])
            if p_value < threshold:
                drifted_features.append(
                    {"feature": i, "statistic": float(stat), "p_value": float(p_value)}
                )

        return {
            "drift_detected": len(drifted_features) > 0,
            "drifted_features": drifted_features,
            "total_features": reference.shape[1],
        }


class DataQualityChecker:
    """Check data quality metrics."""

    def check(self, data: np.ndarray, expected_range: tuple | None = None) -> dict:
        nan_count = int(np.isnan(data).sum())
        inf_count = int(np.isinf(data).sum())
        unique_counts = [len(np.unique(data[:, i])) for i in range(data.shape[1])]

        results = {
            "nan_count": nan_count,
            "inf_count": inf_count,
            "nan_ratio": float(nan_count / data.size),
            "unique_counts": unique_counts,
            "passed": nan_count == 0 and inf_count == 0,
        }

        if expected_range:
            out_of_range = int(((data < expected_range[0]) | (data > expected_range[1])).sum())
            results["out_of_range"] = out_of_range
            results["range_check_passed"] = out_of_range == 0

        return results


class BiasMonitor:
    """Monitor for bias in model predictions across groups."""

    def check(self, y_pred: np.ndarray, sensitive_attr: np.ndarray) -> dict:
        groups = np.unique(sensitive_attr)
        group_rates = {}

        for group in groups:
            mask = sensitive_attr == group
            group_rates[str(group)] = float(y_pred[mask].mean())

        rates = list(group_rates.values())
        max_disparity = max(rates) - min(rates) if rates else 0

        return {
            "group_rates": group_rates,
            "max_disparity": max_disparity,
            "bias_detected": max_disparity > 0.1,
        }


class AlertManager:
    """Manage monitoring alerts."""

    def __init__(self):
        self.alerts: list[dict] = []

    def check_and_alert(self, check_name: str, passed: bool, details: dict) -> str | None:
        if not passed:
            alert = {
                "type": check_name,
                "severity": "warning",
                "details": details,
            }
            self.alerts.append(alert)
            return f"ALERT: {check_name} failed - {details}"
        return None

    def get_alerts(self) -> list[dict]:
        return self.alerts

    def clear_alerts(self) -> None:
        self.alerts = []
