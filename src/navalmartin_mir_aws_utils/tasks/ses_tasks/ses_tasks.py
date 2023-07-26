from typing import Any
from pydantic import EmailStr
from navalmartin_mir_aws_utils import AWSCredentials_SES
from navalmartin_mir_aws_utils import get_aws_client_factory
from navalmartin_mir_aws_utils.utils import Email


def verify_email_identity(email: EmailStr, credentials: AWSCredentials_SES, ses_client: Any = None) -> dict:
    """Before we can send an email using SES, we need to verify the email address

    Parameters
    ----------
    email: The email to verify
    credentials: The credentials to use to connect to the AWS SES client
    ses_client: Use the ses client provided by the client code

    Returns
    -------
    A dictionary describing the client response
    """

    if ses_client is None:
        ses_client = get_aws_client_factory(credentials=credentials)

    response = ses_client.verify_email_identity(EmailAddress=email)
    return response


def send_simple_email(
        email: Email,
        credentials: AWSCredentials_SES, ses_client: Any = None
) -> dict:
    """Send a simple text-based email. If the email body contains
    HTML use the send_html_email method below

    Parameters
    ----------
    email
    credentials
    ses_client

    Returns
    -------

    """
    if ses_client is None:
        ses_client = get_aws_client_factory(credentials=credentials)

    reply_emails = []
    if email.reply_to is not None:
        reply_emails = [email.reply_to]

    # format the email and send it
    response = ses_client.send_email(
        Source=email.source,
        Destination={
            "ToAddresses": [
                email.destination,
            ],
            "CcAddresses": email.ccs,
        },
        ReplyToAddresses=reply_emails,
        Message={
            "Subject": {"Data": email.subject.data, "Charset": email.charset},
            "Body": {"Text": {"Data": email.body.data, "Charset": email.charset}},
        },
    )
    return response


def send_html_email(email: Email,
                    credentials: AWSCredentials_SES,
                    ses_client: Any = None) -> dict:
    """

    Parameters
    ----------
    email
    credentials
    ses_client

    Returns
    -------

    """
    if ses_client is None:
        ses_client = get_aws_client_factory(credentials=credentials)

    reply_emails = []
    if email.reply_to is not None:
        reply_emails = [email.reply_to]

    # format the email and send it
    response = ses_client.send_email(
            Source=email.source,
            Destination={
                "ToAddresses": [
                    email.destination,
                ],
                "CcAddresses": email.ccs,
            },
            ReplyToAddresses=reply_emails,
            Message={
                "Subject": {"Data": email.subject.data, "Charset": email.charset},
                "Body": {"Html": {"Data": email.body.data, "Charset": email.charset}},
            },
        )
    return response
