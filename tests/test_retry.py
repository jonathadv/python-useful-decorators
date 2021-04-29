import pytest
from decorators.retry import retry, RetryError


def test_retry_three_errors():
    """Should raise RetryError after three attempts"""

    @retry(report=print)
    def my_testable_function():
        raise Exception("Error from my_testable_function")

    with pytest.raises(RetryError):
        my_testable_function()


def test_retry_one_error():
    """Should not raise RetryError since it works in the second attempt"""
    errors_to_raise = 1

    @retry(report=print)
    def my_testable_function():
        nonlocal errors_to_raise
        if errors_to_raise:
            errors_to_raise -= 1
            raise Exception("Error from my_testable_function")

    my_testable_function()
