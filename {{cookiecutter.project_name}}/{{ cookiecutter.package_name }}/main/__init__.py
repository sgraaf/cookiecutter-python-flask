"""The main module."""
from flask import Blueprint

bp = Blueprint("main", __name__)

from {{ cookiecutter.package_name }}.main import routes  # noqa: E402
