from contextlib import contextmanager
from robot.api import logger
from datetime import datetime
import time

class EmailContextManager:
    def __init__(self, onesec_instance):
        self.onesec = onesec_instance

    @contextmanager
    def temporary_mailbox(self):
        """
        Context manager for temporary email usage. 
        Generates a mailbox and provides it for the duration of the context.
        """
        try:
            email_address = self.onesec.generate_random_mailbox(1)[0]
            login, domain = email_address.split('@')
            logger.info(f"Created temporary mailbox: {email_address}")
            
            yield email_address, login, domain
            
        finally:
            logger.info(f"Finished using temporary mailbox: {email_address}")

    @contextmanager
    def wait_for_email(self, login, domain, timeout=60, interval=5, subject=None, sender=None):
        """
        Context manager that waits for an email to arrive.
        """
        start_time = datetime.now()
        
        try:
            while (datetime.now() - start_time).seconds < timeout:
                messages = self.onesec.get_messages(login, domain)
                for msg in messages:
                    if (subject is None or msg['subject'] == subject) and \
                       (sender is None or msg['from'] == sender):
                        message_id = msg['id']
                        email_content = self.onesec.read_message(login, domain, message_id)
                        logger.info(f"Found matching email with ID: {message_id}")
                        yield email_content
                        return
                
                time.sleep(interval)
            
            raise TimeoutError(f"No matching email found within {timeout} seconds")
            
        finally:
            logger.info("Finished waiting for email")