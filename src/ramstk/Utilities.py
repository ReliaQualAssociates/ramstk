# -*- coding: utf-8 -*-
#
#       ramstk.Utilities.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Utility functions for interacting with the RAMSTK application."""

import os
import os.path
import sys

# Add localization support.
import gettext

_ = gettext.gettext

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2017 Doyle "weibullguy" Rowland'


class OutOfRangeError(Exception):
    """Exception raised when an input value is outside legal limits."""

    def __init__(self, message):
        """
        Initialize OutOfRangeError instance.

        :param str message: the message to display to the user when this
                            exception is raised.
        """
        Exception.__init__(self)

        self.message = message


class NoParentError(Exception):
    """Exception raised when a parent element does not exist."""

    pass


class NoMatrixError(Exception):
    """Exception raised when no Matrices are returned."""

    pass


def create_logger(log_name, log_level, log_file, to_tty=False):
    """
    Create a logger instance.

    :param str log_name: the name of the log used in the application.
    :param str log_level: the level of messages to log.
    :param str log_file: the full path of the log file for this logger instance
                         to write to.
    :keyword boolean to_tty: boolean indicating whether this logger will also
                             dump messages to the terminal.
    :return: _logger
    :rtype:
    """
    import logging

    _logger = logging.getLogger(log_name)
    _formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if log_level == 'DEBUG':
        log_level = logging.ERROR
    elif log_level == 'INFO':
        log_level = logging.INFO

    if not to_tty:
        _fh = logging.FileHandler(log_file)
        _fh.setLevel(log_level)
        _fh.setFormatter(_formatter)

        _logger.addHandler(_fh)
    else:
        _ch = logging.StreamHandler()
        _ch.setLevel(log_level)
        _ch.setFormatter(_formatter)

        _logger.addHandler(_ch)

    return _logger


def date_to_ordinal(date):
    """
    Convert date strings to ordinal dates for use in the database.

    :param str date: the date string to convert.
    :return: ordinal representation of the passed date.
    :rtype: int
    """
    from dateutil.parser import parse

    try:
        return parse(str(date)).toordinal()
    except (ValueError, TypeError):
        return parse('01/01/70').toordinal()


def dir_exists(directory):
    """
    Check if a directory exists.

    :param str directory: a string representing the directory path to check
                          for.
    :return: False if the directory does not exist, True otherwise.
    :rtype: bool
    """
    return os.path.isdir(directory)


def error_handler(message):
    """
    Convert string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """
    if 'argument must be a string or a number' in message[0]:  # Type error
        _error_code = 10  # pragma: no cover
    elif 'invalid literal for int() with base 10' in message[0]:  # Value error
        _error_code = 10
    elif 'could not convert string to float' in message[0]:  # Value error
        _error_code = 10
    elif 'float division by zero' in message[0]:  # Zero division error
        _error_code = 20
    elif 'integer division or modulo by zero' in message[
            0]:  # Zero division error
        _error_code = 20
    elif 'index out of range' in message[0]:  # Index error
        _error_code = 40
    else:  # Unhandled error
        print(message)
        _error_code = 1000  # pragma: no cover

    return _error_code


def file_exists(_file):
    """
    Check if a file exists.

    :param str _file: a string representing the filepath to check for.
    :return: True if the file exists, False otherwise.
    :rtype: bool
    """
    return os.path.isfile(_file)


def missing_to_default(field, default):
    """
    Convert missing values into default values.

    :param field: the original, missing, value.
    :param default: the new, default, value.
    :return: field; the new value if field is an empty string, the old value
             otherwise.
    :rtype: any
    """
    return none_to_default(field, default)


def none_to_default(field, default):
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


def none_to_string(string):
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


def ordinal_to_date(ordinal):
    """
    Convert ordinal dates to date strings in ISO-8601 format.

    Defaults to the current date if a bad value is passed as the argument.

    :param int ordinal: the ordinal date to convert.
    :return: the ISO-8601 date representation of the passed ordinal.
    :rtype: date
    """
    from datetime import datetime

    try:
        return str(datetime.fromordinal(int(ordinal)).strftime('%Y-%m-%d'))
    except ValueError:
        ordinal = datetime.now().toordinal()
        return str(datetime.fromordinal(int(ordinal)).strftime('%Y-%m-%d'))


def split_string(string):
    """
    Split a colon-delimited string into its constituent parts.

    :param list string: the colon delimited string that needs to be split into
                        a list.
    :return: _strlist
    :rtype: list of strings
    """
    _strlist = string.rsplit(':')

    return _strlist


def boolean_to_integer(boolean):
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


def integer_to_boolean(integer):
    """
    Convert an integer to boolean value.

    Any value greater than zero is returned as True, all others are returned as
    False.

    :param int integer: the integer to convert.
    :return: _result
    :rtype: bool
    """
    _result = False

    if integer > 0:
        _result = True

    return _result


def string_to_boolean(string):
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


def prefix(join=None):
    """Return the prefix that this code was installed into."""
    _return = False

    # constants for this execution
    _path = os.path.abspath(__file__)
    _name = os.path.basename(os.path.dirname(_path))
    _this = os.path.basename(_path)

    # rule set
    _rules = [
        # to match: /usr/lib/python2.5/site-packages/project/prefix.py
        # or: /usr/local/lib/python2.6/dist-packages/project/prefix.py
        lambda x: x == 'lib',
        lambda x: x == ('python%s' % sys.version[:3]),
        lambda x: x in ['site-packages', 'dist-packages'],
        lambda x: x == _name,  # 'project'
        lambda x: x == _this,  # 'prefix.py'
    ]

    # matching engine
    while len(_rules) > 0:
        (_path, _token) = os.path.split(_path)
        _rule = _rules.pop()
        if not _rule(_token):
            _return = True

    # usually returns: /usr/ or /usr/local/ (but without slash postfix)
    if join is None:
        _return = _path
    else:
        _return = os.path.join(_path, join)  # add on join if it exists!

    return _return


def name(pop=[], suffix=None):
    """
    Return the name of this particular project.

    If pop is a list containing more than one element, name() will remove those
    items from the path tail before deciding on the project name. If there is
    an element which does not exist in the path tail, then raise.  If a suffix
    is specified, then it is removed if found at end.
    """
    _path = os.path.dirname(os.path.abspath(__file__))
    if isinstance(pop, str):
        pop = [pop]  # force single strings to list

    while len(pop) > 0:
        (_path, _tail) = os.path.split(_path)
        if pop.pop() != _tail:
            raise ValueError('Element doesnʼt match path tail.')

    _path = os.path.basename(_path)
    if suffix is not None and _path.endswith(suffix):
        _path = _path[0:-len(suffix)]

    return _path
