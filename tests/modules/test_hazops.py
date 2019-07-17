# pylint: disable=protected-access
# -*- coding: utf-8 -*-
#
#       ramstk.tests.modules.test_hazard_analysis.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2018 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the HazardAnalysis class. """

# Third Party Imports
import pytest
from treelib import Tree

# RAMSTK Package Imports
from ramstk.dao import DAO
from ramstk.dao.programdb import RAMSTKHazardAnalysis
from ramstk.modules.hazops import dtcHazardAnalysis, dtmHazardAnalysis

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2018 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'revision_id': 1,
    'hardware_id': 1,
    'hazard_id': 1,
    'potential_hazard': '',
    'potential_cause': '',
    'assembly_effect': '',
    'assembly_severity': 'Major',
    'assembly_probability': 'Level A - Frequent',
    'assembly_hri': 20,
    'assembly_mitigation': b'',
    'assembly_severity_f': 'Major',
    'assembly_probability_f': 'Level A - Frequent',
    'assembly_hri_f': 20,
    'system_effect': '',
    'system_severity': 'Major',
    'system_probability': 'Level A - Frequent',
    'system_hri': 20,
    'system_mitigation': b'',
    'system_severity_f': 'Major',
    'system_probability_f': 'Level A - Frequent',
    'system_hri_f': 20,
    'remarks': b'',
    'function_1': '',
    'function_2': '',
    'function_3': '',
    'function_4': '',
    'function_5': '',
    'result_1': 0.0,
    'result_2': 0.0,
    'result_3': 0.0,
    'result_4': 0.0,
    'result_5': 0.0,
    'user_blob_1': b'',
    'user_blob_2': b'',
    'user_blob_3': b'',
    'user_float_1': 0.0,
    'user_float_2': 0.0,
    'user_float_3': 0.0,
    'user_int_1': 0,
    'user_int_2': 0,
    'user_int_3': 0,
}


