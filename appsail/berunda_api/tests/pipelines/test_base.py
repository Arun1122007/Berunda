"""Tests for pipelines.base module."""

from __future__ import annotations

import pytest

from src.pipelines.base import BasePipeline, Pipeline, PipelineStep, create_ingestion_pipeline


class TestBasePipeline:
    def test_abstract_cannot_instantiate(self):
        with pytest.raises(TypeError):
            BasePipeline()  # type: ignore


class TestPipelineStep:
    def test_create_step(self):
        def f(state):
            return state
        step = PipelineStep(name="test", func=f)
        assert step.name == "test"

    def test_step_with_dependencies(self):
        def f(state):
            return state
        step = PipelineStep(name="b", func=f, depends_on=["a"])
        assert "a" in step.depends_on


class TestPipeline:
    def test_add_step(self):
        pipeline = Pipeline("test")
        pipeline.add_step(PipelineStep(name="s1", func=lambda s: s))
        assert len(pipeline.steps) == 1

    def test_add_multiple_steps(self):
        pipeline = Pipeline("test")
        pipeline.add_steps(
            PipelineStep(name="a", func=lambda s: s),
            PipelineStep(name="b", func=lambda s: s),
        )
        assert len(pipeline.steps) == 2

    def test_validate_valid(self):
        pipeline = Pipeline("test").add_step(PipelineStep(name="s1", func=lambda s: s))
        result = pipeline.validate()
        assert result["valid"] is True

    def test_validate_missing_deps(self):
        pipeline = Pipeline("test").add_step(
            PipelineStep(name="s2", func=lambda s: s, depends_on=["s1"])
        )
        result = pipeline.validate()
        assert result["valid"] is False

    def test_run_empty(self):
        pipeline = Pipeline("empty")
        import asyncio
        result = asyncio.run(pipeline.run())
        assert result["success"] is True
        assert result["pipeline"] == "empty"

    def test_run_with_steps(self):
        pipeline = Pipeline("test").add_step(
            PipelineStep(name="add_one", func=lambda s: {"value": s.get("value", 0) + 1})
        )
        import asyncio
        result = asyncio.run(pipeline.run({"value": 5}))
        assert result["success"] is True
        assert result["step_results"]["add_one"]["value"] == 6

    def test_status_tracking(self):
        pipeline = Pipeline("status_test")
        assert pipeline.get_status()["state"] == "idle"
        import asyncio
        asyncio.run(pipeline.run())
        assert pipeline.get_status()["state"] == "completed"

    def test_error_stops_pipeline(self):
        pipeline = Pipeline("error_test", on_error="stop").add_steps(
            PipelineStep(name="ok", func=lambda s: {"ok": True}),
            PipelineStep(name="fail", func=lambda s: 1 / 0),
            PipelineStep(name="never_reached", func=lambda s: {"done": True}),
        )
        import asyncio
        result = asyncio.run(pipeline.run())
        assert result["success"] is False
        assert "fail" in result["errors"]
        assert "never_reached" not in result["step_results"]


class TestCreateIngestionPipeline:
    def test_creates_pipeline(self):
        pipeline = create_ingestion_pipeline("csv")
        assert pipeline.name == "csv_ingestion"
        assert len(pipeline.steps) == 3
