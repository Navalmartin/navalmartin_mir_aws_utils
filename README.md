# navalmartin_mir_aws_utils

Various utilities for working with AWS in Python. The official
PyPi package can be found <a href="https://pypi.org/project/navalmartin-mir-aws-utils/">here</a>.
This package is basically wrappers on top of boto3 that allows for easier development with AWS.


## Dependencies

- boto3
- pydantic
- pydantic[email]

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
pip uninstall navalmartin-mir-aws-utils
```

## How to use

Below are several examples of using the provided utilities. In general, for the examples to
work you need to install AWS CLI and configure it with your credentials.

You can check which specific version you have installed by

```
import navalmartin_mir_aws_utils
print(navalmartin_mir_aws_utils.__version__)
```

### Signup/signout AWS Cognito

```
from navalmartin_mir_aws_utils import AWSCredentials_CognitoIDP
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

### Work with S3

Deleting objects with specific key

```
from navalmartin_mir_aws_utils.aws_credentials import AWSCredentials_S3
from navalmartin_mir_aws_utils.s3_utils import delete_all_objs_with_key

AWS_REGION = "YOUR_AWS_REGION"
AWS_S3_BUCKET_NAME = "YOUR_AWS_S3_BUCKET_NAME"
AWS_ACCESS_KEY = "YOUR_AWS_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY"

if __name__ == '__main__':
    aws_s3_credentials = AWSCredentials_S3(aws_s3_bucket_name=AWS_S3_BUCKET_NAME,
                                           aws_region=AWS_REGION,
                                           aws_access_key=AWS_ACCESS_KEY,
                                           aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    key = "63b5bc8cc5f1cdcad7ef54e7/"

    delete_response = delete_all_objs_with_key(key=key,
                                               aws_creds=aws_s3_credentials)
    print(delete_response)
```

### Create an ```FilePathBatch```

The utilities allow you to create batches of files and read these files sequentially. The class ```FilePathBatch```
attempts to do most of the common chores needed

```
from pathlib import Path
from navalmartin_mir_aws_utils import FilePathBatch
from navalmartin_mir_aws_utils import AWSCredentials_S3

AWS_REGION = "YOUR_AWS_REGION"
AWS_S3_BUCKET_NAME = "YOUR_AWS_S3_BUCKET_NAME"
AWS_ACCESS_KEY = "YOUR_AWS_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY"
IMAGE_STR_TYPES = ('.jpg', '.png', '.jpeg')

def read_pil_image_to_byte_string(image_path: Path):
    try:
        import PIL
        from PIL import Image
        import io

        image = Image.open(image_path)
        img_byte_arr = io.BytesIO()
        # image.save expects a file-like as a argument
        image.save(img_byte_arr, format=image.format)
        # Turn the BytesIO object back into a bytes object
        imgByteArr = img_byte_arr.getvalue()
        return imgByteArr
    except ModuleNotFoundError as e:
        print(f"ERROR: This example needs module {str(e)}")
    except PIL.UnidentifiedImageError as e:
        print(f"ERROR: This does not look like an image file. {str(e)}")
    except Exception as e:
        print(f"{str(e)}")

if __name__ == '__main__':
    aws_s3_credentials = AWSCredentials_S3(aws_s3_bucket_name=AWS_S3_BUCKET_NAME,
                                           aws_region=AWS_REGION,
                                           aws_access_key=AWS_ACCESS_KEY,
                                           aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    image_batch = FilePathBatch(s3_credentials=aws_s3_credentials,
                                do_build_client=False)

    # set the files from localhost
    image_batch.load_from_list(files=['/home/alex/qi3/mir_lambda_tasks/test_images/img_7_8.jpg',
                                      '/home/alex/qi3/mir_lambda_tasks/test_images/img_7_3.jpg',
                                      '/home/alex/qi3/mir_lambda_tasks/test_images/not_an_image.txt',
                                      '/home/alex/qi3/mir_lambda_tasks/test_images/not_an_image.png'])

    print(f"Number of files in batch {len(image_batch)}")
    print(f"The 2nd file is {image_batch[2]}")

    # read the image...
    image_byte = image_batch.read_file_byte_string(key=1, read_from_local_host=True,
                                                   file_reader=read_pil_image_to_byte_string)

    # read the image...this is not an image
    image_byte = image_batch.read_file_byte_string(key=2, read_from_local_host=True,
                                                   file_reader=read_pil_image_to_byte_string)

    # read the image...this is not an image
    image_byte = image_batch.read_file_byte_string(key=3, read_from_local_host=True,
                                                   file_reader=read_pil_image_to_byte_string)

    # read the images
    file_prefix = "YOUR-PREFIX"
    image_batch.read(prefixes=(file_prefix,),
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


### Using SecretsManager

Belowe the required credentials are accessed via what you have entered when you configured AWS CLI
on your machine.

```
from botocore.exceptions import ClientError
from navalmartin_mir_aws_utils import get_aws_client_factory, AWSCredentials_SecretsManager

AWS_SECRET_NAME = "YOUR-AWS-Secrets-Manager"
AWS_REGION = "YOUR-AWS-REGION"

if __name__ == '__main__':

    try:
        credentials = AWSCredentials_SecretsManager(aws_region=AWS_REGION,
                                                    secret_name=AWS_SECRET_NAME)
        client = get_aws_client_factory(credentials=credentials)

        get_secret_value_response = client.get_secret_value(SecretId=credentials.secret_name)
        print(get_secret_value_response)
    except ClientError as e:
        print(str(e))
```

### Using SES

SES is a simple email service that we  can use to send marketing emails such as special offers, 
transactional emails such as order confirmations, and other types of correspondence such as newsletters. 
You can find more details <a herf="https://docs.aws.amazon.com/ses/latest/dg/Welcome.html">here</a>.

```
from pydantic import EmailStr
from navalmartin_mir_aws_utils import AWSCredentials_SES
from navalmartin_mir_aws_utils.tasks import send_simple_email
from navalmartin_mir_aws_utils.utils import Email, EmailSubject, EmailBody


if __name__ == '__main__':

    credentials = AWSCredentials_SES(aws_region="eu-west-2")
    email = Email(source=EmailStr("some_email@provider.com"),
                  destination=EmailStr("some_email@provider.com"),
                  subject=EmailSubject(data="First notification from mir"),
                  body=EmailBody(data="This your first AWS SES notification from mir. Expect more"),
                  reply_to=EmailStr("alex@navalmartin.com"))

    print(email.dict())
    response = send_simple_email(email=email, credentials=credentials)
    print(response)
```

Note that for the code above to work, you need to have a registered email address with AWS. Also,
the email you have registered will be initially in a sandbox therefore you won't be able to actually
send emails to others unless the destination email is also a verified email with AWS.





