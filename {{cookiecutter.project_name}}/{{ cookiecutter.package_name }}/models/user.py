"""User model."""
from __future__ import annotations

from datetime import datetime
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidAlgorithmError,
    InvalidAudienceError,
    InvalidIssuedAtError,
    InvalidIssuerError,
    InvalidKeyError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError,
)
from sqlalchemy.orm import Mapped

from {{ cookiecutter.package_name }}.database import Model, TimestampMixin
from {{ cookiecutter.package_name }}.extensions import bcrypt, db, login_manager


class User(UserMixin, TimestampMixin, Model):
    """A user of the app."""

    __tablename__ = "users"
    email_address: Mapped[str] = db.Column(
        db.String(120), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = db.Column(db.String(128), nullable=False)
    first_name: Mapped[str] = db.Column(db.String(64), nullable=False)
    family_name: Mapped[str] = db.Column(db.String(64), nullable=False)
    is_active: Mapped[bool] = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_at: Mapped[datetime | None] = db.Column(db.DateTime, nullable=True)
    last_seen_at: Mapped[datetime | None] = db.Column(db.DateTime, nullable=True)

    @property
    def password(self) -> None:
        """Get the password.

        Raises:
            AttributeError: password is not a readable attribute.
        """
        raise AttributeError("`password` is not a readable attribute")

    @password.setter
    def password(self, password: str) -> None:
        """Set the password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    @property
    def full_name(self) -> str:
        """The full name of the `User`."""
        return f"{self.first_name} {self.family_name}"

    @property
    def is_confirmed(self) -> bool:
        """Whether the user is confirmed (or not)."""
        return self.confirmed_at is not None

    def verify_password(self, password: str) -> bool:
        """Check the password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in: int = 3600) -> str:
        """Get a "reset password" token."""
        return jwt.encode(
            payload={"reset_password": self.id, "exp": time() + expires_in},
            key=current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_reset_password_token(token: str) -> User | None:
        """Verify the "reset password" token."""
        try:
            id = jwt.decode(
                jwt=token, key=current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )["reset_password"]
        except (
            InvalidTokenError,
            DecodeError,
            InvalidSignatureError,
            ExpiredSignatureError,
            InvalidAudienceError,
            InvalidIssuerError,
            InvalidIssuedAtError,
            InvalidKeyError,
            InvalidAlgorithmError,
            MissingRequiredClaimError,
        ):
            return None
        return User.get_by_id(id)

    def get_confirmation_token(self, expires_in: int = 3600) -> str:
        """Get a confirmation token."""
        return jwt.encode(
            payload={"confirmation": self.id, "exp": time() + expires_in},
            key=current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_confirmation_token(token: str) -> User | None:
        """Verify the confirmation token."""
        try:
            id = jwt.decode(
                jwt=token, key=current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )["confirmation"]
        except (
            InvalidTokenError,
            DecodeError,
            InvalidSignatureError,
            ExpiredSignatureError,
            InvalidAudienceError,
            InvalidIssuerError,
            InvalidIssuedAtError,
            InvalidKeyError,
            InvalidAlgorithmError,
            MissingRequiredClaimError,
        ):
            return None
        return User.get_by_id(id)

    @classmethod
    def get_by_email_address(cls, email_address: str) -> User | None:
        """Get a `User` by their email address."""
        return User.query.filter_by(email_address=email_address).first()


@login_manager.user_loader
def load_user(id: str | bytes | int | float) -> User | None:
    """Load a `User' by their `id`."""
    return User.get_by_id(id)
