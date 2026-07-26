from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict, Any

T = TypeVar("T")


class Repository(ABC, Generic[T]):

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        ...

    @abstractmethod
    def list(self, offset: int = 0, limit: int = 100, **filters: Any) -> List[T]:
        ...

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> T:
        ...

    @abstractmethod
    def update(self, entity_id: int, data: Dict[str, Any]) -> Optional[T]:
        ...

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        ...
