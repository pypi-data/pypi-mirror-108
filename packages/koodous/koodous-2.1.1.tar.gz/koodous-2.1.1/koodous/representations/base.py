from datetime import datetime, timezone


class BaseRepresentation:
    """API objects base representation."""

    def __init__(self, data: dict):
        """

        :param data the representation data.
        """
        self.data = data

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.data == self.data
        return False

    def __hash__(self):
        return hash(self.data.values())

    @staticmethod
    def _fromtimestamp(timestamp):
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
