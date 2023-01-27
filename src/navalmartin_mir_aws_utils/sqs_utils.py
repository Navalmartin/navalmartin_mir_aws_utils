from navalmartin_mir_aws_utils.aws_credentials import AWSCredentials_SQS
from navalmartin_mir_aws_utils.boto3_client import get_aws_sqs_client
from navalmartin_mir_aws_utils.sqs_queue_config import SQSMessageConfig


def send_sqs_message(sqs_credentials: AWSCredentials_SQS,
                     sqs_msg: SQSMessageConfig) -> dict:
    """

    :param sqs_credentials:
    :param sqs_msg:
    :return:
    """
    sqs_client = get_aws_sqs_client(credentials=sqs_credentials)
    response: dict = sqs_client.send_message(QueueUrl=sqs_credentials.queue_url,
                                             MessageBody=sqs_msg.message_body,
                                             DelaySeconds=sqs_msg.delay_seconds,
                                             MessageAttributes=sqs_msg.message_attributes if sqs_msg.message_attributes is not None else {},
                                             MessageGroupId=sqs_msg.message_group_id)
    return response

