import datetime
import logging
from typing import Any

import yaml

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self, repo, config_path: str = "config/analytics/metrics.yaml"):
        self.repo = repo
        self.config = self._load_config(config_path)
        self.cache: dict[str, Any] = {}  # Naive in-memory cache for MVP. Catalyst cache in production.

    def _load_config(self, path: str) -> dict:
        try:
            with open(path) as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"Could not load analytics config {path}: {e}")
            return {"metrics": {}, "privacy_suppression": {"min_count_threshold": 5}}

    async def get_kpi(
        self,
        metric_id: str,
        district_id: str | None = None,
        police_station_id: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None
    ) -> dict[str, Any]:
        """Calculates a specific KPI and applies privacy suppression if needed."""
        # 1. Fetch raw count from repo
        current_value = await self.repo.calculate_kpi(
            metric_id,
            district_id=district_id,
            police_station_id=police_station_id,
            start_date=start_date,
            end_date=end_date
        )

        # 2. PoP Comparison (Period-over-Period) mock logic for MVP
        previous_value = int(current_value * 0.9) if current_value else 0
        absolute_change = current_value - previous_value
        perc_change = round((absolute_change / previous_value) * 100, 2) if previous_value else 0.0

        # 3. Privacy Suppression
        min_threshold = self.config.get("privacy_suppression", {}).get("min_count_threshold", 5)
        if 0 < current_value < min_threshold:
            return {
                "success": False,
                "error": {
                    "code": "SUPPRESSED_DUE_TO_LOW_COUNT",
                    "message": f"Results suppressed as count is below minimum threshold of {min_threshold}"
                }
            }

        return {
            "success": True,
            "data": {
                "metric": metric_id,
                "label": self.config.get("metrics", {}).get(metric_id, {}).get("description", metric_id),
                "value": current_value,
                "previous_value": previous_value,
                "absolute_change": absolute_change,
                "percentage_change": perc_change,
                "trend": "UP" if absolute_change > 0 else "DOWN" if absolute_change < 0 else "FLAT"
            },
            "context": {
                "filters": {
                    "district_id": district_id,
                    "police_station_id": police_station_id
                },
                "period": {
                    "start": start_date,
                    "end": end_date
                },
                "scope": "STATION" if police_station_id else "DISTRICT" if district_id else "GLOBAL",
                "freshness_timestamp": datetime.datetime.now().isoformat(),
                "data_status": "COMPLETE"
            }
        }

    async def get_trends(
        self,
        metric_id: str,
        grain: str = "daily",
        district_id: str | None = None,
        police_station_id: str | None = None
    ) -> dict[str, Any]:
        """Calculates time-series trends for charts."""
        trends = await self.repo.calculate_trend(
            metric_id,
            grain=grain,
            district_id=district_id,
            police_station_id=police_station_id
        )

        return {
            "success": True,
            "data": trends,
            "context": {
                "aggregation_grain": grain,
                "filters": {
                    "district_id": district_id,
                    "police_station_id": police_station_id
                }
            }
        }
