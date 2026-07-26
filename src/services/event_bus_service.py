"""Event Bus Service for Phase 3 Enterprise Scale Event-Driven Architecture.

Provides pub/sub decoupling for domain events (e.g. fir.created, entity.merged, anomaly.detected)
using Zoho Catalyst Signals or local async queue fallback.
"""
import asyncio
import logging
from collections.abc import Callable
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger("berunda.event_bus")


class EventBusService:
    """Event Bus abstraction for publishing and subscribing to enterprise domain events."""

    _instance: Optional["EventBusService"] = None

    def __init__(self):
        self.subscribers: dict[str, list[Callable[[dict[str, Any]], Any]]] = {}
        self.event_log: list[dict[str, Any]] = []
        self._queue: asyncio.Queue = asyncio.Queue()
        self._worker_task: asyncio.Task | None = None
        self._notification_service: Any | None = None

    @classmethod
    def get_instance(cls) -> "EventBusService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def connect_notification_service(self, notification_service: Any):
        """Link notification service to automatically broadcast events over WebSocket."""
        self._notification_service = notification_service
        logger.info("Connected NotificationService to EventBusService")

    def subscribe(self, topic: str, callback: Callable[[dict[str, Any]], Any]):
        """Subscribe a callback handler to a specific event topic or wildcard '*'."""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)
        logger.info(f"Subscribed callback {callback.__name__} to topic '{topic}'")

    async def publish(self, topic: str, payload: dict[str, Any], correlation_id: str | None = None) -> dict[str, Any]:
        """Publish an event to a topic asynchronously."""
        event = {
            "eventId": f"evt_{len(self.event_log) + 1000}",
            "topic": topic,
            "timestamp": datetime.utcnow().isoformat(),
            "correlationId": correlation_id or "system",
            "payload": payload,
        }
        self.event_log.append(event)
        logger.info(f"[EVENT BUS] Published event {event['eventId']} to topic '{topic}'")

        # Notify direct subscribers and wildcard subscribers
        handlers = self.subscribers.get(topic, []) + self.subscribers.get("*", [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Error executing event handler for topic '{topic}': {e}", exc_info=True)

        # Broadcast over WebSocket if notification service is connected
        if self._notification_service:
            try:
                await self._notification_service.broadcast(event_type=topic, payload=payload)
            except Exception as e:
                logger.warning(f"Failed to broadcast event over WebSocket: {e}")

        return event

    def get_recent_events(self, limit: int = 50, topic_filter: str | None = None) -> list[dict[str, Any]]:
        """Retrieve recent published events for audit or websocket broadcasting."""
        if topic_filter:
            events = [e for e in self.event_log if e["topic"] == topic_filter]
        else:
            events = self.event_log
        return events[-limit:]


# Global singleton instance access helper
def get_event_bus() -> EventBusService:
    return EventBusService.get_instance()
