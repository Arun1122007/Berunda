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
    import os
    import secrets
    import logging

    # Hash passwords
    default_pw = secrets.token_urlsafe(12)
    admin_raw_pw = os.environ.get("INITIAL_ADMIN_PASSWORD", default_pw)
    analyst_raw_pw = os.environ.get("INITIAL_ANALYST_PASSWORD", default_pw)

    if admin_raw_pw == default_pw:
        logging.getLogger("alembic").info(f"Generated secure initial password for seed users: {default_pw}")

    admin_pw = bcrypt.hashpw(admin_raw_pw.encode(), bcrypt.gensalt()).decode("utf-8")
    analyst_pw = bcrypt.hashpw(analyst_raw_pw.encode(), bcrypt.gensalt()).decode("utf-8")

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
