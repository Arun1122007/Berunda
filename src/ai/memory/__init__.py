"""Memory management — conversation history, persistent context, and retrieval-augmented memory."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Message:
    role: str  # user, assistant, system
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseMemory(ABC):
    """Abstract base class for memory systems."""

    @abstractmethod
    def add(self, message: Message) -> None:
        pass

    @abstractmethod
    def get_history(self, limit: int | None = None) -> list[Message]:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass


class InMemoryMemory(BaseMemory):
    """Simple in-memory message store."""

    def __init__(self, max_history: int = 20):
        self.messages: list[Message] = []
        self.max_history = max_history

    def add(self, message: Message) -> None:
        self.messages.append(message)
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history :]

    def get_history(self, limit: int | None = None) -> list[Message]:
        if limit:
            return self.messages[-limit:]
        return self.messages

    def clear(self) -> None:
        self.messages = []


class TokenWindowMemory(BaseMemory):
    """Sliding window memory based on token count."""

    def __init__(self, max_tokens: int = 4096):
        self.messages: list[Message] = []
        self.max_tokens = max_tokens

    def add(self, message: Message) -> None:
        self.messages.append(message)
        self._trim()

    def _trim(self) -> None:
        while self._estimate_tokens() > self.max_tokens and len(self.messages) > 1:
            self.messages.pop(0)

    def _estimate_tokens(self) -> int:
        total = sum(len(m.content) for m in self.messages)
        return total // 4

    def get_history(self, limit: int | None = None) -> list[Message]:
        if limit:
            return self.messages[-limit:]
        return self.messages

    def clear(self) -> None:
        self.messages = []


def create_memory(memory_type: str = "in_memory", **kwargs) -> BaseMemory:
    memories = {
        "in_memory": InMemoryMemory,
        "token_window": TokenWindowMemory,
    }
    if memory_type not in memories:
        raise ValueError(f"Unknown memory type: {memory_type}")
    return memories[memory_type](**kwargs)
