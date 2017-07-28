#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestHardware.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing Hardware module algorithms and models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from hardware.Hardware import Model

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestHardwareModel(unittest.TestCase):
    """
    Class for testing the Hardware data model class.
    """

    _general_values = (0, 1, u'Alt Part #', u'Attachments', u'CAGE Code',
                       100, u'Comp Ref Des', 0.0, 0.0, 0.0, 0, u'Description',
                       100.0, u'Figure #', u'LCN', 0, 0, 100.0, u'Name',
                       u'NSN', u'Page #', 0, 0, u'Part #', 1, u'Ref Des',
                       u'Remarks', 0, u'Spec #', 102, 0, 0, 0.0, 2017)

    _stress_values = (0, 0, 0, u'Reason', 30.0, 25.0)

    _rel_values = (1.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.00193413,
                   2.84319e-09, 0.00193413, 1, 0.0, u'', 0.0, 0.0, 0.0, 2, 0.0,
                   0.0, 0.0, 0.0, 0.0, 517.028792, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1.0, 0, 1.0, 0, 0.980845, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   u'', u'', u'', u'', u'')

    def setUp(self):
        """
        Setup the test fixture for the Hardware class.
        """

        self.DUT = Model()

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)
        self.DUT.dao = self._dao

    @attr(all=True, static=True)
    def test00_create(self):
        """
        (TestHardware) __init__ should return a Hardware model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.user_float,
                         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.assertEqual(self.DUT.user_int, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(self.DUT.user_varchar, ['', '', '', '', ''])

        self.assertEqual(self.DUT.dao, self._dao)
        
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.hardware_id, None)
        self.assertEqual(self.DUT.alt_part_number, '')
        self.assertEqual(self.DUT.attachments, '')
        self.assertEqual(self.DUT.cage_code, '')
        self.assertEqual(self.DUT.comp_ref_des, '')
        self.assertEqual(self.DUT.cost, 0.0)
        self.assertEqual(self.DUT.cost_failure, 0.0)
        self.assertEqual(self.DUT.cost_hour, 0.0)
        self.assertEqual(self.DUT.cost_type_id, 0)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.duty_cycle, 100.0)
        self.assertEqual(self.DUT.figure_number, '')
        self.assertEqual(self.DUT.lcn, '')
        self.assertEqual(self.DUT.level, 0)
        self.assertEqual(self.DUT.manufacturer_id, 0)
        self.assertEqual(self.DUT.mission_time, 100.0)
        self.assertEqual(self.DUT.name, '')
        self.assertEqual(self.DUT.nsn, '')
        self.assertEqual(self.DUT.overstress, 0)
        self.assertEqual(self.DUT.page_number, '')
        self.assertEqual(self.DUT.parent_id, None)
        self.assertEqual(self.DUT.part, 0)
        self.assertEqual(self.DUT.part_number, '')
        self.assertEqual(self.DUT.quantity, 1)
        self.assertEqual(self.DUT.ref_des, '')
        self.assertEqual(self.DUT.reliability_goal, 1.0)
        self.assertEqual(self.DUT.reliability_goal_measure_id, 0)
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.specification_number, '')
        self.assertEqual(self.DUT.tagged_part, 0)
        self.assertEqual(self.DUT.year_of_manufacture, 2017)

        self.assertEqual(self.DUT.quality_id, 0)

        self.assertEqual(self.DUT.environment_active_id, 0)
        self.assertEqual(self.DUT.environment_dormant_id, 0)
        self.assertEqual(self.DUT.overstress, 0)
        self.assertEqual(self.DUT.reason, '')
        self.assertEqual(self.DUT.temperature_active, 30.0)
        self.assertEqual(self.DUT.temperature_dormant, 25.0)

        self.assertEqual(self.DUT.add_adj_factor, 0.0)
        self.assertEqual(self.DUT.availability_logistics, 1.0)
        self.assertEqual(self.DUT.availability_mission, 1.0)
        self.assertEqual(self.DUT.avail_log_variance, 0.0)
        self.assertEqual(self.DUT.avail_mis_variance, 0.0)
        self.assertEqual(self.DUT.failure_distribution_id, 0)
        self.assertEqual(self.DUT.scale_parameter, 0.0)
        self.assertEqual(self.DUT.shape_parameter, 0.0)
        self.assertEqual(self.DUT.location_parameter, 0.0)
        self.assertEqual(self.DUT.hazard_rate_active, 0.0)
        self.assertEqual(self.DUT.hazard_rate_dormant, 0.0)
        self.assertEqual(self.DUT.hazard_rate_logistics, 0.0)
        self.assertEqual(self.DUT.hazard_rate_method_id, 0)
        self.assertEqual(self.DUT.hazard_rate_mission, 0.0)
        self.assertEqual(self.DUT.hazard_rate_model, {})
        self.assertEqual(self.DUT.hazard_rate_percent, 0.0)
        self.assertEqual(self.DUT.hazard_rate_software, 0.0)
        self.assertEqual(self.DUT.hazard_rate_specified, 0.0)
        self.assertEqual(self.DUT.hazard_rate_type_id, 0)
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
        self.assertEqual(self.DUT.survival_analysis_id, 0)

    @attr(all=True, static=True)
    def test02_set_general_attributes(self):
        """
        (TestHardware) _set_general_attributes should return a 0 error code on success
        """

        (_error_code,
         _error_msg) = self.DUT._set_general_attributes(self._general_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(_error_msg, '')

    @attr(all=True, static=True)
    def test03_set_general_attributes_wrong_type(self):
        """
        (TestHardware) _set_general_attributes should return a 10 error code when passed a wrong data type
        """

        _general_values = (0, 1, 'Alt Part #', 'Attachments', 'CAGE Code',
                           100, 'Comp Ref Des', 0.0, 0.0, 0.0, 0, 'Description',
                           100.0, 'Figure #', 'LCN', 0, 0, 100.0, 'Name',
                           'NSN', 'Page #', 0, 0, 'Part #', 1, 'Ref Des',
                           'Remarks', 0, 'Spec #', 102, 0, 0, None, 2017)

        (_error_code,
         _error_msg) = self.DUT._set_general_attributes(_general_values)
        self.assertEqual(_error_code, 10)
        self.assertEqual(_error_msg,
                         "ERROR: Hardware._set_general_attributes(): Converting one or more general inputs to the correct data type.")

    @attr(all=True, static=True)
    def test04_set_general_attributes_missing_index(self):
        """
        (TestHardware) _set_general_attributes should return a 40 error code when too few items are passed
        """

        _general_values = (0, 1, 'Alt Part #', 'Attachments', 'CAGE Code',
                           100, 'Comp Ref Des', 0.0, 0.0, 0.0, 0,
                           'Description', 100.0, 'Figure #', 'LCN', 0, 0,
                           100.0, 'Name', 'NSN', 'Page #', 0, 0, 'Part #', 1,
                           'Ref Des', 'Remarks', 0, 'Spec #', 102, 0, 0.0,
                           2017)

        (_error_code,
         _error_msg) = self.DUT._set_general_attributes(_general_values)
        self.assertEqual(_error_code, 40)
        self.assertEqual(_error_msg,
                         "ERROR: Hardware._set_general_attributes(): Insufficient number of general input values.  Require 34 only 33 were passed.")

    @attr(all=True, static=True)
    def test05_set_stress_attributes(self):
        """
        (TestHardware) _set_stress_attributes should return a 0 error code on success
        """

        (_error_code,
         _error_msg) = self.DUT._set_stress_attributes(self._stress_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(_error_msg, '')

    @attr(all=True, static=True)
    def test06_set_stress_attributes_wrong_type(self):
        """
        (TestHardware) _set_stress_attributes should return a 10 error code when passed a wrong data type
        """

        _stress_values = (0, 1, 2, 'Reason', None, 23.0)

        (_error_code,
         _error_msg) = self.DUT._set_stress_attributes(_stress_values)
        self.assertEqual(_error_code, 10)
        self.assertEqual(_error_msg, 'ERROR: Hardware._set_stress_attributes: Converting one or more stress inputs to the correct data type.')

    @attr(all=True, static=True)
    def test07_set_stress_attributes_missing_index(self):
        """
        (TestHardware) _set_stress_attributes should return a 40 error code when too few items are passed
        """

        _stress_values = (0, 1, 2, 'Reason', 23.0)

        (_error_code,
         _error_msg) = self.DUT._set_stress_attributes(_stress_values)
        self.assertEqual(_error_code, 40)
        self.assertEqual(_error_msg, 'ERROR: Hardware._set_stress_attributes: Insufficient stress input values.  Require six, only 5 were passed.')

    @attr(all=True, static=True)
    def test08_set_reliability_attributes(self):
        """
        (TestHardware) _set_reliability_attributes should return a 0 error code on success
        """

        (_error_code,
         _error_msg) = self.DUT._set_reliability_attributes(self._rel_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(_error_msg, '')

    @attr(all=True, static=True)
    def test09_set_reliability_attributes_wrong_type(self):
        """
        (TestHardware) _set_reliability_attributes should return a 10 error code when passed a wrong data type
        """

        _rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, None, 0.0, 0.0, 1.0, 0, 1.0, 0, 1.0, 1.0,
                       0.0, 0.0, 0, 0.0)

        (_error_code,
         _error_msg) = self.DUT._set_reliability_attributes(_rel_values)
        self.assertEqual(_error_code, 10)
        self.assertEqual(_error_msg, 'ERROR: Hardware._set_reliability_attributes: Converting one or more reliability inputs to the correct data type.')

    @attr(all=True, static=True)
    def test10_set_reliability_attributes_missing_index(self):
        """
        (TestHardware) _set_reliability_attributes should return a 40 error code when too few items are passed
        """

        _rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0, 1.0, 0, 1.0, 1.0,
                       0.0, 0.0, 0, 0.0)

        (_error_code,
         _error_msg) = self.DUT._set_reliability_attributes(_rel_values)
        self.assertEqual(_error_code, 40)
        self.assertEqual(_error_msg, 'ERROR: Hardware._set_reliability_attributess: Insufficient reliability input values.  Require 39 only 38 were passed.')

    @attr(all=True, static=True)
    def test11_set_user_attributes(self):
        """
        (TestHardware) set_user_attributes should return a 0 error code on success
        """

        _user_values = (0.0, 1.0, 2.0, 30.0, 440.0, 5, 6, 7.0, 8.0, 99.0, 10.0,
                        11, 12, 13.0, 14, 15.0, 16.0, 17.0, 18, 19.0, 0.0, 1.0, 2,
                        3, 440.0, 50, 60, 7.0, 80.0, 90, 'Zero', 'One', 'Two',
                        'Three', '4')

        (_error_code,
         _error_msg) = self.DUT._set_user_attributes(_user_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, static=True)
    def test12_set_user_attributes_wrong_type(self):
        """
        (TestHardware) set_user_attributes should return a 10 error code when passed a wrong data type
        """

        _user_values = (0.0, 1.0, 2.0, 30.0, 440.0, 5, 6, 7.0, 8.0, 99.0, 10.0,
                        11, 12, None, 14, 15.0, 16.0, 17.0, 18, 19.0, 0.0, 1.0, 2,
                        3, 440.0, 50, 60, 7.0, 80.0, 90, 'Zero', 'One', 'Two',
                        'Three', '4')

        (_error_code,
         _error_msg) = self.DUT._set_user_attributes(_user_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, static=True)
    def test13_set_user_attributes_missing_index(self):
        """
        (TestHardware) set_user_attributes should return a 40 error code when too few items are passed
        """

        _user_values = (0.0, 1.0, 2.0, 30.0, 440.0, 5, 6, 7.0, 8.0, 99.0, 10.0,
                        11, 12, 13.0, 14, 15.0, 16.0, 17.0, 18, 19.0, 0.0, 1.0, 2,
                        3, 440.0, 50, 60, 7.0, 80.0, 90, 'Zero', 'One', 'Two',
                        'Three')

        (_error_code,
         _error_msg) = self.DUT._set_user_attributes(_user_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, static=True)
    def test14_set_attributes(self):
        """
        (TestHardware) set_attributes should return a 0 error code on success
        """

        _all_values = self._general_values + self._stress_values + \
                      self._rel_values # + self._user_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)

        self.assertEqual(_error_code[0], 0)
        self.assertEqual(_error_code[1], 0)
        self.assertEqual(_error_code[2], 0)

    @attr(all=True, dynamic=True)
    def test15_get_general_attributes(self):
        """
        (TestHardware) _get_general_attributes should return a tuple of attribute values on success
        """

        _general_values = (0, 2, u'', u'', u'', 0, u'', 0.0, 0.0, 0.0, 2, u'',
                           100.0, u'', u'', 1, 0, 10.0, u'Sub-System 1', u'',
                           u'', 1, 0, u'', 1, u'SS1', u'None', 0,
                           u'Specification', 0, 0, 0, 0.0, 2014)

        self.DUT.hardware_id = 2

        self.assertEqual(self.DUT._get_general_attributes(), _general_values)

    @attr(all=True, dynamic=True)
    def test16_get_stress_attributes(self):
        """
        (TestHardware) _get_stress_attributes should return a tuple of attribute values on success
        """

        _stress_values = (0, 0, 0, u'Reason', 30.0, 25.0)

        self.DUT.hardware_id = 2

        self.assertEqual(self.DUT._get_stress_attributes(), _stress_values)

    @attr(all=True, dynamic=True)
    def test17_get_reliability_attributes(self):
        """
        (TestHardware) _get_reliability_attributes should return a tuple of attribute values on success
        """

        _rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.00193411,
                       0.0, 0.00193411, 1, 0.0, 0.0, 0.0, 0.0, 1, 0.0, 0.0,
                       0.0, 0.0, 0.0, 517.033352, 0.0, 0.0, 0.0, 0.0, 0.0,
                       1.0, 0, 1.0, 0, 0.980845, 1.0, 0.0, 0.0, 0, 0.0)

        self.DUT.hardware_id = 2

        self.assertEqual(self.DUT._get_reliability_attributes(), _rel_values)

    @attr(all=True, dynamic=True)
    def test18_get_attributes(self):
        """
        (TestHardware) get_attributes should return a tuple of attribute values on success
        """

        _all_values = (0, 2, u'', u'', u'', 0, u'', 0.0, 0.0, 0.0, 2, u'',
                       100.0, u'', u'', 1, 0, 10.0, u'Sub-System 1', u'', u'',
                       1, 0, u'', 1, u'SS1', u'None', 0, u'Specification', 0,
                       0, 0, 0.0, 2014, 0, 0, 0, u'Reason', 30.0, 25.0, 0.0,
                       1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.00193411, 0.0,
                       0.00193411, 1, 0.0, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0,
                       0.0, 0.0, 517.033352, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0,
                       1.0, 0, 0.980845, 1.0, 0.0, 0.0, 0, 0.0)

        self.DUT.hardware_id = 2

        self.assertEqual(self.DUT.get_attributes(), _all_values)

    @attr(all=False, static=False)
    def test19_attribute_sanity(self):
        """
        (TestHardware) get_attributes(set_attributes(values)) == values
        """

        _base_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                        'Comp Ref Des', 0.0, 0.0, 0.0, 'Description',
                        100.0, 0, 0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0,
                        'Name', 'NSN', 0, 'Page #', 0, 0, 'Part #', 1,
                        'Ref Des', 1.0, 0, 'Remarks', 0.0, 'Spec #', 0,
                        30.0, 30.0, 0.0, 2014, 0, 0, 0, 0.0, 0, 0)
        _stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                          0.0, 1.0, 30.0, 25.0, 0.0, 25.0, '')
        _rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0)
        #_user_values = (0.0, 1.0, 2.0, 30.0, 440.0, 5, 6, 7.0, 8.0, 99.0, 10.0,
        #                11, 12, 13.0, 14, 15.0, 16.0, 17.0, 18, 19.0, 0.0, 1.0,
        #                2, 3, 440.0, 50, 60, 7.0, 80.0, 90, 'Zero', 'One',
        #                'Two', 'Three', '4')

        _all_values = _base_values + _stress_values + _rel_values # + _user_values

        self.DUT.set_attributes(_all_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result[:38], _base_values[:38])
        self.assertEqual(_result[38:50], _stress_values[:12])
        self.assertEqual(_result[50], _stress_values[16])
        self.assertEqual(_result[51:], _rel_values)

    @attr(all=True, static=True)
    def test20_calculate_reliability(self):
        """
        (TestHardware) calculate_reliability should return a 0 error code and empty message on success
        """

        self.DUT.hazard_rate_method_id = 1
        self.DUT.hazard_rate_active = 0.00005632
        self.DUT.hazard_rate_dormant = 0.00000289
        self.DUT.hazard_rate_software = 0.0000003341

        (_code, _msg) = self.DUT.calculate_reliability()
        self.assertEqual(_code, 0)
        self.assertEqual(_msg, '')
        self.assertAlmostEqual(self.DUT.hazard_rate_logistics, 5.95441e-05)
        self.assertAlmostEqual(self.DUT.mtbf_logistics, 16794.2751675)
        self.assertAlmostEqual(self.DUT.reliability_logistics, 0.9940633)
        self.assertAlmostEqual(self.DUT.hazard_rate_mission, 5.95441e-05)
        self.assertAlmostEqual(self.DUT.reliability_mission, 0.9940633)

        self.assertAlmostEqual(self.DUT.hr_active_variance, 3.1719424e-09)
        self.assertAlmostEqual(self.DUT.hr_dormant_variance, 8.3521e-12)

    @attr(all=True, static=True)
    def test21_calculate_reliability_zero_division(self):
        """
        (TestHardware) calculate_reliability should return a 10 error code when encountering a ZeroDivisionError
        """

        self.DUT.hazard_rate_method_id = 1
        self.DUT.hazard_rate_active = 0.0
        self.DUT.hazard_rate_dormant = 0.0
        self.DUT.hazard_rate_software = 0.0

        (_code, _msg) = self.DUT.calculate_reliability()
        self.assertEqual(_code, 10)
        self.assertEqual(_msg, 'ERROR: Hardware._calculate_reliability(): Zero division error when calculating logistics MTBF.  Active hazard rate = 0.000000, dormant hazard rate = 0.000000, software hazard rate = 0.000000.')

    @attr(all=True, static=True)
    def test22_calculate_cost(self):
        """
        (TestHardware) calculate_costs should return a 0 error code and empty message on success
        """

        self.DUT.cost = 100.00
        self.DUT.hazard_rate_logistics = 0.00005132
        self.DUT.mission_time = 100.0

        (_code, _msg) = self.DUT.calculate_costs()
        self.assertEqual(_code, 0)
        self.assertEqual(_msg, '')
        self.assertAlmostEqual(self.DUT.cost_failure, 19485.5806703)
        self.assertEqual(self.DUT.cost_hour, 1.0)

    @attr(all=True, static=True)
    def test23_calculate_cost_zero_division_cost_per_failure(self):
        """
        (TestHardware) calculate_costs should return a 10 error code and non-empty message when encountering a ZeroDivisionError calculating cost/failure
        """

        self.DUT.cost = 100.00
        self.DUT.hazard_rate_logistics = 0.0
        self.DUT.mission_time = 100.0

        (_code, _msg) = self.DUT.calculate_costs()
        self.assertEqual(_code, 10)
        self.assertEqual(_msg, 'ERROR: Hardware._calculate_cost(): Zero division error when calculating cost per failure.  Logistics hazard rate = 0.000000, mission time = 100.000000.')

    @attr(all=True, static=True)
    def test24_calculate_cost_zero_division_cost_per_hour(self):
        """
        (TestHardware) calculate_costs should return a 10 error code and non-empty message when encountering a ZeroDivisionError calculating cost/hour
        """

        self.DUT.cost = 100.00
        self.DUT.hazard_rate_logistics = 0.00005132
        self.DUT.mission_time = 0.0

        (_code, _msg) = self.DUT.calculate_costs()
        self.assertEqual(_code, 10)
        self.assertEqual(_msg, 'ERROR: Hardware._calculate_cost(): Zero division error when calculating cost per hour.  Mission time = 0.000000.')

    @attr(all=True, static=True)
    def test25_calculate(self):
        """
        (TestHardware) calculate should return a list of 0 error codes and empty message on success
        """

        self.DUT.cost = 100.00
        self.DUT.hazard_rate_method_id = 1
        self.DUT.hazard_rate_active = 0.00005632
        self.DUT.hazard_rate_dormant = 0.00000289
        self.DUT.hazard_rate_software = 0.0000003341
        self.DUT.mission_time = 100.0

        (_code, _msg) = self.DUT.calculate()
        self.assertEqual(_code[0], 0)
        self.assertEqual(_msg[0], '')
        self.assertEqual(_code[2], 0)
        self.assertEqual(_msg[2], '')
        self.assertAlmostEqual(self.DUT.hazard_rate_logistics, 5.95441e-05)
        self.assertAlmostEqual(self.DUT.mtbf_logistics, 16794.2751675)
        self.assertAlmostEqual(self.DUT.reliability_logistics, 0.9940633)
        self.assertAlmostEqual(self.DUT.hazard_rate_mission, 5.95441e-05)
        self.assertAlmostEqual(self.DUT.reliability_mission, 0.9940633)

        self.assertAlmostEqual(self.DUT.hr_active_variance, 3.1719424e-09)
        self.assertAlmostEqual(self.DUT.hr_dormant_variance, 8.3521e-12)

        self.assertAlmostEqual(self.DUT.cost_failure, 16794.2751675)
        self.assertEqual(self.DUT.cost_hour, 1.0)

    @attr(all=True, dynamic=True)
    def test26_save_general_attributes(self):
        """
        (TestHardware) save_general_attributes should return a 0 error code on success
        """

        self.DUT.parent_id = 1
        self.DUT.hardware_id = 101

        _error_code = self.DUT.save_general_attributes()
        self.assertEqual(_error_code, 0)

    @attr(all=True, dynamic=True)
    def test27_save_stress_attributes(self):
        """
        (TestHardware) save_stress_attributes should return a 0 error code on success
        """

        self.DUT.hardware_id = 101
        self.environment_active_id = 2
        self.environment_dormant_id = 3
        self.overstress = 0
        self.reason = ''
        self.temperature_active = 36.2
        self.temperature_dormant = 23.0

        _error_code = self.DUT.save_stress_attributes()
        self.assertEqual(_error_code, 0)

    @attr(all=True, dynamic=True)
    def test28_save_reliability_attributes(self):
        """
        (TestHardware) save_reliability_attributes should return a 0 error code on success
        """

        self.DUT.hardware_id = 101

        _error_code = self.DUT.save_reliability_attributes()
        self.assertEqual(_error_code, 0)

    @attr(all=True, dynamic=True)
    def test29_save_attributes(self):
        """
        (TestHardware) save_attributes should return a list of 0 error code on success
        """

        self.DUT.parent_id = 1
        self.DUT.hardware_id = 101
        self.environment_active_id = 2
        self.environment_dormant_id = 3
        self.overstress = 0
        self.reason = ''
        self.temperature_active = 36.2
        self.temperature_dormant = 23.0

        _error_code = self.DUT.save_attributes()
        self.assertEqual(_error_code[0], 0)
        self.assertEqual(_error_code[1], 0)
        self.assertEqual(_error_code[2], 0)

    @attr(all=True, dynamic=True)
    def test30_add_hardware(self):
        """
        (TestHardware) add_hardware should return a 0 error code on success
        """

        (_error_code,
         _msg,
         _item_id) = self.DUT.add_hardware(0, self._dao, 0, 0)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'SUCCESS: Hardware.add_hardware: Succesfully added a Hardware record to the RTK Program database.')
        self.assertEqual(_item_id, 116)

    @attr(all=True, dynamic=True)
    def test31_add_hardware_foreign_key_error(self):
        """
        (TestHardware) add_hardware should return a 787 error code when there is a foreign key constraint failure
        """

        (_error_code,
         _msg,
         _item_id) = self.DUT.add_hardware(-1, self._dao, 0, 0)

        self.assertEqual(_error_code, 787)
        self.assertEqual(_msg, 'ERROR: Hardware.add_hardware(): Failed to add new record to table rtk_stress.  Database returned error code: 787')
        self.assertEqual(_item_id, -1)

    @attr(all=True, dynamic=True)
    def test32_remove_hardware(self):
        """
        (TestHardware) remove_hardware should return a 0 error code on success
        """

        (_error_code,
         _msg) = self.DUT.remove_hardware(116, self._dao)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'SUCCESS: Hardware.remove_hardware(): Succesfully removed record hardware_id=116 and all child records from the RTK Program database.')
