from pydantic import EmailStr
from navalmartin_mir_aws_utils import AWSCredentials_SES
from navalmartin_mir_aws_utils.tasks import send_simple_email
from navalmartin_mir_aws_utils.utils import Email, EmailSubject, EmailBody


if __name__ == '__main__':

    credentials = AWSCredentials_SES(aws_region="eu-west-2")
    email = Email(source=EmailStr("some_email@provider.com"),
                  destination=EmailStr("some_email@provider.com"),
                  subject=EmailSubject(data="First notification from mir"),
                  body=EmailBody(data="This your first AWS SES notification from mir. Expect more"),
                  reply_to=EmailStr("alex@navalmartin.com"))

    print(email.dict())
    response = send_simple_email(email=email, credentials=credentials)
    print(response)
