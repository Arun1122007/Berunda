from __future__ import annotations

import math
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import func, select

from src.models.int_models import AnomalyAlert
from src.models.src_models import CaseMaster
from src.services.base import BaseService


class AnomalyService(BaseService):
    async def detect_anomalies(self, case_master_id: int) -> dict:
        """Run z-score anomaly detection for the district and crime head of a case."""
        case = await self.session.get(CaseMaster, case_master_id)
        if not case:
            return {
                "case_master_id": case_master_id,
                "is_anomaly": False,
                "reason": "case_not_found",
            }

        district_id = case.PoliceStationID or 1
        crime_head_id = case.CrimeMajorHeadID or 1
        now = datetime.now(timezone.utc)
        four_weeks_ago = now - timedelta(weeks=4)

        stmt = select(func.count(CaseMaster.CaseMasterID)).where(
            CaseMaster.PoliceStationID == district_id,
            CaseMaster.CrimeMajorHeadID == crime_head_id,
            CaseMaster.CrimeRegisteredDate >= four_weeks_ago.date(),
        )
        result = await self.session.execute(stmt)
        recent_count = result.scalar_one()

        stmt3 = select(func.avg(func.count(CaseMaster.CaseMasterID))).where(
            CaseMaster.CrimeMajorHeadID == crime_head_id,
        )
        stmt3 = (
            select(func.count(CaseMaster.CaseMasterID))
            .where(
                CaseMaster.CrimeMajorHeadID == crime_head_id,
            )
            .group_by(CaseMaster.PoliceStationID)
        )
        result3 = await self.session.execute(stmt3)
        district_counts = [row[0] for row in result3]

        mean = sum(district_counts) / len(district_counts) if district_counts else 1.0
        variance = (
            sum((c - mean) ** 2 for c in district_counts) / len(district_counts)
            if len(district_counts) > 1
            else 1.0
        )
        std_dev = math.sqrt(variance) if variance > 0 else 1.0

        z_score = (recent_count - mean) / std_dev if std_dev > 0 else 0.0
        is_anomaly = abs(z_score) > 2.0

        if is_anomaly:
            existing = await self.session.execute(
                select(AnomalyAlert)
                .where(
                    AnomalyAlert.DistrictID == district_id,
                    AnomalyAlert.CrimeHeadID == crime_head_id,
                    AnomalyAlert.AlertLevel == 1,
                )
                .limit(1)
            )
            if not existing.scalar_one_or_none():
                alert = AnomalyAlert(
                    DistrictID=district_id,
                    CrimeHeadID=crime_head_id,
                    ZScore=round(z_score, 4),
                    AlertLevel=1,
                    WeekStart=four_weeks_ago,
                    ObservedCount=recent_count,
                    BaselineMean=round(mean, 4),
                    StdDev=round(std_dev, 4),
                )
                self.session.add(alert)
                await self.session.commit()

        return {
            "case_master_id": case_master_id,
            "is_anomaly": is_anomaly,
            "z_score": round(z_score, 4),
            "district_id": district_id,
            "crime_head_id": crime_head_id,
        }

    async def get_alerts(
        self,
        district_id: int | None = None,
        alert_only: bool = True,
        week_start: date | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[AnomalyAlert], int]:
        query = select(AnomalyAlert)
        count_query = select(func.count(AnomalyAlert.AnomalyAlertID))

        if district_id is not None:
            query = query.where(AnomalyAlert.DistrictID == district_id)
            count_query = count_query.where(AnomalyAlert.DistrictID == district_id)
        if alert_only:
            query = query.where(AnomalyAlert.AlertLevel == 1)
            count_query = count_query.where(AnomalyAlert.AlertLevel == 1)
        if week_start is not None:
            query = query.where(AnomalyAlert.WeekStart >= week_start)
            count_query = count_query.where(AnomalyAlert.WeekStart >= week_start)

        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        query = query.order_by(AnomalyAlert.ZScore.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.session.execute(query)
        items = list(result.scalars().all())
        return items, total
