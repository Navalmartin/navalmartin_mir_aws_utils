"""
Various utilities for working with AWS in Python. The official
PyPi package can be found <a href="https://pypi.org/project/navalmartin-mir-aws-utils/">here</a>.
This package is basically wrappers on top of boto3 that allows for easier development with AWS.
"""
__version__ = '0.0.26'
from .boto3_client import get_aws_client_factory
from .aws_credentials import (AWSCredentials_S3,
                              AWSCredentials_SQS,
                              AWSCredentials_CognitoIDP,
                              AWSCredentials_SecretsManager,
                              AWSCredentials_SES,
                              AWSCredentials_SFN)
from .file_s3_batch import FilePathBatch

