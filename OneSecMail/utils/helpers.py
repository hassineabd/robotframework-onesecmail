import re

class Helpers:
    @staticmethod
    def validate_email_format(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not bool(re.match(pattern, email)):
            raise ValueError("Invalid email format. Please provide a valid email address.")
        return True

    @staticmethod
    def validate_count(count):
        if not isinstance(count, int) or count <= 0:
            raise ValueError("Count must be a positive integer.")

    @staticmethod
    def split_email(email):
        if Helpers.validate_email_format(email):
            return email.split('@')
    
    @staticmethod
    def save_file(content, filename):
        with open(filename, 'wb') as file:
            file.write(content)