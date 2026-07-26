
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
