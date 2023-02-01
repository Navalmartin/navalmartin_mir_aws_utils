from typing import Any, List


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
