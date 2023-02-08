from navalmartin_mir_aws_utils.aws_credentials import AWSCredentials_SQS
from navalmartin_mir_aws_utils.sqs_queue_config import SQSMessageConfig
from navalmartin_mir_aws_utils.sqs_utils import send_sqs_message, read_one_sqs_message, delete_sqs_message

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

    message = "task_id:123"
    sqs_msg = SQSMessageConfig(message_body=message,
                               message_group_id=AWS_SQS_GROUP_ID,
                               message_attributes=None,
                               message_deduplication_id="123")

    response = send_sqs_message(sqs_credentials=aws_sqs_credentials,
                                sqs_msg=sqs_msg)

    print(response)

    read_response = read_one_sqs_message(aws_sqs_credentials)
    print(read_response)

    receipt_handle = read_response['Messages'][0]['ReceiptHandle']
    # get the receipt handler to delete the message
    # this signals that the message has been consumed
    delete_response = delete_sqs_message(aws_sqs_credentials, receipt_handle=receipt_handle)
    print(delete_response)
