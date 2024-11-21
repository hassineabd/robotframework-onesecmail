from _constants import BASE_URL, TIMEOUT, Action
import requests

class OneSecMailClient:
    def __init__(self):
        self.session = requests.Session()

    def generate_random_mailbox(self, count=1):
        count = validate_count(count)
        params = {
            'action': Action.GENERATE_RANDOM_MAILBOX.value,
            'count': count
        }
        response = self.session.get(BASE_URL, params=params, timeout=TIMEOUT)
        self._verify_response_code(response)
        return response.json()
