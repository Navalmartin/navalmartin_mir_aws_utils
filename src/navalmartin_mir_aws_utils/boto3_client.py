import boto3
from navalmartin_mir_aws_utils.aws_credentials import (AWSCredentials_S3, AWSCredentials_SQS, AWSCredentials_CognitoIDP)


def get_aws_s3_client(credentials: AWSCredentials_S3):
    """Get the AWS S3 client

    Parameters
    ----------
    credentials: Credentials for accessing the S3 service
    Returns
    -------
    """
    return boto3.client('s3',
                        aws_access_key_id=credentials.aws_access_key,
                        aws_secret_access_key=credentials.aws_secret_access_key,
                        region_name=credentials.aws_region)


def get_aws_sqs_client(credentials: AWSCredentials_SQS):
    """Get the AWS SQS client

    Parameters
    ----------
    credentials: Credentials for accessing the SQS service

    Returns
    -------

    """
    return boto3.client('sqs',
                        aws_access_key_id=credentials.aws_access_key,
                        aws_secret_access_key=credentials.aws_secret_access_key,
                        region_name=credentials.aws_region)


def get_aws_cognito_idp_client(credentials: AWSCredentials_CognitoIDP):
    """Get the Cognito IDP client for the given credentials

    Parameters
    ----------
    credentials: Credentials for accessing the Cognito IDP service

    """
    return boto3.client("cognito-idp", credentials.aws_region)









