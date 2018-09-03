#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.modules.test_allocation.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2018 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Allocation class. """

import pytest

from treelib import Tree

from rtk.dao import DAO, RAMSTKAllocation
from rtk.modules.allocation import dtmAllocation, dtcAllocation

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2018 Andrew "Weibullguy" Rowland'


@pytest.mark.integration
def test_create_allocation_data_model(test_dao):
    """ __init__ should return instance of Allocation data model. """
    DUT = dtmAllocation(test_dao)

    assert isinstance(DUT, dtmAllocation)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a treelib Tree() on success when selecting Allocations. """
    DUT = dtmAllocation(test_dao)
    _tree = DUT.do_select_all(revision_id=1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(2).data, RAMSTKAllocation)


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RAMSTKAllocation data model on success. """
    DUT = dtmAllocation(test_dao)
    DUT.do_select_all(revision_id=1)

    _allocation = DUT.do_select(2)

    assert isinstance(_allocation, RAMSTKAllocation)
    assert _allocation.hardware_id == 2
    assert _allocation.availability_alloc == 0.0
    assert _allocation.parent_id == 1


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent Allocation ID is requested. """
    DUT = dtmAllocation(test_dao)
    DUT.do_select_all(revision_id=1)

    _allocation = DUT.do_select(100)

    assert _allocation is None


@pytest.mark.integration
def test_do_select_children(test_dao):
    """ do_select_children() should return the immediate subtree of the passed node ID. """
    DUT = dtmAllocation(test_dao)
    DUT.do_select_all(revision_id=1)

    _nodes = DUT.do_select_children(1)

    assert isinstance(_nodes, list)
    assert isinstance(_nodes[0].data, RAMSTKAllocation)
    assert _nodes[0].identifier == 2


@pytest.mark.integration
def test_do_insert(test_dao):
    """ do_insert() should return a zero error code on success. """
    DUT = dtmAllocation(test_dao)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_insert(
        revision_id=1, hardware_id=9, parent_id=1)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Adding one or more items to the RAMSTK "
                    "Program database.")
    assert DUT.last_id == 9


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmAllocation(test_dao)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Deleting an item from the RAMSTK Program "
                    "database.")
    assert DUT.last_id == 8


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a Revision ID that doesn't exist. """
    DUT = dtmAllocation(test_dao)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code == 1
    assert _msg == ("\n  RAMSTK ERROR: Attempted to delete non-existent Allocation "
                    "ID 300.")


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmAllocation(test_dao)
    DUT.do_select_all(revision_id=1)

    _allocation = DUT.do_select(1)
    _allocation.n_sub_systems = 2

    _error_code, _msg = DUT.do_update(1)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating the RAMSTK Program database.")


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed an Allocation ID that doesn't exist. """
    DUT = dtmAllocation(test_dao)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2207
    assert _msg == ("RAMSTK ERROR: Attempted to save non-existent Allocation "
                    "ID 100.")


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmAllocation(test_dao)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating all line items in the reliability "
                    "allocation analysis worksheet.")


@pytest.mark.integration
def test_do_calculate_equal_apportionment(test_dao):
    """ do_calculate() should return False on success when using equal apportionment. """
    DUT = dtmAllocation(test_dao)
    DUT.do_select_all(revision_id=1)

    _parent = DUT.do_select(1)
    _parent.reliability_goal = 0.99975
    _children = DUT.do_select_children(1)

    assert not DUT.do_calculate(1)
    assert _parent.hazard_rate_goal == pytest.approx(2.5003126e-06)
    assert _parent.mtbf_goal == pytest.approx(399949.9979165)
    for _child in _children:
        assert _child.data.reliability_alloc == pytest.approx(0.9999375)
        assert _child.data.mtbf_alloc == pytest.approx(1599799.9916666)


@pytest.mark.integration
def test_do_calculate_agree_apportionment(test_dao):
    """ do_calculate() should return False on success when using AGREE apportionment. """
    DUT = dtmAllocation(test_dao)
    DUT.do_select_all(revision_id=1)

    _parent = DUT.do_select(1)
    _parent.method_id = 2
    _parent.reliability_goal = 0.99975
    _children = DUT.do_select_children(1)

    _children[0].data.weight_factor = 0.2
    _children[1].data.weight_factor = 0.4
    _children[2].data.weight_factor = 0.6
    _children[3].data.weight_factor = 0.7

    assert not DUT.do_calculate(1)
    assert _parent.hazard_rate_goal == pytest.approx(2.5003126e-06)
    assert _parent.mtbf_goal == pytest.approx(399949.9979165)
    assert _children[0].data.reliability_alloc == pytest.approx(0.9996875)
    assert _children[1].data.reliability_alloc == pytest.approx(0.9998437)
    assert _children[2].data.reliability_alloc == pytest.approx(0.9998958)
    assert _children[3].data.reliability_alloc == pytest.approx(0.9999107)


@pytest.mark.integration
def test_do_calculate_arinc_apportionment(test_dao):
    """ do_calculate() should return False on success when using ARINC apportionment. """
    DUT = dtmAllocation(test_dao)
    DUT.do_select_all(revision_id=1)

    # The [parent, child 1, child 2, child 3, child 4] hazard rates.
    _hazard_rates = [0.005862, 0.000392, 0.000168, 0.0000982, 0.000212]

    _parent = DUT.do_select(1)
    _parent.method_id = 3
    _parent.reliability_goal = 0.99975
    _children = DUT.do_select_children(1)

    _children[0].data.weight_factor = 0.2
    _children[1].data.weight_factor = 0.4
    _children[2].data.weight_factor = 0.6
    _children[3].data.weight_factor = 0.7

    assert not DUT.do_calculate(1, hazard_rates=_hazard_rates)
    assert _parent.hazard_rate_goal == pytest.approx(2.5003126e-06)
    assert _parent.mtbf_goal == pytest.approx(399949.9979165)
    assert _children[0].data.reliability_alloc == pytest.approx(0.9999833)
    assert _children[1].data.reliability_alloc == pytest.approx(0.9999928)
    assert _children[2].data.reliability_alloc == pytest.approx(0.9999958)
    assert _children[3].data.reliability_alloc == pytest.approx(0.9999910)