@pytest.mark.integration
def test_create_hazard_analysis_data_model(test_dao):
    """ __init__ should return instance of HazardAnalysis data model. """
    DUT = dtmHazardAnalysis(test_dao, test=True)

    assert isinstance(DUT, dtmHazardAnalysis)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a treelib Tree() on success when selecting HazardAnalysiss. """
    DUT = dtmHazardAnalysis(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.tree.get_node('2.2').data, RAMSTKHazardAnalysis)


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RAMSTKHazardAnalysis data model on success. """
    DUT = dtmHazardAnalysis(test_dao, test=True)
    DUT.do_select_all(revision_id=1)
    _hazard_analysis = DUT.do_select('2.2')

    assert isinstance(_hazard_analysis, RAMSTKHazardAnalysis)
    assert _hazard_analysis.hardware_id == 2
    assert _hazard_analysis.hazard_id == 2
    assert _hazard_analysis.assembly_severity == 'Major'


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent HazardAnalysis ID is requested. """
    DUT = dtmHazardAnalysis(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _hazard_analysis = DUT.do_select('100')

    assert _hazard_analysis is None


@pytest.mark.integration
def test_do_select_children(test_dao):
    """ do_select_children() should return the immediate subtree of the passed node ID. """
    DUT = dtmHazardAnalysis(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _nodes = DUT.do_select_children(2)

    assert isinstance(_nodes, Tree)
    assert isinstance(_nodes['2.2'].data, RAMSTKHazardAnalysis)
    assert _nodes['2.2'].identifier == '2.2'


@pytest.mark.integration
def test_do_insert(test_dao):
    """ do_insert() should return a zero error code on success. """
    DUT = dtmHazardAnalysis(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_insert(revision_id=1, hardware_id=2)

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK "
        "Program database."
    )
    assert DUT.last_id == 8


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmHazardAnalysis(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_delete('2.2')

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Deleting an item from the RAMSTK Program "
        "database."
    )
    assert DUT.last_id == '7.7'


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a Revision ID that doesn't exist. """
    DUT = dtmHazardAnalysis(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code == 2005
    assert _msg == (
        "  RAMSTK ERROR: Attempted to delete non-existent Hazard "
        "Analysis ID 300."
    )


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmHazardAnalysis(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _hazard_analysis = DUT.do_select('3.3')
    _hazard_analysis.assembly_probability = 'Level D - Remote'

    _error_code, _msg = DUT.do_update('3.3')

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating the RAMSTK Program database.")


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed an HazardAnalysis ID that doesn't exist. """
    DUT = dtmHazardAnalysis(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2207
    assert _msg == (
        "RAMSTK ERROR: Attempted to save non-existent Hazard Analysis "
        "ID 100."
    )


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmHazardAnalysis(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update_all(hardware_id=3)

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Updating all records in the HazOps table "
        "for Hardware ID 3."
    )


@pytest.mark.integration
def test_do_calculate_hri(test_dao):
    """ do_calculate() should return False on success. """
    DUT = dtmHazardAnalysis(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _hazard_analysis = DUT.do_select('3.3')
    _hazard_analysis.assembly_severity = 'Medium'
    _hazard_analysis.assembly_probability = 'Level A - Frequent'
    _hazard_analysis.assembly_severity_f = 'Slight'
    _hazard_analysis.assembly_probability_f = 'Level C - Occasional'
    _hazard_analysis.system_severity = 'Medium'
    _hazard_analysis.system_probability = 'Level B - Reasonably Probable'
    _hazard_analysis.system_severity_f = 'Low'
    _hazard_analysis.system_probability_f = 'Level D - Remote'

    assert not DUT.do_calculate('3.3')
    assert _hazard_analysis.assembly_hri == 20
    assert _hazard_analysis.assembly_hri_f == 6
    assert _hazard_analysis.system_hri == 16
    assert _hazard_analysis.system_hri_f == 6


@pytest.mark.integration
def test_create_hazard_analysis_data_controller(test_dao, test_configuration):
    """ __init__() should return instance of HazardAnalysis data controller. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')

    assert isinstance(DUT, dtcHazardAnalysis)
    assert isinstance(DUT._dtm_data_model, dtmHazardAnalysis)


@pytest.mark.integration
def test_request_do_select_all(test_dao, test_configuration):
    """ request_do_select_all() should return a Tree of RAMSTKHazardAnalysis data models. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert isinstance(DUT._dtm_data_model.tree, Tree)
    assert isinstance(
        DUT._dtm_data_model.tree.get_node('3.3').data, RAMSTKHazardAnalysis,
    )


@pytest.mark.integration
def test_request_do_select(test_dao, test_configuration):
    """ request_do_select() should return an RAMSTKHazardAnalysis data model. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert isinstance(DUT.request_do_select('3.3'), RAMSTKHazardAnalysis)


@pytest.mark.integration
def test_request_do_select_non_existent_id(test_dao, test_configuration):
    """ request_do_select() should return None when requesting an HazardAnalysis that doesn't exist. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT.request_do_select(100) is None


@pytest.mark.integration
def test_request_do_insert(test_dao, test_configuration):
    """ request_do_insert() should return False on success. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_insert(revision_id=1, hardware_id=8)


@pytest.mark.integration
def test_request_do_delete(test_dao, test_configuration):
    """ request_do_delete() should return False on success. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_delete('3.3')


@pytest.mark.integration
def test_request_do_delete_non_existent_id(test_dao, test_configuration):
    """ request_do_delete() should return True when attempting to delete a non-existent HazardAnalysis. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT.request_do_delete(100)


@pytest.mark.integration
def test_request_do_update(test_dao, test_configuration):
    """ request_do_update() should return False on success. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_update(2)


@pytest.mark.integration
def test_request_do_update_non_existent_id(test_dao, test_configuration):
    """ request_do_update() should return True when attempting to save a non-existent HazardAnalysis. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT.request_do_update(100)


@pytest.mark.integration
def test_request_do_update_all(test_dao, test_configuration):
    """ request_do_update_all() should return False on success. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_update_all(hardware_id=2)


@pytest.mark.integration
def test_request_do_calculate(test_dao, test_configuration):
    """ request_do_calculate() should return False on success. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_calculate('4.4')
