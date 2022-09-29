import typing as t

__all__: t.Sequence[str] = "CacheFailureError"


class CacheFailureError(ToolboxError):
    """Exception raised when a cache lookup fails."""
