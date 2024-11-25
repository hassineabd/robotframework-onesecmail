from robot.api import logger

class _LoggingKeywords():
    def __init__(self):
        self._log_level = 'INFO'

    def _log(self, message, level='INFO'):
        level = level.upper()
        if level == 'INFO':
            logger.info(message)
        elif level == 'DEBUG':
            logger.debug(message)
        elif level == 'WARN':
            logger.warn(message)

    def _log_list(self, items, what='item'):
        msg = f"Found {len(items)} {what}{'s' if len(items) != 1 else ''}"
        self._log(msg)
        for index, item in enumerate(items, 1):
            self._log(f"{index}: {item}")
        return items