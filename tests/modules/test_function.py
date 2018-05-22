# -*- coding: utf-8 -*-
#
#       tests.modules.test_function.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test Class for Function data model and data controller."""

import pytest

from treelib import Tree
import pandas as pd

from rtk.dao import DAO, RTKFunction
from rtk.modules.function import dtcFunction, dtmFunction
from rtk.datamodels import RTKDataMatrix

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'type_id': 0,
    'total_part_count': 0,
    'availability_mission': 1.0,
    'cost': 0.0,
    'hazard_rate_mission': 0.0,
    'mpmt': 0.0,
    'parent_id': 0,
    'mtbf_logistics': 0.0,
    'safety_critical': 0,
    'mmt': 0.0,
    'hazard_rate_logistics': 0.0,
    'remarks': '',
    'mtbf_mission': 0.0,
    'function_code': 'PRESS-001',
    'name': u'Function Name',
    'level': 0,
    'mttr': 0.0,
    'mcmt': 0.0,
    'function_id': 1,
    'availability_logistics': 1.0,
    'total_mode_count': 0
}


@pytest.mark.integration
def test_create_data_model(test_dao):
    """ __init__() should return a Function model. """
    DUT = dtmFunction(test_dao)

    assert isinstance(DUT, dtmFunction)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_select_all(test_dao):
    """ select_all() should return a Tree() object populated with RTKFunction instances on success. """
    DUT = dtmFunction(test_dao)
    _tree = DUT.select_all(1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RTKFunction)


@pytest.mark.integration
def test_select(test_dao):
    """ select() should return an instance of the RTKFunction data model on success. """
    DUT = dtmFunction(test_dao)
    DUT.select_all(1)
    _function = DUT.select(1)

    assert isinstance(_function, RTKFunction)
    assert _function.function_id == 1
    assert _function.availability_logistics == 1.0


@pytest.mark.integration
def test_select_non_existent_id(test_dao):
    """ select() should return None when a non-existent Function ID is requested. """
    DUT = dtmFunction(test_dao)
    _function = DUT.select(100)

    assert _function is None


