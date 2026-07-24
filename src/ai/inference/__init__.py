"""Inference engine — LLM invocation, streaming, fallback, retry, and response parsing."""

from __future__ import annotations

import asyncio
from typing import Any


class InferenceEngine:
    """Robust LLM inference with retry, fallback, and streaming."""

    def __init__(
        self,
        primary_provider: Any,
        fallback_provider: Any | None = None,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 30.0,
    ):
        self.primary = primary_provider
        self.fallback = fallback_provider
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    async def complete(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 4096,
        stream: bool = False,
        **kwargs,
    ) -> str:
        """Complete with retry and fallback."""
        last_error = None

        for attempt in range(self.max_retries):
            try:
                if stream:
                    result = ""
                    async for chunk in self.primary.complete_stream(
                        prompt, temperature=temperature, max_tokens=max_tokens, **kwargs
                    ):
                        result += chunk
                    return result
                else:
                    return await self.primary.complete(
                        prompt, temperature=temperature, max_tokens=max_tokens, **kwargs
                    )
            except Exception as e:
                last_error = e
                delay = min(self.base_delay * (2**attempt), self.max_delay)
                await asyncio.sleep(delay)

        if self.fallback:
            try:
                return await self.fallback.complete(
                    prompt, temperature=temperature, max_tokens=max_tokens, **kwargs
                )
            except Exception as e:
                last_error = e

        raise RuntimeError(f"Inference failed after retries: {last_error}")

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings with retry."""
        last_error = None
        for attempt in range(self.max_retries):
            try:
                return await self.primary.embed(texts)
            except Exception as e:
                last_error = e
                delay = min(self.base_delay * (2**attempt), self.max_delay)
                await asyncio.sleep(delay)

        if self.fallback:
            try:
                return await self.fallback.embed(texts)
            except Exception as e:
                last_error = e

        raise RuntimeError(f"Embedding failed: {last_error}")


class ChainOfThought:
    """Chain-of-thought orchestration for complex queries."""

    def __init__(self, engine: InferenceEngine):
        self.engine = engine

    async def decompose(self, query: str) -> list[str]:
        """Decompose a complex query into sub-questions."""
        prompt = (
            "Break down this complex query into 3-5 simpler sub-questions "
            "that can be answered independently:\n\n"
            f"Query: {query}\n\n"
            "Return only the sub-questions, one per line."
        )
        response = await self.engine.complete(prompt, temperature=0.2)
        return [line.strip() for line in response.split("\n") if line.strip()]

    async def solve(self, query: str, context: dict[str, Any] | None = None) -> str:
        """Solve a complex query using CoT."""
        sub_questions = await self.decompose(query)
        answers = []

        for sq in sub_questions:
            prompt = f"""Answer this sub-question based on available context:

Sub-question: {sq}
Context: {context or "No additional context"}

Provide a concise answer:"""
            answer = await self.engine.complete(prompt, temperature=0.2)
            answers.append(f"Q: {sq}\nA: {answer}")

        sub_answers_text = "\n".join(answers)
        leading = "Synthesize a final answer using these sub-answers:\n\n"
        synthesis_prompt = f"""{leading}Original query: {query}
Sub-answers:
{sub_answers_text}

Final answer:"""
        return await self.engine.complete(synthesis_prompt, temperature=0.3)


class ToolRouter:
    """Routes queries to appropriate tools."""

    def __init__(self, engine: InferenceEngine, tools: dict[str, Any]):
        self.engine = engine
        self.tools = tools

    async def select_tool(self, query: str) -> str | None:
        """Select the most appropriate tool for a query."""
        tool_descriptions = "\n".join(
            f"- {name}: {tool.description}" for name, tool in self.tools.items()
        )
        prompt = f"""Given this query, select the most appropriate tool:

Query: {query}

Available tools:
{tool_descriptions}

Return only the tool name, or 'none' if no tool is needed."""
        response = await self.engine.complete(prompt, temperature=0.1)
        tool_name = response.strip().lower()
        return tool_name if tool_name in self.tools else None

    async def execute(self, query: str) -> Any:
        """Execute the appropriate tool."""
        tool_name = await self.select_tool(query)
        if tool_name and tool_name in self.tools:
            return await self.tools[tool_name].execute(query)
        return None
