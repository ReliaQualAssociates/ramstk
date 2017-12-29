#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestCapacitor.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for the capacitor module."""

import sys
from os.path import dirname

import gettext

import unittest
from nose.plugins.attrib import attr

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk",
)

from analyses.prediction import Capacitor

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestCapacitorModule(unittest.TestCase):
    """Class for testing the Capacitor module functions."""

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
        """Set up the test fixture for the Capacitor module."""
        pass

    @attr(all=True, unit=True)
    def test00a_calculate_mil_hdbk_217f_part_count(self):
        """(TestCapacitorModule) calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success."""
        self._attributes['subcategory_id'] = 1
        self._attributes['specification_id'] = 1
        self._attributes['environment_active_id'] = 1
        self._attributes['quality_id'] = 1
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.0036)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertEqual(_attributes['hazard_rate_active'], 0.000108)

    @attr(all=True, unit=True)
    def test00b_calculate_mil_hdbk_217f_part_count_all(self):
        """(TestCapacitorModule) calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success."""
        self._attributes['environment_active_id'] = 1
        self._attributes['quality_id'] = 1
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        # Calculate MIL-HDBK-217FN2, section 10.1
        self._attributes['subcategory_id'] = 1
        self._attributes['specification_id'] = 1
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.0036)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertEqual(_attributes['hazard_rate_active'], 0.000108)

        self._attributes['subcategory_id'] = 1
        self._attributes['specification_id'] = 2
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.0039)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 0.0001169999)

        # Calculate MIL-HDBK-217FN2, section 10.2
        self._attributes['subcategory_id'] = 2
        self._attributes['specification_id'] = 0
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.0047)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertEqual(_attributes['hazard_rate_active'], 0.000141)

        # Calculate MIL-HDBK-217FN2, section 10.3
        self._attributes['subcategory_id'] = 3
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.0021)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertEqual(_attributes['hazard_rate_active'], 6.3E-5)

        # Calculate MIL-HDBK-217FN2, section 10.4
        self._attributes['subcategory_id'] = 4
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.0029)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 8.6999999E-5)

        # Calculate MIL-HDBK-217FN2, section 10.5
        self._attributes['subcategory_id'] = 5
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.0041)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertEqual(_attributes['hazard_rate_active'], 0.000123)

        # Calculate MIL-HDBK-217FN2, section 10.6
        self._attributes['subcategory_id'] = 6
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.0023)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertEqual(_attributes['hazard_rate_active'], 6.9E-5)

        # Calculate MIL-HDBK-217FN2, section 10.7
        self._attributes['subcategory_id'] = 7
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.0005)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertEqual(_attributes['hazard_rate_active'], 1.5E-5)

        # Calculate MIL-HDBK-217FN2, section 10.8
        self._attributes['subcategory_id'] = 8
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.018)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 0.0005399999)

        # Calculate MIL-HDBK-217FN2, section 10.9
        self._attributes['subcategory_id'] = 9
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.00032)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 9.6E-6)

        # Calculate MIL-HDBK-217FN2, section 10.10
        self._attributes['subcategory_id'] = 10
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.0036)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 0.000108)

        # Calculate MIL-HDBK-217FN2, section 10.11
        self._attributes['subcategory_id'] = 11
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.00078)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 2.34E-5)

        # Calculate MIL-HDBK-217FN2, section 10.12
        self._attributes['subcategory_id'] = 12
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.0018)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 5.4E-5)

        # Calculate MIL-HDBK-217FN2, section 10.13
        self._attributes['subcategory_id'] = 13
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.0061)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 0.000183)

        # Calculate MIL-HDBK-217FN2, section 10.14
        self._attributes['subcategory_id'] = 14
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.024)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 0.0007199999)

        # Calculate MIL-HDBK-217FN2, section 10.15
        self._attributes['subcategory_id'] = 15
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.029)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 0.00087)

        # Calculate MIL-HDBK-217FN2, section 10.16
        self._attributes['subcategory_id'] = 16
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.08)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 0.0024)

        # Calculate MIL-HDBK-217FN2, section 10.17
        self._attributes['subcategory_id'] = 17
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.033)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 0.00099)

        # Calculate MIL-HDBK-217FN2, section 10.18
        self._attributes['subcategory_id'] = 18
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.8)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 0.024)

        # Calculate MIL-HDBK-217FN2, section 10.19
        self._attributes['subcategory_id'] = 19
        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.4)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 0.012)

    @attr(all=True, unit=True)
    def test00c_calculate_mil_hdbk_217f_part_count_missing_subcategory(self):
        """(TestCapacitorModule) calculate_mil_hdbk_217f_part_count() should return an error message when the subcategory ID is missing."""
        self._attributes['subcategory_id'] = 0
        self._attributes['specification_id'] = 1
        self._attributes['environment_active_id'] = 1
        self._attributes['quality_id'] = 1
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(
            _msg,
            'RTK WARNING: Base hazard rate is 0.0 when calculating capacitor, hardware ID: 6'
        )
        self.assertEqual(_attributes['lambda_b'], 0.0)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertEqual(_attributes['hazard_rate_active'], 0.0)

    @attr(all=True, unit=True)
    def test00d_calculate_mil_hdbk_217f_part_count_missing_specification(self):
        """(TestCapacitorModule) calculate_mil_hdbk_217f_part_count() should return an error message when the specification ID is missing and needed."""
        self._attributes['subcategory_id'] = 1
        self._attributes['specification_id'] = 0
        self._attributes['environment_active_id'] = 1
        self._attributes['quality_id'] = 1
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(
            _msg,
            'RTK WARNING: Base hazard rate is 0.0 when calculating capacitor, hardware ID: 6'
        )
        self.assertEqual(_attributes['lambda_b'], 0.0)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertEqual(_attributes['hazard_rate_active'], 0.0)

    @attr(all=True, unit=True)
    def test00e_calculate_mil_hdbk_217f_part_count_missing_subcategory(self):
        """(TestCapacitorModule) calculate_mil_hdbk_217f_part_count() should return an error message when the active environment ID is missing."""
        self._attributes['subcategory_id'] = 1
        self._attributes['specification_id'] = 1
        self._attributes['environment_active_id'] = 100
        self._attributes['quality_id'] = 1
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(
            _msg,
            'RTK WARNING: Base hazard rate is 0.0 when calculating capacitor, hardware ID: 6'
        )
        self.assertEqual(_attributes['lambda_b'], 0.0)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertEqual(_attributes['hazard_rate_active'], 0.0)

    @attr(all=True, unit=True)
    def test00f_calculate_mil_hdbk_217f_part_count_no_specification(self):
        """(TestCapacitorModule) calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success when calculating a capacitor that is not specification dependent."""
        self._attributes['subcategory_id'] = 12
        self._attributes['specification_id'] = 0
        self._attributes['environment_active_id'] = 4
        self._attributes['quality_id'] = 3
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        _attributes, _msg = Capacitor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.0097)
        self.assertEqual(_attributes['piQ'], 0.30)
        self.assertEqual(_attributes['hazard_rate_active'], 0.00291)

    @attr(all=True, unit=True)
    def test01a_calculate_mil_hdbk_217f_part_stress(self):
        """(TestCapacitorModule) calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
        self._attributes['subcategory_id'] = 1
        self._attributes['specification_id'] = 1
        self._attributes['environment_active_id'] = 4
        self._attributes['temperature_active'] = 32.0
        self._attributes['temperature_rated_max'] = 85.0
        self._attributes['quality_id'] = 2
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1
        self._attributes['capacitance'] = 0.0000033
        self._attributes['voltage_rated'] = 5.0
        self._attributes['voltage_ac_operating'] = 0.05
        self._attributes['voltage_dc_operating'] = 3.3

        _attributes, _msg = Capacitor.calculate_217f_part_stress(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertAlmostEqual(_attributes['voltage_ratio'], 0.67)
        self.assertAlmostEqual(_attributes['lambda_b'], 0.07944039)
        self.assertAlmostEqual(_attributes['piCV'], 0.3617763)
        self.assertEqual(_attributes['piQ'], 7.0)
        self.assertEqual(_attributes['piE'], 5.0)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 1.005887691)

    @attr(all=True, unit=True)
    def test02a_calculate_dormant_hazard_rate(self):
        """(TestCapacitorModule) calculate_dormant_hazard_rate() should return a dictionary of updated values on success."""
        self._attributes['environment_active_id'] = 4
        self._attributes['environment_dormant_id'] = 3
        self._attributes['hazard_rate_active'] = 1.005887691

        _attributes, _msg = Capacitor.calculate_dormant_hazard_rate(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertAlmostEqual(_attributes['hazard_rate_dormant'], 0.100588769)

    @attr(all=True, unit=True)
    def test02b_calculate_dormant_hazard_rate_unknown_env_id(self):
        """(TestCapacitorModule) calculate_dormant_hazard_rate() should return an error message when an unknown environment ID is passed."""
        self._attributes['environment_active_id'] = 24
        self._attributes['environment_dormant_id'] = 3
        self._attributes['hazard_rate_active'] = 1.005887691

        _attributes, _msg = Capacitor.calculate_dormant_hazard_rate(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(
            _msg, 'RTK ERROR: Unknown active and/or dormant environment ID. '
            'Active ID: 24, Dormant ID: 3')
        self.assertEqual(_attributes['hazard_rate_dormant'], 0.0)

    @attr(all=True, unit=True)
    def test03a_overstressed_mild_env(self):
        """(TestCapacitorModule) overstressed() should return overstress=False and reason='' on success without an overstressed condition in non-harsh environment."""
        self._attributes['environment_active_id'] = 1
        self._attributes['voltage_operating'] = 10.0
        self._attributes['voltage_rated'] = 20.0

        _attributes = Capacitor.overstressed(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertFalse(_attributes['overstress'])
        self.assertEqual(_attributes['reason'], '')

    @attr(all=True, unit=True)
    def test03b_overstressed_mild_env_voltage_margin(self):
        """(TestCapacitorModule) overstressed() should return overstress=True on success with operating voltage too close to rated in a non-harsh environment."""
        self._attributes['environment_active_id'] = 1
        self._attributes['voltage_operating'] = 19.0
        self._attributes['voltage_rated'] = 20.0

        _attributes = Capacitor.overstressed(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertTrue(_attributes['overstress'])
        self.assertEqual(_attributes['reason'],
                         '1. Operating voltage > 90% rated voltage.\n')

    @attr(all=True, unit=True)
    def test03c_overstressed_harsh_env(self):
        """(TestCapacitorModule) overstressed() should return overstress=False and reason='' on success without an overstressed condition in a harsh environment."""
        self._attributes['environment_active_id'] = 3
        self._attributes['voltage_operating'] = 10.0
        self._attributes['voltage_rated'] = 20.0
        self._attributes['temperature_rated_max'] = 85.0
        self._attributes['temperature_active'] = 55.0

        _attributes = Capacitor.overstressed(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertFalse(_attributes['overstress'])
        self.assertEqual(_attributes['reason'], '')

    @attr(all=True, unit=True)
    def test03d_overstressed_harsh_env_voltage_margin(self):
        """(TestCapacitorModule) overstressed() should return overstress=True on success with operating voltage too close to rated in a harsh environment."""
        self._attributes['environment_active_id'] = 3
        self._attributes['voltage_operating'] = 15.0
        self._attributes['voltage_rated'] = 20.0
        self._attributes['temperature_rated_max'] = 85.0
        self._attributes['temperature_active'] = 55.0

        _attributes = Capacitor.overstressed(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertTrue(_attributes['overstress'])
        self.assertEqual(_attributes['reason'],
                         '1. Operating voltage > 60% rated voltage.\n')

    @attr(all=True, unit=True)
    def test03e_overstressed_harsh_env_temperature_margin(self):
        """(TestCapacitorModule) overstressed() should return overstress=True on success with operating temperature too close to maximum rated in a harsh environment."""
        self._attributes['environment_active_id'] = 3
        self._attributes['voltage_operating'] = 10.0
        self._attributes['voltage_rated'] = 20.0
        self._attributes['temperature_rated_max'] = 85.0
        self._attributes['temperature_active'] = 80.0

        _attributes = Capacitor.overstressed(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertTrue(_attributes['overstress'])
        self.assertEqual(_attributes['reason'],
                         '1. Operating temperature within 10.0C of maximum '
                         'rated temperature.\n')

    @attr(all=True, unit=True)
    def test04a_calculate(self):
        """(TestCapacitorModule) calculate() should return should return a dictionary of updated values on success."""
        self._attributes['subcategory_id'] = 1
        self._attributes['specification_id'] = 1
        self._attributes['environment_active_id'] = 1
        self._attributes['environment_dormant_id'] = 2
        self._attributes['quality_id'] = 1
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        self._attributes['hazard_rate_method_id'] = 1
        _attributes, _msg = Capacitor.calculate(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.0036)
        self.assertEqual(_attributes['piQ'], 0.030)
        self.assertEqual(_attributes['hazard_rate_active'], 0.000108)

        self._attributes['hazard_rate_method_id'] = 2
        _attributes, _msg = Capacitor.calculate(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertAlmostEqual(_attributes['lambda_b'], 0.009968927)
        self.assertEqual(_attributes['piQ'], 3.0)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 0.01081956)

