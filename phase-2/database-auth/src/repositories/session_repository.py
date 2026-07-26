from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session as SASession

from ..models import Session
from .base import Repository


class SessionRepository(Repository[Session]):

    def __init__(self, db: SASession):
        self.db = db

    def get_by_id(self, entity_id: int) -> Optional[Session]:
        return self.db.query(Session).filter(Session.SessionID == entity_id).first()

    def find_by_hash(self, token_hash: str) -> Optional[Session]:
        return self.db.query(Session).filter(
            Session.TokenHash == token_hash,
            Session.RevokedAt.is_(None),
        ).first()

    def list(
        self,
        offset: int = 0,
        limit: int = 100,
        **filters: Any,
    ) -> List[Session]:
        q = self.db.query(Session)
        if "user_id" in filters and filters["user_id"] is not None:
            q = q.filter(Session.UserID == filters["user_id"])
        return q.offset(offset).limit(limit).all()

    def create(self, data: Dict[str, Any]) -> Session:
        session = Session(**data)
        self.db.add(session)
        self.db.flush()
        return session

    def revoke(self, session_id: int) -> Optional[Session]:
        session = self.db.query(Session).filter(Session.SessionID == session_id).first()
        if not session:
            return None
        session.RevokedAt = datetime.now(timezone.utc)
        self.db.flush()
        return session

    def update(self, entity_id: int, data: Dict[str, Any]) -> Optional[Session]:
        session = self.db.query(Session).filter(Session.SessionID == entity_id).first()
        if not session:
            return None
        for key, value in data.items():
            if hasattr(session, key):
                setattr(session, key, value)
        self.db.flush()
        return session

    def delete(self, entity_id: int) -> bool:
        session = self.db.query(Session).filter(Session.SessionID == entity_id).first()
        if not session:
            return False
        self.db.delete(session)
        self.db.flush()
        return True
