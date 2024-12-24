import os
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.BuiltIn import RobotNotRunningError
from robot.api import logger

class _LoggingKeywords():
    @property
    def _log_level(self):
        try:
            return BuiltIn().get_variable_value("${LOG_LEVEL}", default='INFO')
        except RobotNotRunningError:
            return 'INFO'

    def _log(self, message, level='INFO'):
        """Log messages with specified level (INFO by default)"""
        level = level.upper()
        if level == 'INFO':
            logger.info(message)
        elif level == 'DEBUG':
            logger.debug(message)
        elif level == 'WARN':
            logger.warn(message)
        elif level == 'ERROR':
            logger.error(message)

    def _log_list(self, items, what='item'):
        """Log a list of items with a summary count"""
        msg = [f'Found {len(items)} {what}{"s" if len(items) != 1 else ""}.']
        for index, item in enumerate(items):
            msg.append(f'{index + 1}: {item}')
        self._log('\n'.join(msg))
        return items
    
    def _get_log_dir(self):
        variables = BuiltIn().get_variables()
        logfile = variables['${LOG FILE}']
        if logfile != 'NONE':
            return os.path.dirname(logfile)
        return variables['${OUTPUTDIR}']