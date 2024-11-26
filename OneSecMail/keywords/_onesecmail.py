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
    
    @not_keyword
    def _validate_field(self, field, valid_fields):
        """Validate if the given field is valid"""
        field = field.lower()
        if field not in valid_fields:
            raise ValueError(f"Invalid field: {field}. Valid fields are {valid_fields}.")
        return field

    @not_keyword
    def _get_email_content(self, email_response, field):
        body_fields = ['body', 'htmlbody', 'textbody']
        if field.lower() in body_fields:
            return self._fetch_email_body(email_response)
        return email_response[field]

    @not_keyword
    def _search_emails(self, emails, email, field, value):
        for email_summary in emails:
            email_response = self.read_email(email, email_summary['id'])
            content = self._get_email_content(email_response, field)
            if content and value in content:
                return email_response
        return None

    @keyword
    def find_recieved_email_by_field(self, email, field, value):
        valid_fields = ['from', 'subject', 'attachment', 'body', 'textBody', 'htmlBody']
        field = self._validate_field(field, valid_fields)
        emails = self.get_emails(email)
        return self._search_emails(emails, email, field, value)

    @not_keyword
    def _fetch_email_body(self, email_content):
        body_fields = ['textBody', 'htmlBody', 'body']
        for field in body_fields:
            if field in email_content and email_content[field]:
                return email_content[field]
        raise ValueError("No content found in the email body.")