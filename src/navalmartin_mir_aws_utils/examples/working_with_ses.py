from pydantic import EmailStr
from navalmartin_mir_aws_utils import AWSCredentials_SES
from navalmartin_mir_aws_utils.tasks import send_simple_email, send_html_email
from navalmartin_mir_aws_utils.utils import Email, EmailSubject, EmailBody


if __name__ == "__main__":
    credentials = AWSCredentials_SES(aws_region="eu-west-2")
    email = Email(
        source=EmailStr("mir-surveys@mir.blue"),
        destination=EmailStr("alex@navalmartin.com"),
        subject=EmailSubject(data="First notification from mir"),
        body=EmailBody(
            data="This your first AWS SES notification from mir. Expect more."
        ),
    )

    print(email.dict())
    response = send_simple_email(email=email, credentials=credentials)
    print(response)

    email_html = """<html>
    <p>Your survey PDF has been compiled. You can access it here <a href="{0}">my-survey</a>.
    Alternatively, you can login to your account <a href="https://mir.blue/session/login">here</a>.
    </p>
    
    <p>
    For any questions or clarifications you may have regarding this survey, please get in 
    touch at mir-surveys@min.blue. Please use the survey id in your email.</>
    
    <p>Thank you for using mir.</p>
    
    </html>
    """.format("https://mir.blue/session/login")
    email = Email(
        source=EmailStr("mir-surveys@mir.blue"),
        destination=EmailStr("alex@navalmartin.com"),
        subject=EmailSubject(data="Your survey 1235 is ready."),
        body=EmailBody(
            data=email_html
        ),
    )

    print(email.dict())
    response = send_html_email(email=email, credentials=credentials)
    print(response)
