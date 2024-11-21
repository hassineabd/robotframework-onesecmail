
import requests
from OneSecMail.utils.decorators import handle_request

class RequestHandler:

    @handle_request
    def get(self, full_url):
        response = requests.get(full_url)
        response.raise_for_status()
        return response