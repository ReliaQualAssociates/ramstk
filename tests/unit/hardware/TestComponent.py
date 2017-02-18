#!/usr/bin/env python -O
"""
This is the test class for testing Component module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestComponent.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from hardware.component.Component import Model, Component

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestComponentModel(unittest.TestCase):
    """
    Class for testing the Component data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Component class.
        """

        self.DUT = Model()

        self._base_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                             'Comp Ref Des', 0.0, 0.0, 0.0, 'Description',
                             100.0, 0, 0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0,
                             'Name', 'NSN', 0, 'Page #', 0, 0, 'Part #', 1,
                             'Ref Des', 1.0, 0, 'Remarks', 0.0, 'Spec #', 0,
                             30.0, 30.0, 0.0, 2014, 0, 0, 0, 0.0, 0, 0)
        self._stress_values = (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0,
                               9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, '')
        self._rel_values = (0.0, 1.0, 2.0, 3.0, 4.0, 5, 6.0, 7.0, 8.0, 9.0,
                            10.0, 11.0, 12, 13.0, {}, 15.0, 16.0, 17.0, 18,
                            19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0,
                            27.0, 28.0, 29.0, 30.0, 31.0, 32.0, 33.0, 34.0, 35)
        self._user_values = (0.0, 1.0, 2.0, 3.0, 4.0, 5, 6, 7.0, 8.0, 9.0,
                             10.0, 11, 12, 13.0, 14, 15.0, 16.0, 17.0, 18,
                             19.0, 20.0, 21.0, 22, 23, 24.0, 25, 26, 27.0,
                             28.0, 29, 'Thirty', '31', 'Thirty Two', '33',
                             '34')

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestComponent) __init__ should return an Component model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        # Properly sources the Hardware class.
        self.assertEqual(self.DUT.revision_id, None)

        # Scalar values are correct.
        self.assertEqual(self.DUT.category_id, 0)
        self.assertEqual(self.DUT.subcategory_id, 0)
        self.assertEqual(self.DUT.junction_temperature, 30.0)
        self.assertEqual(self.DUT.knee_temperature, 25.0)
        self.assertEqual(self.DUT.thermal_resistance, 0.0)
        self.assertEqual(self.DUT.reference_temperature, 25.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestComponent) _set_attributes should return a 0 error code on success
        """

        _all_values = self._base_values + self._stress_values + \
            self._rel_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code[0], 0)
        self.assertEqual(_error_code[1], 0)
        self.assertEqual(_error_code[2], 0)
        self.assertEqual(_error_code[3], 0)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestComponent) _set_attributes should return a 10 error code when passed a wrong data type
        """

        _stress_values = (0.0, 1.0, None, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0,
                          10.0, 11.0, 12.0, 13.0, 14.0, 15.0, '')
        _all_values = self._base_values + _stress_values + self._rel_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code, [0, 10, 0, 0])

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestComponent) _set_attributes should return a 40 error code when passed too few inputs
        """

        _rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0,
                       0)
        _all_values = self._base_values + self._stress_values + _rel_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code, [0, 0, 40, 0])

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestComponent) get_attributes should return a tuple of attribute values
        """

        _all_values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0,
                       0, '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1,
                       '', 1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0,
                       '', 0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0, 30.0, 25.0, 0.0, 25.0)

        self.assertEqual(self.DUT.get_attributes(), _all_values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestComponent) get_attributes(set_attributes(values)) == values
        """

        _all_values = self._base_values + self._stress_values + \
            self._rel_values

        self.DUT.set_attributes(_all_values)
        _result = self.DUT.get_attributes()

        self.assertEqual(_result[:38], self._base_values[:38])
        self.assertEqual(_result[38:50], self._stress_values[:12])
        self.assertEqual(_result[50], self._stress_values[16])
        self.assertEqual(_result[51:87], self._rel_values)

        # Verify the Component specific attributes.
        self.assertEqual(_result[87:], self._stress_values[12:16])


class TestComponentController(unittest.TestCase):
    """
    Class for testing the Component data controller class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Component class.
        """

        self.DUT = Component()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestComponent) __init__ should return a Component controller
        """

        self.assertTrue(isinstance(self.DUT, Component))
