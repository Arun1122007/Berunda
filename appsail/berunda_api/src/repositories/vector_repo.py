from __future__ import annotations

import json
import logging

import numpy as np
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.ai.vector_store import VectorStore

logger = logging.getLogger("berunda.vector_repo")


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(v1, v2) / (norm1 * norm2))


class SQLiteVectorStore(VectorStore):
    """Local SQLite-based mock vector store.

    In a real production environment, this would be Pinecone or pgvector.
    We are simulating vector search by storing the vector as JSON and computing
    cosine similarity in memory during retrieval.
    """

    def __init__(self, session: AsyncSession, table_name: str = "SearchVectorIndex"):
        self.session = session
        self.table_name = table_name

    async def _init_table(self):
        """Create the table if it doesn't exist."""
        # Using a raw query for the mock table to avoid complex migrations for this phase
        await self.session.execute(
            text(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id TEXT PRIMARY KEY,
                vector_json TEXT,
                metadata_json TEXT
            )
            """)
        )
        await self.session.commit()

    async def upsert(self, records: list[dict]):
        await self._init_table()
        for r in records:
            stmt = text(f"""
                INSERT INTO {self.table_name} (id, vector_json, metadata_json)
                VALUES (:id, :vector, :metadata)
                ON CONFLICT(id) DO UPDATE SET
                vector_json = :vector, metadata_json = :metadata
            """)
            await self.session.execute(stmt, {
                "id": r["id"],
                "vector": json.dumps(r["vector"]),
                "metadata": json.dumps(r.get("metadata", {}))
            })
        await self.session.commit()

    async def search(self, vector: list[float], filters: dict, limit: int = 10) -> list[dict]:
        await self._init_table()

        # Load all records (simulate vector scan)
        result = await self.session.execute(text(f"SELECT id, vector_json, metadata_json FROM {self.table_name}"))
        rows = result.fetchall()

        scored_results = []
        for row in rows:
            record_id, vec_str, meta_str = row
            try:
                record_vec = json.loads(vec_str)
                meta = json.loads(meta_str)

                # Apply hard filters (Metadata Scope filtering)
                match = True
                for k, v in filters.items():
                    if k not in meta:
                        match = False
                        break

                    if isinstance(v, list):
                        if meta[k] not in v:
                            match = False
                            break
                    else:
                        if meta[k] != v:
                            match = False
                            break

                if not match:
                    continue

                score = cosine_similarity(vector, record_vec)
                scored_results.append({
                    "id": record_id,
                    "score": score,
                    "metadata": meta
                })
            except Exception as e:
                logger.error(f"Error parsing vector record {record_id}: {e}")

        # Sort and limit
        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:limit]

    async def delete(self, record_ids: list[str]):
        await self._init_table()
        if not record_ids:
            return

        placeholders = ",".join(f":id_{i}" for i in range(len(record_ids)))
        params = {f"id_{i}": val for i, val in enumerate(record_ids)}

        stmt = text(f"DELETE FROM {self.table_name} WHERE id IN ({placeholders})")
        await self.session.execute(stmt, params)
        await self.session.commit()

    async def fetch(self, record_ids: list[str]) -> list[dict]:
        await self._init_table()
        if not record_ids:
            return []

        placeholders = ",".join(f":id_{i}" for i in range(len(record_ids)))
        params = {f"id_{i}": val for i, val in enumerate(record_ids)}

        stmt = text(f"SELECT id, vector_json, metadata_json FROM {self.table_name} WHERE id IN ({placeholders})")
        result = await self.session.execute(stmt, params)

        out = []
        for row in result.fetchall():
            out.append({
                "id": row[0],
                "vector": json.loads(row[1]),
                "metadata": json.loads(row[2])
            })
        return out

    def health_check(self) -> dict:
        return {"status": "ok", "type": "sqlite_mock"}
