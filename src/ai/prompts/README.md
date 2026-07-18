# Prompt Management (`src/ai/prompts/`)

> **Module:** AI Prompts
> **Classification:** INTERNAL

---

## Overview

The prompt management system provides versioned, modular prompt templates for
all AI interactions. Prompts are stored on disk as text files with Jinja2-style
template variables and are loaded on demand by the `PromptManager`.

---

## Directory Structure

```
prompts/
├── system/          — System-level prompts (agent persona, constraints)
│   ├── investigator_v1.txt
│   ├── analyst_v2.txt
│   └── admin_v1.txt
├── tasks/           — Task-specific prompts (per operation)
│   ├── search_cases_v1.txt
│   ├── entity_analysis_v2.txt
│   └── link_analysis_v1.txt
├── evaluation/      — Evaluation/grading prompts
│   ├── faithfulness_v1.txt
│   ├── relevance_v1.txt
│   └── hallucination_v2.txt
└── versions/        — Version registry (JSON metadata about each version)
    ├── system_versions.json
    ├── task_versions.json
    └── evaluation_versions.json
```

---

## Versioning

Each prompt file is versioned by suffix (e.g., `_v1`, `_v2`). The version
registry in `versions/` tracks:

- Available versions per prompt
- Active (default) version
- Changelog per version
- Deprecation status

```json
{
  "investigator": {
    "versions": ["1", "2"],
    "active": "2",
    "changelog": {
      "2": "Added structured output format instructions"
    }
  }
}
```

---

## Template Variables

Prompts use `{variable}` syntax for interpolation:

```text
You are a crime investigation assistant.
Analyze the following FIR data and provide insights.

Context:
{context}

Question: {question}
```

Variables are passed as keyword arguments to `load_prompt()`:

```python
prompt = load_prompt(
    "system.investigator",
    version="2",
    context=retrieved_chunks,
    question=user_query,
)
```

---

## Usage

```python
from berunda.ai.prompts import load_prompt, list_prompts

# List all available prompts
available = list_prompts()
print(available["system"])  # ['investigator', 'analyst', 'admin']

# Load latest version of a system prompt
system_prompt = load_prompt("system.investigator")

# Load a specific version
task_prompt = load_prompt("tasks.search_cases", version="1")

# Load with template variables
rendered = load_prompt(
    "tasks.entity_analysis",
    entity_name="John Doe",
    case_count="15",
)
```

---

## Best Practices

1. **Keep system prompts stable** — Changes to system prompts affect all
   downstream behavior. Test thoroughly before promoting a new version.
2. **Version aggressively** — Create a new version for every meaningful change.
   Old versions remain available for rollback.
3. **Use descriptive names** — Prompt names should clearly indicate their purpose.
4. **Template validation** — The `PromptManager` raises `KeyError` if required
   template variables are missing.
