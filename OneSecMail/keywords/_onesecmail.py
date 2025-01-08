import datetime
import time
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
    def get_emails_summary(self, email):
        login, domain = Helpers.split_email(email)
        return self._client._get_messages(login, domain)

    @keyword
    def read_email(self, email, email_id):
        login, domain = Helpers.split_email(email)
        return self._client._read_message(login, domain, email_id)
    
    @keyword
    def fetch_attachment_content(self, email, email_id, filename):
        login, domain = Helpers.split_email(email)
        return self._client._fetch_attachment_content(login, domain, email_id, filename)

    @keyword
    def download_attachment(self, email, email_id, filename):
        login, domain = Helpers.split_email(email)
        content = self._client._fetch_attachment_content(login, domain, email_id, filename)
        Helpers.save_file(content, filename)

# further 
    @not_keyword
    def _validate_field(self, field, valid_fields):
        field = field.lower()
        if field not in valid_fields:
            raise ValueError(f"Invalid field: {field}. Valid fields are {valid_fields}.")
        return field
    
    @keyword
    def wait_for_email(self, email, field, expected_value, timeout=30, interval=5):
        """Wait for an email matching the specified field value and return its content.
        
        Args:
            email: Email address to check
            field: Field to match ('from', 'subject', or 'date')
            expected_value: Value to match in the specified field
            timeout: Maximum time to wait in seconds
            interval: Time between checks in seconds
        
        Returns:
            dict: The matching email content
            
        Raises:
            ValueError: If field is invalid
            TimeoutError: If no matching email is found within timeout period
        """
        self._validate_field(field, ['from', 'subject', 'date'])
        
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        while datetime.datetime.now() < end_time:
            try:
                email_id = self.get_email_id_matching_field(email, field, expected_value)
                return self.read_email(email, email_id)
            except ValueError:
                time.sleep(interval)
                continue
                
        raise TimeoutError(
            f"No email with {field}='{expected_value}' arrived within {timeout} seconds"
        )


    @keyword
    def get_email_id_matching_field(self, email, field, expected_value):
        self._validate_field(field, ['from', 'subject', 'date'])
        emails = self.get_emails_summary(email)
        for email_data in emails:
            if email_data.get(field) == expected_value:
                return email_data['id']
        raise ValueError(f"No email found with {field} matching {expected_value}.")
    
    @keyword
    def get_all_recieved_email_data(self, email, field):
        """Returns a list of field values for all emails in the mailbox.
        
        Valid fields are: subject, date, from, attachments, body, textBody, htmlBody"""
        self._validate_field(field, ['from', 'subject', 'date', 'attachments', 'body', 'textBody', 'htmlBody'])
        email_ids = [email_data['id'] for email_data in self.get_emails_summary(email)]
        field_values = []
        for email_id in email_ids:
            email_content = self.read_email(email, email_id)
            field_values.append(email_content.get(field, f'No {field.title()}'))
        return field_values