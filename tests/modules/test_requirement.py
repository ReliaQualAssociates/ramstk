# pylint: disable=protected-access
# -*- coding: utf-8 -*-
#
#       tests.modules.test_requirement.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Requirement module algorithms and models. """

# Standard Library Imports
from datetime import date

# Third Party Imports
import pandas as pd
import pytest
from treelib import Tree

# RAMSTK Package Imports
from ramstk.dao import DAO, RAMSTKRequirement
from ramstk.modules import RAMSTKDataMatrix
from ramstk.modules.requirement import dtcRequirement, dtmRequirement

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'owner': '',
    'priority': 0,
    'parent_id': 0,
    'requirement_code': 'REL-0001',
    'q_complete_4': 0,
    'requirement_type': '',
    'q_complete_5': 0,
    'validated_date': date.today(),
    'revision_id': 1,
    'requirement_id': 1,
    'q_consistent_8': 0,
    'q_consistent_7': 0,
    'q_consistent_6': 0,
    'q_consistent_5': 0,
    'q_consistent_4': 0,
    'q_consistent_3': 0,
    'q_consistent_2': 0,
    'q_consistent_1': 0,
    'q_clarity_3': 0,
    'specification': '',
    'q_complete_0': 0,
    'q_complete_1': 0,
    'q_complete_2': 0,
    'q_complete_3': 0,
    'page_number': '',
    'figure_number': '',
    'q_complete_6': 0,
    'q_complete_7': 0,
    'q_complete_8': 0,
    'q_complete_9': 0,
    'q_consistent_0': 0,
    'q_clarity_6': 0,
    'q_clarity_7': 0,
    'q_clarity_4': 0,
    'q_clarity_5': 0,
    'q_clarity_2': 0,
    'description': 'REL-0001',
    'q_clarity_0': 0,
    'q_clarity_1': 0,
    'q_verifiable_4': 0,
    'derived': 0,
    'q_verifiable_0': 0,
    'q_verifiable_1': 0,
    'q_clarity_8': 0,
    'q_verifiable_3': 0,
    'q_verifiable_2': 0,
    'validated': 0,
    'q_verifiable_5': 0,
}


