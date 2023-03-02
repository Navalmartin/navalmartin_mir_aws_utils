__version__ = '0.0.14'
from .boto3_client import get_aws_client_factory
from .aws_credentials import (AWSCredentials_S3,
                              AWSCredentials_SQS,
                              AWSCredentials_CognitoIDP,
                              AWSCredentials_SecretsManager)
