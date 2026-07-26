import os

services_dir = r"c:\Hackathons\H2S\Berunda\src\ai\services"
os.makedirs(services_dir, exist_ok=True)

files = {
    "__init__.py": "",
    "fir_extraction.py": """
from typing import List, Optional
from pydantic import BaseModel, Field
from src.ai.providers import create_provider
from src.ai.prompts.registry import PromptRegistry
from src.ai.schemas import Message

class ExtractedField(BaseModel):
    field_name: str
    suggested_value: str
    source_reference: Optional[str] = None
    confidence: Optional[float] = None
    status: str = "suggested"

class FIRExtractionResult(BaseModel):
    fields: List[ExtractedField]
    warnings: List[str] = []
    unsupported_fields: List[str] = []
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
""",

    "summarization.py": """
from pydantic import BaseModel
from src.ai.providers import create_provider
from src.ai.prompts.registry import PromptRegistry
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
""",

    "crime_category.py": """
from typing import List, Optional
from pydantic import BaseModel
from src.ai.providers import create_provider
from src.ai.prompts.registry import PromptRegistry
from src.ai.schemas import Message

class CrimeCategorySuggestion(BaseModel):
    primary_category: str
    alternatives: List[str] = []
    explanation: str
    confidence: Optional[float] = None

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
""",

    "related_cases.py": """
from typing import List
from pydantic import BaseModel
from src.ai.providers import create_provider

class RelatedCaseCandidate(BaseModel):
    candidate_fir_id: str
    relevance_indicator: str
    explanation: str
    generator_version: str

class RelatedCaseService:
    def __init__(self, provider_name="mock"):
        self.provider = create_provider(provider_name)
        self.generator_version = "v1"

    async def generate_candidates(self, source_fir_id: str, allowed_station_ids: List[str]) -> List[RelatedCaseCandidate]:
        # Enforce authorization BEFORE candidate generation
        if not allowed_station_ids:
            return []
            
        if self.provider.provider_name == "mock":
            return [
                RelatedCaseCandidate(
                    candidate_fir_id=f"{allowed_station_ids[0]}-FIR-999",
                    relevance_indicator="High",
                    explanation="Shared vehicle license plate",
                    generator_version=self.generator_version
                )
            ]
        return []
""",

    "semantic_search.py": """
from typing import List
from pydantic import BaseModel
from src.ai.providers import create_provider

class SearchResult(BaseModel):
    fir_id: str
    explanation: str
    score: float

class SemanticSearchService:
    def __init__(self, provider_name="mock"):
        self.provider = create_provider(provider_name)

    async def search(self, query: str, allowed_station_ids: List[str]) -> List[SearchResult]:
        if not allowed_station_ids:
            return []

        embeddings = await self.provider.embed([query])
        
        if self.provider.provider_name == "mock":
            return [
                SearchResult(fir_id=f"{allowed_station_ids[0]}-FIR-101", explanation="Matches vehicle theft", score=0.95)
            ]
        return []
""",

    "investigation_assistant.py": """
from pydantic import BaseModel
from src.ai.providers import create_provider
from src.ai.prompts.registry import PromptRegistry
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
"""
}

for filename, content in files.items():
    path = os.path.join(services_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Created {len(files)} AI services in {services_dir}")
