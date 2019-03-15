#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       ramstk.tests.modules.pof.test_pof.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Physics of Failure (PoF) class."""

from treelib import Tree

import pytest

from ramstk.dao import (RAMSTKMode, RAMSTKMechanism, RAMSTKOpLoad,
                        RAMSTKOpStress, RAMSTKTestMethod)
from ramstk.modules.pof import (dtcPoF, dtmOpLoad, dtmOpStress, dtmTestMethod,
                                dtmPoF)
from ramstk.modules.fmea import dtmMechanism

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {'hardware_id': 1}


@pytest.mark.integration
def test_pof_create_data_model(test_dao):
    """ __init__() should return an instance of the PoF data model. """
    DUT = dtmPoF(test_dao, test=True)

    assert isinstance(DUT, dtmPoF)
    assert isinstance(DUT.dtm_mechanism, dtmMechanism)
    assert isinstance(DUT.dtm_opload, dtmOpLoad)
    assert isinstance(DUT.dtm_opstress, dtmOpStress)
    assert isinstance(DUT.dtm_testmethod, dtmTestMethod)


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a treelib Tree() on success. """
    DUT = dtmPoF(test_dao, test=True)
    DUT.do_select_all(hardware_id=1)

    assert isinstance(DUT.tree, Tree)


@pytest.mark.integration
def test_do_select_all_non_existent_id(test_dao):
    """ do_select_all() should return an empty Tree() when passed a Mechanism ID that doesn't exist. """
    DUT = dtmPoF(test_dao, test=True)
    DUT.do_select_all(hardware_id=100)

    assert isinstance(DUT.tree, Tree)
    assert DUT.tree.get_node(0).tag == 'PhysicsOfFailure'
    assert DUT.tree.get_node(1) is None


@pytest.mark.integration
def test_do_select_mode(test_dao):
    """ do_select() should return an instance of RAMSTKMode on success. """
    DUT = dtmPoF(test_dao, test=True)
    DUT.do_select_all(hardware_id=1)

    _entity = DUT.do_select('0.4')

    assert isinstance(_entity, RAMSTKMode)
    assert _entity.description == 'System Test Failure Mode'


@pytest.mark.integration
def test_do_select_mechanism(test_dao):
    """ do_select() should return an instance of RAMSTKMechanism on success. """
    DUT = dtmPoF(test_dao, test=True)
    DUT.do_select_all(hardware_id=1)

    _entity = DUT.do_select('0.4.1')

    assert isinstance(_entity, RAMSTKMechanism)
    assert _entity.description == 'Test Failure Mechanism #1 for Mode ID 4'


@pytest.mark.integration
def test_do_select_opload(test_dao):
    """ do_elect() should return an instance of RAMSTKOpLoad on success."""
    DUT = dtmPoF(test_dao, test=True)
    DUT.do_select_all(hardware_id=1)
    _entity = DUT.do_select('0.4.1.1')

    assert isinstance(_entity, RAMSTKOpLoad)
    assert _entity.description == 'Test Operating Load'


@pytest.mark.integration
def test_do_select_opstress(test_dao):
    """ do_select() should return an instance of RAMSTKOpStress on success."""
    DUT = dtmPoF(test_dao, test=True)
    DUT.do_select_all(hardware_id=1)
    _entity = DUT.do_select('0.4.1.1.1s')

    assert isinstance(_entity, RAMSTKOpStress)
    assert _entity.description == 'Test Operating Stress'


@pytest.mark.integration
def test_do_select_test_method(test_dao):
    """ do_select() should return an instance of RAMSTKTestMethod on success."""
    DUT = dtmPoF(test_dao, test=True)
    DUT.do_select_all(hardware_id=1)
    _entity = DUT.do_select('0.4.1.1.1t')

    assert isinstance(_entity, RAMSTKTestMethod)
    assert _entity.description == 'Test Test Method'


@pytest.mark.integration
def test_do_insert_opload(test_dao):
    """ do_insert() should return a zero error code on success when adding a new Operating Load to a PoF. """
    DUT = dtmPoF(test_dao, test=True)
    DUT.do_select_all(hardware_id=1)

    _error_code, _msg = DUT.do_insert(
        entity_id=1, parent_id='0.4.1', level='opload')

    # Verify the insert went well.
    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program database."
    )

    # Verify the insert added an OpLoad.
    _node_id = '0.4.1.{0:d}'.format(DUT.dtm_opload.last_id)
    _opload = DUT.do_select(_node_id)

    assert isinstance(_opload, RAMSTKOpLoad)


@pytest.mark.integration
def test_do_insert_opstress(test_dao):
    """ do_insert() should return a zero error code on success when adding a new Operating Stress to a PoF. """
    DUT = dtmPoF(test_dao, test=True)
    DUT.do_select_all(hardware_id=1)

    _error_code, _msg = DUT.do_insert(
        entity_id=1, parent_id='0.4.1.1', level='opstress')

    # Verify the insert went well.
    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program database."
    )

    # Verify the insert added an OpStress.
    _node_id = '0.4.1.1.{0:d}s'.format(DUT.dtm_opstress.last_id)
    _opstress = DUT.do_select(_node_id)

    assert isinstance(_opstress, RAMSTKOpStress)


