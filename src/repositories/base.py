import abc
from typing import Any, Generic, TypeVar

T = TypeVar('T')

class BaseRepository(Generic[T], abc.ABC):
    """Abstract Base Class for Data Repositories."""

    @abc.abstractmethod
    async def get_by_id(self, id: str) -> T | None:
        """Fetch a single record by its primary key."""
        pass

    @abc.abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100, filters: dict[str, Any] | None = None) -> list[T]:
        """List records with pagination and optional filtering."""
        pass

    @abc.abstractmethod
    async def create(self, data: T) -> T:
        """Create a new record."""
        pass

    @abc.abstractmethod
    async def update(self, id: str, data: dict[str, Any]) -> T | None:
        """Update an existing record."""
        pass

    @abc.abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete (or soft delete) a record."""
        pass
