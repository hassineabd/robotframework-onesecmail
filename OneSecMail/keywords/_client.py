import requests
from robot.api import logger
from ._constants import BASE_URL, TIMEOUT, Action, RequestParam
from OneSecMail.utils.decorators import catch_on_request

class _OneSecMailClient():
    """
    A client for interacting with the OneSecMail API.
    """
    def __init__(self):
        self.session = requests.Session()
        self.base_url = BASE_URL
        self.timeout = TIMEOUT

    @catch_on_request
    def _generate_temporary_mailbox(self, count):
        params = {RequestParam.ACTION: Action.GENERATE_RANDOM_MAILBOX,
                    RequestParam.COUNT : count}
        return self.session.get(self.base_url, params=params)

    @catch_on_request
    def _get_messages(self, login, domain):
        params = {RequestParam.ACTION: Action.GET_MESSAGES,
                   RequestParam.LOGIN: login,
                   RequestParam.DOMAIN: domain}
        return self.session.get(self.base_url, params=params)

    @catch_on_request
    def _read_message(self, login, domain, email_id):
        params = {RequestParam.ACTION: Action.READ_MESSAGE,
                   RequestParam.LOGIN: login,
                   RequestParam.DOMAIN: domain,
                   RequestParam.ID: email_id}
        return self.session.get(self.base_url, params=params)

    @catch_on_request
    def _download_attachment(self, login, domain, email_id, filename):
        params = {RequestParam.ACTION: Action.DOWNLOAD_ATTACHMENT,
                   RequestParam.LOGIN: login,
                   RequestParam.DOMAIN: domain,
                   RequestParam.ID: email_id,
                   RequestParam.FILE: filename}
        return self.session.get(self.base_url, params=params)


