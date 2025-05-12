from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

@dataclass(frozen=True)
class Result(Generic[T]):
    """
    A container for operation results, encapsulating success/failure, an error, and an optional value.

    Usage:
        ok_res = Result.ok(42)
        fail_res = Result.fail(ValueError("Something went wrong"))
    """
    is_success: bool
    error: Optional[Exception] = None
    value: Optional[T] = None

    @property
    def is_failure(self) -> bool:
        return not self.is_success

    def get_value(self) -> Optional[T]:
        """
        Retrieves the contained value if the result is a success.
        Raises if the result is a failure.
        """
        if not self.is_success:
            raise Exception("Can't retrieve the value from a failed result.")
        return self.value

    @classmethod
    def ok(cls, value: Optional[T] = None) -> 'Result[T]':
        """Creates a successful Result, optionally wrapping a value."""
        return cls(is_success=True, error=None, value=value)

    @classmethod
    def fail(cls, error: Exception) -> 'Result[T]':
        """Creates a failed Result, wrapping an error."""
        return cls(is_success=False, error=error, value=None)
