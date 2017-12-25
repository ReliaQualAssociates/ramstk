#!/usr/bin/env python -O
"""
This is the test class for testing Assembly module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestAssembly.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk",
)

import unittest
from nose.plugins.attrib import attr

from hardware.assembly.Assembly import Model, Assembly

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestAssemblyModel(unittest.TestCase):
    """
    Class for testing the Assembly data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Assembly class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestAssembly) __init__ should return an Assembly model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        # Properly sources the Hardware class.
        self.assertEqual(self.DUT.revision_id, None)

        # Dictionaries are empty.
        self.assertEqual(self.DUT.dicAssemblies, {})
        self.assertEqual(self.DUT.dicComponents, {})

        # Scalar values are correct.
        self.assertEqual(self.DUT.cost_type, 0)
        self.assertEqual(self.DUT.repairable, 1)
        self.assertEqual(self.DUT.total_part_quantity, 0)
        self.assertEqual(self.DUT.total_power_dissipation, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestAssembly) _set_attributes should return a 0 error code on success
        """

        _base_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                        'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                        0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                        0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                        'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014, 0,
                        0, 0, 0.0, 0, 0)
        _stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                          0.0, 1.0, 30.0, 25.0, 0.0, 25.0, "")
        _rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0)
        _user_values = (0.0, 1.0, 2.0, 30.0, 440.0, 5, 6, 7.0, 8.0, 99.0, 10.0,
                        11, 12, 13.0, 14, 15.0, 16.0, 17.0, 18, 19.0, 0.0, 1.0,
                        2, 3, 440.0, 50, 60, 7.0, 80.0, 90, 'Zero', 'One',
                        'Two', 'Three', '4')

        _all_values = _base_values + _stress_values + _rel_values

        (_error_code, _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code[0], 0)
        self.assertEqual(_error_code[1], 0)
        self.assertEqual(_error_code[2], 0)
        self.assertEqual(_error_code[3], 0)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestAssembly) _set_attributes should return a 10 error code when passed a wrong data type
        """

        _base_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                        'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                        0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                        0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                        'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014, 0,
                        0, 0, 0.0, 0, 0)
        _stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                          0.0, 1.0, 30.0, 25.0, 0.0, 25.0, "")
        _rel_values = (0.0, 1.0, 1.0, None, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0)
        _user_values = (0.0, 1.0, 2.0, 30.0, 440.0, 5, 6, 7.0, 8.0, 99.0, 10.0,
                        11, 12, 13.0, 14, 15.0, 16.0, 17.0, 18, 19.0, 0.0, 1.0,
                        2, 3, 440.0, 50, 60, 7.0, 80.0, 90, 'Zero', 'One',
                        'Two', 'Three', '4')

        _all_values = _base_values + _stress_values + _rel_values

        (_error_code, _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code[0], 0)
        self.assertEqual(_error_code[1], 0)
        self.assertEqual(_error_code[2], 10)
        self.assertEqual(_error_code[3], 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestAssembly) _set_attributes should return a 40 error code when passed too few inputs
        """

        _base_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                        'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                        0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                        0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                        'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014, 0,
                        0, 0, 0.0, 0, 0)
        _stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                          0.0, 1.0, 30.0, 25.0, 0.0, 25.0, "")
        _rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0)
        _user_values = (0.0, 1.0, 2.0, 30.0, 440.0, 5, 6, 7.0, 8.0, 99.0, 10.0,
                        11, 12, 13.0, 14, 15.0, 16.0, 17.0, 18, 19.0, 0.0, 1.0,
                        2, 3, 440.0, 50, 60, 7.0, 80.0, 90, 'Zero', 'One',
                        'Two', 'Three', '4')

        _all_values = _base_values + _stress_values + _rel_values

        (_error_code, _error_msg) = self.DUT.set_attributes(_all_values[:10])
        self.assertEqual(_error_code[0], 40)
        self.assertEqual(_error_code[1], 40)
        self.assertEqual(_error_code[2], 40)
        self.assertEqual(_error_code[3], 0)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestAssembly) get_attributes should return a tuple of attribute values
        """

        _all_values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0,
                       0, '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1,
                       '', 1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0,
                       '', 0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0, 0, 1, 0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _all_values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestAssembly) get_attributes(set_attributes(values)) == values
        """

        _base_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                        'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                        0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                        0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                        'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014, 0,
                        0, 0, 0.0, 0, 0)
        _stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                          0.0, 1.0, 30.0, 25.0, 0.0, 25.0, "")
        _rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0)
        _user_values = (0.0, 1.0, 2.0, 30.0, 440.0, 5, 6, 7.0, 8.0, 99.0, 10.0,
                        11, 12, 13.0, 14, 15.0, 16.0, 17.0, 18, 19.0, 0.0, 1.0,
                        2, 3, 440.0, 50, 60, 7.0, 80.0, 90, 'Zero', 'One',
                        'Two', 'Three', '4')

        _all_values = _base_values + _stress_values + _rel_values

        self.DUT.set_attributes(_all_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result[:38], _base_values[:38])
        self.assertEqual(_result[38:50], _stress_values[:12])
        self.assertEqual(_result[50], _stress_values[16])
        self.assertEqual(_result[51:87], _rel_values)

        # Verify the Assembly specific attributes.
        self.assertEqual(_result[87:], _base_values[38:42])


class TestAssemblyController(unittest.TestCase):
    """
    Class for testing the Assembly data controller class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Assembly class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Assembly()

    @attr(all=True, unit=False)
    def test_create(self):
        """
        (TestAssembly) __init__ should return an Assembly controller
        """

        self.assertTrue(isinstance(self.DUT, Assembly))
