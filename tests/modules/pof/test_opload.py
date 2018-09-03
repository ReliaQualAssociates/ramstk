# -*- coding: utf-8 -*-
#
#       tests.modules.pof.test_opload.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the PoF OpLoad class. """

from treelib import Tree

import pytest

from rtk.modules.pof import dtmOpLoad
from rtk.dao import DAO
from rtk.dao import RAMSTKOpLoad

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "Weibullguy" Rowland'


@pytest.mark.integration
def test_create_opload_data_model(test_dao):
    """ __init__() should return instance of OpLoad data model. """
    DUT = dtmOpLoad(test_dao)

    assert isinstance(DUT, dtmOpLoad)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a treelib Tree() on success when selecting OpLoads. """
    DUT = dtmOpLoad(test_dao)
    _tree = DUT.do_select_all(parent_id=1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RAMSTKOpLoad)


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RAMSTKOpLoad data model on success. """
    DUT = dtmOpLoad(test_dao)
    DUT.do_select_all(parent_id=1)

    _opload = DUT.do_select(1)

    assert isinstance(_opload, RAMSTKOpLoad)
    assert _opload.load_id == 1
    assert _opload.description == 'Test Operating Load'


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent OpLoad ID is requested. """
    DUT = dtmOpLoad(test_dao)
    DUT.do_select_all(parent_id=1)

    _opload = DUT.do_select('100')

    assert _opload is None


@pytest.mark.integration
def test_do_insert(test_dao):
    """ do_insert() should return a zero error code on success. """
    DUT = dtmOpLoad(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_insert(mechanism_id=1)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Adding one or more items to the RAMSTK "
                    "Program database.")
    assert DUT.last_id == 2


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmOpLoad(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Deleting an item from the RAMSTK Program "
                    "database.")


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a OpLoad ID that doesn't exist. """
    DUT = dtmOpLoad(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code == 2005
    assert _msg == ("  RAMSTK ERROR: Attempted to delete non-existent OpLoad "
                    "ID 300.")


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmOpLoad(test_dao)
    DUT.do_select_all(parent_id=1)

    _opload = DUT.do_select(1)
    _opload.pof_include = 1

    _error_code, _msg = DUT.do_update(1)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating the RAMSTK Program database.")


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed an OpLoad ID that doesn't exist. """
    DUT = dtmOpLoad(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2006
    assert _msg == ("RAMSTK ERROR: Attempted to save non-existent OpLoad ID 100.")


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmOpLoad(test_dao)
    DUT.do_select_all(parent_id=1)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating all operating loads in the damage "
                    "modeling worksheet.")
