"""Error handlers."""
from typing import Tuple

from flask import render_template

from {{ cookiecutter.package_name }}.errors import bp
from {{ cookiecutter.package_name }}.extensions import db


@bp.app_errorhandler(404)
def not_found_error(error: Exception) -> Tuple[str, int]:
    """404 error handler."""
    return render_template("errors/404.html"), 404


@bp.app_errorhandler(500)
def internal_error(error: Exception) -> Tuple[str, int]:
    """500 error handler."""
    db.session.rollback()
    return render_template("errors/500.html"), 500
