#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestCrystal.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for the crystal module."""

import pytest

from rtk.analyses.prediction import Crystal

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

PART_COUNT_LAMBDA_B = [
    0.032, 0.096, 0.32, 0.19, 0.51, 0.38, 0.54, 0.70, 0.90, 0.74, 0.016, 0.42,
    1.0, 16.0
]

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

PART_COUNT_PIQ = [1.0, 2.1]

ATTRIBUTES['category_id'] = 8
ATTRIBUTES['add_adj_factor'] = 0.0
ATTRIBUTES['mult_adj_factor'] = 1.0
ATTRIBUTES['duty_cycle'] = 100.0
ATTRIBUTES['quantity'] = 1
ATTRIBUTES['subcategory_id'] = 1


@pytest.mark.calculation
@pytest.mark.parametrize("quality_id", [1, 2])
@pytest.mark.parametrize("environment_active_id",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
def test_calculate_mil_hdbk_217f_part_count(quality_id, environment_active_id):
    """(TestCrystalModule) calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['quality_id'] = quality_id
    ATTRIBUTES['environment_active_id'] = environment_active_id

    lambda_b = PART_COUNT_LAMBDA_B[environment_active_id - 1]
    piQ = PART_COUNT_PIQ[quality_id - 1]

    _attributes, _msg = Crystal.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if lambda_b == 0.0:
        assert _msg == ('RTK WARNING: Base hazard rate is 0.0 when '
                        'calculating crystal, hardware ID: 6')
    else:
        assert _msg == ''
    assert _attributes['lambda_b'] == lambda_b
    assert _attributes['piQ'] == piQ
    assert _attributes['hazard_rate_active'] == lambda_b * piQ


@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_environment():
    """(TestCrystalModule) calculate_mil_hdbk_217f_part_count() should return an error message when the active environment ID is missing."""
    ATTRIBUTES['environment_active_id'] = 100
    ATTRIBUTES['quality_id'] = 1

    _attributes, _msg = Crystal.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: Base hazard rate is 0.0 when calculating '
                    'crystal, hardware ID: 6, subcategory ID: 1, active '
                    'environment ID: 100')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 1.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_quality():
    """(TestCrystalModule) calculate_mil_hdbk_217f_part_count() should return an error message when the quality ID is missing."""
    ATTRIBUTES['environment_active_id'] = 1
    ATTRIBUTES['quality_id'] = 100

    _attributes, _msg = Crystal.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: piQ is 0.0 when calculating crystal, '
                    'hardware ID: 6 and quality ID: 100')
    assert _attributes['lambda_b'] == 0.032
    assert _attributes['piQ'] == 0.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress():
    """(TestConnectionModule) calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['frequency_operating'] = 10.0

    _attributes, _msg = Crystal.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert pytest.approx(_attributes['lambda_b'], 0.02207717)
    assert _attributes['piQ'] == 1.0
    assert _attributes['piE'] == 6.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.1324630)


@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_frequency():
    """(TestConnectionModule) calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['frequency_operating'] = 0.0

    _attributes, _msg = Crystal.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: Base hazard rate is 0.0 when calculating '
                    'crystal, hardware ID: 6')
    assert pytest.approx(_attributes['lambda_b'], 0.0)
    assert _attributes['piQ'] == 1.0
    assert _attributes['piE'] == 6.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.0)


@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_quality():
    """(TestConnectionModule) calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['quality_id'] = 100
    ATTRIBUTES['frequency_operating'] = 10.0

    _attributes, _msg = Crystal.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: piQ is 0.0 when calculating crystal, '
                    'hardware ID: 6')
    assert pytest.approx(_attributes['lambda_b'], 0.02207717)
    assert _attributes['piQ'] == 0.0
    assert _attributes['piE'] == 6.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.0)


@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_environment():
    """(TestConnectionModule) calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 100
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['frequency_operating'] = 10.0

    _attributes, _msg = Crystal.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: piE is 0.0 when calculating crystal, '
                    'hardware ID: 6')
    assert pytest.approx(_attributes['lambda_b'], 0.02207717)
    assert _attributes['piQ'] == 1.0
    assert _attributes['piE'] == 0.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.0)
