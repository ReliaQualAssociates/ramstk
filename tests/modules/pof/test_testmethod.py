# -*- coding: utf-8 -*-
#
#       tests.modules.pof.test_testmethod.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the PoF TestMethod class."""

from treelib import Tree

import pytest

from rtk.modules.pof import dtmTestMethod
from rtk.dao import DAO
from rtk.dao import RTKTestMethod

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "Weibullguy" Rowland'


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.pof
def test_create_testmethod_data_model(test_dao):
    """ __init__() should return instance of TestMethod data model. """
    DUT = dtmTestMethod(test_dao)

    assert isinstance(DUT, dtmTestMethod)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.pof
def test_select_all(test_dao):
    """select_all() should return a treelib Tree() on success when selecting TestMethods."""
    DUT = dtmTestMethod(test_dao)
    _tree = DUT.select_all(1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RTKTestMethod)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.pof
def test_select(test_dao):
    """select() should return an instance of the RTKTestMethod data model on success."""
    DUT = dtmTestMethod(test_dao)
    DUT.select_all(1)

    _testmethod = DUT.select(1)

    assert isinstance(_testmethod, RTKTestMethod)
    assert _testmethod.test_id == 1
    assert _testmethod.description == 'Test Test Method'


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.pof
def test_select_non_existent_id(test_dao):
    """select() should return None when a non-existent TestMethod ID is requested."""
    DUT = dtmTestMethod(test_dao)
    DUT.select_all(1)

    _testmethod = DUT.select('100')

    assert _testmethod is None


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.pof
def test_insert(test_dao):
    """insert() should return a zero error code on success."""
    DUT = dtmTestMethod(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(stress_id=1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK "
                    "Program database.")
    # If this script is run stand-alone, it will be 2.
    # If this is run as part of a larger suite, it will be 4.
    try:
        assert DUT.last_id == 2
    except AssertionError:
        assert DUT.last_id == 4


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.pof
def test_delete(test_dao):
    """delete() should return a zero error code on success."""
    DUT = dtmTestMethod(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Deleting an item from the RTK Program "
                    "database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.pof
def test_delete_non_existent_id(test_dao):
    """delete() should return a non-zero error code when passed a TestMethod ID that doesn't exist."""
    DUT = dtmTestMethod(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(300)

    assert _error_code == 2005
    assert _msg == ("  RTK ERROR: Attempted to delete non-existent TestMethod "
                    "ID 300.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.pof
def test_update(test_dao):
    """update() should return a zero error code on success."""
    DUT = dtmTestMethod(test_dao)
    DUT.select_all(1)

    _testmethod = DUT.select(1)
    _testmethod.pof_include = 1

    _error_code, _msg = DUT.update(1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.pof
def test_update_non_existent_id(test_dao):
    """update() should return a non-zero error code when passed an TestMethod ID that doesn't exist."""
    DUT = dtmTestMethod(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2006
    assert _msg == (
        "RTK ERROR: Attempted to save non-existent TestMethod ID 100.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.pof
def test_update_all(test_dao):
    """update_all() should return a zero error code on success."""
    DUT = dtmTestMethod(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")
