from __future__ import annotations

# Celery is optional — gracefully degrade when not available (e.g., Catalyst AppSail)
try:
    from src.tasks.anomaly import run_anomaly_detection_task
    from src.tasks.notifications import send_notification_task
    from src.tasks.risk_scoring import compute_risk_score_task

    __all__ = [
        "compute_risk_score_task",
        "run_anomaly_detection_task",
        "send_notification_task",
    ]
except ImportError:
    # Celery not installed — provide no-op stubs
    class _NoOpTask:
        def delay(self, *args, **kwargs):
            pass

        def __call__(self, *args, **kwargs):
            return None

    compute_risk_score_task = _NoOpTask()
    run_anomaly_detection_task = _NoOpTask()
    send_notification_task = _NoOpTask()

    __all__ = [
        "compute_risk_score_task",
        "run_anomaly_detection_task",
        "send_notification_task",
    ]
