"""Repository abstractions and database adapter implementations."""

from src.repositories.catalyst_adapter import (
    CatalystAuditRepository,
    CatalystAuthRepository,
    CatalystEntityRepository,
    CatalystFIRRepository,
)
from src.repositories.core import (
    AuditRepository,
    AuthRepository,
    EntityRepository,
    FileStorage,
    FIRRepository,
    RepositoryFactory,
)
from src.repositories.factory import EnvironmentRepositoryFactory, get_repository_factory
from src.repositories.sqlite_adapter import (
    SQLiteAuditRepository,
    SQLiteAuthRepository,
    SQLiteEntityRepository,
    SQLiteFIRRepository,
)

__all__ = [
    "AuditRepository",
    "AuthRepository",
    "CatalystAuditRepository",
    "CatalystAuthRepository",
    "CatalystEntityRepository",
    "CatalystFIRRepository",
    "EntityRepository",
    "EnvironmentRepositoryFactory",
    "FIRRepository",
    "FileStorage",
    "RepositoryFactory",
    "SQLiteAuditRepository",
    "SQLiteAuthRepository",
    "SQLiteEntityRepository",
    "SQLiteFIRRepository",
    "get_repository_factory",
]
