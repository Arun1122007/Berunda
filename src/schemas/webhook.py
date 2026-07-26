"""Pydantic schemas for Catalyst Webhook notifications and management."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from src.schemas.base import APIBase


class WebhookRegisterRequest(APIBase):
    """Request payload to register a new target webhook URL."""

    url: str = Field(..., description="Target URL (http://, https://, catalyst://, or signal://)")
    events: list[str] | None = Field(
        default=None,
        description="List of subscribed event topics (e.g. ['case.assigned', 'evidence.uploaded', 'supervisor.review.created']). None implies all events.",
    )
    secret: str | None = Field(
        default=None,
        description="Secret key for signing payloads with HMAC-SHA256 (header X-Catalyst-Signature).",
    )
    description: str | None = Field(default="", description="Optional description of the webhook destination.")


class WebhookResponse(APIBase):
    """Response payload for a registered webhook endpoint."""

    id: str = Field(..., description="Unique webhook registration ID")
    url: str = Field(..., description="Target webhook URL")
    events: list[str] = Field(default_factory=list, description="Subscribed event topics")
    description: str = Field(default="", description="Webhook description")
    created_at: str = Field(..., description="ISO 8601 registration timestamp")
    active: bool = Field(default=True, description="Whether the webhook is active")
    success_count: int = Field(default=0, description="Number of successful deliveries")
    failure_count: int = Field(default=0, description="Number of failed deliveries")


class WebhookDeliveryLogResponse(APIBase):
    """Response payload for a webhook delivery attempt log entry."""

    delivery_id: str = Field(..., description="Unique delivery attempt ID")
    webhook_id: str = Field(..., description="ID of the destination webhook")
    url: str = Field(..., description="Target URL delivered to")
    event_type: str = Field(..., description="Domain event topic")
    status: str = Field(..., description="Delivery status ('success' or 'failed')")
    status_code: int = Field(..., description="HTTP status code or simulated code")
    response: str = Field(..., description="Response body or error description")
    timestamp: str = Field(..., description="ISO 8601 delivery timestamp")
    attempts: int = Field(default=1, description="Number of delivery attempts made")


class WebhookTestDispatchRequest(APIBase):
    """Request payload to trigger a test event dispatch to webhooks."""

    event_type: str = Field(default="case.assigned", description="Event topic to simulate")
    payload: dict[str, Any] = Field(
        default_factory=lambda: {"test": True, "message": "Simulated Catalyst Webhook test event"},
        description="Event data payload",
    )
