import datetime
from robot.api import logger
from robot.api.deco import keyword, not_keyword, library
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
    
    @keyword
    def download_attachment(self, email, email_id, attachment_id):
        login, domain = Helpers.split_email(email)
        return self._client._download_attachment(login, domain, email_id, attachment_id)
    
    @keyword
    def fetch_email_by_field(self,field, email):
        field = field.lower()
        if field not in ['from','subject', 'body']:
            raise ValueError(f"Invalid field: {field}. Valid fields are 'from', 'subject' and 'body'.")
        received_emails = self.get_emails(email)

        for email_summary in received_emails :
            logger.info(f"Fetching email with ID: {email_summary['id']}")
            if field == 'body':
                content = self._fetch_email_body(email_response)   
            email_response = self.read_email(email, str(email_summary['id']))
            logger.info(f"Email response: {email_response}")
            return email_response[field]
    
    @keyword
    def find_recieved_email_by_field(self, email, field, value):
        field = field.lower()   
        valid_fields = ['from', 'subject', 'body']
        if field not in valid_fields:
            raise ValueError(f"Invalid field: {field}. Valid fields are {valid_fields}.")

        emails = self.get_emails(email)
        for email_summary in emails:
            email_response = self.read_email(email, email_summary['id'])

            if field == 'body':
                content = self._fetch_email_body(email_response)
            else:
                content = email_response[field]

            if content and value in content:
                return email_response
        return None

    
    #private method
    def _fetch_email_body(self, email_content):
        if 'textBody' in email_content and email_content['textBody']:
            return email_content['textBody']
        elif 'htmlBody' in email_content and email_content['htmlBody']:
            return email_content['htmlBody']
        elif 'body' in email_content and email_content['body']:
            return email_content['body']
        else:
            return "No content found in the email body."
