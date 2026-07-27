

from pydantic import BaseModel

from src.ai.prompts.registry import PromptRegistry
from src.ai.providers import create_provider
from src.ai.schemas import Message


class ExtractedField(BaseModel):
    field_name: str
    suggested_value: str
    source_reference: str | None = None
    confidence: float | None = None
    status: str = "suggested"

class FIRExtractionResult(BaseModel):
    fields: list[ExtractedField]
    warnings: list[str] = []
    unsupported_fields: list[str] = []
    prompt_version: str

class FIRExtractionService:
    def __init__(self, provider_name="mock"):
        self.provider = create_provider(provider_name)
        self.prompt_version = "v1"

    async def extract(self, fir_text: str, user_authorized: bool = True) -> FIRExtractionResult:
        if not user_authorized:
            raise PermissionError("User is not authorized to extract this FIR.")

        prompt = PromptRegistry.get("fir-extraction", self.prompt_version)
        formatted_prompt = prompt.format(text=fir_text[:16000])

        messages = [Message(role="user", content=formatted_prompt)]

        # We assume the mock provider returns valid json when we ask it, or we can mock the structured result here.
        if self.provider.provider_name == "mock":
            # Deterministic mock return for evaluation
            return FIRExtractionResult(
                fields=[
                    ExtractedField(field_name="incident_date", suggested_value="2026-07-14", source_reference="source-span-01", confidence=0.91)
                ],
                prompt_version=self.prompt_version
            )

        return await self.provider.complete_structured(messages, FIRExtractionResult)
