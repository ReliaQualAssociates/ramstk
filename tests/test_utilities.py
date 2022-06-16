# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.test_utilities.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
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
    boolean_to_integer,
    date_to_ordinal,
    deprecated,
    dir_exists,
    file_exists,
    get_install_prefix,
    integer_to_boolean,
    none_to_default,
    none_to_string,
    ordinal_to_date,
    split_string,
    string_to_boolean,
)

TEMPDIR = tempfile.gettempdir()

try:
    VIRTUAL_ENV = glob.glob(os.environ["VIRTUAL_ENV"])[0]
except IndexError:
    VIRTUAL_ENV = os.environ["VIRTUAL_ENV"]
except KeyError:
    if platform.system() == "Linux":
        VIRTUAL_ENV = os.getenv("HOME") + "/.local"
    elif platform.system() == "Windows":
        VIRTUAL_ENV = os.getenv("TEMP")


@pytest.mark.unit
def test_split_string():
    """Should return a list of strings split at the colon (:)."""
    _strings = split_string("one:two:three")

    assert _strings[0] == "one"
    assert _strings[1] == "two"
    assert _strings[2] == "three"


@pytest.mark.unit
def test_none_to_string_none():
    """Should return an empty string when passed None."""
    assert none_to_string(None) == ""


@pytest.mark.unit
def test_none_to_string_string_none():
    """Should return an empty string when passed 'None'."""
    assert none_to_string("None") == ""


@pytest.mark.unit
def test_none_to_string_string():
    """Should return the original string when passed anything other than None."""
    assert none_to_string("The original string") == "The original string"


@pytest.mark.unit
def test_string_to_boolean_true():
    """Should True when passed True."""
    assert string_to_boolean("True")


@pytest.mark.unit
def test_string_to_boolean_yes():
    """Should return True when passed 'yes'."""
    assert string_to_boolean("yes")


@pytest.mark.unit
def test_string_to_boolean_t():
    """Should return True when passed 't'."""
    assert string_to_boolean("t")


@pytest.mark.unit
def test_string_to_boolean_y():
    """Should return True when passed 'y'."""
    assert string_to_boolean("y")


@pytest.mark.unit
def test_string_to_boolean_false():
    """Should return False when passed False."""
    assert not string_to_boolean("False")


@pytest.mark.unit
def test_string_to_boolean_boolean():
    """Should True when passed boolean True."""
    assert string_to_boolean(True)


@pytest.mark.unit
def test_date_to_ordinal():
    """Should return an integer when passed a date."""
    assert date_to_ordinal("2016-05-27") == 736111


@pytest.mark.unit
def test_date_to_ordinal_wrong_type():
    """Should return the ordinal for 1970-01-01 when passed the wrong type."""
    assert date_to_ordinal(None) == 719163


@pytest.mark.unit
def test_ordinal_to_date():
    """Should return the date in YYYY-MM-DD format when passed an ordinal value."""
    assert ordinal_to_date(736111) == "2016-05-27"


@pytest.mark.unit
def test_ordinal_to_date_type_error():
    """Should return current date in YYYY-MM-DD format when passed a non-ordinal."""
    _ordinal = datetime.now().toordinal()
    _today = str(datetime.fromordinal(int(_ordinal)).strftime("%Y-%m-%d"))

    _date = ordinal_to_date("Today")

    assert _date == _today


@pytest.mark.unit
def test_dir_exists():
    """Should return True if the directory exists."""
    assert dir_exists(TEMPDIR)


@pytest.mark.unit
def test_dir_does_not_exist():
    """Should return False if the directory does not exist."""
    assert not dir_exists("/NotThere")


@pytest.mark.unit
@pytest.mark.usefixtures("test_text_file_function")
def test_file_exists(test_text_file_function):
    """Should return True if the file exists."""
    assert file_exists(test_text_file_function)


@pytest.mark.unit
def test_file_does_not_exist():
    """Should return False if the file does not exist."""
    assert not file_exists(TEMPDIR + "/NotThere.txt")


@pytest.mark.unit
def test_none_to_default():
    """Should return the default value if the original value is None."""
    assert none_to_default(None, 10) == 10


@pytest.mark.unit
def test_none_to_default_not_none():
    """Should return the original value if it is not missing."""
    assert none_to_default(40, 10) == 40


@pytest.mark.unit
def test_boolean_to_integer_true_to_one():
    """Should return a one when passed True."""
    assert boolean_to_integer(True) == 1


@pytest.mark.unit
def test_boolean_to_integer_false_to_zero():
    """Should return a zero when passed False."""
    assert boolean_to_integer(False) == 0


@pytest.mark.unit
def test_boolean_to_integer_any_text_to_one():
    """Should return a one when passed a string."""
    assert boolean_to_integer("ChillyMonga") == 1


@pytest.mark.unit
def test_boolean_to_integer_any_number_to_one():
    """Should return a one when passed any number > 0."""
    assert boolean_to_integer(486) == 1


@pytest.mark.unit
def test_integer_to_boolean_zero_to_false():
    """Should return False when passed any number <= 0."""
    assert not integer_to_boolean(0)
    assert not integer_to_boolean(-1)


@pytest.mark.unit
def test_integer_to_boolean_any_number_to_true():
    """Should return True when passed anything number > 0."""
    assert integer_to_boolean(1)
    assert integer_to_boolean(188)


@pytest.mark.unit
def test_integer_to_boolean_type_error():
    """Should raise a TypeError when passed a string."""
    with pytest.raises(TypeError):
        integer_to_boolean("1")


@pytest.mark.unit
def test_get_install_prefix():
    """Should return the path the file is installed."""
    _path = get_install_prefix()

    assert _path == VIRTUAL_ENV


@pytest.mark.unit
def test_deprecated():
    """Should raise a deprecation warning when a function is decorated."""

    @deprecated
    def dummy_add(x, y):
        """Test function for deprecated function."""
        return x + y

    with pytest.warns(DeprecationWarning):
        _sum = dummy_add(1, 1)

    assert _sum == 2
