"""Agent orchestration — multi-agent coordination, task planning, workflow execution, routing."""

from __future__ import annotations

import json
import time
from typing import Any

from src.ai.guardrails import GuardrailManager
from src.ai.memory import BaseMemory, InMemoryMemory, Message
from src.ai.tools import BaseTool


class Orchestrator:
    """Coordinates LLM calls, tools, memory, and guardrails."""

    def __init__(
        self,
        provider: Any,
        memory: BaseMemory | None = None,
        guardrails: GuardrailManager | None = None,
        tools: dict[str, BaseTool] | None = None,
        max_tool_rounds: int = 5,
    ):
        self.provider = provider
        self.memory = memory or InMemoryMemory()
        self.guardrails = guardrails or GuardrailManager()
        self.tools = tools or {}
        self.max_tool_rounds = max_tool_rounds

    async def process(
        self,
        user_input: str,
        system_prompt: str | None = None,
        enable_guardrails: bool = True,
    ) -> dict[str, Any]:
        """Process user input through the full AI pipeline."""
        start_time = time.time()
        tool_calls_made = []
        rounds = 0

        if enable_guardrails:
            check = await self.guardrails.check_input(user_input)
            if not check.passed:
                return {
                    "content": f"Input blocked: {check.reason}",
                    "tool_calls": [],
                    "processing_time_ms": int((time.time() - start_time) * 1000),
                    "blocked": True,
                }

        self.memory.add(Message(role="user", content=user_input))

        history = self.memory.get_history()
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        current_prompt = user_input

        while rounds < self.max_tool_rounds:
            from src.ai.schemas import Message as Msg

            response_obj = await self.provider.complete([Msg(role="user", content=current_prompt)])
            response = response_obj.content
            rounds += 1

            tool_call = self._extract_tool_call(response)
            if not tool_call:
                break

            tool_name, tool_args = tool_call
            if tool_name in self.tools:
                tool_result = await self.tools[tool_name].execute(**tool_args)
                tool_calls_made.append(
                    {
                        "tool": tool_name,
                        "args": tool_args,
                        "result": str(tool_result)[:500],
                    }
                )
                current_prompt = f"Tool '{tool_name}' returned: {json.dumps(tool_result)[:1000]}\n\nProceed with the answer."
            else:
                break

        final_response = current_prompt if rounds == 1 else response

        if enable_guardrails:
            out_check = self.guardrails.check_output(final_response)
            if not out_check.passed and out_check.severity == "block":
                final_response = f"Response blocked: {out_check.reason}"

        self.memory.add(Message(role="assistant", content=final_response))

        return {
            "content": final_response,
            "tool_calls": tool_calls_made,
            "processing_time_ms": int((time.time() - start_time) * 1000),
            "blocked": False,
        }

    def _extract_tool_call(self, text: str) -> tuple[str, dict] | None:
        import re

        pattern = r'\{[^}]*"tool"[^}]*\}'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
                return data.get("tool"), data.get("args", {})
            except (json.JSONDecodeError, KeyError):
                pass
        return None
