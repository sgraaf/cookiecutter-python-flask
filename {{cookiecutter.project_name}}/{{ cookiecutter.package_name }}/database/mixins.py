"""Database mixins module."""
from datetime import datetime
from typing import Type, TypeVar

from sqlalchemy.orm import Mapped

from {{ cookiecutter.package_name }}.extensions import db

T = TypeVar("T", bound="CRUDMixin")


class CRUDMixin:
    """Mixin class for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls: Type[T], **kwargs) -> T:
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    add = create

    def update(self: T, commit: bool = True, **kwargs) -> T:
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if commit:
            return self.save()
        return self

    def save(self: T, commit: bool = True) -> T:
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self: T, commit: bool = True) -> None:
        """Remove the record from the database."""
        db.session.delete(self)
        if commit:
            return db.session.commit()
        return None

    remove = delete


class TimestampMixin:
    """Mixin class for timestamping models."""

    created_at: Mapped[datetime] = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
