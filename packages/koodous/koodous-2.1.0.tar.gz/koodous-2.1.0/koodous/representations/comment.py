from datetime import datetime
from typing import List, Optional

from koodous.representations.base import BaseRepresentation


class Comment(BaseRepresentation):
    """The ruleset representation.
    """

    def __str__(self):
        return f'Comment(id={self.id})'

    def __repr__(self):
        return f'RuleSet()'

    @property
    def id(self) -> int:
        """Comment identifier."""
        return self.data['id']

    @property
    def author_data(self) -> dict:
        """The analyst dict data."""
        return self.data['author']

    @property
    def author(self) -> None:
        """TODO: Return the Author representation."""
        raise NotImplementedError

    @property
    def created_on(self) -> datetime:
        """The date when comment was created."""
        return self._fromtimestamp(self.data['created_on'])

    @property
    def modified_on(self) -> datetime:
        """The date when comment was modified."""
        return self._fromtimestamp(self.data['modified_on'])

    @property
    def apk(self) -> str:
        """APK sha256 hash."""
        return self.data['apk']

    @property
    def text(self) -> None:
        """The comment's content."""
        return self.data['text']