@pytest.mark.integration
def test_do_insert_test_method(test_dao):
    """ do_insert() should return a zero error code on success when adding a new Test Method to a PoF. """
    DUT = dtmPoF(test_dao, test=True)
    DUT.do_select_all(hardware_id=1)

    _error_code, _msg = DUT.do_insert(
        entity_id=1, parent_id='0.4.1.1', level='testmethod')

    # Verify the insert went well.
    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program database."
    )

    # Verify the insert added an OpLoad.
    _node_id = '0.4.1.1.{0:d}t'.format(DUT.dtm_testmethod.last_id)
    _method = DUT.do_select(_node_id)

    assert isinstance(_method, RAMSTKTestMethod)


@pytest.mark.integration
def test_do_insert_non_existent_type(test_dao):
    """ do_insert() should return a non-zero error code when trying a something to a PoF at a level that doesn't exist. """
    DUT = dtmPoF(test_dao, test=True)
    DUT.do_select_all(hardware_id=1)

    _error_code, _msg = DUT.do_insert(
        entity_id=1, parent_id='0.4.1.1', level='scadamoosh')

    # Verify the insert went well.
    assert _error_code == 2005
    assert _msg == ("RAMSTK ERROR: Attempted to add an item to the Physics of "
                    "Failure with an undefined indenture level.  Level "
                    "scadamoosh was requested.  Must be one of opload, "
                    "opstress, or testmethod.")


@pytest.mark.integration
def test_do_insert_no_parent_in_tree(test_dao):
    """ do_insert() should return a 2005 error code when attempting to add something to a non-existant parent Node. """
    DUT = dtmPoF(test_dao, test=True)
    DUT.do_select_all(hardware_id=1)

    _error_code, _msg = DUT.do_insert(
        entity_id=1, parent_id='mechanism_1', level='opload')

    assert _error_code == 2005
    assert _msg == (
        "RAMSTK ERROR: Attempted to add an item under non-existent "
        "Node ID: mechanism_1.")


@pytest.mark.integration
def test_do_delete_opload(test_dao):
    """ do_delete() should return a zero error code on success when removing an Operating Load. """
    DUT = dtmPoF(test_dao, test=True)
    DUT.do_select_all(hardware_id=1)

    _node_id = '0.4.1.{0:d}'.format(DUT.dtm_opload.last_id)

    _error_code, _msg = DUT.do_delete(_node_id)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Deleting an item from the RAMSTK Program "
                    "database.")


@pytest.mark.integration
def test_do_delete_non_existent_node_id(test_dao):
    """ do_delete() should return a 2105 error code when attempting to remove a non-existant item from the PoF. """
    DUT = dtmPoF(test_dao, test=True)
    DUT.do_select_all(hardware_id=1)

    _error_code, _msg = DUT.do_delete('scadamoosh_1')

    assert _error_code == 2005
    assert _msg == ("  RAMSTK ERROR: Attempted to delete non-existent entity "
                    "with Node ID scadamoosh_1 from the Physics of Failure.")


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmPoF(test_dao, test=True)
    DUT.do_select_all(hardware_id=1)

    _error_code, _msg = DUT.do_update('0.4.1')

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating the RAMSTK Program database.")


@pytest.mark.integration
def test_do_update_non_existent_node_id(test_dao):
    """ do_update() should return a 2106 error code when attempting to update a non-existent Node ID from a PoF. """
    DUT = dtmPoF(test_dao, test=True)
    DUT.do_select_all(hardware_id=1)

    _error_code, _msg = DUT.do_update('mode_1000')

    assert _error_code == 2006
    assert _msg == ("RAMSTK ERROR: Attempted to save non-existent entity with "
                    "Node ID mode_1000.")


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmPoF(test_dao, test=True)
    DUT.do_select_all(hardware_id=1)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating all line items in the damage "
                    "modeling worksheet.")


@pytest.mark.integration
def test_create_data_controller(test_dao, test_configuration):
    """ __init__() should return instance of PoF data controller. """
    DUT = dtcPoF(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcPoF)
    assert isinstance(DUT._dtm_data_model, dtmPoF)


@pytest.mark.integration
def test_request_do_select_all(test_dao, test_configuration):
    """ request_do_select_all() should return a treelib Tree() with the PoF. """
    DUT = dtcPoF(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert isinstance(DUT._dtm_data_model.tree, Tree)


@pytest.mark.integration
def test_request_do_insert_opload(test_dao, test_configuration):
    """ request_do_insert() should return False on success when adding an operating load to a PoF. """
    DUT = dtcPoF(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_insert(
        entity_id=1, parent_id='0.4.1', level='opload')


@pytest.mark.integration
def test_request_do_insert_opstress(test_dao, test_configuration):
    """ request_do_insert() should return False on success when adding an operating stress to a PoF. """
    DUT = dtcPoF(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_insert(
        entity_id=1, parent_id='0.4.1.1', level='opstress')


@pytest.mark.integration
def test_request_do_insert_test_method(test_dao, test_configuration):
    """ request_do_insert() should return False on success when adding a test method to a PoF. """
    DUT = dtcPoF(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_insert(
        entity_id=1, parent_id='0.4.1.1', level='testmethod')


@pytest.mark.integration
def test_request_do_update_all(test_dao, test_configuration):
    """ request_do_update_all() should return a zero error code on success. """
    DUT = dtcPoF(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_update_all()
