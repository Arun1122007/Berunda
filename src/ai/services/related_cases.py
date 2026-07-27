

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

    async def generate_candidates(self, source_fir_id: str, allowed_station_ids: list[str]) -> list[RelatedCaseCandidate]:
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
