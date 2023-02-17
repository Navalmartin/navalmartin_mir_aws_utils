from navalmartin_mir_aws_utils.image_s3_batch import ImagePathBatch
from navalmartin_mir_aws_utils.aws_credentials import AWSCredentials_S3

AWS_REGION = "YOUR_AWS_REGION"
AWS_S3_BUCKET_NAME = "YOUR_AWS_S3_BUCKET_NAME"
AWS_ACCESS_KEY = "YOUR_AWS_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY"
IMAGE_STR_TYPES = ('.jpg', '.png', '.jpeg')
MONGO_DB_URL = ""

if __name__ == '__main__':
    aws_s3_credentials = AWSCredentials_S3(aws_s3_bucket_name=AWS_S3_BUCKET_NAME,
                                           aws_region=AWS_REGION,
                                           aws_access_key=AWS_ACCESS_KEY,
                                           aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    image_prefix = "63b5bc8cc5f1cdcad7ef54e7/2/" #'some/image/prefix/'
    image_batch = ImagePathBatch(s3_credentials=aws_s3_credentials)

    # read the images
    image_batch.read(prefixes=(image_prefix,),
                     valid_image_extensions=IMAGE_STR_TYPES,
                     delimiter='/')

    for image_file in image_batch:
        print(image_file)
