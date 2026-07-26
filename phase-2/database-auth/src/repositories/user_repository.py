from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session as SASession

from ..models import User
from .base import Repository


class UserRepository(Repository[User]):

    def __init__(self, db: SASession):
        self.db = db

    def get_by_id(self, entity_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.UserID == entity_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.Email == email).first()

    def list(
        self,
        offset: int = 0,
        limit: int = 100,
        **filters: Any,
    ) -> List[User]:
        q = self.db.query(User)
        if "role" in filters and filters["role"] is not None:
            q = q.filter(User.Role == filters["role"])
        if "is_active" in filters and filters["is_active"] is not None:
            q = q.filter(User.IsActive == filters["is_active"])
        return q.offset(offset).limit(limit).all()

    def create(self, data: Dict[str, Any]) -> User:
        user = User(**data)
        self.db.add(user)
        self.db.flush()
        return user

    def update(self, entity_id: int, data: Dict[str, Any]) -> Optional[User]:
        user = self.db.query(User).filter(User.UserID == entity_id).first()
        if not user:
            return None
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        self.db.flush()
        return user

    def delete(self, entity_id: int) -> bool:
        user = self.db.query(User).filter(User.UserID == entity_id).first()
        if not user:
            return False
        self.db.delete(user)
        self.db.flush()
        return True
