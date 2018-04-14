# -*- coding: utf-8 -*-
#
#       tests.test_utilities.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Utilities module algorithms and models."""

from datetime import datetime
import logging

import pytest

from rtk.Utilities import (create_logger, split_string, none_to_string,
                           string_to_boolean, date_to_ordinal, ordinal_to_date,
                           dir_exists, file_exists, none_to_default,
                           error_handler)

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


def test_create_logger():
    """create_logger() should return a logging.Logger instance."""
    _log = create_logger("test.debug", logging.DEBUG, '/tmp/test.log')

    assert isinstance(_log, logging.Logger)
    assert isfile('/tmp/test.log')


def test_create_logger_to_tty():
    """create_logger() should return a logging.Logger instance."""
    _log = create_logger("test.debug", logging.DEBUG, '', True)

    assert isinstance(_log, logging.Logger)
    assert isfile('/tmp/test.log')


def test_split_string():
    """split_string() should return a list of strings split at the colon (:)."""
    _strings = split_string('one:two:three')

    assert _strings[0] == 'one'
    assert _strings[1] == 'two'
    assert _strings[2] == 'three'


def test_none_to_string_None():
    """none_to_string() should return an empty string when passed None."""
    assert none_to_string(None) == ''


def test_none_to_string_none():
    """none_to_string() should return an empty string when passed 'None'."""
    assert none_to_string('None') == ''


def test_none_to_string_string():
    """none_to_string should return the original string when passed anything other than None or 'None'."""
    assert none_to_string('The original string') == 'The original string'


def test_string_to_boolean_True():
    """ string_to_boolean() should return a 1 when passed True. """
    assert string_to_boolean(True) == 1


def test_string_to_boolean_yes():
    """ string_to_boolean() should return a 1 when passed 'yes'. """
    assert string_to_boolean('yes') == 1


def test_string_to_boolean_t():
    """ string_to_boolean() should return a 1 when passed 't'. """
    assert string_to_boolean('t') == 1


def test_string_to_boolean_y():
    """ string_to_boolean() should return a 1 when passed 'y'. """
    assert string_to_boolean('y') == 1


def test_string_to_boolean_False():
    """ string_to_boolean() should return a 0 when passed False. """
    assert string_to_boolean(False) == 0


def test_date_to_ordinal():
    """ date_to_ordinal() should return an integer when passed a date. """
    assert date_to_ordinal('2016-05-27') == 736111


def test_date_to_ordinal_wrong_type():
    """ date_to_ordinal() should return the ordinal for 1970-01-01 when passed the wrong type. """
    assert date_to_ordinal(None) == 719163


def test_ordinal_to_date():
    """ ordinal_to_date() should return the date in YYYY-MM-DD format when passed an ordinal value. """
    assert ordinal_to_date(736111) == '2016-05-27'


def test_ordinal_to_date_value_error():
    """ ordinal_to_date() should return the current date in YYYY-MM-DD format when passed a non-ordinal value. """
    _ordinal = datetime.now().toordinal()
    _today = str(datetime.fromordinal(int(_ordinal)).strftime('%Y-%m-%d'))

    _date = ordinal_to_date('Today')

    assert _date == _today


def test_dir_exists():
    """ dir_exists() should return True if the directory exists. """
    assert dir_exists('/tmp')


def test_dir_does_not_exist():
    """ dir_exists() should return False if the directory does not exists. """
    assert not dir_exists('/NotThere')


def test_file_exists():
    """ file_exists() should return True if the file exists. """
    assert file_exists('/tmp/test.log')


def test_file_does_not_exist():
    """ file_exists() should return False if the file does not exists. """
    assert not file_exists('/tmp/NotThere.txt')


@pytest.mark.unit
@pytest.mark.utilities
def test_none_to_default():
    """ none_to_default() should return the default value if the original value is None. """
    assert none_to_default(None, 10) == 10


@pytest.mark.unit
@pytest.mark.utilities
def test_none_to_default_not_none():
    """ none_to_default() should return the original value if it is not missing. """
    assert none_to_default(40, 10) == 40


def test_error_handler_type_error():
    """ error_handler() should return a 10 error code when passed a TypeError string. """
    _error_code = error_handler(
        ['The argument must be a string or a number dude!'])
    assert _error_code == 10


def test_error_handler_value_error():
    """ error_handler() should return a 10 error code when passed a ValueError string. """
    _error_code = error_handler(
        ['That is invalid literal for int() with base 10'])
    assert _error_code == 10

    _error_code = error_handler(['I could not convert string to float'])
    assert _error_code == 10


def test_error_handler_zero_division_error():
    """ error_handler() should return a 20 error code when passed a ZeroDivisionError string. """
    _error_code = error_handler(['float division by zero dunna work dude'])
    assert _error_code == 20

    _error_code = error_handler(
        ['That was integer division or modulo by zero'])
    assert _error_code == 20


def test_error_handler_index_error():
    """ error_handler() should return a 40 error code when passed a IndexError string. """
    _error_code = error_handler(['That index out of range'])
    assert _error_code == 40


def test_error_handler_default():
    """ error_handler() should return a 1000 error code when passed a error string it can't parse. """
    _error_code = error_handler(['Some kinda error message'])
    assert _error_code == 1000
