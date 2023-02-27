from typing import Any, List
from navalmartin_mir_aws_utils.aws_credentials import AWSCredentials_S3
from navalmartin_mir_aws_utils.boto3_client import get_aws_s3_client


def get_s3_iterator(s3_client: Any, prefix: str,
                    aws_creds: AWSCredentials_S3, delimiter="/") -> Any:
    paginator = s3_client.get_paginator('list_objects')
    return paginator.paginate(Bucket=aws_creds.aws_s3_bucket_name,
                              Delimiter=delimiter,
                              Prefix=prefix)


def expand_s3_iterator_contents(s3_iterator: Any) -> List[dict]:
    """Get the contents of the provided S3 iterator

    Parameters
    ----------
    s3_iterator: The S3 iterator

    Returns
    -------
    A list of dictionaries
    """

    contents = s3_iterator.search('Contents')
    return [item for item in contents if item is not None]


def expand_s3_iterator_common_prefixes(s3_iterator: Any) -> List[dict]:
    """Get the common prefixes from the iterator

    Parameters
    ----------
    s3_iterator: The S3 iterator

    Returns
    -------
    A list of dictionaries
    """
    contents = s3_iterator.search('CommonPrefixes')
    return [item for item in contents if item is not None]


def delete_s3_all_objs_with_key(keys: List[dict],
                                s3_client: Any,
                                aws_creds: AWSCredentials_S3,
                                **options) -> dict:
    """Delete all the objects on S3 with the given key.

    Parameters
    ----------
    keys: The prefix of the objects
    s3_client: The S3 client the objects sit on
    aws_creds: The credentials to use to create an
    S3 client: if the user provided if None an s3 client is built
    options: Options to pass in the boto3 API call. Currently, the following
    options are used quiet: True | False

    Returns
    -------

    A dictionary with the response of the operation
    """

    if keys is None or len(keys) == 0:
        raise ValueError("Invalid key given")

    if aws_creds is None:
        raise ValueError("AWS credentials not given")

    if s3_client is None:
        s3_client = get_aws_s3_client(credentials=aws_creds)

    delete_dict = {
        'Objects': keys,
        'Quiet': True if 'quiet' in options else False
    }
    response = s3_client.delete_objects(Bucket=aws_creds.aws_s3_bucket_name,
                                        Delete=delete_dict)

    return response


def delete_s3_object_with_key(key: str, s3_client: Any,
                              aws_creds: AWSCredentials_S3,
                              **options) -> dict:
    if key is None or key == "":
        raise ValueError("Invalid key given")

    if aws_creds is None:
        raise ValueError("AWS credentials not given")

    if s3_client is None:
        s3_client = get_aws_s3_client(credentials=aws_creds)

    if 'version_id' in options:
        version_id = options['version_id']
        response = s3_client.delete_object(Bucket=aws_creds.aws_s3_bucket_name,
                                           Key=key, VersionId=version_id)
    else:
        response = s3_client.delete_object(Bucket=aws_creds.aws_s3_bucket_name,
                                           Key=key)

    return response
