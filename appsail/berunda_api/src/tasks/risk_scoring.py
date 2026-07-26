from __future__ import annotations

import asyncio

from sqlalchemy import select, text

from src.database import get_session_factory
from src.models.int_models import PersonEntityLink


def compute_risk_score_task(case_master_id: int) -> dict:
    async def _run():
        from src.services.risk_service import RiskService

        async with get_session_factory()() as session:
            svc = RiskService(session)
            result = await session.execute(
                select(PersonEntityLink.PersonEntityID).where(
                    PersonEntityLink.CaseMasterID == case_master_id,
                    PersonEntityLink.PersonEntityID.isnot(None),
                )
            )
            entity_ids = list({row[0] for row in result if row[0] is not None})
            scores = []
            for eid in entity_ids:
                score = await svc.compute_risk_score(eid)
                scores.append({"person_entity_id": eid, "score": score.Score})
            return {"case_master_id": case_master_id, "entity_scores": scores}

    return asyncio.run(_run())


def batch_recompute_task(district_id: int | None = None) -> dict:
    async def _run():
        from src.services.risk_service import RiskService

        async with get_session_factory()() as session:
            svc = RiskService(session)
            query = "SELECT DISTINCT PersonEntityID FROM int_PersonEntityLink"
            params: dict = {}
            if district_id:
                query += " WHERE PrimaryDistrictID = :district_id"
                params["district_id"] = district_id
            result = await session.execute(text(query), params)
            ids = [row[0] for row in result if row[0] is not None]
            results = []
            for eid in ids:
                score = await svc.compute_risk_score(eid)
                results.append({"person_entity_id": eid, "score": score.Score})
            return {"total": len(results), "results": results}

    return asyncio.run(_run())
