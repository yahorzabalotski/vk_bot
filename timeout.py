"""This module implements timeout decorator."""

import signal
from functools import wraps


class TimeoutError(Exception):
    pass


def timeout(seconds=10):
    def decorator(func):

        def _handle_timeout(signum, frame):
            raise TimeoutError

        @wraps(func)
        def wrapper(*args, **kwargs):

            # set signal handler
            signal.signal(signal.SIGALRM, _handle_timeout)
            # start alarm
            signal.alarm(seconds)

            # the try block is needed because of when func has finished in time
            # less then timeout seconds, finally block cancels send the signal
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)

            return result

        return wrapper

    return decorator
