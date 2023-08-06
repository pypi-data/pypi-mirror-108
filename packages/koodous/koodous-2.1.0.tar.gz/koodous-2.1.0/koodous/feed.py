import os.path
import zipfile
import json
from abc import ABC
from io import BytesIO
from typing import List, NamedTuple, Dict, IO

from koodous.exceptions import FeedPackageException
from koodous.utils import request_download


class Sample(NamedTuple):
    """Sample information."""
    sha256: str
    download_url: str


class Analysis(NamedTuple):
    """Analysis information."""
    sha256: str
    analysis: dict


class Feed(ABC):
    """Feed abstract class.
    """

    def __init__(self, bytes_: BytesIO, package: str):
        """

        :param bytes_: bytes with the file response content.
        :param package: package api parameter.
        """
        self.bytes = bytes_
        self.package = package

    def _unzip(self) -> Dict[str, IO[bytes]]:
        zip_file = zipfile.ZipFile(self.bytes)
        files = {}
        for file_name in zip_file.namelist():
            files[file_name] = zip_file.open(file_name)
        return files

    def write(self, output_file: str) -> None:
        """Write the feed zip to the desired file path.

        :param output_file: path to the file output.
        :return: None.
        """
        with open(output_file, 'wb') as f:
            f.write(self.bytes.getbuffer().tobytes())


class ApksFeed(Feed):
    """Class to interact with the output of the apks feed api.

    Things that can be done with this class:
        - Get the samples sha256s and their download links.
        - Download the samples apks to a folder.
    """

    def samples(self) -> List[Sample]:
        """Get the samples from the feed.

        This methods extract the zip and construct the tuples with the samples information (sha256, download url).

        :return: samples sha256s and the download url.
        """
        unzipped_file = self._unzip()
        # Check that the file samples in in the zip.
        if 'samples' not in unzipped_file:
            raise FeedPackageException('The expected file is not in the package feed zip.')
        # Extract the samples file and create the tuples with the samples.
        samples_file = unzipped_file['samples']
        samples_bytes = samples_file.readlines()
        samples = [sample_bytes.decode().strip().split(';') for sample_bytes in samples_bytes]
        return [Sample(sample[0], sample[1]) for sample in samples]

    @staticmethod
    def download_sample(sample: Sample, output_folder: str) -> None:
        """Download the apk from the sample.

        :param sample: sample (sha256, download link).
        :param output_folder: folder to save the apk.
        :return: None.
        """
        file_path = os.path.join(output_folder, f'{sample.sha256}.apk')
        # Download and store the sample.
        request_download(sample.download_url, file_path)

    def download_samples(self, samples: List[Sample], output_folder: str) -> None:
        """Download the apks from the samples

        :param samples: list of samples.
        :param output_folder: folder to save the apk.
        :return: None.
        """
        # Check that the directory exists.
        if not os.path.isdir(output_folder):
            raise FileNotFoundError(f'The directory {output_folder} does not exist.')
        # Download the samples.
        for sample in samples:
            self.download_sample(sample, output_folder)


class AnalysesFeed(Feed):
    """Class to interact with the output of the analyses feed.

    Things that can be done with this class:
    - Get the analysis reports directly in json format with ``analysis()``.
    """

    def analyses(self) -> List[Analysis]:
        """Obtain the analyses from the feed and create a list with them.

        :return: tuples with the sha256 of the analyzed sample and the analysis report of it.
        """
        unzipped_file = self._unzip()
        analyses = []
        for name, file in unzipped_file.items():
            sha256 = name[:-len('.json')]
            analysis = json.load(file)
            analyses.append(Analysis(sha256, analysis))
        return analyses
