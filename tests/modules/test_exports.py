# -*- coding: utf-8 -*-
#
#       ramstk.tests.modules.test_exports.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2018 Doyle "weibullguy" Rowland
"""Test class for testing the Exports class."""
#pylint: disable=protected-access

from collections import OrderedDict
import pandas as pd

import pytest

from ramstk.dao import DAO
from ramstk.modules.exports import dtmExports, dtcExports
from ramstk.modules.function import dtmFunction
from ramstk.modules.requirement import dtmRequirement
from ramstk.modules.hardware import dtmHardwareBoM, dtmDesignElectric, dtmReliability
from ramstk.modules.validation import dtmValidation

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2018 Doyle "weibullguy" Rowland'


@pytest.mark.integration
def test_create_export_data_model(test_dao):
    """__init__() should return an instance of the Export data model."""
    DUT = dtmExports(test_dao)

    assert isinstance(DUT, dtmExports)
    assert isinstance(DUT.dao, DAO)
    assert DUT._dic_column_headers['Function'] == [
        'revision_id', 'function_id', 'level', 'function_code', 'name',
        'parent_id', 'remarks', 'safety_critical', 'type_id'
    ]
    assert DUT._dic_column_headers['Requirement'] == [
        'revision_id', 'requirement_id', 'derived', 'description',
        'figure_number', 'owner', 'page_number', 'parent_id', 'priority',
        'requirement_code', 'specification', 'requirement_type', 'validated',
        'validated_date'
    ]
    assert DUT._dic_column_headers['Hardware'] == [
        'revision_id', 'hardware_id', 'alt_part_num', 'cage_code',
        'category_id', 'comp_ref_des', 'cost', 'cost_type_id', 'description',
        'duty_cycle', 'figure_number', 'lcn', 'level', 'manufacturer_id',
        'mission_time', 'name', 'nsn', 'page_number', 'parent_id', 'part',
        'part_number', 'quantity', 'ref_des', 'remarks', 'repairable',
        'specification_number', 'subcategory_id', 'tagged_part',
        'year_of_manufacture'
    ]
    assert DUT._dic_column_headers['Design Electric'] == [
        'hardware_id', 'application_id', 'area', 'capacitance',
        'configuration_id', 'construction_id', 'contact_form_id',
        'contact_gauge', 'contact_rating_id', 'current_operating',
        'current_rated', 'current_ratio', 'environment_active_id',
        'environment_dormant_id', 'family_id', 'feature_size',
        'frequency_operating', 'insert_id', 'insulation_id',
        'manufacturing_id', 'matching_id', 'n_active_pins', 'n_circuit_planes',
        'n_cycles', 'n_elements', 'n_hand_soldered', 'n_wave_soldered',
        'operating_life', 'overstress', 'package_id', 'power_operating',
        'power_rated', 'power_ratio', 'reason', 'resistance',
        'specification_id', 'technology_id', 'temperature_active',
        'temperature_case', 'temperature_dormant', 'temperature_hot_spot',
        'temperature_junction', 'temperature_knee', 'temperature_rated_max',
        'temperature_rated_min', 'temperature_rise', 'theta_jc', 'type_id',
        'voltage_ac_operating', 'voltage_dc_operating', 'voltage_esd',
        'voltage_rated', 'voltage_ratio', 'weight', 'years_in_production'
    ]
    assert DUT._dic_column_headers['Reliability'] == [
        'hardware_id', 'add_adj_factor', 'failure_distribution_id',
        'hazard_rate_method_id', 'hazard_rate_model', 'hazard_rate_specified',
        'hazard_rate_type_id', 'location_parameter', 'mtbf_specified',
        'mult_adj_factor', 'quality_id', 'reliability_goal',
        'reliability_goal_measure_id', 'scale_parameter', 'shape_parameter',
        'survival_analysis_id'
    ]
    assert DUT._dic_column_headers['Validation'] == [
        'revision_id', 'validation_id', 'acceptable_maximum',
        'acceptable_mean', 'acceptable_minimum', 'acceptable_variance',
        'confidence', 'cost_average', 'cost_maximum', 'cost_minimum',
        'date_start', 'date_end', 'description', 'measurement_unit', 'name',
        'status', 'task_type', 'task_specification', 'time_average',
        'time_maximum', 'time_minimum'
    ]
    assert DUT._output_data is None


@pytest.mark.integration
def test_do_load_output_function(test_dao):
    """do_load_output() should return None when loading Functions for export."""
    DUT = dtmExports(test_dao)

    _function = dtmFunction(test_dao, test=True)
    _function.do_select_all(revision_id=1)

    assert DUT.do_load_output('Function', _function.tree) is None


@pytest.mark.integration
def test_do_load_output_requirement(test_dao):
    """do_load_output() should return None when loading Requirements for export."""
    DUT = dtmExports(test_dao)

    _requirement = dtmRequirement(test_dao)
    _tree = _requirement.do_select_all(revision_id=1)

    assert DUT.do_load_output('Requirement', _tree) is None


