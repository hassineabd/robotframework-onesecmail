from robot.api.exceptions import RobotError

class OneSecMailException(RobotError):
    """Base exception class for OneSecMail"""
    ROBOT_SUPPRESS_NAME = True

class MailboxGenerationError(OneSecMailException):
    """Raised when failed to generate a new mailbox"""
    ROBOT_SUPPRESS_NAME = True

class MessageNotFoundError(OneSecMailException):
    """Raised when a requested email message is not found"""
    ROBOT_SUPPRESS_NAME = True

class InvalidEmailFormatError(OneSecMailException):
    """Raised when email format is invalid"""
    ROBOT_SUPPRESS_NAME = True

class APIRateLimitError(OneSecMailException):
    """Raised when API rate limit is exceeded"""
    ROBOT_SUPPRESS_NAME = True

class InvalidCredentialsError(OneSecMailException):
    """Raised when login/domain combination is invalid"""
    ROBOT_SUPPRESS_NAME = True

class MessageDeleteError(OneSecMailException):
    """Raised when message deletion fails"""
    ROBOT_SUPPRESS_NAME = True

class APIConnectionError(OneSecMailException):
    """Raised when connection to API fails"""
    ROBOT_SUPPRESS_NAME = True

class CodeExtractionError(OneSecMailException):
    """Raised when code extraction from email body fails"""
    ROBOT_SUPPRESS_NAME = True