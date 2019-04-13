#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.modules.fmea.test_fmea.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the FMEA class."""

from treelib import Tree

import pytest

from ramstk.dao import RAMSTKMode
from ramstk.dao import RAMSTKMechanism
from ramstk.dao import RAMSTKCause
from ramstk.dao import RAMSTKControl
from ramstk.dao import RAMSTKAction
from ramstk.modules.fmea import (dtcFMEA, dtmFMEA, dtmAction, dtmControl,
                                 dtmMode, dtmMechanism, dtmCause)

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Doyle "weibullguy" Rowland'

ATTRIBUTES = {'function_id': 1, 'hardware_id': 1, 'functional': True}


@pytest.mark.integration
def test_create_data_model(test_dao):
    """ __init__() should return instance of FMEA data model. """
    DUT = dtmFMEA(test_dao, test=True)

    assert isinstance(DUT, dtmFMEA)
    assert isinstance(DUT.dtm_mode, dtmMode)
    assert isinstance(DUT.dtm_mechanism, dtmMechanism)
    assert isinstance(DUT.dtm_cause, dtmCause)
    assert isinstance(DUT.dtm_control, dtmControl)
    assert isinstance(DUT.dtm_action, dtmAction)


@pytest.mark.integration
def test_do_select_all_functional(test_dao):
    """ do_select_all() should return a treelib Tree() on success when selecting a Functional FMEA. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=True)

    assert isinstance(DUT.tree, Tree)


@pytest.mark.integration
def test_do_select_all_hardware(test_dao):
    """ do_select_all() should return a treelib Tree() on success when selecting a Hardware FMEA. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=False)

    assert isinstance(DUT.tree, Tree)


@pytest.mark.integration
def test_do_select_all_non_existent_hardware_id(test_dao):
    """ do_select_all() should return an empty Tree() when passed a Hardware ID that doesn't exist. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=100, functional=False)

    assert isinstance(DUT.tree, Tree)
    assert DUT.tree.get_node(0).tag == 'FMEA'
    assert DUT.tree.get_node(1) is None


@pytest.mark.integration
def test_do_select_all_non_existent_function_id(test_dao):
    """ do_select_all() should return an empty Tree() when passed a Function ID that doesn't exist. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=100, functional=True)

    assert isinstance(DUT.tree, Tree)
    assert DUT.tree.get_node(0).tag == 'FMEA'
    assert DUT.tree.get_node(1) is None


@pytest.mark.integration
def test_do_select_mode(test_dao):
    """ do_select() should return an instance of RAMSTKMode on success. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=True)

    _entity = DUT.do_select('0.1')
    assert isinstance(_entity, RAMSTKMode)
    assert _entity.description == ("Test Functional Failure Mode #1")


@pytest.mark.integration
def test_do_select_mechanism(test_dao):
    """ do_select() should return an instance of RAMSTKMechanism on success. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=False)

    _entity = DUT.do_select('0.4.1')

    assert isinstance(_entity, RAMSTKMechanism)
    assert _entity.description == 'Test Failure Mechanism #1 for Mode ID 4'


@pytest.mark.integration
def test_do_select_cause(test_dao):
    """ do_select() should return an instance of RAMSTKCause on success. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=False)

    _entity = DUT.do_select('0.4.1.4')

    assert isinstance(_entity, RAMSTKCause)
    assert _entity.description == 'Test Failure Cause #1 for Mechanism ID 1'


@pytest.mark.integration
def test_do_select_control_functional(test_dao):
    """ do_select() should return an instance of RAMSTKControl when selecting from a functional FMEA on success. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=True)

    _entity = DUT.do_select('0.1.1.1c')

    assert isinstance(_entity, RAMSTKControl)
    assert _entity.description == (
        "Test Functional FMEA Control #1 for Cause ID 1")


