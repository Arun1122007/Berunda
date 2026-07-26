"""FastAPI router for Catalyst Webhook notifications and management."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from src.middleware.auth import get_current_user, require_role
from src.schemas.webhook import (
    WebhookDeliveryLogResponse,
    WebhookRegisterRequest,
    WebhookResponse,
    WebhookTestDispatchRequest,
)
from src.services.event_bus_service import get_event_bus
from src.services.webhook_service import get_webhook_service

router = APIRouter(prefix="/api/v1/webhooks", tags=["Webhooks"])


@router.post("", response_model=WebhookResponse, status_code=status.HTTP_201_CREATED)
async def register_webhook(
    data: WebhookRegisterRequest,
    user: dict[str, Any] = Depends(require_role(["admin", "supervisor"])),
):
    """Register a new target webhook URL for domain event notifications."""
    service = get_webhook_service()
    try:
        record = service.register_webhook(
            url=data.url,
            events=data.events,
            secret=data.secret,
            description=data.description,
        )
        return record
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("", response_model=list[WebhookResponse])
async def list_webhooks(
    user: dict[str, Any] = Depends(require_role(["admin", "supervisor", "officer"])),
):
    """List all registered Catalyst Webhooks."""
    service = get_webhook_service()
    return service.list_webhooks()


@router.delete("/{webhook_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unregister_webhook(
    webhook_id: str,
    user: dict[str, Any] = Depends(require_role(["admin", "supervisor"])),
):
    """Remove a registered webhook endpoint."""
    service = get_webhook_service()
    if not service.unregister_webhook(webhook_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Webhook not found")
    return None


@router.get("/deliveries", response_model=list[WebhookDeliveryLogResponse])
async def get_delivery_logs(
    limit: int = 50,
    webhook_id: str | None = None,
    event_type: str | None = None,
    user: dict[str, Any] = Depends(require_role(["admin", "supervisor", "officer"])),
):
    """Retrieve recent webhook delivery attempt logs."""
    service = get_webhook_service()
    return service.get_delivery_log(limit=limit, webhook_id=webhook_id, event_type=event_type)


@router.post("/test-dispatch", response_model=list[WebhookDeliveryLogResponse])
async def test_dispatch_webhook(
    data: WebhookTestDispatchRequest,
    user: dict[str, Any] = Depends(require_role(["admin", "supervisor"])),
):
    """Trigger a simulated test event dispatch to matching registered webhooks."""
    event_bus = get_event_bus()
    await event_bus.publish(topic=data.event_type, payload=data.payload, correlation_id="test-dispatch")
    service = get_webhook_service()
    return service.get_delivery_log(limit=10, event_type=data.event_type)
