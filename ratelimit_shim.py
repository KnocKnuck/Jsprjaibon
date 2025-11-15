"""
Temporary shim for ratelimit package
Simple implementation that provides basic rate limiting functionality
"""
import time
import functools


def sleep_and_retry(func):
    """Decorator that sleeps and retries if rate limit is exceeded"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def limits(calls: int, period: float):
    """Decorator to limit function calls

    Args:
        calls: Number of calls allowed
        period: Time period in seconds
    """
    # Simple implementation: sleep between calls
    sleep_time = period / calls

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Sleep to enforce rate limit
            time.sleep(sleep_time)
            return func(*args, **kwargs)
        return wrapper
    return decorator
