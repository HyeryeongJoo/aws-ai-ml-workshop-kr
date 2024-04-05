import functools
import logging
import random
import time

logging.basicConfig()
logger = logging.getLogger('retry-bedrock-invocation')
logger.setLevel(logging.INFO)

def retry(total_try_cnt=5, sleep_in_sec=5, retryable_exceptions=()):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for cnt in range(total_try_cnt):
                logger.info(f"trying {func.__name__}() [{cnt+1}/{total_try_cnt}]")

                try:
                    result = func(*args, **kwargs)
                    logger.info(f"in retry(), {func.__name__}() returned '{result}'")

                    if result: return result
                except retryable_exceptions as e:
                    logger.info(f"in retry(), {func.__name__}() raised retryable exception '{e}'")
                    pass
                except Exception as e:
                    logger.info(f"in retry(), {func.__name__}() raised {e}")
                    raise e

                time.sleep(sleep_in_sec)
            logger.info(f"{func.__name__} finally has been failed")
        return wrapper
    return decorator