import base64
import hmac
import hashlib
from pydantic import BaseModel, Field, EmailStr


class AWSCognitoSignUpUserData(BaseModel):
    email: EmailStr = Field(title="email")
    password: str = Field(title="password")
    name: str = Field(title="name")
    surname: str = Field(title="surname")


class AWSCognitoSignInUserData(BaseModel):
    username: EmailStr = Field(title="email")
    password: str = Field(title="password")


def get_secret_hash(username: str, client_id: str, client_secret: str):
    msg = username + client_id
    dig = hmac.new(str(client_secret).encode("utf-8"),
                   msg=str(msg).encode("utf-8"),
                   digestmod=hashlib.sha256, ).digest()
    d2 = base64.b64encode(dig).decode()
    return d2
