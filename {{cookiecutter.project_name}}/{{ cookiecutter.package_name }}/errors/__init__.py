"""The errors module."""
from flask import Blueprint

bp = Blueprint("errors", __name__)

from {{ cookiecutter.package_name }}.errors import handlers  # noqa: E402
