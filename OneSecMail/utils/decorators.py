from functools import wraps
import requests  # handle server error decorator

def validate_email_format(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'email' in kwargs:
            email = kwargs['email']
            if not isinstance(email, str):
                raise ValueError("Email must be a string")
            if '@' not in email:
                raise ValueError("Email must contain @ symbol")
            if len(email.split('@')) != 2:
                raise ValueError("Email must contain exactly one @ symbol")
            local, domain = email.split('@')
            if not local or not domain:
                raise ValueError("Email local part and domain cannot be empty")
            if '.' not in domain:
                raise ValueError("Email domain must contain at least one dot")
        return func(*args, **kwargs)
    return wrapper

def handle_request(func):
    def wrapper(self, *args, **kwargs):
        try:
            response = func(self, *args, **kwargs)
            response.raise_for_status()
            
            if response.status_code != 200:
                raise Exception("Server error occurred while processing the request")
                
            return response
        except requests.RequestException as e:
            raise Exception(f"Error making request: {str(e)}")
        except Exception as e:
            # Only re-raise if it's not a ValueError
            if not isinstance(e, ValueError):
                raise Exception(f"Unexpected error: {str(e)}")
            raise
    return wrapper