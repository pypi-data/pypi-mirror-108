"""Koodous API class."""
import os
from http import HTTPStatus
from io import BytesIO
from itertools import count
from typing import Optional, Union, Iterator, Dict, Any
from datetime import datetime

import requests

from koodous.constants import KOODOUS_API_URL, KOODOUS_API_ENDPOINTS
from koodous.exceptions import ApiUnauthorizedException, FeedPackageException, ApkNotFound
from koodous.feed import ApksFeed, AnalysesFeed
from koodous.representations.apk import Apk
from koodous.representations.comment import Comment
from koodous.utils import package_param, sha256sum, extract_url_parameters, request_download


class ApiBase:
    """Main class to interact with the different Koodous modules apis.
    """
    api_url: str
    api_endpoints: Dict[str, str]

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Internal method to do the requests and handle possible exceptions.

        :param method: HTTP method : ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
        :param endpoint: endpoint of the Koodous API.
        :param kwargs: dictionary with the arguments to the request.
        :return: the response object.
        """
        r = requests.request(method, self.api_url + endpoint, **kwargs)
        return r

    def _iterator_cursor_pagination(self, endpoint: str, params: Optional[dict] = None, **kwargs) -> Iterator[Any]:
        """Iterator over endpoints with cursor pagination.

        :param endpoint: endpoint.
        :param params: request query parameters.
        :param kwargs: dictionary with the arguments to the request.
        :return: iterator over the results data.
        """
        # Check if the params is None.
        params = params or {}
        # Iterate over the cursor pages.
        next_cursor = ''
        while next_cursor is not None:
            r_params = {
                'cursor': next_cursor,
                **params
            }
            r = self.request('GET', endpoint, params=r_params, **kwargs)
            # Check the response status code.
            r.raise_for_status()
            # Get the response and yield every apk, when it finish, go to the next cursor (page).
            response_json = r.json()
            yield from response_json['results']
            # Extract the next cursor from the fully url.
            next_cursor_url = response_json['next']
            if next_cursor_url:
                next_cursor = extract_url_parameters(next_cursor_url)['cursor'][0]
            else:
                next_cursor = None

    def _iterator_page_pagination(self, endpoint: str, params: Optional[dict] = None, **kwargs):
        """Iterator over endpoints with page pagination.

        :param endpoint: endpoint.
        :param params: request query parameters.
        :param kwargs: dictionary with the arguments to the request.
        :return: iterator over the results data.
        """
        # Check if the params is None.
        params = params or {}
        # Iterate over the pages.
        for page in count(1):
            r_params = {
                'page': page,
                **params
            }
            r = self.request('GET', endpoint, params=r_params, **kwargs)
            # Check the response status code.
            r.raise_for_status()
            # Get the response and yield every apk, when it finish, go to the next cursor (page).
            response_json = r.json()
            yield from response_json['results']
            # Return None when it's the last page.
            if response_json['next'] is None:
                return


class ApiWithTokenBase(ApiBase):
    """Proxy class to use the apis that needs token authentication.
    """

    def __init__(self, token: str, *args, **kwargs):
        """

        :param token: authentication token.
        """
        super(ApiWithTokenBase, self).__init__(*args, **kwargs)
        self.token = token

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Internal method to do the requests and handle possible exceptions.

        :param method: HTTP method : ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
        :param endpoint: endpoint of the Koodous API.
        :param kwargs: dictionary with the arguments to the request.
        :return: the response object.
        """
        # Update or add the headers to the request kwargs.
        headers = kwargs.get('headers', {})
        headers.update({'Authorization': f'Token {self.token}'})
        kwargs.update({'headers': headers})
        # Do the request and handle exceptions.
        r = super(ApiWithTokenBase, self).request(method, endpoint, **kwargs)
        if r.status_code == HTTPStatus.UNAUTHORIZED:
            raise ApiUnauthorizedException('The token is invalid or insufficient permissions.')
        return r


