# pylint: disable=protected-access
# -*- coding: utf-8 -*-
#
#       tests.modules.fmea.test_mode.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the Mode class."""

# Third Party Imports
import pytest
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKMode
from ramstk.modules.fmea import dtmMode

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Doyle "weibullguy" Rowland'


@pytest.mark.integration
def test_create(test_dao):
    """ __init__() should return instance of Mode data model. """
    DUT = dtmMode(test_dao)

    assert isinstance(DUT, dtmMode)
    assert DUT.last_id is None


@pytest.mark.integration
def test_do_select_all_functional(test_dao):
    """ do_select_all() should return a Tree() object populated with RAMSTKMode instances on success. """
    DUT = dtmMode(test_dao)
    _tree = DUT.do_select_all(parent_id=1, functional=True)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RAMSTKMode)


@pytest.mark.integration
def test_do_select_all_hardware(test_dao):
    """ do_select_all() should return a Tree() object populated with RAMSTKMode instances on success. """
    DUT = dtmMode(test_dao)
    _tree = DUT.do_select_all(parent_id=1, functional=False)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(4).data, RAMSTKMode)


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RAMSTKMode data model on success. """
    DUT = dtmMode(test_dao)
    DUT.do_select_all(parent_id=1, functional=False)
    _mode = DUT.do_select(4)

    assert isinstance(_mode, RAMSTKMode)
    assert _mode.mode_id == 4
    assert _mode.description == ("System Test Failure Mode")


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent Mode ID is requested. """
    DUT = dtmMode(test_dao)
    DUT.do_select_all(parent_id=1, functional=False)
    _mode = DUT.do_select(100)

    assert _mode is None


@pytest.mark.integration
def test_do_insert_functional_mode(test_dao):
    """ do_insert() should return a zero error code on success when inserting a functional failure Mode. """
    DUT = dtmMode(test_dao)
    DUT.do_select_all(parent_id=1, functional=True)

    _error_code, _msg = DUT.do_insert(function_id=1, hardware_id=-1)

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program "
        "database."
    )


@pytest.mark.integration
def test_do_insert_hardware_mode(test_dao):
    """ do_insert() should return a zero error code on success when inserting a hardware failure Mode. """
    DUT = dtmMode(test_dao)
    DUT.do_select_all(parent_id=1, functional=False)

    _error_code, _msg = DUT.do_insert(function_id=-1, hardware_id=1)

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program "
        "database."
    )


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmMode(test_dao)
    DUT.do_select_all(parent_id=1, functional=False)
    DUT.do_insert(function_id=-1, hardware_id=1)

    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Deleting an item from the RAMSTK Program "
        "database."
    )


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a Mode ID that doesn't exist. """
    DUT = dtmMode(test_dao)
    DUT.do_select_all(parent_id=1, functional=False)

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code == 2005
    assert _msg == (
        "  RAMSTK ERROR: Attempted to delete non-existent Mode ID "
        "300."
    )


@pytest.mark.integration
def test_do_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmMode(test_dao)
    DUT.do_select_all(parent_id=1, functional=False)

    _mode = DUT.do_select(4)
    _mode.isolation_method = 'Method to isolate the failure.'

    _error_code, _msg = DUT.do_update(4)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating the RAMSTK Program database.")


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed a Mode ID that doesn't exist. """
    DUT = dtmMode(test_dao)
    DUT.do_select_all(parent_id=1, functional=False)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2006
    assert _msg == ("RAMSTK ERROR: Attempted to save non-existent Mode ID 100.")


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmMode(test_dao)
    DUT.do_select_all(parent_id=1, functional=False)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Updating all records in the FMEA modes "
        "table."
    )
