"""Email module."""
from threading import Thread
from typing import List, Optional

from flask import Flask, current_app
from flask_mail import Message

from {{ cookiecutter.package_name }}.extensions import mail


def send_async_email(app: Flask, msg: Message) -> None:
    """Send an email asynchronously."""
    with app.app_context():
        mail.send(msg)


def send_email(
    subject: str,
    recipients: List[str],
    text_body: Optional[str] = None,
    html_body: Optional[str] = None,
    sender: Optional[str] = None,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
) -> None:
    """Send an email.

    Args:
        subject (str): The subject.
        recipients (List[str]): The recipients.
        text_body (Optional[str]): The body in plaintext.
        html_body (Optional[str]): The body in HTML.
        sender (Optional[str]): The sender.
        cc (Optional[List[str]]): The CC's.
        bcc (Optional[List[str]]): The BCC's.

    Raises:
        ValueError: If the body is not specified (either `text` or `html` or both).
    """
    if text_body is None and html_body is None:
        raise ValueError(
            "Either `text_body` or `html_body` (or both) need to be specified."
        )
    # prepare the email message
    msg = Message(
        subject=subject,
        recipients=recipients,
        body=text_body,
        html=html_body,
        cc=cc,
        bcc=bcc,
    )
    # set the sender
    if sender is not None:
        msg.sender = sender
    # send the email message asynchronously
    Thread(
        target=send_async_email, args=(current_app._get_current_object(), msg)
    ).start()
