from __future__ import annotations

from celery import shared_task


@shared_task(name="notifications.send")
def send_notification_task(
    user_id: int,
    title: str,
    message: str,
    channel: str = "in_app",
) -> dict:
    import logging

    logger = logging.getLogger(__name__)
    logger.info("Sending notification", extra={"user_id": user_id, "title": title, "channel": channel})
    return {
        "sent": True,
        "user_id": user_id,
        "title": title,
        "channel": channel,
    }
