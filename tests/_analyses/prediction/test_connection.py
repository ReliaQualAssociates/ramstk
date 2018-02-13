#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestConnection.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for the connection module."""

import pytest

import gettext

import unittest
from nose.plugins.attrib import attr

from rtk.analyses.prediction import Component, Connection

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

ATTRIBUTES = {
    'hazard_rate_percent': 0.0,
    'voltage_ac_operating': 0.0,
    'pressure_upstream': 0.0,
    'frequency_operating': 0.0,
    'type_id': 0,
    'resistance': 0.0,
    'friction': 0.0,
    'length_compressed': 0.0,
    'balance_id': 0,
    'scale_parameter': 0.0,
    'lubrication_id': 0,
    'temperature_dormant': 25.0,
    'Cmu': 0.0,
    'ref_des': 'C1',
    'hazard_rate_method_id': 1,
    'lambdaBP': 0.0,
    'Cm': 0.0,
    'flow_operating': 0.0,
    'temperature_case': 0.0,
    'Cac': 0.0,
    'surface_finish': 0.0,
    'contact_form_id': 0,
    'repairable': 0,
    'parent_id': 4,
    'alt_part_num': '',
    'hazard_rate_logistics': 0.0,
    'lambdaBD': 0.0,
    'manufacturer_id': 0,
    'hazard_rate_software': 0.0,
    'shape_parameter': 0.0,
    'total_power_dissipation': 0.0,
    'current_rated': 0.0,
    'cost_type_id': 0,
    'power_operating': 0.0,
    'pressure_downstream': 0.0,
    'diameter_coil': 0.0,
    'configuration_id': 0,
    'meyer_hardness': 0.0,
    'temperature_junction': 0.0,
    'reliability_goal_measure_id': 0,
    'Cgp': 0.0,
    'lcn': '',
    'Ce': 0.0,
    'piR': 0.0,
    'reliability_miss_variance': 0.0,
    'piCYC': 0.0,
    'piS': 0.0,
    'name': '',
    'construction_id': 0,
    'level': 0,
    'insert_id': 0,
    'n_ten': 0,
    'manufacturing_id': 0,
    'Cgt': 0.0,
    'cost_failure': 0.0,
    'family_id': 0,
    'load_id': 0,
    'B1': 0.0,
    'B2': 0.0,
    'piNR': 0.0,
    'revision_id': 1,
    'hazard_rate_dormant': 0.0,
    'comp_ref_des': 'S1:SS1:A1:C1',
    'piTAPS': 0.0,
    'operating_life': 0.0,
    'hazard_rate_specified': 0.0,
    'attachments': '',
    'weight': 0.0,
    'subcategory_id': 1,
    'Csf': 0.0,
    'Csc': 0.0,
    'deflection': 0.0,
    'filter_size': 0.0,
    'reliability_goal': 0.0,
    'cost': 0.0,
    'material_id': 0,
    'voltage_ratio': 0.0,
    'availability_logistics': 1.0,
    'Cst': 0.0,
    'Csw': 0.0,
    'Csv': 0.0,
    'diameter_inner': 0.0,
    'environment_active_id': 0,
    'pressure_rated': 0.0,
    'quality_id': 0,
    'piCV': 0.0,
    'hardware_id': 6,
    'altitude_operating': 0.0,
    'piCR': 0.0,
    'thickness': 0.0,
    'specification_id': 0,
    'diameter_outer': 0.0,
    'matching_id': 0,
    'figure_number': '',
    'hr_mission_variance': 0.0,
    'piCD': 0.0,
    'piCF': 0.0,
    'particle_size': 0.0,
    'reliability_mission': 1.0,
    'environment_dormant_id': 0,
    'n_elements': 0,
    'hazard_rate_active': 5.0,
    'casing_id': 0,
    'mtbf_log_variance': 0.0,
    'temperature_active': 35.0,
    'Ccw': 0.0,
    'Ccv': 0.0,
    'Cpd': 0.0,
    'Ccp': 0.0,
    'Cpf': 0.0,
    'Cs': 0.0,
    'reason': u'',
    'Ccs': 0.0,
    'offset': 0.0,
    'load_operating': 0.0,
    'Ccf': 0.0,
    'impact_id': 0,
    'Cpv': 0.0,
    'Cbl': 0.0,
    'year_of_manufacture': 2017,
    'n_wave_soldered': 0,
    'category_id': 4,
    'pressure_delta': 0.0,
    'length': 0.0,
    'cage_code': '',
    'Cf': 0.0,
    'load_design': 0.0,
    'mtbf_logistics': 0.0,
    'tagged_part': 0,
    'nsn': '',
    'temperature_hot_spot': 0.0,
    'feature_size': 0.0,
    'Clc': 0.0,
    'hr_logistics_variance': 0.0,
    'package_id': 0,
    'technology_id': 0,
    'n_cycles': 0,
    'mtbf_spec_variance': 0.0,
    'n_circuit_planes': 1,
    'contact_gauge': 0,
    'current_operating': 0.0,
    'location_parameter': 0.0,
    'water_per_cent': 0.0,
    'cost_hour': 0.0,
    'contact_rating_id': 0,
    'misalignment_angle': 0.0,
    'area': 0.0,
    'add_adj_factor': 5.0,
    'lambdaCYC': 0.0,
    'rpm_design': 0.0,
    'n_active_pins': 0,
    'capacitance': 0.0,
    'mission_time': 100.0,
    'reliability_logistics': 1.0,
    'lambda_b': 0.0,
    'C2': 0.0,
    'C1': 0.0,
    'failure_distribution_id': 0,
    'hazard_rate_model': u'',
    'quantity': 1,
    'pressure_contact': 0.0,
    'part': 1,
    'duty_cycle': 100.0,
    'Crd': 0.0,
    'voltage_rated': 0.0,
    'n_hand_soldered': 0,
    'hazard_rate_type_id': 1,
    'current_ratio': 0.0,
    'rpm_operating': 0.0,
    'avail_mis_variance': 0.0,
    'Ck': 0.0,
    'mult_adj_factor': 1.0,
    'Ci': 0.0,
    'Ch': 0.0,
    'Cn': 0.0,
    'length_relaxed': 0.0,
    'Cl': 0.0,
    'Cc': 0.0,
    'Cb': 0.0,
    'theta_jc': 0.0,
    'hr_dormant_variance': 0.0,
    'Cg': 0.0,
    'availability_mission': 1.0,
    'voltage_dc_operating': 0.0,
    'Cd': 0.0,
    'power_ratio': 0.0,
    'Cy': 0.0,
    'Cbv': 0.0,
    'Cbt': 0.0,
    'reliability_log_variance': 0.0,
    'overstress': 0,
    'Cr': 0.0,
    'Cq': 0.0,
    'Cp': 0.0,
    'Cw': 0.0,
    'Cv': 0.0,
    'Ct': 0.0,
    'Cnw': 0.0,
    'hr_specified_variance': 0.0,
    'Cnp': 0.0,
    'total_part_count': 0,
    'Csz': 0.0,
    'Calt': 0.0,
    'contact_pressure': 0.0,
    'insulation_id': 0,
    'temperature_rated_max': 0.0,
    'lambdaEOS': 0.0,
    'flow_design': 0.0,
    'years_in_production': 1,
    'hazard_rate_mission': 0.0,
    'avail_log_variance': 0.0,
    'piK': 0.0,
    'piL': 0.0,
    'piM': 0.0,
    'piN': 0.0,
    'Cga': 0.0,
    'piA': 0.0,
    'piC': 0.0,
    'piE': 0.0,
    'piF': 0.0,
    'temperature_rated_min': 0.0,
    'A1': 0.0,
    'A2': 0.0,
    'page_number': '',
    'piP': 0.0,
    'piQ': 10.0,
    'Cgs': 0.0,
    'power_rated': 0.0,
    'piT': 0.0,
    'piU': 0.0,
    'piV': 0.0,
    'Cgv': 0.0,
    'description': '',
    'piPT': 0.0,
    'viscosity_dynamic': 0.0,
    'viscosity_design': 0.0,
    'torque_id': 0,
    'voltage_esd': 0.0,
    'leakage_allowable': 0.0,
    'hr_active_variance': 0.0,
    'remarks': '',
    'width_minimum': 0.0,
    'mtbf_mission': 0.0,
    'application_id': 0,
    'piMFG': 0.0,
    'Cgl': 0.0,
    'piI': 0.0,
    'spring_index': 0.0,
    'mtbf_miss_variance': 0.0,
    'mtbf_specified': 0.0,
    'Cdc': 0.0,
    'Cdl': 0.0,
    'survival_analysis_id': 0,
    'Cdt': 0.0,
    'part_number': '',
    'Cdw': 0.0,
    'Cdp': 0.0,
    'temperature_rise': 0.0,
    'Cds': 0.0,
    'clearance': 0.0,
    'specification_number': '',
    'Cdy': 0.0,
    'diameter_wire': 0.0,
    'service_id': 0
}

