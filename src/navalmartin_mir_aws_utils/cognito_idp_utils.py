from typing import Any, Callable
from navalmartin_mir_aws_utils.aws_credentials import AWSCredentials_CognitoIDP
from navalmartin_mir_aws_utils.boto3_client import get_aws_cognito_idp_client
from navalmartin_mir_aws_utils.utils import AWSCognitoSignUpUserData, AWSCognitoSignInUserData
from navalmartin_mir_aws_utils.utils import get_secret_hash


def global_signout_user_from_pool(access_token: str,
                                  credentials: AWSCredentials_CognitoIDP) -> Any:
    """Signs out users from all devices. 
    It also invalidates all refresh tokens that Amazon Cognito 
    has issued to a user. A user can still use a hosted UI cookie to 
    retrieve new tokens for the duration of the 1-hour cookie validity period.

    Parameters
    ----------
    access_token: The access token that corresponds to the signed in  user
    credentials: Credentials for accessing the Cognito IDP service
    
    """

    client = get_aws_cognito_idp_client(credentials=credentials)
    return client.global_sign_out(AccessToken=access_token)


def signup_cognito_user(user_data: AWSCognitoSignUpUserData,
                        aws_cognito_credentials: AWSCredentials_CognitoIDP,
                        secret_hash_builder: Callable, print_exception_info: bool = False) -> Any:
    """Signup the user on the AWS Cognito

     Parameters
    ----------
    user_data: The user data to signup
    aws_cognito_credentials: Credentials for accessing the Cognito IDP service
    secret_hash_builder: The callable to build the secret hash
    print_exception_info: Flag indicating if information is to be printed upon excpetion

    """
    try:

        aws_region_name = aws_cognito_credentials.aws_region
        aws_cognito_user_client_id = aws_cognito_credentials.aws_cognito_pool_id
        aws_cognito_client_secret = aws_cognito_credentials.aws_cognito_client_secret

        secret_hash = secret_hash_builder(user_data.email,
                                          aws_cognito_user_client_id,
                                          aws_cognito_client_secret)

        boto3_client = get_aws_cognito_idp_client(credentials=aws_cognito_credentials)

        cognito_resp = boto3_client.sign_up(
            ClientId=aws_cognito_user_client_id,
            SecretHash=secret_hash,
            Username=user_data.email,
            Password=user_data.password,
            UserAttributes=[
                {"Name": "family_name", "Value": user_data.surname},
                {"Name": "name", "Value": user_data.name},
            ],
        )
        return cognito_resp, secret_hash
    except Exception as e:
        print("Signup AWS Cognito failed with")

        if print_exception_info:
            print(f"AWS Region name {aws_cognito_credentials.aws_region}")
            print(f"AWS Cognito client Id {aws_cognito_credentials.aws_cognito_client_id}")
            print(f"AWS Cognito client secret {aws_cognito_credentials.aws_cognito_client_secret}")
            print(f"Exception message {str(e)}")
        raise e


def authenticate_and_get_token_for_user(user_data: AWSCognitoSignInUserData,
                                        aws_cognito_credentials: AWSCredentials_CognitoIDP) -> Any:
    client = get_aws_cognito_idp_client(credentials=aws_cognito_credentials)

    secret_hash = get_secret_hash(username=user_data.username,
                                  client_id=aws_cognito_credentials.aws_cognito_client_id,
                                  client_secret=aws_cognito_credentials.aws_cognito_client_secret)

    resp = client.initiate_auth(
        ClientId=aws_cognito_credentials.aws_cognito_client_id,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": user_data.username,
            "PASSWORD": user_data.password,
            "SECRET_HASH": secret_hash,
        },
    )
    return resp
