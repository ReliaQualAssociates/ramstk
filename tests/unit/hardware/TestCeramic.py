#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestCeramic.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing Ceramic capacitor module algorithms and models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from hardware.component.capacitor.fixed.Ceramic import Chip, General

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestCeramicChipModel(unittest.TestCase):
    """
    Class for testing the Ceramic Chip capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Capacitor class.
        """

        self.DUT = Chip()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestCeramicChip) __init__ should return a Cermic Chip capacitor model
        """

        self.assertTrue(isinstance(self.DUT, Chip))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Fixed Paper Bypass capacitor class was properly
        # initialized.
        self.assertEqual(self.DUT._piE, [1.0, 2.0, 10.0, 5.0, 17.0, 4.0, 8.0,
                                         16.0, 35.0, 24.0, 0.5, 13.0, 34.0,
                                         610.0])
        self.assertEqual(self.DUT._piQ, [0.03, 0.1, 0.3, 1.0, 3.0, 10.0])
        self.assertEqual(self.DUT._lambdab_count, [0.00078, 0.0022, 0.013,
                                                   0.0056, 0.023, 0.0077,
                                                   0.015, 0.053, 0.12, 0.048,
                                                   0.00039, 0.017, 0.065,
                                                   0.68])
        self.assertEqual(self.DUT.subcategory, 50)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.spec_sheet, 0)
        self.assertEqual(self.DUT.reference_temperature, 358.0)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestCeramicChip) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results for the 85C specification
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.specification = 2
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.023)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 6.9E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_temp(self):
        """
        (TestCeramicChip) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 85C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 358.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.001364472)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.664684671)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 5.44166362E-11)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_temp(self):
        """
        (TestCeramicChip) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 125C specification
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
                               0.000404291)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.664684671)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.61235464E-11)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestCeramicChip) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
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
        (TestCeramicChip) calculate_part should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
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


class TestCeramicGeneralModel(unittest.TestCase):
    """
    Class for testing the General Ceramic capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the General Ceramic capacitor class.
        """

        self.DUT = General()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestCeramicGeneral) __init__ should return a General Ceramic capacitor model
        """

        self.assertTrue(isinstance(self.DUT, General))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the General Ceramic capacitor class was properly initialized.
        self.assertEqual(self.DUT._piE, [1.0, 2.0, 9.0, 5.0, 15.0, 4.0, 4.0,
                                         8.0, 12.0, 20.0, 0.4, 13.0, 34.0,
                                         610.0])
        self.assertEqual(self.DUT._piQ, [0.03, 0.1, 0.3, 1.0, 3.0, 3.0, 10.0])
        self.assertEqual(self.DUT._lambdab_count, [0.0036, 0.0074, 0.034,
                                                   0.019, 0.056, 0.015, 0.015,
                                                   0.032, 0.048, 0.077, 0.0014,
                                                   0.049, 0.13, 2.3])
        self.assertEqual(self.DUT.subcategory, 49)
        self.assertEqual(self.DUT.reference_temperature, 358.0)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestCeramicGeneral) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.056)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.68E-9)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_temp(self):
        """
        (TestCeramicGeneral) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for 85C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 358.0
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.002115542)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 10.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.457334401)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.93502018e-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid_temp(self):
        """
        (TestCeramicGeneral) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for 125C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 398.0
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.00194303)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 10.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.457334401)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.77722929e-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_temp(self):
        """
        (TestCeramicGeneral) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for 150C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 423.0
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.001857542)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 10.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.457334401)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.69903611E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestCeramicGeneral) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000033
        self.DUT.effective_resistance = 0.5
        self.DUT.reference_temperature = 0.00000001

        self.assertTrue(self.DUT.calculate_part())

    @attr(all=True, unit=True)
    def test_calculate_217_stress_zero_division(self):
        """
        (TestCeramicGeneral) calculate_part should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000033
        self.DUT.effective_resistance = 0.5
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate_part())
