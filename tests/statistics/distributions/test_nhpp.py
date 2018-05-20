#!/usr/bin/env python -O
"""
This is the test class for testing NHPP model algorithms.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tests.statistics.TestNHPP.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
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

import unittest
from nose.plugins.attrib import attr
import numpy as np

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk",
)

import dao.DAO as _dao
from analyses.statistics.NHPP import *


class TestNHPP(unittest.TestCase):
    """
    Class for testing the NHPP functions.
    """

    def setUp(self):
        """
        Setup the test fixture for the Reliability Growth class.
        """

        # Data used to test NHPP model algorithms.  This is the data from
        # example #2 at http://www.reliawiki.org/index.php/Duane_Model
        self.DUANE_FAILS = [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        ]
        self.DUANE_TIMES = [
            9.2, 25, 61.5, 260, 300, 710, 916, 1010, 1220, 2530, 3350, 4200,
            4410, 4990, 5570, 8310, 8530, 9200, 10500, 12100, 13400, 14600,
            22000
        ]

        self.CROW_EXACT_FAILS = [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        ]
        self.CROW_EXACT_TIMES = [
            2.7, 10.3, 12.5, 30.6, 57.0, 61.3, 80.0, 109.5, 125.0, 128.6,
            143.8, 167.9, 229.2, 296.7, 320.6, 328.2, 366.2, 396.7, 421.1,
            438.2, 501.2, 620.0
        ]

        # Data is U.S.S. Halfbeak Number 4 Main Propulsion Diesel Engine
        # unscheduled maintenance action times from Meeker and Escobar.
        self.HALFBEAK_FAILS = [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1
        ]
        self.HALFBEAK_TIMES = [
            1.382, 2.990, 4.124, 6.827, 7.472, 7.567, 8.845, 9.450, 9.794,
            10.848, 11.993, 12.300, 15.413, 16.497, 17.352, 17.632, 18.122,
            19.067, 19.172, 19.299, 19.360, 19.686, 19.940, 19.944, 20.121,
            20.132, 20.431, 20.525, 21.057, 21.061, 21.309, 21.310, 21.378,
            21.391, 21.456, 21.461, 21.603, 21.658, 21.688, 21.750, 21.815,
            21.820, 21.822, 21.888, 21.930, 21.943, 21.946, 22.181, 22.311,
            22.634, 22.635, 22.669, 22.691, 22.846, 22.947, 23.149, 23.305,
            23.491, 23.526, 23.774, 23.791, 23.822, 24.006, 24.286, 25.000,
            25.010, 25.048, 25.268, 25.400, 25.500, 25.518
        ]

    @attr(all=True, unit=True)
    def test_nhpp_power_law_mle_model_fisher_bounds(self):
        """
        (TestNHPP) power_law should return a list of parameter estimates when using MLE and Fisher bounds.
        """

        # Check the value of beta and alpha for exact failure times using MLE
        # and 90% two-sided confidence bounds.
        _results = power_law(
            self.CROW_EXACT_FAILS,
            self.CROW_EXACT_TIMES,
            3,
            fitmeth=1,
            conftype=3,
            alpha=0.90)[0]
        self.assertAlmostEqual(_results[0], 0.1392834)
        self.assertAlmostEqual(_results[1], 0.4239422)
        self.assertAlmostEqual(_results[2], 1.2903691)

        _results = power_law(
            self.CROW_EXACT_FAILS,
            self.CROW_EXACT_TIMES,
            3,
            fitmeth=1,
            conftype=3,
            alpha=0.90)[1]
        self.assertAlmostEqual(_results[0], 0.4673647)
        self.assertAlmostEqual(_results[1], 0.6142104)
        self.assertAlmostEqual(_results[2], 0.8071950)

    @attr(all=True, unit=True)
    def test_nhpp_power_law_mle_model_fisher_bounds_alpha_big(self):
        """
        (TestNHPP) power_law should return a list of parameter estimates when using MLE and Fisher bounds when passing a confidence level > 1.
        """

        # Check the value of beta and alpha for exact failure times using MLE
        # and 90% two-sided confidence bounds.
        _results = power_law(
            self.CROW_EXACT_FAILS,
            self.CROW_EXACT_TIMES,
            3,
            fitmeth=1,
            conftype=3,
            alpha=90)[0]
        self.assertAlmostEqual(_results[0], 0.1392834)
        self.assertAlmostEqual(_results[1], 0.4239422)
        self.assertAlmostEqual(_results[2], 1.2903691)

    @attr(all=True, unit=True)
    def test_nhpp_power_law_mle_model_crow_bounds(self):
        """
        (TestNHPP) power_law should return a list of parameter estimates when using MLE and Crow bounds.
        """

        # Check the value of beta and alpha for exact failure times using MLE
        # and 90% two-sided confidence bounds.
        self.assertEqual(
            power_law(
                self.CROW_EXACT_FAILS,
                self.CROW_EXACT_TIMES,
                1,
                fitmeth=1,
                conftype=1,
                alpha=0.90)[0],
            [0.25541847073060886, 0.42394221488057504, 0.53723575463327322])

        self.assertEqual(
            power_law(
                self.CROW_EXACT_FAILS,
                self.CROW_EXACT_TIMES,
                1,
                fitmeth=1,
                conftype=1,
                alpha=0.90)[1],
            [0.44689920652489762, 0.6142103999317297, 0.95873467356157016])

    @attr(all=True, unit=True)
    def test_nhpp_power_law_mle_model_crow_bounds_type_ii(self):
        """
        (TestNHPP) power_law should return a list of parameter estimates when using MLE and Crow bounds with failure truncated data.
        """

        # Check the value of beta and alpha for exact failure times using MLE
        # and 90% two-sided confidence bounds.
        self.assertEqual(
            power_law(
                self.CROW_EXACT_FAILS,
                self.CROW_EXACT_TIMES,
                1,
                fitmeth=1,
                conftype=1,
                alpha=0.90,
                t_star=620.0)[0],
            [0.27116933362118567, 0.42394221488057504, 0.56002802891429937])

    @attr(all=True, unit=True)
    def test_nhpp_power_law_regression_models(self):
        """
        (TestNHPP) power_law should return a list of parameter estimates when using regression and Fisher bounds.
        """

        # Check the value of alpha (scale) and beta (shape) for exact failure
        # times using regression and 90% two-sided confidence bounds.
        self.assertEqual(
            power_law(
                self.DUANE_FAILS,
                self.DUANE_TIMES,
                3,
                fitmeth=2,
                conftype=3,
                alpha=0.90)[0],
            [0.45881779062955202, 0.51396363200664490, 0.57573751589493760])
        self.assertEqual(
            power_law(
                self.DUANE_FAILS,
                self.DUANE_TIMES,
                3,
                fitmeth=2,
                conftype=3,
                alpha=0.90)[1],
            [0.37222330715953877, 0.3867662537771597, 0.40130920039478057])

    @attr(all=True, unit=False)
    def test_nhpp_loglinear_model_fisher_bounds(self):
        """
        (TestNHPP) power_law should return a list of parameter estimates when using MLE and Fisher bounds.
        """

        # Check the value of beta and alpha for exact failure times using MLE
        # and 90% two-sided confidence bounds.
        self.assertEqual(
            loglinear(
                self.HALFBEAK_FAILS,
                self.HALFBEAK_TIMES,
                3,
                conftype=3,
                alpha=0.90), [[0.0, -1.43, 0.0], [0.0, 0.149, 0.0]])

        #self.assertEqual(power_law(self.CROW_EXACT_FAILS,
        #                           self.CROW_EXACT_TIMES,
        #                           3, fitmeth=1, conftype=3, alpha=0.90)[1],
        #                 [0.46736466889703443,
        #                  0.6142103999317297,
        #                  0.8071949817571866])
