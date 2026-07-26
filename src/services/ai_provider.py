import asyncio
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class AIProvider(ABC):
    @abstractmethod
    async def generate_text(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    async def generate_structured(self, prompt: str, schema: dict, **kwargs) -> dict:
        pass

class MockAIProvider(AIProvider):
    """Mock Provider for local testing when external API keys are unavailable."""
    async def generate_text(self, prompt: str, **kwargs) -> str:
        await asyncio.sleep(0.5) # Simulate latency
        logger.info(f"Mock Provider received prompt: {prompt[:50]}...")
        if "Summarize" in prompt:
            return "This is an AI-generated mock summary of the incident preserving uncertainty."
        if "category" in prompt:
            return "THEFT"
        return "Mock text generation."

    async def generate_structured(self, prompt: str, schema: dict, **kwargs) -> dict:
        await asyncio.sleep(0.5)
        logger.info("Mock Provider structured generation...")
        return {
            "persons": ["UNKNOWN_MALE_1"],
            "locations": ["M.G. Road"],
            "dates": ["2026-07-26"],
            "stolen_items": ["Wallet"]
        }
