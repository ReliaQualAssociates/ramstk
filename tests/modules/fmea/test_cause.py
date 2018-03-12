# -*- coding: utf-8 -*-
#
#       tests.modules.fmea.test_cause.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Cause class."""

from treelib import Tree

import pytest

from rtk.modules.fmea import dtmCause
from rtk.dao import RTKCause

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "weibullguy" Rowland'


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_cause_create(test_dao):
    """ __init__() should return instance of Cause data model. """
    DUT = dtmCause(test_dao)

    assert isinstance(DUT, dtmCause)
    assert DUT.last_id is None


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test01a_select_all(test_dao):
    """ select_all() should return a Tree() object populated with RTKCause instances on success. """
    DUT = dtmCause(test_dao)
    _tree = DUT.select_all(1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RTKCause)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test02a_select(test_dao):
    """ select() should return an instance of the RTKCause data model on success. """
    DUT = dtmCause(test_dao)
    DUT.select_all(1)
    _cause = DUT.select(1)

    assert isinstance(_cause, RTKCause)
    assert _cause.cause_id == 1
    assert _cause.description == 'Test Failure Cause #1'


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test02b_select_non_existent_id(test_dao):
    """ select() should return None when a non-existent Cause ID is requested. """
    DUT = dtmCause(test_dao)
    _cause = DUT.select(100)

    assert _cause is None


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test03a_insert(test_dao):
    """ insert() should return a zero error code on success when inserting a hardware failure Cause. """
    DUT = dtmCause(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(mechanism_id=1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test04a_delete(test_dao):
    """ delete() should return a zero error code on success. """
    DUT = dtmCause(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Deleting an item from the RTK Program "
                    "database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test04b_delete_non_existent_id(test_dao):
    """ delete() should return a non-zero error code when passed a Cause ID that doesn't exist. """
    DUT = dtmCause(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(300)

    assert _error_code == 2005
    assert _msg == ("  RTK ERROR: Attempted to delete non-existent Cause ID "
                    "300.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_05a_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmCause(test_dao)
    DUT.select_all(1)

    _cause = DUT.tree.get_node(1).data
    _cause.description = 'Test Failure Cause #1'

    _error_code, _msg = DUT.update(1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_05b_update_non_existent_id(test_dao):
    """ update() should return a non-zero error code when passed a Cause ID that doesn't exist. """
    DUT = dtmCause(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2006
    assert _msg == ("RTK ERROR: Attempted to save non-existent Cause ID 100.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test06a_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmCause(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")
