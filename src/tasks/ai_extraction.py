"""Background task for AI extraction and suggestion generation."""

from __future__ import annotations

import asyncio
import logging

from src.config import settings
from src.database import get_session_factory

logger = logging.getLogger(__name__)


def request_ai_extraction_task(case_master_id: int) -> dict:
    """Trigger AI extraction background task for a newly submitted or updated FIR."""
    if not getattr(settings, "ENABLE_AI_REVIEW", True):
        logger.info("AI review disabled via settings; skipping extraction for FIR %s", case_master_id)
        return {"status": "DISABLED", "case_master_id": case_master_id}

    async def _run():
        from src.services.ai_assistant_service import AIAssistantService

        async with get_session_factory()() as session:
            svc = AIAssistantService(session)
            try:
                entry = await svc.extract_suggestions(case_master_id)
                return {
                    "status": "SUCCESS",
                    "extraction_id": entry.ExtractionID,
                    "case_master_id": case_master_id,
                }
            except Exception as e:
                logger.error("Failed to run AI extraction for FIR %s: %s", case_master_id, e)
                return {"status": "ERROR", "error": str(e), "case_master_id": case_master_id}

    return asyncio.run(_run())
