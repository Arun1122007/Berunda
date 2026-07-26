"""Auth enhancements: RBAC permissions, password policy, and account lockout.

Usage:
    from auth_enhancements import create_permissions_table, password_policy_validator, account_lockout_manager
"""

import re
import time
from datetime import datetime, timedelta, timezone

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import Session as SASession

from src.models.auth_models import Permission, User

# ────────────────────────────────────────────────────────────
# 1. RBAC Permission Population
# ────────────────────────────────────────────────────────────

ROLE_PERMISSIONS: dict[str, list[tuple[str, str]]] = {
    "admin": [
        ("users", "read"), ("users", "write"), ("users", "delete"),
        ("cases", "read"), ("cases", "write"), ("cases", "delete"),
        ("reports", "read"), ("reports", "write"),
        ("analytics", "read"),
        ("permissions", "read"), ("permissions", "write"),
        ("settings", "read"), ("settings", "write"),
    ],
    "officer": [
        ("cases", "read"), ("cases", "write"),
        ("reports", "read"),
    ],
    "analyst": [
        ("cases", "read"),
        ("reports", "read"),
        ("analytics", "read"),
    ],
    "viewer": [
        ("reports", "read"),
    ],
}


def create_permissions_table(db: SASession) -> int:
    """Sync the auth_Permission table with ROLE_PERMISSIONS.

    Adds missing rows; does NOT remove rows (append-only for safety).
    Returns the number of rows inserted.
    """
    inserted = 0
    for role, resource_actions in ROLE_PERMISSIONS.items():
        for resource, action in resource_actions:
            existing = db.query(Permission).filter_by(
                Role=role, Resource=resource, Action=action
            ).first()
            if not existing:
                db.add(Permission(Role=role, Resource=resource, Action=action))
                inserted += 1
    if inserted:
        db.commit()
    return inserted


def get_effective_permissions(role: str) -> list[dict]:
    """Return the permission list for a given role."""
    return [
        {"resource": r, "action": a}
        for r, a in ROLE_PERMISSIONS.get(role, [])
    ]


# ────────────────────────────────────────────────────────────
# 2. Password Policy Validator
# ────────────────────────────────────────────────────────────

PASSWORD_RULES = {
    "min_length": 8,
    "require_uppercase": True,
    "require_lowercase": True,
    "require_digit": True,
    "require_special": True,
}

SPECIAL_CHARS = re.escape("!@#$%^&*()_+-=[]{}|;:',.<>?/`~")


class PasswordValidationError(ValueError):
    pass


def password_policy_validator(password: str, rules: dict | None = None) -> str:
    """Validate password strength. Returns the password if valid, raises otherwise."""
    cfg = rules or PASSWORD_RULES

    if len(password) < cfg.get("min_length", 8):
        raise PasswordValidationError(
            f"Password must be at least {cfg['min_length']} characters long"
        )
    if cfg.get("require_uppercase") and not re.search(r"[A-Z]", password):
        raise PasswordValidationError("Password must contain at least one uppercase letter")
    if cfg.get("require_lowercase") and not re.search(r"[a-z]", password):
        raise PasswordValidationError("Password must contain at least one lowercase letter")
    if cfg.get("require_digit") and not re.search(r"\d", password):
        raise PasswordValidationError("Password must contain at least one digit")
    if cfg.get("require_special") and not re.search(f"[{SPECIAL_CHARS}]", password):
        raise PasswordValidationError("Password must contain at least one special character")

    return password


# ────────────────────────────────────────────────────────────
# 3. Account Lockout Manager
# ────────────────────────────────────────────────────────────

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15


class AccountLockoutError(PermissionError):
    pass


class AccountLockoutManager:
    """Tracks failed login attempts and enforces account lockout.

    Uses a runtime dictionary + optional DB columns {FailedLoginAttempts, LockedUntil}.
    To persist across restarts, add these columns to auth_User:

        FailedLoginAttempts = Column(Integer, default=0)
        LockedUntil = Column(DateTime(timezone=True), nullable=True)

    This class supports both in-memory (default) and DB-backed tracking.
    """

    def __init__(
        self,
        max_attempts: int = MAX_FAILED_ATTEMPTS,
        lockout_minutes: int = LOCKOUT_DURATION_MINUTES,
        use_db: bool = False,
    ):
        self.max_attempts = max_attempts
        self.lockout_minutes = lockout_minutes
        self.use_db = use_db
        self._memory_store: dict[int, list[float]] = {}

    def record_failed_attempt(self, user: User, db: SASession | None = None) -> None:
        if self.use_db and db:
            self._record_failed_db(user, db)
        else:
            self._record_failed_memory(user.UserID)

    def _record_failed_memory(self, user_id: int) -> None:
        now = time.time()
        if user_id not in self._memory_store:
            self._memory_store[user_id] = []
        self._memory_store[user_id].append(now)
        cutoff = now - (self.lockout_minutes * 60)
        self._memory_store[user_id] = [
            t for t in self._memory_store[user_id] if t > cutoff
        ]

    def _record_failed_db(self, user: User, db: SASession) -> None:
        user.FailedLoginAttempts = getattr(user, "FailedLoginAttempts", 0) + 1
        if user.FailedLoginAttempts >= self.max_attempts:
            user.LockedUntil = datetime.now(timezone.utc) + timedelta(minutes=self.lockout_minutes)
        db.commit()

    def check_lockout(self, user: User, db: SASession | None = None) -> None:
        if self.use_db and db:
            self._check_lockout_db(user, db)
        else:
            self._check_lockout_memory(user.UserID)

    def _check_lockout_memory(self, user_id: int) -> None:
        attempts = self._memory_store.get(user_id, [])
        now = time.time()
        cutoff = now - (self.lockout_minutes * 60)
        recent = [t for t in attempts if t > cutoff]
        if len(recent) >= self.max_attempts:
            oldest = min(recent)
            remaining = int(self.lockout_minutes * 60 - (now - oldest))
            raise AccountLockoutError(
                f"Account locked. Try again in {remaining // 60} minutes."
            )

    def _check_lockout_db(self, user: User, db: SASession) -> None:
        locked_until = getattr(user, "LockedUntil", None)
        if locked_until and locked_until > datetime.now(timezone.utc):
            remaining = int((locked_until - datetime.now(timezone.utc)).total_seconds() // 60)
            raise AccountLockoutError(
                f"Account locked. Try again in {remaining} minutes."
            )

    def reset_attempts(self, user: User, db: SASession | None = None) -> None:
        if self.use_db and db:
            user.FailedLoginAttempts = 0
            user.LockedUntil = None
            db.commit()
        else:
            self._memory_store.pop(user.UserID, None)

    def is_locked(self, user: User, db: SASession | None = None) -> bool:
        try:
            self.check_lockout(user, db)
            return False
        except AccountLockoutError:
            return True


# ────────────────────────────────────────────────────────────
# 4. Column definitions for DB-backed lockout (for migration scripts)
# ────────────────────────────────────────────────────────────

FAILED_ATTEMPT_COLS = [
    Column("FailedLoginAttempts", Integer, default=0),
    Column("LockedUntil", DateTime(timezone=True), nullable=True),
]


def get_lockout_column_defs() -> list[Column]:
    """Return Column definitions for FailedLoginAttempts and LockedUntil.

    Use in migration scripts to add lockout support to auth_User:
        from auth_enhancements import get_lockout_column_defs
        for col in get_lockout_column_defs():
            op.add_column("auth_User", col)
    """
    return FAILED_ATTEMPT_COLS
