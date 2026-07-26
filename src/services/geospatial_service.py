import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class GeospatialService:
    def __init__(self, repo):
        self.repo = repo
        self.min_count = 5 # Privacy threshold

    async def get_heatmap_data(
        self,
        district_id: Optional[str] = None,
        police_station_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Returns aggregated geographic cells representing incident density.
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
