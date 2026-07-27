import datetime

from sqlalchemy import JSON, Column, DateTime, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AISuggestion(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "ai_suggestions"

    id = Column(String, primary_key=True)
    fir_id = Column(String, index=True)
    capability = Column(String)  # extraction, summarization, etc.
    suggested_value = Column(JSON)
    status = Column(String, default="suggested") # suggested, under_review, accepted, rejected, superseded

    # Review details
    reviewer_id = Column(String, nullable=True)
    review_timestamp = Column(DateTime, nullable=True)
    review_reason = Column(String, nullable=True)

    # Provenance
    prompt_version = Column(String)
    model_version = Column(String)
    generation_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
