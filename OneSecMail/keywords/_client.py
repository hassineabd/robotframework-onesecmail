import requests
from ._constants import BASE_URL, TIMEOUT, Action
from OneSecMail.utils.decorators import request
from .keywordgroup import KeywordGroup

class _OneSecMailClient(KeywordGroup):
    """
    A client for interacting with the OneSecMail API.
    """
    def __init__(self):
        self.session = requests.Session()
        self.base_url = BASE_URL
        self.timeout = TIMEOUT

    @request
    def _generate_temporary_mailbox(self, count):
        params = {'action': Action.GENERATE_RANDOM_MAILBOX.value,
                   'count': count}
        return self.session.get(self.base_url, params=params)

    @request
    def _get_messages(self, login, domain):
        params = {'action': Action.GET_MESSAGES.value,
                   'login': login,
                   'domain': domain}
        return self.session.get(self.base_url, params=params)

    @request
    def _read_message(self, login, domain, message_id):
        params = {'action': Action.READ_MESSAGE.value,
                   'login': login,
                   'domain': domain,
                   'id': message_id}
        return self.session.get(self.base_url, params=params)

    @request
    def _download_attachment(self, login, domain, message_id, filename):
        params = {'action': Action.DOWNLOAD_ATTACHMENT.value,
                   'login': login,
                   'domain': domain,
                   'id': message_id,
                   'file': filename}
        return self.session.get(self.base_url, params=params)
