from navalmartin_mir_aws_utils.aws_credentials import AWSCredentials_CognitoIDP
from navalmartin_mir_aws_utils.cognito_idp_utils import (global_signout_user_from_pool,
                                                         authenticate_and_get_token_for_user)
from navalmartin_mir_aws_utils.utils import AWSCognitoSignInUserData

AWS_REGION = ""
AWS_COGNITO_POOL_ID = ""
AWS_COGNITO_CLIENT_ID = ""
AWS_COGNITO_CLIENT_SECRET = ""

if __name__ == '__main__':
    user_data = AWSCognitoSignInUserData(username="",
                                         password="")

    aws_credentials = AWSCredentials_CognitoIDP(aws_region=AWS_REGION,
                                                aws_cognito_pool_id=AWS_COGNITO_POOL_ID,
                                                aws_cognito_client_id=AWS_COGNITO_CLIENT_ID,
                                                aws_cognito_client_secret=AWS_COGNITO_CLIENT_SECRET,
                                                aws_access_key=None, aws_secret_access_key=None)

    response = authenticate_and_get_token_for_user(aws_cognito_credentials=aws_credentials,
                                                   user_data=user_data)

    access_token = response["AuthenticationResult"]["AccessToken"]
    print(f"Access token {access_token}")

    response = global_signout_user_from_pool(access_token=access_token,
                                             credentials=aws_credentials)

    print(f"Revoke response {response}")
