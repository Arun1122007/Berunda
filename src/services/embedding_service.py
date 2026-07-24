"""Embedding Service for generating and storing vector embeddings."""

from __future__ import annotations

import json

from sqlalchemy.ext.asyncio import AsyncSession

from src.ai.providers import create_provider
from src.models.int_models import RAGCorpusChunk
from src.services.base import BaseService


class EmbeddingService(BaseService):
    """Service for handling vector embeddings."""

    def __init__(self, session: AsyncSession, provider_name: str = "openai"):
        super().__init__(session)
        self.provider = create_provider(provider_name, model="text-embedding-3-small")

    async def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts using the configured provider."""
        if not texts:
            return []
        return await self.provider.embed(texts)

    async def store_chunks(self, chunks: list[dict]):
        """Store RAG chunks with their embeddings in the database."""
        # chunk format: {"CaseMasterID": int, "ChunkIndex": int, "ChunkText": str, "TenantDistrictID": int}  # noqa: E501

        texts_to_embed = [c["ChunkText"] for c in chunks]
        embeddings = await self.generate_embeddings(texts_to_embed)

        for i, chunk_data in enumerate(chunks):
            # Serialize embedding as JSON string for storage in Text column
            embedding_json = json.dumps(embeddings[i])

            chunk_record = RAGCorpusChunk(
                CaseMasterID=chunk_data.get("CaseMasterID"),
                ChunkIndex=chunk_data.get("ChunkIndex", 0),
                ChunkText=chunk_data.get("ChunkText"),
                TenantDistrictID=chunk_data.get("TenantDistrictID"),
                Embedding=embedding_json,
            )
            self.session.add(chunk_record)

        await self.session.commit()