PART_COUNT_LAMBDA_B = {
        1: {
            1: [
                0.011, 0.14, 0.11, 0.069, 0.20, 0.058, 0.098, 0.23, 0.34, 0.37,
                0.0054, 0.16, 0.42, 6.8
            ],
            2: [
                0.012, 0.015, 0.13, 0.075, 0.21, 0.06, 0.1, 0.22, 0.32, 0.38,
                0.0061, 0.18, 0.54, 7.3
            ]
        },
        2: [
            0.0054, 0.021, 0.055, 0.035, 0.10, 0.059, 0.11, 0.085, 0.16, 0.19,
            0.0027, 0.078, 0.21, 3.4
        ],
        3: [
            0.0019, 0.0058, 0.027, 0.012, 0.035, 0.015, 0.023, 0.021, 0.025,
            0.048, 0.00097, 0.027, 0.070, 1.3
        ],
        4: [
            0.053, 0.11, 0.37, 0.69, 0.27, 0.27, 0.43, 0.85, 1.5, 1.0, 0.027,
            0.53, 1.4, 27.0
        ],
        5: {
            1: [
                0.0026, 0.0052, 0.018, 0.010, 0.029, 0.010, 0.016, 0.016,
                0.021, 0.042, 0.0013, 0.023, 0.062, 1.1
            ],
            2: [
                0.00014, 0.00028, 0.00096, 0.00056, 0.0015, 0.00056, 0.00084,
                0.00084, 0.0011, 0.0022, 0.00007, 0.0013, 0.0034, 0.059
            ],
            3: [
                0.00026, 0.00052, 0.0018, 0.0010, 0.0029, 0.0010, 0.0016,
                0.0016, 0.0021, 0.0042, 0.00013, 0.0023, 0.0062, 0.11
            ],
            4: [
                0.000050, 0.000100, 0.000350, 0.000200, 0.000550, 0.000200,
                0.000300, 0.000300, 0.000400, 0.000800, 0.000025, 0.000450,
                0.001200, 0.021000
            ],
            5: [
                0.0000035, 0.000007, 0.000025, 0.000014, 0.000039, 0.000014,
                0.000021, 0.000021, 0.000028, 0.000056, 0.0000018, 0.000031,
                0.000084, 0.0015
            ],
            6: [
                0.00012, 0.00024, 0.00084, 0.00048, 0.0013, 0.00048, 0.00072,
                0.00072, 0.00096, 0.0019, 0.00005, 0.0011, 0.0029, 0.050
            ],
            7: [
                0.000069, 0.000138, 0.000483, 0.000276, 0.000759, 0.000276,
                0.000414, 0.000414, 0.000552, 0.001104, 0.000035, 0.000621,
                0.001656, 0.02898
            ]
        }
    }

