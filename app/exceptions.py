"""
SE — Error & exception usage: domain-specific hierarchy instead of bare strings everywhere.
"""


class TasteMapError(Exception):
    """Base application error (inheritance root for all TasteMap failures)."""


class ValidationError(TasteMapError):
    """Raised when user input fails business rules."""

    def __init__(self, message: str, field: str | None = None):
        super().__init__(message)
        self.field = field
        self.message = message


class UploadError(TasteMapError):
    """Raised when an uploaded file is missing or has an invalid type."""


class DatabaseError(TasteMapError):
    """Raised when persistence fails unexpectedly."""


class NetworkError(TasteMapError):
    """Raised when HTTP/socket operations fail."""
