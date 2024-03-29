#!/usr/bin/env python -O
"""
This is the test class for testing SPLAN model algorithms.
"""

# Standard Library Imports
# -*- coding: utf-8 -*-
#
#       tests.statistics.TestSPLAN.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import sys
import unittest
from os.path import dirname

# Third Party Imports
import numpy as np
from analyses.statistics.growth.SPLAN import (
    calculate_fef,
    calculate_growth_potential,
    calculate_management_strategy,
    calculate_probability,
)
from nose.plugins.attrib import attr

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/ramstk",
)


__author__ = "Doyle Rowland"
__email__ = "doyle.rowland@reliaqual.com"
__organization__ = "ReliaQual Associates, LLC"
__copyright__ = 'Copyright 2015 Doyle "weibullguy" Rowland'


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
