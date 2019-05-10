#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       ramstk.tests.modules.test_similar_item.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2018 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the SimilarItem class. """

import pytest

from treelib import Tree

from ramstk.dao import DAO
from ramstk.dao import RAMSTKSimilarItem
from ramstk.modules.similar_item import dtmSimilarItem, dtcSimilarItem

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2018 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'revision_id': 1,
    'hardware_id': 1,
    'change_description_1': b'',
    'change_description_2': b'',
    'change_description_3': b'',
    'change_description_4': b'',
    'change_description_5': b'',
    'change_description_6': b'',
    'change_description_7': b'',
    'change_description_8': b'',
    'change_description_9': b'',
    'change_description_10': b'',
    'change_factor_1': 1.0,
    'change_factor_2': 1.0,
    'change_factor_3': 1.0,
    'change_factor_4': 1.0,
    'change_factor_5': 1.0,
    'change_factor_6': 1.0,
    'change_factor_7': 1.0,
    'change_factor_8': 1.0,
    'change_factor_9': 1.0,
    'change_factor_10': 1.0,
    'environment_from_id': 0,
    'environment_to_id': 0,
    'function_1': '',
    'function_2': '',
    'function_3': '',
    'function_4': '',
    'function_5': '',
    'method_id': 0,
    'parent_id': 0,
    'quality_from_id': 0,
    'quality_to_id': 0,
    'result_1': 0.0,
    'result_2': 0.0,
    'result_3': 0.0,
    'result_4': 0.0,
    'result_5': 0.0,
    'temperature_from': 30.0,
    'temperature_to': 30.0,
    'user_blob_1': b'',
    'user_blob_2': b'',
    'user_blob_3': b'',
    'user_blob_4': b'',
    'user_blob_5': b'',
    'user_float_1': 0.0,
    'user_float_2': 0.0,
    'user_float_3': 0.0,
    'user_float_4': 0.0,
    'user_float_5': 0.0,
    'user_int_1': 0,
    'user_int_2': 0,
    'user_int_3': 0,
    'user_int_4': 0,
    'user_int_5': 0
}


