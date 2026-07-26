from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Sequence

from src.domain.models import FIR, Session, User


class FIRRepository(ABC):
    @abstractmethod
    async def list(
        self,
        district_id: Optional[str] = None,
        police_station_id: Optional[str] = None,
        case_status_id: Optional[str] = None,
        crime_major_head_id: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[Sequence[FIR], int]:
        ...

    @abstractmethod
    async def get_by_id(self, fir_id: uuid.UUID) -> Optional[FIR]:
        ...

    @abstractmethod
    async def get_by_crime_no(self, crime_no: str) -> Optional[FIR]:
        ...

    @abstractmethod
    async def create(self, fir: FIR) -> FIR:
        ...

    @abstractmethod
    async def update(self, fir: FIR) -> FIR:
        ...

    @abstractmethod
    async def delete(self, fir_id: uuid.UUID) -> None:
        ...


class UserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        ...

    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        ...

    @abstractmethod
    async def create(self, user: User) -> User:
        ...

    @abstractmethod
    async def list_by_district(self, district_id: str) -> Sequence[User]:
        ...


class SessionRepository(ABC):
    @abstractmethod
    async def create(self, session: Session) -> Session:
        ...

    @abstractmethod
    async def revoke(self, session_id: uuid.UUID) -> None:
        ...

    @abstractmethod
    async def find_by_hash(self, token_hash: str) -> Optional[Session]:
        ...

    @abstractmethod
    async def find_active_by_user_id(self, user_id: uuid.UUID) -> Optional[Session]:
        ...