@pytest.mark.integration
def test_data_model_create(test_dao):
    """ __init__() should return a Requirement model. """
    DUT = dtmRequirement(test_dao, test=True)

    assert isinstance(DUT, dtmRequirement)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a Tree() object populated with RAMSTKRequirement instances on success. """
    DUT = dtmRequirement(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.tree.get_node(1).data, RAMSTKRequirement)


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RAMSTKRequirement data model on success. """
    DUT = dtmRequirement(test_dao, test=True)
    DUT.do_select_all(revision_id=1)
    _requirement = DUT.do_select(1)

    assert isinstance(_requirement, RAMSTKRequirement)
    assert _requirement.requirement_id == 1
    assert _requirement.requirement_code == 'REL-0001'


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent Requirement ID is requested. """
    DUT = dtmRequirement(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _requirement = DUT.do_select(100)

    assert _requirement is None


@pytest.mark.integration
def test_do_insert_sibling(test_dao):
    """ do_insert() should return False on success when inserting a sibling Requirement. """
    DUT = dtmRequirement(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_insert(revision_id=1, parent_id=0)

    assert _error_code == 0
    assert _msg == (
        'RAMSTK SUCCESS: Adding one or more items to the RAMSTK '
        'Program database.'
    )
    assert DUT.last_id == 2


@pytest.mark.integration
def test_do_insert_child(test_dao):
    """ do_insert() should return False on success when inserting a child (derived) Requirement. """
    DUT = dtmRequirement(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_insert(revision_id=1, parent_id=DUT.last_id)

    assert _error_code == 0
    assert _msg == (
        'RAMSTK SUCCESS: Adding one or more items to the RAMSTK '
        'Program database.'
    )
    assert DUT.last_id == 3


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmRequirement(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == (
        'RAMSTK SUCCESS: Deleting an item from the RAMSTK Program '
        'database.'
    )
    assert DUT.last_id == 2


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a Requirement ID that doesn't exist. """
    DUT = dtmRequirement(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_delete('300')

    assert _error_code == 2005
    assert _msg == (
        '  RAMSTK ERROR: Attempted to delete non-existent '
        'Requirement ID 300.'
    )


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmRequirement(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _requirement = DUT.do_select(1)
    _requirement.requirement_code = 'REL-0001'

    _error_code, _msg = DUT.do_update(1)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Updating the RAMSTK Program database.')


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed a Requirement ID that doesn't exist. """
    DUT = dtmRequirement(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update('100')

    assert _error_code == 2005
    assert _msg == (
        'RAMSTK ERROR: Attempted to save non-existent Requirement '
        'ID 100.'
    )


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmRequirement(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Updating all records in the requirement "
        "table."
    )


@pytest.mark.integration
def test_data_controller_create(test_dao, test_configuration):
    """ __init__ should return a Requirement Data Controller. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcRequirement)
    assert isinstance(DUT._dtm_data_model, dtmRequirement)
    assert isinstance(DUT._dmx_rqmt_hw_matrix, RAMSTKDataMatrix)
    assert isinstance(DUT._dmx_rqmt_sw_matrix, RAMSTKDataMatrix)
    assert isinstance(DUT._dmx_rqmt_val_matrix, RAMSTKDataMatrix)


@pytest.mark.integration
def test_request_do_select_all(test_dao, test_configuration):
    """ request_do_select_all() should return a Tree of RAMSTKRequirement models. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)

    _tree = DUT.request_do_select_all(ATTRIBUTES)

    assert isinstance(
        DUT._dtm_data_model.tree.get_node(1).data, RAMSTKRequirement,
    )


@pytest.mark.integration
def test_request_do_select_all_matrix(test_dao, test_configuration):
    """ _request_do_select_all_matrix() should return a tuple containing the matrix, column headings, and row headings. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)

    (_matrix, _column_hdrs, _row_hdrs) = DUT._request_do_select_all_matrix(
        1, 'rqrmnt_hrdwr',
    )

    assert isinstance(_matrix, pd.DataFrame)
    assert _column_hdrs == {
        1: 'S1',
        2: 'S1:SS1',
        3: 'S1:SS2',
        4: 'S1:SS3',
        5: 'S1:SS4',
        6: 'S1:SS1:A1',
        7: 'S1:SS1:A2',
        8: 'S1:SS1:A3',
    }
    assert _row_hdrs == {1: 'REL-0001', 2: ''}


@pytest.mark.integration
def test_request_do_select(test_dao, test_configuration):
    """ request_do_select() should return an RAMSTKRequirement model. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    _requirement = DUT.request_do_select(1)

    assert isinstance(_requirement, RAMSTKRequirement)


@pytest.mark.integration
def test_request_do_select_non_existent_id(test_dao, test_configuration):
    """ request_do_select() should return None when requesting a Requirement that doesn't exist. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)

    assert DUT.request_do_select(100) is None


@pytest.mark.integration
def test_request_do_create_matrix(test_dao, test_configuration):
    """ request_do_create_matrix should return None. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT._request_do_create_matrix(1, 'rqrmnt_hrdwr') is None
    assert DUT._request_do_create_matrix(1, 'rqrmnt_vldtn') is None


@pytest.mark.integration
def test_request_do_insert(test_dao, test_configuration):
    """ request_do_insert() should return False on success. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_insert(revision_id=1, parent_id=0)


@pytest.mark.integration
def test_request_do_insert_matrix_row(test_dao, test_configuration):
    """ _request_do_insert_matrix() should return False on successfully inserting a row. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT._request_do_select_all_matrix(
        1, 'rqrmnt_hrdwr',
    )

    assert not DUT.request_do_insert_matrix('rqrmnt_hrdwr', 4, 'COST-0001')
    assert DUT._dmx_rqmt_hw_matrix.dic_row_hdrs[4] == 'COST-0001'


@pytest.mark.integration
def test_request_do_insert_matrix_duplicate_row(test_dao, test_configuration):
    """ _request_do_insert_matrix() should return True when attempting to insert a duplicate row. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT._request_do_select_all_matrix(
        1, 'rqrmnt_hrdwr',
    )

    assert DUT.request_do_insert_matrix('rqrmnt_hrdwr', 1, 'COST-0001')


@pytest.mark.integration
def test_request_do_insert_non_existent_matrix(test_dao, test_configuration):
    """ _request_do_insert_matrix() should return True when attempting to insert to a non-existent matrix. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT._request_do_select_all_matrix(
        1, 'rqrmnt_hrdwr',
    )

    assert DUT.request_do_insert_matrix('rqrmnt_rvsn', 4, 'COST-0001')


@pytest.mark.integration
def test_request_do_insert_matrix_column(test_dao, test_configuration):
    """ _request_do_insert_matrix() should return False on successfully inserting a column. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT._request_do_select_all_matrix(
        1, 'rqrmnt_hrdwr',
    )

    assert not DUT.request_do_insert_matrix(
        'rqrmnt_hrdwr', 9, 'S1:SS1:A11', row=False,
    )
    assert DUT._dmx_rqmt_hw_matrix.dic_column_hdrs[9] == 'S1:SS1:A11'


@pytest.mark.integration
def test_request_do_delete(test_dao, test_configuration):
    """ request_do_delete() should return False on success. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)
    DUT.request_do_insert(revision_id=1, parent_id=0)

    assert not DUT.request_do_delete(DUT.request_last_id())


@pytest.mark.integration
def test_request_do_delete_non_existent_id(test_dao, test_configuration):
    """ request_do_delete() should return True when attempting to delete a non-existent Requirement. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT.request_do_delete('100')


@pytest.mark.integration
def test_request_do_delete_matrix_row(test_dao, test_configuration):
    """ _request_do_delete_matrix() should return False on successfully deleting a row. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    DUT._request_do_select_all_matrix(1, 'rqrmnt_hrdwr')
    DUT.request_do_insert_matrix('rqrmnt_hrdwr', 4, 'COST-0001')

    assert not DUT._request_do_delete_matrix('rqrmnt_hrdwr', 4)


@pytest.mark.integration
def test_request_do_delete_nonexistent_matrix(test_dao, test_configuration):
    """ _request_do_delete_matrix() should return True when attempting to deletie from a non-existent matrix. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    DUT._request_do_select_all_matrix(1, 'rqrmnt_hrdwr')
    DUT.request_do_insert_matrix('rqrmnt_hrdwr', 4, 'COST-0001')

    assert DUT._request_do_delete_matrix('rqrmnt_rvsn', 4)

@pytest.mark.integration
def test_request_do_delete_matrix_non_existent_row(
        test_dao,
        test_configuration,
):
    """ _request_do_delete_matrix() should return True when attempting to delete a non-existent row. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    DUT._request_do_select_all_matrix(1, 'rqrmnt_hrdwr')

    assert DUT._request_do_delete_matrix('rqrmnt_hrdwr', 4)


@pytest.mark.integration
def test_request_do_delete_matrix_column(test_dao, test_configuration):
    """ _request_do_delete_matrix() should return False on successfully deleting a column. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    DUT._request_do_select_all_matrix(1, 'rqrmnt_hrdwr')
    DUT.request_do_insert_matrix('rqrmnt_hrdwr', 4, 'S1:SS1:A1', row=False)

    assert not DUT._request_do_delete_matrix('rqrmnt_hrdwr', 4, row=False)


@pytest.mark.integration
def test_request_do_update(test_dao, test_configuration):
    """ request_do_update() should return False on success. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_update(1)


@pytest.mark.integration
def test_request_do_update_non_existent_id(test_dao, test_configuration):
    """ request_do_update() should return True when attempting to save a non-existent Requirement. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT.request_do_update(100)


@pytest.mark.integration
def test_request_do_update_matrix(test_dao, test_configuration):
    """ _request_do_update_matrix() should return False on success. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    DUT._request_do_select_all_matrix(1, 'rqrmnt_hrdwr')

    assert not DUT._request_do_update_matrix(1, 'rqrmnt_hrdwr')


@pytest.mark.integration
def test_request_do_update_non_existent_matrix(test_dao, test_configuration):
    """ _request_do_update_matrix() should return True when attempting to update a non-existent matrix. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    DUT._request_do_select_all_matrix(1, 'rqrmnt_hrdwr')

    assert DUT._request_do_update_matrix(1, 'rqrmnt_rqrmnt')


@pytest.mark.integration
def test_request_do_update_all(test_dao, test_configuration):
    """ request_do_update_all() should return False on success. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_update_all()


@pytest.mark.integration
def test_request_get_attributes(test_dao, test_configuration):
    """ request_get_attributes() should return a dict of {attribute name:attribute value} pairs. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    _attributes = DUT.request_get_attributes(1)

    assert isinstance(_attributes, dict)
    assert _attributes['requirement_code'] == 'REL-0001'


@pytest.mark.integration
def test_request_set_attributes(test_dao, test_configuration):
    """ request_set_attributes() should return a zero error code on success. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    _error_code, _msg = DUT.request_set_attributes(1, 'requirement_code', 1)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Updating RAMSTKRequirement 1 attributes.')


@pytest.mark.integration
def test_request_last_id(test_dao, test_configuration):
    """ request_last_id() should return the last Requirement ID used in the RAMSTK Program database. """
    DUT = dtcRequirement(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT.request_last_id() == 3
