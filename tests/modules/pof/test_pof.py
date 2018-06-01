#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.modules.pof.test_pof.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Physics of Failure (PoF) class."""

from treelib import Tree

import pytest

from rtk.dao import (RTKMechanism, RTKOpLoad, RTKOpStress, RTKTestMethod)
from rtk.modules.pof import (dtcPoF, dtmOpLoad, dtmOpStress, dtmTestMethod,
                             dtmPoF)
from rtk.modules.fmea import dtmMechanism

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "Weibullguy" Rowland'


@pytest.mark.integration
def test_pof_create_data_model(test_dao):
    """ __init__() should return an instance of the PoF data model. """
    DUT = dtmPoF(test_dao)

    assert isinstance(DUT, dtmPoF)
    assert isinstance(DUT.dtm_mechanism, dtmMechanism)
    assert isinstance(DUT.dtm_opload, dtmOpLoad)
    assert isinstance(DUT.dtm_opstress, dtmOpStress)
    assert isinstance(DUT.dtm_testmethod, dtmTestMethod)


@pytest.mark.integration
def test_select_all(test_dao):
    """ do_select_all() should return a treelib Tree() on success. """
    DUT = dtmPoF(test_dao)

    _tree = DUT.do_select_all(parent_id=1)

    assert isinstance(_tree, Tree)


@pytest.mark.integration
def test_select_all_non_existent_id(test_dao):
    """ do_select_all() should return an empty Tree() when passed a Mechanism ID that doesn't exist. """
    DUT = dtmPoF(test_dao)

    _tree = DUT.do_select_all(parent_id=100)

    assert isinstance(_tree, Tree)
    assert _tree.get_node(0).tag == 'PhysicsOfFailure'
    assert _tree.get_node(1) is None


@pytest.mark.integration
def test_select_mechanism(test_dao):
    """ select() should return an instance of RTKMechanism on success. """
    DUT = dtmPoF(test_dao)
    DUT.do_select_all(parent_id=4)

    _entity = DUT.select('0.1')

    assert isinstance(_entity, RTKMechanism)
    assert _entity.description == 'Test Failure Mechanism #1 for Mode ID 4'


@pytest.mark.integration
def test_select_opload(test_dao):
    """ select() should return an instance of RTKOpLoad on success."""
    DUT = dtmPoF(test_dao)
    DUT.do_select_all(parent_id=4)
    _entity = DUT.select('0.1.1')

    assert isinstance(_entity, RTKOpLoad)
    assert _entity.description == 'Test Operating Load'


@pytest.mark.integration
def test_select_opstress(test_dao):
    """ select() should return an instance of RTKOpStress on success."""
    DUT = dtmPoF(test_dao)
    DUT.do_select_all(parent_id=4)
    _entity = DUT.select('0.1.1.1s')

    assert isinstance(_entity, RTKOpStress)
    assert _entity.description == 'Test Operating Stress'


@pytest.mark.integration
def test_select_test_method(test_dao):
    """ select() should return an instance of RTKTestMethod on success."""
    DUT = dtmPoF(test_dao)
    DUT.do_select_all(parent_id=4)
    _entity = DUT.select('0.1.1.1t')

    assert isinstance(_entity, RTKTestMethod)
    assert _entity.description == 'Test Test Method'


@pytest.mark.integration
def test_insert_opload(test_dao):
    """ insert() should return a zero error code on success when adding a new Operating Load to a PoF. """
    DUT = dtmPoF(test_dao)
    DUT.do_select_all(parent_id=4)

    _error_code, _msg = DUT.insert(
        entity_id=1, parent_id='0.1', level='opload')

    # Verify the insert went well.
    assert _error_code == 0
    assert _msg == (
        "RTK SUCCESS: Adding one or more items to the RTK Program database.")

    # Verify the insert added an OpLoad.
    _node_id = '0.1.{0:d}'.format(DUT.dtm_opload.last_id)
    _opload = DUT.select(_node_id)

    assert isinstance(_opload, RTKOpLoad)


@pytest.mark.integration
def test_insert_opstress(test_dao):
    """ insert() should return a zero error code on success when adding a new Operating Stress to a PoF. """
    DUT = dtmPoF(test_dao)
    DUT.do_select_all(parent_id=4)

    _error_code, _msg = DUT.insert(
        entity_id=1, parent_id='0.1.1', level='opstress')

    # Verify the insert went well.
    assert _error_code == 0
    assert _msg == (
        "RTK SUCCESS: Adding one or more items to the RTK Program database.")

    # Verify the insert added an OpStress.
    _node_id = '0.1.1.{0:d}s'.format(DUT.dtm_opstress.last_id)
    _opstress = DUT.select(_node_id)

    assert isinstance(_opstress, RTKOpStress)


