"""Routes of the main module."""
from datetime import datetime
from urllib.parse import urlparse

from flask import current_app, make_response, render_template, request
from flask_login import current_user, login_required
from werkzeug import Response

from {{ cookiecutter.package_name }}.main import bp
from {{ cookiecutter.package_name }}.utils import URL


@bp.before_request
def before_request() -> None:
    """Set the locale of the application context before each request."""
    if current_user.is_authenticated:
        current_user.update(last_seen_at=datetime.utcnow())


@bp.route("/")
@bp.route("/index")
@login_required
def index() -> str:
    """Index."""
    return render_template("main/index.html", title="Home")


@bp.route("/sitemap.xml")
def sitemap() -> Response:
    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc

    # static routes with static content
    urlset = []
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            url = URL(loc=f"{host_base}{str(rule)}")
            urlset.append(url)

    response = make_response(
        render_template("main/sitemap.xml", urlset=urlset, host_base=host_base)
    )
    response.headers["Content-Type"] = "application/xml"

    return response
