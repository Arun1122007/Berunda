"""Tests for pipeline subpackages."""

from __future__ import annotations

import pandas as pd
import pytest

from src.pipelines.evaluation import EvaluationPipeline, PipelineEvaluator
from src.pipelines.inference import InferencePipeline
from src.pipelines.ingestion import (
    APIIngestionSource,
    CSVIngestionSource,
    IngestionConfig,
    IngestionPipeline,
    ValidationSchema,
    ingest_data,
    store_data,
    validate_data,
)
from src.pipelines.preprocessing import PreprocessingPipeline, PreprocessorConfig, preprocess_data
from src.pipelines.training import TrainingPipeline, TrainingPipelineConfig, train_model


@pytest.fixture
def sample_csv():
    return "name,age\nAlice,30\nBob,25\n"


class TestCSVIngestionSource:
    async def test_read_csv(self):
        source = CSVIngestionSource()
        data = await source.read("a,b\n1,2\n3,4")
        assert len(data) == 2

    async def test_validate(self):
        source = CSVIngestionSource()
        data = await source.read("a,b\n1,2")
        result = await source.validate(data, expected_columns=["a", "b"])
        assert result["valid"] is True

    async def test_validate_missing_columns(self):
        source = CSVIngestionSource()
        data = await source.read("a\n1")
        result = await source.validate(data, expected_columns=["a", "b"])
        assert result["valid"] is False


class TestAPIIngestionSource:
    def test_init(self):
        source = APIIngestionSource("https://api.example.com", "key123")
        assert source.base_url == "https://api.example.com"
        assert source.api_key == "key123"


class TestValidationSchema:
    def test_validate_row_valid(self):
        schema = ValidationSchema({"age": "int", "score": "float"})
        errors = schema.validate_row({"age": "25", "score": "95.5"})
        assert len(errors) == 0

    def test_validate_row_missing(self):
        schema = ValidationSchema({"name": "str"})
        errors = schema.validate_row({})
        assert len(errors) > 0

    def test_validate_row_type_mismatch(self):
        schema = ValidationSchema({"age": "int"})
        errors = schema.validate_row({"age": "not_a_number"})
        assert len(errors) > 0


class TestIngestionPipeline:
    async def test_run_csv(self):
        pipeline = IngestionPipeline(IngestionConfig(source_type="csv"))
        result = await pipeline.run("a,b\n1,2\n3,4")
        assert result["ingested"] == 2

    async def test_run_csv_validation_fails(self):
        pipeline = IngestionPipeline(
            IngestionConfig(source_type="csv", expected_columns=["a", "b", "c"])
        )
        result = await pipeline.run("a,b\n1,2")
        assert len(result["errors"]) > 0

    async def test_validate_method(self):
        pipeline = IngestionPipeline()
        result = pipeline.validate()
        assert result["valid"] is True

    async def test_get_status(self):
        pipeline = IngestionPipeline()
        assert pipeline.get_status()["state"] == "idle"

    async def test_unsupported_source(self):
        pipeline = IngestionPipeline(IngestionConfig(source_type="json"))
        with pytest.raises(ValueError):
            await pipeline.run("{}")


class TestIngestionConvenience:
    async def test_ingest_data(self):
        result = await ingest_data({"source_data": "a,b\n1,2", "ingestion_config": {}})
        assert "ingestion_result" in result

    async def test_validate_data(self):
        result = await validate_data({"ingestion_result": {"errors": []}})
        assert result["validation_result"]["valid"] is True

    async def test_store_data(self):
        result = await store_data({"ingestion_result": {"ingested": 5}})
        assert result["storage_result"]["stored"] is True


class TestPreprocessingPipeline:
    async def test_run_with_dataframe(self):
        pipeline = PreprocessingPipeline()
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        result = await pipeline.run(data=df)
        assert "preprocessed_data" in result

    async def test_run_with_dict(self):
        pipeline = PreprocessingPipeline()
        result = await pipeline.run(data={"x": [1, 2], "y": [3, 4]})
        assert "preprocessed_data" in result

    async def test_with_config(self):
        config = PreprocessorConfig(
            date_columns=["dt"],
            categorical_columns=["cat"],
            fill_strategy="zero",
        )
        pipeline = PreprocessingPipeline(config)
        df = pd.DataFrame({"dt": ["2024-01-01"], "cat": ["A"], "num": [None]})
        result = await pipeline.run(data=df)
        assert result["preprocessed_data"]["num"].iloc[0] == 0

    async def test_preprocess_data_convenience(self):
        state = {
            "data": {"a": [1, 2]},
            "preprocessor_config": {"fill_strategy": "mean"},
        }
        result = await preprocess_data(state)
        assert "preprocessed_data" in result


class TestTrainingPipeline:
    async def test_run(self):
        df = pd.DataFrame({
            "CrimeMajorHeadID": [0, 1, 0, 1, 0, 1],
            "IncidentFromDate": pd.date_range("2024-01-01", periods=6),
            "BriefFacts": ["theft"] * 6,
        })
        config = TrainingPipelineConfig(model_type="random_forest")
        pipeline = TrainingPipeline(config)
        result = await pipeline.run(df)
        assert "training_metrics" in result
        assert "evaluation" in result

    async def test_validate(self):
        pipeline = TrainingPipeline()
        result = pipeline.validate()
        assert result["valid"] is True

    async def test_train_model_convenience(self):
        import numpy as np
        x = np.random.rand(20, 3)
        y = np.random.randint(0, 2, 20)
        state = {"X": x.tolist(), "y": y.tolist(), "training_config": {}}
        result = await train_model(state)
        assert "training_result" in result or "error" in result


class TestInferencePipeline:
    async def test_validate_missing_model(self):
        pipeline = InferencePipeline()
        result = pipeline.validate(model_name="nonexistent")
        assert result["valid"] is False

    async def test_validate_ok(self):
        pipeline = InferencePipeline()
        result = pipeline.validate()
        assert result["valid"] is True

    async def test_get_status(self):
        pipeline = InferencePipeline()
        assert pipeline.get_status()["state"] == "idle"


class TestEvaluationPipeline:
    async def test_run_classification(self):
        import numpy as np
        pipeline = EvaluationPipeline()
        result = await pipeline.run(
            y_true=np.array([0, 1, 0, 1]),
            y_pred=np.array([0, 1, 0, 1]),
            y_prob=np.array([[0.9, 0.1], [0.2, 0.8], [0.8, 0.2], [0.3, 0.7]]),
            task="classification",
        )
        assert "accuracy" in result
        assert result["accuracy"] == 1.0

    async def test_run_regression(self):
        import numpy as np
        pipeline = EvaluationPipeline()
        result = await pipeline.run(
            y_true=np.array([1.0, 2.0, 3.0]),
            y_pred=np.array([1.0, 2.0, 3.0]),
            task="regression",
        )
        assert result["r2"] == 1.0
