#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.modules.usage.test_environment.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Environment class."""

from treelib import Tree

import pytest

from rtk.modules.usage import dtmEnvironment
from rtk.dao import DAO
from rtk.dao import RTKEnvironment

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_create_data_model(test_dao):
    """ __init__() should create an Environment data model. """
    DUT = dtmEnvironment(test_dao)

    assert isinstance(DUT, dtmEnvironment)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)
    assert DUT.last_id is None


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_select_all(test_dao):
    """ select_all() should return a Tree() object populated with RTKEnvironment instances on success. """
    DUT = dtmEnvironment(test_dao)

    _tree = DUT.select_all(1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RTKEnvironment)


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_select_all_non_existent_id(test_dao):
    """ select_all() should return an empty Tree() when passed an Environment ID that doesn't exist. """
    DUT = dtmEnvironment(test_dao)

    _tree = DUT.select_all(100)

    assert isinstance(_tree, Tree)
    assert len(_tree.all_nodes()) == 1


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_select(test_dao):
    """ select() should return an instance of the RTKEnvironment data model on success. """
    DUT = dtmEnvironment(test_dao)
    DUT.select_all(1)

    _environment = DUT.select(1)

    assert isinstance(_environment, RTKEnvironment)
    assert _environment.environment_id == 1
    assert _environment.name == 'Condition Name'


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_select_non_existent_id(test_dao):
    """ select() should return None when passed an Environment ID that doesn't exist. """
    DUT = dtmEnvironment(test_dao)
    DUT.select_all(1)

    assert DUT.select(100) is None


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_insert(test_dao):
    """ insert() should return a zero error code on success. """
    DUT = dtmEnvironment(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(phase_id=1)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Adding one or more items to the RTK Program '
                    'database.')


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_delete(test_dao):
    """ delete() should return a zero error code on success. """
    DUT = dtmEnvironment(test_dao)
    DUT.select_all(1)
    DUT.insert(phase_id=1)

    _error_code, _msg = DUT.delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Deleting an item from the RTK Program '
                    'database.')


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_delete_non_existent_id(test_dao):
    """ delete() should return a non-zero error code when passed a Environment ID that doesn't exist. """
    DUT = dtmEnvironment(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(100)

    assert _error_code == 2005
    assert _msg == ('  RTK ERROR: Attempted to delete non-existent '
                    'Environment ID 100.')


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmEnvironment(test_dao)
    DUT.select_all(1)

    _environment = DUT.select(1)
    _environment.description = 'Test Mission Description'

    _error_code, _msg = DUT.update(1)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_update_non_existent_id(test_dao):
    """ update() should return a non-zero error code when passed a Environment ID that doesn't exist. """
    DUT = dtmEnvironment(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2006
    assert _msg == ('RTK ERROR: Attempted to save non-existent Environment ID '
                    '100.')


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmEnvironment(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')
