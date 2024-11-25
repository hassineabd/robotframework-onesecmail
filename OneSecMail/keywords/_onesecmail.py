import re
import requests
from robot.api import logger
from robot.api.deco import keyword, not_keyword, library
from datetime import datetime
from OneSecMail.utils.helpers import Helpers
from ._client import _OneSecMailClient

class _OneSecMailKeywords():
    def __init__(self):
        self._client = _OneSecMailClient()

    @keyword 
    def generate_temporary_mailbox(self, count=1):
        Helpers.validate_count(count)
        return self._client._generate_temporary_mailbox(count)

    @keyword
    def get_emails(self, email):
        login, domain = Helpers.split_email(email)
        return self._client._get_messages(login, domain)

    @keyword
    def read_email(self, email, email_id):
        login, domain = Helpers.split_email(email)
        return self._client._read_message(login, domain, email_id)

    # @keyword
    # def fetch_email_by(self,attribute, email):
    #     attribute = attribute.lower()
    #     emails = self.get_emails(email)
    #     for email in emails :
    #         email_response = self.read_email(email, email['id'])
            
    #         if attribute not in ['subject', 'body']:
    #             raise ValueError(f"Invalid attribute: {attribute}. Valid attributes are 'subject' and 'body'.")
    #         return email_response[attribute]
    
    # @keyword
    # def find_email_by_attribute(self, email, attribute, value):
    #     attribute = attribute.lower()
    #     valid_attributes = ['from', 'subject', 'body']
    #     if attribute not in valid_attributes:
    #         raise ValueError(f"Invalid attribute: {attribute}. Valid attributes are {valid_attributes}.")

    #     emails = self.get_emails(email)
    #     for email_summary in emails:
    #         email_response = self.read_email(email, email_summary['id'])
            
    #         if attribute == 'body':
    #             content = self._fetch_email_body(email_response)
    #         else:
    #             content = email_response.get(attribute)

    #         if content and value in content:
    #             return email_response
    #     return None

    
    # #private method
    # def _fetch_email_body(self, email_response):
    #     if 'textBody' in email_response and email_response['textBody']:
    #         return email_response['textBody']
    #     elif 'htmlBody' in email_response and email_response['htmlBody']:
    #         return email_response['htmlBody']
    #     elif 'body' in email_response and email_response['body']:
    #         return email_response['body']
    #     else:
    #         return "No content found in the email body."
    

    # def filter_dates_after_reference(self, date_list, reference_time):
    #     reference_datetime = datetime.strptime(reference_time, '%Y-%m-%d %H:%M:%S')
    #     filtered_dates = [
    #         date_str for date_str in date_list 
    #         if datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') > reference_datetime
    #     ]
    #     return filtered_dates
