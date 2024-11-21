import re
import requests
from robot.api import logger
from robot.api.deco import keyword, not_keyword, library
from datetime import datetime
from .keywordgroup import KeywordGroup
from OneSecMail.utils.helpers import Helpers
from ._client import _OneSecMailClient

class _OneSecMailKeywords(KeywordGroup):
    def __init__(self):
        self._client = _OneSecMailClient()

    @keyword 
    def generate_temporary_mailbox(self, count=1):
        Helpers.validate_count(count)
        response = self._client._generate_temporary_mailbox(count)
        return Helpers.response_to_list(response)

    @keyword
    def get_messages(self, email):
        login, domain = Helpers.split_email(email)
        response = self._client._get_messages(login, domain)
        return Helpers.response_to_list(response)



            # Keys from message are : id, from, subject, date, body


    def get_last_email_message(self, email):
        messages = self.get_messages(email)
        return self.get_email_by_index(messages, -1)

    def read_message(self, email, email_id):
        """Reads the content of a specific email."""
        login, domain = Helpers.split_email(email)
        message = self._client._read_message(login, domain, email_id)
        return Helpers.response_to_list(message)

    def read_last_message(self, email):
        return self.get_messages(email)[-1]
        
    def read_last_message_subject(self, email):
        return self.read_last_message(email)['subject']

    def read_last_message_body(self, email):
        return self.read_last_message(email)['body']

    def read_message_attribute_by_index(self, email, index=-1, attribute=None):
        """
        Reads a message at the specified index and returns a specific attribute.
        If attribute is None, returns the entire message.

        Args:
            email (str): The email address to fetch messages for.
            index (int, optional): The index of the message to read. Defaults to -1 (last message).
            attribute (str, optional): The specific attribute to retrieve from the message.
                                    If None, returns the entire message.

        Returns:
            The value of the specified attribute, or the entire message if attribute is None.
            Returns None if the index is out of bounds.
        """
        messages = self.get_messages(email)

        # Handle index out of bounds
        if not messages or abs(index) >= len(messages):
            logger.warn(f"No message at index {index}. Total messages: {len(messages)}")
            return None

        message = messages[index]
        if attribute:
            return message.get(attribute)
        else:
            return message
    
    def extract_code_from_body(self, email_body, number_of_digit:int = 5):
        """
        By default extracts a 5-digit code from the email body using regex.

        Args:
            email_body (str): The email body content.
            number_of_digit (str)
        Returns:
            str: The extracted code if found, otherwise None.
        """
        pattern = r'\b\d{5}\b'
        match = re.search(pattern, email_body)
        if match:
            return match.group()
        else:
            return None


    def get_email_body_as_string(self, email_response):
        if 'textBody' in email_response and email_response['textBody']:
            return email_response['textBody']
        elif 'htmlBody' in email_response and email_response['htmlBody']:
            return email_response['htmlBody']
        elif 'body' in email_response and email_response['body']:
            return email_response['body']
        else:
            return "No content found in the email body."
    

    def filter_dates_after_reference(self, date_list, reference_time):
        reference_datetime = datetime.strptime(reference_time, '%Y-%m-%d %H:%M:%S')
        filtered_dates = [
            date_str for date_str in date_list 
            if datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') > reference_datetime
        ]

        return filtered_dates
