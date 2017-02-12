#!/usr/bin/env python -O
"""
This is the test class for testing Capacitor module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestCapacitor.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import gettext

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from hardware.component.capacitor.Capacitor import Model

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'

_ = gettext.gettext


class TestCapacitorModel(unittest.TestCase):
    """
    Class for testing the Capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Capacitor class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

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
        (TestCapacitor) __init__ should return a Capacitor model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.q_override, 0.0)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.spec_sheet, 0)
        self.assertEqual(self.DUT.acvapplied, 0.0)
        self.assertEqual(self.DUT.capacitance, 0.0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.reason, "")
        self.assertEqual(self.DUT.piQ, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.piCV, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestCapacitor) set_attributes should return a 0 error code on success
        """
        
        _my_values = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, "")
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + _my_values
        
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestCapacitor) set_attributes should return a 40 error code when too few items are passed
        """

        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestCapacitor) set_attributes should return a 10 error code when the wrong type is passed
        """
        
        _my_values = (0.0, 0.0, 0.0, 0.0, None, 0.0, 0.0, 0, 0, 0, "") 
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestCapacitor) get_attributes should return a tuple of attribute values
        """
        
        _my_values = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, "")
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
        (TestCapacitor) get_attributes(set_attributes(values)) == values
        """

        _my_values = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, "")
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
        (TestCapacitor) _overstressed should return False and overstress=False on success without an overstressed condition in non-harsh environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_voltage = 10.0
        self.DUT.rated_voltage = 20.0
        self.assertFalse(self.DUT._overstressed())
        self.assertFalse(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_mild_env_voltage_margin(self):
        """
        (TestCapacitor) _overstressed should return False and overstress=True on success with operating voltage too close to rated in a non-harsh environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_voltage = 19.0
        self.DUT.rated_voltage = 20.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env(self):
        """
        (TestCapacitor) _overstressed should return False and overstress=False on success without an overstressed condition in a harsh environment
        """

        self.DUT.environment_active = 3
        self.DUT.operating_voltage = 10.0
        self.DUT.rated_voltage = 20.0
        self.DUT.max_rated_temperature = 85.0
        self.DUT.temperature_active = 55.0
        self.assertFalse(self.DUT._overstressed())
        self.assertFalse(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_voltage_margin(self):
        """
        (TestCapacitor) _overstressed should return False and overstress=True on success with operating voltage too close to rated in a harsh environment
        """

        self.DUT.environment_active = 3
        self.DUT.operating_voltage = 15.0
        self.DUT.rated_voltage = 20.0
        self.DUT.max_rated_temperature = 85.0
        self.DUT.temperature_active = 55.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_temperature_margin(self):
        """
        (TestCapacitor) _overstressed should return False and overstress=True on success with operating temperature too close to maximum rated in a harsh environment
        """

        self.DUT.environment_active = 3
        self.DUT.operating_voltage = 10.0
        self.DUT.rated_voltage = 20.0
        self.DUT.max_rated_temperature = 85.0
        self.DUT.temperature_active = 80.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_calculate_overflow_error(self):
        """
        (TestCapacitor) calculate_part should return True when there is an OverflowError.
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3

        self.assertTrue(self.DUT.calculate_part())

    @attr(all=True, unit=True)
    def test_calculate_attribute_error(self):
        """
        (TestCapacitor) calculate_part should return True when there is an AttributeError.
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.DUT.reference_temperature = 358.0

        self.assertTrue(self.DUT.calculate_part())
