#!/usr/bin/env python -O
"""
This is the test class for testing Display module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestDisplay.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from hardware.component.semiconductor.optoelectronic.Display import *

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestDisplayModel(unittest.TestCase):
    """
    Class for testing the Optoelectronic Display data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Optoelectronic Display class.
        """

        self.DUT = Display()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestDisplay) __init__ should return a Optoelectronic Display data model
        """

        self.assertTrue(isinstance(self.DUT, Display))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify the Semiconductor class was properly initialized.
        self.assertEqual(self.DUT.category, 2)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.q_override, 0.0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piQ, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.piT, 0.0)

        # Verify the Optoelectronic Display class was properly initialized.
        self.assertEqual(self.DUT._lst_lambdab, [0.0055, 0.0040, 0.0025, 0.013,
                                                 0.013, 0.0064, 0.0033, 0.017,
                                                 0.017, 0.0086, 0.0013,
                                                 0.00023])
        self.assertEqual(self.DUT._lst_piE, [1.0, 2.0, 8.0, 5.0, 12.0, 4.0,
                                             6.0, 6.0, 8.0, 17.0, 0.5, 9.0,
                                             24.0, 450.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.7, 1.0, 2.4, 5.5, 8.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [0.7, 1.0, 2.4, 5.5, 8.0])
        self.assertEqual(self.DUT._lst_lambdab_count, [0.0062, 0.016, 0.045,
                                                       0.032, 0.10, 0.046,
                                                       0.058, 0.11, 0.19, 0.18,
                                                       0.0031, 0.082, 0.28,
                                                       2.0])
        self.assertEqual(self.DUT.subcategory, 23)
        self.assertEqual(self.DUT.type, 0)
        self.assertEqual(self.DUT.construction, 0)
        self.assertEqual(self.DUT.n_characters, 0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestDisplay) set_attributes should return a 0 error code on success
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 0.01, 2.0, 1.0, 1.0, 0.5, 0.8, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 2, 4, 8)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.type, 2)
        self.assertEqual(self.DUT.construction, 4)
        self.assertEqual(self.DUT.n_characters, 8)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestDisplay) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 2.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestDisplay) set_attributes should return a 10 error code when the wrong type is passed
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 1.0, 0.01, 2.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, '', 8)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestDisplay) get_attributes should return a tuple of attribute values
        """

        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0,
                   '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '',
                   1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1,
                   0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0,
                   0.0, 30.0, 0.0, 30.0,
                   0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 0, 0, 0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestDisplay) get_attributes(set_attributes(values)) == values
        """

        _in_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                      'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                      0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                      'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                      'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                      1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                      0.0, 1.0,
                      0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                      0, 0, 1, 0.0,
                      0, 0, 0.0, 30.0, 0.0, 358.0,
                      1.0, 0.01, 2.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 4, 2, 8)
        _out_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                       'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                       0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                       0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                       'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                       1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                       0.0, 1.0,
                       0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0,
                       0, 0, 0.0, 30.0, 0.0, 358.0,
                       3, 1.0, 0.01, 2.0, 1.0, 1.0, '', 4, 2, 8)

        self.DUT.set_attributes(_in_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _out_values)

    @attr(all=True, unit=True)
    def test_overstressed_high_voltage(self):
        """
        (TestDisplay) _overstressed should return False and overstress=False on success with operating voltage greater than rated
        """

        self.DUT.operating_voltage = 18.0
        self.DUT.rated_voltage = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_high_temperature(self):
        """
        (TestDisplay) _overstressed should return False and overstress=False on success with junction temperature greater than 125C
        """

        self.DUT.junction_temperature = 135.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestDisplay) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.10)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.7)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 7.0E-08)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_no_logic(self):
        """
        (TestDisplay) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with no logic chip
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.junction_temperature = 38.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.rated_voltage = 3.3
        self.DUT.type = 1
        self.DUT.construction = 1
        self.DUT.n_characters = 7

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piQ * piE')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'],
                         0.003053)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 1.4789835)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.7)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 6.2324365E-09)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_with_logic(self):
        """
        (TestDisplay) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with a logic chip
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.junction_temperature = 38.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.rated_voltage = 3.3
        self.DUT.type = 2
        self.DUT.construction = 2
        self.DUT.n_characters = 2

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.00043)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 1.4789835)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.7)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.8697309E-09)
