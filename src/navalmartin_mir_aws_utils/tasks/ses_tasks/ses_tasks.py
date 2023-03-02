from typing import Any
from navalmartin_mir_aws_utils import AWSCredentials_SES
from navalmartin_mir_aws_utils import get_aws_client_factory
from navalmartin_mir_aws_utils.utils import Email


def send_simple_email(email: Email, credentials: AWSCredentials_SES, ses_client: Any = None):

    if ses_client is None:
        ses_client = get_aws_client_factory(credentials=credentials)

    # format the email and send it
    response = ses_client.send_email(
        Source=email.source,
        Destination={
            'ToAddresses': [
                email.destination,
            ],
            'CcAddresses': email.ccs
        },
        ReplyToAddresses=[
            email.reply_to,
        ],
        Message={
            'Subject': {
                'Data': email.subject.data
            },
            'Body': {
                'Text': {
                    'Data': email.body.data
                }
            }
        }
    )
    return response


