#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestResistor.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for the resistor module."""

import sys
from os.path import dirname

import gettext

import unittest
from nose.plugins.attrib import attr

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk",
)

from analyses.prediction import Resistor

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestResistorModule(unittest.TestCase):
    """Class for testing the Resistor module functions."""

    _attributes = {
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

    def setUp(self):
        """Set up the test fixture for the Resistor module."""
        self._dic_lambda_b = {
            1: [
                0.0005, 0.0022, 0.0071, 0.0037, 0.012, 0.0052, 0.0065, 0.016,
                0.025, 0.025, 0.00025, 0.0098, 0.035, 0.36
            ],
            2: {
                1: [
                    0.0012, 0.0027, 0.011, 0.0054, 0.020, 0.0063, 0.013, 0.018,
                    0.033, 0.030, 0.00025, 0.014, 0.044, 0.69
                ],
                2: [
                    0.0012, 0.0027, 0.011, 0.0054, 0.020, 0.0063, 0.013, 0.018,
                    0.033, 0.030, 0.00025, 0.014, 0.044, 0.69
                ],
                3: [
                    0.0014, 0.0031, 0.013, 0.0061, 0.023, 0.0072, 0.014, 0.021,
                    0.038, 0.034, 0.00028, 0.016, 0.050, 0.78
                ],
                4: [
                    0.0014, 0.0031, 0.013, 0.0061, 0.023, 0.0072, 0.014, 0.021,
                    0.038, 0.034, 0.00028, 0.016, 0.050, 0.78
                ]
            },
            3: [
                0.012, 0.025, 0.13, 0.062, 0.21, 0.078, 0.10, 0.19, 0.24, 0.32,
                0.0060, 0.18, 0.47, 8.2
            ],
            4: [
                0.0023, 0.0066, 0.031, 0.013, 0.055, 0.022, 0.043, 0.077, 0.15,
                0.10, 0.0011, 0.055, 0.15, 1.7
            ],
            5: [
                0.0085, 0.018, 0.10, 0.045, 0.16, 0.15, 0.17, 0.30, 0.38, 0.26,
                0.0068, 0.13, 0.37, 5.4
            ],
            6: {
                1: [
                    0.014, 0.031, 0.16, 0.077, 0.26, 0.073, 0.15, 0.19, 0.39,
                    0.42, 0.0042, 0.21, 0.62, 9.4
                ],
                2: [
                    0.013, 0.028, 0.15, 0.070, 0.24, 0.065, 0.13, 0.18, 0.35,
                    0.38, 0.0038, 0.19, 0.56, 8.6
                ]
            },
            7: [
                0.008, 0.18, 0.096, 0.045, 0.15, 0.044, 0.088, 0.12, 0.24,
                0.25, 0.004, 0.13, 0.37, 5.5
            ],
            8: [
                0.065, 0.32, 1.4, 0.71, 1.6, 0.71, 1.9, 1.0, 2.7, 2.4, 0.032,
                1.3, 3.4, 62.0
            ],
            9: [
                0.025, 0.055, 0.35, 0.15, 0.58, 0.16, 0.26, 0.35, 0.58, 1.1,
                0.013, 0.52, 1.6, 24.0
            ],
            10: [
                0.33, 0.73, 7.0, 2.9, 12.0, 3.5, 5.3, 7.1, 9.8, 23.0, 0.16,
                11.0, 33.0, 510.0
            ],
            11: [
                0.15, 0.35, 3.1, 1.2, 5.4, 1.9, 2.8, 0.0, 0.0, 9.0, 0.075, 0.0,
                0.0, 0.0
            ],
            12: [
                0.15, 0.34, 2.9, 1.2, 5.0, 1.6, 2.4, 0.0, 0.0, 7.6, 0.076, 0.0,
                0.0, 0.0
            ],
            13: [
                0.043, 0.15, 0.75, 0.35, 1.3, 0.39, 0.78, 1.8, 2.8, 2.5, 0.21,
                1.2, 3.7, 49.0
            ],
            14: [
                0.05, 0.11, 1.1, 0.45, 1.7, 2.8, 4.6, 4.6, 7.5, 3.3, 0.025,
                1.5, 4.7, 67.0
            ],
            15: [
                0.048, 0.16, 0.76, 0.36, 1.3, 0.36, 0.72, 1.4, 2.2, 2.3, 0.024,
                1.2, 3.4, 52.0
            ]
        }
        self._lst_piQ = [0.030, 0.10, 0.30, 1.0, 3.0, 10.0]

    @attr(all=True, unit=True)
    def test00a_calculate_mil_hdbk_217f_part_count(self):
        """(TestResistorModule) calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success."""
        self._attributes['subcategory_id'] = 2
        self._attributes['specification_id'] = 1
        self._attributes['environment_active_id'] = 1
        self._attributes['quality_id'] = 1
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        _attributes, _msg = Resistor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.0012)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 3.6E-05)

    @attr(all=True, unit=True)
    def test00b_calculate_mil_hdbk_217f_part_count_all(self):
        """(TestResistorModule) calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success for each subcategory, active environment, and quality level combination."""
        self._attributes['specification_id'] = 1
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        for subcategory_id in xrange(1, 16):
            self._attributes['subcategory_id'] = subcategory_id
            for environment_active_id in xrange(1, 15):
                self._attributes[
                    'environment_active_id'] = environment_active_id
                for quality_id in xrange(1, 7):
                    self._attributes['quality_id'] = quality_id
                    _test_msg = 'test00b_calculate_mil_hdbk_217f_part_count_{}_{}_{} ' \
                                'failed'.format(subcategory_id,
                                                environment_active_id,
                                                quality_id)

                    _attributes, _msg = Resistor.calculate_217f_part_count(
                        **self._attributes)

                    self.assertTrue(isinstance(_attributes, dict), _test_msg)

                    if (subcategory_id in [11, 12]
                            and environment_active_id in [8, 9, 12, 13, 14]):
                        self.assertEqual(
                            _msg,
                            'RTK INFO: Base hazard rate is 0.0 when ' \
                            'calculating resistor, hardware ID: 6, ' \
                            'subcategory ID: {0:d}, and active environment ' \
                            'ID: {1:d}.  This is expected as the base ' \
                            'hazard rate is zero for this environment.'.
                            format(subcategory_id, environment_active_id))
                    else:
                        self.assertEqual(_msg, '', _test_msg)

                    if subcategory_id in [2, 6]:
                        _lambda_b = self._dic_lambda_b[subcategory_id][1][
                            environment_active_id - 1]
                    else:
                        _lambda_b = self._dic_lambda_b[subcategory_id][
                            environment_active_id - 1]
                    _piQ = self._lst_piQ[quality_id - 1]
                    self.assertEqual(_attributes['lambda_b'], _lambda_b,
                                     _test_msg)
                    self.assertEqual(_attributes['piQ'], _piQ, _test_msg)
                    self.assertEqual(_attributes['hazard_rate_active'],
                                     _lambda_b * _piQ, _test_msg)

    @attr(all=True, unit=True)
    def test00c_calculate_mil_hdbk_217f_part_count_missing_subcategory(self):
        """(TestResistorModule) calculate_mil_hdbk_217f_part_count() should return an error message when the subcategory ID is missing."""
        self._attributes['subcategory_id'] = 0
        self._attributes['specification_id'] = 1
        self._attributes['environment_active_id'] = 1
        self._attributes['quality_id'] = 1
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        _attributes, _msg = Resistor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(
            _msg,
            'RTK WARNING: Base hazard rate is 0.0 when calculating ' \
            'resistor, hardware ID: 6, subcategory ID: 0, specification ' \
            'ID: 1, active environment ID: 1, and quality ID: 1.'
        )
        self.assertEqual(_attributes['lambda_b'], 0.0)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertEqual(_attributes['hazard_rate_active'], 0.0)

    @attr(all=True, unit=True)
    def test00d_calculate_mil_hdbk_217f_part_count_missing_specification(self):
        """(TestResistorModule) calculate_mil_hdbk_217f_part_count() should return an error message when the specification ID is missing and needed."""
        self._attributes['subcategory_id'] = 2
        self._attributes['specification_id'] = 0
        self._attributes['environment_active_id'] = 1
        self._attributes['quality_id'] = 1
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        _attributes, _msg = Resistor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(
            _msg,
            'RTK WARNING: Base hazard rate is 0.0 when calculating ' \
            'resistor, hardware ID: 6, subcategory ID: 2, specification ' \
            'ID: 0, active environment ID: 1, and quality ID: 1.'
        )
        self.assertEqual(_attributes['lambda_b'], 0.0)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertEqual(_attributes['hazard_rate_active'], 0.0)

    @attr(all=True, unit=True)
    def test00e_calculate_mil_hdbk_217f_part_count_missing_environment(self):
        """(TestResistorModule) calculate_mil_hdbk_217f_part_count() should return an error message when the active environment ID is missing."""
        self._attributes['subcategory_id'] = 1
        self._attributes['specification_id'] = 1
        self._attributes['environment_active_id'] = 100
        self._attributes['quality_id'] = 1
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        _attributes, _msg = Resistor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(
            _msg,
            'RTK WARNING: Base hazard rate is 0.0 when calculating '
            'resistor, hardware ID: 6, subcategory ID: 1, specification ' \
            'ID: 1, active environment ID: 100, and quality ID: 1.'
        )
        self.assertEqual(_attributes['lambda_b'], 0.0)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertEqual(_attributes['hazard_rate_active'], 0.0)

    @attr(all=True, unit=True)
    def test00f_calculate_mil_hdbk_217f_part_count_no_specification(self):
        """(TestResistorModule) calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success when calculating a resistor that is not specification dependent."""
        self._attributes['subcategory_id'] = 12
        self._attributes['specification_id'] = 0
        self._attributes['environment_active_id'] = 4
        self._attributes['quality_id'] = 3
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        _attributes, _msg = Resistor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 1.2)
        self.assertEqual(_attributes['piQ'], 0.30)
        self.assertEqual(_attributes['hazard_rate_active'], 0.36)

    @attr(all=True, unit=True)
    def test01a_calculate_mil_hdbk_217f_part_stress(self):
        """(TestResistorModule) calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
        self._attributes['subcategory_id'] = 10
        self._attributes['power_rated'] = 5.0
        self._attributes['power_operating'] = 1.5
        self._attributes['voltage_rated'] = 250.0
        self._attributes['voltage_ac_operating'] = 0.05
        self._attributes['voltage_dc_operating'] = 15.0
        self._attributes['resistance'] = 3.3E4
        self._attributes['construction_id'] = 2
        self._attributes['n_elements'] = 4
        self._attributes['quality_id'] = 2
        self._attributes['environment_active_id'] = 4
        self._attributes['temperature_active'] = 32.0
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        _attributes, _msg = Resistor.calculate_217f_part_stress(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertAlmostEqual(_attributes['power_ratio'], 0.3)
        self.assertAlmostEqual(_attributes['voltage_ratio'], 0.8901438)
        self.assertAlmostEqual(_attributes['lambda_b'], 4.2888845)
        self.assertEqual(_attributes['piQ'], 5.0)
        self.assertEqual(_attributes['piE'], 8.0)
        self.assertAlmostEqual(_attributes['piV'], 1.4)
        self.assertAlmostEqual(_attributes['piR'], 1.1)
        self.assertAlmostEqual(_attributes['piC'], 1.0)
        self.assertAlmostEqual(_attributes['piTAPS'], 1.112)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 293.7851584)

    @attr(all=True, unit=True)
    def test02a_calculate_dormant_hazard_rate(self):
        """(TestResistorModule) calculate_dormant_hazard_rate() should return a dictionary of updated values on success."""
        self._attributes['environment_active_id'] = 4
        self._attributes['environment_dormant_id'] = 3
        self._attributes['hazard_rate_active'] = 1.005887691

        _attributes, _msg = Resistor.calculate_dormant_hazard_rate(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertAlmostEqual(_attributes['hazard_rate_dormant'], 0.100588769)

    @attr(all=True, unit=True)
    def test02b_calculate_dormant_hazard_rate_unknown_env_id(self):
        """(TestResistorModule) calculate_dormant_hazard_rate() should return an error message when an unknown environment ID is passed."""
        self._attributes['environment_active_id'] = 24
        self._attributes['environment_dormant_id'] = 3
        self._attributes['hazard_rate_active'] = 1.005887691

        _attributes, _msg = Resistor.calculate_dormant_hazard_rate(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(
            _msg, 'RTK ERROR: Unknown active and/or dormant environment ID. '
            'Active ID: 24, Dormant ID: 3')
        self.assertEqual(_attributes['hazard_rate_dormant'], 0.0)

    @attr(all=True, unit=True)
    def test03a_overstressed_mild_env(self):
        """(TestResistorModule) overstressed() should return overstress=False and reason='' on success without an overstressed condition in non-harsh environment."""
        self._attributes['environment_active_id'] = 1
        self._attributes['power_operating'] = 0.18
        self._attributes['power_rated'] = 0.5

        _attributes = Resistor.overstressed(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertFalse(_attributes['overstress'])
        self.assertEqual(_attributes['reason'], '')

    @attr(all=True, unit=True)
    def test03b_overstressed_mild_env_power_margin(self):
        """(TestResistorModule) overstressed() should return overstress=True on success with operating power too close to rated in a non-harsh environment."""
        self._attributes['environment_active_id'] = 1
        self._attributes['power_operating'] = 0.48
        self._attributes['power_rated'] = 0.5

        _attributes = Resistor.overstressed(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertTrue(_attributes['overstress'])
        self.assertEqual(_attributes['reason'],
                         '1. Operating power > 90% rated power.\n')

    @attr(all=True, unit=True)
    def test03c_overstressed_harsh_env(self):
        """(TestResistorModule) overstressed() should return overstress=False and reason='' on success without an overstressed condition in a harsh environment."""
        self._attributes['environment_active_id'] = 3
        self._attributes['power_operating'] = 0.15
        self._attributes['power_rated'] = 0.5

        _attributes = Resistor.overstressed(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertFalse(_attributes['overstress'])
        self.assertEqual(_attributes['reason'], '')

    @attr(all=True, unit=True)
    def test03d_overstressed_harsh_env_voltage_margin(self):
        """(TestResistorModule) overstressed() should return overstress=True on success with operating voltage too close to rated in a harsh environment."""
        self._attributes['environment_active_id'] = 3
        self._attributes['power_operating'] = 0.40
        self._attributes['power_rated'] = 0.5

        _attributes = Resistor.overstressed(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertTrue(_attributes['overstress'])
        self.assertEqual(_attributes['reason'],
                         '1. Operating power > 50% rated power.\n')

    @attr(all=True, unit=True)
    def test04a_calculate(self):
        """(TestResistorModule) calculate() should return should return a dictionary of updated values on success."""
        self._attributes['subcategory_id'] = 12
        self._attributes['environment_active_id'] = 4
        self._attributes['quality_id'] = 3
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        self._attributes['hazard_rate_method_id'] = 1
        _attributes, _msg = Resistor.calculate(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 1.2)
        self.assertEqual(_attributes['piQ'], 0.30)
        self.assertEqual(_attributes['hazard_rate_active'], 0.36)

        self._attributes['hazard_rate_method_id'] = 2
        self._attributes['subcategory_id'] = 10
        self._attributes['power_rated'] = 5.0
        self._attributes['power_operating'] = 1.5
        self._attributes['voltage_rated'] = 250.0
        self._attributes['voltage_ac_operating'] = 0.05
        self._attributes['voltage_dc_operating'] = 15.0
        self._attributes['resistance'] = 3.3E4
        self._attributes['construction_id'] = 2
        self._attributes['n_elements'] = 4
        self._attributes['quality_id'] = 2
        self._attributes['temperature_active'] = 32.0
        _attributes, _msg = Resistor.calculate(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertAlmostEqual(_attributes['power_ratio'], 0.3)
        self.assertAlmostEqual(_attributes['voltage_ratio'], 0.8901438)
        self.assertAlmostEqual(_attributes['lambda_b'], 4.2888845)
        self.assertEqual(_attributes['piQ'], 5.0)
        self.assertEqual(_attributes['piE'], 8.0)
        self.assertAlmostEqual(_attributes['piV'], 1.4)
        self.assertAlmostEqual(_attributes['piR'], 1.1)
        self.assertAlmostEqual(_attributes['piC'], 1.0)
        self.assertAlmostEqual(_attributes['piTAPS'], 1.112)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 293.7851584)
