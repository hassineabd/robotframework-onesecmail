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
        # try:
        #     if isinstance(count, float):
        #         raise ValueError("Count must be a positive integer.")
        #     count = int(count)
        #     return count > 0
        # except (ValueError, TypeError):
        #     raise ValueError("Count must be a positive integer.")
        
    @staticmethod
    def response_to_list(response):
        if not response:
            return []
        return [item for item in response]

    @staticmethod
    def split_email(email):
        if Helpers.validate_email_format(email):
            return email.split('@')

    @staticmethod
    def verify_response_code(response):
        if response.status_code != 200:
            raise Exception(f"Unexpected status code: {response.status_code}")

    @staticmethod
    def handle_server_error(response):
        if response.status_code == 500:
            raise Exception("Internal Server Error")

    @staticmethod    
    def get_email_by_index(self, messages, index=0):
        """
        Retrieves the email JSON object at the specified index.
        Returns:
            dict: The email JSON object at the specified index.
        Raises:
            IndexError: If the index is out of range.
        """
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