import re
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)

class PrivacyGateway:
    """
    Acts as a secure interceptor before data reaches the external AI Model Provider.
    Strips raw PII based on simple Regex/NLP heuristics.
    """
    PHONE_REGEX = re.compile(r'\+?\d{10,13}')
    EMAIL_REGEX = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
    
    @classmethod
    def apply_privacy_mask(cls, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Replaces sensitive tokens with placeholders and stores mapping.
        """
        if not text:
            return text, {}
            
        token_map = {}
        masked_text = text
        
        # Mask Phones
        for i, match in enumerate(cls.PHONE_REGEX.finditer(masked_text)):
            placeholder = f"[PHONE_{i}]"
            token_map[placeholder] = match.group()
            masked_text = masked_text.replace(match.group(), placeholder)
            
        # Mask Emails
        for i, match in enumerate(cls.EMAIL_REGEX.finditer(masked_text)):
            placeholder = f"[EMAIL_{i}]"
            token_map[placeholder] = match.group()
            masked_text = masked_text.replace(match.group(), placeholder)
            
        logger.debug(f"Privacy Gateway masked {len(token_map)} tokens.")
        return masked_text, token_map

    @classmethod
    def restore_privacy_mask(cls, text: str, token_map: Dict[str, str]) -> str:
        """
        Restores sensitive tokens to output if the schema requires it.
        (Usually, for Analytics or Public Summaries, we leave them masked).
        """
        if not text or not token_map:
            return text
            
        restored = text
        for placeholder, original in token_map.items():
            restored = restored.replace(placeholder, original)
        return restored