@pytest.mark.integration
def test_insert_test_method(test_dao):
    """ insert() should return a zero error code on success when adding a new Test Method to a PoF. """
    DUT = dtmPoF(test_dao)
    DUT.do_select_all(parent_id=4)

    _error_code, _msg = DUT.insert(
        entity_id=1, parent_id='0.1.1', level='testmethod')

    # Verify the insert went well.
    assert _error_code == 0
    assert _msg == (
        "RTK SUCCESS: Adding one or more items to the RTK Program database.")

    # Verify the insert added an OpLoad.
    _node_id = '0.1.1.{0:d}t'.format(DUT.dtm_testmethod.last_id)
    _method = DUT.select(_node_id)

    assert isinstance(_method, RTKTestMethod)


@pytest.mark.integration
def test_insert_non_existent_type(test_dao):
    """ insert() should return a non-zero error code when trying a something to a PoF at a level that doesn't exist. """
    DUT = dtmPoF(test_dao)
    DUT.do_select_all(parent_id=4)

    _error_code, _msg = DUT.insert(
        entity_id=1, parent_id='0.1.1', level='scadamoosh')

    # Verify the insert went well.
    assert _error_code == 2005
    assert _msg == ("RTK ERROR: Attempted to add an item to the Physics of "
                    "Failure with an undefined indenture level.  Level "
                    "scadamoosh was requested.  Must be one of opload, "
                    "opstress, or testmethod.")


@pytest.mark.integration
def test_insert_no_parent_in_tree(test_dao):
    """ insert() should return a 2005 error code when attempting to add something to a non-existant parent Node. """
    DUT = dtmPoF(test_dao)
    DUT.do_select_all(parent_id=4)

    _error_code, _msg = DUT.insert(
        entity_id=1, parent_id='mechanism_1', level='opload')

    assert _error_code == 2005
    assert _msg == ("RTK ERROR: Attempted to add an item under non-existent "
                    "Node ID: mechanism_1.")


@pytest.mark.integration
def test_delete_opload(test_dao):
    """ delete() should return a zero error code on success when removing an Operating Load. """
    DUT = dtmPoF(test_dao)
    DUT.do_select_all(parent_id=4)

    _node_id = '0.1.{0:d}'.format(DUT.dtm_opload.last_id)

    _error_code, _msg = DUT.delete(_node_id)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Deleting an item from the RTK Program "
                    "database.")


@pytest.mark.integration
def test_delete_non_existent_node_id(test_dao):
    """ delete() should return a 2105 error code when attempting to remove a non-existant item from the PoF. """
    DUT = dtmPoF(test_dao)
    DUT.do_select_all(parent_id=4)

    _error_code, _msg = DUT.delete('scadamoosh_1')

    assert _error_code == 2005
    assert _msg == ("  RTK ERROR: Attempted to delete non-existent entity "
                    "with Node ID scadamoosh_1 from the Physics of Failure.")


@pytest.mark.integration
def test_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmPoF(test_dao)
    DUT.do_select_all(parent_id=4)

    _error_code, _msg = DUT.update('0.1')

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
def test_update_non_existent_node_id(test_dao):
    """ update() should return a 2106 error code when attempting to update a non-existent Node ID from a PoF. """
    DUT = dtmPoF(test_dao)
    DUT.do_select_all(parent_id=4)

    _error_code, _msg = DUT.update('mode_1000')

    assert _error_code == 2006
    assert _msg == ("RTK ERROR: Attempted to save non-existent entity with "
                    "Node ID mode_1000.")


@pytest.mark.integration
def test_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmPoF(test_dao)
    DUT.do_select_all(parent_id=4)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating all line items in the damage "
                    "modeling worksheet.")


@pytest.mark.integration
def test_pof_create_data_controller(test_dao, test_configuration):
    """ __init__() should return instance of PoF data controller. """
    DUT = dtcPoF(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcPoF)
    assert isinstance(DUT._dtm_data_model, dtmPoF)


@pytest.mark.integration
def test_request_do_select_all(test_dao, test_configuration):
    """ request_do_select_all() should return a treelib Tree() with the PoF. """
    DUT = dtcPoF(test_dao, test_configuration, test=True)

    assert isinstance(DUT.request_do_select_all(1), Tree)


@pytest.mark.integration
def test_request_do_insert_opload(test_dao, test_configuration):
    """ request_do_insert() should return False on success when adding an operating load to a PoF. """
    DUT = dtcPoF(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(4)

    assert not DUT.request_do_insert(
        entity_id=1, parent_id='0.1', level='opload')


@pytest.mark.integration
def test_request_do_insert_opstress(test_dao, test_configuration):
    """ request_do_insert() should return False on success when adding an operating stress to a PoF. """
    DUT = dtcPoF(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(4)

    assert not DUT.request_do_insert(
        entity_id=1, parent_id='0.1.1', level='opstress')


@pytest.mark.integration
def test_request_do_insert_test_method(test_dao, test_configuration):
    """ request_do_insert() should return False on success when adding a test method to a PoF. """
    DUT = dtcPoF(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(4)

    assert not DUT.request_do_insert(
        entity_id=1, parent_id='0.1.1', level='testmethod')


@pytest.mark.integration
def test_request_do_update_all(test_dao, test_configuration):
    """ request_do_update_all() should return a zero error code on success. """
    DUT = dtcPoF(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(4)

    assert not DUT.request_do_update_all()
