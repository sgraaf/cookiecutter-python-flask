"""Base model class module."""
from __future__ import annotations

from flask_sqlalchemy.model import camel_to_snake_case
from sqlalchemy.orm import declared_attr, Mapped

from {{ cookiecutter.package_name }}.database.mixins import CRUDMixin
from {{ cookiecutter.package_name }}.extensions import db


class Model(CRUDMixin, db.Model):  # type: ignore
    """Base model class.

    Features:
    * Adds type hint(s) for IDE autocomplete.
    * Adds a 'primary key' column named `id` and `get_by_id` convenience method.
    * Adds CRUD convenience methods.
    """

    __abstract__ = True
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return f"{camel_to_snake_case(cls.__name__)}s"

    @classmethod
    def get_by_id(cls: type[Model], id: str | bytes | int | float) -> Model | None:
        """Get record by id."""
        if any(
            (
                isinstance(id, (str, bytes)) and id.isdigit(),
                isinstance(id, (int, float)),
            )
        ):
            return cls.query.get(int(id))
        return None
