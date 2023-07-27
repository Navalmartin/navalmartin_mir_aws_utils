"""
Various utilities for working with AWS in Python. The official
PyPi package can be found <a href="https://pypi.org/project/navalmartin-mir-aws-utils/">here</a>.
This package is basically wrappers on top of boto3 that allows for easier development with AWS.
"""
__version__ = "0.0.34"
from .boto3_client import get_aws_client_factory
from .aws_credentials import (
    AWSCredentials_S3,
    AWSCredentials_SQS,
    AWSCredentials_CognitoIDP,
    AWSCredentials_SecretsManager,
    AWSCredentials_SES,
    AWSCredentials_SFN,
    AWSCredentials_SageMaker
)
from .file_s3_batch import FilePathBatch
from .s3_utils import (get_s3_iterator,
                       expand_s3_iterator_contents,
                       expand_s3_iterator_common_prefixes,
                       delete_s3_all_objs_with_key,
                       delete_s3_object_with_key,
                       save_object_to_s3,
                       generate_presigned_url)

from .utils.simple_email import (Email,
                                 EmailBody,
                                 EmailSubject)

from .tasks.ses_tasks.ses_tasks import (verify_email_identity,
                                        send_simple_email,
                                        send_html_email)
