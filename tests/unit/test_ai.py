from __future__ import annotations

import pytest
from unittest.mock import patch, MagicMock

from src.ai.agent import AnalystAgent, InvestigatorAgent, ReviewerAgent, create_agent
from src.ai.evaluation import (
    Evaluator,
    FaithfulnessEvaluator,
    HallucinationEvaluator,
    RelevanceEvaluator,
)
from src.ai.guardrails import GuardrailManager, InputGuardrail, OutputGuardrail
from src.ai.inference import ChainOfThought, InferenceEngine, ToolRouter
from src.ai.memory import InMemoryMemory, Message, TokenWindowMemory, create_memory
from src.ai.observability import TelemetryEvent, TelemetryStore
from src.ai.orchestration import Orchestrator
from src.ai.providers import (
    CatalystProvider,
    MockProvider,
    ProviderRegistry,
    create_provider,
)
from src.ai.schemas import AgentConfig, ToolCall, ToolResult
from src.ai.tools import BaseTool, SearchCasesTool, get_all_tools, get_tool, register_tool


class TestProviders:
    def test_create_mock(self):
        p = create_provider("mock", model="test")
        assert p.provider_name == "mock"
        assert p.model == "test"

    def test_create_catalyst(self):
        p = create_provider("catalyst", model="test")
        assert p.provider_name == "catalyst"

    def test_create_openai(self):
        p = create_provider("openai", model="gpt-4")
        assert p.provider_name == "openai"

    def test_provider_registry(self):
        ProviderRegistry.register("mock", MockProvider)
        p = ProviderRegistry.create("mock", model="test")
        assert isinstance(p, MockProvider)

    def test_mock_complete(self):
        from src.ai.schemas import Message

        p = MockProvider(model="test")
        import asyncio

        result = asyncio.run(p.complete([Message(role="user", content="hello")]))
        assert result.content
        assert result.provider == "mock"

    @pytest.mark.asyncio
    @patch("src.ai.providers.catalyst.CatalystProvider._post_chat")
    async def test_catalyst_complete(self, mock_post_chat):
        from src.ai.schemas import Message

        mock_post_chat.return_value = {"choices": [{"message": {"content": "mocked response"}}]}
        
        p = CatalystProvider(model="test")
        result = await p.complete([Message(role="user", content="hello")])
        
        assert result.content == "mocked response"
        assert result.provider == "catalyst"

    def test_mock_embed(self):
        p = MockProvider(model="test")
        import asyncio

        embs = asyncio.run(p.embed(["hello", "world"]))
        assert len(embs) == 2
        assert len(embs[0]) == 1536


class TestMemory:
    def test_in_memory_add_and_get(self):
        mem = InMemoryMemory(max_history=5)
        mem.add(Message(role="user", content="hello"))
        mem.add(Message(role="assistant", content="hi"))
        history = mem.get_history()
        assert len(history) == 2
        assert history[0].content == "hello"
        assert history[1].role == "assistant"

    def test_in_memory_max_history(self):
        mem = InMemoryMemory(max_history=3)
        for i in range(5):
            mem.add(Message(role="user", content=str(i)))
        assert len(mem.get_history()) == 3
        assert mem.get_history()[0].content == "2"

    def test_token_window(self):
        mem = TokenWindowMemory(max_tokens=10)
        mem.add(Message(role="user", content="a" * 50))
        assert len(mem.get_history()) == 1
        mem.add(Message(role="user", content="b" * 50))
        # Should have trimmed
        assert len(mem.get_history()) <= 2

    def test_clear(self):
        mem = InMemoryMemory()
        mem.add(Message(role="user", content="test"))
        mem.clear()
        assert len(mem.get_history()) == 0

    def test_create_memory_factory(self):
        mem = create_memory("in_memory")
        assert isinstance(mem, InMemoryMemory)
        mem2 = create_memory("token_window", max_tokens=1000)
        assert isinstance(mem2, TokenWindowMemory)


@pytest.mark.asyncio
class TestGuardrails:
    async def test_input_pii_aadhaar(self):
        g = InputGuardrail()
        result = await g.check("My aadhaar is 1234 5678 9012")
        assert not result.passed
        assert "PII" in result.reason

    async def test_input_toxic(self):
        g = InputGuardrail()
        result = await g.check("I will kill you")
        assert not result.passed

    async def test_input_clean(self):
        g = InputGuardrail()
        result = await g.check("What is the crime rate in Bangalore?")
        assert result.passed

    def test_output_sensitive_terms(self):
        g = OutputGuardrail()
        result = g.check("The accused belongs to scheduled caste community")
        assert not result.passed

    def test_output_clean(self):
        g = OutputGuardrail()
        result = g.check("The suspect was arrested on 2024-01-15")
        assert result.passed

    async def test_guardrail_manager(self):
        mgr = GuardrailManager()
        assert not (await mgr.check_input("My phone is +919876543210")).passed
        assert (await mgr.check_input("What is the weather?")).passed


