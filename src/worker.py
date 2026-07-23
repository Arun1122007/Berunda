from __future__ import annotations

import os

from celery import Celery

BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery(
    "berunda",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=["src.tasks.risk_scoring", "src.tasks.anomaly", "src.tasks.notifications"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    beat_schedule={
        "scan-anomalies-6h": {
            "task": "anomaly.scan_period",
            "schedule": 21600.0,
            "kwargs": {"hours": 24},
        },
        "batch-recompute-risk-daily": {
            "task": "risk_scoring.batch_recompute",
            "schedule": 86400.0,
            "kwargs": {},
        },
    },
)
