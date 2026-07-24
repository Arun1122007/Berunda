from __future__ import annotations

import logging

from celery import shared_task

logger = logging.getLogger(__name__)


def _get_notification_service():
    try:
        from src.main import app
        return getattr(app.state, "notification_service", None)
    except Exception:
        return None


@shared_task(name="notifications.send")
def send_notification_task(
    user_id: int,
    title: str,
    message: str,
    channel: str = "in_app",
) -> dict:
    logger.info("Sending notification", extra={"user_id": user_id, "title": title, "channel": channel})
    if channel == "websocket":
        import asyncio
        service = _get_notification_service()
        if service is not None:
            asyncio.run_coroutine_threadsafe(
                service.send_to_user(user_id, "notification", {
                    "title": title,
                    "message": message,
                }),
                asyncio.get_event_loop(),
            )
    return {
        "sent": True,
        "user_id": user_id,
        "title": title,
        "channel": channel,
    }
