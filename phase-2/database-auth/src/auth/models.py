from dataclasses import dataclass
from typing import Optional


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str


@dataclass
class UserInfo:
    user_id: int
    email: str
    role: str
    district_id: Optional[int] = None
