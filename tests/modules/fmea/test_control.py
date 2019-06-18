# pylint: disable=protected-access
# -*- coding: utf-8 -*-
#
#       tests.modules.fmea.TestControl.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Control class."""

# Third Party Imports
import pytest
from treelib import Tree

# RAMSTK Package Imports
from ramstk.dao.programdb import RAMSTKControl
from ramstk.modules.fmea import dtmControl

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Doyle "weibullguy" Rowland'


@pytest.mark.integration
def test_create_data_model(test_dao):
    """ __init__() should return instance of Control data model. """
    DUT = dtmControl(test_dao)

    assert isinstance(DUT, dtmControl)
    assert DUT.last_id is None


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a Tree() object populated with RAMSTKControl instances on success. """
    DUT = dtmControl(test_dao)
    _tree = DUT.do_select_all(parent_id=1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RAMSTKControl)


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_elect() should return an instance of the RAMSTKControl data model on success. """
    DUT = dtmControl(test_dao)
    DUT.do_select_all(parent_id=1)
    _control = DUT.do_select(1)

    assert isinstance(_control, RAMSTKControl)
    assert _control.control_id == 1


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent Control ID is requested. """
    DUT = dtmControl(test_dao)
    DUT.do_select_all(parent_id=1)
    _control = DUT.do_select(100)

    assert _control is None


@pytest.mark.integration
def test_do_insert_control(test_dao):
    """ do_insert() should return False on success when inserting a Control into a hardware FMEA. """
    DUT = dtmControl(test_dao)
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
    DUT = dtmControl(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Deleting an item from the RAMSTK Program "
        "database."
    )


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a Control ID that doesn't exist. """
    DUT = dtmControl(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code, 2005
    assert _msg == (
        "  RAMSTK ERROR: Attempted to delete non-existent Control ID "
        "300."
    )


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmControl(test_dao)
    DUT.do_select_all(parent_id=1)

    _control = DUT.do_select(1)
    _control.description = 'Test Functional FMEA Control #1 for Cause ID 1'

    _error_code, _msg = DUT.do_update(1)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating the RAMSTK Program database.")


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed a Control ID that doesn't exist. """
    DUT = dtmControl(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2006
    assert _msg == (
        "RAMSTK ERROR: Attempted to save non-existent Control ID "
        "100."
    )


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmControl(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Updating all records in the FMEA controls "
        "table."
    )
