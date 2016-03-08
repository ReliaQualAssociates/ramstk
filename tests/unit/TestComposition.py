#!/usr/bin/env python -O
"""
This is the test class for testing Carbon Composition resistor module
algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestComposition.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from hardware.component.resistor.fixed.Composition import Composition
from hardware.component.resistor.variable.Composition import VarComposition

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestCompositionModel(unittest.TestCase):
    """
    Class for testing the Carbon Composition resistor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Carbon Composition resistor class.
        """

        self.DUT = Composition()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestCarbonComposition) __init__ should return a Carbon Composition resistor model
        """

        self.assertTrue(isinstance(self.DUT, Composition))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Resistor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Carbon Composition resistor class was properly
        # initialized.
        self.assertEqual(self.DUT._lst_piR, [1.0, 1.1, 1.6, 2.5])
        self.assertEqual(self.DUT._lst_piE, [1.0, 3.0, 8.0, 5.0, 13.0, 4.0,
                                             5.0, 7.0, 11.0, 19.0, 0.5, 11.0,
                                             27.0, 490.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.03, 0.1, 0.3, 1.0, 3.0,
                                                   10.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [0.03, 0.1, 0.3, 1.0, 5.0,
                                                    15.0])
        self.assertEqual(self.DUT._lst_lambdab_count, [0.0005, 0.0022, 0.0071,
                                                       0.0037, 0.012, 0.0052,
                                                       0.0065, 0.016, 0.025,
                                                       0.025, 0.00025, 0.0098,
                                                       0.035, 0.36])
        self.assertEqual(self.DUT.subcategory, 25)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestCarbonComposition) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.012)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.6E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_resistance(self):
        """
        (TestCarbonComposition) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with low resistance
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.113
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 1.1E4

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0004169734)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.7527606E-11)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid1_resistance(self):
        """
        (TestCarbonComposition) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with mid-range resistance
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.113
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 3.3E5

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0004169734)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.1)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.12803666E-11)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid2_resistance(self):
        """
        (TestCarbonComposition) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with mid-range resistance
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.113
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 3.3E6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0004169734)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.6)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 6.00441696E-11)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_resistance(self):
        """
        (TestCarbonComposition) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with high resistance
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.113
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 3.3E7

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0004169734)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 2.5)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 9.3819015E-11)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestCarbonComposition) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 113.0
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 1.1E4

        self.assertTrue(self.DUT.calculate_part())


class TestVarCompositionModel(unittest.TestCase):
    """
    Class for testing the VarComposition Variable resistor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the VarComposition Variable resistor class.
        """

        self.DUT = VarComposition()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestVarComposition) __init__ should return a VarComposition Variable resistor model
        """

        self.assertTrue(isinstance(self.DUT, VarComposition))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Resistor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the VarComposition resistor class was properly
        # initialized.
        self.assertEqual(self.DUT._lst_piE, [1.0, 2.0, 19.0, 8.0, 29.0, 40.0,
                                             65.0, 48.0, 78.0, 46.0, 0.5, 25.0,
                                             66.0, 1200.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.03, 0.1, 0.3, 1.0, 3.0,
                                                   10.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [2.5, 5.0])
        self.assertEqual(self.DUT._lst_lambdab_count, [0.05, 0.11, 1.1, 0.45,
                                                       1.7, 2.8, 4.6, 4.6, 7.5,
                                                       3.3, 0.025, 1.5, 4.7,
                                                       67.0])
        self.assertEqual(self.DUT.subcategory, 38)
        self.assertEqual(self.DUT.n_taps, 3)
        self.assertEqual(self.DUT.piTAPS, 0.0)
        self.assertEqual(self.DUT.piV, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestVarComposition) set_attributes should return a 0 error code on success
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
        (TestVarComposition) set_attributes should return a 40 error code with missing inputs
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
        (TestVarComposition) set_attributes should return a 10 error code with a wrong data type
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
        (TestVarComposition) get_attributes should return a tuple of attribute values
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
        (TestVarComposition) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 1.7)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 5.1E-08)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_resistance(self):
        """
        (TestVarComposition) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for low resistances
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
                               0.02112810)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 2.5)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.3091114E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid1_resistance(self):
        """
        (TestVarComposition) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for mid-range resistances
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
                               0.02112810)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.2)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 2.5)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.5709337E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid2_resistance(self):
        """
        (TestVarComposition) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with mid-range resistances
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
                               0.02112810)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.4)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 2.5)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.8327560E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_resistance(self):
        """
        (TestVarComposition) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with high resistance
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
                               0.01960337)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.8)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 1.05)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 2.5)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.0405921E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestVarComposition) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 1130.0
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 1.1E4

        self.assertTrue(self.DUT.calculate_part())
