from dataclasses import dataclass


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str


@dataclass
class UserInfo:
    user_id: int
    email: str
    role: str
    district_id: int | None = None
