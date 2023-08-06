class ApiException(Exception):
    """Koodous API base class."""


class ApiUnauthorizedException(ApiException):
    """Exception when is made a request without the correct token or insufficient privileges."""


class FeedException(ApiException):
    """Base class for the feed exceptions."""


class FeedPackageException(FeedException):
    """Exception related to the feed package."""


class PackageInvalidFormatException(FeedException):
    """Package format invalid exception. Check the koodous api docs."""


class ApkNotFound(ApiException):
    """Apk sample not found."""
