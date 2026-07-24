"""AI observability — token tracking, cost monitoring, latency measurement, and quality metrics."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TelemetryEvent:
    event_type: str  # completion, tool_call, error
    provider: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_ms: float = 0.0
    cost: float = 0.0
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class TelemetryStore:
    """Ring-buffer telemetry store."""

    def __init__(self, max_events: int = 1000):
        self.events: list[TelemetryEvent] = []
        self.max_events = max_events

    def record(self, event: TelemetryEvent) -> None:
        self.events.append(event)
        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events :]

    def record_completion(
        self,
        provider: str,
        model: str,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        latency_ms: float = 0.0,
        error: str | None = None,
    ) -> None:
        cost = (prompt_tokens * 0.000002) + (completion_tokens * 0.000008)
        self.record(
            TelemetryEvent(
                event_type="error" if error else "completion",
                provider=provider,
                model=model,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                latency_ms=latency_ms,
                cost=cost,
                error=error,
            )
        )

    def get_stats(self) -> dict[str, Any]:
        if not self.events:
            return {}

        total = len(self.events)
        errors = sum(1 for e in self.events if e.error)
        total_cost = sum(e.cost for e in self.events)
        total_tokens = sum(e.prompt_tokens + e.completion_tokens for e in self.events)
        avg_latency = sum(e.latency_ms for e in self.events) / total if total else 0

        return {
            "total_requests": total,
            "error_rate": errors / total if total else 0,
            "total_cost": round(total_cost, 6),
            "total_tokens": total_tokens,
            "avg_latency_ms": round(avg_latency, 2),
            "errors": errors,
        }

    def get_events(
        self,
        event_type: str | None = None,
        limit: int = 100,
    ) -> list[TelemetryEvent]:
        filtered = self.events
        if event_type:
            filtered = [e for e in filtered if e.event_type == event_type]
        return filtered[-limit:]

    def clear(self) -> None:
        self.events = []


telemetry = TelemetryStore()


class TelemetryMiddleware:
    """Middleware to automatically record telemetry."""

    async def wrap_completion(self, provider: Any, prompt: str, **kwargs) -> str:
        start = time.time()
        try:
            result = await provider.complete(prompt, **kwargs)
            telemetry.record_completion(
                provider=provider.__class__.__name__,
                model=provider.model if hasattr(provider, "model") else "unknown",
                latency_ms=(time.time() - start) * 1000,
            )
            return result
        except Exception as e:
            telemetry.record_completion(
                provider=provider.__class__.__name__,
                model=provider.model if hasattr(provider, "model") else "unknown",
                latency_ms=(time.time() - start) * 1000,
                error=str(e),
            )
            raise
