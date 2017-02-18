#!/usr/bin/env python -O
"""
This is the test class for testing Carbon Film resistor module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestFilm.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from hardware.component.resistor.fixed.Film import *
from hardware.component.resistor.variable.Film import *

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestFilmModel(unittest.TestCase):
    """
    Class for testing the Carbon Film resistor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Carbon Film resistor class.
        """

        self.DUT = Film()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestCarbonFilm) __init__ should return a Carbon Film resistor model
        """

        self.assertTrue(isinstance(self.DUT, Film))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Resistor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Carbon Film resistor class was properly
        # initialized.
        self.assertEqual(self.DUT._lst_piR, [1.0, 1.1, 1.6, 2.5])
        self.assertEqual(self.DUT._lst_piE, [1.0, 2.0, 8.0, 4.0, 14.0, 4.0,
                                             8.0, 10.0, 18.0, 19.0, 0.2, 10.0,
                                             28.0, 510.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.03, 0.1, 0.3, 1.0, 3.0,
                                                   10.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [0.03, 0.1, 0.3, 1.0, 5.0,
                                                    5.0, 15.0])
        self.assertEqual(self.DUT._lambdab_count, [[0.0012, 0.0027, 0.011,
                                                    0.0054, 0.020, 0.0063,
                                                    0.013, 0.018, 0.033, 0.030,
                                                    0.00025, 0.014, 0.044,
                                                    0.69],
                                                   [0.0012, 0.0027, 0.011,
                                                    0.0054, 0.020, 0.0063,
                                                    0.013, 0.018, 0.033, 0.030,
                                                    0.00025, 0.014, 0.044,
                                                    0.69],
                                                   [0.0014, 0.0031, 0.013,
                                                    0.0061, 0.023, 0.0072,
                                                    0.014, 0.021, 0.038, 0.034,
                                                    0.00028, 0.016, 0.050,
                                                    0.78],
                                                   [0.0014, 0.0031, 0.013,
                                                    0.0061, 0.023, 0.0072,
                                                    0.014, 0.021, 0.038, 0.034,
                                                    0.00028, 0.016, 0.050,
                                                    0.78]])
        self.assertEqual(self.DUT.subcategory, 26)
        self.assertEqual(self.DUT.specification, 0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestCarbonFilm) set_attributes should return a 0 error code on success
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
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.specification, 1)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestResistor) get_attributes should return a tuple of attribute values
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
                   0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestCarbonFilm) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.specification = 2

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.02)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 6.0E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_insulated(self):
        """
        (TestCarbonFilm) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for insulated resistors
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.operating_power = 0.113
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 1.0E4
        self.DUT.specification = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.001069402)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 6.4164103E-11)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_non_insulated(self):
        """
        (TestCarbonFilm) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for non-insulated resistors
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.113
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 3.3E5
        self.DUT.specification = 3

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.001818069)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.1)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.19992554E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid_resistance(self):
        """
        (TestCarbonFilm) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with mid-range resistance
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.113
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 3.3E6
        self.DUT.specification = 3

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.001818069)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.6)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.74534624E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_resistance(self):
        """
        (TestCarbonFilm) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with high resistance
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.113
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 3.3E7
        self.DUT.specification = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.001069402)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 2.5)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.604103E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestCarbonFilm) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 1130.0
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 1.1E4

        self.assertTrue(self.DUT.calculate_part())


