"""Prompt management for Berunda AI agents.

Provides versioned, template-based prompt loading with variable interpolation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.shared.logging import get_logger

logger = get_logger(__name__)

PROMPT_ROOT = Path(__file__).resolve().parent


class PromptManager:
    """Manages versioned prompt templates."""

    def __init__(self, root: Path | None = None):
        self.root = root or PROMPT_ROOT
        self._cache: dict[str, str] = {}

    def _resolve_path(self, name: str, category: str, version: str | None = None) -> Path:
        category_dir = self.root / category
        if not category_dir.exists():
            raise FileNotFoundError(f"Prompt category '{category}' not found")

        if version:
            version_dir = category_dir / "versions" / version
            if not version_dir.exists():
                raise FileNotFoundError(f"Version '{version}' not found for {category}.{name}")
            return version_dir / f"{name}.txt"

        # Find latest version
        versions_dir = category_dir / "versions"
        if not versions_dir.exists():
            raise FileNotFoundError(f"No versions directory for {category}.{name}")

        versions = sorted([d.name for d in versions_dir.iterdir() if d.is_dir()], reverse=True)
        if not versions:
            raise FileNotFoundError(f"No versions found for {category}.{name}")

        latest = versions[0]
        return versions_dir / latest / f"{name}.txt"

    def load(
        self, name: str, category: str = "system", version: str | None = None, **variables: Any
    ) -> str:
        """Load and render a prompt template."""
        path = self._resolve_path(name, category, version)
        cache_key = f"{category}/{name}/{version or 'latest'}"

        if cache_key not in self._cache:
            self._cache[cache_key] = path.read_text(encoding="utf-8")

        template = self._cache[cache_key]
        try:
            return template.format(**variables)
        except KeyError as e:
            raise ValueError(f"Missing template variable: {e}") from e

    def list_prompts(self, category: str | None = None) -> dict[str, list[str]]:
        """List all available prompts."""
        result: dict[str, list[str]] = {}
        categories = [category] if category else ["system", "tasks", "evaluation"]

        for cat in categories:
            cat_dir = self.root / cat / "versions"
            if not cat_dir.exists():
                result[cat] = []
                continue

            prompts: list[str] = []
            for version_dir in cat_dir.iterdir():
                if version_dir.is_dir():
                    for prompt_file in version_dir.glob("*.txt"):
                        prompts.append(prompt_file.stem)
            result[cat] = sorted(set(prompts))

        return result

    def get_metadata(self, name: str, category: str = "system", version: str | None = None) -> dict:
        """Get prompt metadata."""
        path = self._resolve_path(name, category, version)
        meta_path = path.with_suffix(".json")
        if meta_path.exists():
            return json.loads(meta_path.read_text(encoding="utf-8"))
        return {"name": name, "category": category, "version": version or "latest"}


# Global instance
prompt_manager = PromptManager()


def load_prompt(
    name: str, category: str = "system", version: str | None = None, **variables: Any
) -> str:
    """Convenience function to load a prompt."""
    return prompt_manager.load(name, category, version, **variables)


def list_prompts(category: str | None = None) -> dict[str, list[str]]:
    """Convenience function to list prompts."""
    return prompt_manager.list_prompts(category)


def get_prompt_metadata(name: str, category: str = "system", version: str | None = None) -> dict:
    """Convenience function to get prompt metadata."""
    return prompt_manager.get_metadata(name, category, version)
