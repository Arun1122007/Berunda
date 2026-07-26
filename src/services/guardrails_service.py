"""Guardrails Service for tracking and enforcing AI safety policies."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.ai.guardrails import GuardrailManager, GuardrailResult
from src.models.gov_models import FairnessCheckResult
from src.services.base import BaseService
from src.shared.logging import get_logger

logger = get_logger(__name__)


class GuardrailsService(BaseService):
    """Service to enforce and log guardrails."""

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.manager = GuardrailManager()

    async def check_input(self, text: str, user_id: int | None = None) -> GuardrailResult:
        """Check user input and log if blocked."""
        result = self.manager.check_input(text)

        if not result.passed:
            logger.warning(f"Input guardrail triggered: {result.reason}")

        return result

    async def check_output(
        self, text: str, context: dict[str, Any] | None = None, user_id: int | None = None
    ) -> GuardrailResult:
        """Check AI output and log fairness/safety warnings."""
        result = self.manager.check_output(text, context)

        if not result.passed:
            logger.warning(f"Output guardrail triggered: {result.reason}")

            # Log sensitive term matches to FairnessCheckResult for audit
            if "demographic references" in result.reason:
                check_record = FairnessCheckResult(
                    CheckType="LLM Output Demographic Check",
                    Passed=0,
                    Details=result.reason,
                    CheckedBy=f"AI System (User: {user_id})" if user_id else "AI System",
                )
                self.session.add(check_record)
                try:
                    await self.session.commit()
                except Exception as e:
                    logger.error(f"Failed to log fairness check: {e}")
                    await self.session.rollback()

        return result
