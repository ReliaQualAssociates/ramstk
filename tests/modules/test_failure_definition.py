# -*- coding: utf-8 -*-
#
#       ramstk.tests.failure_definition.TestFailureDefinition.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Failure Definition module algorithms and models."""

from treelib import Tree

import pytest

from ramstk.modules.failure_definition import (dtmFailureDefinition,
                                               dtcFailureDefinition)
from ramstk.dao import DAO
from ramstk.dao import RAMSTKFailureDefinition

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'definition_id': 1,
    'definition': b'Test Failure Definition',
    'revision_id': 1
}


@pytest.mark.integration
def test_create_data_model(test_dao):
    """ __init__ should return instance of a FailureDefition data model. """
    DUT = dtmFailureDefinition(test_dao, test=True)

    assert isinstance(DUT, dtmFailureDefinition)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a Tree() object populated with RAMSTKFailureDefinitions instances on success. """
    DUT = dtmFailureDefinition(test_dao, test=True)

    assert DUT.do_select_all(revision_id=1) is None
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.tree.get_node(1).data, RAMSTKFailureDefinition)


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RAMSTKFailureDefinition data model on success. """
    DUT = dtmFailureDefinition(test_dao, test=True)
    DUT.do_select_all(revision_id=1)
    _definition = DUT.do_select(1)

    assert isinstance(_definition, RAMSTKFailureDefinition)
    assert _definition.definition_id == 1
    assert _definition.definition == b'Failure Definition'


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent Definition ID is requested. """
    DUT = dtmFailureDefinition(test_dao, test=True)
    _definition = DUT.do_select(100)

    assert _definition is None


@pytest.mark.integration
def test_do_insert(test_dao):
    """ do_insert() should return False on success. """
    DUT = dtmFailureDefinition(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_insert(revision_id=1)

    assert _error_code == 0
    assert _msg == (
        'RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program '
        'database.')
    assert DUT.last_id == 2


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmFailureDefinition(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Deleting an item from the RAMSTK Program '
                    'database.')


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a Revision ID that doesn't exist. """
    DUT = dtmFailureDefinition(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code == 2005
    assert _msg == ('  RAMSTK ERROR: Attempted to delete non-existent Failure '
                    'Definition ID 300.')


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmFailureDefinition(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _definition = DUT.do_select(1)
    _definition.definition = b'Test Failure Definition'

    _error_code, _msg = DUT.do_update(1)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Updating the RAMSTK Program database.')


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed a Failure Definition ID that doesn't exist. """
    DUT = dtmFailureDefinition(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2005
    assert _msg == ('RAMSTK ERROR: Attempted to save non-existent Failure '
                    'Definition ID 100.')


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmFailureDefinition(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating all records in the failure "
                    "definition table.")


@pytest.mark.integration
def test_controller_create(test_dao, test_configuration):
    """ __init__() should return a Failure Definition Data Controller. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcFailureDefinition)
    assert isinstance(DUT._dtm_data_model, dtmFailureDefinition)


@pytest.mark.integration
def test_request_do_select_all(test_dao, test_configuration):
    """ request_do_select_all() should return a Tree of RAMSTKFailureDefinition models. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert isinstance(
        DUT._dtm_data_model.tree.get_node(1).data, RAMSTKFailureDefinition)


@pytest.mark.integration
def test_request_do_select(test_dao, test_configuration):
    """ request_do_select() should return an RAMSTKFailureDefinition model. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert isinstance(DUT.request_do_select(1), RAMSTKFailureDefinition)


@pytest.mark.integration
def test_request_non_existent_id(test_dao, test_configuration):
    """ request_do_select() should return None when requesting a Failure Definition that doesn't exist. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)

    assert DUT.request_do_select(100) is None


@pytest.mark.integration
def test_request_get_attributes(test_dao, test_configuration):
    """ request_get_attributes() should return a dict of {attribute name:attribute value} pairs. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    _attributes = DUT.request_get_attributes(1)

    assert isinstance(_attributes, dict)
    assert _attributes['definition'] == b'Test Failure Definition'


@pytest.mark.integration
def test_request_set_attributes(test_dao, test_configuration):
    """ request_set_attributes() should return a dict of {attribute name:attribute value} pairs. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    _error_code, _msg = DUT.request_set_attributes(
        module_id=1, key='definition', value=b'New Failure Definition')

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Updating RAMSTKFailureDefinition 1 attributes.")


@pytest.mark.integration
def test_request_do_insert(test_dao, test_configuration):
    """ request_do_insert() should return False on success. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_insert(revision_id=1)


@pytest.mark.integration
def test_request_last_id(test_dao, test_configuration):
    """ request_last_id() should return the last Revision ID used in the RAMSTK Program database. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT.request_last_id() == 2


@pytest.mark.integration
def test_request_do_delete(test_dao, test_configuration):
    """ request_do_delete() should return False on success. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_delete(2)


@pytest.mark.integration
def test_request_do_delete_non_existent_id(test_dao, test_configuration):
    """ request_do_delete() should return True when attempting to delete a non-existent Failure Definition. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT.request_do_delete(100)


@pytest.mark.integration
def test_request_do_update(test_dao, test_configuration):
    """ request_do_update() should return False on success. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_update(1)


@pytest.mark.integration
def test_request_do_update_non_existent_id(test_dao, test_configuration):
    """ request_do_update() should return True when attempting to save a non-existent Failure Definition. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT.request_do_update(100)


@pytest.mark.integration
def test_request_do_update_all(test_dao, test_configuration):
    """ request_do_update_all() should return False on success. """
    DUT = dtcFailureDefinition(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_update_all()
