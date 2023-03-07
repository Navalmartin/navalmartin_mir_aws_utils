import json
from navalmartin_mir_aws_utils import AWSCredentials_SecretsManager
from navalmartin_mir_aws_utils import get_aws_client_factory

def get_error_return(error: str) -> dict:
    return {'result': 'FAILED', 'error': error}

def get_success_return(success_msg: str = "OK") -> dict:
    return {'result': success_msg, 'error': []}


def get_secrets(credentials: AWSCredentials_SecretsManager) -> dict:
    """Returns a dictionary wiht the SecretString of the specified
    secrets manager
    """
    client = get_aws_client_factory(credentials=credentials)
    get_secret_value_response = client.get_secret_value(SecretId=credentials.secret_name)
    secret_string = get_secret_value_response['SecretString']
    secret_string = json.loads(secret_string)
    return secret_string