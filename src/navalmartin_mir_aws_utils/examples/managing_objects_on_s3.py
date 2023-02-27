from navalmartin_mir_aws_utils.aws_credentials import AWSCredentials_S3
from navalmartin_mir_aws_utils.s3_utils import delete_s3_all_objs_with_key, delete_s3_object_with_key

AWS_REGION = "YOUR_AWS_REGION"
AWS_S3_BUCKET_NAME = "YOUR_AWS_S3_BUCKET_NAME"
AWS_ACCESS_KEY = "YOUR_AWS_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY"

if __name__ == '__main__':
    # credentials so that we can access S3
    aws_s3_credentials = AWSCredentials_S3(aws_s3_bucket_name=AWS_S3_BUCKET_NAME,
                                           aws_region=AWS_REGION,
                                           aws_access_key=AWS_ACCESS_KEY,
                                           aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    print("---------Deleting one object")

    # delete an object from S3
    key = "63b5bc8cc5f1cdcad7ef54e7/2/2/img_1.jpeg"
    delete_response = delete_s3_object_with_key(key=key, s3_client=None, aws_creds=aws_s3_credentials)

    print(delete_response)
    print("---------Deleting multiple objects")
    keys = [{'Key': '63b5bc8cc5f1cdcad7ef54e7/2/2/img_2.jpeg'},
            {'Key': '63b5bc8cc5f1cdcad7ef54e7/2/2/img_3.jpeg'}]
    delete_response = delete_s3_all_objs_with_key(keys=keys, s3_client=None,
                                                  aws_creds=aws_s3_credentials)
    print(delete_response)
