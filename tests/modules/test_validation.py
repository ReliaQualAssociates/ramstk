#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.modules.test_validation.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing Validation module algorithms and models. """

from treelib import Tree

import pytest

from rtk.dao import DAO
from rtk.dao import RAMSTKValidation
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
def test_do_select_all(test_dao):
    """ do_select_all() should return a Tree() object populated with RAMSTKValidation instances on success. """
    DUT = dtmValidation(test_dao)
    _tree = DUT.do_select_all(revision_id=1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RAMSTKValidation)


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RAMSTKValidation data model on success. """
    DUT = dtmValidation(test_dao)
    DUT.do_select_all(revision_id=1)

    _validation = DUT.do_select(1)

    assert isinstance(_validation, RAMSTKValidation)
    assert _validation.validation_id == 1


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent Validation ID is requested. """
    DUT = dtmValidation(test_dao)
    _validation = DUT.do_select(100)

    assert _validation is None


@pytest.mark.integration
def test_request_do_delete_matrix_row(test_dao, test_configuration):
    """ request_do_delete_matrix() should return False on successfully deleting a row. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all_matrix(1, 'vldtn_hrdwr')
    DUT.request_do_insert_matrix('vldtn_hrdwr', 5, 'Validation task from test')

    assert not DUT.request_do_delete_matrix('vldtn_hrdwr', 5)


@pytest.mark.integration
def test_request_do_delete_matrix_non_existent_row(test_dao,
                                                   test_configuration):
    """ request_do_delete_matrix() should return True when attempting to delete a non-existent row. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all_matrix(1, 'vldtn_hrdwr')

    assert DUT.request_do_delete_matrix('vldtn_hrdwr', 5)


@pytest.mark.integration
def test_request_do_delete_matrix_column(test_dao, test_configuration):
    """ request_do_delete_matrix() should return False on successfully deleting a column. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all_matrix(1, 'vldtn_hrdwr')
    DUT.request_do_insert_matrix('vldtn_hrdwr', 5, 'S1:SS1:A1', row=False)

    assert not DUT.request_do_delete_matrix('vldtn_hrdwr', 5, row=False)


@pytest.mark.integration
def test_do_insert(test_dao):
    """ do_insert() should return False on success. """
    DUT = dtmValidation(test_dao)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_insert(revision_id=1)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program '
                    'database.')
    assert DUT.last_id == 2


@pytest.mark.integration
def test_request_do_insert_matrix_row(test_dao, test_configuration):
    """ request_do_insert_matrix() should return False on successfully inserting a row. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_do_select_all_matrix(
        1, 'vldtn_hrdwr')

    assert not DUT.request_do_insert_matrix('vldtn_hrdwr', 5,
                                            'Validation task from test')
    assert DUT._dmx_vldtn_hw_matrix.dic_row_hdrs[
        5] == 'Validation task from test'


@pytest.mark.integration
def test_request_do_insert_matrix_duplicate_row(test_dao, test_configuration):
    """ request_do_insert_matrix() should return True when attempting to insert a duplicate row. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_do_select_all_matrix(
        1, 'vldtn_hrdwr')

    assert DUT.request_do_insert_matrix('vldtn_hrdwr', 1,
                                        'Validation task from test')


@pytest.mark.integration
def test_request_do_insert_matrix_column(test_dao, test_configuration):
    """ request_do_insert_matrix() should return False on successfully inserting a column. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_do_select_all_matrix(
        5, 'vldtn_hrdwr')

    assert not DUT.request_do_insert_matrix(
        'vldtn_hrdwr', 9, 'S1:SS1:A11', row=False)
    assert DUT._dmx_vldtn_hw_matrix.dic_column_hdrs[9] == 'S1:SS1:A11'


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmValidation(test_dao)
    DUT.do_select_all(revision_id=1)
    DUT.do_insert(revision_id=1)

    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Deleting an item from the RAMSTK Program '
                    'database.')


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a Validation ID that doesn't exist. """
    DUT = dtmValidation(test_dao)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code == 2005
    assert _msg == ('  RAMSTK ERROR: Attempted to delete non-existent '
                    'Validation ID 300.')


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmValidation(test_dao)
    DUT.do_select_all(revision_id=1)

    _validation = DUT.do_select(DUT.last_id)
    _validation.availability_logistics = 0.9832

    _error_code, _msg = DUT.do_update(DUT.last_id)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Updating the RAMSTK Program database.')


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed a Validation ID that doesn't exist. """
    DUT = dtmValidation(test_dao)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2006
    assert _msg == ('RAMSTK ERROR: Attempted to save non-existent Validation ID '
                    '100.')


