#!/usr/bin/env python -O
"""
This is the test class for testing the Mechanism class.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       TestMechanism.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

# We add this to ensure the imports within the rtk packages will work.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao

from fmea.Mechanism import *


class TestMechanismModel(unittest.TestCase):
    """
    Class for testing the Mechanism model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Mechanism model class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_mechanism_create(self):
        """
        (TestMechanism) __init__ should return instance of Mechanism data model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.mode_id, 0)
        self.assertEqual(self.DUT.mechanism_id, 0)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.rpn_occurrence, 10)
        self.assertEqual(self.DUT.rpn_detection, 10)
        self.assertEqual(self.DUT.rpn, 1000)
        self.assertEqual(self.DUT.rpn_occurrence_new, 10)
        self.assertEqual(self.DUT.rpn_detection_new, 10)
        self.assertEqual(self.DUT.rpn_new, 1000)
        self.assertEqual(self.DUT.include_pof, 0)

    @attr(all=True, unit=True)
    def test_set_good_attributes(self):
        """
        (TestMechanism) set_attributes should return 0 with good inputs
        """

        _values = (0, 0, 'Test Mechanism', 10, 10, 1000, 10, 10, 1000, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestMechanism) set_attributes should return 40 with missing input(s)
        """

        _values = (0, 0, 'Test Mechanism', 10, 10, 1000, 10, 10, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestMechanism) set_attributes should return 10 with wrong data type
        """

        _values = (0, 0, 'Test Mechanism', 10, None, 1000, 10, 10, 1000, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_value(self):
        """
        (TestMechanism) set_attributes should return 50 with bad value
        """

        _values = (0, 0, 10, 'Test Mechanism', 10, 1000, 10, 10, 1000, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 50)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestMechanism) get_attributes should return good values
        """

        _values = (0, 0, '', 10, 10, 1000, 10, 10, 1000, 0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestMechanism) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 0, 'Test Mechanism', 10, 10, 1000, 10, 10, 1000, 0)

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)

    @attr(all=True, unit=True)
    def test_rpn(self):
        """
        (TestMechanism) calculate always returns a value between 1 - 1000
        """

        for severity in range(1, 11):
            for occurrence in range(1, 11):
                for detection in range(1, 11):
                    self.assertIn(self.DUT.calculate(severity,
                                                     occurrence,
                                                     detection),
                                  range(1, 1001))

    @attr(all=True, unit=True)
    def test_rpn_out_of_range_inputs(self):
        """
        (TestMechanism) calculate raises OutOfRangeError for 10 < input < 1
        """

        self.assertRaises(OutOfRangeError, self.DUT.calculate, 0, 1, 1)
        self.assertRaises(OutOfRangeError, self.DUT.calculate, 11, 1, 1)
        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 0, 1)
        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 11, 1)
        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 1, 0)
        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 1, 11)
