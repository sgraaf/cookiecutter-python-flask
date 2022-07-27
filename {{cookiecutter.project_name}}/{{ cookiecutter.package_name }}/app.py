"""The app module, containing the application factory function."""
import logging
from inspect import getmembers
from logging.handlers import RotatingFileHandler, SMTPHandler
from typing import Any, Dict

from flask import Flask

from config import LOGS_DIR, Config
from {{ cookiecutter.package_name }} import models
from {{ cookiecutter.package_name }}.extensions import bcrypt, bootstrap, db, login_manager, mail, moment
from {{ cookiecutter.package_name }}.utils import CustomJSONEncoder, datetime_format


def register_extensions(app: Flask) -> None:
    """Register Flask extensions."""
    db.init_app(app)
    bcrypt.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)


def register_blueprints(app: Flask) -> None:
    """Register Flask blueprints."""
    from {{ cookiecutter.package_name }} import auth, errors, main

    app.register_blueprint(auth.bp)
    app.register_blueprint(errors.bp)
    app.register_blueprint(main.bp)


def register_shell_context(app: Flask) -> None:
    """Register shell context objects."""

    def make_shell_context() -> Dict[str, Any]:
        shell_context: Dict[str, Any] = {"db": db}
        shell_context.update(
            {
                k: v
                for k, v in getmembers(models)
                if isinstance(v, type) and issubclass(v, db.Model)
            }
        )
        return shell_context

    app.shell_context_processor(make_shell_context)


def configure_logging(app: Flask) -> None:
    """Configure logging."""
    if not app.debug and not app.testing:
        if app.config["MAIL_SERVER"]:
            auth = None
            if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
                auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
            secure = None
            if app.config["MAIL_USE_TLS"]:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
                fromaddr=app.config["MAIL_DEFAULT_SENDER"],
                toaddrs=app.config["ADMINS"],
                subject="{{ cookiecutter.friendly_name }} Failure",
                credentials=auth,
                secure=secure,
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        LOGS_DIR.mkdir(exist_ok=True)
        file_handler = RotatingFileHandler(
            LOGS_DIR / "{{ cookiecutter.package_name }}.log",
            maxBytes=10240,
            backupCount=10,
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)


def create_app(config_class: object = Config) -> Flask:
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    Args:
        config_class (object): The configuration object to use.

    Returns:
        Flask: The Flask application.
    """
    # initialize the app
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.filters["datetime_format"] = datetime_format
    # register extensions
    register_extensions(app)
    # register blueprints
    register_blueprints(app)
    # register shell context
    register_shell_context(app)
    # configure logging
    configure_logging(app)
    # set the JSON encoder
    app.json_encoder = CustomJSONEncoder
    return app
