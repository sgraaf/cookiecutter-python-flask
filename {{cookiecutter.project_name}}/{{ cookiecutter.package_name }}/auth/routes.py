"""Routes of the auth module."""
from datetime import datetime
from typing import Union

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug import Response
from werkzeug.urls import url_parse

from {{ cookiecutter.package_name }}.auth import bp
from {{ cookiecutter.package_name }}.auth.email import send_confirmation_email, send_password_reset_email
from {{ cookiecutter.package_name }}.auth.forms import (
    LoginForm,
    RegistrationForm,
    ResetPasswordForm,
    ResetPasswordRequestForm,
)
from {{ cookiecutter.package_name }}.models import User


@bp.route("/login", methods=["GET", "POST"])
def login() -> Union[str, Response]:
    """Login."""
    if current_user.is_authenticated:  # user is already authenticated
        return redirect(url_for("main.index"))
    next_page = request.args.get("next")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email_address(form.email_address.data)
        if user is None or not user.verify_password(form.password.data):
            flash("Invalid email address or password.", "danger")
            return redirect(url_for("auth.login"))
        if not user.is_active:
            flash(
                "First confirm your email address before you attempt to sign in.",
                "danger",
            )
            return redirect(url_for("auth.login"))
        login_user(user, remember=True)
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("auth/login.html", form=form, next_page=next_page)


@bp.route("/logout")
def logout() -> Response:
    """Logout."""
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/register", methods=["GET", "POST"])
def register() -> Union[str, Response]:
    """Registration."""
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.create(
            first_name=form.first_name.data,
            family_name=form.family_name.data,
            email_address=form.email_address.data,
            password=form.password.data,
        )
        send_confirmation_email(user)
        flash(
            "Thank you for signing up! A confirmation email has been sent to your email address.",
            "success",
        )
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@bp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request() -> Union[str, Response]:
    """Password reset request."""
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.get_by_email_address(form.email_address.data)
        if user:
            send_password_reset_email(user)
        flash(
            "Check your inbox for instructions to reset your password.",
            "warning",
        )
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password_request.html", form=form)


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token: str) -> Union[str, Response]:
    """Password reset."""
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("main.index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.update(password=form.password.data)
        flash("Your password has been reset.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form)


@bp.route("/confirmation/<token>")
def confirmation(token: str) -> Response:
    """Confirmation."""
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    user = User.verify_confirmation_token(token)
    if not user:
        return redirect(url_for("main.index"))
    user.update(is_active=True, confirmed_at=datetime.utcnow())
    flash("Your email address is confirmed.", "success")
    return redirect(url_for("auth.login"))
