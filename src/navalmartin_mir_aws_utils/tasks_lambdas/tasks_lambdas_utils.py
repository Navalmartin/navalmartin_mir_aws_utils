import json
from typing import Any, Callable, Union, Dict
from navalmartin_mir_aws_utils import AWSCredentials_SecretsManager
from navalmartin_mir_aws_utils import get_aws_client_factory

OK = "OK"


def get_error_return(error: str) -> dict:
    return {'result': 'FAILED', 'error': error}


def get_success_return(success_msg: str = "OK") -> dict:
    return {'result': success_msg, 'error': []}


def get_secrets(credentials: AWSCredentials_SecretsManager) -> dict:
    """Returns a dictionary wiht the SecretString of the specified
    secrets manager
    """
    client = get_aws_client_factory(credentials=credentials)
    get_secret_value_response = client.get_secret_value(SecretId=credentials.secret_name)
    secret_string = get_secret_value_response['SecretString']
    secret_string = json.loads(secret_string)
    return secret_string


async def validate_sqs_event_record(event: dict,
                                    context: Any,
                                    db_writer: Callable = None) -> Union[Dict, str]:
    """Validate the event and write in the DB that monitors the errors

    Parameters
    ----------
    event: The event the lambda was called to validate
    db_writer: The writer to write in the DB
    context: The context the lambda was called

    Returns
    -------

    """
    if 'Records' not in event:
        print(f"No 'Records' was provided in the given event. Finishing task...")

        if db_writer is not None:
            await db_writer(error_type="GENERAL_SQS_MESSAGE_ERROR",
                            error_msg="No 'Records' was provided in the given event",
                            task_id=context.function_name,
                            lambda_arn=context.invoked_function_arn,
                            lambda_request_id=context.aws_request_id,
                            event=event)
        return get_error_return(error=f"No 'Records' was provided in the given event.")
    else:

        if len(event['Records']) == 0:
            print(f"'Records' attribute is empty in the provided event. Finishing task...")
            if db_writer is not None:
                await db_writer(error_type="GENERAL_SQS_MESSAGE_ERROR",
                                error_msg="'Records' attribute is empty in the provided event.",
                                task_id=context.function_name,
                                lambda_arn=context.invoked_function_arn,
                                lambda_request_id=context.aws_request_id,
                                event=event)
            return get_error_return(error=f"'Records' attribute is "
                                          f"empty in the provided event.")

        if 'body' not in event['Records'][0]:
            print(f"'Records' attribute does not have 'body' attribute "
                  f"in the provided event. Finishing task...")

            if db_writer is not None:
                await db_writer(error_type="GENERAL_SQS_MESSAGE_ERROR",
                                error_msg="'Records' attribute does not have 'body' "
                                          "attribute in the provided event.",
                                task_id=context.function_name,
                                lambda_arn=context.invoked_function_arn,
                                lambda_request_id=context.aws_request_id,
                                event=event)

            return get_error_return(error=f"'Records' attribute does not "
                                          f"have 'body' attribute in the provided event.")

        if 'receiptHandle' not in event['Records'][0]:
            print(f"'Records' attribute does not have 'receiptHandle' "
                  f"attribute in the provided event.")
            if db_writer is not None:
                await db_writer(error_type="GENERAL_SQS_MESSAGE_ERROR",
                                error_msg="'Records' attribute does not have 'receiptHandle' "
                                                           "attribute in the provided event.",
                                task_id=context.function_name,
                                lambda_arn=context.invoked_function_arn,
                                lambda_request_id=context.aws_request_id,
                                event=event)
            return get_error_return(error=f"'Records' attribute does not have 'receiptHandle' "
                                          f"attribute in the provided event.")

        return OK
