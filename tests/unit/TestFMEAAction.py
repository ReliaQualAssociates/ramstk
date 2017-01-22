#!/usr/bin/env python -O
"""
This is the test class for testing the Action class.
"""

# -*- coding: utf-8 -*-
#
#       rtk.tests.fmea.TestAction.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from analyses.fmea.Action import Model, Action

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2015 Andrew "weibullguy" Rowland'


class TestActionModel(unittest.TestCase):
    """
    Class for testing the Action model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Action model class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_action_create(self):
        """
        (TestAction) __init__ should return instance of Action data model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.mode_id, 0)
        self.assertEqual(self.DUT.mechanism_id, 0)
        self.assertEqual(self.DUT.cause_id, 0)
        self.assertEqual(self.DUT.action_id, 0)
        self.assertEqual(self.DUT.action_recommended, '')
        self.assertEqual(self.DUT.action_category, 0)
        self.assertEqual(self.DUT.action_owner, 0)
        self.assertEqual(self.DUT.action_due_date, 0)
        self.assertEqual(self.DUT.action_status, 0)
        self.assertEqual(self.DUT.action_taken, '')
        self.assertEqual(self.DUT.action_approved, 0)
        self.assertEqual(self.DUT.action_approved_date, 0)
        self.assertEqual(self.DUT.action_closed, 0)
        self.assertEqual(self.DUT.action_closed_date, 0)

    @attr(all=True, unit=True)
    def test_set_good_attributes(self):
        """
        (TestAction) set_attributes should return 0 with good inputs
        """

        _values = (0, 0, 0, 0, 'Test Recommended Action', 0, 0, 0, 0,
                   'Test Action Taken', 0, 0, 0, 0)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestAction) set_attributes should return 40 with missing input(s)
        """

        _values = (0, 0, 0, 0, 'Test Recommended Action', 0, 0, 0, 0,
                   'Test Action Taken', 0, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestAction) set_attributes should return 10 with wrong data type
        """

        _values = (0, 0, 0, None, 'Test Recommended Action', 0, 0, 0, 0,
                   'Test Action Taken', 0, 0, 0, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_value(self):
        """
        (TestAction) set_attributes should return 10 with bad value
        """

        _values = (0, 0, 0, 'Test Recommended Action', 0, 0, 0, 0, 0,
                   'Test Action Taken', 0, 0, 0, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestAction) get_attributes should return good values
        """

        _values = (0, 0, 0, 0, '', 0, 0, 0, 0, '', 0, 0, 0, 0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestAction) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 0, 0, 0, 'Test Recommended Action', 0, 0, 0, 0,
                   'Test Action Taken', 0, 0, 0, 0)

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)


class TestActionController(unittest.TestCase):
    """
    Class for testing the FMEA Action data controller.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Action model class.
        """

        self.DUT = Action()

    @attr(all=True, unit=True)
    def test_action_create(self):
        """
        (TestAction) __init__ should return instance of Action data controller
        """

        self.assertTrue(isinstance(self.DUT, Action))
