#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.modules.test_similar_item.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2018 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the SimilarItem class."""

import pytest

from treelib import Tree

from rtk.dao import DAO
from rtk.dao import RTKSimilarItem
from rtk.modules.similar_item import dtmSimilarItem, dtcSimilarItem

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2018 Andrew "Weibullguy" Rowland'


@pytest.mark.integration
def test_create_similar_item_data_model(test_dao):
    """ __init__ should return instance of SimilarItem data model. """
    DUT = dtmSimilarItem(test_dao)

    assert isinstance(DUT, dtmSimilarItem)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_select_all(test_dao):
    """select_all() should return a treelib Tree() on success when selecting SimilarItems."""
    DUT = dtmSimilarItem(test_dao)
    _tree = DUT.select_all(1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(2).data, RTKSimilarItem)


@pytest.mark.integration
def test_select(test_dao):
    """select() should return an instance of the RTKSimilarItem data model on success."""
    DUT = dtmSimilarItem(test_dao)
    DUT.select_all(1)

    _similar_item = DUT.select(2)

    assert isinstance(_similar_item, RTKSimilarItem)
    assert _similar_item.hardware_id == 2
    assert _similar_item.change_description_1 == ''
    assert _similar_item.parent_id == 1


@pytest.mark.integration
def test_select_non_existent_id(test_dao):
    """select() should return None when a non-existent SimilarItem ID is requested."""
    DUT = dtmSimilarItem(test_dao)
    DUT.select_all(1)

    _similar_item = DUT.select(100)

    assert _similar_item is None


@pytest.mark.integration
def test_select_children(test_dao):
    """select_children() should return the immediate subtree of the passed node ID."""
    DUT = dtmSimilarItem(test_dao)
    DUT.select_all(1)

    _nodes = DUT.select_children(1)

    assert isinstance(_nodes, list)
    assert isinstance(_nodes[0].data, RTKSimilarItem)
    assert _nodes[0].identifier == 2


@pytest.mark.integration
def test_insert(test_dao):
    """insert() should return a zero error code on success."""
    DUT = dtmSimilarItem(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(revision_id=1, hardware_id=15, parent_id=1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK "
                    "Program database.")
    assert DUT.last_id == 15


@pytest.mark.integration
def test_delete(test_dao):
    """delete() should return a zero error code on success."""
    DUT = dtmSimilarItem(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Deleting an item from the RTK Program "
                    "database.")


@pytest.mark.integration
def test_delete_non_existent_id(test_dao):
    """delete() should return a non-zero error code when passed a Revision ID that doesn't exist."""
    DUT = dtmSimilarItem(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(300)

    assert _error_code == 2005
    assert _msg == (
        "  RTK ERROR: Attempted to delete non-existent SimilarItem "
        "ID 300.")


@pytest.mark.integration
def test_update(test_dao):
    """update() should return a zero error code on success."""
    DUT = dtmSimilarItem(test_dao)
    DUT.select_all(1)

    _similar_item = DUT.select(1)
    _similar_item.n_sub_systems = 2

    _error_code, _msg = DUT.update(1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
def test_update_non_existent_id(test_dao):
    """update() should return a non-zero error code when passed an SimilarItem ID that doesn't exist."""
    DUT = dtmSimilarItem(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2207
    assert _msg == ("RTK ERROR: Attempted to save non-existent SimilarItem "
                    "ID 100.")


@pytest.mark.integration
def test_update_all(test_dao):
    """update_all() should return a zero error code on success."""
    DUT = dtmSimilarItem(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
def test_topic_633(test_dao):
    """calculate() should return False on success when using Topic 633 similar item analysis."""
    DUT = dtmSimilarItem(test_dao)
    DUT.select_all(1)

    _node = DUT.select(1)
    _node.method_id = 1
    _node.temperature_from = 27.5
    _node.temperature_to = 35.0
    _node.quality_from_id = 2
    _node.quality_to_id = 3
    _node.environment_from_id = 1
    _node.environment_to_id = 3

    assert not DUT.calculate(1, 2.5003126e-06)
    assert _node.change_factor_1 == 0.6
    assert _node.change_factor_2 == 0.3
    assert _node.change_factor_3 == 0.9
    assert _node.result_1 == pytest.approx(1.5434028e-05)


@pytest.mark.integration
def test_user_defined(test_dao):
    """calculate() should return False on success when using user defined similar item analysis."""
    DUT = dtmSimilarItem(test_dao)
    DUT.select_all(1)

    _node = DUT.select(1)
    _node.method_id = 2
    _node.change_factor_1 = 0.75
    _node.change_factor_2 = 1.2
    _node.change_factor_3 = 0.95
    _node.change_factor_4 = 1.05
    _node.function_1 = 'hr * pi1 * pi2 * pi3 *pi4'

    assert not DUT.calculate(1, 2.5003126e-06)
    assert _node.result_1 == pytest.approx(2.2446556e-06)


@pytest.mark.integration
def test_create_similar_item_data_controller(test_dao, test_configuration):
    """ __init__ should return instance of SimilarItem data controller. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')

    assert isinstance(DUT, dtcSimilarItem)
    assert isinstance(DUT._dtm_data_model, dtmSimilarItem)


@pytest.mark.integration
def test_request_select_all(test_dao, test_configuration):
    """ request_select_all() should return a Tree of RTKSimilarItem data models. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')

    _tree = DUT.request_select_all(1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(2).data, RTKSimilarItem)


@pytest.mark.integration
def test_request_select(test_dao, test_configuration):
    """ request_select() should return an RTKSimilarItem data model. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    assert isinstance(DUT.request_select(2), RTKSimilarItem)


@pytest.mark.integration
def test_request_non_existent_id(test_dao, test_configuration):
    """ request_select() should return None when requesting an SimilarItem that doesn't exist. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    assert DUT.request_select(100) is None


@pytest.mark.integration
def test_request_insert(test_dao, test_configuration):
    """ request_insert() should return False on success. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    assert not DUT.request_insert(revision_id=1, hardware_id=10, parent_id=1)


@pytest.mark.integration
def test_request_delete(test_dao, test_configuration):
    """ request_delete() should return False on success. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    assert not DUT.request_delete(10)


@pytest.mark.integration
def test_request_delete_non_existent_id(test_dao, test_configuration):
    """ request_delete() should return True when attempting to delete a non-existent SimilarItem. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    assert DUT.request_delete(100)


@pytest.mark.integration
def test_request_update(test_dao, test_configuration):
    """ request_update() should return False on success. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    assert not DUT.request_update(2)


@pytest.mark.integration
def test_request_update_non_existent_id(test_dao, test_configuration):
    """ request_update() should return True when attempting to save a non-existent SimilarItem. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    assert DUT.request_update(100)


@pytest.mark.integration
def test_request_update_all(test_dao, test_configuration):
    """ request_update_all() should return False on success. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    assert not DUT.request_update_all()


@pytest.mark.integration
def test_request_calculate(test_dao, test_configuration):
    """ request_calculate() should return False on success. """
    DUT = dtcSimilarItem(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    DUT.request_select(1).method_id = 2
    DUT.request_select(1).change_factor_1 = 0.75
    DUT.request_select(1).change_factor_2 = 1.2
    DUT.request_select(1).change_factor_3 = 0.95
    DUT.request_select(1).change_factor_4 = 1.05
    DUT.request_select(1).function_1 = 'hr * pi1 * pi2 * pi3 *pi4'

    assert not DUT.request_calculate(1, 2.5003126e-06)
    assert DUT.request_select(1).result_1 == pytest.approx(2.2446556e-06)
