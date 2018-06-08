# -*- coding: utf-8 -*-
#
#       tests.modules.fmea.test_mechanism.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the FMEA and PoF failure Mechanism class."""

from treelib import Tree

import pytest

from rtk.modules.fmea import dtmMechanism
from rtk.dao import DAO
from rtk.dao import RTKMechanism

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "Weibullguy" Rowland'


@pytest.mark.integration
def test_create_mechanism_data_model(test_dao):
    """ __init__() should return instance of Mechanism data model. """
    DUT = dtmMechanism(test_dao)

    assert isinstance(DUT, dtmMechanism)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a treelib Tree() on success when selecting Mechanisms. """
    DUT = dtmMechanism(test_dao)
    _tree = DUT.do_select_all(parent_id=4)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RTKMechanism)


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RTKMechanism data model on success. """
    DUT = dtmMechanism(test_dao)
    DUT.do_select_all(parent_id=4)

    _mechanism = DUT.do_select(1)

    assert isinstance(_mechanism, RTKMechanism)
    assert _mechanism.mechanism_id == 1
    assert _mechanism.description == 'Test Failure Mechanism #1 for Mode ID 4'


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent Mechanism ID is requested. """
    DUT = dtmMechanism(test_dao)
    DUT.do_select_all(parent_id=4)

    _mechanism = DUT.do_select('100')

    assert _mechanism is None


def test_do_insert_1(test_dao):
    """ do_insert() should return a zero error code on success. """
    DUT = dtmMechanism(test_dao)
    DUT.do_select_all(parent_id=4)

    _error_code, _msg = DUT.do_insert(mode_id=4)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK "
                    "Program database.")


@pytest.mark.integration
def test_do_insert_2(test_dao):
    """ do_insert() should return a zero error code on success. """
    DUT = dtmMechanism(test_dao)
    DUT.do_select_all(parent_id=4)

    _error_code, _msg = DUT.do_insert(mode_id=4)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK "
                    "Program database.")


def test_do_insert_3(test_dao):
    """ do_insert() should return a zero error code on success. """
    DUT = dtmMechanism(test_dao)
    DUT.do_select_all(parent_id=4)

    _error_code, _msg = DUT.do_insert(mode_id=4)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK "
                    "Program database.")


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmMechanism(test_dao)
    DUT.do_select_all(parent_id=4)

    __, __ = DUT.do_insert(mode_id=4)
    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Deleting an item from the RTK Program "
                    "database.")


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a Mechanism ID that doesn't exist. """
    DUT = dtmMechanism(test_dao)
    DUT.do_select_all(parent_id=4)

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code == 2005
    assert _msg == ("  RTK ERROR: Attempted to delete non-existent Mechanism "
                    "ID 300.")


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmMechanism(test_dao)
    DUT.do_select_all(parent_id=4)

    _mechanism = DUT.do_select(1)
    _mechanism.pof_include = 1

    _error_code, _msg = DUT.do_update(1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed an Mechanism ID that doesn't exist. """
    DUT = dtmMechanism(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2006
    assert _msg == (
        "RTK ERROR: Attempted to save non-existent Mechanism ID 100.")


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmMechanism(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating all records in the FMEA mechanisms "
                    "table.")
