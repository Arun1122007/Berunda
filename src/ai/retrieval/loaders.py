from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseLoader(ABC):
    """Abstract base class for document loaders."""

    @abstractmethod
    def load(self, source: str) -> list[dict[str, Any]]:
        """Load documents from source. Returns list of {text, metadata}."""
        pass


class TextFileLoader(BaseLoader):
    """Load plain text files."""

    def load(self, source: str) -> list[dict[str, Any]]:
        with open(source, encoding="utf-8") as f:
            text = f.read()
        return [{"text": text, "metadata": {"source": source}}]


class CSVLoader(BaseLoader):
    """Load CSV files as documents."""

    def load(self, source: str) -> list[dict[str, Any]]:
        import csv

        results = []
        with open(source, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                text = " ".join(f"{k}: {v}" for k, v in row.items())
                results.append({"text": text, "metadata": dict(row)})
        return results


class JSONLoader(BaseLoader):
    """Load JSON files as documents."""

    def load(self, source: str) -> list[dict[str, Any]]:
        import json

        with open(source, encoding="utf-8") as f:
            data = json.load(f)
        results = []
        if isinstance(data, list):
            for i, item in enumerate(data):
                text = json.dumps(item, ensure_ascii=False)
                results.append({"text": text, "metadata": {"index": i, "source": source}})
        else:
            text = json.dumps(data, ensure_ascii=False)
            results.append({"text": text, "metadata": {"source": source}})
        return results


def create_loader(loader_type: str) -> BaseLoader:
    """Factory for loaders."""
    loaders = {
        "text": TextFileLoader,
        "csv": CSVLoader,
        "json": JSONLoader,
    }
    if loader_type not in loaders:
        raise ValueError(f"Unknown loader type: {loader_type}")
    return loaders[loader_type]()  # type: ignore[abstract]
