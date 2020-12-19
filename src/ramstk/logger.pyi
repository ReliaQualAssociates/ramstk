# Standard Library Imports
import logging
from typing import Any, Dict

LOGFORMAT: Any


class RAMSTKLogManager:
    loggers: Dict[str, logging.Logger] = ...
    log_file: Any = ...

    def __init__(self, log_file: str) -> None:
        ...

    def _do_log_fail_message(self, error_message: str) -> None:
        ...

    @staticmethod
    def _get_console_handler(log_level: str) -> logging.Handler:
        ...

    def _get_file_handler(self, log_level: str) -> logging.Handler:
        ...

    def do_create_logger(self,
                         logger_name: str,
                         log_level: str,
                         to_tty: bool = ...) -> None:
        ...

    def do_log_debug(self, logger_name: str, message: str) -> None:
        ...

    def do_log_exception(self, logger_name: str, exception: object) -> None:
        ...

    def do_log_info(self, logger_name: str, message: str) -> None:
        ...

    def do_log_warning(self, logger_name: str, message: str) -> None:
        ...

    def do_log_error(self, logger_name: str, message: str) -> None:
        ...

    def do_log_critical(self, logger_name: str, message: str) -> None:
        ...
