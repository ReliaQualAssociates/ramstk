#!/usr/bin/env python -O
"""
This is the test class for testing the Mode class.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestFMEAMode.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from analyses.fmea.Mode import Model, Mode, OutOfRangeError

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2016 Andrew "weibullguy" Rowland'


class TestFMEAModeModel(unittest.TestCase):
    """
    Class for testing the Mode model class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Mode model class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_mode_create(self):
        """
        (TestFMEAMode) __init__ should return instance of Mode data model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.assembly_id, 0)
        self.assertEqual(self.DUT.function_id, 0)
        self.assertEqual(self.DUT.mode_id, 0)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.mission, '')
        self.assertEqual(self.DUT.mission_phase, '')
        self.assertEqual(self.DUT.local_effect, '')
        self.assertEqual(self.DUT.next_effect, '')
        self.assertEqual(self.DUT.end_effect, '')
        self.assertEqual(self.DUT.detection_method, '')
        self.assertEqual(self.DUT.other_indications, '')
        self.assertEqual(self.DUT.isolation_method, '')
        self.assertEqual(self.DUT.design_provisions, '')
        self.assertEqual(self.DUT.operator_actions, '')
        self.assertEqual(self.DUT.severity_class, '')
        self.assertEqual(self.DUT.hazard_rate_source, '')
        self.assertEqual(self.DUT.mode_probability, '')
        self.assertEqual(self.DUT.effect_probability, 1.0)
        self.assertEqual(self.DUT.mode_ratio, 0.0)
        self.assertEqual(self.DUT.mode_hazard_rate, 0.0)
        self.assertEqual(self.DUT.mode_op_time, 0.0)
        self.assertEqual(self.DUT.mode_criticality, 0.0)
        self.assertEqual(self.DUT.rpn_severity, 10)
        self.assertEqual(self.DUT.rpn_severity_new, 10)
        self.assertEqual(self.DUT.critical_item, 0)
        self.assertEqual(self.DUT.single_point, 0)
        self.assertEqual(self.DUT.remarks, '')

    @attr(all=True, unit=True)
    def test_set_good_attributes(self):
        """
        (TestFMEAMode) set_attributes should return 0 with good inputs
        """

        _values = (0, 0, 0, 'Test Mode', 'Mission', 'Mission Phase', 'Local',
                   'Next', 'End', 'Detection Method', 'Other Indications',
                   'Isolation Method', 'Design Provisions', 'Operator Actions',
                   'Severity Class', 'Hazard Rate Source', 'Mode Probability',
                   1.0, 0.0, 0.0, 0.0, 0.0, 10, 10, 0, 0, 'Remarks')

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestFMEAMode) set_attributes should return 40 with missing input(s)
        """

        _values = (0, 0, 0, 'Test Mode', 'Mission', 'Mission Phase', 'Local',
                   'Next', 'End', 'Detection Method', 'Other Indications',
                   'Isolation Method', 'Design Provisions', 'Operator Actions',
                   'Severity Class', 'Hazard Rate Source', 'Mode Probability',
                   1.0, 0.0, 0.0, 0.0, 0.0, 10, 10, 0, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestFMEAMode) set_attributes should return 10 with wrong data type
        """

        _values = (0, 0, 0, 'Test Mode', 'Mission', 'Mission Phase', 'Local',
                   'Next', 'End', 'Detection Method', 'Other Indications',
                   'Isolation Method', 'Design Provisions', 'Operator Actions',
                   'Severity Class', 'Hazard Rate Source', 'Mode Probability',
                   1.0, 0.0, 0.0, None, 0.0, 10, 10, 0, 0, 'Remarks')

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_value(self):
        """
        (TestFMEAMode) set_attributes should return 10 with bad value
        """

        _values = (0, 0, 0, 'Test Mode', 'Mission', 'Mission Phase', 'Local',
                   'Next', 'End', 'Detection Method', 'Other Indications',
                   'Isolation Method', 'Design Provisions', 'Operator Actions',
                   'Severity Class', 'Hazard Rate Source', 'Mode Probability',
                   1.0, 0.0, 0.0, 'Remarks', 0.0, 0.0, 10, 10, 0, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestFMEAMode) get_attributes should return good values
        """

        _values = (0, 0, 0, '', '', '', '', '', '', '', '', '', '', '', '', '',
                   '', 1.0, 0.0, 0.0, 0.0, 0.0, 10, 10, 0, 0, '')

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestFMEAMode) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 0, 0, 'Test Mode', 'Mission', 'Mission Phase', 'Local',
                   'Next', 'End', 'Detection Method', 'Other Indications',
                   'Isolation Method', 'Design Provisions', 'Operator Actions',
                   'Severity Class', 'Hazard Rate Source', 'Mode Probability',
                   1.0, 0.0, 0.0, 0.0, 0.0, 10, 10, 0, 0, 'Remarks')

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)

    @attr(all=True, unit=True)
    def test_criticality(self):
        """
        (TestFMEAMode) calculate always returns a value between 0 - 1
        """

        pass

    @attr(all=False, unit=True)
    def test_criticality_out_of_range_hazard_rate_input(self):
        """
        (TestFMEAMode) calculate raises OutOfRangeError for item_hr < 0.0
        """

        self.assertRaises(OutOfRangeError, self.DUT.calculate, 0.0, 1, 1)

    @attr(all=False, unit=True)
    def test_criticality_out_of_range_ratio_input(self):
        """
        (TestFMEAMode) calculate raises OutOfRangeError for 0.0 > ratio > 1.0
        """

        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1.1, -0.1, 1)

    @attr(all=False, unit=True)
    def test_criticality_out_of_range_op_time_input(self):
        """
        (TestFMEAMode) calculate raises OutOfRangeError for 0.0 > operating time
        """

        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 0.5, -1.2)

    @attr(all=False, unit=True)
    def test_criticality_out_of_range_eff_prob_input(self):
        """
        (TestFMEAMode) calculate raises OutOfRangeError for 0.0 <= effect probability =< 1.0
        """

        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 11, 1, 2.3)

    @attr(all=False, unit=True)
    def test_criticality_out_of_range_mode_hazard_rate(self):
        """
        (TestFMEAMode) calculate raises OutOfRangeError for 0 > mode hazard rate
        """

        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, -0.5, 1)

    @attr(all=False, unit=True)
    def test_criticality_out_of_range_mode_criticaility(self):
        """
        (TestFMEAMode) calculate raises OutOfRangeError for 0 > mode criticality
        """

        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, -0.5, 1)


class TestModeController(unittest.TestCase):
    """
    Class for testing the FMEA Mode data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the FMEA Mode class.
        """

        self.DUT = Mode()

    @attr(all=True, unit=True)
    def test_controller_create(self):
        """
        (TestFMEAMode) __init__ should create a Mode data controller
        """

        self.assertTrue(isinstance(self.DUT, Mode))
