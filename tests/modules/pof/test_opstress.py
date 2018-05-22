# -*- coding: utf-8 -*-
#
#       tests.modules.pof.test_opstress.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the PoF OpStress class."""

from treelib import Tree

import pytest

from rtk.modules.pof import dtmOpStress
from rtk.dao import DAO
from rtk.dao import RTKOpStress

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "Weibullguy" Rowland'


@pytest.mark.integration
def test_create_opstress_data_model(test_dao):
    """ __init__() should return instance of OpStress data model. """
    DUT = dtmOpStress(test_dao)

    assert isinstance(DUT, dtmOpStress)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_select_all(test_dao):
    """select_all() should return a treelib Tree() on success when selecting OpStresss."""
    DUT = dtmOpStress(test_dao)
    _tree = DUT.select_all(1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RTKOpStress)


@pytest.mark.integration
def test_select(test_dao):
    """select() should return an instance of the RTKOpStress data model on success."""
    DUT = dtmOpStress(test_dao)
    DUT.select_all(1)

    _opstress = DUT.select(1)

    assert isinstance(_opstress, RTKOpStress)
    assert _opstress.stress_id == 1
    assert _opstress.description == 'Test Operating Stress'


@pytest.mark.integration
def test_select_non_existent_id(test_dao):
    """select() should return None when a non-existent OpStress ID is requested."""
    DUT = dtmOpStress(test_dao)
    DUT.select_all(1)

    _opstress = DUT.select('100')

    assert _opstress is None


@pytest.mark.integration
def test_insert(test_dao):
    """insert() should return a zero error code on success."""
    DUT = dtmOpStress(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(load_id=1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK "
                    "Program database.")
    assert DUT.last_id == 2


@pytest.mark.integration
def test_delete(test_dao):
    """delete() should return a zero error code on success."""
    DUT = dtmOpStress(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Deleting an item from the RTK Program "
                    "database.")


@pytest.mark.integration
def test_delete_non_existent_id(test_dao):
    """delete() should return a non-zero error code when passed a OpStress ID that doesn't exist."""
    DUT = dtmOpStress(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(300)

    assert _error_code == 2005
    assert _msg == ("  RTK ERROR: Attempted to delete non-existent OpStress "
                    "ID 300.")


@pytest.mark.integration
def test_update(test_dao):
    """update() should return a zero error code on success."""
    DUT = dtmOpStress(test_dao)
    DUT.select_all(1)

    _opstress = DUT.select(1)
    _opstress.pof_include = 1

    _error_code, _msg = DUT.update(1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
def test_update_non_existent_id(test_dao):
    """update() should return a non-zero error code when passed an OpStress ID that doesn't exist."""
    DUT = dtmOpStress(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2006
    assert _msg == (
        "RTK ERROR: Attempted to save non-existent OpStress ID 100.")


@pytest.mark.integration
def test_update_all(test_dao):
    """update_all() should return a zero error code on success."""
    DUT = dtmOpStress(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")
