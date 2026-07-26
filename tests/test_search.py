import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from src.ai.query_parser import QueryParser
from src.services.search_service import SearchService

@pytest.mark.asyncio
async def test_query_parser():
    parser = QueryParser()
    result = parser.parse("Looking for unsolved vehicle theft cases")
    
    assert "filters" in result
    assert result["filters"]["crime_category"] == [1] # Vehicle theft maps to 1
    assert result["filters"]["case_status"] == [1, 2] # Unsolved/pending

@pytest.mark.asyncio
@patch('src.ai.embedding_provider.OpenAIEmbeddingProvider.create_embedding', new_callable=AsyncMock)
@patch('src.repositories.vector_repo.SQLiteVectorStore.search', new_callable=AsyncMock)
async def test_hybrid_search(mock_search, mock_embed):
    # Mocking
    mock_embed.return_value = [0.1] * 1536
    mock_search.return_value = [
        {
            "id": "FIR_123",
            "score": 0.95,
            "metadata": {
                "fir_id": "123",
                "official_fir_number": "FIR/2026/123",
                "crime_category": "1"
            }
        }
    ]
    
    session = AsyncMock()
    service = SearchService(session)
    user = {"role": "officer", "district_id": 101}
    
    # Execution
    response = await service.search_hybrid("vehicle theft", user=user)
    
    # Validation
    assert response["query"] == "vehicle theft"
    assert len(response["results"]) == 1
    assert response["results"][0]["fir_id"] == "123"
    
    # Assert RBAC scope was applied to the vector search
    mock_search.assert_called_once()
    filters_passed = mock_search.call_args[1].get("filters")
    assert filters_passed["district_id"] == "101"
    
@pytest.mark.asyncio
async def test_rbac_citizen_blocked():
    session = AsyncMock()
    service = SearchService(session)
    user = {"role": "citizen"}
    
    with pytest.raises(PermissionError, match="Citizens are restricted"):
        await service.search_hybrid("vehicle theft", user=user)
