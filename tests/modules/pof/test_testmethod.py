# -*- coding: utf-8 -*-
#
#       tests.modules.pof.test_testmethod.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the PoF TestMethod class. """

from treelib import Tree

import pytest

from ramstk.modules.pof import dtmTestMethod
from ramstk.dao import DAO
from ramstk.dao import RAMSTKTestMethod

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Doyle "weibullguy" Rowland'


@pytest.mark.integration
def test_create_testmethod_data_model(test_dao):
    """ __init__() should return instance of TestMethod data model. """
    DUT = dtmTestMethod(test_dao)

    assert isinstance(DUT, dtmTestMethod)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a treelib Tree() on success when selecting TestMethods. """
    DUT = dtmTestMethod(test_dao)
    _tree = DUT.do_select_all(parent_id=1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RAMSTKTestMethod)


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RAMSTKTestMethod data model on success. """
    DUT = dtmTestMethod(test_dao)
    DUT.do_select_all(parent_id=1)

    _testmethod = DUT.do_select(1)

    assert isinstance(_testmethod, RAMSTKTestMethod)
    assert _testmethod.test_id == 1
    assert _testmethod.description == 'Test Test Method'


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent TestMethod ID is requested. """
    DUT = dtmTestMethod(test_dao)
    DUT.do_select_all(parent_id=1)

    _testmethod = DUT.do_select('100')

    assert _testmethod is None


@pytest.mark.integration
def test_do_insert(test_dao):
    """ do_insert() should return a zero error code on success. """
    DUT = dtmTestMethod(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_insert(load_id=1)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Adding one or more items to the RAMSTK "
                    "Program database.")
    # If this script is run stand-alone, it will be 2.
    # If this is run as part of a larger suite, it will be 4.
    try:
        assert DUT.last_id == 2
    except AssertionError:
        assert DUT.last_id == 4


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmTestMethod(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Deleting an item from the RAMSTK Program "
                    "database.")


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a TestMethod ID that doesn't exist. """
    DUT = dtmTestMethod(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code == 2005
    assert _msg == ("  RAMSTK ERROR: Attempted to delete non-existent TestMethod "
                    "ID 300.")


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmTestMethod(test_dao)
    DUT.do_select_all(parent_id=1)

    _testmethod = DUT.do_select(1)
    _testmethod.pof_include = 1

    _error_code, _msg = DUT.do_update(1)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating the RAMSTK Program database.")


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed an TestMethod ID that doesn't exist. """
    DUT = dtmTestMethod(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2006
    assert _msg == (
        "RAMSTK ERROR: Attempted to save non-existent TestMethod ID 100.")


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmTestMethod(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating all test methods in the damage "
                    "modeling worksheet.")
