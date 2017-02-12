#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestLogic.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing Logic IC module algorithms and models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from hardware.component.integrated_circuit.Logic import Logic

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestLogicModel(unittest.TestCase):
    """
    Class for testing the Logic IC data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Logic IC class.
        """

        self.DUT = Logic()
        
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
        self._ic_values = (1.0, 0.05, 3.0, 4.0, 5.0, 1, "")
        
    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestLogic) __init__ should return an Logic IC data model
        """

        self.assertTrue(isinstance(self.DUT, Logic))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Inductor class was properly initialized.
        self.assertEqual(self.DUT.category, 1)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.piQ, 1.0)

        # Verify the Logic IC class was properly initialized.
        self.assertEqual(self.DUT.subcategory, 2)
        self.assertEqual(self.DUT.technology, 0)
        self.assertEqual(self.DUT.family, 0)
        self.assertEqual(self.DUT.package, 0)
        self.assertEqual(self.DUT.n_gates, 0)
        self.assertEqual(self.DUT.n_pins, 0)
        self.assertEqual(self.DUT.years_production, 0.0)
        self.assertEqual(self.DUT.case_temperature, 0.0)
        self.assertEqual(self.DUT.C1, 0.0)
        self.assertEqual(self.DUT.C2, 0.0)
        self.assertEqual(self.DUT.piL, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestLogic) set_attributes should return a 0 error code on success
        """

        _my_values = (1, 2,  3, 206, 8, 1.5, 75.0, 0.0025, 0.0097, 1.2)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._ic_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.technology, 1)
        self.assertEqual(self.DUT.family, 2)
        self.assertEqual(self.DUT.package, 3)
        self.assertEqual(self.DUT.n_gates, 206)
        self.assertEqual(self.DUT.n_pins, 8)
        self.assertEqual(self.DUT.years_production, 1.5)
        self.assertEqual(self.DUT.case_temperature, 75.0)
        self.assertEqual(self.DUT.C1, 0.0025)
        self.assertEqual(self.DUT.C2, 0.0097)
        self.assertEqual(self.DUT.piL, 1.2)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestLogic) set_attributes should return a 40 error code when too few items are passed
        """
        
        _my_values = (1, 2,  3, 206, 8, 1.5, 75.0, 0.0025, 1.2)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._ic_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestLogic) set_attributes should return a 10 error code when the wrong type is passed
        """
        
        _my_values = (1, 2,  3, 206, 8, 1.5, 75.0, 0.0025, None, 1.2)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._ic_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestLogic) get_attributes should return a tuple of attribute values
        """
        
        _my_values = (0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0)
        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0, '', 
                   50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '', 1.0, 0, '', 
                   0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                   1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 
                   0.0, 0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0, 0, 0, 0, 0, 0, 
                   0, 0, 0, 0], ['', '', '', '', ''], 0, 0, 0.0, 30.0, 0.0, 30.0, 
                   0.0, 0.0, 1.0, 0.0, 0.0, 0, "") + _my_values

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestLogic) get_attributes(set_attributes(values)) == values
        """

        _my_values = (0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._ic_values + \
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
        self.assertEqual(_result[95:102], self._ic_values)
        
        self.assertEqual(_result[102:], _my_values)
        
    @attr(all=True, unit=False)
    def test_calculate_217_count(self):
        """
        (TestLogic) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality = 1
        self.DUT.technology = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')

    @attr(all=True, unit=True)
    def test_calculate_217_count_all(self):
        """
        (TestLogic) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.n_gates = 100
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.035)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 8.75E-9)

        self.DUT.n_gates = 1000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.055)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.375E-8)

        self.DUT.n_gates = 3000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.097)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.425E-8)

        self.DUT.n_gates = 10000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.33)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 8.25E-8)

        self.DUT.n_gates = 30000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.48)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.2E-7)

        self.DUT.n_gates = 60000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.63)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.575E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestLogic) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.operating_power = 0.25
        self.DUT.thermal_resistance = 60.0

        self.DUT.technology = 1
        self.DUT.family = 2
        self.DUT.package = 3
        self.DUT.n_gates = 206
        self.DUT.n_pins = 18
        self.DUT.years_production = 1.5
        self.DUT.case_temperature = 35.0

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.junction_temperature, 50.0)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         '(C1 * piT + C2 * piE) * piQ * piL')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['C1'], 0.005)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['C2'], 0.0063511495)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 0.3709554)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piL'], 1.2458647)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.379876E-8)
