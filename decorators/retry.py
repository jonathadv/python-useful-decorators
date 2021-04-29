# pylint: disable=broad-except
"""
Retry Module
"""

import time
from typing import Union, List, Tuple, Type, Callable


class RetryError(Exception):
    """Base Exception for the Retry module"""

    def __init__(self, *args, problems: List, **kwargs):
        super().__init__(*args, **kwargs)
        self.problems = problems or []


# based on http://code.activestate.com/recipes/580745-retry-decorator-in-python/
def retry(
    attempts: int = 3,
    delays: Tuple[Union[int, float]] = (0, 1, 5),
    exceptions: Union[Type[Exception], Tuple[Exception]] = Exception,
    report: Callable = lambda *args: None,
):
    """
    Catches one or more exception types raised by the wrapped function
    and try to run the function again the number of times set in `attempts`.

    :param attempts: The number of attempts to rerun the function. Defaults to 3.
    :type attempts: int
    :param delays: A tuple of integers or floats where each item is the time in seconds
    to wait before trying again. Defaults to (0, 1, 5).
    :type delays: int
    :param exceptions: A single Exception or a Tuple of Exceptions which will be handled to rerun the function.
    :type exceptions: Exception
    :type exceptions: Tuple[Exception]
    :param report: A function which receives a string as argument to log the results.
    :type report: Callable

    :raises RetryError
    """

    def wrapper(function):
        def wrapped(*args, **kwargs):
            problems = []
            for attempt, delay in zip(range(attempts), delays):
                try:
                    return function(*args, **kwargs)
                except exceptions as problem:
                    problems.append(problem)
                    attempt_err_msg = (
                        f"{function.__name__}() failed: `{problem}`"
                        f" - attempt {attempt+1} of {attempts}. Delaying for {delay}s."
                    )
                    report(attempt_err_msg)
                    time.sleep(delay)

            final_err_msg = f"{function.__name__}() failed after {attempts} attempts. problems = {str(problems)}"
            report(final_err_msg)
            raise RetryError(final_err_msg, problems=problems)

        return wrapped

    return wrapper
