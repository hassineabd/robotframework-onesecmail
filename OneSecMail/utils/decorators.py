from functools import wraps
from requests.exceptions import RequestException 
import requests
from robot.api import logger


def catch_on_request(is_json=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
                response.raise_for_status()
                return response.json() if is_json else response.content
                
            except (RequestException, requests.HTTPError) as e:
                logger.error(f"Connection error in {func.__name__}: {e}. Probably too many requests.")
                raise 
        return wrapper
    return decorator