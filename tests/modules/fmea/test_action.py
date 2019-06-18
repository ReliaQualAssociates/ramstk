# pylint: disable=protected-access
# -*- coding: utf-8 -*-
#
#       tests.modules.fmea.test_action.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Action class."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from treelib import Tree

# RAMSTK Package Imports
from ramstk.dao.programdb import RAMSTKAction
from ramstk.modules.fmea import dtmAction

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2015 Doyle "weibullguy" Rowland'


@pytest.mark.integration
def test_create_data_model(test_dao):
    """ __init__() should return instance of Action data model. """
    DUT = dtmAction(test_dao)

    assert isinstance(DUT, dtmAction)
    assert DUT.last_id is None


@pytest.mark.integration
def test_do_select_all_functional(test_dao):
    """ do_select_all() should return a Tree() object populated with RAMSTKAction instances on success. """
    DUT = dtmAction(test_dao)
    _tree = DUT.do_select_all(parent_id=1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RAMSTKAction)


@pytest.mark.integration
def test_do_select_all_hardware(test_dao):
    """ do_select_all() should return a Tree() object populated with RAMSTKAction instances on success. """
    DUT = dtmAction(test_dao)
    _tree = DUT.do_select_all(parent_id=1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RAMSTKAction)


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RAMSTKAction data model on success. """
    DUT = dtmAction(test_dao)
    DUT.do_select_all(parent_id=1)
    _action = DUT.do_select(1)

    assert isinstance(_action, RAMSTKAction)
    assert _action.action_id == 1
    assert _action.action_due_date == date.today() + timedelta(days=30)


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent Action ID is requested. """
    DUT = dtmAction(test_dao)
    DUT.do_select_all(parent_id=1)
    _action = DUT.do_select(100)

    assert _action is None


@pytest.mark.integration
def test_do_insert_functional_mode(test_dao):
    """ do_insert() should return False on success when inserting a functional FMEA action. """
    DUT = dtmAction(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_insert(mode_id=1, cause_id=-1)

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program "
        "database."
    )


@pytest.mark.integration
def test_do_insert_hardware_mode(test_dao):
    """ do_insert() should return False on success when inserting a hardware FMEA action. """
    DUT = dtmAction(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_insert(mode_id=-1, cause_id=1)

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program "
        "database."
    )


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmAction(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Deleting an item from the RAMSTK Program "
        "database."
    )


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a Mode ID that doesn't exist. """
    DUT = dtmAction(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code == 2005
    assert _msg == (
        "  RAMSTK ERROR: Attempted to delete non-existent Action "
        "ID 300."
    )


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmAction(test_dao)
    DUT.do_select_all(parent_id=1)

    _action = DUT.tree.get_node(1).data
    _action.action_recommended = (
        b"Test Functional FMEA Recommended Action "
        b"#1 for Cause ID 1"
    )

    _error_code, _msg = DUT.do_update(1)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating the RAMSTK Program database.")


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed an Action ID that doesn't exist. """
    DUT = dtmAction(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2006
    assert _msg == (
        "RAMSTK ERROR: Attempted to save non-existent Action ID 100."
    )


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmAction(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Updating all records in the FMEA actions "
        "table."
    )
