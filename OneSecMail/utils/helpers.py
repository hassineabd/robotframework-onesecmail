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
    def get_email_by_index(self, messages, index=0):
        if 0 <= index < len(messages):
            return messages[index]
        else:
            raise IndexError("Index out of range for messages list.")
    
    @staticmethod
    def get_value_from_email(self, message, key):
        """
            Keys are : id, from, subject, date, body
        """
        return message.get(key, None)