@pytest.mark.integration
def test_insert_sibling(test_dao):
    """ insert() should return False on success when inserting a sibling Function. """
    DUT = dtmFunction(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(revision_id=1, parent_id=0)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")
    assert DUT.last_id == 4

    DUT.delete(DUT.last_id)


@pytest.mark.integration
def test_insert_child(test_dao):
    """ insert() should return False on success when inserting a child Function. """
    DUT = dtmFunction(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(revision_id=1, parent_id=1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")
    assert DUT.last_id == 4

    DUT.delete(DUT.last_id)


@pytest.mark.integration
def test_delete(test_dao):
    """ delete() should return a zero error code on success. """
    DUT = dtmFunction(test_dao)
    DUT.select_all(1)
    DUT.insert(revision_id=1, parent_id=1)

    _error_code, _msg = DUT.delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Deleting an item from the RTK Program "
                    "database.")


@pytest.mark.integration
def test_delete_non_existent_id(test_dao):
    """ delete() should return a non-zero error code when passed a Function ID that doesn't exist. """
    DUT = dtmFunction(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(300)

    assert _error_code == 2005
    assert _msg == ("  RTK ERROR: Attempted to delete non-existent Function "
                    "ID 300.")


@pytest.mark.integration
def test_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmFunction(test_dao)
    DUT.select_all(1)

    _function = DUT.tree.get_node(1).data
    _function.availability_logistics = 0.9832

    _error_code, _msg = DUT.update(1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
def test_update_non_existent_id(test_dao):
    """ update() should return a non-zero error code when passed a Function ID that doesn't exist. """
    DUT = dtmFunction(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2006
    assert _msg == ("RTK ERROR: Attempted to save non-existent Function ID "
                    "100.")


@pytest.mark.integration
def test_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmFunction(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
def test_calculate_mtbf(test_dao):
    """ calculate_mtbf() should return a zero error code on success. """
    DUT = dtmFunction(test_dao)
    DUT.select_all(1)

    _function = DUT.select(1)
    _function.hazard_rate_logistics = 0.00000151
    _function.hazard_rate_mission = 0.000002

    _error_code, _msg = DUT.calculate_mtbf(1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Calculating MTBF metrics for Function ID 1.")
    assert _function.mtbf_logistics == pytest.approx(662251.6556291)
    assert _function.mtbf_mission == pytest.approx(500000.0)


@pytest.mark.integration
def test_calculate_mtbf_divide_by_zero(test_dao):
    """ calculate_mtbf() should return a non-zero error code when attempting to divide by zero. """
    DUT = dtmFunction(test_dao)
    DUT.select_all(1)

    _function = DUT.select(1)
    _function.hazard_rate_mission = 0.0

    _error_code, _msg = DUT.calculate_mtbf(1)

    assert _error_code == 102
    assert _msg == ("RTK ERROR: Zero Division Error when calculating the "
                    "mission MTBF for Function ID 1.  Mission hazard rate: "
                    "0.000000.")


@pytest.mark.integration
def test_calculate_availability(test_dao):
    """ calculate_availability() should return False on success. """
    DUT = dtmFunction(test_dao)
    DUT.select_all(1)

    _function = DUT.tree.get_node(1).data
    _function.mpmt = 0.5
    _function.mcmt = 1.2
    _function.mttr = 5.8
    _function.mmt = 0.85
    _function.mtbf_logistics = 662251.6556291
    _function.mtbf_mission = 500000.0

    _error_code, _msg = DUT.calculate_availability(1)
    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Calculating availability metrics for "
                    "Function ID 1.")
    assert _function.availability_logistics == pytest.approx(0.9999912)
    assert _function.availability_mission == pytest.approx(0.9999884)


@pytest.mark.integration
def test_calculate_availability_divide_by_zero(test_dao):
    """ calculate_availability() should return True when attempting to divide by zero. """
    DUT = dtmFunction(test_dao)
    DUT.select_all(1)

    _function = DUT.tree.get_node(1).data
    _function.mttr = 0.0
    _function.mtbf_logistics = 662251.6556291
    _function.mtbf_mission = 0.0

    _error_code, _msg = DUT.calculate_availability(1)
    assert _error_code == 102
    assert _msg == ("RTK ERROR: Zero Division Error when calculating the "
                    "mission availability for Function ID 1.  Mission MTBF: "
                    "0.000000 MTTR: 0.000000.")


@pytest.mark.integration
def test_create_controller(test_dao, test_configuration):
    """ __init__() should return a Function Data Controller. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcFunction)
    assert isinstance(DUT._dtm_data_model, dtmFunction)
    assert isinstance(DUT._dmx_fctn_hw_matrix, RTKDataMatrix)


@pytest.mark.integration
def test_request_select_all(test_dao, test_configuration):
    """ request_select_all() should return a Tree of RTKFunction models. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    _tree = DUT.request_select_all(1)

    assert isinstance(_tree.get_node(1).data, RTKFunction)


@pytest.mark.integration
def test_request_select_all_matrix(test_dao, test_configuration):
    """ request_select_all_matrix() should return a tuple containing the matrix, column headings, and row headings. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_select_all_matrix(
        1, 'fnctn_hrdwr')

    assert isinstance(_matrix, pd.DataFrame)
    assert _column_hdrs == {
        1: u'S1',
        2: u'S1:SS1',
        4: u'S1:SS3',
        3: u'S1:SS2',
        5: u'S1:SS4',
        6: u'S1:SS1:A1',
        7: u'S1:SS1:A2',
        8: u'S1:SS1:A3'
    }
    assert _row_hdrs == {1: u'FUNC-0001', 2: u'FUNC-0002', 3: u'FUNC-0003'}


@pytest.mark.integration
def test_request_select(test_dao, test_configuration):
    """ request_select() should return an RTKFunction model. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _function = DUT.request_select(1)

    assert isinstance(_function, RTKFunction)


@pytest.mark.integration
def test_request_select_non_existent_id(test_dao, test_configuration):
    """ request_select() should return None when requesting a Function that doesn't exist. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    _function = DUT.request_select(100)

    assert _function is None


@pytest.mark.integration
def test_request_insert(test_dao, test_configuration):
    """ request_insert() should return False on success. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_insert(revision_id=1, parent_id=0)

    DUT.request_delete(DUT.request_last_id())


@pytest.mark.integration
def test_insert_matrix_row(test_dao, test_configuration):
    """ request_insert_matrix() should return False on successfully inserting a row. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_select_all_matrix(
        1, 'fnctn_hrdwr')

    assert not DUT.request_insert_matrix('fnctn_hrdwr', 4, 'Function Code')
    assert DUT._dmx_fctn_hw_matrix.dic_row_hdrs[4] == 'Function Code'


@pytest.mark.integration
def test_insert_matrix_duplicate_row(test_dao, test_configuration):
    """ request_insert_matrix() should return True when attempting to insert a duplicate row. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_select_all_matrix(
        1, 'fnctn_hrdwr')

    assert DUT.request_insert_matrix('fnctn_hrdwr', 2, 'Function Code')


@pytest.mark.integration
def test_insert_matrix_column(test_dao, test_configuration):
    """ request_insert_matrix() should return False on successfully inserting a column. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_select_all_matrix(
        1, 'fnctn_hrdwr')

    assert not DUT.request_insert_matrix(
        'fnctn_hrdwr', 9, 'S1:SS1:A2', row=False)
    assert DUT._dmx_fctn_hw_matrix.dic_column_hdrs[9] == 'S1:SS1:A2'


@pytest.mark.integration
def test_request_delete(test_dao, test_configuration):
    """ request_delete() should return False on success. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)
    DUT.request_insert(revision_id=1, parent_id=0)

    assert not DUT.request_delete(DUT.request_last_id())


@pytest.mark.integration
def test_request_delete_non_existent_id(test_dao, test_configuration):
    """ request_delete() should return True when attempting to delete a non-existent Function. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert DUT.request_delete(100)


@pytest.mark.integration
def test_request_delete_matrix_row(test_dao, test_configuration):
    """ request_delete_matrix() should return False on successfully deleting a row. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_select_all_matrix(
        1, 'fnctn_hrdwr')
    DUT.request_insert_matrix('fnctn_hrdwr', 4, 'Function Code')

    assert not DUT.request_delete_matrix('fnctn_hrdwr', 4)


@pytest.mark.integration
def test_request_delete_matrix_non_existent_row(test_dao, test_configuration):
    """ request_delete_matrix() should return True when attempting to delete a non-existent row. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_select_all_matrix(
        1, 'fnctn_hrdwr')

    assert DUT.request_delete_matrix('fnctn_hrdwr', 4)


@pytest.mark.integration
def test_request_delete_matrix_column(test_dao, test_configuration):
    """ request_delete_matrix() should return False on successfully deleting a column. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_select_all_matrix(
        1, 'fnctn_hrdwr')
    DUT.request_insert_matrix('fnctn_hrdwr', 4, 'S1:SS1:A1', row=False)

    assert not DUT.request_delete_matrix('fnctn_hrdwr', 4, row=False)


@pytest.mark.integration
def test_request_update(test_dao, test_configuration):
    """ request_update() should return False on success. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_update(1)


@pytest.mark.integration
def test_request_update_non_existent_id(test_dao, test_configuration):
    """ request_update() should return True when attempting to save a non-existent Function. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert DUT.request_update(100)


@pytest.mark.integration
def test_request_update_matrix(test_dao, test_configuration):
    """ request_update_matrix() should return False on success. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_select_all_matrix(
        1, 'fnctn_hrdwr')

    assert not DUT.request_update_matrix(1, 'fnctn_hrdwr')


@pytest.mark.integration
def test_request_update_non_existent_matrix(test_dao, test_configuration):
    """ request_update_matrix() should return True when attempting to update a non-existent matrix. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_select_all_matrix(
        1, 'fnctn_hrdwr')

    assert DUT.request_update_matrix(1, 'fnctn_sftwr')


@pytest.mark.integration
def test_request_update_all(test_dao, test_configuration):
    """ request_update_all() should return False on success. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_update_all()


@pytest.mark.integration
def test_request_calculate_mtbf(test_dao, test_configuration):
    """ request_calculate_mtbf() should return False on success. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _function = DUT.request_select(1)
    _function.hazard_rate_logistics = 0.00000151
    _function.hazard_rate_mission = 0.0000000152

    assert not DUT.request_calculate_mtbf(1)

    assert _function.mtbf_logistics == pytest.approx(662251.6556291)
    assert _function.mtbf_mission == pytest.approx(65789473.6842105)


@pytest.mark.integration
def test_request_calculate_availability(test_dao, test_configuration):
    """ request_calculate_availability() should return False on success. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _function = DUT.request_select(1)
    _function.mpmt = 0.5
    _function.mcmt = 1.2
    _function.mttr = 5.8
    _function.mmt = 0.85
    _function.mtbf_logistics = 547885.1632698
    _function.mtbf_mission = 500000.0

    assert not DUT.request_calculate_availability(1)
    assert _function.availability_logistics == pytest.approx(0.9999894)
    assert _function.availability_mission == pytest.approx(0.9999884)


@pytest.mark.integration
def test_request_get_attributes(test_dao, test_configuration):
    """ request_get_attributes() should return a dict of {attribute name:attribute value} pairs. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _attributes = DUT.request_get_attributes(1)

    assert isinstance(_attributes, dict)
    assert _attributes['name'] == 'Function Name'


@pytest.mark.integration
def test_request_set_attributes(test_dao, test_configuration):
    """ request_set_attributes() should return a dict of {attribute name:attribute value} pairs. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _error_code, _msg = DUT.request_set_attributes(1, ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKFunction 1 attributes.")


@pytest.mark.integration
def test_request_last_id(test_dao, test_configuration):
    """ request_last_id() should return the last Function ID used in the RTK Program database. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _last_id = DUT.request_last_id()

    assert _last_id == 3
