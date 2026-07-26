"""Catalyst Webhook Service — Real-time event notifications via Zoho Catalyst Webhooks.

Dispatches real-time HTTP POST webhook notifications for domain events:
- case.assigned
- evidence.uploaded
- supervisor.review.created
"""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any

import httpx

from src.shared.logging import get_logger

logger = get_logger(__name__)


class CatalystWebhookService:
    """Manages target webhook registrations and delivers real-time event notifications."""

    _instance: CatalystWebhookService | None = None

    def __init__(self) -> None:
        self._webhooks: dict[str, dict[str, Any]] = {}
        self._delivery_log: list[dict[str, Any]] = []
        self._lock = asyncio.Lock()

        # Check for default environment webhook
        env_url = os.environ.get("CATALYST_WEBHOOK_URL")
        if env_url:
            self.register_webhook(
                url=env_url,
                events=None,
                secret=os.environ.get("CATALYST_WEBHOOK_SECRET"),
                description="Default environment webhook",
            )

    @classmethod
    def get_instance(cls) -> CatalystWebhookService:
        if cls._instance is None:
            cls._instance = cls()
            from src.services.event_bus_service import EventBusService
            if EventBusService._instance is not None:
                EventBusService._instance.connect_webhook_service(cls._instance)
        return cls._instance

    def register_webhook(
        self,
        url: str,
        events: list[str] | None = None,
        secret: str | None = None,
        description: str | None = "",
    ) -> dict[str, Any]:
        """Register a new target webhook endpoint."""
        if not any(url.startswith(p) for p in ("http://", "https://", "catalyst://", "signal://", "mock://", "test://")):
            raise ValueError("URL must start with http://, https://, catalyst://, signal://, mock://, or test://")

        webhook_id = f"whk_{uuid.uuid4().hex[:8]}"
        record = {
            "id": webhook_id,
            "url": url,
            "events": events or [],
            "secret": secret,
            "description": description or "",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "active": True,
            "success_count": 0,
            "failure_count": 0,
        }
        self._webhooks[webhook_id] = record
        logger.info(f"Registered Catalyst Webhook {webhook_id} targeting {url} for events: {events or 'ALL'}")
        return self._format_webhook_response(record)

    def unregister_webhook(self, webhook_id: str) -> bool:
        """Remove a registered webhook endpoint."""
        if webhook_id in self._webhooks:
            del self._webhooks[webhook_id]
            logger.info(f"Unregistered Catalyst Webhook {webhook_id}")
            return True
        return False

    def list_webhooks(self) -> list[dict[str, Any]]:
        """Return all registered webhooks."""
        return [self._format_webhook_response(record) for record in self._webhooks.values()]

    def get_delivery_log(
        self, limit: int = 50, webhook_id: str | None = None, event_type: str | None = None
    ) -> list[dict[str, Any]]:
        """Retrieve recent webhook delivery logs."""
        logs = self._delivery_log
        if webhook_id:
            logs = [entry for entry in logs if entry["webhook_id"] == webhook_id]
        if event_type:
            logs = [entry for entry in logs if entry["event_type"] == event_type]
        return logs[-limit:]

    async def dispatch(
        self,
        event_type: str,
        payload: dict[str, Any],
        correlation_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Dispatch an event payload to all matching registered webhook targets asynchronously."""
        async with self._lock:
            active_targets = [
                wh
                for wh in self._webhooks.values()
                if wh["active"]
                and (not wh["events"] or "*" in wh["events"] or event_type in wh["events"])
            ]

        if not active_targets:
            logger.debug(f"No active webhooks subscribed to event '{event_type}'")
            return []

        event_id = f"wh_evt_{uuid.uuid4().hex[:12]}"
        timestamp = datetime.now(timezone.utc).isoformat()
        body_data = {
            "id": event_id,
            "event": event_type,
            "timestamp": timestamp,
            "correlationId": correlation_id or "system",
            "payload": payload,
            "source": "zoho-catalyst-signals",
        }
        body_bytes = json.dumps(body_data, sort_keys=True).encode("utf-8")

        results = []
        for target in active_targets:
            res = await self._send_to_target(target, event_id, event_type, timestamp, body_bytes, correlation_id)
            results.append(res)

        return results

    async def _send_to_target(
        self,
        target: dict[str, Any],
        event_id: str,
        event_type: str,
        timestamp: str,
        body_bytes: bytes,
        correlation_id: str | None,
    ) -> dict[str, Any]:
        url = target["url"]
        webhook_id = target["id"]
        headers = {
            "Content-Type": "application/json",
            "X-Catalyst-Event": event_type,
            "X-Catalyst-Webhook-ID": event_id,
            "X-Catalyst-Delivery": timestamp,
        }
        if correlation_id:
            headers["X-Correlation-ID"] = correlation_id
        if target["secret"]:
            sig = hmac.new(target["secret"].encode("utf-8"), body_bytes, hashlib.sha256).hexdigest()
            headers["X-Catalyst-Signature"] = f"sha256={sig}"

        delivery_id = f"del_{uuid.uuid4().hex[:8]}"
        attempts = 0
        max_attempts = 3
        status = "failed"
        status_code = 500
        response_text = ""

        # Check if simulated/serverless signal target
        if any(url.startswith(p) for p in ("catalyst://", "signal://", "mock://", "test://")):
            attempts = 1
            status = "success"
            status_code = 200
            response_text = f"Catalyst Signal dispatched successfully to {url}"
            async with self._lock:
                target["success_count"] += 1
        else:
            async with httpx.AsyncClient(timeout=10.0) as client:
                for attempt in range(1, max_attempts + 1):
                    attempts = attempt
                    try:
                        resp = await client.post(url, content=body_bytes, headers=headers)
                        status_code = resp.status_code
                        response_text = resp.text[:200]
                        if 200 <= status_code < 300:
                            status = "success"
                            async with self._lock:
                                target["success_count"] += 1
                            break
                        else:
                            if attempt < max_attempts:
                                await asyncio.sleep(0.5 * (2 ** (attempt - 1)))
                    except Exception as exc:
                        response_text = f"Error: {exc!s}"
                        if attempt < max_attempts:
                            await asyncio.sleep(0.5 * (2 ** (attempt - 1)))

            if status != "success":
                async with self._lock:
                    target["failure_count"] += 1

        log_entry = {
            "delivery_id": delivery_id,
            "webhook_id": webhook_id,
            "url": url,
            "event_type": event_type,
            "status": status,
            "status_code": status_code,
            "response": response_text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "attempts": attempts,
        }

        async with self._lock:
            self._delivery_log.append(log_entry)
            if len(self._delivery_log) > 500:
                self._delivery_log = self._delivery_log[-500:]

        logger.info(
            f"[CATALYST WEBHOOK] Delivery {delivery_id} ({status}) to {url} for event '{event_type}' "
            f"(HTTP {status_code}, {attempts} attempt(s))"
        )
        return log_entry

    def _format_webhook_response(self, record: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": record["id"],
            "url": record["url"],
            "events": record["events"],
            "description": record["description"],
            "created_at": record["created_at"],
            "active": record["active"],
            "success_count": record["success_count"],
            "failure_count": record["failure_count"],
        }


def get_webhook_service() -> CatalystWebhookService:
    return CatalystWebhookService.get_instance()
