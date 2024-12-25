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

# Add to existing decorators.py
from functools import wraps

def require_email(func):
    """Decorator to handle email parameter for OneSecMail keywords.
    
    If email is not provided, uses the registered email from the instance.
    Validates email format and raises appropriate errors.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Check if the function expects email as a parameter
        if 'email' in func.__code__.co_varnames:
            # If email is provided as positional arg
            if len(args) >= func.__code__.co_varnames.index('email'):
                email_idx = func.__code__.co_varnames.index('email')
                email = args[email_idx]
            # If email is provided as keyword arg
            else:
                email = kwargs.get('email')
            
            # If no email provided, use registered email
            if email is None:
                email = self._active_email
                if email is None:
                    raise ValueError("No email address provided or registered. Use 'Register Email' first.")
                
                # Reconstruct args/kwargs with the active email
                if len(args) >= func.__code__.co_varnames.index('email'):
                    args_list = list(args)
                    args_list[email_idx] = email
                    args = tuple(args_list)
                else:
                    kwargs['email'] = email
            
        return func(self, *args, **kwargs)
    return wrapper