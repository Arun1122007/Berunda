"""Idempotency key management — prevents duplicate operations."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any


class IdempotencyScope(str, Enum):
    FIR_CREATE = "fir:create"
    FIR_UPDATE = "fir:update"
    EVIDENCE_UPLOAD = "evidence:upload"
    AI_PROCESSING = "ai:processing"
    REPORT_REQUEST = "report:request"
    ASSIGNMENT = "assignment:create"


@dataclass
class IdempotencyRecord:
    key: str
    scope: str
    response_status: int
    response_body: str
    created_at: datetime
    expires_at: datetime

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.expires_at

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "scope": self.scope,
            "response_status": self.response_status,
            "response_body": self.response_body,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "is_expired": self.is_expired(),
        }


def generate_idempotency_key(scope: str, **params: Any) -> str:
    raw = scope + ":" + json.dumps(params, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def get_expiry(minutes: int = 60) -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)


class InMemoryIdempotencyStore:
    def __init__(self):
        self._store: dict[str, IdempotencyRecord] = {}

    async def get(self, key: str) -> IdempotencyRecord | None:
        record = self._store.get(key)
        if record is None:
            return None
        if record.is_expired():
            del self._store[key]
            return None
        return record

    async def set(self, record: IdempotencyRecord) -> None:
        self._store[record.key] = record

    async def exists(self, key: str) -> bool:
        record = self._store.get(key)
        if record is None:
            return False
        if record.is_expired():
            del self._store[key]
            return False
        return True


_idempotency_store = InMemoryIdempotencyStore()


def get_idempotency_store() -> InMemoryIdempotencyStore:
    return _idempotency_store
