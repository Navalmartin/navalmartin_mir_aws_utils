"""module simple_email. Models an email to be sent via SES
"""
from typing import List, Optional, Dict
from pydantic import EmailStr, BaseModel, Field


class EmailBody(BaseModel):
    data: str = Field(title="data", description="The actual email content we want to send")
    charset: Optional[str] = Field(title="charset", description="The character set used in the data")
    html: Optional[Dict] = Field(title="html",
                                 description="The content of the message, in HTML format. Use this for email "
                                             "clients that can process HTML. You can include clickable links, "
                                             "formatted text, and much more in an HTML message.")


class EmailSubject(BaseModel):
    data: str = Field(title="data", description="The actual subject of the email")
    charset: Optional[str] = Field(title="charset", description="The character set used in the data")


class Email(BaseModel):

    source: EmailStr
    destination: EmailStr
    subject: EmailSubject = Field(title="subject")
    body: EmailBody = Field(title="body")
    ccs: Optional[List[EmailStr]] = Field(title="ccs", default=[])
    reply_to: Optional[EmailStr] = Field(title="reply_to", default=None)


