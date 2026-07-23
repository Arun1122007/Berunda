"""Seed initial test users for authentication.

Revision ID: 006
Revises: 005
"""

import bcrypt

from alembic import op

revision = "006"
down_revision = "005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Hash passwords
    admin_pw = bcrypt.hashpw(b"admin", bcrypt.gensalt()).decode("utf-8")
    analyst_pw = bcrypt.hashpw(b"analyst", bcrypt.gensalt()).decode("utf-8")

    op.execute(f"""
        INSERT INTO "auth_User" ("Email", "HashedPassword", "Role", "IsActive")
        VALUES ('admin@berunda.gov', '{admin_pw}', 'admin', true)
    """)
    op.execute(f"""
        INSERT INTO "auth_User" ("Email", "HashedPassword", "Role", "IsActive")
        VALUES ('analyst@berunda.gov', '{analyst_pw}', 'analyst', true)
    """)


def downgrade() -> None:
    op.execute(
        "DELETE FROM \"auth_User\" WHERE \"Email\" IN ('admin@berunda.gov', 'analyst@berunda.gov')"
    )