class TestFilmPowerPowerModel(unittest.TestCase):
    """
    Class for testing the Carbon Film Power resistor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Carbon Film Power resistor class.
        """

        self.DUT = FilmPower()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestCarbonFilmPower) __init__ should return a Carbon Film Power resistor model
        """

        self.assertTrue(isinstance(self.DUT, FilmPower))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Resistor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Carbon Film Power resistor class was properly
        # initialized.
        self.assertEqual(self.DUT._lst_piR, [1.0, 1.2, 1.3, 3.5])
        self.assertEqual(self.DUT._lst_piE, [1.0, 2.0, 10.0, 5.0, 17.0, 6.0,
                                             8.0, 14.0, 18.0, 25.0, 0.5, 14.0,
                                             36.0, 660.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.03, 0.1, 0.3, 1.0, 3.0,
                                                   10.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [1.0, 3.0])
        self.assertEqual(self.DUT._lst_lambdab_count, [0.012, 0.025, 0.13,
                                                       0.062, 0.21, 0.078,
                                                       0.10, 0.19, 0.24, 0.32,
                                                       0.0060, 0.18, 0.47,
                                                       8.2])
        self.assertEqual(self.DUT.subcategory, 27)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestCarbonFilmPower) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.specification = 2

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.21)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 6.3E-9)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_resistance(self):
        """
        (TestCarbonFilmPower) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with low resistance range
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.operating_power = 0.113
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 33.0

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.01274247)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.548494E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid1_resistance(self):
        """
        (TestCarbonFilmPower) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with mid-range resistance
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.113
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 3300.0

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.01274247)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.2)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.0581928E-08)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid2_resistance(self):
        """
        (TestCarbonFilmPower) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with mid-range resistance
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
                               0.01274247)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.3)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.3130422E-08)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_resistance(self):
        """
        (TestCarbonFilmPower) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with high resistance
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
                               0.01274247)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 3.5)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 8.919729E-08)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestCarbonFilmPower) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 1130.0
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 1.1E4

        self.assertTrue(self.DUT.calculate_part())


class TestFilmNetworkModel(unittest.TestCase):
    """
    Class for testing the Carbon Film Network resistor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Carbon Film Network resistor class.
        """

        self.DUT = FilmNetwork()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestCarbonFilmNetwork) __init__ should return a Carbon Film Network resistor model
        """

        self.assertTrue(isinstance(self.DUT, FilmNetwork))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Resistor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Carbon FilmNetwork resistor class was properly
        # initialized.
        self.assertEqual(self.DUT._lst_piE, [1.0, 2.0, 10.0, 5.0, 17.0, 6.0,
                                             8.0, 14.0, 18.0, 25.0, 0.5, 14.0,
                                             36.0, 660.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.03, 0.1, 0.3, 1.0, 3.0,
                                                   10.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [1.0, 3.0])
        self.assertEqual(self.DUT._lst_lambdab_count, [0.0023, 0.0066, 0.031,
                                                       0.013, 0.055, 0.022,
                                                       0.043, 0.077, 0.15,
                                                       0.10, 0.0011, 0.055,
                                                       0.15, 1.7])
        self.assertEqual(self.DUT.subcategory, 28)
        self.assertEqual(self.DUT.n_resistors, 1)
        self.assertEqual(self.DUT.piT, 0.0)
        self.assertEqual(self.DUT.piNR, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestCarbonFilmNetwork) set_attributes should return a 0 error code on success
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
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 8)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.n_resistors, 8)
        self.assertEqual(self.DUT.piT, 0.1)
        self.assertEqual(self.DUT.piNR, 8.0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestCarbonFilmNetwork) set_attributes should return a 40 error code with missing inputs
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
        (TestCarbonFilmNetwork) set_attributes should return a 10 error code with a wrong data type
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
        (TestCarbonFilmNetwork) get_attributes should return a tuple of attribute values
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
                   0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 1, 0.0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestCarbonFilmNetwork) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.055)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.65E-09)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_case_temp_known(self):
        """
        (TestCarbonFilmNetwork) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with case temperature known
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.junction_temperature = 30.0
        self.DUT.operating_power = 0.113
        self.DUT.rated_power = 0.25
        self.DUT.n_resistors = 8

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piNR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.00006)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 1.2518214)
        self.assertEqual(self.DUT.hazard_rate_model['piNR'], 8.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.2017485E-09)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_case_temp_unknown(self):
        """
        (TestCarbonFilmNetwork) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with case temperature unknown
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.junction_temperature = 0.0
        self.DUT.operating_power = 0.113
        self.DUT.rated_power = 0.25
        self.DUT.n_resistors = 8

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piNR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.00006)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 3.4542461)
        self.assertEqual(self.DUT.hazard_rate_model['piNR'], 8.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.3160763E-09)


class TestVarFilmModel(unittest.TestCase):
    """
    Class for testing the VarFilm Variable resistor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the VarFilm Variable resistor class.
        """

        self.DUT = VarFilm()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestVarFilm) __init__ should return a VarFilm Variable resistor model
        """

        self.assertTrue(isinstance(self.DUT, VarFilm))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Resistor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the VarFilm resistor class was properly
        # initialized.
        self.assertEqual(self.DUT._lst_piE, [1.0, 3.0, 14.0, 7.0, 24.0, 6.0,
                                             12.0, 20.0, 30.0, 39.0, 0.5, 22.0,
                                             57.0, 1000.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.03, 0.1, 0.3, 1.0, 3.0,
                                                   10.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [2.0, 4.0])
        self.assertEqual(self.DUT._lst_lambdab_count, [0.048, 0.16, 0.76, 0.36,
                                                       1.3, 0.36, 0.72, 1.4,
                                                       2.2, 2.3, 0.024, 1.2,
                                                       3.4, 52.0])
        self.assertEqual(self.DUT.subcategory, 39)
        self.assertEqual(self.DUT.n_taps, 3)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.piTAPS, 0.0)
        self.assertEqual(self.DUT.piV, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestVarFilm) set_attributes should return a 0 error code on success
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
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 5, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.n_taps, 5)
        self.assertEqual(self.DUT.specification, 1)
        self.assertEqual(self.DUT.piTAPS, 0.75)
        self.assertEqual(self.DUT.piV, 0.3)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestVarFilm) set_attributes should return a 40 error code with missing inputs
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
        (TestVarFilm) set_attributes should return a 10 error code with a wrong data type
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
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 5, '')

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestVarFilm) get_attributes should return a tuple of attribute values
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
                   0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 3, 0, 0.0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestVarFilm) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 1.3)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.9E-08)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_resistance(self):
        """
        (TestVarFilm) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for low resistances
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
        self.DUT.specification = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.03185164)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.3682591E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid1_resistance(self):
        """
        (TestVarFilm) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for mid-range resistances
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.075
        self.DUT.rated_power = 0.25
        self.DUT.rated_voltage = 200.0
        self.DUT.resistance = 1.3E5
        self.DUT.n_taps = 5
        self.DUT.specification = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.03185164)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.2)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.8419110E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid2_resistance(self):
        """
        (TestVarFilm) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with mid-range resistances
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.075
        self.DUT.rated_power = 0.25
        self.DUT.rated_voltage = 200.0
        self.DUT.resistance = 3.3E5
        self.DUT.n_taps = 5
        self.DUT.specification = 2

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.03495881)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.4)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.6390004E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_resistance(self):
        """
        (TestVarFilm) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with high resistance
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.05
        self.DUT.rated_power = 0.25
        self.DUT.rated_voltage = 350.0
        self.DUT.resistance = 1.6E6
        self.DUT.n_taps = 5
        self.DUT.specification = 2

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.03279464)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.8)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 1.05)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.6085265E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestVarFilm) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 1130.0
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 1.1E6
        self.DUT.specification = 1

        self.assertTrue(self.DUT.calculate_part())
