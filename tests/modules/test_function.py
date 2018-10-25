# -*- coding: utf-8 -*-
#
#       tests.modules.test_function.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test Class for Function data model and data controller."""

import pytest

from treelib import Tree
import pandas as pd

from ramstk.dao import DAO, RAMSTKFunction
from ramstk.modules.function import dtcFunction, dtmFunction
from ramstk.modules import RAMSTKDataMatrix

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Doyle "weibullguy" Rowland'

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
    DUT = dtmFunction(test_dao, test=True)

    assert isinstance(DUT, dtmFunction)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a Tree() object populated with RAMSTKFunction instances on success. """
    DUT = dtmFunction(test_dao, test=True)

    assert DUT.do_select_all(revision_id=1) is None
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.tree.get_node(1).data, RAMSTKFunction)


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RAMSTKFunction data model on success. """
    DUT = dtmFunction(test_dao, test=True)
    DUT.do_select_all(revision_id=1)
    _function = DUT.do_select(1)

    assert isinstance(_function, RAMSTKFunction)
    assert _function.function_id == 1
    assert _function.availability_logistics == 1.0


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent Function ID is requested. """
    DUT = dtmFunction(test_dao, test=True)
    _function = DUT.do_select(100)

    assert _function is None


@pytest.mark.integration
def test_do_insert_sibling(test_dao):
    """ do_insert() should return False on success when inserting a sibling Function. """
    DUT = dtmFunction(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_insert(revision_id=1, parent_id=0)

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program "
        "database.")
    assert DUT.last_id == 4

    DUT.do_delete(DUT.last_id)


@pytest.mark.integration
def test_do_insert_child(test_dao):
    """ do_insert() should return False on success when inserting a child Function. """
    DUT = dtmFunction(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_insert(revision_id=1, parent_id=1)

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program "
        "database.")
    assert DUT.last_id == 4

    DUT.do_delete(DUT.last_id)


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmFunction(test_dao, test=True)
    DUT.do_select_all(revision_id=1)
    DUT.do_insert(revision_id=1, parent_id=1)

    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Deleting an item from the RAMSTK Program "
                    "database.")


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a Function ID that doesn't exist. """
    DUT = dtmFunction(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code == 2005
    assert _msg == ("RAMSTK ERROR: Attempted to delete non-existent "
                    "Function ID 300.")


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmFunction(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _function = DUT.tree.get_node(1).data
    _function.availability_logistics = 0.9832

    _error_code, _msg = DUT.do_update(1)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating the RAMSTK Program " "database.")


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed a Function ID that doesn't exist. """
    DUT = dtmFunction(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2005
    assert _msg == ("RAMSTK ERROR: Attempted to save non-existent "
                    "Function ID 100.")


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmFunction(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating all records in the "
                    "function table.")


@pytest.mark.integration
def test_create_controller(test_dao, test_configuration):
    """ __init__() should return a Function Data Controller. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcFunction)
    assert isinstance(DUT._dtm_data_model, dtmFunction)
    assert isinstance(DUT._dmx_fctn_hw_matrix, RAMSTKDataMatrix)


@pytest.mark.integration
def test_request_do_select_all(test_dao, test_configuration):
    """ request_select_all() should return a Tree of RAMSTKFunction models. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)

    assert DUT.request_do_select_all(revision_id=1) is None
    assert isinstance(
        DUT._dtm_data_model.tree.get_node(1).data, RAMSTKFunction)


@pytest.mark.integration
def test_request_do_select_all_matrix(test_dao, test_configuration):
    """ request_do_select_all_matrix() should return a tuple containing the matrix, column headings, and row headings. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_do_select_all_matrix(
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
def test_request_do_select(test_dao, test_configuration):
    """ request_do_select() should return an RAMSTKFunction model. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    _function = DUT.request_do_select(1)

    assert isinstance(_function, RAMSTKFunction)


@pytest.mark.integration
def test_request_do_select_non_existent_id(test_dao, test_configuration):
    """ request_do_select() should return None when requesting a Function that doesn't exist. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    _function = DUT.request_do_select(100)

    assert _function is None


@pytest.mark.integration
def test_request_do_insert(test_dao, test_configuration):
    """ request_do_insert() should return False on success. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    assert not DUT.request_do_insert(revision_id=1, parent_id=0)

    DUT.request_do_delete(DUT.request_last_id())


@pytest.mark.integration
def test_request_do_insert_matrix_row(test_dao, test_configuration):
    """ request_do_insert_matrix() should return False on successfully inserting a row. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_do_select_all_matrix(
        1, 'fnctn_hrdwr')

    assert not DUT.request_do_insert_matrix('fnctn_hrdwr', 4, 'Function Code')
    assert DUT._dmx_fctn_hw_matrix.dic_row_hdrs[4] == 'Function Code'


@pytest.mark.integration
def test_request_do_insert_matrix_duplicate_row(test_dao, test_configuration):
    """ request_do_insert_matrix() should return True when attempting to insert a duplicate row. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_do_select_all_matrix(
        1, 'fnctn_hrdwr')

    assert DUT.request_do_insert_matrix('fnctn_hrdwr', 2, 'Function Code')


@pytest.mark.integration
def test_request_do_insert_matrix_column(test_dao, test_configuration):
    """ request_do_insert_matrix() should return False on successfully inserting a column. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_do_select_all_matrix(
        1, 'fnctn_hrdwr')

    assert not DUT.request_do_insert_matrix(
        'fnctn_hrdwr', 9, 'S1:SS1:A2', row=False)
    assert DUT._dmx_fctn_hw_matrix.dic_column_hdrs[9] == 'S1:SS1:A2'


@pytest.mark.integration
def test_request_do_delete(test_dao, test_configuration):
    """ request_do_delete() should return False on success. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)
    DUT.request_do_insert(revision_id=1, parent_id=0)

    assert not DUT.request_do_delete(DUT.request_last_id())


@pytest.mark.integration
def test_request_do_delete_non_existent_id(test_dao, test_configuration):
    """ request_do_delete() should return True when attempting to delete a non-existent Function. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    assert DUT.request_do_delete(100)


@pytest.mark.integration
def test_request_do_delete_matrix_row(test_dao, test_configuration):
    """ request_do_delete_matrix() should return False on successfully deleting a row. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_do_select_all_matrix(
        1, 'fnctn_hrdwr')
    DUT.request_do_insert_matrix('fnctn_hrdwr', 4, 'Function Code')

    assert not DUT.request_do_delete_matrix('fnctn_hrdwr', 4)


@pytest.mark.integration
def test_request_do_delete_matrix_non_existent_row(test_dao,
                                                   test_configuration):
    """ request_do_delete_matrix() should return True when attempting to delete a non-existent row. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_do_select_all_matrix(
        1, 'fnctn_hrdwr')

    assert DUT.request_do_delete_matrix('fnctn_hrdwr', 4)


@pytest.mark.integration
def test_request_do_delete_matrix_column(test_dao, test_configuration):
    """ request_do_delete_matrix() should return False on successfully deleting a column. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_do_select_all_matrix(
        1, 'fnctn_hrdwr')
    DUT.request_do_insert_matrix('fnctn_hrdwr', 4, 'S1:SS1:A1', row=False)

    assert not DUT.request_do_delete_matrix('fnctn_hrdwr', 4, row=False)


@pytest.mark.integration
def test_request_do_update(test_dao, test_configuration):
    """ request_do_update() should return False on success. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    assert not DUT.request_do_update(1)


@pytest.mark.integration
def test_request_do_update_non_existent_id(test_dao, test_configuration):
    """ request_do_update() should return True when attempting to save a non-existent Function. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    assert DUT.request_do_update(100)


@pytest.mark.integration
def test_request_do_update_matrix(test_dao, test_configuration):
    """ request_do_update_matrix() should return False on success. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_do_select_all_matrix(
        1, 'fnctn_hrdwr')

    assert not DUT.request_do_update_matrix(1, 'fnctn_hrdwr')


@pytest.mark.integration
def test_request_do_update_non_existent_matrix(test_dao, test_configuration):
    """ request_do_update_matrix() should return True when attempting to update a non-existent matrix. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_do_select_all_matrix(
        1, 'fnctn_hrdwr')

    assert DUT.request_do_update_matrix(1, 'fnctn_sftwr')


@pytest.mark.integration
def test_request_do_update_all(test_dao, test_configuration):
    """ request_do_update_all() should return False on success. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    assert not DUT.request_do_update_all()


@pytest.mark.integration
def test_request_get_attributes(test_dao, test_configuration):
    """ request_get_attributes() should return a dict of {attribute name:attribute value} pairs. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    _attributes = DUT.request_get_attributes(1)

    assert isinstance(_attributes, dict)
    assert _attributes['name'] == 'Function Name'


@pytest.mark.integration
def test_request_set_attributes(test_dao, test_configuration):
    """ request_set_attributes() should return a dict of {attribute name:attribute value} pairs. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    (_error_code, _msg) = DUT.request_set_attributes(1, 'availability_mission',
                                                     0.9978)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKFunction 1 attributes.")


@pytest.mark.integration
def test_request_last_id(test_dao, test_configuration):
    """ request_last_id() should return the last Function ID used in the RAMSTK Program database. """
    DUT = dtcFunction(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    _last_id = DUT.request_last_id()

    assert _last_id == 3
