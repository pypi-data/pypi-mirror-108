import hashlib
from datetime import datetime
from typing import Optional, Union, Dict, List
from urllib.parse import urlparse, parse_qs

import requests

from koodous.exceptions import PackageInvalidFormatException


def package_param(package: Optional[Union[str, datetime]]) -> str:
    """Validate and create the package parameter.

    Using the datetime object you can't specify a hourly package because the datetime minute is 0 when it is not
    set.

    :param package: package parameter.
    :return: package string to the request.
    """
    if isinstance(package, datetime):
        return package.strftime('%Y%m%dT%H%M')
    elif isinstance(package, str):
        return package  # TODO: Check that the string is valid.
    else:
        raise PackageInvalidFormatException('The package type is not valid. See the api docs.')


def sha256sum(file_path: str) -> str:
    """Calculate the file sha256.

    :param file_path: path to the file.
    :return: file checksum (sha256).
    """
    h = hashlib.sha256()
    b = bytearray(128*1024)
    mv = memoryview(b)
    with open(file_path, 'rb', buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def extract_url_parameters(url: str) -> Dict[str, List[str]]:
    """Extract the query parameters from a url string.

    :param url: the url string.
    :return: the dictionary with the query parameters.
    """
    url_parsed = urlparse(url)
    qs_parsed = parse_qs(url_parsed.query)
    return qs_parsed


def request_download(download_url: str, output_filepath: str, chunk_size: int = 8192, **kwargs) -> None:
    """Request to download a file from a url.

    This method use a simple ``GET`` request without any pre-defined headers or parameters.

    :param download_url: download url.
    :param output_filepath: full path to the write the file.
    :param chunk_size: chunk size.
    :param kwargs: kwargs to be included in the GET request.
    :return: None.
    """
    with requests.get(download_url, stream=True, **kwargs) as r:
        r.raise_for_status()
        with open(output_filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
