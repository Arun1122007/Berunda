from __future__ import annotations

import re


class QueryParser:
    """Parses natural language queries into semantic intent and structured filters.

    In a full production setup, this would use a structured LLM output (e.g. OpenAI function calling).
    For this implementation, we use deterministic matching for key categories and dates to ensure
    speed and reliability.
    """

    def parse(self, query: str) -> dict:
        query_lower = query.lower()

        filters = {}
        semantic_text = query

        # 1. Category extraction
        # We would map against actual `CrimeMajorHead` DB records, but we mock a few common ones
        categories = {
            "theft": 1,
            "robbery": 2,
            "assault": 3,
            "cyber": 4,
            "fraud": 5,
            "vehicle": 1 # Vehicle theft maps to theft for simplicity
        }

        detected_categories = []
        for word, cat_id in categories.items():
            if word in query_lower:
                detected_categories.append(cat_id)
                # optionally remove from semantic text to avoid double-weighting
                # semantic_text = semantic_text.replace(word, "")

        if detected_categories:
            filters["crime_category"] = list(set(detected_categories))

        # 2. Status extraction
        if any(w in query_lower for w in ["unresolved", "pending", "unsolved"]):
            filters["case_status"] = [1, 2] # Mock IDs for pending statuses

        # 3. Clean up semantic text
        semantic_text = re.sub(r'\s+', ' ', semantic_text).strip()

        return {
            "original_query": query,
            "semantic_text": semantic_text,
            "filters": filters
        }