@pytest.mark.integration
def test_do_select_control_hardware(test_dao):
    """ do_select() should return an instance of RAMSTKControl when selecting from a hardware FMEA on success. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=False)
    _entity = DUT.do_select('0.4.1.4.4c')

    assert isinstance(_entity, RAMSTKControl)
    assert _entity.description == 'Test FMEA Control #1 for Cause ID 4'


@pytest.mark.integration
def test_do_select_action_functional(test_dao):
    """ do_select() should return an instance of RAMSTKAction when selecting from a functional FMEA on success. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=True)

    _entity = DUT.do_select('0.1.1.1a')

    assert isinstance(_entity, RAMSTKAction)
    assert _entity.action_recommended == ("Test Functional FMEA Recommended "
                                          "Action #1 for Cause ID 1")


@pytest.mark.integration
def test_do_select_action_hardware(test_dao):
    """ do_select() should return an instance of RAMSTKAction when selecting from a hardware FMEA on success. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=False)

    _entity = DUT.do_select('0.4.1.4.4a')
    print DUT.tree.nodes
    assert isinstance(_entity, RAMSTKAction)
    assert _entity.action_recommended == ("Test FMEA Recommended Action #1 "
                                          "for Cause ID 4")


@pytest.mark.integration
def test_do_insert_mode_functional(test_dao):
    """ do_insert() should return a zero error code on success when adding a new Mode to a Functional FMEA. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=True)

    _error_code, _msg = DUT.do_insert(entity_id=1, parent_id=0, level='mode')

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program "
        "database.")
    _node_id = '0.' + str(DUT.dtm_mode.last_id)

    _mode = DUT.do_select(_node_id)

    assert isinstance(_mode, RAMSTKMode)
    assert _mode.function_id == 1
    assert _mode.hardware_id == -1

    _tree_mode = DUT.tree.get_node(_node_id)
    assert isinstance(_tree_mode.data, RAMSTKMode)
    assert _tree_mode.data == _mode


@pytest.mark.integration
def test_do_insert_mode_hardware(test_dao):
    """ do_insert() should return a zero error code on success when adding a new Mode to a Hardware FMEA. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=False)

    _error_code, _msg = DUT.do_insert(entity_id=1, parent_id=0, level='mode')

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program "
        "database.")
    _node_id = '0.' + str(DUT.dtm_mode.last_id)

    _mode = DUT.do_select(_node_id)

    assert isinstance(_mode, RAMSTKMode)
    assert _mode.function_id == -1
    assert _mode.hardware_id == 1

    _tree_mode = DUT.tree.get_node(_node_id)
    assert isinstance(_tree_mode.data, RAMSTKMode)
    assert _mode == _tree_mode.data


@pytest.mark.integration
def test_do_insert_mode_hardware_non_existant_level(test_dao):
    """ do_insert() should return a non-zero error code when trying to add a non-existant level. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=False)

    _error_code, _msg = DUT.do_insert(entity_id=1, parent_id=0, level='juice')

    assert _error_code == 2005
    assert _msg == (
        "RAMSTK ERROR: Attempted to add an item to the FMEA with an "
        "undefined indenture level.  Level juice was requested.  "
        "Must be one of mode, mechanism, cause, control, or "
        "action.")


@pytest.mark.integration
def test_do_insert_mechanism(test_dao):
    """ do_insert() should return a zero error code on success when adding a new Mechanism to a Hardware FMEA. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=False)

    _error_code, _msg = DUT.do_insert(
        entity_id=4, parent_id='0.4', level='mechanism')

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program "
        "database.")
    _node_id = '0.4.' + str(DUT.dtm_mechanism.last_id)

    _mechanism = DUT.do_select(_node_id)

    assert isinstance(_mechanism, RAMSTKMechanism)
    assert _mechanism.mode_id == 4
    assert _mechanism.mechanism_id == DUT.dtm_mechanism.last_id

    _tree_mechanism = DUT.tree.get_node(_node_id)
    assert isinstance(_tree_mechanism.data, RAMSTKMechanism)
    assert _mechanism == _tree_mechanism.data


@pytest.mark.integration
def test_do_insert_cause(test_dao):
    """ do_insert() should return a zero error code on success when adding a new Cause to a Hardware FMEA. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=False)

    _error_code, _msg = DUT.do_insert(
        entity_id=1, parent_id='0.4.1', level='cause')

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program "
        "database.")

    _node_id = '0.4.1.' + str(DUT.dtm_cause.last_id)

    _cause = DUT.do_select(_node_id)

    assert isinstance(_cause, RAMSTKCause)
    assert _cause.mechanism_id == 1
    assert _cause.cause_id == DUT.dtm_cause.last_id

    _tree_cause = DUT.tree.get_node(_node_id)
    assert isinstance(_tree_cause.data, RAMSTKCause)
    assert _tree_cause.data == _cause


