import datetime

from src.models.ai_suggestions import AISuggestion


class ReviewWorkflowService:
    def __init__(self, db_session):
        self.db = db_session

    def accept_suggestion(self, suggestion_id: str, reviewer_id: str):
        suggestion = self.db.query(AISuggestion).filter(AISuggestion.id == suggestion_id).first()
        if not suggestion:
            raise ValueError("Suggestion not found")
        if suggestion.status != "suggested":
            raise ValueError(f"Cannot accept suggestion in state {suggestion.status}")

        suggestion.status = "accepted"
        suggestion.reviewer_id = reviewer_id
        suggestion.review_timestamp = datetime.datetime.utcnow()
        self.db.commit()

        # In a real app, this would also write to the official FIR table here
        return suggestion

    def reject_suggestion(self, suggestion_id: str, reviewer_id: str, reason: str):
        suggestion = self.db.query(AISuggestion).filter(AISuggestion.id == suggestion_id).first()
        if not suggestion:
            raise ValueError("Suggestion not found")
        if suggestion.status != "suggested":
            raise ValueError(f"Cannot reject suggestion in state {suggestion.status}")

        suggestion.status = "rejected"
        suggestion.reviewer_id = reviewer_id
        suggestion.review_reason = reason
        suggestion.review_timestamp = datetime.datetime.utcnow()
        self.db.commit()
        return suggestion
