
from pydantic import BaseModel

from src.ai.prompts.registry import PromptRegistry
from src.ai.providers import create_provider
from src.ai.schemas import Message


class AssistantResponse(BaseModel):
    answer: str
    citations: list[str]

class InvestigationAssistantService:
    def __init__(self, provider_name="mock"):
        self.provider = create_provider(provider_name)
        self.prompt_version = "v1"

    async def answer_question(self, question: str, context: str, user_authorized: bool = True) -> AssistantResponse:
        if not user_authorized:
            raise PermissionError("Unauthorized to query this context.")

        prompt = PromptRegistry.get("investigation-assistant", self.prompt_version)
        messages = [Message(role="user", content=prompt.format(context=context, question=question))]

        if self.provider.provider_name == "mock":
            if "ignore" in question.lower() or "all cases" in question.lower():
                return AssistantResponse(answer="I cannot fulfill this request.", citations=[])
            return AssistantResponse(answer="Based on the FIR, the incident occurred at 10 PM.", citations=["FIR-paragraph-2"])

        return await self.provider.complete_structured(messages, AssistantResponse)
