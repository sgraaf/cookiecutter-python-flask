"""Authentication forms."""
from flask_wtf import FlaskForm
from wtforms import EmailField, Field, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

from {{ cookiecutter.package_name }}.models import User


class LoginForm(FlaskForm):
    """Login form."""

    email_address = EmailField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    """Registration form."""

    first_name = StringField("First name", validators=[DataRequired()])
    family_name = StringField("Last name", validators=[DataRequired()])
    email_address = EmailField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")

    def validate_email_address(self, email_address: Field) -> None:
        """Validate the email address."""
        user = User.get_by_email_address(email_address.data)
        if user is not None:
            raise ValidationError(
                f"There already exists an account using the email address {email_address.data}"
            )


class ResetPasswordRequestForm(FlaskForm):
    """Password reset request form."""

    email_address = EmailField("Email address", validators=[DataRequired(), Email()])
    submit = SubmitField("Send instructions")


class ResetPasswordForm(FlaskForm):
    """Password reset form."""

    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Reset Password")
