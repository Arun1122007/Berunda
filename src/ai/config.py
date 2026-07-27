import os


class AIConfig:
    AI_ENABLED = os.getenv("AI_ENABLED", "true").lower() == "true"
    PROVIDER = os.getenv("LLM_PROVIDER", "mock")
    MODEL = os.getenv("LLM_MODEL", "mock-model-v1")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "mock-embed-v1")

    EXTRACTION_TIMEOUT_SEC = int(os.getenv("AI_EXTRACTION_TIMEOUT_SEC", "30"))
    SUMMARIZATION_TIMEOUT_SEC = int(os.getenv("AI_SUMMARIZATION_TIMEOUT_SEC", "30"))
    SEARCH_TIMEOUT_SEC = int(os.getenv("AI_SEARCH_TIMEOUT_SEC", "15"))
    MAX_RETRIES = int(os.getenv("AI_MAX_RETRIES", "3"))
    MAX_FIR_INPUT_LENGTH = int(os.getenv("AI_MAX_FIR_INPUT_LENGTH", "16000"))
    MAX_RETRIEVAL_RESULTS = int(os.getenv("AI_MAX_RETRIEVAL_RESULTS", "5"))

    EVALUATION_MODE = os.getenv("AI_EVALUATION_MODE", "false").lower() == "true"
    REDACTION_MODE = os.getenv("AI_REDACTION_MODE", "strict")

    # Feature Flags
    FEATURE_FIR_EXTRACTION = os.getenv("AI_FEATURE_FIR_EXTRACTION", "true").lower() == "true"
    FEATURE_SUMMARIZATION = os.getenv("AI_FEATURE_SUMMARIZATION", "true").lower() == "true"
    FEATURE_CRIME_CATEGORY = os.getenv("AI_FEATURE_CRIME_CATEGORY", "true").lower() == "true"
    FEATURE_RELATED_CASES = os.getenv("AI_FEATURE_RELATED_CASES", "true").lower() == "true"
    FEATURE_SEMANTIC_SEARCH = os.getenv("AI_FEATURE_SEMANTIC_SEARCH", "true").lower() == "true"
    FEATURE_INVESTIGATION_ASSISTANT = os.getenv("AI_FEATURE_INVESTIGATION_ASSISTANT", "true").lower() == "true"

ai_config = AIConfig()
