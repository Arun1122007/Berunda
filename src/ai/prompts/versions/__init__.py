"""
Prompt versioning registry — metadata about prompt template versions.

This package contains JSON registry files (``*.json``) that track:
- Available versions per prompt template
- Active/default version designation
- Version changelogs and migration notes
- Deprecation status

Registries are loaded by ``PromptManager`` and not imported directly.
"""
