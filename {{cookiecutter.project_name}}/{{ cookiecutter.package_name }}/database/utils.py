"""Database utility functions."""
from typing import Any, Dict, Optional

from sqlalchemy.orm import Mapped

from {{ cookiecutter.package_name }}.extensions import db


def foreign_key_reference_col(
    table: str,
    nullable: bool = False,
    foreign_key_kwargs: Optional[Dict[str, Any]] = None,
    column_kwargs: Optional[Dict[str, Any]] = None,
) -> Mapped[int]:
    """Adds a foreign key reference column."""
    foreign_key_kwargs = foreign_key_kwargs or {}
    column_kwargs = column_kwargs or {}

    return db.Column(
        db.Integer,
        db.ForeignKey(f"{table}.id", **foreign_key_kwargs),
        nullable=nullable,
        **column_kwargs,
    )
