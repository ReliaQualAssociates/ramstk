#!/usr/bin/env python -O
"""
This is the test class for testing Hardware module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestHardware.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from hardware.Hardware import Model


__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestHardwareModel(unittest.TestCase):
    """
    Class for testing the Hardware data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Hardware class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestHardware) __init__ should return a Hardware model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.hardware_id, None)
        self.assertEqual(self.DUT.alt_part_number, '')
        self.assertEqual(self.DUT.attachments, '')
        self.assertEqual(self.DUT.cage_code, '')
        self.assertEqual(self.DUT.comp_ref_des, '')
        self.assertEqual(self.DUT.cost, 0.0)
        self.assertEqual(self.DUT.cost_failure, 0.0)
        self.assertEqual(self.DUT.cost_hour, 0.0)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.duty_cycle, 100.0)
        self.assertEqual(self.DUT.environment_active, 0)
        self.assertEqual(self.DUT.environment_dormant, 0)
        self.assertEqual(self.DUT.figure_number, '')
        self.assertEqual(self.DUT.humidity, 50.0)
        self.assertEqual(self.DUT.lcn, '')
        self.assertEqual(self.DUT.level, 1)
        self.assertEqual(self.DUT.manufacturer, 0)
        self.assertEqual(self.DUT.mission_time, 10.0)
        self.assertEqual(self.DUT.name, '')
        self.assertEqual(self.DUT.nsn, '')
        self.assertEqual(self.DUT.overstress, 0)
        self.assertEqual(self.DUT.page_number, '')
        self.assertEqual(self.DUT.parent_id, 0)
        self.assertEqual(self.DUT.part, 0)
        self.assertEqual(self.DUT.part_number, '')
        self.assertEqual(self.DUT.quantity, 1)
        self.assertEqual(self.DUT.ref_des, '')
        self.assertEqual(self.DUT.reliability_goal, 1.0)
        self.assertEqual(self.DUT.reliability_goal_measure, 0)
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.rpm, 0.0)
        self.assertEqual(self.DUT.specification_number, '')
        self.assertEqual(self.DUT.tagged_part, 0)
        self.assertEqual(self.DUT.temperature_active, 30.0)
        self.assertEqual(self.DUT.temperature_dormant, 30.0)
        self.assertEqual(self.DUT.vibration, 0.0)
        self.assertEqual(self.DUT.year_of_manufacture, 2014)

        self.assertEqual(self.DUT.current_ratio, 1.0)
        self.assertEqual(self.DUT.max_rated_temperature, 0.0)
        self.assertEqual(self.DUT.min_rated_temperature, 0.0)
        self.assertEqual(self.DUT.operating_current, 0.0)
        self.assertEqual(self.DUT.operating_power, 0.0)
        self.assertEqual(self.DUT.operating_voltage, 0.0)
        self.assertEqual(self.DUT.power_ratio, 1.0)
        self.assertEqual(self.DUT.rated_current, 1.0)
        self.assertEqual(self.DUT.rated_power, 1.0)
        self.assertEqual(self.DUT.rated_voltage, 1.0)
        self.assertEqual(self.DUT.temperature_rise, 0.0)
        self.assertEqual(self.DUT.voltage_ratio, 1.0)

        self.assertEqual(self.DUT.add_adj_factor, 0.0)
        self.assertEqual(self.DUT.availability_logistics, 1.0)
        self.assertEqual(self.DUT.availability_mission, 1.0)
        self.assertEqual(self.DUT.avail_log_variance, 0.0)
        self.assertEqual(self.DUT.avail_mis_variance, 0.0)
        self.assertEqual(self.DUT.failure_dist, 0)
        self.assertEqual(self.DUT.failure_parameter_1, 0.0)
        self.assertEqual(self.DUT.failure_parameter_2, 0.0)
        self.assertEqual(self.DUT.failure_parameter_3, 0.0)
        self.assertEqual(self.DUT.hazard_rate_active, 0.0)
        self.assertEqual(self.DUT.hazard_rate_dormant, 0.0)
        self.assertEqual(self.DUT.hazard_rate_logistics, 0.0)
        self.assertEqual(self.DUT.hazard_rate_method, 1)
        self.assertEqual(self.DUT.hazard_rate_mission, 0.0)
        self.assertEqual(self.DUT.hazard_rate_model, {})
        self.assertEqual(self.DUT.hazard_rate_percent, 0.0)
        self.assertEqual(self.DUT.hazard_rate_software, 0.0)
        self.assertEqual(self.DUT.hazard_rate_specified, 0.0)
        self.assertEqual(self.DUT.hazard_rate_type, 1)
        self.assertEqual(self.DUT.hr_active_variance, 0.0)
        self.assertEqual(self.DUT.hr_dormant_variance, 0.0)
        self.assertEqual(self.DUT.hr_logistics_variance, 0.0)
        self.assertEqual(self.DUT.hr_mission_variance, 0.0)
        self.assertEqual(self.DUT.hr_specified_variance, 0.0)
        self.assertEqual(self.DUT.mtbf_logistics, 0.0)
        self.assertEqual(self.DUT.mtbf_mission, 0.0)
        self.assertEqual(self.DUT.mtbf_specified, 0.0)
        self.assertEqual(self.DUT.mtbf_log_variance, 0.0)
        self.assertEqual(self.DUT.mtbf_miss_variance, 0.0)
        self.assertEqual(self.DUT.mtbf_spec_variance, 0.0)
        self.assertEqual(self.DUT.mult_adj_factor, 1.0)
        self.assertEqual(self.DUT.reliability_logistics, 1.0)
        self.assertEqual(self.DUT.reliability_mission, 1.0)
        self.assertEqual(self.DUT.rel_log_variance, 0.0)
        self.assertEqual(self.DUT.rel_miss_variance, 0.0)
        self.assertEqual(self.DUT.survival_analysis, 0)

    @attr(all=True, unit=True)
    def test_set_base_attributes(self):
        """
        (TestHardware) _set_base_attributes should return a 0 error code on success
        """

        _base_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                        'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                        0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                        0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                        'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014)

        (_error_code,
         _error_msg) = self.DUT._set_base_attributes(_base_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_base_attributes_wrong_type(self):
        """
        (TestHardware) _set_base_attributes should return a 10 error code when passed a wrong data type
        """

        _base_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                        'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                        0, 'Figure #', None, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                        0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                        'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014)

        (_error_code,
         _error_msg) = self.DUT._set_base_attributes(_base_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_base_attributes_missing_index(self):
        """
        (TestHardware) _set_base_attributes should return a 40 error code when too few items are passed
        """

        _base_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                        'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                        0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                        0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                        'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0)

        (_error_code,
         _error_msg) = self.DUT._set_base_attributes(_base_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_stress_attributes(self):
        """
        (TestHardware) _set_stress_attributes should return a 0 error code on success
        """

        _stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                          0.0, 1.0)

        (_error_code,
         _error_msg) = self.DUT._set_stress_attributes(_stress_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_stress_attributes_wrong_type(self):
        """
        (TestHardware) _set_stress_attributes should return a 10 error code when passed a wrong data type
        """

        _stress_values = (1.0, 0.0, None, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                          0.0, 1.0)

        (_error_code,
         _error_msg) = self.DUT._set_stress_attributes(_stress_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_stress_attributes_missing_index(self):
        """
        (TestHardware) _set_stress_attributes should return a 40 error code when too few items are passed
        """

        _stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0)

        (_error_code,
         _error_msg) = self.DUT._set_stress_attributes(_stress_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_reliability_attributes(self):
        """
        (TestHardware) _set_reliability_attributes should return a 0 error code on success
        """

        _rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0)

        (_error_code,
         _error_msg) = self.DUT._set_reliability_attributes(_rel_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_reliability_attributes_wrong_type(self):
        """
        (TestHardware) _set_reliability_attributes should return a 10 error code when passed a wrong data type
        """

        _rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, None, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0)

        (_error_code,
         _error_msg) = self.DUT._set_reliability_attributes(_rel_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_reliability_attributes_missing_index(self):
        """
        (TestHardware) _set_reliability_attributes should return a 40 error code when too few items are passed
        """

        _rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0)

        (_error_code,
         _error_msg) = self.DUT._set_reliability_attributes(_rel_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestHardware) _set_attributes should return a 0 error code on success
        """

        _all_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                       'Comp Ref Des', 0.0, 0.0, 0.0, 'Description',
                       100.0, 0, 0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0,
                       'Name', 'NSN', 0, 'Page #', 0, 0, 'Part #', 1,
                       'Ref Des', 1.0, 0, 'Remarks', 0.0, 'Spec #', 0,
                       30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0,
                       0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, '', 0.0, 0.0,
                       0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_get_base_attributes(self):
        """
        (TestHardware) _get_base_attributes should return a tuple of attribute values
        """

        _base_values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0,
                        0, 0, '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0,
                        '', 1, '', 1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0,
                        2014)

        self.assertEqual(self.DUT._get_base_attributes(), _base_values)

    @attr(all=True, unit=True)
    def test_get_stress_attributes(self):
        """
        (TestHardware) _get_stress_attributes should return a tuple of attribute values
        """

        _stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0,
                          1.0, 1.0, 0.0, 1.0)

        self.assertEqual(self.DUT._get_stress_attributes(), _stress_values)

    @attr(all=True, unit=True)
    def test_get_reliability_attributes(self):
        """
        (TestHardware) _get_reliability_attributes should return a tuple of attribute values
        """

        _rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0)

        self.assertEqual(self.DUT._get_reliability_attributes(), _rel_values)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestHardware) get_attributes should return a tuple of attribute values
        """

        _all_values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0,
                       0, '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1,
                       '', 1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0,
                       0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0)

        self.assertEqual(self.DUT.get_attributes(), _all_values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestHardware) get_attributes(set_attributes(values)) == values
        """

        _all_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                       'Comp Ref Des', 0.0, 0.0, 0.0, 'Description',
                       100.0, 0, 0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0,
                       'Name', 'NSN', 0, 'Page #', 0, 0, 'Part #', 1,
                       'Ref Des', 1.0, 0, 'Remarks', 0.0, 'Spec #', 0,
                       30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0,
                       0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, '', 0.0, 0.0,
                       0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0)

        self.DUT.set_attributes(_all_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _all_values)

    @attr(all=True, unit=True)
    def test_calculate_cost(self):
        """
        (TestHardware) calculate_costs should return False on success
        """

        self.DUT.cost = 100.00
        self.DUT.hazard_rate_logistics = 0.00005132
        self.DUT.mission_time = 10.0

        self.assertFalse(self.DUT._calculate_costs(self.DUT))
        self.assertEqual(self.DUT.cost_failure, 194855.80670303974)
        self.assertEqual(self.DUT.cost_hour, 10.0)
