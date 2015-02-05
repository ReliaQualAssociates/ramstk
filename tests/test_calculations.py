#!/usr/bin/env python -O
"""
This is the test class for testing general calculation algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       test_calculations.py is part of The RTK Project
#
# All rights reserved.

import unittest

import os
import sys
sys.path.insert(0, os.path.abspath(".."))

from rtk.calculations import beta_bounds, calculate_field_ttf, \
    dormant_hazard_rate


class TestCalculations(unittest.TestCase):
    """
    Class for testing general calculations.
    """

    def test_field_ttf(self):
        """
        Method to test the calculation of times to failure based on start and
        end dates.
        """

        self.assertEqual(calculate_field_ttf(("2014-01-01", "2014-01-15")),
                         14.0)

    def test_beta_bounds(self):
        """
        Method to test the calculation of beta parameters.
        """

        self.assertAlmostEqual(beta_bounds(10.0, 20.0, 40.0, 0.9)[0],
                               13.44239853)

        self.assertAlmostEqual(beta_bounds(10.0, 20.0, 40.0, 0.9)[1],
                               21.66666666)

        self.assertAlmostEqual(beta_bounds(10.0, 20.0, 40.0, 0.9)[2],
                               29.89093480)

        self.assertAlmostEqual(beta_bounds(10.0, 20.0, 40.0, 0.9)[3],
                               5.0)

        self.assertAlmostEqual(beta_bounds(10.0, 20.0, 40.0, 90.0)[0],
                               13.44239853)

        self.assertAlmostEqual(beta_bounds(10.0, 20.0, 40.0, 90.0)[1],
                               21.66666666)

        self.assertAlmostEqual(beta_bounds(10.0, 20.0, 40.0, 90.0)[2],
                               29.89093480)

        self.assertAlmostEqual(beta_bounds(10.0, 20.0, 40.0, 90.0)[3],
                               5.0)

    def test_capacitor_dormant_hazard_rates(self):
        """
        Method to test dormant hazard rate calculations for capacitors.
        """

        # Ground to ground.
        self.assertEqual(dormant_hazard_rate(1, 1, 1, 1, 1), 0.05)
        # Naval to ground
        self.assertEqual(dormant_hazard_rate(1, 1, 4, 1, 1), 0.03)
        # Naval to naval
        self.assertEqual(dormant_hazard_rate(1, 1, 4, 2, 1), 0.05)
        # Airborne to ground
        self.assertEqual(dormant_hazard_rate(1, 1, 6, 1, 1), 0.02)
        # Airborne to airborne
        self.assertEqual(dormant_hazard_rate(1, 1, 6, 3, 1), 0.06)
        # Space to ground
        self.assertEqual(dormant_hazard_rate(1, 1, 11, 1, 1), 1.0)
        # Space to space
        self.assertEqual(dormant_hazard_rate(1, 1, 11, 4, 1), 0.2)

    def test_connection_dormant_hazard_rates(self):
        """
        Method to test dormant hazard rate calculations for connections.
        """

        # Ground to ground.
        self.assertEqual(dormant_hazard_rate(2, 1, 1, 1, 1), 0.2)
        # Naval to ground
        self.assertEqual(dormant_hazard_rate(2, 1, 4, 1, 1), 0.08)
        # Naval to naval
        self.assertEqual(dormant_hazard_rate(2, 1, 4, 2, 1), 0.3)
        # Airborne to ground
        self.assertEqual(dormant_hazard_rate(2, 1, 6, 1, 1), 0.04)
        # Airborne to airborne
        self.assertEqual(dormant_hazard_rate(2, 1, 6, 3, 1), 0.2)
        # Space to ground
        self.assertEqual(dormant_hazard_rate(2, 1, 11, 1, 1), 0.9)
        # Space to space
        self.assertEqual(dormant_hazard_rate(2, 1, 11, 4, 1), 0.4)
