from navalmartin_mir_aws_utils import AWSCredentials_SFN
from navalmartin_mir_aws_utils.boto3_client import get_aws_sfn_client


def start_sfn_execution(aws_sfn_credentials: AWSCredentials_SFN,
                        sfn_input: str,
                        **kwargs) -> dict:
    """Starts the execution of the state machine
    specified by the ARN in the provided AWSCredentials_SFN credentials.
    See here https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/client/start_execution.html
    on how to specify the sfn_input. This must be given even if
    no input is required

    Parameters
    ----------

    aws_sfn_credentials: AWS credentials to access the
    sfn_input: The input to start the execution

    Returns
    -------

    A dictionary with the response of t
    """

    if "stateMachineArn" in kwargs:
        raise ValueError("stateMachineArn should not be specified in kwargs")

    if "input" in kwargs:
        raise ValueError("stateMachineArn should not be specified in kwargs")

    sfn_client = get_aws_sfn_client(credentials=aws_sfn_credentials)
    return sfn_client.start_execution(stateMachineArn=aws_sfn_credentials.state_machine_arn,
                                      input=sfn_input,
                                      **kwargs)
