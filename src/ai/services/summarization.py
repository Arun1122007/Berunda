
from pydantic import BaseModel

from src.ai.prompts.registry import PromptRegistry
from src.ai.providers import create_provider
from src.ai.schemas import Message


class SummarizationResult(BaseModel):
    summary: str
    is_ai_generated: bool = True
    prompt_version: str

class SummarizationService:
    def __init__(self, provider_name="mock"):
        self.provider = create_provider(provider_name)
        self.prompt_version = "v1"

    async def summarize(self, fir_text: str, user_authorized: bool = True) -> SummarizationResult:
        if not user_authorized:
            raise PermissionError("Unauthorized.")

        prompt = PromptRegistry.get("fir-summarization", self.prompt_version)
        messages = [Message(role="user", content=prompt.format(text=fir_text[:16000]))]

        if self.provider.provider_name == "mock":
            return SummarizationResult(summary="[AI GENERATED] The incident involved a vehicle theft on July 14.", prompt_version=self.prompt_version)

        return await self.provider.complete_structured(messages, SummarizationResult)
