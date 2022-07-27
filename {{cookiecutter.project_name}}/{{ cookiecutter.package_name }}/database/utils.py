"""Database utility functions."""
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Mapped

from {{ cookiecutter.package_name }}.extensions import db


def foreign_key_reference_col(
    column_or_model_or_table: Union[db.Column, db.Model, str],
    nullable: bool = False,
    primary_key: bool = False,
    foreign_key_kwargs: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Mapped[int]:
    """Adds a foreign key reference column."""
    foreign_key_kwargs = foreign_key_kwargs or {}

    if isinstance(column_or_model_or_table, db.Column):
        fk_column = column_or_model_or_table
    elif isinstance(column_or_model_or_table, db.Model):
        fk_column = column_or_model_or_table.id
    elif isinstance(column_or_model_or_table, str):
        fk_column = f"{column_or_model_or_table}.id"
    else:
        raise TypeError(
            "`column_or_model_or_table` must be either a `Column`, `Model`, or `str`."
        )

    return db.Column(
        db.Integer,
        db.ForeignKey(fk_column, **foreign_key_kwargs),
        nullable=nullable,
        primary_key=primary_key,
        **kwargs,
    )
