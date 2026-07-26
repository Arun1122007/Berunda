from __future__ import annotations

from src.config import settings
from src.shared.logging import get_logger

logger = get_logger(__name__)

BROKER_URL = settings.CELERY_BROKER_URL
RESULT_BACKEND = settings.CELERY_RESULT_BACKEND

celery_app = None
try:
    from celery import Celery, signals

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

    @signals.worker_shutdown.connect
    def _on_worker_shutdown(**kwargs):
        logger.info("Celery worker shutting down — cleaning up resources")
        import asyncio
        import contextlib

        from src.database import dispose_engine

        with contextlib.suppress(Exception):
            asyncio.run(dispose_engine())
except ImportError:
    logger.warning("Celery not installed — worker tasks disabled")
