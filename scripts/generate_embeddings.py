import argparse
import asyncio
import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.ai.embedding_provider import OpenAIEmbeddingProvider
from src.database import get_session
from src.models.src_models import CaseMaster
from src.repositories.vector_repo import SQLiteVectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("generate_embeddings")

async def process_batch(session, cases, embedding_provider, vector_store, dry_run=False):
    texts = []
    metadata_list = []
    record_ids = []

    for case in cases:
        if not case.occurrence or not case.occurrence.BriefFacts:
            continue
            
        # 1. Privacy Validation (Placeholder: assume BriefFacts is already masked by Phase 2 for this test)
        privacy_safe_narrative = case.occurrence.BriefFacts
        
        # 2. Text Construction Template
        text = f"Crime category: {case.CrimeMajorHeadID}\nSummary: {privacy_safe_narrative}"
        texts.append(text)
        
        # 3. Metadata Construction
        metadata = {
            "fir_id": str(case.CaseMasterID),
            "official_fir_number": case.CrimeNo,
            "police_station_id": str(case.PoliceStationID),
            "crime_category": str(case.CrimeMajorHeadID),
            "case_status": str(case.CaseStatusID),
            "privacy_profile": "AI_PROCESSING_SAFE",
            "synthetic_data": True
        }
        metadata_list.append(metadata)
        record_ids.append(f"FIR_{case.CaseMasterID}")

    if not texts:
        return 0

    if dry_run:
        logger.info(f"[DRY-RUN] Would generate {len(texts)} embeddings and store them.")
        return len(texts)

    # 4. Generate Embeddings
    try:
        logger.info(f"Generating embeddings for {len(texts)} records...")
        embeddings = await embedding_provider.create_embeddings(texts)
    except Exception as e:
        logger.error(f"Failed to generate embeddings: {e}")
        return 0

    # 5. Vector Storage
    records = []
    for i, vec in enumerate(embeddings):
        records.append({
            "id": record_ids[i],
            "vector": vec,
            "metadata": metadata_list[i]
        })
        
    await vector_store.upsert(records)
    logger.info(f"Upserted {len(records)} vectors successfully.")
    return len(records)

async def main():
    parser = argparse.ArgumentParser(description="Generate and store FIR semantic embeddings.")
    parser.add_argument("--dry-run", action="store_true", help="Run without persisting changes.")
    parser.add_argument("--limit", type=int, default=100, help="Maximum number of records to process.")
    args = parser.parse_args()

    async for session in get_session():
        embedding_provider = OpenAIEmbeddingProvider()
        vector_store = SQLiteVectorStore(session)

        # Ensure table exists
        if not args.dry_run:
            await vector_store._init_table()

        stmt = select(CaseMaster).options(selectinload(CaseMaster.occurrence)).limit(args.limit)
        result = await session.execute(stmt)
        cases = result.scalars().all()

        logger.info(f"Found {len(cases)} cases to process.")
        
        # Process in batches of 50
        batch_size = 50
        total_processed = 0
        for i in range(0, len(cases), batch_size):
            batch = cases[i:i + batch_size]
            processed = await process_batch(session, batch, embedding_provider, vector_store, dry_run=args.dry_run)
            total_processed += processed
            
        logger.info(f"Finished embedding generation. Processed {total_processed} valid records.")
        break # get_session yields once

if __name__ == "__main__":
    asyncio.run(main())