@pytest.mark.integration
def test_do_load_output_hardware(test_dao):
    """do_load_output() should return None when loading Hardware for export."""
    DUT = dtmExports(test_dao)

    _hardware = dtmHardwareBoM(test_dao)
    _tree = _hardware.do_select_all(revision_id=1)

    assert DUT.do_load_output('Hardware', _tree) is None


@pytest.mark.integration
def test_do_load_output_design_electric(test_dao):
    """do_load_output() should return None when loading Design Electric for export."""
    DUT = dtmExports(test_dao)

    _hardware = dtmDesignElectric(test_dao)
    _tree = _hardware.do_select_all(hardware_id=1)

    assert DUT.do_load_output('Design Electric', _tree) is None


@pytest.mark.integration
def test_do_load_output_reliability(test_dao):
    """do_load_output() should return None when loading Reliability for export."""
    DUT = dtmExports(test_dao)

    _hardware = dtmReliability(test_dao)
    _tree = _hardware.do_select_all(hardware_id=1)

    assert DUT.do_load_output('Reliability', _tree) is None


@pytest.mark.integration
def test_do_load_output_validation(test_dao):
    """do_load_output() should return None when loading Validations for export."""
    DUT = dtmExports(test_dao)

    _validation = dtmValidation(test_dao)
    _tree = _validation.do_select_all(revision_id=1)

    assert DUT.do_load_output('Validation', _tree) is None


@pytest.mark.integration
def test_do_export_to_csv(test_dao, test_export_file):
    """do_export() should return None when exporting to a CSV file."""
    DUT = dtmExports(test_dao)

    _function = dtmFunction(test_dao, test=True)
    _function.do_select_all(revision_id=1)
    DUT.do_load_output('Function', _function.tree)

    _test_csv = test_export_file + '_function.csv'
    assert DUT.do_export('csv', _test_csv) is None


@pytest.mark.integration
def test_do_export_to_xls(test_dao, test_export_file):
    """do_export() should return None when exporting to an Excel file."""
    DUT = dtmExports(test_dao)

    _requirement = dtmRequirement(test_dao)
    _tree = _requirement.do_select_all(revision_id=1)
    DUT.do_load_output('Requirement', _tree)

    _test_excel = test_export_file + '_requirement.xls'
    assert DUT.do_export('excel', _test_excel) is None


@pytest.mark.integration
def test_do_export_to_xlsx(test_dao, test_export_file):
    """do_export() should return None when exporting to an Excel file."""
    DUT = dtmExports(test_dao)

    _requirement = dtmRequirement(test_dao)
    _tree = _requirement.do_select_all(revision_id=1)
    DUT.do_load_output('Requirement', _tree)

    _test_excel = test_export_file + '_requirement.xlsx'
    assert DUT.do_export('excel', _test_excel) is None


@pytest.mark.integration
def test_do_export_to_xlsm(test_dao, test_export_file):
    """do_export() should return None when exporting to an Excel file."""
    DUT = dtmExports(test_dao)

    _requirement = dtmRequirement(test_dao)
    _tree = _requirement.do_select_all(revision_id=1)
    DUT.do_load_output('Requirement', _tree)

    _test_excel = test_export_file + '_requirement.xlsm'
    assert DUT.do_export('excel', _test_excel) is None

@pytest.mark.integration
def test_do_export_to_text(test_dao, test_export_file):
    """do_export() should return None when exporting to a text file."""
    DUT = dtmExports(test_dao)

    _function = dtmFunction(test_dao, test=True)
    _function.do_select_all(revision_id=1)
    DUT.do_load_output('Function', _function.tree)

    _test_text = test_export_file + '_function.txt'
    assert DUT.do_export('text', _test_text) is None


@pytest.mark.integration
def test_create_data_controller(test_dao, test_configuration):
    """__init__() should create an instance of the Export data controller."""
    DUT = dtcExports(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcExports)
    assert isinstance(DUT._dtm_data_model, dtmExports)


@pytest.mark.integration
def test_request_do_load_output(test_dao, test_configuration):
    """
    request_do_load_output() should return None."""
    DUT = dtcExports(test_dao, test_configuration, test=True)

    _function = dtmFunction(test_dao, test=True)
    _function.do_select_all(revision_id=1)

    assert DUT.request_do_load_output('Function', _function.tree) is None


@pytest.mark.integration
def test_request_do_export_to_csv(test_dao, test_configuration, test_export_file):
    """
    request_do_export() should return None when exporting to a CSV file.
    """
    DUT = dtcExports(test_dao, test_configuration, test=True)

    _function = dtmFunction(test_dao, test=True)
    _function.do_select_all(revision_id=1)
    DUT.request_do_load_output('Function', _function.tree)

    _test_csv = test_export_file + '_function.csv'

    assert DUT.request_do_export('csv', _test_csv) is None
