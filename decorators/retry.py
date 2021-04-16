import time


class RetryError(Exception):
    pass


# based on http://code.activestate.com/recipes/580745-retry-decorator-in-python/
def retry(attempts=3, exception=Exception, report=lambda *args: None):
    def wrapper(function):
        def wrapped(*args, **kwargs):
            problems = []
            for attempt in range(attempts):
                try:
                    return function(*args, **kwargs)
                except exception as problem:
                    problems.append(problem)
                    report(
                        f"{function.__name__}() failed: `{problem}` - attempt {attempt+1} of {attempts}"
                    )
                    time.sleep(1)

            report(
                f"{function.__name__}() failed definitely. problems = {str(problems)}"
            )
            raise RetryError(
                f"{function.__name__}() failed definitely. problems = {str(problems)}"
            )

        return wrapped

    return wrapper
