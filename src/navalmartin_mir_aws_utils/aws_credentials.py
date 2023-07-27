"""module aws_credentials. Utility class to move around
credentials. This class is not used to load the
credentials. It is the application's duty to do so

"""


class AWSCredentials(object):
    def __init__(
            self,
            aws_client_name: str = None,
            aws_access_key: str = None,
            aws_secret_access_key: str = None,
    ):
        self.aws_client_name: str = aws_client_name
        self.aws_access_key: str = aws_access_key
        self.aws_secret_access_key = aws_secret_access_key


class AWSCredentials_S3(AWSCredentials):
    def __init__(
            self,
            aws_s3_bucket_name: str,
            aws_region: str,
            aws_access_key: str = None,
            aws_secret_access_key: str = None,
    ):
        super(AWSCredentials_S3, self).__init__(
            aws_client_name="s3",
            aws_secret_access_key=aws_secret_access_key,
            aws_access_key=aws_access_key,
        )
        self.aws_s3_bucket_name = aws_s3_bucket_name
        self.aws_region = aws_region

    def __str__(self) -> str:
        result = f"aws_client_name={self.aws_client_name}\n"
        result += f"aws_access_key={self.aws_access_key}\n"
        result += f"aws_secret_access_key={self.aws_secret_access_key}\n"
        result += f"aws_region={self.aws_region}\n"
        result += f"aws_s3_bucket_name={self.aws_s3_bucket_name}"
        return result


class AWSCredentials_SQS(AWSCredentials):
    def __init__(
            self,
            aws_sqs_queue_name: str,
            aws_region: str,
            aws_queue_url: str,
            aws_access_key: str = None,
            aws_secret_access_key: str = None,
    ):
        super(AWSCredentials_SQS, self).__init__(
            aws_client_name="sqs",
            aws_secret_access_key=aws_secret_access_key,
            aws_access_key=aws_access_key,
        )
        self.aws_sqs_queue_name: str = aws_sqs_queue_name
        self.aws_region: str = aws_region
        self.queue_url: str = aws_queue_url

    def __str__(self) -> str:
        result = f"aws_client_name={self.aws_client_name}\n"
        result += f"aws_access_key={self.aws_access_key}\n"
        result += f"aws_secret_access_key={self.aws_secret_access_key}\n"
        result += f"aws_region={self.aws_region}\n"
        result += f"queue_url={self.queue_url}\n"
        result += f"aws_sqs_queue_name={self.aws_sqs_queue_name}"
        return result


class AWSCredentials_CognitoIDP(AWSCredentials):
    def __init__(
            self,
            aws_region: str,
            aws_cognito_pool_id: str,
            aws_cognito_client_id: str,
            aws_cognito_client_secret: str,
            aws_access_key: str = None,
            aws_secret_access_key: str = None,
    ):
        super(AWSCredentials_CognitoIDP, self).__init__(
            aws_client_name="cognito-idp",
            aws_access_key=aws_access_key,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.aws_region = aws_region
        self.aws_cognito_pool_id = aws_cognito_pool_id
        self.aws_cognito_client_id = aws_cognito_client_id
        self.aws_cognito_client_secret = aws_cognito_client_secret

    def __str__(self) -> str:
        result = f"aws_client_name={self.aws_client_name}\n"
        result += f"aws_access_key={self.aws_access_key}\n"
        result += f"aws_secret_access_key={self.aws_secret_access_key}\n"
        result += f"aws_region={self.aws_region}\n"
        result += f"aws_cognito_pool_id={self.aws_cognito_pool_id}\n"
        result += f"aws_cognito_client_id={self.aws_cognito_client_id}\n"
        result += f"aws_cognito_client_secret={self.aws_cognito_client_secret}"
        return result


class AWSCredentials_SecretsManager(AWSCredentials):
    def __init__(
            self,
            aws_region: str,
            secret_name: str,
            aws_access_key: str = None,
            aws_secret_access_key: str = None,
    ):
        super(AWSCredentials_SecretsManager, self).__init__(
            aws_client_name="secretsmanager",
            aws_access_key=aws_access_key,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.aws_region = aws_region
        self.secret_name = secret_name

    def __str__(self) -> str:
        result = f"aws_client_name={self.aws_client_name}\n"
        result += f"aws_access_key={self.aws_access_key}\n"
        result += f"aws_secret_access_key={self.aws_secret_access_key}\n"
        result += f"aws_region={self.aws_region}\n"
        result += f"secret_name={self.secret_name}"
        return result


class AWSCredentials_SES(AWSCredentials):
    def __init__(
            self,
            aws_region: str,
            aws_access_key: str = None,
            aws_secret_access_key: str = None,
    ):
        super(AWSCredentials_SES, self).__init__(
            aws_client_name="ses",
            aws_access_key=aws_access_key,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.aws_region = aws_region

    def __str__(self) -> str:
        result = f"aws_client_name={self.aws_client_name}\n"
        result += f"aws_access_key={self.aws_access_key}\n"
        result += f"aws_secret_access_key={self.aws_secret_access_key}\n"
        result += f"aws_region={self.aws_region}"
        return result


class AWSCredentials_SFN(AWSCredentials):
    def __init__(
            self,
            state_machine_arn: str,
            aws_region: str,
            aws_access_key: str = None,
            aws_secret_access_key: str = None,
    ):
        super(AWSCredentials_SFN, self).__init__(
            aws_client_name="sfn",
            aws_access_key=aws_access_key,
            aws_secret_access_key=aws_secret_access_key,
        )

        self.aws_region = aws_region
        self.state_machine_arn = state_machine_arn


class AWSCredentials_SageMaker(AWSCredentials):
    def __init__(self, aws_region: str,
                 aws_access_key: str = None,
                 aws_secret_access_key: str = None):
        super(AWSCredentials_SageMaker, self).__init__(aws_client_name='sagemaker',
                                                       aws_access_key=aws_access_key,
                                                       aws_secret_access_key=aws_secret_access_key)
        self.aws_region = aws_region

    def __str__(self) -> str:
        result = f"aws_client_name={self.aws_client_name}\n"
        result += f"aws_access_key={self.aws_access_key}\n"
        result += f"aws_secret_access_key={self.aws_secret_access_key}\n"
        result += f"aws_region={self.aws_region}"
        return result
