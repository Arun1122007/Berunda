"""
Prompt manager — load, list, and manage versioned prompt templates.

The prompt system provides a central registry of prompt templates organized
by category (system, task, evaluation) and version. Templates are stored
as files in the prompts directory tree and loaded on demand.

Exports:
    PromptManager: Class for loading, caching, and versioning prompts.
    load_prompt: Convenience function to load a single prompt by name.
    list_prompts: Return available prompt names grouped by category.
"""

from berunda.ai.prompts.manager import PromptManager


_manager: PromptManager | None = None


def _get_manager() -> PromptManager:
    global _manager
    if _manager is None:
        _manager = PromptManager()
    return _manager


def load_prompt(name: str, version: str | None = None, **kwargs: str) -> str:
    """Load and render a prompt template by name.

    Args:
        name: Dot-separated prompt name (e.g. ``system.investigator``).
        version: Optional version string; uses latest if omitted.
        **kwargs: Template variables to interpolate into the prompt.

    Returns:
        The rendered prompt string.
    """
    return _get_manager().load(name, version=version, **kwargs)


def list_prompts(category: str | None = None) -> dict[str, list[str]]:
    """List available prompts, optionally filtered by category.

    Args:
        category: One of ``system``, ``task``, ``evaluation``, or ``None`` for all.

    Returns:
        Dictionary mapping category names to lists of prompt names.
    """
    return _get_manager().list_prompts(category=category)


__all__ = [
    "PromptManager",
    "load_prompt",
    "list_prompts",
]
