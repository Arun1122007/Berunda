"""Generate initial Alembic migration from model metadata."""

import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from src.models.base import Base

REVISION_ID = "001"
DOWN_REVISION = None
DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

COLUMN_TYPE_MAP = {
    "INTEGER": "sa.Integer",
    "BIGINT": "sa.BigInteger",
    "SMALLINT": "sa.SmallInteger",
    "VARCHAR": "sa.String",
    "TEXT": "sa.Text",
    "BOOLEAN": "sa.Boolean",
    "DATE": "sa.Date",
    "DATETIME": "sa.DateTime",
    "FLOAT": "sa.Float",
    "NUMERIC": "sa.Numeric",
    "JSON": "sa.JSON",
    "BLOB": "sa.LargeBinary",
}


def _map_type(col):
    for t_name, _ in COLUMN_TYPE_MAP.items():
        if t_name in str(col.type).upper():
            return t_name.lower()
    return "sa.String"


def generate():
    migration_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "src", "alembic", "versions"
    )
    os.makedirs(migration_dir, exist_ok=True)

    filename = os.path.join(migration_dir, f"{REVISION_ID}_initial_schema.py")
    lines = []
    lines.append('"""initial schema — create all model tables."""')
    lines.append("")
    lines.append("import sqlalchemy as sa")
    lines.append("from alembic import op")
    lines.append("")
    lines.append(f"revision = {REVISION_ID!r}")
    lines.append(f"down_revision = {DOWN_REVISION!r}")
    lines.append("branch_labels = None")
    lines.append("depends_on = None")
    lines.append("")

    # upgrade
    lines.append("")
    lines.append("def upgrade() -> None:")
    for table in Base.metadata.sorted_tables:
        lines.append("    op.create_table(")
        lines.append(f"        {table.name!r},")
        for col in table.columns:
            col_type = str(col.type)
            nullable = "nullable=True" if col.nullable else "nullable=False"
            pk = "primary_key=True" in str(col).lower() or col.primary_key
            pk_str = ", primary_key=True" if pk else ""
            default = ""
            if col.default is not None and hasattr(col.default, "arg"):
                d = col.default.arg
                if isinstance(d, str):
                    default = f", server_default={d!r}"
                elif callable(d):
                    default = ", server_default=sa.func.now()"
                else:
                    default = f", server_default={d!r}"
            fk = ""
            for fk_col in col.foreign_keys:
                fk = f", sa.ForeignKey({fk_col.column.table.name!r}.{fk_col.column.name!r})"
                break
            lines.append(
                f"        sa.Column({col.name!r}, sa.{col_type}, {nullable}{pk_str}{fk}{default}),"
            )
        lines.append("    )")
        lines.append("")

    lines.append("")
    lines.append("def downgrade() -> None:")
    for table in reversed(Base.metadata.sorted_tables):
        lines.append(f"    op.drop_table({table.name!r})")
    lines.append("")

    content = "\n".join(lines)
    with open(filename, "w") as f:
        f.write(content)
    print(f"Generated migration: {filename}")
    print(f"Tables: {len(Base.metadata.sorted_tables)}")


if __name__ == "__main__":
    generate()
