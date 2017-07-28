#!/usr/bin/env python -O
"""
This is the test class for testing Validation module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestValidation.py is part of The RTK Project
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
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from validation.Validation import Model, Validation

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestValidationModel(unittest.TestCase):
    """
    Class for testing the Validation data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Validation class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestValidation) __init__ should return a Validation model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.revision_id, 0)
        self.assertEqual(self.DUT.validation_id, 0)
        self.assertEqual(self.DUT.task_description, '')
        self.assertEqual(self.DUT.task_type, 0)
        self.assertEqual(self.DUT.task_specification, '')
        self.assertEqual(self.DUT.measurement_unit, 0)
        self.assertEqual(self.DUT.min_acceptable, 0.0)
        self.assertEqual(self.DUT.mean_acceptable, 0.0)
        self.assertEqual(self.DUT.max_acceptable, 0.0)
        self.assertEqual(self.DUT.variance_acceptable, 0.0)
        self.assertEqual(self.DUT.start_date, 719163)
        self.assertEqual(self.DUT.end_date, 719163)
        self.assertEqual(self.DUT.status, 0.0)
        self.assertEqual(self.DUT.minimum_time, 0.0)
        self.assertEqual(self.DUT.average_time, 0.0)
        self.assertEqual(self.DUT.maximum_time, 0.0)
        self.assertEqual(self.DUT.mean_time, 0.0)
        self.assertEqual(self.DUT.time_variance, 0.0)
        self.assertEqual(self.DUT.minimum_cost, 0.0)
        self.assertEqual(self.DUT.average_cost, 0.0)
        self.assertEqual(self.DUT.maximum_cost, 0.0)
        self.assertEqual(self.DUT.mean_cost, 0.0)
        self.assertEqual(self.DUT.cost_variance, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestValidation) set_attributes should return a 0 error code on success
        """

        _values = (0, 0, 'Description', 0, 'Specification', 0, 0.0, 0.0,
                   0.0, 0.0, 719163, 719163, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 95.0)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestValidation) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (0, 0, 'Description', 0, 'Specification', 0, 0.0, 0.0,
                   0.0, 0.0, 719163, 'Date', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 95.0)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestValidation) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 0, 'Description', 0, 'Specification', 0, 0.0, 0.0,
                   0.0, 0.0, 719163, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 95.0)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestValidation) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (0, 0, '', 0, '', 0, 0.0, 0.0, 0.0, 0.0, 719163,
                          719163, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 95.0))

    @attr(all=True, unit=True)
    def test_calculate_task_time(self):
        """
        (TestValidation) calculate returns False on successfully calculating tasks times
        """

        self.DUT.minimum_time = 25.2
        self.DUT.average_time = 36.8
        self.DUT.maximum_time = 44.1

        self.assertFalse(self.DUT.calculate())
        self.assertAlmostEqual(self.DUT.mean_time, 36.08333333)
        self.assertAlmostEqual(self.DUT.time_variance, 9.9225)

    @attr(all=True, unit=True)
    def test_calculate_task_cost(self):
        """
        (TestValidation) calculate returns False on successfully calculating tasks costs
        """

        self.DUT.minimum_cost = 252.00
        self.DUT.average_cost = 368.00
        self.DUT.maximum_cost = 441.00
        self.DUT.confidence = 0.95

        self.assertFalse(self.DUT.calculate())
        self.assertAlmostEqual(self.DUT.mean_cost, 360.83333333)
        self.assertAlmostEqual(self.DUT.cost_variance, 992.25)


class TestValidationController(unittest.TestCase):
    """
    Class for testing the Validation data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Validation class.
        """

        self.DUT = Validation()

    @attr(all=True, unit=True)
    def test_controller_create(self):
        """
        (TestValidation) __init__ should create a Validation data controller
        """

        self.assertTrue(isinstance(self.DUT, Validation))
        self.assertEqual(self.DUT._dao, None)
        self.assertEqual(self.DUT._last_id, None)
        self.assertEqual(self.DUT.dicTasks, {})
        self.assertEqual(self.DUT.dicStatus, {})
