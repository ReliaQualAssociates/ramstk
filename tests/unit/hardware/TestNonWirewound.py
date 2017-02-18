#!/usr/bin/env python -O
"""
This is the test class for testing fixed and variable NonWirewound resistor module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestNonWirewound.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from hardware.component.resistor.variable.NonWirewound import NonWirewound

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestNonWirewoundModel(unittest.TestCase):
    """
    Class for testing the NonWirewound Variable resistor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the NonWirewound Variable resistor class.
        """

        self.DUT = NonWirewound()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestNonWirewound) __init__ should return a NonWirewound Variable resistor model
        """

        self.assertTrue(isinstance(self.DUT, NonWirewound))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Resistor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the NonWirewound resistor class was properly
        # initialized.
        self.assertEqual(self.DUT._lst_piE, [1.0, 3.0, 14.0, 6.0, 24.0, 5.0,
                                             7.0, 12.0, 18.0, 39.0, 0.5, 22.0,
                                             57.0, 1000.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.03, 0.1, 0.3, 1.0, 3.0,
                                                   10.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [0.02, 0.06, 0.2, 0.6, 3.0,
                                                    10.0])
        self.assertEqual(self.DUT._lst_lambdab_count, [0.043, 0.15, 0.75, 0.35,
                                                       1.3, 0.39, 0.78, 1.8,
                                                       2.8, 2.5, 0.21, 1.2,
                                                       3.7, 49.0])
        self.assertEqual(self.DUT.subcategory, 37)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestNonWirewound) set_attributes should return a 0 error code on success
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
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.75, 0.3, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 5)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.n_taps, 5)
        self.assertEqual(self.DUT.piTAPS, 0.75)
        self.assertEqual(self.DUT.piV, 0.3)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestNonWirewound) set_attributes should return a 40 error code with missing inputs
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
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestNonWirewound) set_attributes should return a 10 error code with a wrong data type
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
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, '')

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestNonWirewound) get_attributes should return a tuple of attribute values
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
                   0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 3, 0.0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestNonWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 1.3)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_active, 3.9E-08)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_resistance(self):
        """
        (TestNonWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for low resistances
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.operating_power = 0.075
        self.DUT.rated_power = 0.25
        self.DUT.rated_voltage = 200.0
        self.DUT.resistance = 3.3E3
        self.DUT.n_taps = 5

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.02503457)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.02)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.8613908E-09)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid1_resistance(self):
        """
        (TestNonWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for mid-range resistances
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.075
        self.DUT.rated_power = 0.25
        self.DUT.rated_voltage = 200.0
        self.DUT.resistance = 1.3E5
        self.DUT.n_taps = 5

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.02503457)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.2)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.02)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.2336689E-09)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid2_resistance(self):
        """
        (TestNonWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with mid-range resistances
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.075
        self.DUT.rated_power = 0.25
        self.DUT.rated_voltage = 200.0
        self.DUT.resistance = 3.3E5
        self.DUT.n_taps = 5

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.02503457)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.4)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.02)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.6059471E-09)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_resistance(self):
        """
        (TestNonWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with high resistance
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.05
        self.DUT.rated_power = 0.25
        self.DUT.rated_voltage = 200.0
        self.DUT.resistance = 6.1E5
        self.DUT.n_taps = 5

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.02386025)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.8)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 1.05)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.02)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.3530051E-09)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestNonWirewound) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 1130.0
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 1.1E4

        self.assertTrue(self.DUT.calculate_part())
