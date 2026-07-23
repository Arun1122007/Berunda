from __future__ import annotations

from celery import shared_task
from sqlalchemy import text

from src.database import async_session_factory


@shared_task(name="anomaly.detect_case")
def run_anomaly_detection_task(case_master_id: int) -> dict:
    import asyncio

    async def _run():
        from src.services.anomaly_service import AnomalyService

        async with async_session_factory() as session:
            svc = AnomalyService(session)
            is_anomaly = await svc.detect_anomalies(case_master_id)
            return {"case_master_id": case_master_id, "is_anomaly": is_anomaly}

    return asyncio.run(_run())


@shared_task(name="anomaly.scan_period")
def scan_period_task(hours: int = 24) -> dict:
    import asyncio

    async def _run():
        from src.services.anomaly_service import AnomalyService

        async with async_session_factory() as session:
            svc = AnomalyService(session)
            result = await session.execute(
                text(
                    "SELECT CaseMasterID FROM case_master "
                    "WHERE CreatedAt >= NOW() - INTERVAL ':hours' HOUR"
                ),
                {"hours": hours},
            )
            ids = [row[0] for row in result]
            findings = []
            for cid in ids:
                is_anomaly = await svc.detect_anomalies(cid)
                findings.append({"case_master_id": cid, "is_anomaly": is_anomaly})
            return {"scanned": len(ids), "findings": findings}

    return asyncio.run(_run())