@pytest.mark.integration
def test_do_update_status(test_dao):
    """ do_update_status() should return a zero error code on success. """
    DUT = dtmValidation(test_dao)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update_status()

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Updating the RAMSTK Program database.')


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmValidation(test_dao)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating all records in the validation "
                    "table.")


@pytest.mark.integration
def test_do_calculate_time(test_dao):
    """ do_calculate() returns False on successfully calculating tasks times. """
    DUT = dtmValidation(test_dao)
    DUT.do_select_all(revision_id=1)
    _validation = DUT.do_select(1)
    _validation.time_minimum = 25.2
    _validation.time_average = 36.8
    _validation.time_maximum = 44.1
    _validation.confidence = 0.95

    assert not DUT.do_calculate(1, metric='time')
    assert _validation.time_mean == pytest.approx(36.08333333)
    assert _validation.time_variance == pytest.approx(9.9225)


@pytest.mark.integration
def test_do_calculate_cost(test_dao):
    """ do_calculate() returns False on successfully calculating tasks costs. """
    DUT = dtmValidation(test_dao)
    DUT.do_select_all(revision_id=1)
    _validation = DUT.do_select(1)
    _validation.cost_minimum = 252.00
    _validation.cost_average = 368.00
    _validation.cost_maximum = 441.00
    _validation.confidence = 0.95

    assert not DUT.do_calculate(1, metric='cost')
    assert _validation.cost_mean == pytest.approx(360.83333333)
    assert _validation.cost_variance == pytest.approx(992.25)


@pytest.mark.integration
def test_data_controller_create(test_dao, test_configuration):
    """ __init__() should return a Validation Data Controller. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcValidation)
    assert isinstance(DUT._dtm_data_model, dtmValidation)


@pytest.mark.integration
def test_request_do_select_all(test_dao, test_configuration):
    """ request_do_select_all() should return a Tree of RAMSTKValidation models. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    _tree = DUT.request_do_select_all(revision_id=1)

    assert isinstance(_tree.get_node(1).data, RAMSTKValidation)


@pytest.mark.integration
def test_request_do_select(test_dao, test_configuration):
    """ request_do_select() should return an RAMSTKValidation model. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    assert isinstance(DUT.request_do_select(1), RAMSTKValidation)


@pytest.mark.integration
def test_request_do_select_non_existent_id(test_dao, test_configuration):
    """ request_do_select() should return None when requesting a Validation that doesn't exist. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)

    assert DUT.request_do_select(100) is None


@pytest.mark.integration
def test_request_do_insert(test_dao, test_configuration):
    """ request_do_insert() should return False on success. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    assert not DUT.request_do_insert(revision_id=1)


@pytest.mark.integration
def test_request_do_delete(test_dao, test_configuration):
    """ request_do_delete() should return False on success. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    assert not DUT.request_do_delete(2)


@pytest.mark.integration
def test_request_do_delete_non_existent_id(test_dao, test_configuration):
    """ request_do_delete() should return True when attempting to delete a non-existent Validation. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    assert DUT.request_do_delete(100)


@pytest.mark.integration
def test_request_do_update(test_dao, test_configuration):
    """ request_do_update() should return False on success. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    assert not DUT.request_do_update(1)


@pytest.mark.integration
def test_request_do_update_non_existent_id(test_dao, test_configuration):
    """ request_do_update() should return True when attempting to save a non-existent Validation. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    assert DUT.request_do_update(100)


@pytest.mark.integration
def test_request_do_update_all(test_dao, test_configuration):
    """ request_do_update_all() should return False on success. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    assert not DUT.request_do_update_all()


@pytest.mark.integration
def test_request_do_calculate(test_dao, test_configuration):
    """ request_do_calculate() should return False on success. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)
    _validation = DUT.request_do_select(1)
    _validation.cost_minimum = 252.00
    _validation.cost_average = 368.00
    _validation.cost_maximum = 441.00
    _validation.time_minimum = 25.2
    _validation.time_average = 36.8
    _validation.time_maximum = 44.1
    _validation.confidence = 0.95

    assert not DUT.request_do_calculate(1)
    assert _validation.time_mean == pytest.approx(36.08333333)
    assert _validation.time_variance == pytest.approx(9.9225)
    assert _validation.cost_mean == pytest.approx(360.83333333)
    assert _validation.cost_variance == pytest.approx(992.25)
