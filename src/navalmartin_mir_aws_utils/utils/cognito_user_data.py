from pydantic import BaseModel, Field, EmailStr


class AWSCognitoSignUpUserData(BaseModel):
    email: EmailStr = Field(title="email", description="The email of the user to sign-up")
    password: str = Field(title="password", description="The password of the user to sign-up")
    name: str = Field(title="name", description="The name of the user to sign-up")
    surname: str = Field(title="surname", description="The surname of the user to sign-up")


class AWSCognitoSignInUserData(BaseModel):
    username: EmailStr = Field(title="username", description="The username of the user to sign-in")
    password: str = Field(title="password", description="The password of the user to sign-in")