DORMANT_MULT = {
            1: {
                2: 0.005
            },
            2: {
                2: 0.005
            },
            3: {
                2: 0.005
            },
            4: {
                2: 0.003,
                3: 0.008
            },
            5: {
                2: 0.003,
                3: 0.008
            },
            6: {
                1: 0.0005,
                2: 0.003
            },
            7: {
                1: 0.0005,
                2: 0.003
            },
            8: {
                1: 0.0005,
                2: 0.003
            },
            9: {
                1: 0.0005,
                2: 0.003
            },
            10: {
                1: 0.0005,
                2: 0.003
            },
            11: {
                2: 0.03,
                4: 0.02
            }
        }

PART_COUNT_PIQ = [1.0, 2.0]


ATTRIBUTES['category_id'] = 8
ATTRIBUTES['add_adj_factor'] = 0.0
ATTRIBUTES['mult_adj_factor'] = 1.0
ATTRIBUTES['duty_cycle'] = 100.0
ATTRIBUTES['quantity'] = 1


@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5])
@pytest.mark.parametrize("type_id", [1, 2,3,4,5,6,7])
@pytest.mark.parametrize("quality_id", [1, 2])
@pytest.mark.parametrize("environment_active_id",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
def test_calculate_mil_hdbk_217f_part_count(subcategory_id, type_id,
                                            quality_id, environment_active_id):
    """(TestCapacitorModule) calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['subcategory_id'] = subcategory_id
    ATTRIBUTES['type_id'] = type_id
    ATTRIBUTES['quality_id'] = quality_id
    ATTRIBUTES['environment_active_id'] = environment_active_id

    if subcategory_id in [1, 5]:
        try:
            lambda_b = PART_COUNT_LAMBDA_B[subcategory_id][type_id][
                environment_active_id - 1]
        except KeyError:
            lambda_b = 0.0
    else:
        lambda_b = PART_COUNT_LAMBDA_B[subcategory_id][environment_active_id
                                                       - 1]

    piQ = PART_COUNT_PIQ[quality_id - 1]

    _attributes, _msg = Connection.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if lambda_b == 0.0:
        assert _msg == ('RTK WARNING: Base hazard rate is 0.0 when '
                        'calculating connection, hardware ID: 6')
    else:
        assert _msg == ''
    assert _attributes['lambda_b'] == lambda_b
    assert _attributes['piQ'] == piQ
    assert _attributes['hazard_rate_active'] == lambda_b * piQ


@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_subcategory():
    """(TestCapacitorModule) calculate_mil_hdbk_217f_part_count() should return an error message when the subcategory ID is missing."""
    ATTRIBUTES['subcategory_id'] = 0
    ATTRIBUTES['type_id'] = 1
    ATTRIBUTES['quality_id'] = 1

    _attributes, _msg = Connection.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: Base hazard rate is 0.0 when calculating '
                    'connection, hardware ID: 6')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 1.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_type():
    """(TestCapacitorModule) calculate_mil_hdbk_217f_part_count() should return an error message when the type ID is missing and needed."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['type_id'] = 0
    ATTRIBUTES['quality_id'] = 1

    _attributes, _msg = Connection.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: Base hazard rate is 0.0 when calculating '
                    'connection, hardware ID: 6')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'], 0.030
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_environment():
    """(TestCapacitorModule) calculate_mil_hdbk_217f_part_count() should return an error message when the active environment ID is missing."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['type_id'] = 1
    ATTRIBUTES['environment_active_id'] = 100
    ATTRIBUTES['quality_id'] = 1

    _attributes, _msg = Connection.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: Base hazard rate is 0.0 when calculating '
                    'connection, hardware ID: 6')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 1.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress():
    """(TestConnectionModule) calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 3
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['type_id'] = 1
    ATTRIBUTES['specification_id'] = 1
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['quality_id'] = 2
    ATTRIBUTES['insert_id'] = 1
    ATTRIBUTES['contact_gauge'] = 20
    ATTRIBUTES['current_operating'] = 2
    ATTRIBUTES['n_cycles'] = 2
    ATTRIBUTES['n_active_pins'] = 20

    _attributes, _msg = Connection.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert pytest.approx(_attributes['voltage_ratio'], 0.67)
    assert pytest.approx(_attributes['lambda_b'], 0.07944039)
    assert pytest.approx(_attributes['piCV'], 0.3617763)
    assert _attributes['piQ'] == 10.0
    assert pytest.approx(_attributes['hazard_rate_active'], 1.005887691)
    assert pytest.approx(_attributes['temperature_rise'], 2.3072012)
    assert pytest.approx(_attributes['lambda_b'], 0.0006338549)
    assert _attributes['piK'] == 2.0
    assert pytest.approx(_attributes['piP'], 4.0062301)
    assert _attributes['piE'] == 21.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.1066535)


