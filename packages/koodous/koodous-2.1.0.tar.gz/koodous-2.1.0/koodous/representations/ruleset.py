from datetime import datetime
from typing import List, Optional

from koodous.representations.base import BaseRepresentation
from koodous.representations.rule import Rule


class Ruleset(BaseRepresentation):
    """The ruleset representation.
    """

    def __str__(self):
        return f'RuleSet(id={self.id}, name={self.name}, active={self.active}, deleted={self.deleted})'

    def __repr__(self):
        return f'RuleSet(id={self.id}, name={self.name})'

    @property
    def id(self) -> int:
        """The ruleset identifier."""
        return self.data['id']

    @property
    def created_on(self) -> datetime:
        """The date when the ruleset was created."""
        return self._fromtimestamp(self.data['created_on'])

    @property
    def modified_on(self) -> datetime:
        """The last date when the ruleset was modified."""
        return self._fromtimestamp(self.data['modified_on'])

    @property
    def name(self) -> str:
        """The ruleset name."""
        return self.data['name']

    @property
    def rules(self) -> List[Rule]:
        """The set of rules."""
        raise NotImplementedError  # TODO

    @property
    def rules_raw(self) -> str:
        """The set of rules in raw string."""
        return self.data['rules']

    @property
    def active(self) -> bool:
        """If the ruleset is active or not."""
        return self.data['active']

    @property
    def privacy(self) -> str:
        """The ruleset privacy parameter. Can be `public` or `private`."""
        return self.data['privacy']

    @property
    def social(self) -> bool:
        """If the ruleset is inside the Koodous system."""
        return self.data['social']

    @property
    def pending_social(self) -> bool:
        """TODO"""
        return self.data['pending_social']

    @property
    def deleted(self) -> bool:
        """If the ruleset is deleted."""
        return self.data['deleted']

    @property
    def send_notifications(self) -> bool:
        """If the ruleset will notify or not."""
        return self.data['send_notifications']

    @property
    def detections(self) -> int:
        """The number of matches done with this ruleset."""
        return self.data['detections']

    @property
    def rating(self) -> int:
        """The ruleset rating."""
        return self.data['rating']

    @property
    def parent(self) -> Optional[str]:
        """TODO"""
        return self.data['parent']
