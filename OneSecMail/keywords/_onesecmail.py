import datetime
import time
from robot.api import logger
from robot.api.deco import keyword, not_keyword, library
from OneSecMail.utils.helpers import Helpers
from ._client import _OneSecMailClient
from ._logging import _LoggingKeywords

class _OneSecMailKeywords():
    def __init__(self):
        self._client = _OneSecMailClient()
        self._p= _LoggingKeywords()
        self._active_email= None

    def _resolve_email(self, email):
        email = email or self._active_email

        if not email:
            raise ValueError(
                "No email address provided or registered. "
                "Use 'Register Email' first or provide email argument."
            )
        return email

    @keyword 
    def generate_temporary_mailbox(self, count=1):
        """Generate one or more temporary email addresses.
        
        Args:
            count: Number of email addresses to generate (default: 1)
            
        Returns:
            list: List of generated email addresses
            
        Raises:
            ValueError: If count is less than 1
        """
        Helpers.validate_count(count)
        return self._client._generate_temporary_mailbox(count)
    
    @keyword
    def get_inbox_summary(self, email=None):
        """Get summary of all emails in the inbox.
        
        Args:
            email: Email address to check (optional if already registered)
            
        Returns:
            list: List of email summaries containing id, from, subject and date
            
        Raises:
            ValueError: If no email is provided or registered
        """
        email =  self._resolve_email(email)
        login, domain = Helpers.split_email(email)
        return self._client._get_messages(login, domain)

    @keyword
    def read_email(self, message_id, email=None):
        """Read a specific email message.
        
        Args:
            message_id: ID of the email to read
            email: Email address to check (optional if already registered)
            
        Returns:
            dict: Email content including subject, body, attachments etc.
            
        Raises:
            ValueError: If no email is provided or registered
        """
        email =  self._resolve_email(email)
        login, domain = Helpers.split_email(email)
        return self._client._read_message(login, domain, message_id)
    
    @keyword
    def fetch_attachment_content(self, message_id, filename, email=None):
        """Fetch content of an email attachment.
        
        Args:
            message_id: ID of the email containing the attachment
            filename: Name of the attachment file
            email: Email address to check (optional if already registered)
            
        Returns:
            bytes: Content of the attachment
            
        Raises:
            ValueError: If no email is provided or registered
        """
        email =  self._resolve_email(email)
        login, domain = Helpers.split_email(email)
        return self._client._fetch_attachment_content(login, domain, message_id, filename)
    
    @keyword
    def download_attachment(self, message_id, filename, email=None):
        """Download an email attachment to local file system.
        
        Args:
            message_id: ID of the email containing the attachment
            filename: Name of the attachment file
            email: Email address to check (optional if already registered)
            
        Raises:
            ValueError: If no email is provided or registered
        """
        email =  self._resolve_email(email)
        login, domain = Helpers.split_email(email)
        content = self._client._fetch_attachment_content(login, domain, message_id, filename)
        if content:
            Helpers.save_file(content, filename)
        else :
            self._p._log("File doesn't have any content or doesn't exist", 'warn')

    @keyword
    def register_email(self, email):
        """Register an email address for subsequent operations.
        
        Args:
            email: Email address to register
            
        Raises:
            ValueError: If email format is invalid
        """
        Helpers.validate_email_format(email)
        self._active_email = email
        self._p._log(f"Email address {email} has been registered")

    @keyword
    def get_active_email(self):
        """Get the currently registered email address.
        
        Returns:
            str: Currently registered email address or None
        """
        if not self._active_email:
            self._p._log("No email address is registered. Use 'Register Email' first.", 'warn')
        self._p._log(f"Active email address: {self._active_email}")
        return self._active_email

    @not_keyword
    def _validate_field(self, field, valid_fields):
        field = field.lower()
        if field not in valid_fields:
            raise ValueError(f"Invalid field: {field}. Valid fields are {valid_fields}.")
        return field
    
    @keyword
    def wait_for_inbox(self, field, expected_value, email=None, timeout=30, interval=5):
        """Wait for an email matching the specified field value and return its content.
        
        Args:
            field: Field to match ('from', 'subject', or 'date')
            expected_value: Value to match in the specified field
            email: Email address to check (optional if already registered)
            timeout: Maximum time to wait in seconds (default: 30)
            interval: Time between checks in seconds (default: 5)
        
        Returns:
            dict: The matching email content
            
        Raises:
            ValueError: If field is invalid
            TimeoutError: If no matching email is found within timeout period
        """
        self._validate_field(field, ['from', 'subject', 'date'])
        email = self._resolve_email(email)
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        while datetime.datetime.now() < end_time:
            try:
                email_id = self.get_email_id_matching_field(field, expected_value, email)
                return self.read_email(email_id, email)
            except ValueError:
                time.sleep(interval)
                continue
                
        raise TimeoutError(
            f"No email with {field}='{expected_value}' arrived within {timeout} seconds"
        )

    @keyword
    def get_email_id_matching_field(self, field, expected_value, email=None):
        """Get ID of first email matching the specified field value.
        
        Args:
            field: Field to match ('from', 'subject', or 'date')
            expected_value: Value to match in the specified field
            email: Email address to check (optional if already registered)
            
        Returns:
            str: ID of the matching email
            
        Raises:
            ValueError: If no matching email is found or field is invalid
        """
        email = self._resolve_email(email)
        self._validate_field(field, ['from', 'subject', 'date'])
        emails = self.get_inbox_summary(email)
        for email_data in emails:
            if email_data.get(field) == expected_value:
                return email_data['id']
        raise ValueError(f"No email found with {field} matching {expected_value}.")
    
    @keyword
    def get_all_received_email_data(self, field, email=None):
        """Returns a list of field values for all emails in the mailbox.
        
        Args:
            field: Field to extract (subject, date, from, attachments, body, textBody, htmlBody)
            email: Email address to check (optional if already registered)
            
        Returns:
            list: List of field values from all emails
            
        Raises:
            ValueError: If field is invalid or no email is provided/registered
        """
        email = self._resolve_email(email)
        self._validate_field(field, ['from', 'subject', 'date', 'attachments', 'body', 'textBody', 'htmlBody'])
        email_ids = [email_data['id'] for email_data in self.get_inbox_summary(email)]
        field_values = []
        for email_id in email_ids:
            email_content = self.read_email(email_id, email)
            field_values.append(email_content.get(field, f'No {field.title()}'))
        return field_values