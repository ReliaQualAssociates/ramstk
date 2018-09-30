#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       ramstk.tests.modules.usage.test_environment.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Environment class."""

from treelib import Tree

import pytest

from ramstk.modules.usage import dtmEnvironment
from ramstk.dao import DAO
from ramstk.dao import RAMSTKEnvironment

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Doyle "weibullguy" Rowland'


@pytest.mark.integration
def test_create_data_model(test_dao):
    """ __init__() should create an Environment data model. """
    DUT = dtmEnvironment(test_dao)

    assert isinstance(DUT, dtmEnvironment)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)
    assert DUT.last_id is None


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a Tree() object populated with RAMSTKEnvironment instances on success. """
    DUT = dtmEnvironment(test_dao)

    _tree = DUT.do_select_all(phase_id=1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RAMSTKEnvironment)


@pytest.mark.integration
def test_do_select_all_non_existent_id(test_dao):
    """ do_select_all() should return an empty Tree() when passed an Environment ID that doesn't exist. """
    DUT = dtmEnvironment(test_dao)

    _tree = DUT.do_select_all(phase_id=100)

    assert isinstance(_tree, Tree)
    assert len(_tree.all_nodes()) == 1


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RAMSTKEnvironment data model on success. """
    DUT = dtmEnvironment(test_dao)
    DUT.do_select_all(phase_id=1)

    _environment = DUT.do_select(1)

    assert isinstance(_environment, RAMSTKEnvironment)
    assert _environment.environment_id == 1
    assert _environment.name == 'Condition Name'


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when passed an Environment ID that doesn't exist. """
    DUT = dtmEnvironment(test_dao)
    DUT.do_select_all(phase_id=1)

    assert DUT.do_select(100) is None


@pytest.mark.integration
def test_do_insert(test_dao):
    """ do_insert() should return a zero error code on success. """
    DUT = dtmEnvironment(test_dao)
    DUT.do_select_all(phase_id=1)

    _error_code, _msg = DUT.do_insert(phase_id=1)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program '
                    'database.')


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmEnvironment(test_dao)
    DUT.do_select_all(phase_id=1)
    DUT.do_insert(phase_id=1)

    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Deleting an item from the RAMSTK Program '
                    'database.')


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a Environment ID that doesn't exist. """
    DUT = dtmEnvironment(test_dao)
    DUT.do_select_all(phase_id=1)

    _error_code, _msg = DUT.do_delete(100)

    assert _error_code == 2005
    assert _msg == ('  RAMSTK ERROR: Attempted to delete non-existent '
                    'Environment ID 100.')


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmEnvironment(test_dao)
    DUT.do_select_all(phase_id=1)

    _environment = DUT.do_select(1)
    _environment.description = 'Test Mission'

    _error_code, _msg = DUT.do_update(1)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Updating the RAMSTK Program database.')


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed a Environment ID that doesn't exist. """
    DUT = dtmEnvironment(test_dao)
    DUT.do_select_all(phase_id=1)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2006
    assert _msg == ('RAMSTK ERROR: Attempted to save non-existent Environment ID '
                    '100.')


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmEnvironment(test_dao)
    DUT.do_select_all(phase_id=1)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating all records in the usage profile "
                    "environment table.")
