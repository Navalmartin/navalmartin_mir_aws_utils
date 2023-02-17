# navalmartin_mir_aws_utils

Various utilities for working with AWS in Python. The official
PyPi package can be found <a href="https://pypi.org/project/navalmartin-mir-aws-utils/">here</a>.


## Dependencies

- boto3

## Installation

Installing the utilities via ```pip```

```
pip install navalmartin-mir-aws-utils
```

For a specific version you can use

```
pip install navalmartin-mir-aws-utils==x.x.x
```

You can uninstall the project via

```
pip uninstall navalmartin_mir_aws_utils
```

## How to use

### Signup/signout AWS Cognito

```
from navalmartin_mir_aws_utils.aws_credentials import AWSCredentials_CognitoIDP
from navalmartin_mir_aws_utils.cognito_idp_utils import (global_signout_user_from_pool,
                                                         authenticate_and_get_token_for_user)
from navalmartin_mir_aws_utils.utils import AWSCognitoSignInUserData

AWS_REGION = ""
AWS_COGNITO_POOL_ID = ""
AWS_COGNITO_CLIENT_ID = ""
AWS_COGNITO_CLIENT_SECRET = ""

if __name__ == '__main__':
    user_data = AWSCognitoSignInUserData(username="",
                                         password="")

    aws_credentials = AWSCredentials_CognitoIDP(aws_region=AWS_REGION,
                                                aws_cognito_pool_id=AWS_COGNITO_POOL_ID,
                                                aws_cognito_client_id=AWS_COGNITO_CLIENT_ID,
                                                aws_cognito_client_secret=AWS_COGNITO_CLIENT_SECRET,
                                                aws_access_key=None, aws_secret_access_key=None)

    response = authenticate_and_get_token_for_user(aws_cognito_credentials=aws_credentials,
                                                   user_data=user_data)

    access_token = response["AuthenticationResult"]["AccessToken"]
    print(f"Access token {access_token}")

    response = global_signout_user_from_pool(access_token=access_token,
                                             credentials=aws_credentials)

    print(f"Revoke response {response}")

```

### Create an ```ImageBatch```

```
from navalmartin_mir_aws_utils.image_s3_batch import ImagePathBatch
from navalmartin_mir_aws_utils.aws_credentials import AWSCredentials_S3

AWS_REGION = "YOUR_AWS_REGION"
AWS_S3_BUCKET_NAME = "YOUR_AWS_S3_BUCKET_NAME"
AWS_ACCESS_KEY = "YOUR_AWS_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY"
IMAGE_STR_TYPES = ('.jpg', '.png')

if __name__ == '__main__':
    aws_s3_credentials = AWSCredentials_S3(aws_s3_bucket_name=AWS_S3_BUCKET_NAME,
                                           aws_region=AWS_REGION,
                                           aws_access_key=AWS_ACCESS_KEY,
                                           aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    image_prefix = 'some/image/prefix/'
    image_batch = ImagePathBatch(s3_credentials=aws_s3_credentials)

    # read the images
    image_batch.read(image_prefixes=(image_prefix,),
                     valid_image_extensions=IMAGE_STR_TYPES,
                     delimiter='/')

    for image_file in image_batch:
        print(image_file)
```

### Message an SQS queue

Send a message to an SQS queue

```
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
```




