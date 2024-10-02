# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.test_exceptions.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Exception module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.exceptions import DataAccessError, OutOfRangeError, RAMSTKError


@pytest.mark.unit
def test_ramstk_base_exception():
    """Should return a base exception class."""
    dut = RAMSTKError(msg="This is a test exception message.")

    assert dut.msg == "This is a test exception message."


@pytest.mark.unit
def test_ramstk_base_exception_no_message():
    """Should return a base exception class with the default message."""
    dut = RAMSTKError()

    assert dut.msg == "An error occurred with RAMSTK."


@pytest.mark.unit
def test_data_access_exception():
    """Should return a DataAccessError exception class."""
    dut = DataAccessError(msg="This is a test data access error message.")

    assert dut.msg == "This is a test data access error message."


@pytest.mark.unit
def test_data_access_exception_no_message():
    """Should return a DataAccessError exception class with the default message."""
    dut = DataAccessError()

    assert dut.msg == "Data access error."


@pytest.mark.unit
def test_out_of_range_exception():
    """Should return a OutOfRangeError exception class."""
    dut = OutOfRangeError(msg="This is a test out of range error message.")

    assert dut.msg == "This is a test out of range error message."


@pytest.mark.unit
def test_out_of_range_exception_no_message():
    """Should return a OutOfRangeError exception class with the default message."""
    dut = OutOfRangeError()

    assert dut.msg == "Input value is out of the allowed range."
