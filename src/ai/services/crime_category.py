

from pydantic import BaseModel

from src.ai.prompts.registry import PromptRegistry
from src.ai.providers import create_provider
from src.ai.schemas import Message


class CrimeCategorySuggestion(BaseModel):
    primary_category: str
    alternatives: list[str] = []
    explanation: str
    confidence: float | None = None

class CrimeCategoryService:
    def __init__(self, provider_name="mock"):
        self.provider = create_provider(provider_name)
        self.prompt_version = "v1"

    async def suggest(self, fir_text: str) -> CrimeCategorySuggestion:
        prompt = PromptRegistry.get("crime-category", self.prompt_version)
        messages = [Message(role="user", content=prompt.format(text=fir_text[:16000]))]

        if self.provider.provider_name == "mock":
            return CrimeCategorySuggestion(primary_category="Vehicle Theft", explanation="Mention of stolen car", confidence=0.85)

        return await self.provider.complete_structured(messages, CrimeCategorySuggestion)
