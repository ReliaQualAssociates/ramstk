#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.modules.test_hazard_analysis.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2018 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the HazardAnalysis class."""

import pytest

from treelib import Tree

from rtk.dao import DAO
from rtk.dao import RTKHazardAnalysis
from rtk.analyses.hazard import dtmHazardAnalysis, dtcHazardAnalysis

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2018 Andrew "Weibullguy" Rowland'


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_create_hazard_analysis_data_model(test_dao):
    """ __init__ should return instance of HazardAnalysis data model. """
    DUT = dtmHazardAnalysis(test_dao)

    assert isinstance(DUT, dtmHazardAnalysis)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_select_all(test_dao):
    """select_all() should return a treelib Tree() on success when selecting HazardAnalysiss."""
    DUT = dtmHazardAnalysis(test_dao)
    _tree = DUT.select_all(1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node('2.2').data, RTKHazardAnalysis)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_select(test_dao):
    """select() should return an instance of the RTKHazardAnalysis data model on success."""
    DUT = dtmHazardAnalysis(test_dao)
    DUT.select_all(1)

    _hazard_analysis = DUT.select('2.2')

    assert isinstance(_hazard_analysis, RTKHazardAnalysis)
    assert _hazard_analysis.hardware_id == 2
    assert _hazard_analysis.hazard_id == 2
    assert _hazard_analysis.assembly_severity_id == 4


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_select_non_existent_id(test_dao):
    """select() should return None when a non-existent HazardAnalysis ID is requested."""
    DUT = dtmHazardAnalysis(test_dao)
    DUT.select_all(1)

    _hazard_analysis = DUT.select('100')

    assert _hazard_analysis is None


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_select_children(test_dao):
    """select_children() should return the immediate subtree of the passed node ID."""
    DUT = dtmHazardAnalysis(test_dao)
    DUT.select_all(1)

    _nodes = DUT.select_children(2)

    assert isinstance(_nodes, list)
    assert isinstance(_nodes[0].data, RTKHazardAnalysis)
    assert _nodes[0].identifier == '2.2'


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_insert(test_dao):
    """insert() should return a zero error code on success."""
    DUT = dtmHazardAnalysis(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(revision_id=1, hardware_id=2)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK "
                    "Program database.")
    assert DUT.last_id == 8


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_delete(test_dao):
    """delete() should return a zero error code on success."""
    DUT = dtmHazardAnalysis(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete('2.2')

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Deleting an item from the RTK Program "
                    "database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_delete_non_existent_id(test_dao):
    """delete() should return a non-zero error code when passed a Revision ID that doesn't exist."""
    DUT = dtmHazardAnalysis(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(300)

    assert _error_code == 2005
    assert _msg == ("  RTK ERROR: Attempted to delete non-existent Hazard "
                    "Analysis ID 300.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_update(test_dao):
    """update() should return a zero error code on success."""
    DUT = dtmHazardAnalysis(test_dao)
    DUT.select_all(1)

    _hazard_analysis = DUT.select('3.3')
    _hazard_analysis.assembly_probability_id = 2

    _error_code, _msg = DUT.update('3.3')

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_update_non_existent_id(test_dao):
    """update() should return a non-zero error code when passed an HazardAnalysis ID that doesn't exist."""
    DUT = dtmHazardAnalysis(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2207
    assert _msg == ("RTK ERROR: Attempted to save non-existent Hazard Analysis "
                    "ID 100.")

@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_update_all(test_dao):
    """update_all() should return a zero error code on success."""
    DUT = dtmHazardAnalysis(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_calculate_hri(test_dao):
    """calculate() should return False on success."""
    DUT = dtmHazardAnalysis(test_dao)
    DUT.select_all(1)

    _hazard_analysis = DUT.select('3.3')
    _hazard_analysis.assembly_severity_id = 4
    _hazard_analysis.assembly_probability_id = 5
    _hazard_analysis.assembly_severity_id_f = 2
    _hazard_analysis.assembly_probability_id_f = 3
    _hazard_analysis.system_severity_id = 4
    _hazard_analysis.system_probability_id = 4
    _hazard_analysis.system_severity_id_f = 3
    _hazard_analysis.system_probability_id_f = 2

    assert not DUT.calculate('3.3')
    assert _hazard_analysis.assembly_hri == 20
    assert _hazard_analysis.assembly_hri_f == 6
    assert _hazard_analysis.system_hri == 16
    assert _hazard_analysis.system_hri_f == 6


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_create_hazard_analysis_data_controller(test_dao, test_configuration):
    """ __init__ should return instance of HazardAnalysis data controller. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')

    assert isinstance(DUT, dtcHazardAnalysis)
    assert isinstance(DUT._dtm_data_model, dtmHazardAnalysis)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_request_select_all(test_dao, test_configuration):
    """ request_select_all() should return a Tree of RTKHazardAnalysis data models. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')

    _tree = DUT.request_select_all(1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node('3.3').data, RTKHazardAnalysis)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_request_select(test_dao, test_configuration):
    """ request_select() should return an RTKHazardAnalysis data model. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    assert isinstance(DUT.request_select('3.3'), RTKHazardAnalysis)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_request_non_existent_id(test_dao, test_configuration):
    """ request_select() should return None when requesting an HazardAnalysis that doesn't exist. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    assert DUT.request_select(100) is None


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_request_insert(test_dao, test_configuration):
    """ request_insert() should return False on success. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    assert not DUT.request_insert(revision_id=1, hardware_id=8)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_request_delete(test_dao, test_configuration):
    """ request_delete() should return False on success. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    assert not DUT.request_delete('3.3')


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_request_delete_non_existent_id(test_dao, test_configuration):
    """ request_delete() should return True when attempting to delete a non-existent HazardAnalysis. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    assert DUT.request_delete(100)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_request_update(test_dao, test_configuration):
    """ request_update() should return False on success. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    assert not DUT.request_update(2)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_request_update_non_existent_id(test_dao, test_configuration):
    """ request_update() should return True when attempting to save a non-existent HazardAnalysis. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    assert DUT.request_update(100)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_request_update_all(test_dao, test_configuration):
    """ request_update_all() should return False on success. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    assert not DUT.request_update_all()


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.hazard_analysis
def test_request_calculate(test_dao, test_configuration):
    """ request_calculate() should return False on success. """
    DUT = dtcHazardAnalysis(test_dao, test_configuration, test='True')
    DUT.request_select_all(1)

    assert not DUT.request_calculate('4.4')

