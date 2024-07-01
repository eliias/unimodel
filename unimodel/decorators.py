from time import sleep
from random import uniform


def retry_with_backoff(retries: int = 3, backoff_in_seconds: int = 1):
    def rwb(f):
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return f(*args, **kwargs)
                except Exception:  # noqa
                    if x == retries:
                        raise

                    backoff_for = backoff_in_seconds * 2**x + uniform(0, 1)
                    sleep(backoff_for)
                    x += 1

        return wrapper

    return rwb
