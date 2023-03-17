"""module image_s3_batch. Represents
a batch of images on S3

"""
import os
from typing import List, Any, Union, Callable
from navalmartin_mir_aws_utils.aws_credentials import AWSCredentials_S3
from navalmartin_mir_aws_utils.boto3_client import get_aws_s3_client
from navalmartin_mir_aws_utils.s3_utils import expand_s3_iterator_contents, expand_s3_iterator_common_prefixes

S3_URI = "s3://"

class FilePathBatch(object):

    def __init__(self, s3_credentials: AWSCredentials_S3, delimiter: str = '/',
                 do_build_client: bool = True):
        self.aws_bucket_credentials = s3_credentials
        self.files: List[Any] = []
        self.delimiter = delimiter
        self._current_pos: int = -1
        self._client: Any = None

        if do_build_client:
            self.build_client()

    def __len__(self):
        return len(self.files)

    def __iter__(self):
        self._current_pos = 0
        return self

    def __next__(self):
        if len(self.files) == 0:
            raise StopIteration

        if self._current_pos < len(self.files):
            result = self.files[self._current_pos]
            self._current_pos += 1
            return result
        else:
            self._current_pos = -1
            raise StopIteration

    def __getitem__(self, key: Union[int, str]) -> str:
        """Returns the image that corresponds to the given key

        Parameters
        ----------
        key

        Returns
        -------

        A string representing the image in the batch
        """
        if type(key) == int:

            if key >= len(self.files):
                raise ValueError(f"Invalid key. Integer key {key} cannot be >= {len(self.files)}")

            key = self.files[key]
            return key
        elif type(key) == str:
            if key not in self.files:
                raise ValueError(f"key={key} not in {self.files}")
            return key
        else:
            raise ValueError(f"key type {type(key)} is not valid")

    def reinit(self, s3_credentials: AWSCredentials_S3, delimiter: str = '/',
               do_build_client: bool = True):
        """Set the file batch to the state just after the constructor
        was called

        Parameters
        ----------
        s3_credentials
        delimiter
        do_build_client

        Returns
        -------

        """

        self.aws_bucket_credentials = s3_credentials
        self.files: List[Any] = []
        self.delimiter = delimiter
        self._current_pos: int = -1
        self._client: Any = None

        if do_build_client:
            self.build_client()

    def build_client(self) -> Any:
        """Build an S3 client from the given AWS S3 credentials

        Returns
        -------

        """
        self._client = get_aws_s3_client(credentials=self.aws_bucket_credentials)

    def load_from_list(self, files: List[str], delimiter="/"):
        self.files = files
        self.delimiter = delimiter

    def read_file_byte_string(self, key: Union[int, str],
                              read_from_local_host: bool = False,
                              file_reader: Callable = None) -> str:
        """Returns the byte string associated with the given key

        Parameters
        ----------
        file_reader
        read_from_local_host
        key: The key of the object to read

        Returns
        -------

        The byte string of the object that is represented by the
        given key

        """

        if read_from_local_host:
            image = self[key]
            return file_reader(image)

        file_obj = self.get_object(key=key)

        if 'Body' not in file_obj:
            raise ValueError("Body is missing from file object response")

        return file_obj['Body'].read()

    def read(self, prefixes: tuple, valid_image_extensions: tuple,
             delimiter: str = '/'):

        self.delimiter = delimiter

        # empty the files as we will read new ones
        self.files = []

        if self._client is None:
            self.build_client()

        # get the object that lists the objects
        # on S3
        paginator = self._client.get_paginator('list_objects')

        for prefix in prefixes:
            s3_iterator = paginator.paginate(Bucket=self.aws_bucket_credentials.aws_s3_bucket_name,
                                             Delimiter=self.delimiter,
                                             Prefix=prefix)

            contents = expand_s3_iterator_contents(s3_iterator)

            if len(contents) != 0:
                self.read_from_contents(contents=contents,
                                        valid_image_extensions=valid_image_extensions)

            common_prefixes = expand_s3_iterator_common_prefixes(s3_iterator=s3_iterator)
            if len(common_prefixes) != 0:
                self.read_from_common_prefixes(common_prefixes=common_prefixes,
                                               valid_image_extensions=valid_image_extensions)

    def copy_to(self, s3_credentials_to: AWSCredentials_S3) -> None:
        """Copy the images in the bucket to the S3 bucket specified
        by the provided credentials

        Parameters
        ----------
        s3_credentials_to: The credentials to use for the bucket to copy

        Returns
        -------

        """

        if len(self.files) == 0:
            print("WARNING: Image batch is empty...")
            return

        raise NotImplementedError("The function is not implemented")

    def copy_file_to(self, key: Union[int, str],
                     s3_credentials_to: AWSCredentials_S3,
                     new_filename: str = "",
                     **kwargs) -> dict:
        """Copies the specified file identified by the given key
        into the bucket specified in the given AWSCredentials_S3 credentials

        Parameters
        ----------
        key: The index of the file to copy to
        s3_credentials_to: Credentials for accessing the new bucket
        kwargs: Arguments to orchestrate how the copy is done

        Returns
        -------

        """

        item_to_copy = self[key]

        if new_filename == "":
            new_filename = item_to_copy

        if self._client is None:
            self.build_client()

        copy_source = self.aws_bucket_credentials.aws_s3_bucket_name + "/" + item_to_copy
        copy_response = self._client.copy_object(Bucket=s3_credentials_to.aws_s3_bucket_name,
                                                 Key=new_filename,
                                                 CopySource=copy_source,
                                                 **kwargs)
        return copy_response

    def get_object(self, key: Union[int, str]) -> Any:
        """Returns the object specified with the given key.

        Parameters
        ----------
        key: The key of the object to return

        Returns
        -------

        """

        if type(key) == int:

            if key >= len(self.files):
                raise ValueError(f"Invalid key. Integer key {key} cannot be >= {len(self.files)}")

            key = self.files[key]
        elif type(key) == str:
            if key not in self.files:
                raise ValueError(f"key={key} not in {self.files}")
        else:
            raise ValueError(f"key type {type(key)} is not valid")

        if self._client is None:
            raise ValueError("S3 client is not built")

        file_byte_string = self._client.get_object(Bucket=self.aws_bucket_credentials.aws_s3_bucket_name,
                                                   Key=key)

        return file_byte_string

    def read_from_contents(self, contents: List[dict], valid_image_extensions: tuple) -> None:
        """Read the contents of the S3 bucket

        Parameters
        ----------
        contents: The contents to use for reading the images
        valid_image_extensions: The valid_image_extensions to look for

        Returns
        -------

        """

        n_extensions = len(valid_image_extensions)
        for content in contents:

            image = content.get('Key')

            if n_extensions != 0:

                img_extension = os.path.splitext(image)[1]
                if img_extension in valid_image_extensions:
                    self.files.append(content.get('Key'))
            else:
                self.files.append(content.get('Key'))

    def read_from_common_prefixes(self, common_prefixes: List[dict],
                                  valid_image_extensions: tuple) -> None:
        """Read from the common_prefixes

        Parameters
        ----------
        common_prefixes: The common_prefixes to use for reading
        valid_image_extensions: The valid_image_extensions to look for

        Returns
        -------

        """

        if self._client is None:
            raise ValueError("S3 client is not built")

        paginator = self._client.get_paginator('list_objects')
        for item in common_prefixes:
            prefix = item['Prefix']

            s3_iterator = paginator.paginate(Bucket=self.aws_bucket_credentials.aws_s3_bucket_name,
                                             Delimiter=self.delimiter,
                                             Prefix=prefix)

            contents = expand_s3_iterator_contents(s3_iterator)
            self.read_from_contents(contents=contents,
                                    valid_image_extensions=valid_image_extensions)
