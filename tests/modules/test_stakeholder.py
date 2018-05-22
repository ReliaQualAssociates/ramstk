#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.modules.test_stakeholder.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing Stakeholder module algorithms and models."""

from treelib import Tree

import pytest

from rtk.modules.stakeholder import dtmStakeholder, dtcStakeholder
from rtk.dao import DAO
from rtk.dao import RTKStakeholder

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "weibullguy" Rowland'


@pytest.mark.integration
def test_create_data_model(test_dao):
    """ __init__() should return a Stakeholder model. """
    DUT = dtmStakeholder(test_dao)

    assert isinstance(DUT, dtmStakeholder)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_select_all(test_dao):
    """ select_all() should return a Tree() object populated with RTKStakeholder instances on success. """
    DUT = dtmStakeholder(test_dao)

    _tree = DUT.select_all(1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RTKStakeholder)


@pytest.mark.integration
def test_select(test_dao):
    """ select() should return an instance of the RTKStakeholder data model on success. """
    DUT = dtmStakeholder(test_dao)
    DUT.select_all(1)

    _stakeholder = DUT.select(1)

    assert isinstance(_stakeholder, RTKStakeholder)
    assert _stakeholder.stakeholder_id == 1
    assert _stakeholder.description == 'Test Stakeholder Input'


@pytest.mark.integration
def test_select_non_existent_id(test_dao):
    """ select() should return None when a non-existent Stakeholder ID is requested. """
    DUT = dtmStakeholder(test_dao)

    _stakeholder = DUT.select(100)

    assert _stakeholder is None


@pytest.mark.integration
def test_insert(test_dao):
    """ insert() should return False on success. """
    DUT = dtmStakeholder(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(revision_id=1)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Adding one or more items to the RTK Program '
                    'database.')
    assert DUT.last_id == 2


@pytest.mark.integration
def test_delete(test_dao):
    """ delete() should return a zero error code on success. """
    DUT = dtmStakeholder(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(2)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Deleting an item from the RTK Program '
                    'database.')


@pytest.mark.integration
def test_delete_non_existent_id(test_dao):
    """ delete() should return a non-zero error code when passed a Stakeholder ID that doesn't exist. """
    DUT = dtmStakeholder(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(300)

    assert _error_code == 2005
    assert _msg == ('  RTK ERROR: Attempted to delete non-existent '
                    'Stakeholder ID 300.')


@pytest.mark.integration
def test_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmStakeholder(test_dao)
    DUT.select_all(1)

    _stakeholder = DUT.select(1)
    _stakeholder.description = 'Be very reliable.'

    _error_code, _msg = DUT.update(1)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')


@pytest.mark.integration
def test_update_non_existent_id(test_dao):
    """ update() should return a non-zero error code when passed a Stakeholder ID that doesn't exist. """
    DUT = dtmStakeholder(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2006
    assert _msg == ('RTK ERROR: Attempted to save non-existent Stakeholder ID '
                    '100.')


@pytest.mark.integration
def test_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmStakeholder(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')


@pytest.mark.integration
def test_calculate_weight(test_dao):
    """ calculate_weight() returns False on success and calculate values are correct. """
    DUT = dtmStakeholder(test_dao)
    DUT.select_all(1)
    _stakeholder = DUT.select(1)

    _stakeholder.planned_rank = 4
    _stakeholder.customer_rank = 2
    _stakeholder.priority = 2
    _stakeholder.user_float_1 = 1.0
    _stakeholder.user_float_2 = 2.0
    _stakeholder.user_float_3 = 3.0
    _stakeholder.user_float_4 = 4.0
    _stakeholder.user_float_5 = 5.0

    assert not DUT.calculate_weight(1)
    assert _stakeholder.improvement == 1.4
    assert _stakeholder.overall_weight == pytest.approx(336.0)


@pytest.mark.integration
def test_data_controller_create(test_dao, test_configuration):
    """ __init__() should create a Stakeholder data controller. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcStakeholder)
    assert isinstance(DUT._dtm_data_model, dtmStakeholder)


@pytest.mark.integration
def test_request_select_all(test_dao, test_configuration):
    """ request_select_all() should return a Tree of RTKStakeholder models. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)

    _tree = DUT.request_select_all(1)

    assert isinstance(_tree.get_node(1).data, RTKStakeholder)


@pytest.mark.integration
def test_request_select(test_dao, test_configuration):
    """ request_select() should return an RTKStakeholder model. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _stakeholder = DUT.request_select(1)

    assert isinstance(_stakeholder, RTKStakeholder)


@pytest.mark.integration
def test_request_select_non_existent_id(test_dao, test_configuration):
    """ request_select() should return None when requesting a Stakeholder that doesn't exist. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _stakeholder = DUT.request_select(100)

    assert _stakeholder is None


@pytest.mark.integration
def test_request_insert(test_dao, test_configuration):
    """ request_insert() should return False on success. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_insert(revision_id=1)


@pytest.mark.integration
def test_request_delete(test_dao, test_configuration):
    """ request_delete() should return False on success. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_delete(2)


@pytest.mark.integration
def test_request_delete_non_existent_id(test_dao, test_configuration):
    """ request_delete() should return True when attempting to delete a non-existent Stakeholder. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert DUT.request_delete(100)


@pytest.mark.integration
def test_request_update(test_dao, test_configuration):
    """ request_update() should return False on success. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_update(1)


@pytest.mark.integration
def test_request_update_non_existent_id(test_dao, test_configuration):
    """ request_update() should return True when attempting to save a non-existent Stakeholder. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert DUT.request_update(100)


@pytest.mark.integration
def test_request_update_all(test_dao, test_configuration):
    """ request_update_all() should return False on success. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_update_all()


@pytest.mark.integration
def test_request_calculate_weight(test_dao, test_configuration):
    """ request_calculate_weight() should return False on success. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _stakeholder = DUT.request_select(1)
    _stakeholder.planned_rank = 4
    _stakeholder.customer_rank = 2
    _stakeholder.priority = 2
    _stakeholder.user_float_1 = 1.0
    _stakeholder.user_float_2 = 2.0
    _stakeholder.user_float_3 = 3.0
    _stakeholder.user_float_4 = 4.0
    _stakeholder.user_float_5 = 5.0

    assert not DUT.request_calculate_weight(1)
    assert _stakeholder.improvement == 1.4
    assert _stakeholder.overall_weight == pytest.approx(336.0)
