from typing import Any
from navalmartin_mir_aws_utils.aws_credentials import AWSCredentials_SQS
from navalmartin_mir_aws_utils.boto3_client import get_aws_sqs_client
from navalmartin_mir_aws_utils.sqs_queue_config import SQSMessageConfig


def send_sqs_message(sqs_credentials: AWSCredentials_SQS,
                     sqs_msg: SQSMessageConfig, sqs_client: Any = None) -> dict:
    """Send a message to the SQS queue specified
    under the sqs credentials

    Parameters
    ----------
    sqs_credentials: The credentials to use to send the message
    sqs_msg: The message configuration

    Returns
    -------
    A dictionary with the response attributes
    """

    if sqs_client is not None:
        response = sqs_client.send_message(QueueUrl=sqs_credentials.queue_url,
                                           MessageBody=sqs_msg.message_body,
                                           # DelaySeconds=sqs_msg.delay_seconds,
                                           MessageAttributes=sqs_msg.message_attributes if sqs_msg.message_attributes is not None else {},
                                           MessageGroupId=sqs_msg.message_group_id,
                                           MessageDeduplicationId=sqs_msg.message_deduplication_id)
        return response

    new_sqs_client = get_aws_sqs_client(credentials=sqs_credentials)
    response: dict = new_sqs_client.send_message(QueueUrl=sqs_credentials.queue_url,
                                                 MessageBody=sqs_msg.message_body,
                                                 # DelaySeconds=sqs_msg.delay_seconds,
                                                 MessageAttributes=sqs_msg.message_attributes if sqs_msg.message_attributes is not None else {},
                                                 MessageGroupId=sqs_msg.message_group_id,
                                                 MessageDeduplicationId=sqs_msg.message_deduplication_id)
    return response


def read_one_sqs_message(sqs_credentials: AWSCredentials_SQS,
                         sqs_client: Any = None) -> dict:
    """

    Parameters
    ----------
    sqs_client: The SQS client to use for the operation
    sqs_credentials: The credentials to use for the queue

    Returns
    -------

    A dictionary of the response
    """

    if sqs_client is not None:
        response = sqs_client.receive_message(QueueUrl=sqs_credentials.queue_url,
                                              MaxNumberOfMessages=1)
        return response

    new_sqs_client = get_aws_sqs_client(credentials=sqs_credentials)
    response = new_sqs_client.receive_message(QueueUrl=sqs_credentials.queue_url,
                                              MaxNumberOfMessages=1)

    return response


def delete_sqs_message(sqs_credentials: AWSCredentials_SQS, receipt_handle: str,
                       sqs_client: Any = None) -> dict:
    """Deletes the message from the queue

    Parameters
    ----------
    sqs_client: The SQS client to use for the operation
    sqs_credentials: The credentials to use for the queue
    receipt_handle: This is the handle received when receiving the message

    Returns
    -------

    """

    if sqs_client is not None:
        response = sqs_client.delete_message(QueueUrl=sqs_credentials.queue_url,
                                             ReceiptHandle=receipt_handle)
        return response

    new_sqs_client = get_aws_sqs_client(credentials=sqs_credentials)
    response = new_sqs_client.delete_message(QueueUrl=sqs_credentials.queue_url,
                                             ReceiptHandle=receipt_handle)
    return response