@pytest.mark.integration
def test_do_insert_control_functional(test_dao):
    """ do_insert() should return a zero error code on success when adding a new Control to a Functional FMEA. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=True)

    _error_code, _msg = DUT.do_insert(
        entity_id=1, parent_id='0.1', level='control')

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program "
        "database.")
    _node_id = '0.1.' + str(DUT.dtm_control.last_id) + 'c'

    _control = DUT.do_select(_node_id)

    assert isinstance(_control, RAMSTKControl)
    assert _control.cause_id == 1

    _tree_control = DUT.tree.get_node(_node_id)
    assert isinstance(_tree_control.data, RAMSTKControl)
    assert _control == _tree_control.data


@pytest.mark.integration
def test_do_insert_control_hardware(test_dao):
    """ do_insert() should return a zero error code on success when adding a new Control to a Hardware FMEA. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=False)

    _error_code, _msg = DUT.do_insert(
        entity_id=4, parent_id='0.4.1.4', level='control')

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program "
        "database.")
    _node_id = '0.4.1.4.' + str(DUT.dtm_control.last_id) + 'c'

    _control = DUT.do_select(_node_id)

    assert isinstance(_control, RAMSTKControl)
    assert _control.cause_id == 4

    _tree_control = DUT.tree.get_node(_node_id)
    assert isinstance(_tree_control.data, RAMSTKControl)
    assert _control == _tree_control.data


@pytest.mark.integration
def test_do_insert_action_functional(test_dao):
    """ do_insert() should return a zero error code on success when adding a new Action to a Functional FMEA. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=True)

    _error_code, _msg = DUT.do_insert(
        entity_id=1, parent_id='0.1', level='action')

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program "
        "database.")
    _node_id = '0.1.' + str(DUT.dtm_action.last_id) + 'a'

    _action = DUT.do_select(_node_id)

    assert isinstance(_action, RAMSTKAction)
    assert _action.cause_id == 1

    _tree_action = DUT.tree.get_node(_node_id)
    assert isinstance(_tree_action.data, RAMSTKAction)
    assert _action == _tree_action.data


@pytest.mark.integration
def test_do_insert_action_hardware(test_dao):
    """ do_insert() should return a zero error code on success when adding a new Action to a Hardware FMEA. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=False)

    _error_code, _msg = DUT.do_insert(
        entity_id=4, parent_id='0.4.1.4', level='action')

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program "
        "database.")
    _node_id = '0.4.1.4.' + str(DUT.dtm_action.last_id) + 'a'

    _action = DUT.do_select(_node_id)

    assert isinstance(_action, RAMSTKAction)
    assert _action.cause_id == 4

    _tree_action = DUT.tree.get_node(_node_id)
    assert isinstance(_tree_action.data, RAMSTKAction)
    assert _action == _tree_action.data


@pytest.mark.integration
def test_do_insert_non_existent_type(test_dao):
    """ do_insert() should return a 2005 error code when attempting to add something other than a Mode, Mechanism, Cause, Control, or Action. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=False)

    _error_code, _msg = DUT.do_insert(
        entity_id=100, parent_id=0, level='scadamoosh')

    assert _error_code == 2005
    assert _msg == (
        "RAMSTK ERROR: Attempted to add an item to the FMEA with an "
        "undefined indenture level.  Level scadamoosh was "
        "requested.  Must be one of mode, mechanism, cause, "
        "control, or action.")


@pytest.mark.integration
def test_do_insert_no_parent_in_tree(test_dao):
    """ do_insert() should return a 2005 error code when attempting to add something to a non-existant parent Node. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=False)

    _error_code, _msg = DUT.do_insert(
        entity_id=1, parent_id='mode_1', level='action')

    assert _error_code == 2005
    assert _msg == (
        "RAMSTK ERROR: Attempted to add an item under non-existent "
        "Node ID: mode_1.")


