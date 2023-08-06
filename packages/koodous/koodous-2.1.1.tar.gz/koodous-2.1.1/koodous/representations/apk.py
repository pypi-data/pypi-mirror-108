from datetime import datetime
from typing import List

from koodous.representations.base import BaseRepresentation


class Apk(BaseRepresentation):
    """Apk sample representation.
    """

    def __str__(self):
        return f'ApkSample({self.sha256}, app={self.app}, detected={self.detected})'

    def __repr__(self):
        return f'ApkSample({self.sha256}'

    @property
    def created_on(self) -> datetime:
        """The date when the apk was created on koodous."""
        return self._fromtimestamp(self.data['created_on'])

    @property
    def rating(self) -> int:
        """The value of users votes."""
        return self.data['rating']

    @property
    def image(self) -> str:
        """The app image shown on devices."""
        return self.data['image']

    @property
    def tags(self) -> List[str]:
        """The app tag list."""
        return self.data['tags']

    @property
    def md5(self) -> str:
        """The apk md5 hash."""
        return self.data['md5']

    @property
    def sha1(self) -> str:
        """The apk sha1 hash."""
        return self.data['sha1']

    @property
    def sha256(self) -> str:
        """The apk sha256 hash."""
        return self.data['sha256']

    @property
    def app(self) -> str:
        """The app name shown on devices."""
        return self.data['app']

    @property
    def package_name(self) -> str:
        """The app package identifier."""
        return self.data['package_name']

    @property
    def company(self) -> str:
        """The company or developer identifier."""
        return self.data['company']

    @property
    def developer(self) -> str:
        """The company or developer identifier."""
        return self.company

    @property
    def displayed_version(self) -> str:
        """The app version shown on market."""
        return self.data['displayed_version']

    @property
    def size(self) -> int:
        """The app size in bytes."""
        return self.data['size']

    @property
    def stored(self) -> bool:
        """TODO"""
        return self.data['stored']

    @property
    def analyzed(self) -> bool:
        """The apks has been analyzed or not by Koodous system."""
        return self.data['analyzed']

    @property
    def is_apk(self) -> bool:
        """TODO"""
        return self.data['is_apk']

    @property
    def detected(self) -> bool:
        """The apk has been detected by Koodous system."""
        return self.data['detected']

    @property
    def corrupted(self) -> bool:
        """The app cannot be executed properly."""
        return self.data['corrupted']

    @property
    def repo(self) -> str:
        """TODO"""
        return self.data['repo']

    @property
    def on_devices(self) -> bool:
        """TODO"""
        return self.data['on_devices']
