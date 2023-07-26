from navalmartin_mir_aws_utils.aws_credentials import AWSCredentials_S3
from navalmartin_mir_aws_utils import (
    delete_s3_all_objs_with_key,
    delete_s3_object_with_key,
    generate_presigned_url
)

AWS_REGION = "YOUR-AWS-REGION"
AWS_S3_BUCKET_NAME = "YOUR-AWS-BUCKET-NAME"

if __name__ == "__main__":

    # credentials so that we can access S3
    aws_s3_credentials = AWSCredentials_S3(
        aws_s3_bucket_name=AWS_S3_BUCKET_NAME,
        aws_region=AWS_REGION
    )

    print("---------Deleting one object")

    # delete an object from S3
    key = "your-key-to-delete"
    delete_response = delete_s3_object_with_key(
        key=key, s3_client=None, aws_creds=aws_s3_credentials
    )

    print(delete_response)
    print("---------Deleting multiple objects")
    keys = [
        {"Key": "key-1-to-delete"},
        {"Key": "key-2-to-delete"},
    ]
    delete_response = delete_s3_all_objs_with_key(
        keys=keys, s3_client=None, aws_creds=aws_s3_credentials
    )
    print(delete_response)

    key = "your-key-to-access"
    response = generate_presigned_url(aws_creds=aws_s3_credentials,
                                      object_name=key,
                                      client_method_name='get_object',
                                      expiration=4600)
    print(response)
