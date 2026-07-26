import pytest
from sqlalchemy import select

from src.models.int_models import AIExtractionQueue, ERMergeCandidate
from src.models.src_models import CaseMaster, EvidenceMaster


@pytest.mark.asyncio
async def test_schema_phase3_tables_exist(in_memory_db):
    """
    Verify that the Phase 3 P0 tables can be queried and exist in the schema.
    """
    async with in_memory_db() as session:
        # Just selecting from them will fail if the table doesn't exist
        case_query = await session.execute(select(CaseMaster).limit(1))
        assert case_query is not None

        evidence_query = await session.execute(select(EvidenceMaster).limit(1))
        assert evidence_query is not None

        ai_queue_query = await session.execute(select(AIExtractionQueue).limit(1))
        assert ai_queue_query is not None

        er_queue_query = await session.execute(select(ERMergeCandidate).limit(1))
        assert er_queue_query is not None

    print("Phase 3 schema tables exist and can be queried.")
