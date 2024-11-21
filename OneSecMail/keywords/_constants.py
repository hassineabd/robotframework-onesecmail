from enum import Enum

BASE_URL = "https://www.1secmail.com/api/v1/"
TIMEOUT = 10

class Action(Enum):
    GENERATE_RANDOM_MAILBOX = 'genRandomMailbox'
    GET_DOMAIN_LIST = 'getDomainList'
    GET_MESSAGES = 'getMessages'
    READ_MESSAGE = 'readMessage'
    DOWNLOAD_ATTACHMENT = 'download'