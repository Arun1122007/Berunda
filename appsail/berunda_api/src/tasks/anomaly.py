from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from src.database import get_session_factory
from src.models.src_models import CaseMaster


def run_anomaly_detection_task(case_master_id: int) -> dict:
    async def _run():
        from src.services.anomaly_service import AnomalyService

        async with get_session_factory()() as session:
            svc = AnomalyService(session)
            result = await svc.detect_anomalies(case_master_id)
            return result

    return asyncio.run(_run())


def scan_period_task(hours: int = 24) -> dict:
    async def _run():
        from src.services.anomaly_service import AnomalyService

        async with get_session_factory()() as session:
            svc = AnomalyService(session)
            cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
            result = await session.execute(
                select(CaseMaster.CaseMasterID).where(
                    CaseMaster.CrimeRegisteredDate >= cutoff.date()
                )
            )
            ids = [row[0] for row in result]
            findings = []
            for cid in ids:
                findings.append(await svc.detect_anomalies(cid))
            return {"scanned": len(ids), "findings": findings}

    return asyncio.run(_run())
