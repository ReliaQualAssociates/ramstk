#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestConnection.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing Connection module algorithms and models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from hardware.component.connection.Connection import Model

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestConnectionModel(unittest.TestCase):
    """
    Class for testing the Connection data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Connection class.
        """

        self.DUT = Model()
        
        self._base_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                             'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                             0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                             0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                             'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014)
        self._stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                               0.0, 1.0)
        self._rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                            0.0, 0)
        self._user_values = (0.0, 1.0, 2.0, 30.0, 440.0, 5, 6, 7.0, 8.0, 99.0, 10.0,
                             11, 12, 13.0, 14, 15.0, 16.0, 17.0, 18, 19.0, 0.0, 1.0, 
                             2, 3, 440.0, 50, 60, 7.0, 80.0, 90, 'Zero', 'One', 
                             'Two', 'Three', '4')
        self._comp_values = (0, 0, 0.0, 30.0, 0.0, 358.0)
        
    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestConnection) __init__ should return a Connection data model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Connection class was properly initialized.
        self.assertEqual(self.DUT.category, 8)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestConnection) set_attributes should return a 0 error code on success
        """
        
        _my_values = (0.0, 0.0, 0.0, 0.0, 0, "")
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestConnection) set_attributes should return a 40 error code when too few items are passed
        """
        
        _my_values = (0.0, 0.0, 0.0, 0.0, 0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestConnection) set_attributes should return a 10 error code when the wrong type is passed
        """
        
        _my_values = (0.0, 0.0, None, 0.0, 0, "")
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestConnection) get_attributes should return a tuple of attribute values
        """
        
        _my_values = (0.0, 0.0, 1.0, 0.0, 0, "")
        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0, '', 
                   50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '', 1.0, 0, '', 
                   0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                   1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 
                   0.0, 0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0, 0, 0, 0, 0, 0, 
                   0, 0, 0, 0], ['', '', '', '', ''], 0, 0, 0.0, 30.0, 0.0, 30.0) + \
                   _my_values

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestConnection) get_attributes(set_attributes(values)) == values
        """

        _my_values = (0.0, 0.0, 1.0, 0.0, 0, "")
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + _my_values
                  
        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()

        self.assertEqual(_result[:38], self._base_values)
        self.assertEqual(_result[38:50], self._stress_values)
        self.assertEqual(_result[50:86], self._rel_values)
        self.assertEqual(_result[86], list(self._user_values[:20]))
        self.assertEqual(_result[87], list(self._user_values[20:30]))
        self.assertEqual(_result[88], list(self._user_values[30:35]))
        self.assertEqual(_result[89:95], self._comp_values)
        
        self.assertEqual(_result[95:], _my_values)
        
    @attr(all=True, unit=True)
    def test_overstressed_mild_env(self):
        """
        (TestConnection) _overstressed should return False and overstress=False on success without an overstressed condition in non-harsh environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_voltage = 10.0
        self.DUT.rated_voltage = 20.0
        self.DUT.operating_current = 0.001
        self.DUT.rated_current = 0.004
        self.assertFalse(self.DUT._overstressed())
        self.assertFalse(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_mild_env_voltage_margin(self):
        """
        (TestConnection) _overstressed should return False and overstress=True on success with operating voltage too close to rated in a non-harsh environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_voltage = 19.0
        self.DUT.rated_voltage = 20.0
        self.DUT.operating_current = 0.001
        self.DUT.rated_current = 0.004
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_mild_env_current_margin(self):
        """
        (TestConnection) _overstressed should return False and overstress=True on success with operating current too close to rated in a non-harsh environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_voltage = 10.0
        self.DUT.rated_voltage = 20.0
        self.DUT.operating_current = 0.0039
        self.DUT.rated_current = 0.004
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env(self):
        """
        (TestConnection) _overstressed should return False and overstress=False on success without an overstressed condition in harsh environment
        """

        self.DUT.environment_active = 3
        self.DUT.operating_voltage = 10.0
        self.DUT.rated_voltage = 20.0
        self.DUT.operating_current = 0.001
        self.DUT.rated_current = 0.004
        self.assertFalse(self.DUT._overstressed())
        self.assertFalse(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_voltage_margin(self):
        """
        (TestConnection) _overstressed should return False and overstress=True on success with operating voltage too close to rated in a harsh environment
        """

        self.DUT.environment_active = 3
        self.DUT.operating_voltage = 17.0
        self.DUT.rated_voltage = 20.0
        self.DUT.operating_current = 0.001
        self.DUT.rated_current = 0.004
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_current_margin(self):
        """
        (TestConnection) _overstressed should return False and overstress=True on success with operating current too close to rated in a harsh environment
        """

        self.DUT.environment_active = 3
        self.DUT.operating_voltage = 10.0
        self.DUT.rated_voltage = 20.0
        self.DUT.operating_current = 0.0036
        self.DUT.rated_current = 0.004
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_temperature_margin(self):
        """
        (TestConnection) _overstressed should return False and overstress=True on success with operating temperatures too close to rated in a harsh environment
        """

        self.DUT.environment_active = 3
        self.DUT.operating_voltage = 10.0
        self.DUT.rated_voltage = 20.0
        self.DUT.operating_current = 0.003
        self.DUT.rated_current = 0.004
        self.DUT.temperature_rise = 70.3
        self.DUT.temperature_active = 38.0
        self.max_rated_temperature = 125.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_calculate_attribute_error(self):
        """
        (TestConnection) calculate_part should return True when there is an AttributeError.
        """

        self.DUT.hazard_rate_type = 1
        self.DUT.environment_active = 1

        self.assertTrue(self.DUT.calculate_part())
