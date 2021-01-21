# -*- coding: utf-8 -*-
#
#       ramstk.logger.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Logger Module."""

# Standard Library Imports
import logging
import sys
from typing import Dict

# Third Party Imports
from pubsub import pub

LOGFORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(lineno)s : %(message)s')


class RAMSTKLogManager:
    """Class to manage logging of RAMSTK messages."""
    loggers: Dict[str, logging.Logger] = {}

    def __init__(self, log_file: str) -> None:
        """Initialize an instance of the LogManager.

        :param log_file: the absolute path to the log file to use with this
            log manager.
        """
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.log_file = log_file

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_log_fail_message,
                      'fail_connect_program_database')
        pub.subscribe(self._do_log_fail_message, 'fail_delete_environment')
        pub.subscribe(self._do_log_fail_message,
                      'fail_delete_failure_definition')
        pub.subscribe(self._do_log_fail_message, 'fail_delete_fmea')
        pub.subscribe(self._do_log_fail_message, 'fail_delete_function')
        pub.subscribe(self._do_log_fail_message, 'fail_delete_hazard')
        pub.subscribe(self._do_log_fail_message, 'fail_delete_mission')
        pub.subscribe(self._do_log_fail_message, 'fail_delete_mission_phase')
        pub.subscribe(self._do_log_fail_message, 'fail_delete_revision')
        pub.subscribe(self._do_log_fail_message, 'fail_import_module')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_action')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_cause')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_control')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_environment')
        pub.subscribe(self._do_log_fail_message,
                      'fail_insert_failure_definition')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_mechanism')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_mission')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_mission_phase')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_mode')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_function')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_hazard')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_hardware')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_validation')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_stakeholder')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_revision')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_requirement')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_opload')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_opstress')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_record')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_test_method')
        pub.subscribe(self._do_log_fail_message, 'fail_update_fmea')
        pub.subscribe(self._do_log_fail_message, 'fail_update_function')
        pub.subscribe(self._do_log_fail_message, 'fail_update_hardware')
        pub.subscribe(self._do_log_fail_message, 'fail_update_record')
        pub.subscribe(self._do_log_fail_message, 'fail_update_requirement')
        pub.subscribe(self._do_log_fail_message, 'fail_update_revision')

        pub.subscribe(self.do_log_debug, 'do_log_debug_msg')
        pub.subscribe(self.do_log_info, 'do_log_info_msg')
        pub.subscribe(self.do_log_warning, 'do_log_warning_msg')
        pub.subscribe(self.do_log_error, 'do_log_error_msg')
        pub.subscribe(self.do_log_critical, 'do_log_critical_msg')

        # Create a logger for the pypubsub fail_* messages.
        self.do_create_logger(__name__, "WARN")

    def _do_log_fail_message(self, error_message: str) -> None:
        """Log PyPubSub broadcast fail messages.

        :param error_message: the error message that was part of the
            broadcast package.
        :return: None
        :rtype: None
        """
        self.loggers[__name__].warning(error_message)

    @staticmethod
    def _get_console_handler(log_level: str) -> logging.Handler:
        """Create the log handler for console output.

        :return: _c_handler
        :rtype: :class:`logging.Handler`
        """
        _c_handler = logging.StreamHandler(sys.stdout)
        _c_handler.setLevel(log_level)
        _c_handler.setFormatter(LOGFORMAT)

        return _c_handler

    def _get_file_handler(self, log_level: str) -> logging.Handler:
        """Create the log handler for file output.

        :return: _f_handler
        :rtype: :class:`logging.Handler`
        """
        _f_handler = logging.FileHandler(self.log_file)
        _f_handler.setLevel(log_level)
        _f_handler.setFormatter(LOGFORMAT)

        return _f_handler

    def do_create_logger(self,
                         logger_name: str,
                         log_level: str,
                         to_tty: bool = False) -> None:
        """Create a logger instance.

        :param logger_name: the name of the logger used in the application.
        :param log_level: the level of messages to log.
        :param to_tty: boolean indicating whether this logger will
            also dump messages to the terminal.
        :return: None
        :rtype: None
        """
        _logger = logging.getLogger(logger_name)
        _logger.setLevel(log_level)

        _logger.addHandler(self._get_file_handler(log_level))
        if to_tty:
            _logger.addHandler(self._get_console_handler(log_level))

        self.loggers[logger_name] = _logger

    def do_log_debug(self, logger_name: str, message: str) -> None:
        """Log DEBUG level messages.

        :param logger_name: the name of the logger used in the application.
        :param message: the message to log.
        :return: None
        :rtype: None
        """
        if self.loggers[logger_name].isEnabledFor(logging.DEBUG):
            self.loggers[logger_name].debug(message)

    def do_log_exception(self, logger_name: str, exception: object) -> None:
        """Log EXCEPTIONS.

        :param logger_name: the name of the logger used in the application.
        :param exception: the exception to log.
        :return: None
        :rtype: None
        """
        if self.loggers[logger_name].isEnabledFor(logging.WARNING):
            self.loggers[logger_name].exception(exception)

    def do_log_info(self, logger_name: str, message: str) -> None:
        """Log INFO level messages.

        :param logger_name: the name of the logger used in the application.
        :param message: the message to log.
        :return: None
        :rtype: None
        """
        if self.loggers[logger_name].isEnabledFor(logging.INFO):
            self.loggers[logger_name].info(message)

    def do_log_warning(self, logger_name: str, message: str) -> None:
        """Log WARN level messages.

        :param logger_name: the name of the logger used in the application.
        :param message: the message to log.
        :return: None
        :rtype: None
        """
        if self.loggers[logger_name].isEnabledFor(logging.WARNING):
            self.loggers[logger_name].warning(message)

    def do_log_error(self, logger_name: str, message: str) -> None:
        """Log ERROR level messages.

        :param logger_name: the name of the logger used in the application.
        :param message: the message to log.
        :return: None
        :rtype: None
        """
        if self.loggers[logger_name].isEnabledFor(logging.ERROR):
            self.loggers[logger_name].error(message)

    def do_log_critical(self, logger_name: str, message: str) -> None:
        """Log CRITICAL level messages.

        :param logger_name: the name of the logger used in the application.
        :param message: the message to log.
        :return: None
        :rtype: None
        """
        self.loggers[logger_name].critical(message)
