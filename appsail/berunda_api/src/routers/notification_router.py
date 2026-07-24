"""WebSocket notification router — real-time push for connected clients."""

from __future__ import annotations

import logging
from typing import Any

import jwt
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse

from src.middleware.auth import JWT_ALGORITHM, JWT_SECRET

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/notifications", tags=["Notifications"])


def _decode_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None


@router.websocket("/ws")
async def notification_websocket(websocket: WebSocket, token: str = ""):
    payload = _decode_token(token)
    if payload is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_id: int = payload.get("user_id")
    if user_id is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    service = getattr(
        websocket.app.state, "notification_service", None
    )
    if service is None:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        return

    await service.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await service.disconnect(user_id, websocket)


@router.get("/health")
async def notification_health() -> dict[str, Any]:
    from src.main import app

    service = getattr(app.state, "notification_service", None)
    return {
        "service": "notification_ws",
        "available": service is not None,
        "active_connections": service.active_connections if service else 0,
    }
