import logging
from typing import Any

logger = logging.getLogger(__name__)

class GeospatialService:
    def __init__(self, repo):
        self.repo = repo
        self.min_count = 5 # Privacy threshold

    async def get_heatmap_data(
        self,
        district_id: str | None = None,
        police_station_id: str | None = None
    ) -> dict[str, Any]:
        """Returns aggregated geographic cells representing incident density.

        Applies bounding to prevent exact address reconstruction.
        """
        raw_clusters = await self.repo.get_geospatial_clusters(
            district_id=district_id,
            police_station_id=police_station_id
        )

        safe_clusters = []
        for cluster in raw_clusters:
            if cluster.get("count", 0) >= self.min_count:
                safe_clusters.append(cluster)

        if not safe_clusters:
            return {
                "success": False,
                "error": {
                    "code": "SUPPRESSED_DUE_TO_LOW_COUNT",
                    "message": "Insufficient data to safely render heatmap."
                }
            }

        return {
            "success": True,
            "data": safe_clusters,
            "context": {
                "suppression_applied": len(raw_clusters) != len(safe_clusters),
                "clusters_rendered": len(safe_clusters),
                "clusters_suppressed": len(raw_clusters) - len(safe_clusters)
            }
        }
