# -*- coding: utf-8 -*-
#
#       tests.modules.fmea.test_action.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Action class."""

from datetime import date, timedelta

from treelib import Tree

import pytest

from rtk.modules.fmea import dtmAction
from rtk.dao import RTKAction

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2015 Andrew "weibullguy" Rowland'


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_create_data_model(test_dao):
    """ __init__() should return instance of Action data model. """
    DUT = dtmAction(test_dao)

    assert isinstance(DUT, dtmAction)
    assert DUT.last_id is None


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_all_functional(test_dao):
    """ select_all() should return a Tree() object populated with RTKAction instances on success. """
    DUT = dtmAction(test_dao)
    _tree = DUT.select_all(1, functional=True)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RTKAction)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_all_hardware(test_dao):
    """ select_all() should return a Tree() object populated with RTKAction instances on success. """
    DUT = dtmAction(test_dao)
    _tree = DUT.select_all(1, functional=False)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(2).data, RTKAction)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select(test_dao):
    """ select() should return an instance of the RTKAction data model on success. """
    DUT = dtmAction(test_dao)
    DUT.select_all(1, functional=False)
    _action = DUT.select(2)

    assert isinstance(_action, RTKAction)
    assert _action.action_id == 2
    assert _action.action_due_date == date.today() + timedelta(days=30)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_non_existent_id(test_dao):
    """ select() should return None when a non-existent Action ID is requested. """
    DUT = dtmAction(test_dao)
    DUT.select_all(1, functional=False)
    _action = DUT.select(100)

    assert _action is None


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_insert_functional_mode(test_dao):
    """ insert() should return False on success when inserting a functional FMEA action. """
    DUT = dtmAction(test_dao)
    DUT.select_all(1, functional=True)

    _error_code, _msg = DUT.insert(mode_id=1, cause_id=-1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_insert_hardware_mode(test_dao):
    """ insert() should return False on success when inserting a hardware FMEA action. """
    DUT = dtmAction(test_dao)
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
    DUT = dtmAction(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Deleting an item from the RTK Program "
                    "database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_delete_non_existent_id(test_dao):
    """ delete() should return a non-zero error code when passed a Mode ID that doesn't exist. """
    DUT = dtmAction(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.delete(300)

    assert _error_code == 2005
    assert _msg == ("  RTK ERROR: Attempted to delete non-existent Action ID "
                    "300.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmAction(test_dao)
    DUT.select_all(1, functional=False)

    _action = DUT.tree.get_node(2).data
    _action.action_recommended = 'Do this stuff and do it now!!'

    _error_code, _msg = DUT.update(2)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_update_non_existent_id(test_dao):
    """ update() should return a non-zero error code when passed an Action ID that doesn't exist. """
    DUT = dtmAction(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2006
    assert _msg == ("RTK ERROR: Attempted to save non-existent Action ID 100.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmAction(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")
