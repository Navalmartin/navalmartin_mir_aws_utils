"""module image_s3_batch. Represents
a batch of images on S3

"""
import os
from typing import List
from navalmartin_mir_aws_utils.aws_credentials import AWSCredentials_S3
from navalmartin_mir_aws_utils.boto3_client import get_aws_s3_client


class ImagePathBatch(object):
    def __init__(self, s3_credentials: AWSCredentials_S3):
        self.aws_bucket_credentials = s3_credentials
        self.images: List[dict] = []
        self._current_pos: int = -1

    def read(self, image_prefixes: tuple, valid_image_extensions: tuple,
             delimiter: str = '/'):

        client = get_aws_s3_client(credentials=self.aws_bucket_credentials)

        n_extensions = len(valid_image_extensions)

        # get the object that lists the objects
        # on S3
        paginator = client.get_paginator('list_objects')

        for prefix in image_prefixes:
            s3_iterator = paginator.paginate(Bucket=self.aws_bucket_credentials.aws_s3_bucket_name,
                                             Delimiter=delimiter,
                                             Prefix=prefix)

            for content in s3_iterator.search('Contents'):

                image = content.get('Key')

                if n_extensions != 0:

                    img_extension = os.path.splitext(image)[1]
                    if img_extension in valid_image_extensions:
                        self.images.append({'img': content.get('Key'),
                                            'bucket': self.aws_bucket_credentials.aws_s3_bucket_name})
                else:
                    self.images.append({'img': content.get('Key'),
                                        'bucket': self.aws_bucket_credentials.aws_s3_bucket_name})

    def copy_to(self, s3_credentials_to: AWSCredentials_S3):
        raise NotImplementedError("The function is not implemented")

    def __len__(self):
        return len(self.images)

    def __iter__(self):
        self._current_pos = 0
        return self

    def __next__(self):
        if len(self.images) == 0:
            raise StopIteration

        if self._current_pos < len(self.images):
            result = self.images[self._current_pos]
            self._current_pos += 1
            return result
        else:
            self._current_pos = -1
            raise StopIteration