class TestEvaluation:
    def test_faithfulness_good(self):
        ev = FaithfulnessEvaluator()
        result = ev.evaluate(
            "The suspect was arrested in Bangalore",
            "The suspect was arrested in Bangalore city yesterday",
        )
        assert result.passed

    def test_faithfulness_poor(self):
        ev = FaithfulnessEvaluator()
        result = ev.evaluate(
            "Aliens landed in Delhi",
            "Crime statistics for Bangalore 2024",
        )
        assert not result.passed

    def test_relevance(self):
        ev = RelevanceEvaluator()
        result = ev.evaluate("What is the crime rate?", "The crime rate in Bangalore is high")
        assert result.passed

    def test_hallucination(self):
        ev = HallucinationEvaluator()
        result = ev.evaluate(
            "The suspect was arrested. The culprit was from Mars.",
            "The suspect was arrested in Bangalore.",
        )
        assert not result.passed

    def test_evaluator_suite(self):
        ev = Evaluator()
        results = ev.evaluate_all(
            "Bangalore crime",
            "Crime in Bangalore has increased",
            "Crime statistics show increase in Bangalore",
        )
        assert len(results) == 3
        assert results["faithfulness"].passed
        assert results["relevance"].passed


class TestTools:
    def test_search_tool(self):
        tool = SearchCasesTool()
        assert tool.name == "search_cases"
        assert "Search FIR" in tool.description

    def test_get_tool(self):
        assert get_tool("search_cases") is not None
        assert get_tool("nonexistent") is None

    def test_get_all_tools(self):
        tools = get_all_tools()
        assert len(tools) >= 5

    def test_register_tool(self):
        class TestTool(BaseTool):
            name = "test_tool"
            description = "Test tool"

            async def execute(self, query, **kwargs):
                return {"result": "test"}

        register_tool(TestTool())
        assert get_tool("test_tool") is not None

    def test_base_tool_abstract(self):
        with pytest.raises(TypeError):
            BaseTool()


class TestSchemas:
    def test_agent_config_defaults(self):
        cfg = AgentConfig()
        assert cfg.max_tool_rounds == 5
        assert cfg.enable_guardrails
        assert cfg.temperature == 0.3

    def test_tool_call(self):
        tc = ToolCall(id="1", name="search", arguments={"q": "test"})
        assert tc.name == "search"

    def test_tool_result(self):
        tr = ToolResult(id="1", output={"result": "ok"})
        assert tr.output["result"] == "ok"


class TestObservability:
    def test_telemetry_store(self):
        store = TelemetryStore(max_events=100)
        store.record(TelemetryEvent(event_type="completion", provider="mock", model="test"))
        assert len(store.get_events()) == 1
        stats = store.get_stats()
        assert stats["total_requests"] == 1

    def test_telemetry_clear(self):
        store = TelemetryStore()
        store.record(TelemetryEvent(event_type="completion", provider="mock", model="test"))
        store.clear()
        assert len(store.get_events()) == 0

    def test_record_completion(self):
        store = TelemetryStore()
        store.record_completion(
            provider="mock", model="test", prompt_tokens=10, completion_tokens=20
        )
        stats = store.get_stats()
        assert stats["total_tokens"] == 30
        assert stats["total_cost"] > 0


class TestAgent:
    def test_create_investigator(self):
        agent = create_agent("investigator")
        assert isinstance(agent, InvestigatorAgent)
        assert "investigation" in agent.config.system_prompt.lower()

    def test_create_analyst(self):
        agent = create_agent("analyst")
        assert isinstance(agent, AnalystAgent)

    def test_create_reviewer(self):
        agent = create_agent("reviewer")
        assert isinstance(agent, ReviewerAgent)

    def test_agent_run_returns_blocked_on_pii(self):
        agent = create_agent("investigator")
        import asyncio

        result = asyncio.run(agent.run("My aadhaar is 1234 5678 9012"))
        assert result.get("blocked")


class TestInference:
    def test_inference_engine_creation(self):
        provider = MockProvider(model="test")
        engine = InferenceEngine(primary_provider=provider)
        assert engine.max_retries == 3

    def test_chain_of_thought(self):
        provider = MockProvider(model="test")
        engine = InferenceEngine(primary_provider=provider)
        cot = ChainOfThought(engine)
        assert cot is not None

    def test_tool_router(self):
        router = ToolRouter(None, {})
        assert router is not None


class TestOrchestration:
    def test_orchestrator_creation(self):
        provider = MockProvider(model="test")
        orch = Orchestrator(provider=provider)
        assert orch.max_tool_rounds == 5
