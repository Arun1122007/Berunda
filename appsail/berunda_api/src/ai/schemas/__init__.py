"""AI schemas — request/response models, input validation, and serialization for AI operations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class ToolResult:
    id: str
    output: Any = None
    error: str | None = None


@dataclass
class Message:
    role: str  # user, assistant, system, tool
    content: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)
    tool_call_id: str | None = None


@dataclass
class AgentRequest:
    messages: list[Message]
    agent_type: str = "investigator"
    max_tokens: int = 4096
    temperature: float = 0.3
    stream: bool = False


@dataclass
class AgentResponse:
    content: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)
    finish_reason: str = "stop"
    usage: dict[str, int] = field(default_factory=dict)
    processing_time_ms: float = 0.0


@dataclass
class AgentConfig:
    system_prompt: str = ""
    max_tool_rounds: int = 5
    enable_guardrails: bool = True
    memory_type: str = "in_memory"
    memory_kwargs: dict = field(default_factory=lambda: {"max_history": 20})
    temperature: float = 0.3
    max_tokens: int = 4096
