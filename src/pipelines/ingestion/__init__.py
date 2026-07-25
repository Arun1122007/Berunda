"""Pipeline ingestion utilities."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from io import StringIO
from typing import Any


@dataclass
class IngestionConfig:
    """Configuration for data ingestion."""

    source_type: str = "csv"  # csv, json, api
    batch_size: int = 100
    encoding: str = "utf-8"
    validate_schema: bool = True
    expected_columns: list[str] | None = None


class CSVIngestionSource:
    """Read data from CSV strings or files."""

    async def read(self, content: str | list[str]) -> list[dict]:
        if isinstance(content, list):
            content = "\n".join(content)
        reader = csv.DictReader(StringIO(content))
        return [row for row in reader]

    async def validate(self, data: list[dict], expected_columns: list[str] | None = None) -> dict:
        if not data:
            return {"valid": True, "count": 0, "errors": []}

        errors = []
        if expected_columns:
            actual_columns = set(data[0].keys())
            missing = set(expected_columns) - actual_columns
            if missing:
                errors.append(f"Missing columns: {missing}")

        return {
            "valid": len(errors) == 0,
            "count": len(data),
            "errors": errors,
        }


class APIIngestionSource:
    """Read data from external API endpoints."""

    def __init__(self, base_url: str, api_key: str | None = None):
        self.base_url = base_url
        self.api_key = api_key

    async def fetch(self, endpoint: str, params: dict | None = None) -> list[dict]:
        import httpx

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                # Try common pagination patterns
                for key in ("results", "data", "items", "records"):
                    if key in data and isinstance(data[key], list):
                        return data[key]
            return [data]


class ValidationSchema:
    """Schema validation for ingested data."""

    def __init__(self, schema: dict[str, str]):
        self.schema = schema  # {column_name: type_name}

    def validate_row(self, row: dict) -> list[str]:
        errors = []
        for col, expected_type in self.schema.items():
            value = row.get(col)
            if value is None or value == "":
                errors.append(f"Missing required field: {col}")
                continue
            if expected_type == "int":
                try:
                    int(value)
                except (ValueError, TypeError):
                    errors.append(f"Column '{col}' expected int, got '{value}'")
            elif expected_type == "float":
                try:
                    float(value)
                except (ValueError, TypeError):
                    errors.append(f"Column '{col}' expected float, got '{value}'")
            elif expected_type == "date":
                from datetime import datetime

                try:
                    datetime.fromisoformat(str(value))
                except (ValueError, TypeError):
                    errors.append(f"Column '{col}' expected date, got '{value}'")
        return errors


class IngestionPipeline:
    """End-to-end ingestion pipeline."""

    def __init__(self, config: IngestionConfig | None = None):
        self.config = config or IngestionConfig()

    async def run(self, source_data: Any) -> dict:
        results: dict[str, Any] = {"ingested": 0, "errors": [], "batches": []}

        if self.config.source_type == "csv":
            reader = CSVIngestionSource()
            data = await reader.read(source_data)
            validation = await reader.validate(data, self.config.expected_columns)
        else:
            raise ValueError(f"Unsupported source type: {self.config.source_type}")

        if not validation["valid"]:
            return {**results, "errors": validation["errors"]}

        # Batch processing
        for i in range(0, len(data), self.config.batch_size):
            batch = data[i : i + self.config.batch_size]
            results["batches"].append(
                {
                    "batch_index": i // self.config.batch_size,
                    "size": len(batch),
                }
            )
            results["ingested"] += len(batch)

        return results


# Convenience functions matching Pipeline interface
async def ingest_data(state: dict) -> dict:
    config = IngestionConfig(**state.get("ingestion_config", {}))
    pipeline = IngestionPipeline(config)
    data = state.get("source_data", "")
    return {"ingestion_result": await pipeline.run(data)}


async def validate_data(state: dict) -> dict:
    ingestion_result = state.get("ingestion_result", {})
    return {"validation_result": {"valid": len(ingestion_result.get("errors", [])) == 0}}


async def store_data(state: dict) -> dict:
    return {
        "storage_result": {
            "stored": True,
            "records": state.get("ingestion_result", {}).get("ingested", 0),
        }
    }
