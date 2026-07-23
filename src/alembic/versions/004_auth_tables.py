"""Add auth tables for users, sessions, and permissions."""

import sqlalchemy as sa
from sqlalchemy.sql import func

from alembic import op

revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create auth_User table
    op.create_table(
        "auth_User",
        sa.Column("UserID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("Email", sa.String(length=255), nullable=False),
        sa.Column("HashedPassword", sa.String(length=255), nullable=False),
        sa.Column("Role", sa.String(length=50), nullable=False),
        sa.Column(
            "DistrictID", sa.Integer(), sa.ForeignKey("src_District.DistrictID"), nullable=True
        ),
        sa.Column("IsActive", sa.Boolean(), nullable=True, server_default=sa.text("1")),
        sa.Column("CreatedAt", sa.DateTime(), server_default=func.now(), nullable=True),
        sa.Column("UpdatedAt", sa.DateTime(), server_default=func.now(), nullable=True),
    )
    op.create_index("ix_auth_User_Email", "auth_User", ["Email"], unique=True)

    # Create auth_Session table
    op.create_table(
        "auth_Session",
        sa.Column("SessionID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("UserID", sa.Integer(), sa.ForeignKey("auth_User.UserID"), nullable=False),
        sa.Column("TokenHash", sa.String(length=255), nullable=False),
        sa.Column("ExpiresAt", sa.DateTime(), nullable=False),
        sa.Column("RevokedAt", sa.DateTime(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(), server_default=func.now(), nullable=True),
    )
    op.create_index("ix_auth_Session_TokenHash", "auth_Session", ["TokenHash"], unique=True)

    # Create auth_Permission table
    op.create_table(
        "auth_Permission",
        sa.Column("PermissionID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("Role", sa.String(length=50), nullable=False),
        sa.Column("Resource", sa.String(length=100), nullable=False),
        sa.Column("Action", sa.String(length=50), nullable=False),
        sa.Column("CreatedAt", sa.DateTime(), server_default=func.now(), nullable=True),
    )
    op.create_index("ix_auth_Permission_Role", "auth_Permission", ["Role"])


def downgrade() -> None:
    op.drop_index("ix_auth_Permission_Role", table_name="auth_Permission")
    op.drop_table("auth_Permission")
    op.drop_index("ix_auth_Session_TokenHash", table_name="auth_Session")
    op.drop_table("auth_Session")
    op.drop_index("ix_auth_User_Email", table_name="auth_User")
    op.drop_table("auth_User")
