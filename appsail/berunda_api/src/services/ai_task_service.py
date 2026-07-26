import datetime
import logging
import uuid
from typing import Any

import yaml

from src.services.ai_provider import MockAIProvider
from src.services.privacy_gateway import PrivacyGateway

logger = logging.getLogger(__name__)

class AITaskService:
    def __init__(self, repo, config_path: str = "config/ai/prompts.yaml"):
        self.repo = repo
        self.provider = MockAIProvider()
        self.config = self._load_config(config_path)

    def _load_config(self, path: str) -> dict:
        try:
            with open(path) as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"Could not load AI config {path}: {e}")
            return {"prompts": {}}

    async def execute_task(self, fir_id: int, task_name: str, requested_by: int) -> dict[str, Any]:
        """Orchestrates the AI task.

        1. Fetches raw FIR.
        2. Applies Privacy Gateway.
        3. Formats the versioned Prompt.
        4. Calls Provider.
        5. Saves output for Human Review.
        """
        # 1. Fetch raw FIR
        fir_record = await self.repo.get_fir(fir_id)
        if not fir_record:
            return {"success": False, "error": {"code": "FIR_NOT_FOUND"}}

        raw_narrative = getattr(fir_record.occurrence, "BriefDescription", "No description available.")

        # 2. Privacy Masking
        safe_narrative, token_map = PrivacyGateway.apply_privacy_mask(raw_narrative)

        # 3. Prompt Construction
        prompt_config = self.config.get("prompts", {}).get(task_name, {})
        if not prompt_config:
            return {"success": False, "error": {"code": "PROMPT_NOT_CONFIGURED"}}

        formatted_prompt = prompt_config.get("template", "").format(narrative=safe_narrative)
        task_type = prompt_config.get("task", "unknown")

        # 4. Provider Call
        if task_type == "extraction":
            raw_result = await self.provider.generate_structured(formatted_prompt, {})
        else:
            raw_result = {"summary": await self.provider.generate_text(formatted_prompt)}

        # 5. Output Enveloping and Persistence
        output_id = f"AI_OUTPUT_{uuid.uuid4().hex[:8].upper()}"
        confidence = 0.85 # Mock confidence

        await self.repo.save_ai_task({
            "output_id": output_id,
            "task_type": task_name,
            "record_id": fir_id,
            "requested_by": requested_by,
            "status": "PENDING_REVIEW"
        })

        return {
            "success": True,
            "data": {
                "output_id": output_id,
                "task_type": task_name,
                "result": raw_result,
                "confidence": confidence,
                "confidence_band": "MEDIUM" if confidence < 0.9 else "HIGH",
                "review_required": True,
                "sources": [{"record_id": fir_id, "field": "BriefDescription"}]
            },
            "context": {
                "model": "hybrid-v1.0",
                "model_version": "1.0",
                "prompt_version": prompt_config.get("version", "1.0"),
                "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "privacy_profile": "INVESTIGATOR_VIEW"
            },
            "warnings": ["AI_GENERATED_REVIEW_REQUIRED"]
        }

    async def review_output(self, output_id: str, reviewer_id: int, status: str, feedback: str | None = None) -> dict:
        """Processes human-in-the-loop review actions (ACCEPTED, REJECTED, MODIFIED)."""
        updated = await self.repo.update_ai_review(output_id, reviewer_id, status, feedback)
        if not updated:
            return {"success": False, "error": {"code": "OUTPUT_NOT_FOUND"}}

        return {"success": True, "data": {"output_id": output_id, "status": status}}
