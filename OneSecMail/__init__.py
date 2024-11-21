
from OneSecMail.keywords import *

__version__ = 0.1

class OneSecMail(
    _LoggingKeywords,
    _LanguageDetector,
    _OneSecMailKeywords
):
    """OneSecMail Library for Robot Framework
    
    API documentation: https://www.1secmail.com/api/
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 0.1