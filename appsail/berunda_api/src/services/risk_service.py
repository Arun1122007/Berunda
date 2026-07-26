from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import func, select

from src.exceptions import NotFoundError
from src.models.int_models import PersonEntity, PersonEntityLink, RiskScore
from src.models.src_models import CaseMaster
from src.services.base import BaseService


class RiskService(BaseService):
    async def get_scores(
        self,
        person_entity_id: int | None = None,
        min_score: float | None = None,
        max_score: float | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[RiskScore], int]:
        query = select(RiskScore)
        count_query = select(func.count(RiskScore.RiskScoreID))

        if person_entity_id is not None:
            query = query.where(RiskScore.PersonEntityID == person_entity_id)
            count_query = count_query.where(RiskScore.PersonEntityID == person_entity_id)
        if min_score is not None:
            query = query.where(RiskScore.Score >= min_score)
            count_query = count_query.where(RiskScore.Score >= min_score)
        if max_score is not None:
            query = query.where(RiskScore.Score <= max_score)
            count_query = count_query.where(RiskScore.Score <= max_score)

        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        query = query.order_by(RiskScore.Score.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.session.execute(query)
        items = list(result.scalars().all())
        return items, total

    async def compute_risk_score(self, person_entity_id: int) -> RiskScore:
        entity = await self.session.get(PersonEntity, person_entity_id)
        if not entity:
            raise NotFoundError(f"PersonEntity {person_entity_id} not found")

        links = await self.session.execute(
            select(PersonEntityLink).where(PersonEntityLink.PersonEntityID == person_entity_id)
        )
        link_records = list(links.scalars().all())
        linked_case_ids = [rec.CaseMasterID for rec in link_records if rec.CaseMasterID]

        total_cases = len(linked_case_ids)
        features: dict[str, Any] = {
            "total_linked_cases": total_cases,
            "unique_person_ids": len(
                set(rec.PersonEntityID for rec in link_records if rec.PersonEntityID)
            ),
        }
        recency = 0.0
        severity = 0.0
        if linked_case_ids:
            cases = await self.session.execute(
                select(CaseMaster).where(CaseMaster.CaseMasterID.in_(linked_case_ids))
            )
            case_records = list(cases.scalars().all())

            dates = [c.CrimeRegisteredDate for c in case_records if c.CrimeRegisteredDate]
            scores = [c.GravityOffenceID for c in case_records if c.GravityOffenceID]

            features["case_count"] = len(case_records)
            if dates:
                date_range = (max(dates) - min(dates)).days if len(dates) > 1 else 0
                recency = min(1.0, date_range / 365.0)
                features["date_range_days"] = date_range
            if scores:
                severity = min(1.0, sum(scores) / (len(scores) * 10.0))  # type: ignore[assignment]
                features["avg_gravity_score"] = round(sum(scores) / len(scores), 2)
            features["multiple_crime_heads"] = len(
                set(c.CrimeMajorHeadID for c in case_records if c.CrimeMajorHeadID)
            )

        recidivism = min(1.0, total_cases / 10.0)
        final_score = round(0.4 * recidivism + 0.3 * recency + 0.3 * severity, 4)
        features["recidivism_factor"] = recidivism
        features["recency_factor"] = recency
        features["severity_factor"] = severity

        score = RiskScore(
            PersonEntityID=person_entity_id,
            Score=min(1.0, max(0.0, final_score)),
            ModelVersion="rule-based-v2",
            FeaturesJSON=json.dumps(features),
            ComputedAt=datetime.now(timezone.utc),
        )
        self.session.add(score)
        await self.session.commit()
        await self.session.refresh(score)
        return score
