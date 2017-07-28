#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestIC.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing Integrated Circuit module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from hardware.component.integrated_circuit.IntegratedCircuit import Model

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestICModel(unittest.TestCase):
    """
    Class for testing the Integrated Circuit data model class.
    """

    _base_values = (0, 1, 'Alt Part #', 'Attachments', 'CAGE Code',
                    'Comp Ref Des', 6.0, 7.0, 8.0, 'Description', 10.0, 11, 12,
                    'Figure #', 15.0, 'LCN', 17, 18, 19.0, 'Name', 'NSN', 22,
                    'Page #', 24, 25, 'Part #', 26, 'Ref Des', 28.0, 29,
                    'Remarks', 31.0, 'Spec #', 33, 34.0, 35.0, 36.0, 2014, 38,
                    39, 40, 41.0, 42, 43)
    _stress_values = (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0,
                      11.0, 12.0, 13.0, 14.0, 15.0, '')
    _rel_values = (0.0, 1.0, 2.0, 3.0, 4.0, 5, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0,
                   12, 13.0, {}, 15.0, 16.0, 17.0, 18, 19.0, 20.0, 21.0, 22.0,
                   23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0,
                   33.0, 34.0, 35)
    _comp_values = (0.0, 1.0, 2.0, 3.0, 4.0, 5, 6, 7.0, 8.0, 9.0, 10.0, 11, 12,
                    13.0, 14, 15.0, 16.0, 17.0, 18, 19.0, 20.0, 21.0, 22, 23,
                    24.0, 25, 26, 27.0, 28.0, 29, 'Thirty', '31', 'Thirty Two',
                    '33', '34')

    def setUp(self):
        """
        Setup the test fixture for the Integrated Circuit class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestIC) __init__ should return a Integrated Circuit data model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)

        # Verify Integrated Circuit class was properly initialized.
        self.assertEqual(self.DUT.q_override, 0.0)
        self.assertEqual(self.DUT.case_temperature, 30.0)
        self.assertEqual(self.DUT.activation_energy, 0.0)
        self.assertEqual(self.DUT.years_produced, 1.0)

        self.assertEqual(self.DUT.category_id, 1)
        self.assertEqual(self.DUT.technology_id, 0)
        self.assertEqual(self.DUT.quality_id, 0)
        self.assertEqual(self.DUT.num_elements, 0)

        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.C1, 0.0)
        self.assertEqual(self.DUT.C2, 0.0)
        self.assertEqual(self.DUT.piT, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.piL, 0.0)
        self.assertEqual(self.DUT.piQ, 1.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestIC) set_attributes should return a 0 error code on success
        """

        _all_values = self._base_values + self._stress_values + \
            self._rel_values + self._comp_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code, [0, 0, 0, 0, 0])

        self.assertEqual(self.DUT.category_id, 42)
        self.assertEqual(self.DUT.technology_id, 20)
        self.assertEqual(self.DUT.quality_id, 22)
        self.assertEqual(self.DUT.num_elements, 21)
        self.assertEqual(self.DUT.base_hr, 4.0)
        self.assertEqual(self.DUT.C1, 5.0)
        self.assertEqual(self.DUT.C2, 7.0)
        self.assertEqual(self.DUT.piT, 6.0)
        self.assertEqual(self.DUT.piE, 8.0)
        self.assertEqual(self.DUT.piL, 9.0)
        self.assertEqual(self.DUT.piQ, 10.0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestIC) set_attributes should return a 40 error code when too few items are passed
        """

        _comp_values = (0.0, 30.0, 0.65, 1.5, 0.00115, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                        0, 8)

        _all_values = self._base_values + self._stress_values + \
            self._rel_values + _comp_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code[4], 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestIC) set_attributes should return a 10 error code when the wrong type is passed
        """

        _comp_values = (0.0, None, 0.65, 1.5, 0.00115, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                        0, 8, 0)

        _all_values = self._base_values + self._stress_values + \
            self._rel_values + _comp_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code[4], 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestIC) get_attributes should return a tuple of attribute values
        """

        _all_values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0,
                       0, '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1,
                       '', 1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0,
                       '', 0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0, 0, 0, 30.0, 25.0, 0.0, 25.0, 0.0, 1.0, 2.0, 3.0,
                       4.0, 5, 6, 7.0, 8.0, 9.0, 10.0, 11, 12, 13.0)

        self.assertEqual(self.DUT.get_attributes(), _all_values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestIC) get_attributes(set_attributes(values)) == values
        """

        _base_values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0,
                        0, 0, '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0,
                        '', 1, '', 1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0,
                        2014, 0, 0, 0, 0.0, 1, 0)
        _stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                          0.0, 1.0, 30.0, 25.0, 0.0, 25.0, '')
        _rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0)
        _comp_values = (0.0, 30.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,
                        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 8, 0)

        _all_values = _base_values + _stress_values + _rel_values + \
            _comp_values

        self.DUT.set_attributes(_all_values)
        _result = self.DUT.get_attributes()

        self.assertEqual(_result[:38], _base_values[:38])
        self.assertEqual(_result[38:50], _stress_values[:12])
        self.assertEqual(_result[50], _stress_values[16])
        self.assertEqual(_result[51:87], _rel_values)
        self.assertEqual(_result[87:91], _stress_values[12:16])
        self.assertEqual(_result[91], _base_values[42])
        self.assertEqual(_result[92:], _comp_values[:14])

    @attr(all=True, unit=True)
    def test_overstressed_mild_env_high_voltage(self):
        """
        (TestIC) _overstressed should return False and overstress=False on success with operating voltage greater than rated in a non-harsh environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_voltage = 3.5
        self.DUT.rated_voltage = 3.3
        self.DUT.operating_current = 0.001
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_mild_env_low_voltage(self):
        """
        (TestIC) _overstressed should return False and overstress=True on success with operating voltage too far from rated in a non-harsh environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_voltage = 3.1
        self.DUT.rated_voltage = 3.3
        self.DUT.operating_current = 0.001
        self.DUT.rated_current = 0.004
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_mild_env_current_margin(self):
        """
        (TestIC) _overstressed should return False and overstress=True on success with operating current too close to rated in a non-harsh environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.rated_voltage = 3.3
        self.DUT.operating_current = 0.0038
        self.DUT.rated_current = 0.004
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_high_voltage(self):
        """
        (TestIC) _overstressed should return False and overstress=False on success with operating voltage greater than rated in a harsh environment
        """

        self.DUT.environment_active = 3
        self.DUT.operating_voltage = 3.5
        self.DUT.rated_voltage = 3.3
        self.DUT.operating_current = 0.0038
        self.DUT.rated_current = 0.004
        self.DUT.junction_temperature = 105.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_low_voltage(self):
        """
        (TestIC) _overstressed should return False and overstress=True on success with operating voltage less than rated in a harsh environment
        """

        self.DUT.environment_active = 3
        self.DUT.operating_voltage = 1.25
        self.DUT.rated_voltage = 3.3
        self.DUT.operating_current = 0.001
        self.DUT.rated_current = 0.004
        self.DUT.junction_temperature = 105.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_current_margin(self):
        """
        (TestIC) _overstressed should return False and overstress=True on success with operating current too close to rated in a harsh environment
        """

        self.DUT.environment_active = 3
        self.DUT.operating_voltage = 3.3
        self.DUT.rated_voltage = 3.3
        self.DUT.operating_current = 0.0033
        self.DUT.rated_current = 0.004
        self.DUT.hot_spot_temperature = 105.0
        self.DUT.max_rated_temperature = 150.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_temperature_margin(self):
        """
        (TestIC) _overstressed should return False and overstress=True on success with operating temperatures too close to rated in a harsh environment
        """

        self.DUT.environment_active = 3
        self.DUT.operating_voltage = 3.3
        self.DUT.rated_voltage = 3.3
        self.DUT.operating_current = 0.003
        self.DUT.rated_current = 0.004
        self.DUT.junction_temperature = 145.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_calculate_attribute_error(self):
        """
        (TestIC) calculate_part should return True when there is an AttributeError.
        """

        self.DUT.hazard_rate_type = 1
        self.DUT.environment_active = 1

        self.assertTrue(self.DUT.calculate_part())
