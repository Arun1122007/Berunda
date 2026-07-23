from __future__ import annotations

from src.pipelines.base import Pipeline, PipelineStep, create_ingestion_pipeline
from src.pipelines.evaluation import PipelineEvaluator
from src.pipelines.inference import InferencePipeline
from src.pipelines.ingestion import (
    CSVIngestionSource,
    IngestionConfig,
    IngestionPipeline,
    ValidationSchema,
)
from src.pipelines.preprocessing import PreprocessingPipeline, PreprocessorConfig
from src.pipelines.training import TrainingPipeline, TrainingPipelineConfig


class TestPipeline:
    def test_pipeline_creation(self):
        p = Pipeline("test")
        assert p.name == "test"
        assert len(p.steps) == 0

    def test_add_step(self):
        p = Pipeline("test")

        async def dummy(state):
            return {"result": "ok"}

        p.add_step(PipelineStep(name="step1", func=dummy))
        assert len(p.steps) == 1

    def test_add_steps(self):
        p = Pipeline("test")

        async def a(state):
            return {"a": 1}

        async def b(state):
            return {"b": 2}

        p.add_steps(
            PipelineStep(name="step_a", func=a),
            PipelineStep(name="step_b", func=b, depends_on=["step_a"]),
        )
        assert len(p.steps) == 2

    def test_pipeline_run(self):
        p = Pipeline("test")

        async def step1(state):
            return {"greeting": "hello"}

        async def step2(state):
            prev = state.get("s1", {}).get("greeting", "")
            return {"message": f"{prev} world"}

        p.add_steps(
            PipelineStep(name="s1", func=step1),
            PipelineStep(name="s2", func=step2, depends_on=["s1"]),
        )

        import asyncio

        result = asyncio.run(p.run())
        assert result["success"]
        assert result["step_results"]["s1"]["greeting"] == "hello"
        assert result["step_results"]["s2"]["message"] == "hello world"

    def test_pipeline_run_failure_stop(self):
        p = Pipeline("fail_test", on_error="stop")

        async def failing(state):
            raise ValueError("Something went wrong")

        p.add_step(PipelineStep(name="fail", func=failing))

        import asyncio

        result = asyncio.run(p.run())
        assert not result["success"]
        assert "fail" in result["errors"]

    def test_create_ingestion_pipeline(self):
        pipe = create_ingestion_pipeline("csv")
        assert pipe.name == "csv_ingestion"
        assert len(pipe.steps) == 3


class TestIngestion:
    def test_csv_source(self):
        source = CSVIngestionSource()
        import asyncio

        data = asyncio.run(source.read("name,age\nAlice,30\nBob,25\n"))
        assert len(data) == 2
        assert data[0]["name"] == "Alice"

    def test_csv_validate(self):
        source = CSVIngestionSource()
        import asyncio

        data = asyncio.run(source.read("name,age\nAlice,30\n"))
        result = asyncio.run(source.validate(data, expected_columns=["name", "age"]))
        assert result["valid"]

    def test_csv_validate_missing_columns(self):
        source = CSVIngestionSource()
        import asyncio

        data = asyncio.run(source.read("name\nAlice\n"))
        result = asyncio.run(source.validate(data, expected_columns=["name", "age"]))
        assert not result["valid"]

    def test_ingestion_pipeline_csv(self):
        pipe = IngestionPipeline(IngestionConfig(source_type="csv"))
        import asyncio

        result = asyncio.run(pipe.run("col1,col2\n1,2\n3,4"))
        assert result["ingested"] == 2

    def test_validation_schema(self):
        schema = ValidationSchema({"id": "int", "name": "str"})
        errors = schema.validate_row({"id": "abc", "name": "test"})
        assert len(errors) == 1
        assert "int" in errors[0]

    def test_validation_schema_valid(self):
        schema = ValidationSchema({"id": "int"})
        errors = schema.validate_row({"id": "123", "name": "test"})
        assert len(errors) == 0

    def test_ingestion_config_defaults(self):
        cfg = IngestionConfig()
        assert cfg.source_type == "csv"
        assert cfg.batch_size == 100


class TestPreprocessing:
    def test_preprocessor_config_defaults(self):
        cfg = PreprocessorConfig()
        assert cfg.fill_strategy == "mean"

    def test_preprocessing_pipeline(self):
        import pandas as pd

        cfg = PreprocessorConfig(
            date_columns=["date"],
            fill_strategy="zero",
        )
        pipe = PreprocessingPipeline(cfg)
        df = pd.DataFrame(
            {
                "date": ["2024-01-15", "invalid-date"],
                "value": [1.0, None],
            }
        )
        result = pipe.run(df)
        assert "value" in result.columns

    def test_text_cleaning(self):
        import pandas as pd

        cfg = PreprocessorConfig(text_columns=["text"])
        pipe = PreprocessingPipeline(cfg)
        df = pd.DataFrame({"text": ["<p>Hello</p> http://test.com world"]})
        result = pipe.run(df)
        cleaned = result.iloc[0, 0]
        assert "p>" not in cleaned
        assert "http" not in cleaned


class TestTraining:
    def test_training_pipeline_config(self):
        cfg = TrainingPipelineConfig()
        assert cfg.model_type == "linear"

    def test_training_pipeline_creation(self):
        pipe = TrainingPipeline()
        assert pipe.trainer is not None


class TestInference:
    def test_inference_pipeline_creation(self):
        pipe = InferencePipeline()
        assert pipe.registry is not None


class TestPipelineEvaluation:
    def test_pipeline_evaluator_creation(self):
        ev = PipelineEvaluator()
        assert ev.evaluator is not None

    def test_pipeline_evaluate(self):
        import numpy as np

        ev = PipelineEvaluator()
        import asyncio

        result = asyncio.run(
            ev.evaluate(
                np.array([0, 1, 0, 1]),
                np.array([0, 1, 0, 1]),
                "test_pipeline",
            )
        )
        assert result["metrics"]["accuracy"] == 1.0
        assert result["pipeline"] == "test_pipeline"
