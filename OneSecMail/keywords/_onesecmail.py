import datetime
import time
from robot.api import logger
from robot.api.deco import keyword, not_keyword, library
from OneSecMail.utils.helpers import Helpers
from ._client import _OneSecMailClient
from OneSecMail.utils.decorators import require_email

class _OneSecMailKeywords():
    def __init__(self):
        self._client = _OneSecMailClient()
        self._active_email = None

    @keyword
    def create_and_register_mailbox(self):
        """Create a new temporary email and register it for use in subsequent keywords."""
        email = self._client._generate_temporary_mailbox(1)[0]
        self.register_email(email)
        return email

    @keyword
    def register_email(self, email):
        """Register an email address for use in subsequent keywords."""
        Helpers.validate_email_format(email)
        self._active_email = email
        logger.info(f"Registered email address: {email}")

    @keyword
    def get_active_email(self):
        """Get the currently registered email address."""
        if not self._active_email:
            raise ValueError("No email address is registered. Use 'Register Email' first.")
        return self._active_email

    @keyword
    @require_email
    def get_emails_summary(self, email=None):
        """Get summary of all emails in the mailbox."""
        login, domain = Helpers.split_email(email)
        return self._client._get_messages(login, domain)

    @keyword
    @require_email
    def wait_for_email(self, field, expected_value, timeout=60, interval=5, email=None):
        """Wait for an email matching the specified field value."""
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
    @require_email
    def read_email(self, email_id, email=None):
        """Read a specific email by ID."""
        login, domain = Helpers.split_email(email)
        return self._client._read_message(login, domain, email_id)

    @keyword
    @require_email
    def get_email_id_matching_field(self, field, expected_value, email=None):
        """Get email ID matching the specified field value."""
        self._validate_field(field, ['from', 'subject', 'date'])
        emails = self.get_emails_summary(email)
        for email_data in emails:
            if email_data.get(field) == expected_value:
                return email_data['id']
        raise ValueError(f"No email found with {field} matching {expected_value}.")
    
    def _validate_field(self, field, valid_fields):
        """Validate that the provided field is in the list of valid fields.
        
        Args:
            field: Field name to validate
            valid_fields: List of valid field names
            
        Raises:
            ValueError: If field is not in valid_fields
        """
        if field not in valid_fields:
            raise ValueError(f"Invalid field '{field}'. Must be one of: {', '.join(valid_fields)}")