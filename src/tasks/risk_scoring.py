from __future__ import annotations

from celery import shared_task
from sqlalchemy import text

from src.database import async_session_factory


@shared_task(name="risk_scoring.compute")
def compute_risk_score_task(case_master_id: int) -> dict:
    from src.services.risk_service import RiskService

    return RiskService.compute_sync(case_master_id)


@shared_task(name="risk_scoring.batch_recompute")
def batch_recompute_task(district_id: int | None = None) -> dict:
    import asyncio

    async def _run():
        from src.services.risk_service import RiskService

        async with async_session_factory() as session:
            svc = RiskService(session)
            query = "SELECT CaseMasterID FROM case_master"
            params: dict = {}
            if district_id:
                query += " WHERE DistrictID = :district_id"
                params["district_id"] = district_id
            result = await session.execute(text(query), params)
            ids = [row[0] for row in result]
            results = []
            for cid in ids:
                score = await svc.compute_risk_score(cid)
                results.append({"case_master_id": cid, "risk_score": score})
            return {"total": len(results), "results": results}

    return asyncio.run(_run())
