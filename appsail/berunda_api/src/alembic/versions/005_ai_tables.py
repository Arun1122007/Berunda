"""Add AI tables for usage, prompts, and conversations."""

import sqlalchemy as sa
from sqlalchemy.sql import func

from alembic import op

revision = "005"
down_revision = "004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ai_UsageRecord
    op.create_table(
        "ai_UsageRecord",
        sa.Column("UsageID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("Provider", sa.String(length=50), nullable=False),
        sa.Column("Model", sa.String(length=100), nullable=False),
        sa.Column("Feature", sa.String(length=100), nullable=False),
        sa.Column("TokensIn", sa.Integer(), nullable=True, server_default=sa.text("0")),
        sa.Column("TokensOut", sa.Integer(), nullable=True, server_default=sa.text("0")),
        sa.Column("CostUSD", sa.Float(), nullable=True, server_default=sa.text("0.0")),
        sa.Column("LatencyMs", sa.Integer(), nullable=True, server_default=sa.text("0")),
        sa.Column("UserID", sa.Integer(), sa.ForeignKey("auth_User.UserID"), nullable=True),
        sa.Column(
            "DistrictID", sa.Integer(), sa.ForeignKey("src_District.DistrictID"), nullable=True
        ),
        sa.Column("CreatedAt", sa.DateTime(), server_default=func.now(), nullable=True),
    )

    # ai_PromptVersion
    op.create_table(
        "ai_PromptVersion",
        sa.Column("PromptVersionID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("PromptName", sa.String(length=100), nullable=False),
        sa.Column("Version", sa.String(length=20), nullable=False),
        sa.Column("Template", sa.Text(), nullable=False),
        sa.Column("ModelConfig", sa.JSON(), nullable=True),
        sa.Column("IsActive", sa.Boolean(), nullable=True, server_default=sa.text("1")),
        sa.Column("CreatedAt", sa.DateTime(), server_default=func.now(), nullable=True),
    )
    op.create_index("ix_ai_PromptVersion_PromptName", "ai_PromptVersion", ["PromptName"])

    # ai_Conversation
    op.create_table(
        "ai_Conversation",
        sa.Column("ConversationID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("UserID", sa.Integer(), sa.ForeignKey("auth_User.UserID"), nullable=False),
        sa.Column("AgentType", sa.String(length=50), nullable=False),
        sa.Column("Title", sa.String(length=200), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(), server_default=func.now(), nullable=True),
        sa.Column("UpdatedAt", sa.DateTime(), server_default=func.now(), nullable=True),
    )

    # ai_Message
    op.create_table(
        "ai_Message",
        sa.Column("MessageID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column(
            "ConversationID",
            sa.Integer(),
            sa.ForeignKey("ai_Conversation.ConversationID"),
            nullable=False,
        ),
        sa.Column("Role", sa.String(length=20), nullable=False),
        sa.Column("Content", sa.Text(), nullable=False),
        sa.Column("ToolCalls", sa.JSON(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(), server_default=func.now(), nullable=True),
    )

    # ai_Feedback
    op.create_table(
        "ai_Feedback",
        sa.Column("FeedbackID", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("MessageID", sa.Integer(), sa.ForeignKey("ai_Message.MessageID"), nullable=False),
        sa.Column("UserID", sa.Integer(), sa.ForeignKey("auth_User.UserID"), nullable=False),
        sa.Column("IsPositive", sa.Boolean(), nullable=False),
        sa.Column("Comments", sa.Text(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(), server_default=func.now(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("ai_Feedback")
    op.drop_table("ai_Message")
    op.drop_table("ai_Conversation")
    op.drop_index("ix_ai_PromptVersion_PromptName", table_name="ai_PromptVersion")
    op.drop_table("ai_PromptVersion")
    op.drop_table("ai_UsageRecord")
