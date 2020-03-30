# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name
# -*- coding: utf-8 -*-
#
#       tests.exim.test_exports.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle "weibullguy" Rowland
"""Test class for testing the Exports module."""

# Third Party Imports
import pandas as pd
import pytest

# RAMSTK Package Imports
from ramstk.controllers import (
    dmFunction, dmHardware, dmRequirement, dmValidation
)
from ramstk.exim import COLUMN_HEADERS, Export


@pytest.mark.unit
def test_header_lists():
    """The COLUMN_HEADERS dict should contain a list of column headers for each workstream module."""
    assert isinstance(COLUMN_HEADERS, dict)
    assert COLUMN_HEADERS['Function'] == [
        'revision_id', 'function_id', 'level', 'function_code', 'name',
        'parent_id', 'remarks', 'safety_critical', 'type_id'
    ]
    assert COLUMN_HEADERS['Requirement'] == [
        'revision_id', 'requirement_id', 'derived', 'description',
        'figure_number', 'owner', 'page_number', 'parent_id', 'priority',
        'requirement_code', 'specification', 'requirement_type', 'validated',
        'validated_date'
    ]
    assert COLUMN_HEADERS['Hardware'] == [
        'revision_id', 'hardware_id', 'alt_part_num', 'cage_code',
        'category_id', 'comp_ref_des', 'cost', 'cost_type_id', 'description',
        'duty_cycle', 'figure_number', 'lcn', 'level', 'manufacturer_id',
        'mission_time', 'name', 'nsn', 'page_number', 'parent_id', 'part',
        'part_number', 'quantity', 'ref_des', 'remarks', 'repairable',
        'specification_number', 'subcategory_id', 'tagged_part',
        'year_of_manufacture'
    ]
    assert COLUMN_HEADERS['Design Electric'] == [
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
    assert COLUMN_HEADERS['Reliability'] == [
        'hardware_id', 'add_adj_factor', 'failure_distribution_id',
        'hazard_rate_method_id', 'hazard_rate_model', 'hazard_rate_specified',
        'hazard_rate_type_id', 'location_parameter', 'mtbf_specified',
        'mult_adj_factor', 'quality_id', 'reliability_goal',
        'reliability_goal_measure_id', 'scale_parameter', 'shape_parameter',
        'survival_analysis_id'
    ]
    assert COLUMN_HEADERS['Validation'] == [
        'revision_id', 'validation_id', 'acceptable_maximum',
        'acceptable_mean', 'acceptable_minimum', 'acceptable_variance',
        'confidence', 'cost_average', 'cost_maximum', 'cost_minimum',
        'date_start', 'date_end', 'description', 'measurement_unit', 'name',
        'status', 'task_type', 'task_specification', 'time_average',
        'time_maximum', 'time_minimum'
    ]


@pytest.mark.usefixtures('test_program_dao')
class TestExport():
    """Test class for export methods."""
    @pytest.mark.unit
    def test_do_load_output_function(self, test_program_dao):
        """do_load_output() should return a Pandas DataFrame when loading Functions for export."""
        _function = dmFunction()
        _function.do_connect(test_program_dao)
        _function.do_select_all(revision_id=1)

        DUT = Export()

        assert DUT.do_load_output('Function', 1) is None
        assert isinstance(DUT._df_output_data, pd.DataFrame)

    @pytest.mark.unit
    def test_do_load_output_requirement(self, test_program_dao):
        """do_load_output() should return None when loading Requirements for export."""
        _requirement = dmRequirement()
        _requirement.do_connect(test_program_dao)
        _requirement.do_select_all(1)

        DUT = Export()

        assert DUT.do_load_output('Requirement', 1) is None
        assert isinstance(DUT._df_output_data, pd.DataFrame)

    @pytest.mark.unit
    def test_do_load_output_hardware(self, test_program_dao):
        """do_load_output() should return None when loading Hardware for export."""
        _hardware = dmHardware()
        _hardware.do_connect(test_program_dao)
        _hardware.do_select_all(1)

        DUT = Export()

        assert DUT.do_load_output('Hardware', 7) is None
        assert isinstance(DUT._df_output_data, pd.DataFrame)

    @pytest.mark.unit
    def test_do_load_output_validation(self, test_program_dao):
        """do_load_output() should return None when loading Validations for export."""
        _validation = dmValidation()
        _validation.do_connect(test_program_dao)
        _validation.do_select_all(1)

        DUT = Export()

        assert DUT.do_load_output('Validation', 1) is None
        assert isinstance(DUT._df_output_data, pd.DataFrame)

    @pytest.mark.unit
    def test_do_export_to_csv(self, test_program_dao, test_export_dir):
        """do_export() should return None when exporting to a CSV file."""
        _function = dmFunction()
        _function.do_connect(test_program_dao)
        _function.do_select_all(revision_id=1)

        DUT = Export()
        DUT.do_load_output('Function', 1)

        _test_csv = test_export_dir + 'test_export_function.csv'
        assert DUT.do_export('csv', _test_csv) is None

    @pytest.mark.unit
    def test_do_export_to_xls(self, test_program_dao, test_export_dir):
        """do_export() should return None when exporting to an Excel file."""
        _requirement = dmRequirement()
        _requirement.do_connect(test_program_dao)
        _requirement.do_select_all(1)

        DUT = Export()

        assert DUT.do_load_output('Requirement', 1) is None

        _test_excel = test_export_dir + 'test_export_requirement.xls'
        assert DUT.do_export('excel', _test_excel) is None

    @pytest.mark.unit
    def test_do_export_to_xlsx(self, test_program_dao, test_export_dir):
        """do_export() should return None when exporting to an Excel file."""
        _requirement = dmRequirement()
        _requirement.do_connect(test_program_dao)
        _requirement.do_select_all(1)

        DUT = Export()

        assert DUT.do_load_output('Requirement', 1) is None

        _test_excel = test_export_dir + 'test_export_requirement.xlsx'
        assert DUT.do_export('excel', _test_excel) is None

    @pytest.mark.unit
    def test_do_export_to_xlsm(self, test_program_dao, test_export_dir):
        """do_export() should return None when exporting to an Excel file."""
        _requirement = dmRequirement()
        _requirement.do_connect(test_program_dao)
        _requirement.do_select_all(1)

        DUT = Export()

        assert DUT.do_load_output('Requirement', 1) is None

        _test_excel = test_export_dir + 'test_export_requirement.xlsm'
        assert DUT.do_export('excel', _test_excel) is None

    @pytest.mark.unit
    def test_do_export_to_excel_unknown_extension(self, test_program_dao,
                                                  test_export_dir):
        """do_export() should return None when exporting to an Excel file and default to using the xlwt engine."""
        _requirement = dmRequirement()
        _requirement.do_connect(test_program_dao)
        _requirement.do_select_all(1)

        DUT = Export()

        assert DUT.do_load_output('Requirement', 1) is None

        _test_excel = test_export_dir + 'test_export_requirement.xlbb'
        assert DUT.do_export('excel', _test_excel) is None

    @pytest.mark.unit
    def test_do_export_to_text(self, test_program_dao, test_export_dir):
        """do_export() should return None when exporting to a text file."""
        _function = dmFunction()
        _function.do_connect(test_program_dao)
        _function.do_select_all(revision_id=1)

        DUT = Export()
        DUT.do_load_output('Function', 1)

        _test_text = test_export_dir + 'test_export_function.txt'
        assert DUT.do_export('text', _test_text) is None
