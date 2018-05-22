#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.modules.test_validation.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing Validation module algorithms and models. """

from treelib import Tree

import pytest

from rtk.dao import DAO
from rtk.dao import RTKValidation
from rtk.modules.validation import dtmValidation, dtcValidation

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "weibullguy" Rowland'


@pytest.mark.integration
def test_data_model_create(test_dao):
    """ __init__() should return a Validation model. """
    DUT = dtmValidation(test_dao)

    assert isinstance(DUT, dtmValidation)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_select_all(test_dao):
    """ select_all() should return a Tree() object populated with RTKValidation instances on success. """
    DUT = dtmValidation(test_dao)
    _tree = DUT.select_all(1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RTKValidation)


@pytest.mark.integration
def test_select(test_dao):
    """ select() should return an instance of the RTKValidation data model on success. """
    DUT = dtmValidation(test_dao)
    DUT.select_all(1)

    _validation = DUT.select(1)

    assert isinstance(_validation, RTKValidation)
    assert _validation.validation_id == 1


@pytest.mark.integration
def test_select_non_existent_id(test_dao):
    """ select() should return None when a non-existent Validation ID is requested. """
    DUT = dtmValidation(test_dao)
    _validation = DUT.select(100)

    assert _validation is None


@pytest.mark.integration
def test_insert(test_dao):
    """ insert() should return False on success. """
    DUT = dtmValidation(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(revision_id=1)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Adding one or more items to the RTK Program '
                    'database.')
    assert DUT.last_id == 2


@pytest.mark.integration
def test_delete(test_dao):
    """ delete() should return a zero error code on success. """
    DUT = dtmValidation(test_dao)
    DUT.select_all(1)
    DUT.insert(revision_id=1)

    _error_code, _msg = DUT.delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Deleting an item from the RTK Program '
                    'database.')


@pytest.mark.integration
def test_delete_non_existent_id(test_dao):
    """ delete() should return a non-zero error code when passed a Validation ID that doesn't exist. """
    DUT = dtmValidation(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(300)

    assert _error_code == 2005
    assert _msg == ('  RTK ERROR: Attempted to delete non-existent '
                    'Validation ID 300.')


@pytest.mark.integration
def test_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmValidation(test_dao)
    DUT.select_all(1)

    _validation = DUT.select(DUT.last_id)
    _validation.availability_logistics = 0.9832

    _error_code, _msg = DUT.update(DUT.last_id)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')


@pytest.mark.integration
def test_update_non_existent_id(test_dao):
    """ update() should return a non-zero error code when passed a Validation ID that doesn't exist. """
    DUT = dtmValidation(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2006
    assert _msg == ('RTK ERROR: Attempted to save non-existent Validation ID '
                    '100.')


@pytest.mark.integration
def test_update_status(test_dao):
    """ update_status() should return a zero error code on success. """
    DUT = dtmValidation(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update_status()

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')


@pytest.mark.integration
def test_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmValidation(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')


@pytest.mark.integration
def test_calculate_task_time(test_dao):
    """ calculate_task_time() returns False on successfully calculating tasks times. """
    DUT = dtmValidation(test_dao)
    DUT.select_all(1)
    _validation = DUT.select(1)
    _validation.time_minimum = 25.2
    _validation.time_average = 36.8
    _validation.time_maximum = 44.1
    _validation.confidence = 0.95

    assert not DUT.calculate_time(1)
    assert _validation.time_mean == pytest.approx(36.08333333)
    assert _validation.time_variance == pytest.approx(9.9225)


@pytest.mark.integration
def test_calculate_task_cost(test_dao):
    """ calculate_task_cost() returns False on successfully calculating tasks costs. """
    DUT = dtmValidation(test_dao)
    DUT.select_all(1)
    _validation = DUT.select(1)
    _validation.cost_minimum = 252.00
    _validation.cost_average = 368.00
    _validation.cost_maximum = 441.00
    _validation.confidence = 0.95

    assert not DUT.calculate_costs(1)
    assert _validation.cost_mean == pytest.approx(360.83333333)
    assert _validation.cost_variance == pytest.approx(992.25)


@pytest.mark.integration
def test_data_controller_create(test_dao, test_configuration):
    """ __init__() should return a Validation Data Controller. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcValidation)
    assert isinstance(DUT._dtm_data_model, dtmValidation)


@pytest.mark.integration
def test_request_select_all(test_dao, test_configuration):
    """ request_select_all() should return a Tree of RTKValidation models. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    _tree = DUT.request_select_all(1)

    assert isinstance(_tree.get_node(1).data, RTKValidation)


@pytest.mark.integration
def test_request_select(test_dao, test_configuration):
    """ request_select() should return an RTKValidation model. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert isinstance(DUT.request_select(1), RTKValidation)


@pytest.mark.integration
def test_request_non_existent_id(test_dao, test_configuration):
    """ request_select() should return None when requesting a Validation that doesn't exist. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)

    assert DUT.request_select(100) is None


@pytest.mark.integration
def test_request_insert(test_dao, test_configuration):
    """ request_insert() should return False on success. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_insert(revision_id=1)


@pytest.mark.integration
def test_request_delete(test_dao, test_configuration):
    """ request_delete() should return False on success. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_delete(2)


@pytest.mark.integration
def test_request_delete_non_existent_id(test_dao, test_configuration):
    """ request_delete() should return True when attempting to delete a non-existent Validation. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert DUT.request_delete(100)


@pytest.mark.integration
def test_request_update(test_dao, test_configuration):
    """ request_update() should return False on success. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_update(1)


@pytest.mark.integration
def test_request_update_non_existent_id(test_dao, test_configuration):
    """ request_update() should return True when attempting to save a non-existent Validation. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert DUT.request_update(100)


@pytest.mark.integration
def test_request_update_all(test_dao, test_configuration):
    """ request_update_all() should return False on success. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_update_all()


@pytest.mark.integration
def test_request_calculate(test_dao, test_configuration):
    """ request_calculate() should return False on success. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)
    _validation = DUT.request_select(1)
    _validation.cost_minimum = 252.00
    _validation.cost_average = 368.00
    _validation.cost_maximum = 441.00
    _validation.time_minimum = 25.2
    _validation.time_average = 36.8
    _validation.time_maximum = 44.1
    _validation.confidence = 0.95

    assert not DUT.request_calculate(1)
    assert _validation.time_mean == pytest.approx(36.08333333)
    assert _validation.time_variance == pytest.approx(9.9225)
    assert _validation.cost_mean == pytest.approx(360.83333333)
    assert _validation.cost_variance == pytest.approx(992.25)
