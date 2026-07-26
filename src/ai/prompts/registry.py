from typing import Dict, Any, Optional

class PromptRegistry:
    _prompts: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def register(cls, prompt_id: str, version: str, template: str, metadata: Optional[Dict] = None):
        if prompt_id not in cls._prompts:
            cls._prompts[prompt_id] = {}
        
        cls._prompts[prompt_id][version] = {
            "template": template,
            "metadata": metadata or {}
        }

    @classmethod
    def get(cls, prompt_id: str, version: str) -> str:
        if prompt_id not in cls._prompts or version not in cls._prompts[prompt_id]:
            raise ValueError(f"Prompt {prompt_id} version {version} not found.")
        return cls._prompts[prompt_id][version]["template"]

# Pre-register Phase 8 prompts
PromptRegistry.register("fir-extraction", "v1", "Extract structured information from this FIR: {text}")
PromptRegistry.register("fir-summarization", "v1", "Summarize this FIR in 3 sentences, citing sources: {text}")
PromptRegistry.register("crime-category", "v1", "Suggest crime category from the taxonomy for this FIR: {text}")
PromptRegistry.register("investigation-assistant", "v1", "Answer the question using ONLY the provided context. If unknown, say insufficient information. Context: {context} Question: {question}")
