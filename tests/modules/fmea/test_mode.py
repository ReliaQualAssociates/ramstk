# -*- coding: utf-8 -*-
#
#       tests.modules.fmea.test_mode.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the Mode class."""

from treelib import Tree

import pytest

from rtk.modules.fmea import dtmMode
from rtk.dao import RTKMode

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "weibullguy" Rowland'


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_create(test_dao):
    """ __init__() should return instance of Mode data model. """
    DUT = dtmMode(test_dao)

    assert isinstance(DUT, dtmMode)
    assert DUT.last_id is None


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_all_functional(test_dao):
    """ select_all() should return a Tree() object populated with RTKMode instances on success. """
    DUT = dtmMode(test_dao)
    _tree = DUT.select_all(1, functional=True)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RTKMode)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_all_hardware(test_dao):
    """ select_all() should return a Tree() object populated with RTKMode instances on success. """
    DUT = dtmMode(test_dao)
    _tree = DUT.select_all(1, functional=False)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(4).data, RTKMode)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select(test_dao):
    """ select() should return an instance of the RTKMode data model on success. """
    DUT = dtmMode(test_dao)
    DUT.select_all(1, functional=False)
    _mode = DUT.select(4)

    assert isinstance(_mode, RTKMode)
    assert _mode.mode_id == 4
    assert _mode.description == ("System Test Failure Mode")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_non_existent_id(test_dao):
    """ select() should return None when a non-existent Mode ID is requested. """
    DUT = dtmMode(test_dao)
    DUT.select_all(1, functional=False)
    _mode = DUT.select(100)

    assert _mode is None


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_insert_functional_mode(test_dao):
    """ insert() should return a zero error code on success when inserting a functional failure Mode. """
    DUT = dtmMode(test_dao)
    DUT.select_all(1, functional=True)

    _error_code, _msg = DUT.insert(function_id=1, hardware_id=-1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_insert_hardware_mode(test_dao):
    """ insert() should return a zero error code on success when inserting a hardware failure Mode. """
    DUT = dtmMode(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.insert(function_id=-1, hardware_id=1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_delete(test_dao):
    """ delete() should return a zero error code on success. """
    DUT = dtmMode(test_dao)
    DUT.select_all(1, functional=False)
    DUT.insert(function_id=-1, hardware_id=1)

    _error_code, _msg = DUT.delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Deleting an item from the RTK Program "
                    "database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_delete_non_existent_id(test_dao):
    """ delete() should return a non-zero error code when passed a Mode ID that doesn't exist. """
    DUT = dtmMode(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.delete(300)

    assert _error_code == 2005
    assert _msg == ("  RTK ERROR: Attempted to delete non-existent Mode ID "
                    "300.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmMode(test_dao)
    DUT.select_all(1, functional=False)

    _mode = DUT.select(4)
    _mode.isolation_method = 'Method to isolate the failure.'

    _error_code, _msg = DUT.update(4)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_update_non_existent_id(test_dao):
    """ update() should return a non-zero error code when passed a Mode ID that doesn't exist. """
    DUT = dtmMode(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2006
    assert _msg == ("RTK ERROR: Attempted to save non-existent Mode ID 100.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmMode(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")
