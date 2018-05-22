#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.failure_definition.TestFailureDefinition.py is part of The
#       RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing Failure Definition module algorithms and models."""

from treelib import Tree

import pytest

from rtk.modules.failure_definition import (dtmFailureDefinition,
                                            dtcFailureDefinition)
from rtk.dao import DAO
from rtk.dao import RTKFailureDefinition

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

ATTRIBUTES = {
    'definition_id': 1,
    'definition': 'Test Failure Definition',
    'revision_id': 1
}


@pytest.mark.integration
def test_create_data_model(test_dao):
    """ __init__ should return instance of a FailureDefition data model. """
    DUT = dtmFailureDefinition(test_dao)

    assert isinstance(DUT, dtmFailureDefinition)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_select_all(test_dao):
    """ select_all() should return a Tree() object populated with RTKFailureDefinitions instances on success. """
    DUT = dtmFailureDefinition(test_dao)
    _tree = DUT.select_all(1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RTKFailureDefinition)


@pytest.mark.integration
def test_select(test_dao):
    """ select() should return an instance of the RTKFailureDefinition data model on success. """
    DUT = dtmFailureDefinition(test_dao)
    DUT.select_all(1)

    _definition = DUT.select(1)

    assert isinstance(_definition, RTKFailureDefinition)
    assert _definition.definition_id == 1
    assert _definition.definition == 'Failure Definition'


@pytest.mark.integration
def test_select_non_existent_id(test_dao):
    """ select() should return None when a non-existent Definition ID is requested. """
    DUT = dtmFailureDefinition(test_dao)
    _definition = DUT.select(100)

    assert _definition is None


@pytest.mark.integration
def test_insert(test_dao):
    """ insert() should return False on success. """
    DUT = dtmFailureDefinition(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(revision_id=1)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Adding one or more items to the RTK Program '
                    'database.')
    assert DUT.last_id == 2


@pytest.mark.integration
def test_delete(test_dao):
    """ delete() should return a zero error code on success. """
    DUT = dtmFailureDefinition(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Deleting an item from the RTK Program '
                    'database.')


@pytest.mark.integration
def test_delete_non_existent_id(test_dao):
    """ delete() should return a non-zero error code when passed a Revision ID that doesn't exist. """
    DUT = dtmFailureDefinition(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(300)

    assert _error_code == 2005
    assert _msg == ('  RTK ERROR: Attempted to delete non-existent Failure '
                    'Definition ID 300.')


@pytest.mark.integration
def test_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmFailureDefinition(test_dao)
    DUT.select_all(1)

    _definition = DUT.select(1)
    _definition.definition = 'Test Failure Definition'

    _error_code, _msg = DUT.update(1)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')


@pytest.mark.integration
def test_update_non_existent_id(test_dao):
    """ update() should return a non-zero error code when passed a Failure Definition ID that doesn't exist. """
    DUT = dtmFailureDefinition(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2207
    assert _msg == ('RTK ERROR: Attempted to save non-existent Failure '
                    'Definition ID 100.')


@pytest.mark.integration
def test_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmFailureDefinition(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')


@pytest.mark.integration
def test_controller_create(test_dao, test_configuration):
    """ __init__() should return a Failure Definition Data Controller. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcFailureDefinition)
    assert isinstance(DUT._dtm_data_model, dtmFailureDefinition)


@pytest.mark.integration
def test_request_select_all(test_dao, test_configuration):
    """ request_select_all() should return a Tree of RTKFailureDefinition models. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    _tree = DUT.request_select_all(1)

    assert isinstance(_tree.get_node(1).data, RTKFailureDefinition)


@pytest.mark.integration
def test_request_select(test_dao, test_configuration):
    """ request_select() should return an RTKFailureDefinition model. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert isinstance(DUT.request_select(1), RTKFailureDefinition)


@pytest.mark.integration
def test_request_non_existent_id(test_dao, test_configuration):
    """ request_select() should return None when requesting a Failure Definition that doesn't exist. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)

    assert DUT.request_select(100) is None


@pytest.mark.integration
def test_request_get_attributes(test_dao, test_configuration):
    """ request_get_attributes() should return a dict of {attribute name:attribute value} pairs. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _attributes = DUT.request_get_attributes(1)

    assert isinstance(_attributes, dict)
    assert _attributes['definition'] == 'Test Failure Definition'


@pytest.mark.integration
def test_request_set_attributes(test_dao, test_configuration):
    """ request_set_attributes() should return a dict of {attribute name:attribute value} pairs. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _error_code, _msg = DUT.request_set_attributes(1, ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKFailureDefinition 1 attributes.")


@pytest.mark.integration
def test_request_insert(test_dao, test_configuration):
    """ request_insert() should return False on success. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_insert(revision_id=1)


@pytest.mark.integration
def test_request_last_id(test_dao, test_configuration):
    """ request_last_id() should return the last Revision ID used in the RTK Program database. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert DUT.request_last_id() == 2


@pytest.mark.integration
def test_request_delete(test_dao, test_configuration):
    """ request_delete() should return False on success. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_delete(2)


@pytest.mark.integration
def test_request_delete_non_existent_id(test_dao, test_configuration):
    """ request_delete() should return True when attempting to delete a non-existent Failure Definition. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert DUT.request_delete(100)


@pytest.mark.integration
def test_request_update(test_dao, test_configuration):
    """ request_update() should return False on success. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_update(1)


@pytest.mark.integration
def test_request_update_non_existent_id(test_dao, test_configuration):
    """ request_update() should return True when attempting to save a non-existent Failure Definition. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert DUT.request_update(100)


@pytest.mark.integration
def test_request_update_all(test_dao, test_configuration):
    """ request_update_all() should return False on success. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_update_all()
