# -*- coding: utf-8 -*-
#
#       tests.test_utilities.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Utilities module algorithms and models."""

# Standard Library Imports
import glob
import os
import platform
import tempfile
from datetime import datetime

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk import (
    boolean_to_integer, date_to_ordinal, dir_exists, file_exists,
    get_install_prefix, integer_to_boolean, none_to_default,
    none_to_string, ordinal_to_date, split_string, string_to_boolean
)

TEMPDIR = tempfile.gettempdir()

try:
    VIRTUAL_ENV = glob.glob(os.environ['VIRTUAL_ENV'])[0]
except KeyError:
    if platform.system() == 'Linux':
        VIRTUAL_ENV = os.getenv('HOME') + '/.local'
    elif platform.system() == 'Windows':
        VIRTUAL_ENV = os.getenv('TEMP')


def test_split_string():
    """split_string() should return a list of strings split at the colon
    (:)."""
    _strings = split_string('one:two:three')

    assert _strings[0] == 'one'
    assert _strings[1] == 'two'
    assert _strings[2] == 'three'


def test_none_to_string_None():  # pylint: disable=invalid-name
    """none_to_string() should return an empty string when passed None."""
    assert none_to_string(None) == ''


def test_none_to_string_none():
    """none_to_string() should return an empty string when passed 'None'."""
    assert none_to_string('None') == ''


def test_none_to_string_string():
    """none_to_string should return the original string when passed anything
    other than None or 'None'."""
    assert none_to_string('The original string') == 'The original string'


def test_string_to_boolean_True():  # pylint: disable=invalid-name
    """string_to_boolean() should return a 1 when passed True."""
    assert string_to_boolean(True) == 1


def test_string_to_boolean_yes():
    """string_to_boolean() should return a 1 when passed 'yes'."""
    assert string_to_boolean('yes') == 1


def test_string_to_boolean_t():
    """string_to_boolean() should return a 1 when passed 't'."""
    assert string_to_boolean('t') == 1


def test_string_to_boolean_y():
    """string_to_boolean() should return a 1 when passed 'y'."""
    assert string_to_boolean('y') == 1


def test_string_to_boolean_False():  # pylint: disable=invalid-name
    """string_to_boolean() should return a 0 when passed False."""
    assert string_to_boolean(False) == 0


def test_date_to_ordinal():
    """date_to_ordinal() should return an integer when passed a date."""
    assert date_to_ordinal('2016-05-27') == 736111


def test_date_to_ordinal_wrong_type():
    """date_to_ordinal() should return the ordinal for 1970-01-01 when passed
    the wrong type."""
    assert date_to_ordinal(None) == 719163


def test_ordinal_to_date():
    """ordinal_to_date() should return the date in YYYY-MM-DD format when
    passed an ordinal value."""
    assert ordinal_to_date(736111) == '2016-05-27'


def test_ordinal_to_date_value_error():
    """ordinal_to_date() should return the current date in YYYY-MM-DD format
    when passed a non-ordinal value."""
    _ordinal = datetime.now().toordinal()
    _today = str(datetime.fromordinal(int(_ordinal)).strftime('%Y-%m-%d'))

    _date = ordinal_to_date('Today')

    assert _date == _today


def test_dir_exists():
    """dir_exists() should return True if the directory exists."""
    assert dir_exists(TEMPDIR)


def test_dir_does_not_exist():
    """dir_exists() should return False if the directory does not exists."""
    assert not dir_exists('/NotThere')


def test_file_exists():
    """file_exists() should return True if the file exists."""
    _testlog = './test_info.log'
    assert file_exists(_testlog)


def test_file_does_not_exist():
    """file_exists() should return False if the file does not exists."""
    assert not file_exists(TEMPDIR + '/NotThere.txt')


@pytest.mark.unit
def test_none_to_default():
    """none_to_default() should return the default value if the original value
    is None."""
    assert none_to_default(None, 10) == 10


@pytest.mark.unit
def test_none_to_default_not_none():
    """none_to_default() should return the original value if it is not
    missing."""
    assert none_to_default(40, 10) == 40


@pytest.mark.unit
def test_boolean_to_integer_true_to_one():
    """boolean_to_integer() should return a one when passed True."""
    assert boolean_to_integer(True) == 1


@pytest.mark.unit
def test_boolean_to_integer_false_to_zero():
    """boolean_to_integer() should return a zero when passed False."""
    assert boolean_to_integer(False) == 0


@pytest.mark.unit
def test_boolean_to_integer_any_text_to_one():
    """boolean_to_integer() should return a one when passed a string."""
    assert boolean_to_integer('ChillyMonga') == 1


@pytest.mark.unit
def test_boolean_to_integer_any_number_to_one():
    """boolean_to_integer() should return a one when passed any number > 0."""
    assert boolean_to_integer(486) == 1


@pytest.mark.unit
def test_integer_to_boolean_zero_to_false():
    """integer_to_boolean() should return False when passed any number <= 0."""
    assert not integer_to_boolean(0)
    assert not integer_to_boolean(-1)


@pytest.mark.unit
def test_integer_to_boolean_any_number_to_true():
    """integer_to_boolean() should return True when passed anything number >
    0."""
    assert integer_to_boolean(1)
    assert integer_to_boolean(188)


@pytest.mark.unit
def test_integer_to_boolean_type_error():
    """integer_to_boolean() should raise a TypeError when passed a string."""
    with pytest.raises(TypeError):
        integer_to_boolean('1')


@pytest.mark.unit
def test_get_install_prefix():
    """"get_install_prefix() should return the path the file is installed."""
    _path = get_install_prefix()

    assert _path == VIRTUAL_ENV
