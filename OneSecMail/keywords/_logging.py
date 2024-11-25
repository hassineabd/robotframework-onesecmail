from robot.api import logger

class _LoggingKeywords:
    LOG_LEVELS = {
        'DEBUG': ['DEBUG'],
        'INFO': ['DEBUG', 'INFO'],
        'WARN': ['DEBUG', 'INFO', 'WARN']
    }

    def __init__(self):
        self._log_level = 'INFO'

    def _log(self, message, level='INFO'):
        level = level.upper()
        if level not in self.LOG_LEVELS:
            return
        
        if self._log_level in self.LOG_LEVELS[level]:
            getattr(logger, level.lower())(message)

    def debug(self, message):
        self._log(message, 'DEBUG')

    def info(self, message):
        self._log(message, 'INFO')

    def warn(self, message):
        self._log(message, 'WARN')