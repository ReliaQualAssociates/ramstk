# -*- coding: utf-8 -*-
#
#       ramstk.utilities.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Utility functions for interacting with the RAMSTK application."""

# Standard Library Imports
import gettext
import logging
import os
import os.path
import sys
from datetime import datetime
from typing import Any, List

# Third Party Imports
from dateutil.parser import parse

_ = gettext.gettext


def create_logger(log_name: str,
                  log_level: str,
                  log_file: str,
                  to_tty: bool = False) -> object:
    """
    Create a logger instance.

    :param str log_name: the name of the log used in the application.
    :param str log_level: the level of messages to log.
    :param str log_file: the full path of the log file for this logger instance
        to write to.
    :keyword boolean to_tty: boolean indicating whether this logger will also
        dump messages to the terminal.
    :return: _logger
    :rtype: object
    """
    _logger = logging.getLogger(log_name)
    _formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if not to_tty:
        _handler = logging.FileHandler(log_file)
    else:
        _handler = logging.StreamHandler()
    _handler.setFormatter(_formatter)

    _logger.addHandler(_handler)
    _logger.setLevel(log_level)

    return _logger


def date_to_ordinal(date: str) -> int:
    """
    Convert date strings to ordinal dates for use in the database.

    :param str date: the date string to convert.
    :return: ordinal representation of the passed date.
    :rtype: int
    """
    try:
        return parse(str(date)).toordinal()
    except (ValueError, TypeError):
        return parse('01/01/70').toordinal()


def dir_exists(directory: str) -> bool:
    """
    Check if a directory exists.

    :param str directory: a string representing the directory path to check
                          for.
    :return: False if the directory does not exist, True otherwise.
    :rtype: bool
    """
    return os.path.isdir(directory)


def file_exists(_file: str) -> bool:
    """
    Check if a file exists.

    :param str _file: a string representing the filepath to check for.
    :return: True if the file exists, False otherwise.
    :rtype: bool
    """
    return os.path.isfile(_file)


def none_to_default(field: Any, default: Any) -> Any:
    """
    Convert None values into default values.

    :param field: the original value that may be None.
    :param default: the new, default, value.
    :return: field; the new value if field is None, the old value
             otherwise.
    :rtype: any
    """
    _return = field
    if field is None:
        _return = default

    return _return


def none_to_string(string: None) -> str:
    """
    Convert None types to an empty string.

    :param str string: the string to convert.
    :return: string; the converted string.
    :rtype: str
    """
    _return = string
    if string is None or string == 'None':
        _return = ''

    return _return


def ordinal_to_date(ordinal: int) -> str:
    """
    Convert ordinal dates to date strings in ISO-8601 format.

    Defaults to the current date if a bad value is passed as the argument.

    :param int ordinal: the ordinal date to convert.
    :return: the ISO-8601 date representation of the passed ordinal.
    :rtype: str
    """
    try:
        return str(datetime.fromordinal(int(ordinal)).strftime('%Y-%m-%d'))
    except ValueError:
        ordinal = datetime.now().toordinal()
        return str(datetime.fromordinal(int(ordinal)).strftime('%Y-%m-%d'))


def split_string(string: str) -> List[str]:
    """
    Split a colon-delimited string into its constituent parts.

    :param str string: the colon delimited string that needs to be split into
        a list.
    :return: _strlist
    :rtype: list of strings
    """
    _strlist = string.rsplit(':')

    return _strlist


# TODO: This is probably not needed and should be retired.
def boolean_to_integer(boolean: bool) -> int:
    """
    Convert boolean representations of TRUE/FALSE to an integer value.

    :param bool boolean: the boolean to convert.
    :return: _result
    :rtype: int
    """
    _result = 0

    if boolean:
        _result = 1

    return _result


# TODO: This is probably not needed and should be retired.
def integer_to_boolean(integer: int) -> bool:
    """
    Convert an integer to boolean value.

    Any value greater than zero is returned as True, all others are returned as
    False.

    :param int integer: the integer to convert.
    :return: _result
    :rtype: bool
    :raise: TypeError if passed a string.
    """
    _result = False

    if integer > 0:
        _result = True

    return _result


def string_to_boolean(string: str) -> bool:
    """
    Convert string representations of TRUE/FALSE to an boolean value.

    :param str string: the string to convert.
    :return: _result
    :rtype: bool
    """
    _result = False

    _string = str(string)

    if (_string.lower() == 'true' or _string.lower() == 'yes'
            or _string.lower() == 't' or _string.lower() == 'y'):
        _result = True

    return _result


def get_install_prefix() -> str:
    """Return the prefix that this code was installed into."""
    # Constants for this execution
    _path = os.path.abspath(__file__)
    _name = os.path.basename(os.path.dirname(_path))
    _this = os.path.basename(_path)

    # Rule set
    _rules: List[Any] = [
        # to match: /usr/lib/python2.5/site-packages/project/prefix.py
        # or: /usr/local/lib/python2.6/dist-packages/project/prefix.py
        lambda x: x == 'lib',
        lambda x: x == ('python%s' % sys.version[:3]),
        lambda x: x in ['site-packages', 'dist-packages'],
        lambda x: x == _name,  # 'project'
        lambda x: x == _this,  # 'prefix.py'
    ]

    # Matching engine
    while _rules:
        (_path, _token) = os.path.split(_path)
        _rule = _rules.pop()
        if not _rule(_token):
            _path = '/usr/'

    return _path
