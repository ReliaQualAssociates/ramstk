#!/usr/bin/env python
"""
Contains utility functions for interacting with the RTK application.  Import
this module in other modules that need to interact with the RTK application.
"""

# -*- coding: utf-8 -*-
#
#       rtk.Utilities.py is part of The RTK Project
#
# All rights reserved.

import sys
import os
import os.path

# Add localization support.
import gettext

# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)

# Import other RTK modules.
import Configuration

_ = gettext.gettext

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


def create_logger(log_name, log_level, log_file, to_tty=False):
    """
    This function creates a logger instance.

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

    _fh = logging.FileHandler(log_file)
    _fh.setLevel(log_level)

    _formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    _fh.setFormatter(_formatter)

    _logger.addHandler(_fh)

    if to_tty:
        _ch = logging.StreamHandler()
        _ch.setLevel(log_level)
        _ch.setFormatter(_formatter)
        _logger.addHandler(_ch)

    return _logger


def date_to_ordinal(date):
    """
    Converts date strings to ordinal dates for use in the database.

    :param str date: the date string to convert.
    :return: ordinal representation of the passed date.
    :rtype: int
    """

    from dateutil.parser import parse

    try:
        return parse(str(date)).toordinal()
    except(ValueError, TypeError):
        return parse('01/01/70').toordinal()


def dir_exists(directory):
    """
    Helper function to check if a directory exists.

    :param str directory: a string representing the directory path to check
                          for.
    :return: False if the directory does not exist, True otherwise.
    :rtype: bool
    """

    return os.path.isdir(directory)


def error_handler(message):
    """
    Function to convert string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:       # Type error
        _error_code = 10                                            # pragma: no cover
    elif 'invalid literal for int() with base 10' in message[0]:    # Value error
        _error_code = 10
    elif 'could not convert string to float' in message[0]:         # Value error
        _error_code = 10
    elif 'float division by zero' in message[0]:                    # Zero division error
        _error_code = 20
    elif 'integer division or modulo by zero' in message[0]:        # Zero division error
        _error_code = 20
    elif 'index out of range' in message[0]:                        # Index error
        _error_code = 40
    else:                                                           # Unhandled error
        print message
        _error_code = 1000                                          # pragma: no cover

    return _error_code


def file_exists(_file):
    """
    Helper function to check if a file exists.

    :param str _file: a string representing the filepath to check for.
    :return: True if the file exists, False otherwise.
    :rtype: bool
    """

    return os.path.isfile(_file)


def missing_to_default(field, default):
    """
    Function to convert missing values into default values.

    :param field: the original, missing, value.
    :param default: the new, default, value.
    :return: field; the new value if field is an empty string, the old value
             otherwise.
    :rtype: any
    """

    if field == '':
        return default
    else:
        return field


def none_to_string(string):
    """
    Converts None types to an empty string.

    :param str string: the string to convert.
    :return: string; the converted string.
    :rtype: str
    """

    if string is None or string == 'None':
        return ''
    else:
        return string


def ordinal_to_date(ordinal):
    """
    Converts ordinal dates to date strings in ISO-8601 format.  Defaults to
    the current date if a bad value is passed as the argument.

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
    Splits a colon-delimited string into its constituent parts.

    :param list string: the colon delimited string that needs to be split into
                        a list.
    :return: _strlist
    :rtype: list of strings
    """

    _strlist = string.rsplit(':')

    return _strlist


def string_to_boolean(string):
    """
    Converts string representations of TRUE/FALSE to an integer value for use
    in the database.

    :param str string: the string to convert.
    :return: _result
    :rtype: int
    """

    _result = 0

    _string = str(string)

    if(_string.lower() == 'true' or _string.lower() == 'yes' or
       _string.lower() == 't' or _string.lower() == 'y'):
        _result = 1

    return _result


def add_failure_modes(app, revision_id, assembly_id, category_id,
                      subcategory_id):
    """
    Function to add default failure modes to the selected component.

    :param rtk app: the running instance of the RTK application.
    :param int revision_id: the component revision ID.
    :param int assembly_id: the component assembly ID.
    :param int category_id: the component category ID.
    :param int subcategory_id: the component subcategory ID.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """
# TODO: Move this to the Hardware class.
    _err = False

    # Retrieve the default failure modes for the component from the common
    # database.
    _query = "SELECT fld_mode_id, fld_mode_description, fld_mode_ratio \
              FROM tbl_failure_modes \
              WHERE fld_category_id=%d \
              AND fld_subcategory_id=%d \
              AND fld_source=%d" % (category_id, subcategory_id,
                                    int(Configuration.RTK_MODE_SOURCE))
    _modes = app.COMDB.execute_query(_query, None, app.ComCnx)
    try:
        _n_modes = len(_modes)
    except TypeError:
        _n_modes = 0

    # Add the default failure modes to the open RTK Program database.
    _base_query = "INSERT INTO tbl_fmeca \
                   (fld_revision_id, fld_assembly_id, \
                    fld_mode_description, fld_mode_ratio) \
                   VALUES (%d, %d, '%s', %f)"
    for i in range(_n_modes):
        _query = _base_query % (revision_id, assembly_id, _modes[i][1],
                                _modes[i][2])
        if not app.DB.execute_query(_query, None, app.ProgCnx, commit=True):
            _err = True

    if _err:
        rtk_error(_(u"Problem adding one or more failure modes to the open "
                    u"RTK Program database."))
        return True

    return False
