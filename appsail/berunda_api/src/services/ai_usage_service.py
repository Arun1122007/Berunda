"""AI Usage Tracking Service."""

from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.ai_models import AIUsageRecord
from src.services.base import BaseService

logger = logging.getLogger(__name__)

# Estimated costs per 1K tokens (USD)
COST_MODELS = {
    "llama-3.3-70b-versatile": {"in": 0.00059, "out": 0.00079},
    "mixtral-8x7b-32768": {"in": 0.00027, "out": 0.00027},
    "text-embedding-3-small": {"in": 0.00002, "out": 0.00},
}


class AIUsageService(BaseService):
    """Service to track AI API usage and estimate costs."""

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def track_usage(
        self,
        provider: str,
        model: str,
        feature: str,
        tokens_in: int,
        tokens_out: int,
        latency_ms: int = 0,
        user_id: int | None = None,
        district_id: int | None = None,
    ) -> AIUsageRecord:
        """Log an AI API call."""
        # Estimate cost
        cost_usd = 0.0
        if model in COST_MODELS:
            rates = COST_MODELS[model]
            cost_usd = (tokens_in / 1000.0) * rates["in"] + (tokens_out / 1000.0) * rates["out"]

        record = AIUsageRecord(
            Provider=provider,
            Model=model,
            Feature=feature,
            TokensIn=tokens_in,
            TokensOut=tokens_out,
            CostUSD=cost_usd,
            LatencyMs=latency_ms,
            UserID=user_id,
            DistrictID=district_id,
        )

        self.session.add(record)
        try:
            await self.session.commit()
            await self.session.refresh(record)
        except Exception as e:
            logger.error(f"Failed to track AI usage: {e}")
            await self.session.rollback()

        return record
