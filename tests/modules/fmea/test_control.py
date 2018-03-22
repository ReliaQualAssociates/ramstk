# -*- coding: utf-8 -*-
#
#       tests.modules.fmea.TestControl.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Control class."""

from treelib import Tree

import pytest

from rtk.modules.fmea import dtmControl
from rtk.dao import RTKControl

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "weibullguy" Rowland'


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_create_data_model(test_dao):
    """ __init__() should return instance of Control data model. """
    DUT = dtmControl(test_dao)

    assert isinstance(DUT, dtmControl)
    assert DUT.last_id is None


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_all_functional(test_dao):
    """ select_all() should return a Tree() object populated with RTKControl instances on success. """
    DUT = dtmControl(test_dao)
    _tree = DUT.select_all(1, functional=True)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RTKControl)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_all_hardware(test_dao):
    """ select_all() should return a Tree() object populated with RTKControl instances on success. """
    DUT = dtmControl(test_dao)
    _tree = DUT.select_all(1, functional=False)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(4).data, RTKControl)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select(test_dao):
    """ select() should return an instance of the RTKControl data model on success. """
    DUT = dtmControl(test_dao)
    DUT.select_all(1, functional=False)
    _control = DUT.select(4)

    assert isinstance(_control, RTKControl)
    assert _control.control_id == 4


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_non_existent_id(test_dao):
    """ select() should return None when a non-existent Control ID is requested. """
    DUT = dtmControl(test_dao)
    DUT.select_all(1, functional=False)
    _control = DUT.select(100)

    assert _control is None


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_insert_functional_control(test_dao):
    """ insert() should return False on success when inserting a Control into a functional FMEA. """
    DUT = dtmControl(test_dao)
    DUT.select_all(1, functional=True)

    _error_code, _msg = DUT.insert(mode_id=1, cause_id=-1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_insert_hardware_control(test_dao):
    """ insert() should return False on success when inserting a Control into a hardware FMEA. """
    DUT = dtmControl(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.insert(mode_id=-1, cause_id=1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_delete(test_dao):
    """ delete() should return a zero error code on success. """
    DUT = dtmControl(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Deleting an item from the RTK Program "
                    "database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_delete_non_existent_id(test_dao):
    """ delete() should return a non-zero error code when passed a Control ID that doesn't exist. """
    DUT = dtmControl(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.delete(300)

    assert _error_code, 2005
    assert _msg == ("  RTK ERROR: Attempted to delete non-existent Control ID "
                    "300.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmControl(test_dao)
    DUT.select_all(1, functional=False)

    _control = DUT.select(4)
    _control.description = 'Functional FMEA control.'

    _error_code, _msg = DUT.update(4)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_update_non_existent_id(test_dao):
    """ update() should return a non-zero error code when passed a Control ID that doesn't exist. """
    DUT = dtmControl(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2006
    assert _msg == ("RTK ERROR: Attempted to save non-existent Control ID "
                    "100.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmControl(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")