@pytest.mark.calculation
def test_calculate_insert_temperature():
    """Test the calculate_insert_temperature() function."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['current_operating'] = 2.65
    ATTRIBUTES['contact_gauge'] = 20

    _attributes = Connection.do_calculate_insert_temperature(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert pytest.approx(_attributes['temperature_rise'], 3.88315602448)


@pytest.mark.calculation
@pytest.mark.parametrize("environment_active_id",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
@pytest.mark.parametrize("environment_dormant_id", [1, 2, 3, 4])
def test_calculate_dormant_hazard_rate(environment_active_id,
                                       environment_dormant_id):
    """(TestCapacitorModule) calculate_dormant_hazard_rate() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_active'] = 1.005887691
    ATTRIBUTES['environment_active_id'] = environment_active_id
    ATTRIBUTES['environment_dormant_id'] = environment_dormant_id

    try:
        dormant_mult = DORMANT_MULT[environment_active_id][ATTRIBUTES[
            'environment_dormant_id']]
    except KeyError:
        dormant_mult = 0.0

    _attributes, _msg = Component.do_calculate_dormant_hazard_rate(
        **ATTRIBUTES)

    assert isinstance(_attributes, dict)
    try:
        assert _msg == ''
    except AssertionError:
        assert _msg == ('RTK ERROR: Unknown active and/or dormant environment '
                        'ID.  Active ID: {0:d}, '
                        'Dormant ID: {1:d}').format(environment_active_id,
                                                    environment_dormant_id)

    assert pytest.approx(_attributes['hazard_rate_dormant'],
                         ATTRIBUTES['hazard_rate_active'] * dormant_mult)