@pytest.mark.integration
def test_create_similar_item_data_model(test_dao):
    """ __init__ should return instance of SimilarItem data model. """
    DUT = dtmSimilarItem(test_dao, test=True)

    assert isinstance(DUT, dtmSimilarItem)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a treelib Tree() on success when selecting SimilarItems. """
    DUT = dtmSimilarItem(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.tree.get_node(2).data, RAMSTKSimilarItem)


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RAMSTKSimilarItem data model on success. """
    DUT = dtmSimilarItem(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _similar_item = DUT.do_select(2)

    assert isinstance(_similar_item, RAMSTKSimilarItem)
    assert _similar_item.hardware_id == 2
    assert _similar_item.change_description_1 == b''
    assert _similar_item.parent_id == 1


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent SimilarItem ID is requested. """
    DUT = dtmSimilarItem(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _similar_item = DUT.do_select(100)

    assert _similar_item is None


@pytest.mark.integration
def test_do_select_children(test_dao):
    """ do_select_children() should return the immediate subtree of the passed node ID. """
    DUT = dtmSimilarItem(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _nodes = DUT.do_select_children(1)

    assert isinstance(_nodes, list)
    assert isinstance(_nodes[0].data, RAMSTKSimilarItem)
    assert _nodes[0].identifier == 2


@pytest.mark.integration
def test_do_insert(test_dao):
    """ do_insert() should return a zero error code on success. """
    DUT = dtmSimilarItem(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_insert(
        revision_id=1, hardware_id=15, parent_id=1)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Adding one or more items to the RAMSTK "
                    "Program database.")
    assert DUT.last_id == 15


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmSimilarItem(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Deleting an item from the RAMSTK Program "
                    "database.")


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a Revision ID that doesn't exist. """
    DUT = dtmSimilarItem(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code == 2005
    assert _msg == (
        "  RAMSTK ERROR: Attempted to delete non-existent SimilarItem "
        "ID 300.")


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmSimilarItem(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _similar_item = DUT.do_select(1)
    _similar_item.n_sub_systems = 2

    _error_code, _msg = DUT.do_update(1)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating the RAMSTK Program database.")


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed an SimilarItem ID that doesn't exist. """
    DUT = dtmSimilarItem(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2207
    assert _msg == ("RAMSTK ERROR: Attempted to save non-existent SimilarItem "
                    "ID 100.")


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmSimilarItem(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Updating all line items in the similar item "
        "analysis worksheet.")


@pytest.mark.integration
def test_do_calculate_topic_633(test_dao):
    """ do_calculate() should return False on success when using Topic 633 similar item analysis. """
    DUT = dtmSimilarItem(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _node = DUT.do_select(1)
    _node.method_id = 1
    _node.temperature_from = 27.5
    _node.temperature_to = 35.0
    _node.quality_from_id = 2
    _node.quality_to_id = 3
    _node.environment_from_id = 1
    _node.environment_to_id = 3

    assert not DUT.do_calculate(1, hazard_rate=2.5003126e-06)
    assert _node.change_factor_1 == 0.6
    assert _node.change_factor_2 == 0.3
    assert _node.change_factor_3 == 0.9
    assert _node.result_1 == pytest.approx(1.5434028e-05)


@pytest.mark.integration
def test_do_calculate_user_defined(test_dao):
    """ do_calculate() should return False on success when using user defined similar item analysis. """
    DUT = dtmSimilarItem(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _node = DUT.do_select(1)
    _node.method_id = 2
    _node.change_factor_1 = 0.75
    _node.change_factor_2 = 1.2
    _node.change_factor_3 = 0.95
    _node.change_factor_4 = 1.05
    _node.function_1 = 'hr * pi1 * pi2 * pi3 *pi4'

    assert not DUT.do_calculate(1, hazard_rate=2.5003126e-06)
    assert _node.result_1 == pytest.approx(2.2446556e-06)


@pytest.mark.integration
def test_do_roll_up(test_dao):
    """ do_roll_up() should return False on success. """
    DUT = dtmSimilarItem(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    for _node in DUT.do_select_children(1):
        _attributes = _node.data.get_attributes()
        _attributes['change_description_1'] = ((
            'This is change description 1 '
            'for Node ID: {0:d}').format(
                _attributes['hardware_id'])).encode('utf-8')
        _node.data.set_attributes(_attributes)

    DUT.do_update_all()
    DUT.do_select_all(revision_id=1)

    assert not DUT.do_roll_up(1)
    assert DUT.do_select(1).get_attributes()['change_description_1'] == (
        b'This is change description 1 for Node ID: 2\n\nThis is change '
        b'description 1 for Node ID: 3\n\nThis is change description 1 for '
        b'Node ID: 4\n\nThis is change description 1 for Node ID: 5\n\n')


@pytest.mark.integration
def test_create_similar_item_data_controller(test_dao, test_configuration):
    """ __init__() should return instance of SimilarItem data controller. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')

    assert isinstance(DUT, dtcSimilarItem)
    assert isinstance(DUT._dtm_data_model, dtmSimilarItem)


@pytest.mark.integration
def test_request_do_select_all(test_dao, test_configuration):
    """ request_do_select_all() should return a Tree of RAMSTKSimilarItem data models. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert isinstance(DUT._dtm_data_model.tree, Tree)
    assert isinstance(
        DUT._dtm_data_model.tree.get_node(2).data, RAMSTKSimilarItem)


@pytest.mark.integration
def test_request_do_select(test_dao, test_configuration):
    """ request_do_select() should return an RAMSTKSimilarItem data model. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert isinstance(DUT.request_do_select(2), RAMSTKSimilarItem)


@pytest.mark.integration
def test_request_do_select_non_existent_id(test_dao, test_configuration):
    """ request_do_select() should return None when requesting an SimilarItem that doesn't exist. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT.request_do_select(100) is None


@pytest.mark.integration
def test_request_do_insert(test_dao, test_configuration):
    """ request_do_insert() should return False on success. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_insert(
        revision_id=1, hardware_id=10, parent_id=1)


@pytest.mark.integration
def test_request_do_delete(test_dao, test_configuration):
    """ request_do_delete() should return False on success. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_delete(10)


@pytest.mark.integration
def test_request_do_delete_non_existent_id(test_dao, test_configuration):
    """ request_do_delete() should return True when attempting to delete a non-existent SimilarItem. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT.request_do_delete(100)


@pytest.mark.integration
def test_request_do_update(test_dao, test_configuration):
    """ request_do_update() should return False on success. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_update(2)


@pytest.mark.integration
def test_request_do_update_non_existent_id(test_dao, test_configuration):
    """ request_do_update() should return True when attempting to save a non-existent SimilarItem. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT.request_do_update(100)


@pytest.mark.integration
def test_request_do_update_all(test_dao, test_configuration):
    """ request_do_update_all() should return False on success. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_update_all()


@pytest.mark.integration
def test_request_do_calculate(test_dao, test_configuration):
    """ request_do_calculate() should return False on success. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    DUT.request_do_select(1).method_id = 2
    DUT.request_do_select(1).change_factor_1 = 0.75
    DUT.request_do_select(1).change_factor_2 = 1.2
    DUT.request_do_select(1).change_factor_3 = 0.95
    DUT.request_do_select(1).change_factor_4 = 1.05
    DUT.request_do_select(1).function_1 = 'hr * pi1 * pi2 * pi3 *pi4'

    assert not DUT.request_do_calculate(1, hazard_rate=2.5003126e-06)
    assert DUT.request_do_select(1).result_1 == pytest.approx(2.2446556e-06)


@pytest.mark.integration
def test_request_do_calculate_all(test_dao, test_configuration):
    """ request_do_calculate_all() should return False on success. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_calculate_all(hazard_rate=24.5003126e-06)


@pytest.mark.integration
def test_request_do_roll_up(test_dao, test_configuration):
    """ request_do_roll_up() should return False on success. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    for _node in DUT.request_do_select_children(1):
        _attributes = _node.data.get_attributes()
        _attributes['change_description_1'] = ((
            'This is change description 1 '
            'for Node ID: {0:d}').format(
                _attributes['hardware_id'])).encode('utf-8')
        _node.data.set_attributes(_attributes)

    DUT.request_do_update_all()
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_roll_up(1)
    assert DUT.request_do_select(1).get_attributes(
    )['change_description_1'] == (
        b'This is change description 1 for Node ID: 2\n\nThis is change '
        b'description 1 for Node ID: 3\n\nThis is change description 1 for '
        b'Node ID: 4\n\nThis is change description 1 for Node ID: 5\n\n')
