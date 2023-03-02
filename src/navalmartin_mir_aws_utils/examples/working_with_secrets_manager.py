from botocore.exceptions import ClientError
from navalmartin_mir_aws_utils import get_aws_client_factory, AWSCredentials_SecretsManager

AWS_SECRET_NAME = "YOUR-AWS-Secrets-Manager"
AWS_REGION = "YOUR-AWS-REGION"

if __name__ == '__main__':

    try:
        credentials = AWSCredentials_SecretsManager(aws_region=AWS_REGION,
                                                    secret_name=AWS_SECRET_NAME)
        client = get_aws_client_factory(credentials=credentials)

        get_secret_value_response = client.get_secret_value(SecretId=credentials.secret_name)
        print(get_secret_value_response)
    except ClientError as e:
        print(str(e))
