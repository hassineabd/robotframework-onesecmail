import re
import requests
from robot.api import logger
from robot.api.deco import keyword, not_keyword, library
from datetime import datetime

from OneSecMail.keywords._request import RequestHandler
from OneSecMail.utils.decorators import handle_request
from .keywordgroup import KeywordGroup

class _OneSecMailKeywords(KeywordGroup):
    BASE_URL = 'https://www.1secmail.com/api/v1/'
    
    def __init__(self):
        self._request = RequestHandler()
    
    def __validate_email_format(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def __validate_count(self, count):
        try:
            count = int(count)
            return count > 0
        except (ValueError, TypeError):
            return False

    def __handle_server_error(self, response):
        return response.status_code == 500

    def __verify_response_code(self, response):
        return response.status_code == 200

    def __response_to_list(self, response):
        items = response.json()
        if not items:
            raise None
        return [item for item in items]

    def __split_email(self, email):
        if not self.__validate_email_format(email):
            raise ValueError("Invalid email format")
        return email.split('@')

    # @keyword 
    # def generate_random_mailbox(self, count=1):
    #     if not self.__validate_count(count):
    #         raise ValueError("Count must be a positive integer.")
        
    #     try:
    #         response = requests.get(f"{self.BASE_URL}?action=genRandomMailbox&count={count}")
    #         response.raise_for_status()
            
    #         if self.__handle_server_error(response):
    #             raise Exception("Internal server error occurred while generating mailbox")
                
    #         mailboxes = self.__format_mailboxes(response)
    #         return mailboxes
                
    #     except requests.RequestException as e:
    #         raise Exception(f"Error making request: {str(e)}")
    #     except Exception as e:
    #         raise Exception(f"Unexpected error: {str(e)}")
    @keyword 
    def generate_random_mailbox(self, count=1):
        if not self.__validate_count(count):
            raise ValueError("Count must be a positive integer.")
        response = self._request.get(f"{self.BASE_URL}?action=genRandomMailbox&count={count}")
        return self.__response_to_list(response)
    

    @keyword
    def get_messages(self, login, domain):
        """Fetches the list of emails for a specific mailbox."""
        response = requests.get(f"{self.BASE_URL}?action=getMessages&login={login}&domain={domain}")
        if response.status_code == 200:
            return self.__response_to_list(response)
        else:
            raise Exception(f"Failed to get messages: {response.text}")

    @keyword
    def read_message(self, login, domain, email_id):
        """Reads the content of a specific email."""
        response = requests.get(f"{self.BASE_URL}?action=readMessage&login={login}&domain={domain}&id={email_id}")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to read message: {response.text}")

    @keyword
    def delete_message(self, login, domain, email_id):
        """Deletes a specific email."""
        response = requests.get(f"{self.BASE_URL}?action=deleteMessage&login={login}&domain={domain}&id={email_id}")
        if response.status_code == 200:
            logger.info ( "Message deleted successfully")
        else:
            raise Exception(f"Failed to delete message: {response.text}")


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
        """
        Retrieves the email body from the JSON response and returns it as a string.

        Args:
            email_response (dict): The JSON response from the readMessage API.

        Returns:
            str: The email body as a plain text or HTML string.
        """
        if 'textBody' in email_response and email_response['textBody']:
            return email_response['textBody']
        elif 'htmlBody' in email_response and email_response['htmlBody']:
            return email_response['htmlBody']
        elif 'body' in email_response and email_response['body']:
            return email_response['body']
        else:
            return "No content found in the email body."
                

    def get_message_attribute(self, login, domain, attribute:str, order='desc'):
        """
        attributes are : id, from, subject, date, body
        """
        messages = self.get_messages(login, domain)
        message_attributes = [message[attribute] for message in messages if attribute in message]
        #message_ids = [message[f'{attribute}'] for message in messages]
        if order == 'desc':
            message_attributes.sort(reverse=True)
        else:
            message_attributes.sort()
        return message_attributes

    @keyword("get message ids")
    def __get_message_ids(self, login, domain, order='desc'):
        return self.get_message_attribute(login, domain, 'id', order)
    
    @keyword("get message dates")
    def __get_message_dates(self, login, domain, order='desc'):
        return self.get_message_attribute(login, domain, 'date', order)

    def __get_message_subjects(self, login, domain, order='desc'):
        return self.get_message_attribute(login, domain, 'subject', order)
    
    def __get_message_senders(self, login, domain, order='desc'):
        return self.get_message_attribute(login, domain, 'from', order)
    

    def filter_dates_after_reference(self, date_list, reference_time):
        reference_datetime = datetime.strptime(reference_time, '%Y-%m-%d %H:%M:%S')
        filtered_dates = [
            date_str for date_str in date_list 
            if datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') > reference_datetime
        ]

        return filtered_dates


    def get_first_id_in_list(self, message_ids):
        if not message_ids:
            return False
        return str(message_ids[0])
