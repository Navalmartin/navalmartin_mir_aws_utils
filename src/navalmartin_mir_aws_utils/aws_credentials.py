"""module aws_credentials. Utility class to move around
credentials. This class is not used to load the
credentials. It is the application's duty to do so

"""


class AWSCredentials(object):
    def __init__(self, aws_client_name: str = None,
                 aws_access_key: str = None,
                 aws_secret_access_key: str = None):
        self.aws_client_name: str = aws_client_name
        self.aws_access_key: str = aws_access_key
        self.aws_secret_access_key = aws_secret_access_key


class AWSCredentials_S3(AWSCredentials):
    def __init__(self, aws_s3_bucket_name: str, aws_region: str,
                 aws_access_key: str, aws_secret_access_key: str):
        super(AWSCredentials_S3, self).__init__(aws_client_name='s3',
                                                aws_secret_access_key=aws_secret_access_key,
                                                aws_access_key=aws_access_key)
        self.aws_s3_bucket_name = aws_s3_bucket_name
        self.aws_region = aws_region


class AWSCredentials_SQS(AWSCredentials):
    def __init__(self, aws_sqs_queue_name: str, aws_region: str,
                 aws_access_key: str, aws_secret_access_key: str,
                 aws_queue_url: str):
        super(AWSCredentials_SQS, self).__init__(aws_client_name='sqs',
                                                 aws_secret_access_key=aws_secret_access_key,
                                                 aws_access_key=aws_access_key)
        self.aws_sqs_queue_name: str = aws_sqs_queue_name
        self.aws_region: str = aws_region
        self.queue_url: str = aws_queue_url


class AWSCredentials_CognitoIDP(AWSCredentials):
    def __init__(self, aws_region: str,
                 aws_cognito_pool_id: str,
                 aws_cognito_client_id: str,
                 aws_cognito_client_secret: str,
                 aws_access_key: str, aws_secret_access_key: str):
        super(AWSCredentials_CognitoIDP, self).__init__(aws_client_name="cognito-idp",
                                                        aws_access_key=aws_access_key,
                                                        aws_secret_access_key=aws_secret_access_key)
        self.aws_region = aws_region
        self.aws_cognito_pool_id = aws_cognito_pool_id
        self.aws_cognito_client_id = aws_cognito_client_id
        self.aws_cognito_client_secret = aws_cognito_client_secret


class AWSCredentials_SecretsManager(AWSCredentials):
    def __init__(self, aws_region: str,
                 secret_name: str,
                 aws_access_key: str = None,
                 aws_secret_access_key: str = None):
        super(AWSCredentials_SecretsManager, self).__init__(aws_client_name="secretsmanager",
                                                            aws_access_key=aws_access_key,
                                                            aws_secret_access_key=aws_secret_access_key)
        self.aws_region = aws_region
        self.secret_name = secret_name

