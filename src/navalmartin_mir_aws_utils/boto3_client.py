import boto3
from typing import Any, Union

from navalmartin_mir_aws_utils.exceptions import InvalidAWSClientException
from navalmartin_mir_aws_utils.aws_credentials import (AWSCredentials_S3, AWSCredentials_SQS, AWSCredentials_CognitoIDP,
                                                       AWSCredentials_SecretsManager, AWSCredentials_SES,
                                                       AWSCredentials_SFN)

VALID_AWS_CLIENTS = ['s3', 'sqs', "cognito-idp", "secretsmanager", 'ses', 'sfn']


def get_aws_client_factory(credentials: Union[AWSCredentials_S3, AWSCredentials_SQS,
                                              AWSCredentials_CognitoIDP,
                                              AWSCredentials_SecretsManager, AWSCredentials_SES,
                                              AWSCredentials_SFN]) -> Any:
    if credentials.aws_client_name not in VALID_AWS_CLIENTS:
        raise InvalidAWSClientException(client_name=credentials.aws_client_name,
                                        allowed_vals=VALID_AWS_CLIENTS)

    if credentials.aws_client_name == 's3':
        return get_aws_s3_client(credentials=credentials)
    elif credentials.aws_client_name == 'sqs':
        return get_aws_sqs_client(credentials=credentials)
    elif credentials.aws_client_name == "cognito-idp":
        return get_aws_cognito_idp_client(credentials=credentials)
    elif credentials.aws_client_name == "secretsmanager":
        return get_aws_secrets_manager_client(credentials=credentials)
    elif credentials.aws_client_name == 'ses':
        return get_aws_ses_client(credentials=credentials)
    elif credentials.aws_client_name == 'sfn':
        return get_aws_sfn_client(credentials=credentials)

    return None


def get_aws_s3_client(credentials: AWSCredentials_S3):
    """Get the AWS S3 client

    Parameters
    ----------
    credentials: Credentials for accessing the S3 service
    Returns
    -------
    """

    if credentials.aws_region == "" or credentials.aws_region is None:
        raise ValueError("Invalid region name in credentials. "
                         "'credentials.aws_region' cannot be '' or None")

    if credentials.aws_secret_access_key is not None and credentials.aws_access_key is not None:
        return boto3.client(credentials.aws_client_name,
                            aws_access_key_id=credentials.aws_access_key,
                            aws_secret_access_key=credentials.aws_secret_access_key,
                            region_name=credentials.aws_region)

    return boto3.client(credentials.aws_client_name,
                        region_name=credentials.aws_region)


def get_aws_sqs_client(credentials: AWSCredentials_SQS):
    """Get the AWS SQS client

    Parameters
    ----------
    credentials: Credentials for accessing the SQS service

    Returns
    -------

    """

    if credentials.aws_region == "" or credentials.aws_region is None:
        raise ValueError("Invalid region name in credentials. "
                         "'credentials.aws_region' cannot be '' or None")

    if credentials.aws_secret_access_key is not None and credentials.aws_access_key is not None:
        return boto3.client(credentials.aws_client_name,
                            aws_access_key_id=credentials.aws_access_key,
                            aws_secret_access_key=credentials.aws_secret_access_key,
                            region_name=credentials.aws_region)

    return boto3.client(credentials.aws_client_name,
                        region_name=credentials.aws_region)


def get_aws_cognito_idp_client(credentials: AWSCredentials_CognitoIDP):
    """Get the Cognito IDP client for the given credentials

    Parameters
    ----------
    credentials: Credentials for accessing the Cognito IDP service

    """

    if credentials.aws_region == "" or credentials.aws_region is None:
        raise ValueError("Invalid region name in credentials. "
                         "'credentials.aws_region' cannot be '' or None")

    if credentials.aws_secret_access_key is not None and credentials.aws_access_key is not None:
        return boto3.client(credentials.aws_client_name,
                            aws_access_key_id=credentials.aws_access_key,
                            aws_secret_access_key=credentials.aws_secret_access_key,
                            region_name=credentials.aws_region)

    return boto3.client(credentials.aws_client_name, credentials.aws_region)


def get_aws_secrets_manager_client(credentials: AWSCredentials_SecretsManager) -> Any:
    """

    Parameters
    ----------
    credentials

    Returns
    -------

    """

    if credentials.aws_region == "" or credentials.aws_region is None:
        raise ValueError("Invalid region name in credentials. "
                         "'credentials.aws_region' cannot be '' or None")

    if credentials.aws_secret_access_key is not None and credentials.aws_access_key is not None:
        return boto3.client(credentials.aws_client_name,
                            aws_access_key_id=credentials.aws_access_key,
                            aws_secret_access_key=credentials.aws_secret_access_key,
                            region_name=credentials.aws_region)

    return boto3.client(credentials.aws_client_name,
                        region_name=credentials.aws_region)


def get_aws_ses_client(credentials: AWSCredentials_SES) -> Any:

    if credentials.aws_region == "" or credentials.aws_region is None:
        raise ValueError("Invalid region name in credentials. "
                         "'credentials.aws_region' cannot be '' or None")

    if credentials.aws_secret_access_key is not None and credentials.aws_access_key is not None:
        return boto3.client(credentials.aws_client_name,
                            aws_access_key_id=credentials.aws_access_key,
                            aws_secret_access_key=credentials.aws_secret_access_key,
                            region_name=credentials.aws_region)

    return boto3.client(credentials.aws_client_name,
                        region_name=credentials.aws_region)


def get_aws_sfn_client(credentials: AWSCredentials_SFN) -> Any:

    if credentials.aws_region == "" or credentials.aws_region is None:
        raise ValueError("Invalid region name in credentials. "
                         "'credentials.aws_region' cannot be '' or None")

    if credentials.aws_secret_access_key is not None and credentials.aws_access_key is not None:
        return boto3.client(credentials.aws_client_name,
                            aws_access_key_id=credentials.aws_access_key,
                            aws_secret_access_key=credentials.aws_secret_access_key,
                            region_name=credentials.aws_region)

    return boto3.client(credentials.aws_client_name,
                        region_name=credentials.aws_region)