@pytest.mark.integration
def test_do_delete_control_functional(test_dao):
    """ do_delete() should return a zero error code on success when removing a Control. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=True)
    DUT.do_insert(entity_id=1, parent_id='0.1.1', level='control')

    _node_id = '0.1.1.' + str(DUT.dtm_control.last_id) + 'c'

    _error_code, _msg = DUT.do_delete(_node_id)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Deleting an item from the RAMSTK Program "
                    "database.")


@pytest.mark.integration
def test_do_delete_non_existent_node_id(test_dao):
    """ do_delete() should return a 2105 error code when attempting to remove a non-existant item from the FMEA. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=True)

    _error_code, _msg = DUT.do_delete('scadamoosh_1')

    assert _error_code == 2005
    assert _msg == ("  RAMSTK ERROR: Attempted to delete non-existent entity "
                    "with Node ID scadamoosh_1 from the FMEA.")


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=True)

    _error_code, _msg = DUT.do_update('0.1')

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating the RAMSTK Program database.")


@pytest.mark.integration
def test_do_update_non_existent_node_id(test_dao):
    """ do_update() should return a 2106 error code when attempting to update a non-existent Node ID from a functional FMEA. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=True)

    _error_code, _msg = DUT.do_update('mode_1000')

    assert _error_code == 1
    assert _msg == ("RAMSTK ERROR: Attempted to save non-existent Functional "
                    "FMEA entity with Node ID mode_1000.")


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=True)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating all line items in the FMEA.")


@pytest.mark.integration
def test_do_calculate_criticality(test_dao):
    """ do_calculate() returns a zero error code on success when calculate criticality. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=False)
    _mode = DUT.do_select('0.4')

    _mode.mode_ratio = 0.4
    _mode.mode_op_time = 100.0
    _mode.effect_probability = 1.0
    _error_code, _msg = DUT.do_calculate(
        '0.4', item_hr=0.00001, criticality=True, rpn=False)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Calculating failure mode 6 criticality.")
    assert _mode.mode_criticality == pytest.approx(0.0004)


