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

