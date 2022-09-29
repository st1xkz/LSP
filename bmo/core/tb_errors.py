import typing as t

__all__: t.Sequence[str] = ("ToolboxError", "CacheFailureError")


class ToolboxError(Exception):
    """Base class for exceptions in this module."""


class CacheFailureError(ToolboxError):
    """Exception raised when a cache lookup fails."""