@pytest.mark.calculation
@pytest.mark.parametrize("voltage_rated", [40.0, 20.0])
@pytest.mark.parametrize("environment_active_id",
                         [3, 5, 6, 7, 8, 9, 10, 12, 13, 14])
def test_voltage_overstress_harsh_environment(voltage_rated,
                                              environment_active_id):
    """(TestCapacitorModule) overstressed() should return True when voltage ratio > 0.6 in a harsh environment and False otherwise."""
    ATTRIBUTES['voltage_ac_operating'] = 0.005
    ATTRIBUTES['voltage_dc_operating'] = 15.0
    ATTRIBUTES['temperature_rated_max'] = 125.0
    ATTRIBUTES['temperature_active'] = 48.7
    ATTRIBUTES['voltage_rated'] = voltage_rated
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(**_attributes)

    assert isinstance(_attributes, dict)
    if voltage_rated == 40.0:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif voltage_rated == 20.0:
        assert _attributes['overstress']
        assert _attributes['reason'] == ('1. Operating voltage > 70% rated '
                                         'voltage in harsh environment.\n')


@pytest.mark.calculation
@pytest.mark.parametrize("temperature_active", [48.7, 118.2])
@pytest.mark.parametrize("environment_active_id",
                         [3, 5, 6, 7, 8, 9, 10, 12, 13, 14])
def test_temperature_overstress_harsh_environment(temperature_active,
                                                  environment_active_id):
    """(TestCapacitorModule) overstressed() should return True when active temperature is within 10C of rated temperature in a harsh environment and False otherwise."""
    ATTRIBUTES['voltage_rated'] = 40.0
    ATTRIBUTES['voltage_ac_operating'] = 0.005
    ATTRIBUTES['voltage_dc_operating'] = 10.0
    ATTRIBUTES['temperature_rated_max'] = 125.0
    ATTRIBUTES['temperature_active'] = temperature_active
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(**_attributes)

    assert isinstance(_attributes, dict)
    if temperature_active == 48.7:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif temperature_active == 118.2:
        assert _attributes['overstress']
        assert _attributes['reason'] == ('1. Operating temperature within '
                                         '25.0C of maximum rated '
                                         'temperature.\n')


@pytest.mark.calculation
@pytest.mark.parametrize("voltage_rated", [20.0, 12.0])
@pytest.mark.parametrize("environment_active_id", [1, 2, 4, 11])
def test_voltage_overstress_mild_environment(voltage_rated,
                                             environment_active_id):
    """(TestCapacitorModule) overstressed() should return True when voltage ratio > 0.9 in a mild environment and False otherwise."""
    ATTRIBUTES['voltage_ac_operating'] = 0.005
    ATTRIBUTES['voltage_dc_operating'] = 11.0
    ATTRIBUTES['temperature_rated_max'] = 125.0
    ATTRIBUTES['temperature_active'] = 48.7
    ATTRIBUTES['voltage_rated'] = voltage_rated
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(**_attributes)

    assert isinstance(_attributes, dict)
    if voltage_rated == 20.0:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif voltage_rated == 12.0:
        assert _attributes['overstress']
        assert _attributes['reason'] == ('1. Operating voltage > 90% rated '
                                         'voltage in mild environment.\n')
