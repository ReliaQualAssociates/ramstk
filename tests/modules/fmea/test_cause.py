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
def test_cause_create(test_dao):
    """ __init__() should return instance of Cause data model. """
    DUT = dtmCause(test_dao)

    assert isinstance(DUT, dtmCause)
    assert DUT.last_id is None


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a Tree() object populated with RTKCause instances on success. """
    DUT = dtmCause(test_dao)
    _tree = DUT.do_select_all(parent_id=1, functional=False)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(4).data, RTKCause)


@pytest.mark.integration
def test_select(test_dao):
    """ select() should return an instance of the RTKCause data model on success. """
    DUT = dtmCause(test_dao)
    DUT.do_select_all(parent_id=1, functional=False)
    _cause = DUT.select(4)

    assert isinstance(_cause, RTKCause)
    assert _cause.cause_id == 4
    assert _cause.description == 'Test Failure Cause #1 for Mechanism ID 1'


@pytest.mark.integration
def test_select_non_existent_id(test_dao):
    """ select() should return None when a non-existent Cause ID is requested. """
    DUT = dtmCause(test_dao)
    DUT.do_select_all(parent_id=1, functional=False)
    _cause = DUT.select(100)

    assert _cause is None


@pytest.mark.integration
def test_insert(test_dao):
    """ insert() should return a zero error code on success when inserting a hardware failure Cause. """
    DUT = dtmCause(test_dao)
    DUT.do_select_all(parent_id=1, functional=False)

    _error_code, _msg = DUT.do_insert(mode_id=-1, mechanism_id=1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")


@pytest.mark.integration
def test_delete(test_dao):
    """ delete() should return a zero error code on success. """
    DUT = dtmCause(test_dao)
    DUT.do_select_all(parent_id=1, functional=False)

    _error_code, _msg = DUT.delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Deleting an item from the RTK Program "
                    "database.")


@pytest.mark.integration
def test_delete_non_existent_id(test_dao):
    """ delete() should return a non-zero error code when passed a Cause ID that doesn't exist. """
    DUT = dtmCause(test_dao)
    DUT.do_select_all(parent_id=1, functional=False)

    _error_code, _msg = DUT.delete(300)

    assert _error_code == 2005
    assert _msg == ("  RTK ERROR: Attempted to delete non-existent Cause ID "
                    "300.")


@pytest.mark.integration
def test_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmCause(test_dao)
    DUT.do_select_all(parent_id=1, functional=False)

    _cause = DUT.tree.get_node(4).data
    _cause.description = 'Test Failure Cause #1 for Mechanism ID 1'

    _error_code, _msg = DUT.update(4)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
def test_update_non_existent_id(test_dao):
    """ update() should return a non-zero error code when passed a Cause ID that doesn't exist. """
    DUT = dtmCause(test_dao)
    DUT.do_select_all(parent_id=1, functional=False)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2006
    assert _msg == ("RTK ERROR: Attempted to save non-existent Cause ID 100.")


@pytest.mark.integration
def test_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmCause(test_dao)
    DUT.do_select_all(parent_id=1, functional=False)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")
