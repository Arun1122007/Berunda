"""WebSocket notification service — manages connections and broadcasting."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class NotificationService:
    """Manages WebSocket connections per user with thread-safe operations."""

    def __init__(self) -> None:
        self._connections: dict[int, list[WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, user_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._connections.setdefault(user_id, []).append(websocket)
        logger.info("WebSocket connected", extra={"user_id": user_id})

    async def disconnect(self, user_id: int, websocket: WebSocket) -> None:
        async with self._lock:
            conns = self._connections.get(user_id, [])
            if websocket in conns:
                conns.remove(websocket)
            if not conns:
                self._connections.pop(user_id, None)
        logger.info("WebSocket disconnected", extra={"user_id": user_id})

    async def send_to_user(
        self, user_id: int, event_type: str, payload: dict[str, Any] | None = None
    ) -> None:
        message = {"event": event_type, "payload": payload or {}}
        async with self._lock:
            conns = list(self._connections.get(user_id, []))
        for ws in conns:
            try:
                await ws.send_text(json.dumps(message))
            except Exception:
                logger.warning(
                    "Failed to send to user WS",
                    extra={"user_id": user_id},
                    exc_info=True,
                )

    async def broadcast(
        self, event_type: str, payload: dict[str, Any] | None = None
    ) -> None:
        message = {"event": event_type, "payload": payload or {}}
        async with self._lock:
            all_conns = [
                (uid, ws)
                for uid, conns in self._connections.items()
                for ws in list(conns)
            ]
        for user_id, ws in all_conns:
            try:
                await ws.send_text(json.dumps(message))
            except Exception:
                logger.warning(
                    "Failed to broadcast to user WS",
                    extra={"user_id": user_id},
                    exc_info=True,
                )

    @property
    def active_connections(self) -> int:
        return sum(len(conns) for conns in self._connections.values())