class Koodous(ApiWithTokenBase):
    """Main class to interact with the Koodous API.
    """
    api_url = KOODOUS_API_URL
    api_endpoints = KOODOUS_API_ENDPOINTS

    def _download_feed(self, feed: str, package: Optional[Union[str, datetime]] = '') -> requests.Response:
        """Internal method to do the response to the feed endpoint. Can choose between apks, analyses and detections.

        :param package: the package datetime parameter.
        :return: the response instance.
        """
        r = self.request('GET', feed, stream=True, params={'package': package_param(package)})
        # Check the package is available.
        if r.status_code == HTTPStatus.NOT_FOUND:
            raise FeedPackageException('Make sure the date on the package is not older than a week.')
        return r

    def apks(self, search: str = '', **params) -> Iterator[Apk]:
        """Create an apks iterator. This method is alternative to ``list_apks``.

        You can use this method iterating over the it:

        .. code-block:: python

           koodous = Koodous('KOODOUS_API_TOKEN')
           apks = koodous.apks()
           for i in range(10):
               print(next(apks))

        **Be careful with the amount of apks retrieved if you have a small request limit.**

        :param search: the parameters search.
        :param params: other parameters to be included in the request.
        :return: apks iterator.
        """
        r_params = {'search': search, **params}
        yield from (Apk(data) for data in self._iterator_cursor_pagination(self.api_endpoints['apks'], r_params))

    def apk(self, sha256: str) -> Apk:
        """Get the apk sample data.

        :param sha256: sha256 checksum.
        :return: the apk sample representation.
        """
        r = self.request('GET', self.api_endpoints['apks_detail'].format(sha256=sha256))
        # Check the response status code.
        if r.status_code == HTTPStatus.NOT_FOUND:
            raise ApkNotFound(f'The apk {sha256} not found.')
        else:
            r.raise_for_status()
        # Create the apk representation object.
        json_ = r.json()
        return Apk(json_)

    def download_apk(self, sha256: str, output_folder: str) -> str:
        """Download the apk sample.

        :param sha256: sha256 checksum.
        :param output_folder: the folder to save the apk.
        :return: the output file path.
        """
        filename = sha256 + '.apk'
        output_path = os.path.join(output_folder, filename)
        r = self.request('GET', self.api_endpoints['apks_detail_download'].format(sha256=sha256))
        # Check the response status code.
        if r.status_code == HTTPStatus.NOT_FOUND:
            raise ApkNotFound(f'The apk {sha256} not found.')
        elif r.status_code == HTTPStatus.NO_CONTENT:
            raise ApkNotFound(f'The apk {sha256} has no download link.')
        else:
            r.raise_for_status()
        # Get the download url.
        json_ = r.json()
        download_url = json_['download_url']
        # Download and store the sample.
        request_download(download_url, output_path)
        return output_path

    def upload_apk(self, file_path: str) -> None:
        """Upload an apk to the Koodous system.

        :param file_path: the apk file path.
        :return: None.
        """
        # Get the apk sha256.
        sha256 = sha256sum(file_path)
        # Get the upload url.
        r = self.request('GET', self.api_endpoints['apks_detail_upload'].format(sha256=sha256))
        # Check the response status code.
        r.raise_for_status()
        # Get the upload url.
        json_ = r.json()
        upload_url = json_['upload_url']
        # Upload the file to the given url.
        with open(file_path, 'rb') as f:
            files = {'file': f}
            r = self.request('POST', upload_url, files=files)
            r.raise_for_status()

    def analysis_apk(self, sha256: str) -> dict:
        """Get the apk analysis from Koodous system.

        :param sha256: sha256 checksum.
        :return: the analysis representation object.
        """
        r = self.request('GET', self.api_endpoints['apks_detail_analysis'].format(sha256=sha256))
        # Check the response status code.
        r.raise_for_status()
        return r.json()

    def analyze_apk(self, sha256: str) -> None:
        """Send an apk to be analyzed by the Koodous system.

        :param sha256: sha256 checksum.
        :return: None.
        """
        r = self.request('GET', self.api_endpoints['apks_detail_analyze'].format(sha256=sha256))
        # Check the response status code.
        r.raise_for_status()

    def feed_apks(self, package: Optional[Union[str, datetime]] = '') -> ApksFeed:
        """Get the apks feed.

        Note that using the datetime object you can't specify a hourly package because the datetime minute is 0 when it
        is not set.

        :param package: the package datetime. Can be a str with the format %Y%m%dT%H%M or %Y%m%dT%H or a datetime
        object.
        :return: the apks feed instance.
        """
        r = self._download_feed(self.api_endpoints['apks_feed'], package)
        return ApksFeed(BytesIO(r.raw.read(decode_content=True)), package)

    def feed_analyses(self, package: Optional[Union[str, datetime]] = '') -> AnalysesFeed:
        """Get the analyses feed.

        Note that using the datetime object you can't specify a hourly package because the datetime minute is 0 when it
        is not set.

        :param package: the package datetime. Can be a str with the format %Y%m%dT%H%M or %Y%m%dT%H or a datetime
        object.
        :return: the apk analyses instance.
        """
        r = self._download_feed(self.api_endpoints['analyses_feed'], package)
        return AnalysesFeed(BytesIO(r.raw.read(decode_content=True)), package)

    def feed_detected(self, package: Optional[Union[str, datetime]] = '') -> AnalysesFeed:
        """Get the analysis feed from the detected samples only.

        Note that using the datetime object you can't specify a hourly package because the datetime minute is 0 when it
        is not set.

        :param package: the package datetime. Can be a str with the format %Y%m%dT%H%M or %Y%m%dT%H or a datetime
        object.
        :return: the analysis feed instance.
        """
        r = self._download_feed(self.api_endpoints['detected_feed'], package)
        return AnalysesFeed(BytesIO(r.raw.read(decode_content=True)), package)

    def apk_comments(self, sha256: str) -> Iterator[Comment]:
        """Get the comments from an apk.

        :param sha256: apk checksum.
        :return: the apk comments.
        """
        yield from self._iterator_cursor_pagination(self.api_endpoints['apks_detail_comments'].format(sha256=sha256))

    def apk_create_comment(self, sha256: str, text: str) -> None:
        """Create a comment in an apk.

        :param sha256: apk checksum.
        :param text: the comment text.
        :return: None.
        """
        r = self.request('POST', self.api_endpoints['apks_detail_comments'].format(sha256=sha256), data={'text': text})
        r.raise_for_status()

    def apk_update_comment(self, sha256: str, comment_id: int, text: str) -> None:
        """Update a comment in an apk (you must be the owner or have enough permissions).

        :param sha256: apk checksum.
        :param comment_id: comment identifier.
        :param text: the new comment text.
        :return: None.
        """
        endpoint = self.api_endpoints['apks_detail_comments_detail'].format(sha256=sha256, comment_id=comment_id)
        r = self.request('PUT', endpoint, data={'text': text})
        r.raise_for_status()

    def apk_delete_comment(self, sha256: str, comment_id: str) -> None:
        """Delete a comment in a apk (you must be the owner or have enough permissions).

        :param sha256: apk checksum.
        :param comment_id: comment identifier.
        :return: None.
        """
        endpoint = self.api_endpoints['apks_detail_comments_detail'].format(sha256=sha256, comment_id=comment_id)
        r = self.request('DELETE', endpoint)
        r.raise_for_status()
