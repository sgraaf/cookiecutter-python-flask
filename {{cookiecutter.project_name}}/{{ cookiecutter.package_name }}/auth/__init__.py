"""The auth module."""
from flask import Blueprint

bp = Blueprint("auth", __name__)

from {{ cookiecutter.package_name }}.auth import routes  # noqa: E402
