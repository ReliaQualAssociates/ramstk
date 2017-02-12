#!/usr/bin/env python -O
"""
This is the test class for testing SPLAN model algorithms.
"""

# -*- coding: utf-8 -*-
#
#       tests.statistics.TestSPLAN.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr
import numpy as np

from analyses.statistics.growth.SPLAN import calculate_fef, \
                                             calculate_growth_potential, \
                                             calculate_management_strategy, \
                                             calculate_probability

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestCrowAMSAA(unittest.TestCase):
    """
    Class for testing the SPLAN model functions.
    """

    @attr(all=True, unit=True)
    def test01_calculate_management_strategy(self):
        """
        (TestSPLAN) calculate_management_strategy should return a float value when calculating the average management strategy for the overall program
        """

        _avg_ms = calculate_management_strategy(0.7, 50.0, 110.0)
        self.assertAlmostEqual(_avg_ms, 0.7792208)

    @attr(all=True, unit=True)
    def test01a_calculate_management_strategy_zero_fef(self):
        """
        (TestSPLAN) calculate_management_strategy should return 1.0 when calculating the average management strategy and the FEF equals 0.0
        """

        _avg_ms = calculate_management_strategy(0.0, 50.0, 110.0)
        self.assertAlmostEqual(_avg_ms, 1.0)

    @attr(all=True, unit=True)
    def test01b_calculate_management_strategy_zero_mtbfgp(self):
        """
        (TestSPLAN) calculate_management_strategy should return 1.0 when calculating the average management strategy and the goal MTBF equals 0.0
        """

        _avg_ms = calculate_management_strategy(0.7, 50.0, 0.0)
        self.assertAlmostEqual(_avg_ms, 1.0)

    @attr(all=True, unit=True)
    def test02_calculate_probability(self):
        """
        (TestSPLAN) calculate_probability should return a float value when calculating the probability of observing a failure
        """

        _prob1 = calculate_probability(1000.0, 0.95, 45.0)
        _prob2 = calculate_probability(1500.0, 0.90, 64.9350649)
        _prob3 = calculate_probability(2500.0, 0.90, 80.1688181)
        _prob4 = calculate_probability(2000.0, 0.85, 94.0247917)
        _prob5 = calculate_probability(3000.0, 0.75, 101.5902031)
        self.assertAlmostEqual(_prob1, 0.999999999321483)
        self.assertAlmostEqual(_prob2, 0.999999999321483)
        self.assertAlmostEqual(_prob3, 0.999999999321483)
        self.assertAlmostEqual(_prob4, 0.999999999321483)
        self.assertAlmostEqual(_prob5, 0.999999999321483)

    @attr(all=True, unit=True)
    def test02a_calculate_probability_zero_mtbfi(self):
        """
        (TestSPLAN) calculate_probability should return 0.0 when calculating the probability of observing a failure and the initial MTBF equals zero
        """

        _prob = calculate_probability(1000.0, 0.95, 0.0)
        self.assertAlmostEqual(_prob, 0.0)

    @attr(all=True, unit=True)
    def test03_calculate_growth_potential(self):
        """
        (TestSPLAN) calculate_growth_potential should return a float value when calculating the growth potential
        """

        _mtbfgp = calculate_growth_potential(50.0, 0.779, 0.95)
        self.assertAlmostEqual(_mtbfgp, 192.3446817)

    @attr(all=True, unit=True)
    def test03a_calculate_growth_potential_unity_ms_fef(self):
        """
        (TestSPLAN) calculate_growth_potential should return 0.0 when calculating the growth potential and both the MS and FEF are equal to one
        """

        _mtbfgp = calculate_growth_potential(50.0, 1.0, 1.0)
        np.testing.assert_equal(_mtbfgp, np.inf)

    @attr(all=True, unit=True)
    def test04_calculate_fef(self):
        """
        (TestSPLAN) calculate_fef should return a float value on success
        """

        _fef = calculate_fef(0.95, 50.0, 150.0)
        self.assertAlmostEqual(_fef, 0.7017544)

    @attr(all=True, unit=True)
    def test04a_calculate_fef_no_ms(self):
        """
        (TestSPLAN) calculate_fef should return 1.0 when the management strategy equals 0.0
        """

        _fef = calculate_fef(0.0, 50.0, 150.0)
        self.assertEqual(_fef, 1.0)

    @attr(all=True, unit=True)
    def test04b_calculate_fef_no_mtbfgp(self):
        """
        (TestSPLAN) calculate_fef should return 1.0 when the growth potential MTBF equals 0.0
        """

        _fef = calculate_fef(0.95, 50.0, 0.0)
        self.assertEqual(_fef, 1.0)
