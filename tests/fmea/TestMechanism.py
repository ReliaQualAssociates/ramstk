#!/usr/bin/env python -O
"""
This is the test class for testing the FMEA failure Mechanism class.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestFMEAMechanism.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from analyses.fmea.Mechanism import Model, Mechanism, OutOfRangeError

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestMechanismModel(unittest.TestCase):
    """
    Class for testing the Mechanism model class.
    """

    def setUp(self):
        """
        Setups the test fixture for the Mechanism model class.
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
        (TestMechanism) set_attributes should return 10 with bad value
        """

        _values = (0, 0, 10, 'Test Mechanism', 10, 1000, 10, 10, 1000, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

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

    #@attr(all=False, unit=False)
    #def test_rpn(self):
    #    """
    #    (TestMechanism) calculate always returns a value between 1 - 1000
    #    """

    #    for severity in range(1, 11):
    #        for occurrence in range(1, 11):
    #            for detection in range(1, 11):
    #                self.assertIn(self.DUT.calculate(severity,
    #                                                 occurrence,
    #                                                 detection),
    #                              range(1, 1001))

    @attr(all=True, unit=True)
    def test_rpn_out_of_range_severity_inputs(self):
        """
        (TestMechanism) calculate raises OutOfRangeError for 11 < severity inputs < 0
        """

        self.assertRaises(OutOfRangeError, self.DUT.calculate, 0, 1)
        self.assertRaises(OutOfRangeError, self.DUT.calculate, 11, 1)
        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 0)
        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 11)

    @attr(all=True, unit=True)
    def test_rpn_out_of_range_occurrence_inputs(self):
        """
        (TestMechanism) calculate raises OutOfRangeError for 11 < occurrence inputs < 0
        """

        self.DUT.rpn_occurrence = 0
        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 1)
        self.DUT.rpn_occurrence = 11
        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 1)

    @attr(all=True, unit=True)
    def test_rpn_out_of_range_new_occurrence_inputs(self):
        """
        (TestMechanism) calculate raises OutOfRangeError for 11 < new occurrence inputs < 0
        """

        self.DUT.rpn_occurrence_new = 0
        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 1)
        self.DUT.rpn_occurrence_new = 11
        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 1)

    @attr(all=True, unit=True)
    def test_rpn_out_of_range_detection_inputs(self):
        """
        (TestMechanism) calculate raises OutOfRangeError for 11 < detection inputs < 0
        """

        self.DUT.rpn_detection = 0
        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 10)
        self.DUT.rpn_detection = 11
        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 10)

    @attr(all=True, unit=True)
    def test_rpn_out_of_range_new_detection_inputs(self):
        """
        (TestMechanism) calculate raises OutOfRangeError for 11 < new detection inputs < 0
        """

        self.DUT.rpn_detection_new = 0
        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 10)
        self.DUT.rpn_detection_new = 11
        self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 10)


class TestMechanismController(unittest.TestCase):
    """
    Class for testing the FMEA Mechanism data controller.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Mechanism model class.
        """

        self.DUT = Mechanism()

    @attr(all=True, unit=True)
    def test_mechanism_create(self):
        """
        (TestMechanism) __init__ should return instance of Mechanism data controller
        """

        self.assertTrue(isinstance(self.DUT, Mechanism))
