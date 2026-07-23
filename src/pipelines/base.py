from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PipelineStep:
    """A single step in a pipeline."""

    name: str
    func: Callable
    depends_on: list[str] = field(default_factory=list)
    retries: int = 0


class Pipeline:
    """Sequential DAG pipeline execution engine."""

    def __init__(self, name: str, on_error: str = "stop"):
        self.name = name
        self.steps: list[PipelineStep] = []
        self.on_error = on_error  # stop, skip, retry

    def add_step(self, step: PipelineStep) -> Pipeline:
        self.steps.append(step)
        return self

    def add_steps(self, *steps: PipelineStep) -> Pipeline:
        self.steps.extend(steps)
        return self

    async def run(self, initial_state: dict | None = None) -> dict[str, Any]:
        """Run the pipeline, passing state between steps."""
        import asyncio

        state: dict = initial_state or {}
        results: dict[str, Any] = {}
        errors: dict[str, str] = {}
        start_time = time.time()

        for step in self.steps:
            deps_ok = all(dep in results for dep in step.depends_on)
            if not deps_ok:
                errors[step.name] = "Dependencies not met"
                if self.on_error == "stop":
                    break
                continue

            for attempt in range(step.retries + 1):
                try:
                    if asyncio.iscoroutinefunction(step.func):
                        result = await step.func({**state, **results})
                    else:
                        result = step.func({**state, **results})
                    results[step.name] = result
                    break
                except Exception as e:
                    if attempt < step.retries:
                        continue
                    errors[step.name] = str(e)
                    if self.on_error == "stop":
                        break

            if step.name in errors and self.on_error == "stop":
                break

        elapsed = time.time() - start_time
        return {
            "pipeline": self.name,
            "elapsed_seconds": elapsed,
            "state": state,
            "step_results": results,
            "errors": errors,
            "success": len(errors) == 0,
        }


def create_ingestion_pipeline(source_type: str = "csv") -> Pipeline:
    """Create a standard data ingestion pipeline."""
    from src.pipelines.ingestion import ingest_data, store_data, validate_data

    return Pipeline(name=f"{source_type}_ingestion", on_error="stop").add_steps(
        PipelineStep(name="load", func=ingest_data),
        PipelineStep(name="validate", func=validate_data, depends_on=["load"]),
        PipelineStep(name="store", func=store_data, depends_on=["validate"]),
    )
