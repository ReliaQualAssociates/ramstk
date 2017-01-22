#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestTantalum.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing Tantalum capacitor module algorithms and models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from hardware.component.capacitor.electrolytic.Tantalum import Solid, NonSolid

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestSolidTantalumModel(unittest.TestCase):
    """
    Class for testing the Solid Tantalum capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Capacitor class.
        """

        self.DUT = Solid()
        
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
        self._capacitor_values = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, "")
        
    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestSolidTantalum) __init__ should return a Solid Tantalum capacitor model
        """

        self.assertTrue(isinstance(self.DUT, Solid))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Solid Tantalum capacitor class was properly initialized.
        self.assertEqual(self.DUT._piE, [1.0, 2.0, 8.0, 5.0, 14.0, 4.0, 5.0,
                                         12.0, 20.0, 24.0, 0.4, 11.0, 29.0,
                                         530.0])
        self.assertEqual(self.DUT._piQ, [0.001, 0.01, 0.03, 0.03, 0.1, 0.3,
                                         1.0, 1.5, 10.0])
        self.assertEqual(self.DUT._lambdab_count, [0.0018, 0.0039, 0.016,
                                                   0.0097, 0.028, 0.0091,
                                                   0.011, 0.034, 0.057, 0.055,
                                                   0.00072, 0.022, 0.066, 1.0])
        self.assertEqual(self.DUT.subcategory, 51)
        self.assertEqual(self.DUT.effective_resistance, 0.0)
        self.assertEqual(self.DUT.piSR, 0.0)
        self.assertEqual(self.DUT.reference_temperature, 398.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestSolidTantalum) set_attributes should return a 0 error code on success
        """

        _my_values = (0.0, 0.0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._capacitor_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestSolidTantalum) set_attributes should return a 40 error code when too few items are passed
        """

        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._capacitor_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestSolidTantalum) set_attributes should return a 10 error code when the wrong type is passed
        """

        _my_values = (None, 0.0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._capacitor_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestSolidTantalum) get_attributes should return a tuple of attribute values
        """

        _my_values = (0.0, 0.0)
        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0, '', 
                   50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '', 1.0, 0, '', 
                   0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                   1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 
                   0.0, 0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0, 0, 0, 0, 0, 0, 
                   0, 0, 0, 0], ['', '', '', '', ''], 0, 0, 0.0, 30.0, 0.0, 398.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, "") + \
                   _my_values

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestSolidTantalum) get_attributes(set_attributes(values)) == values
        """

        _my_values = (0.0, 0.0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._capacitor_values + \
                  _my_values
                  
        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()

        self.assertEqual(_result[:38], self._base_values)
        self.assertEqual(_result[38:50], self._stress_values)
        self.assertEqual(_result[50:86], self._rel_values)
        self.assertEqual(_result[86], list(self._user_values[:20]))
        self.assertEqual(_result[87], list(self._user_values[20:30]))
        self.assertEqual(_result[88], list(self._user_values[30:35]))
        self.assertEqual(_result[89:95], self._comp_values)
        self.assertEqual(_result[95:106], self._capacitor_values)
        self.assertEqual(_result[106:], _my_values)
        
    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestSolidTantalum) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.hazard_rate_type = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 10.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.0e-05)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestSolidTantalum) calculate_part should return False on success when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.reference_temperature = 398.0
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000027
        self.DUT.effective_resistance = 0.5

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV * piSR')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.008913701)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.001)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 1.126584189)
        self.assertEqual(self.DUT.hazard_rate_model['piSR'], 0.13)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.61092913e-12)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestSolidTantalum) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000027
        self.DUT.effective_resistance = 0.5
        self.DUT.reference_temperature = 0.000000000000001

        self.assertTrue(self.DUT.calculate_part())

    @attr(all=True, unit=True)
    def test_calculate_217_stress_zero_division(self):
        """
        (TestSolidTantalum) calculate_part should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000033
        self.DUT.effective_resistance = 0.5
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate_part())


class TestNonSolidTantalumModel(unittest.TestCase):
    """
    Class for testing the Non-Solid Tantalum capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Non-Solid Tantalum capacitor class.
        """

        self.DUT = NonSolid()
        
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
        self._capacitor_values = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, "")
        
    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestNonSolidTantalum) __init__ should return a NonSolid Tantalum capacitor model
        """

        self.assertTrue(isinstance(self.DUT, NonSolid))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Non-Solid Tantalum capacitor class was properly initialized.
        self.assertEqual(self.DUT._piC, [0.3, 1.0, 2.0, 2.5, 3.0])
        self.assertEqual(self.DUT._piE, [1.0, 2.0, 10.0, 6.0, 16.0, 4.0, 8.0,
                                         14.0, 30.0, 23.0, 0.5, 13.0, 34.0,
                                         610.0])
        self.assertEqual(self.DUT._piQ, [0.03, 0.1, 0.3, 1.0, 1.5, 3.0, 10.0])
        self.assertEqual(self.DUT._lambdab_count, [0.0061, 0.013, 0.069, 0.039,
                                                   0.11, 0.031, 0.061, 0.13,
                                                   0.29, 0.18, 0.0030, 0.069,
                                                   0.26, 4.0])
        self.assertEqual(self.DUT.subcategory, 52)
        self.assertEqual(self.DUT.construction, 0)
        self.assertEqual(self.DUT.piC, 0.0)
        self.assertEqual(self.DUT.reference_temperature, 358.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestNonSolidTantalum) set_attributes should return a 0 error code on success
        """

        _my_values = (0, 0.0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._capacitor_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestNonSolidTantalum) set_attributes should return a 40 error code when too few items are passed
        """

        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._capacitor_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestNonSolidTantalum) set_attributes should return a 10 error code when the wrong type is passed
        """

        _my_values = (0, None)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._capacitor_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)
        self.assertEqual(_error_msg,
                         "ERROR: Converting one or more inputs to correct data type.")

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestNonSolidTantalum) get_attributes should return a tuple of attribute values
        """
        
        _my_values = (0, 0.0)
        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0, '', 
                   50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '', 1.0, 0, '', 
                   0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                   1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 
                   0.0, 0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0, 0, 0, 0, 0, 0, 
                   0, 0, 0, 0], ['', '', '', '', ''], 0, 0, 0.0, 30.0, 0.0, 358.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, "") + \
                   _my_values

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestNonSolidTantalum) get_attributes(set_attributes(values)) == values
        """

        _my_values = (0.0, 0.0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._capacitor_values + \
                  _my_values
                  
        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()

        self.assertEqual(_result[:38], self._base_values)
        self.assertEqual(_result[38:50], self._stress_values)
        self.assertEqual(_result[50:86], self._rel_values)
        self.assertEqual(_result[86], list(self._user_values[:20]))
        self.assertEqual(_result[87], list(self._user_values[20:30]))
        self.assertEqual(_result[88], list(self._user_values[30:35]))
        self.assertEqual(_result[89:95], self._comp_values)
        self.assertEqual(_result[95:106], self._capacitor_values)
        self.assertEqual(_result[106:], _my_values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestNonSolidTantalum) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.hazard_rate_type = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 4.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 10.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.0e-05)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_temp(self):
        """
        (TestNonSolidTantalum) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 85C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.reference_temperature = 358.0
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000027
        self.DUT.construction = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV * piC')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.00546151)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.875555864)
        self.assertEqual(self.DUT.hazard_rate_model['piC'], 0.3)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 8.60734309e-011)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid_temp(self):
        """
        (TestNonSolidTantalum) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 125C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.reference_temperature = 398.0
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000027
        self.DUT.construction = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV * piC')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.003825333)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.875555864)
        self.assertEqual(self.DUT.hazard_rate_model['piC'], 0.3)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.4222874e-011)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_temp(self):
        """
        (TestNonSolidTantalum) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 125C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.reference_temperature = 448.0
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000027
        self.DUT.construction = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV * piC')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.003304474)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.875555864)
        self.assertEqual(self.DUT.hazard_rate_model['piC'], 0.3)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 5.20785263e-011)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestNonSolidTantalum) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000033
        self.DUT.effective_resistance = 0.5
        self.DUT.reference_temperature = 0.00000000000001

        self.assertTrue(self.DUT.calculate_part())

    @attr(all=True, unit=True)
    def test_calculate_217_stress_zero_division(self):
        """
        (TestNonSolidTantalum) calculate_part should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000033
        self.DUT.effective_resistance = 0.5
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate_part())
