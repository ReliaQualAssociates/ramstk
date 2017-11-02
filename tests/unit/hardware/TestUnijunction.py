#!/usr/bin/env python -O
"""
This is the test class for testing Unijunction module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestUnijunction.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr
from hardware.component.semiconductor.transistor.Unijunction import Unijunction

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestUnijunctionModel(unittest.TestCase):
    """
    Class for testing the Unijunction data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Unijunction class.
        """

        self.DUT = Unijunction()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestUnijunction) __init__ should return a Unijunction data model
        """

        self.assertTrue(isinstance(self.DUT, Unijunction))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify the Semiconductor class was properly initialized.
        self.assertEqual(self.DUT.category, 2)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.q_override, 0.0)
        self.assertEqual(self.DUT.piQ, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.piT, 0.0)

        # Verify the Unijunction Transistor class was properly initialized.
        self.assertEqual(self.DUT._lst_piE, [1.0, 6.0, 9.0, 9.0, 19.0, 13.0,
                                             29.0, 20.0, 43.0, 24.0, 0.5, 14.0,
                                             32.0, 320.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.7, 1.0, 2.4, 5.5, 8.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [0.7, 1.0, 2.4, 5.5, 8.0])
        self.assertEqual(self.DUT._lst_lambdab_count, [0.016, 0.12, 0.20, 0.18,
                                                       0.42, 0.35, 0.80, 0.74,
                                                       1.6, 0.66, 0.0079, 0.31,
                                                       0.88, 6.4])
        self.assertEqual(self.DUT.subcategory, 16)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_high_power(self):
        """
        (TestUnijunction) _overstressed should return False and overstress=False on success with operating power greater than rated in a harsh environment
        """

        self.DUT.operating_power = 18.0
        self.DUT.rated_power = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_high_voltage(self):
        """
        (TestUnijunction) _overstressed should return False and overstress=False on success with operating voltage greater than rated in a harsh environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_voltage = 22.8
        self.DUT.rated_voltage = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_high_temperature(self):
        """
        (TestUnijunction) _overstressed should return False and overstress=False on success with junction temperature greater than 125C in a harsh environment
        """

        self.DUT.junction_temperature = 135.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_mild_env_high_power(self):
        """
        (TestUnijunction) _overstressed should return False and overstress=False on success with operating power greater than rated in a mild environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_power = 23.0
        self.DUT.rated_power = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_mild_env_high_voltage(self):
        """
        (TestUnijunction) _overstressed should return False and overstress=False on success with operating voltage greater than rated in a mild environment
        """

        self.DUT.operating_voltage = 23.0
        self.DUT.rated_voltage = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestUnijunction) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.42)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.7)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.94E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestUnijunction) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for a Unijunction transistor
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.junction_temperature = 32.0

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piQ * piE')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.0083)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 1.2107393)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.7)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.2206372E-08)
