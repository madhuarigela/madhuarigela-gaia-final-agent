import time

def with_retries(exceptions=(Exception,), attempts=2, min_wait=2, max_wait=10):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            last = None
            for attempt in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    last = exc
                    if attempt + 1 < attempts:
                        time.sleep(min(max_wait, min_wait * (2 ** attempt)))
            raise last
        return wrapper
    return decorator