@pytest.mark.integration
def test_do_calculate_mechanism_rpn(test_dao):
    """ do_calculate() returns a zero error code on success when calculate RPN for a failure mechanism. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=False)

    for _node in DUT.tree.all_nodes():
        try:
            _attributes = _node.data.get_attributes()
            if _node.data.is_mode:
                _attributes['rpn_severity'] = 7
                _attributes['rpn_severity_new'] = 4
            if _node.data.is_mechanism or _node.data.is_cause:
                _attributes['rpn_detection'] = 4
                _attributes['rpn_occurrence'] = 7
                _attributes['rpn_detection_new'] = 3
                _attributes['rpn_occurrence_new'] = 5

            _node.data.set_attributes(_attributes)
        except AttributeError:
            pass

    _error_code, _msg = DUT.do_calculate(
        '0.4.1', item_hr=0.0, criticality=False, rpn=True)
    _node = DUT.tree.get_node('0.4.1').data

    assert _error_code == 0
    assert _node.rpn == 196
    assert _node.rpn_new == 60


@pytest.mark.integration
def test_do_calculate_cause_rpn(test_dao):
    """ do_calculate() returns a zero error code on success when calculate the RPN for a cause. """
    DUT = dtmFMEA(test_dao, test=True)
    DUT.do_select_all(parent_id=1, functional=False)

    for _node in DUT.tree.all_nodes():
        try:
            _attributes = _node.data.get_attributes()
            if _node.data.is_mode:
                _attributes['rpn_severity'] = 7
                _attributes['rpn_severity_new'] = 4
            if _node.data.is_mechanism or _node.data.is_cause:
                _attributes['rpn_detection'] = 4
                _attributes['rpn_occurrence'] = 7
                _attributes['rpn_detection_new'] = 3
                _attributes['rpn_occurrence_new'] = 5

            _node.data.set_attributes(_attributes)
        except AttributeError:
            pass

    _error_code, _msg = DUT.do_calculate(
        '0.4.1.4', item_hr=0.0, rpn=True, criticality=False)
    _node = DUT.tree.get_node('0.4.1.4').data

    assert _error_code == 0
    assert _node.rpn == 196
    assert _node.rpn_new == 60


@pytest.mark.integration
def test_create_data_controller(test_dao, test_configuration):
    """ __init__() should return instance of FMEA data controller. """
    DUT = dtcFMEA(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcFMEA)
    assert isinstance(DUT._dtm_data_model, dtmFMEA)


@pytest.mark.integration
def test_request_do_select_all_hardware(test_dao, test_configuration):
    """ request_do_select_all() should return a treelib Tree() with the hardware FMEA. """
    DUT = dtcFMEA(test_dao, test_configuration, test=True)
    ATTRIBUTES['parent_id'] = ATTRIBUTES['hardware_id']
    DUT.request_do_select_all(ATTRIBUTES)

    assert isinstance(DUT._dtm_data_model.tree, Tree)


@pytest.mark.integration
def test_request_do_select_all_functional(test_dao, test_configuration):
    """ request_do_select_all() should return a treelib Tree() with the functional FMEA. """
    DUT = dtcFMEA(test_dao, test_configuration, test=True)
    ATTRIBUTES['parent_id'] = ATTRIBUTES['function_id']
    DUT.request_do_select_all(ATTRIBUTES)

    assert isinstance(DUT._dtm_data_model.tree, Tree)


@pytest.mark.integration
def test_request_do_insert_mode_functional(test_dao, test_configuration):
    """ request_do_insert() should return False on success when adding a mode to a functional FMEA. """
    DUT = dtcFMEA(test_dao, test_configuration, test=True)
    ATTRIBUTES['parent_id'] = ATTRIBUTES['function_id']
    DUT.request_do_select_all(ATTRIBUTES)
    assert not DUT.request_do_insert(entity_id=1, parent_id=0, level='mode')


@pytest.mark.integration
def test_request_do_insert_mode_hardware(test_dao, test_configuration):
    """ request_do_insert() should return False on success when addin a mode to a hardware FMEA. """
    DUT = dtcFMEA(test_dao, test_configuration, test=True)
    ATTRIBUTES['parent_id'] = ATTRIBUTES['hardware_id']
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_insert(entity_id=1, parent_id=0, level='mode')


@pytest.mark.integration
def test_request_do_insert_mechanism(test_dao, test_configuration):
    """ request_do_insert() should return a False on success when adding a new Mechanism to a Hardware FMEA. """
    DUT = dtcFMEA(test_dao, test_configuration, test=True)
    ATTRIBUTES['parent_id'] = ATTRIBUTES['hardware_id']
    ATTRIBUTES['functional'] = False
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_insert(
        entity_id=4, parent_id='0.4', level='mechanism')


@pytest.mark.integration
def test_request_do_delete_control_functional(test_dao, test_configuration):
    """ request_do_delete() should return False on success when removing a Control from a functional FMEA. """
    DUT = dtcFMEA(test_dao, test_configuration, test=True)
    ATTRIBUTES['parent_id'] = ATTRIBUTES['function_id']
    ATTRIBUTES['functional'] = True
    DUT.request_do_select_all(ATTRIBUTES)
    _node_id = '0.1.1.' + str(DUT._dtm_data_model.dtm_control.last_id) + 'c'

    assert not DUT.request_do_delete(_node_id)


@pytest.mark.integration
def test_request_do_update_all(test_dao, test_configuration):
    """ request_do_update_all() should return False on success. """
    DUT = dtcFMEA(test_dao, test_configuration, test=True)
    ATTRIBUTES['parent_id'] = ATTRIBUTES['hardware_id']
    ATTRIBUTES['functional'] = False
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_update_all()
