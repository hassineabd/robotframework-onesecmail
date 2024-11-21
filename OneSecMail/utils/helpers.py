import re

def validate_email_format(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_count(self, count):
    try:
        count = int(count)
        return count > 0
    except (ValueError, TypeError):
        return False

def response_to_list(response):
    items = response.json()
    if not items:
        return []
    return [item for item in items]

def split_email(email):
    if not validate_email_format(email):
        return False
    return email.split('@')

def verify_response_code(response):
    if response.status_code != 200:
        raise Exception(f"Unexpected status code: {response.status_code}")

def handle_server_error(response):
    if response.status_code == 500:
        raise Exception("Internal Server Error")