@pytest.mark.integration
def test_do_calculate_foo_apportionment(test_dao):
    """ do_calculate() should return False on success when using FOO apportionment. """
    DUT = dtmAllocation(test_dao)
    DUT.do_select_all(revision_id=1)

    # The [parent, child 1, child 2, child 3, child 4] hazard rates.
    _hazard_rates = [0.005862, 0.000392, 0.000168, 0.0000982, 0.000212]

    _parent = DUT.do_select(1)
    _parent.method_id = 4
    _parent.goal_measure_id = 2
    _parent.hazard_rate_goal = 2.5003126e-06
    _children = DUT.do_select_children(1)

    i = 1
    for _child in _children:
        _child.data.int_factor = 2 * i
        _child.data.soa_factor = 3 * i
        _child.data.op_time_factor = 3 * i + 1
        _child.data.env_factor = i + 1
        i += 1

    assert not DUT.do_calculate(1)
    assert _parent.weight_factor == 8952
    assert _parent.reliability_goal == pytest.approx(0.99975)
    assert _parent.mtbf_goal == pytest.approx(399949.9979165)
    assert _children[0].data.reliability_alloc == pytest.approx(0.9999987)
    assert _children[1].data.reliability_alloc == pytest.approx(0.9999859)
    assert _children[2].data.reliability_alloc == pytest.approx(0.9999397)
    assert _children[3].data.reliability_alloc == pytest.approx(0.9998257)


@pytest.mark.integration
def test_do_calculate_all(test_dao):
    """ do_calculate_all() should return False on success. """
    DUT = dtmAllocation(test_dao)
    DUT.do_select_all(revision_id=1)

    assert not DUT.do_calculate_all()


@pytest.mark.integration
def test_create_allocation_data_controller(test_dao, test_configuration):
    """ __init__() should return instance of Allocation data controller. """
    DUT = dtcAllocation(test_dao, test_configuration, test='True')

    assert isinstance(DUT, dtcAllocation)
    assert isinstance(DUT._dtm_data_model, dtmAllocation)


@pytest.mark.integration
def test_request_do_select_all(test_dao, test_configuration):
    """ request_do_select_all() should return a Tree of RAMSTKAllocation data models. """
    DUT = dtcAllocation(test_dao, test_configuration, test='True')

    _tree = DUT.request_do_select_all(revision_id=1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(2).data, RAMSTKAllocation)


@pytest.mark.integration
def test_request_do_select(test_dao, test_configuration):
    """ request_do_select() should return an RAMSTKAllocation data model. """
    DUT = dtcAllocation(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(revision_id=1)

    assert isinstance(DUT.request_do_select(2), RAMSTKAllocation)


@pytest.mark.integration
def test_request_do_select_non_existent_id(test_dao, test_configuration):
    """ request_do_select() should return None when requesting an Allocation that doesn't exist. """
    DUT = dtcAllocation(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(revision_id=1)

    assert DUT.request_do_select(100) is None


@pytest.mark.integration
def test_request_do_insert(test_dao, test_configuration):
    """ request_do_insert() should return False on success. """
    DUT = dtcAllocation(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(revision_id=1)

    assert not DUT.request_do_insert(
        revision_id=1, hardware_id=10, parent_id=1)


@pytest.mark.integration
def test_request_do_delete(test_dao, test_configuration):
    """ request_do_delete() should return False on success. """
    DUT = dtcAllocation(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(revision_id=1)

    assert not DUT.request_do_delete(10)


@pytest.mark.integration
def test_request_do_delete_non_existent_id(test_dao, test_configuration):
    """ request_do_delete() should return True when attempting to delete a non-existent Allocation. """
    DUT = dtcAllocation(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(revision_id=1)

    assert DUT.request_do_delete(100)


@pytest.mark.integration
def test_request_do_update(test_dao, test_configuration):
    """ request_do_update() should return False on success. """
    DUT = dtcAllocation(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(revision_id=1)

    assert not DUT.request_do_update(2)


@pytest.mark.integration
def test_request_do_update_non_existent_id(test_dao, test_configuration):
    """ request_do_update() should return True when attempting to save a non-existent Allocation. """
    DUT = dtcAllocation(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(revision_id=1)

    assert DUT.request_do_update(100)


@pytest.mark.integration
def test_request_do_update_all(test_dao, test_configuration):
    """ request_do_update_all() should return False on success. """
    DUT = dtcAllocation(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(revision_id=1)

    assert not DUT.request_do_update_all()


@pytest.mark.integration
def test_request_do_calculate(test_dao, test_configuration):
    """ request_do_calculate() should return False on success. """
    DUT = dtcAllocation(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(revision_id=1)

    DUT.request_do_select(1).reliability_goal = 0.99975

    assert not DUT.request_do_calculate(1, method='arinc')

@pytest.mark.integration
def test_request_do_calculate_all(test_dao, test_configuration):
    """ request_do_calculate_all() should return False on success. """
    DUT = dtcAllocation(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(revision_id=1)

    DUT.request_do_select(1).reliability_goal = 0.99975

    assert not DUT.request_do_calculate_all(method='arinc')
