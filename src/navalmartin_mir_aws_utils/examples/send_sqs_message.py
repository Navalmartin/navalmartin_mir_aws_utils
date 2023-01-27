from navalmartin_mir_aws_utils.aws_credentials import AWSCredentials_SQS
from navalmartin_mir_aws_utils.sqs_queue_config import SQSMessageConfig
from navalmartin_mir_aws_utils.sqs_utils import send_sqs_message

AWS_REGION = "YOUR_AWS_REGION"
AWS_S3_BUCKET_NAME = "YOUR_AWS_S3_BUCKET_NAME"
AWS_ACCESS_KEY = "YOUR_AWS_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY"
AWS_SQS_URL = "YOUR_AWS_SQS_URL"
AWS_SQS_NAME = "YOUR_AWS_SQS_NAME"
AWS_SQS_GROUP_ID = "YOUR_AWS_SQS_GROUP_ID"

if __name__ == '__main__':
    aws_sqs_credentials = AWSCredentials_SQS(aws_sqs_queue_name=AWS_SQS_NAME,
                                             aws_queue_url=AWS_SQS_URL,
                                             aws_region=AWS_REGION,
                                             aws_access_key=AWS_ACCESS_KEY,
                                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    sqs_msg = SQSMessageConfig(message_body="Test AWS  SQS msg",
                               message_group_id=AWS_SQS_GROUP_ID,
                               message_attributes=None)

    response = send_sqs_message(sqs_credentials=aws_sqs_credentials,
                                sqs_msg=sqs_msg)

    print(response)
