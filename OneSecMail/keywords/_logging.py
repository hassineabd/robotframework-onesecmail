# -*- coding: utf-8 -*-

import os
import base64
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.BuiltIn import RobotNotRunningError
from robot.api import logger

class _LoggingKeywords():
    LOG_LEVEL_DEBUG = ['DEBUG']
    LOG_LEVEL_INFO = ['DEBUG', 'INFO']
    LOG_LEVEL_WARN = ['DEBUG', 'INFO', 'WARN']

    @property
    def _log_level(self):
        try:
            level = BuiltIn().get_variable_value("${LOG_LEVEL}", default='DEBUG')
        except RobotNotRunningError:
            level = 'DEBUG'
        return level

    def _debug(self, message):
        if self._log_level in self.LOG_LEVEL_DEBUG:
            logger.debug(message)

    def _info(self, message):
        if self._log_level in self.LOG_LEVEL_INFO:
            logger.info(message)

    def _warn(self, message):
        if self._log_level in self.LOG_LEVEL_WARN:
            logger.warn(message)

    def _log(self, message, level='INFO'):
        level = level.upper()
        if (level == 'INFO'):
            self._info(message)
        elif (level == 'DEBUG'):
            self._debug(message)
        elif (level == 'WARN'):
            self._warn(message)
        elif (level == 'HTML'):
            self._html(message)

    def _log_list(self, items, what='item'):
        msg = ['Altogether %d %s%s.' % (len(items), what, ['s', ''][len(items) == 1])]
        for index, item in enumerate(items):
            msg.append('%d: %s' % (index+1, item))
        self._info('\n'.join(msg))
        return items
