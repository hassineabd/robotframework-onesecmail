# constants.py

from enum import Enum

# Base URL
BASE_URL = "https://www.1secmail.com/api/v1/"

# Timeout in seconds
TIMEOUT = 10

# API Actions as Enum
class Action(Enum):
    GENERATE_RANDOM_MAILBOX = 'genRandomMailbox'
    GET_DOMAIN_LIST = 'getDomainList'
    GET_MESSAGES = 'getMessages'
    READ_MESSAGE = 'readMessage'
    DOWNLOAD_ATTACHMENT = 'download'
