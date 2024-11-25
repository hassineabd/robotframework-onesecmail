# https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=10

from enum import Enum

BASE_URL = "https://www.1secmail.com/api/v1/"
TIMEOUT = 10

class Action():
    """
    Action : are url endpoint action options
    """
    GENERATE_RANDOM_MAILBOX = 'genRandomMailbox'
    GET_DOMAIN_LIST = 'getDomainList'
    GET_MESSAGES = 'getMessages'
    READ_MESSAGE = 'readMessage'
    DOWNLOAD_ATTACHMENT = 'download'

class RequestParam():
    """
    RequestParam : are url endpoint parameter
    """
    ACTION = 'action'
    COUNT = 'count'
    LOGIN = 'login'
    DOMAIN = 'domain'
    ID = 'id'
    FILE = 'file'