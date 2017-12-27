#!/usr/bin/env python -O
"""
This is the test class for testing Glass capacitor module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestGlass.py is part of The RTK Project
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

from hardware.component.capacitor.fixed.Glass import Glass

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestGlassModel(unittest.TestCase):
    """
    Class for testing the Glass capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Capacitor class.
        """

        self.DUT = Glass()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestGlass) __init__ should return a Glass capacitor model
        """

        self.assertTrue(isinstance(self.DUT, Glass))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Glass capacitor class was properly
        # initialized.
        self.assertEqual(self.DUT._piE, [
            1.0, 2.0, 10.0, 6.0, 16.0, 5.0, 7.0, 22.0, 28.0, 23.0, 0.5, 13.0,
            34.0, 610.0
        ])
        self.assertEqual(self.DUT._piQ,
                         [0.03, 0.10, 0.30, 1.0, 3.0, 3.0, 10.0])
        self.assertEqual(self.DUT._lambdab_count, [
            0.00032, 0.00096, 0.0059, 0.0029, 0.0094, 0.0044, 0.0062, 0.035,
            0.045, 0.020, 0.00016, 0.0076, 0.030, 0.29
        ])
        self.assertEqual(self.DUT.subcategory, 48)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.spec_sheet, 0)
        self.assertEqual(self.DUT.reference_temperature, 398.0)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestGlass) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.specification = 2
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.0094)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.82E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_temp(self):
        """
        (TestGlass) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 85C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 398.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.000214322)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.712496305)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 9.16222391E-12)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_temp(self):
        """
        (TestGlass) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 125C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 473.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               3.1064e-5)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.712496305)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.32797586E-12)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestGlass) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.00000001

        self.assertTrue(self.DUT.calculate_part())

    @attr(all=True, unit=True)
    def test_calculate_217_stress_zero_division(self):
        """
        (TestGlass) calculate_part should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate_part())
