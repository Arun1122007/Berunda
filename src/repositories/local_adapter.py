from typing import Any, Dict, List, Optional, TypeVar
import uuid

from src.repositories.base import BaseRepository

T = TypeVar('T')

class LocalMemoryRepository(BaseRepository[T]):
    """In-memory fallback repository for local development and testing."""

    def __init__(self, model_cls: type):
        self.model_cls = model_cls
        self._store: Dict[str, Dict[str, Any]] = {}

    async def get_by_id(self, id: str) -> Optional[T]:
        data = self._store.get(id)
        if data:
            return self.model_cls(**data)
        return None

    async def list_all(self, skip: int = 0, limit: int = 100, filters: Optional[Dict[str, Any]] = None) -> List[T]:
        results = []
        for data in list(self._store.values()):
            match = True
            if filters:
                for k, v in filters.items():
                    if data.get(k) != v:
                        match = False
                        break
            if match:
                results.append(self.model_cls(**data))
                
        # Apply skip and limit
        return results[skip : skip + limit]

    async def create(self, data: T) -> T:
        row_data = data.dict() if hasattr(data, "dict") else vars(data)
        
        # Auto-generate ID if missing
        record_id = row_data.get("ROWID") or row_data.get("id") or str(uuid.uuid4())
        row_data["ROWID"] = record_id
        
        self._store[record_id] = row_data
        return self.model_cls(**row_data)

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[T]:
        if id not in self._store:
            return None
        self._store[id].update(data)
        return self.model_cls(**self._store[id])

    async def delete(self, id: str) -> bool:
        if id in self._store:
            del self._store[id]
            return True
        return False
