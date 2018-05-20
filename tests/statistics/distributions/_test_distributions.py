#!/usr/bin/env python -O
"""
This is the test class for testing the statistical distributions module
algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.statistics.TestDistributions.py is part of The RTK Project
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
import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk",
)

import unittest
from nose.plugins.attrib import attr

import numpy as np

from analyses.statistics.Distributions import Exponential, Gaussian, \
                                              LogNormal, Weibull, \
                                              time_between_failures
from survival.Record import Model as Record

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestExponentialDistribution(unittest.TestCase):
    """
    Class for testing the Exponential distribution data model class.
    """

    # Data set of 100 exponentially distributed points with a mean of 100.
    EXP_TEST = np.array(
        [[1.585, 1.585, 1, 1, 1.585], [1.978, 1.978, 1, 1,
                                       1.978], [2.81, 2.81, 1, 1, 2.81],
         [3.679, 3.679, 1, 1, 3.679], [4.248, 4.248, 1, 1, 4.248], [
             5.137, 5.137, 1, 1, 5.137
         ], [5.566, 5.566, 1, 1, 5.566], [6.328, 6.328, 1, 1, 6.328],
         [7.876, 7.876, 1, 1, 7.876], [10.79, 10.79, 1, 1, 10.79], [
             12.398, 12.398, 1, 1, 12.398
         ], [13.095, 13.095, 1, 1, 13.095], [13.64, 13.64, 1, 1, 13.64], [
             14.003, 14.003, 1, 1, 14.003
         ], [14.259, 14.259, 1, 1, 14.259], [14.558, 14.558, 1, 1, 14.558], [
             14.808, 14.808, 1, 1, 14.808
         ], [14.848, 14.848, 1, 1, 14.848], [16.452, 16.452, 1, 1, 16.452], [
             17.743, 17.743, 1, 1, 17.743
         ], [18.793, 18.793, 1, 1, 18.793], [18.917, 18.917, 1, 1, 18.917], [
             19.664, 19.664, 1, 1, 19.664
         ], [20.564, 20.564, 1, 1, 20.564], [28.693, 28.693, 1, 1, 28.693], [
             34.931, 34.931, 1, 1, 34.931
         ], [35.461, 35.461, 1, 1, 35.461], [36.169, 36.169, 1, 1, 36.169], [
             37.765, 37.765, 1, 1, 37.367
         ], [38.951, 38.951, 1, 1, 38.951], [39.576, 39.576, 1, 1, 39.576], [
             40.36, 40.36, 1, 1, 40.36
         ], [41.559, 41.559, 1, 1, 41.559], [42.486, 42.486, 1, 1, 42.486], [
             46.984, 46.984, 1, 1, 46.984
         ], [48.146, 48.146, 1, 1, 48.146], [48.398, 48.398, 1, 1, 48.398], [
             49.315, 49.315, 1, 1, 49.315
         ], [49.364, 49.364, 1, 1, 49.364], [49.76, 49.76, 1, 1, 49.76], [
             49.855, 49.855, 1, 1, 49.855
         ], [52.315, 52.315, 1, 1, 52.315], [52.885, 52.885, 1, 1, 52.885], [
             53.127, 53.127, 1, 1, 53.127
         ], [53.18, 53.18, 1, 1, 53.18], [54.07, 54.07, 1, 1, 54.07], [
             58.595, 58.595, 1, 1, 58.595
         ], [61.993, 61.993, 1, 1, 61.993], [65.542, 65.542, 1, 1, 65.542], [
             66.69, 66.69, 1, 1, 66.69
         ], [66.864, 66.864, 1, 1, 66.864], [67.342, 67.342, 1, 1, 67.342], [
             69.776, 69.776, 1, 1, 69.776
         ], [71.048, 71.048, 1, 1, 71.048], [74.057, 74.057, 1, 1, 74.057], [
             75.549, 75.549, 1, 1, 75.549
         ], [77.095, 77.095, 1, 1, 77.095], [78.747, 78.747, 1, 1, 78.747], [
             80.172, 80.172, 1, 1, 80.172
         ], [82.16, 82.16, 1, 1, 82.16], [82.223, 82.223, 1, 1, 82.223], [
             86.769, 86.769, 1, 1, 86.769
         ], [87.229, 87.229, 1, 1, 87.229], [88.862, 88.862, 1, 1, 88.862], [
             89.103, 89.103, 1, 1, 89.103
         ], [94.072, 94.072, 1, 1, 94.072], [96.415, 96.415, 1, 1, 96.415], [
             101.977, 101.977, 1, 1, 101.977
         ], [111.147, 111.147, 1, 1, 111.147], [
             115.532, 115.532, 1, 1, 115.532
         ], [120.144, 120.144, 1, 1, 120.144], [
             121.963, 121.963, 1, 1, 121.963
         ], [134.763, 134.763, 1, 1, 134.763], [
             137.072, 137.072, 1, 1, 137.072
         ], [141.988, 141.988, 1, 1, 141.988], [
             143.687, 143.687, 1, 1, 143.687
         ], [143.918, 143.918, 1, 1, 143.918], [148.07, 148.07, 1, 1, 148.07],
         [158.98, 158.98, 1, 1, 158.98], [159.732, 159.732, 1, 1, 159.732], [
             163.827, 163.827, 1, 1, 163.827
         ], [169.175, 169.175, 1, 1, 169.175], [
             171.813, 171.813, 1, 1, 171.813
         ], [172.663, 172.663, 1, 1, 172.663], [
             177.992, 177.992, 1, 1, 177.992
         ], [184.263, 184.263, 1, 1, 184.263], [
             185.254, 185.254, 1, 1, 185.254
         ], [194.039, 194.039, 1, 1, 194.039], [
             212.279, 212.279, 1, 1, 212.279
         ], [222.93, 222.93, 1, 1,
             222.93], [226.918, 226.918, 1, 1, 226.918], [
                 241.044, 241.044, 1, 1, 241.044
             ], [263.548, 263.548, 1, 1,
                 263.548], [275.491, 275.491, 1, 1, 275.491], [
                     294.418, 294.418, 1, 1, 294.418
                 ], [297.467, 297.467, 1, 1,
                     297.467], [317.922, 317.922, 1, 1,
                                317.922], [323.763, 323.763, 1, 1, 323.763], [
                                    350.577, 350.577, 1, 1, 350.577
                                ], [351.347, 351.347, 1, 1, 351.347]])

    # Data set of alpha particle interarrival times.  Data is from Table 7.1 in
    # Meeker and Escobar.
    ALPHA = np.array(
        [[0.0, 100.0, 1609, 4, 50.0], [100.0, 300.0, 2424, 4, 200.0],
         [300.0, 500.0, 1770, 4, 400.0], [500.0, 700.0, 1306, 4, 600.0],
         [700.0, 1000.0, 1213, 4, 850.0], [1000.0, 2000.0, 1528, 4, 1500.0],
         [2000.0, 4000.0, 354, 4, 3000.0], [4000.0, np.inf, 16, 2, np.inf]])

    def setUp(self):
        """
        Setup the test fixture for the Exponential distribution class.
        """

        self.DUT = Exponential()

    @attr(all=True, unit=True)
    def test01_log_pdf(self):
        """
        (TestExponentialDistribution) log_pdf should return a numpy array of floats on success
        """

        # Data is the same as that used in the ReliaSoft wiki examples.
        # The table can be found at the following URL, for example.
        # http://reliawiki.org/index.php/The_Lognormal_Distribution#Rank_Regression_on_Y
        # lambda = 0.02711 and rho = -0.9679 when fit to the EXP.
        _data = np.array([['', 0.0, 5.0, 0, 1, 1], ['', 0.0, 10.0, 0, 1, 1], [
            '', 0.0, 15.0, 0, 1, 1
        ], ['', 0.0, 20.0, 0, 1,
            1], ['', 0.0, 25.0, 0, 1, 1], ['', 0.0, 30.0, 0, 1, 1], [
                '', 0.0, 35.0, 0, 1, 1
            ], ['', 0.0, 40.0, 0, 1,
                1], ['', 0.0, 50.0, 0, 1, 1], ['', 0.0, 60.0, 0, 1, 1],
                          ['', 0.0, 70.0, 0, 1, 1], ['', 0.0, 80.0, 0, 1, 1],
                          ['', 0.0, 90.0, 0, 1, 1], ['', 0.0, 100.0, 0, 1, 1]])

        _log_pdf = self.DUT.log_pdf(
            np.array(_data[:, 2], dtype=float), 0.02222222, 0.0)

        np.testing.assert_allclose(_log_pdf, [
            -3.91777369, -4.02888479, -4.13999589, -4.25110699, -4.36221809,
            -4.47332919, -4.58444029, -4.69555139, -4.91777359, -5.13999579,
            -5.36221799, -5.58444019, -5.80666239, -6.02888459
        ])

    @attr(all=True, unit=True)
    def test02_partial_derivatives_exact(self):
        """
        (TestExponentialDistribution) partial_derivatives should return a numpy array with exact data only on success.
        """

        # Leukemia remission times.  Data is from Example 7.2 of Lee and Wang.
        _data = np.array(
            [[0.0, 1.0, 1, 1], [0.0, 1.0, 1, 1], [0.0, 2.0, 1, 1],
             [0.0, 2.0, 1, 1], [0.0, 3.0, 1, 1], [0.0, 4.0, 1, 1],
             [0.0, 4.0, 1, 1], [0.0, 5.0, 1, 1], [0.0, 5.0, 1, 1], [
                 0.0, 6.0, 1, 1
             ], [0.0, 8.0, 1, 1], [0.0, 8.0, 1, 1], [0.0, 9.0, 1, 1], [
                 0.0, 10.0, 1, 1
             ], [0.0, 10.0, 1, 1], [0.0, 12.0, 1, 1], [0.0, 14.0, 1, 1], [
                 0.0, 16.0, 1, 1
             ], [0.0, 20.0, 1, 1], [0.0, 24.0, 1, 1], [0.0, 34.0, 1, 1]])

        _part_deriv = self.DUT.partial_derivatives(1.0, _data)
        self.assertAlmostEqual(_part_deriv, -177.0)

    @attr(all=True, unit=True)
    def test02a_partial_derivatives_right(self):
        """
        (TestExponentialDistribution) partial_derivatives should return a numpy array with exact and right censored data on success.
        """

        # Cancerous mice data.  Data is from Example 7.3 in Lee and Wang.
        _data = np.array(
            [[0.0, 4.0, 1, 1], [0.0, 5.0, 1, 1], [0.0, 8.0, 1, 1],
             [0.0, 9.0, 1, 1], [0.0, 10.0, 1, 1], [0.0, 10.0, 1, 2],
             [0.0, 10.0, 1, 2], [0.0, 10.0, 1, 2], [0.0, 10.0, 1,
                                                    2], [0.0, 10.0, 1, 2]])

        _part_deriv = self.DUT.partial_derivatives(1.0, _data)
        self.assertAlmostEqual(_part_deriv, -81.0)

    @attr(all=True, unit=True)
    def test02b_partial_derivs_interval(self):
        """
        (TestExponentialDistribution) partial_derivatives should return a numpy array with exact, right, and interval censored data on success.
        """

        # Danish AIDS patients.  Data retrieved from:
        # https://encrypted.google.com/books?id=Jwf3M6TtHTkC&pg=PA33&lpg=PA33&dq=exponential+data+set+example+with+interval+censoring&source=bl&ots=_VK8lx0yqP&sig=zbUtQTK8ZHR10Y5LDA_0aZz_OqI&hl=en&sa=X&ei=ekqwU8mWBtCGqgb204LwDw&ved=0CH4Q6AEwCQ#v=onepage&q=exponential%20data%20set%20example%20with%20interval%20censoring&f=false
        _data = np.array(
            [[0.0, 24.0, 24, 3], [24.0, 39.0, 1, 3], [24.0, 113.0, 4, 3],
             [28.0, 88.0, 1, 3], [39.0, 113.0, 2, 3], [57.0, 113.0, 1, 3], [
                 0.0, 39.0, 2, 3
             ], [24.0, 57.0, 10, 3], [24.0, 28.0, 4, 3], [24.0, 88.0, 3, 3],
             [28.0, 39.0, 4, 3], [39.0, 57.0, 3, 3], [57.0, 88.0, 5, 3], [
                 88.0, 113.0, 1, 3
             ], [0.0, 88.0, 34, 2], [0.0, 24.0, 61, 2], [0.0, 28.0, 8, 2],
             [0.0, 39.0, 15, 2], [0.0, 57.0, 22, 2], [0.0, 113.0, 92, 2]])

        # Parameter is 0.0034 for exponential.
        _part_deriv = self.DUT.partial_derivatives(0.0034, _data)
        self.assertAlmostEqual(_part_deriv, -115.5080488)

    @attr(all=True, unit=True)
    def test03_maximum_likelihood_estimate_exact_times(self):
        """
        (TestExponentialDistribution) maximum_likelihood_estimate should return a numpy array of floats on success with exact failure times.
        """

        _fit = self.DUT.maximum_likelihood_estimate(self.EXP_TEST, 0.0,
                                                    10000000.0)

        # Check the mean for exact failure time data.
        self.assertAlmostEqual(_fit[0][0], 0.01062350)

        # Check the variance for exact failure time data.
        self.assertAlmostEqual(_fit[1][0], 1.1530528E-06)

        # Check the goodness of fit statistics for exact failure time data.
        self.assertAlmostEqual(_fit[2][0], -554.4686898)  # Log-likelihood
        self.assertAlmostEqual(_fit[2][1], 1110.9373796)  #
        self.assertAlmostEqual(_fit[2][2], 1112.3978199)  #

    @attr(all=True, unit=True)
    def test03a_maximum_likelihood_estimate_interval_censored(self):
        """
        (TestExponentialDistribution) maximum_likelihood_estimate should return a numpy array of floats on success with interval censored failure times.
        """

        _fit = self.DUT.maximum_likelihood_estimate(self.ALPHA, 0.0,
                                                    10000000.0)

        # Check the mean for interval censored failure time data.
        np.testing.assert_array_equal(_fit[0], [0.0016958399594908262, 0.0])

        # Check the variance for interval censored failure time data.
        np.testing.assert_array_equal(_fit[1],
                                      [4.1646989502606359e-07, 0.0, 0.0])

        # Check the goodness of fit for interval censored failure time data.
        np.testing.assert_array_equal(
            _fit[2],
            [6547.2989156021813, -13092.597831204363, -13093.796650941156])

    @attr(all=True, unit=True)
    def test04_theoretical_distribution(self):
        """
        (TestExponentialDistribution) theoretical_distribution should return a numpy array of floats on success.
        """

        _para = [0.0106235]

        _data = [x[1] for x in self.EXP_TEST]
        _probs = self.DUT.theoretical_distribution(np.array(_data), _para)
        np.testing.assert_almost_equal(_probs, [
            0.01669728, 0.02079404, 0.02941086, 0.03832994, 0.04412548,
            0.05311054, 0.05741615, 0.06501567, 0.08026591, 0.10830182,
            0.12340496, 0.12987181, 0.13489513, 0.13822483, 0.14056535,
            0.14329095, 0.14556324, 0.14592625, 0.16035645, 0.17179350,
            0.18098054, 0.18205874, 0.18852403, 0.19624570, 0.26274399,
            0.31001780, 0.31389180, 0.31903296, 0.33048150, 0.33886416,
            0.34323935, 0.34868668, 0.35693022, 0.36323208, 0.39294418,
            0.40039192, 0.40199499, 0.40779232, 0.40810052, 0.41058535,
            0.41117991, 0.42636869, 0.42983176, 0.43129571, 0.43161583,
            0.43696453, 0.46339015, 0.48241558, 0.50156667, 0.50760853,
            0.50851787, 0.51100731, 0.52348941, 0.52988523, 0.54467532,
            0.55183544, 0.55913595, 0.56680563, 0.57331415, 0.58223105,
            0.58251057, 0.60219386, 0.60413312, 0.61094146, 0.61193628,
            0.63189015, 0.64093963, 0.66154112, 0.69295782, 0.70693305,
            0.72094595, 0.72628666, 0.76108674, 0.76687591, 0.77873839,
            0.78269619, 0.78322880, 0.79258251, 0.81528183, 0.81675164,
            0.82455262, 0.83424270, 0.83882353, 0.84027239, 0.84906379,
            0.85879153, 0.86027036, 0.87272094, 0.89514176, 0.90635993,
            0.91024427, 0.92275174, 0.93917791, 0.94642532, 0.95618371,
            0.95758023, 0.96586542, 0.96791916, 0.97587134, 0.97606791
        ])

    @attr(all=True, unit=True)
    def test05_hazard_function(self):
        """
        (TestExponentialDistribution) hazard_function should return a dict on success.
        """

        _para = [0.0101382, 0.0106235, 0.0113429]

        _hazard = self.DUT.hazard_function(_para, 0, 10, 1)
        self.assertEqual(
            _hazard, {
                0: _para,
                1: _para,
                2: _para,
                3: _para,
                4: _para,
                5: _para,
                6: _para,
                7: _para,
                8: _para,
                9: _para
            })

    @attr(all=True, unit=True)
    def test06_mean(self):
        """
        (TestExponentialDistribution) mean should return a dict on success.
        """

        _para = [0.0101382, 0.0106235, 0.0113429]

        _hazard = self.DUT.mean(_para, 0, 10, 1)
        self.assertEqual(
            _hazard, {
                0: [88.1608759664636, 94.13093613215985, 98.63683888658737],
                1: [88.1608759664636, 94.13093613215985, 98.63683888658737],
                2: [88.1608759664636, 94.13093613215985, 98.63683888658737],
                3: [88.1608759664636, 94.13093613215985, 98.63683888658737],
                4: [88.1608759664636, 94.13093613215985, 98.63683888658737],
                5: [88.1608759664636, 94.13093613215985, 98.63683888658737],
                6: [88.1608759664636, 94.13093613215985, 98.63683888658737],
                7: [88.1608759664636, 94.13093613215985, 98.63683888658737],
                8: [88.1608759664636, 94.13093613215985, 98.63683888658737],
                9: [88.1608759664636, 94.13093613215985, 98.63683888658737]
            })

    @attr(all=True, unit=True)
    def test07_reliability_function(self):
        """
        (TestExponentialDistribution) reliability_function should return a dict on success.
        """

        _para = [0.0101382, 0.0106235, 0.0113429]

        _reliability = self.DUT.reliability_function(_para, 0, 10, 1)
        self.assertEqual(
            _reliability, {
                0: [1.0, 1.0, 1.0],
                1: [
                    0.98991301831630807, 0.98943273007988608,
                    0.98872118814618748
                ],
                2: [
                    0.97992778383210333, 0.97897712735333664,
                    0.97756958788920878
                ],
                3:
                [0.97004327022524806, 0.9686320118029762, 0.9665437644333974],
                4:
                [0.9602584615260974, 0.95839621588099111, 0.95564229916587751],
                5: [
                    0.95057235201307344, 0.94826858437736083,
                    0.94486378947404071
                ],
                6:
                [0.9409839461092937, 0.93824797428948092, 0.93420684856508274],
                7: [
                    0.93149225828024107, 0.92833325469316386,
                    0.92367010528757409
                ],
                8: [
                    0.92209631293246741, 0.91852330661500337,
                    0.91325220395504447
                ],
                9: [
                    0.91279514431331776, 0.90881702290608701,
                    0.90295180417155596
                ]
            })


class TestGaussianDistribution(unittest.TestCase):
    """
    Class for testing the Gaussian distribution data model class.
    """

    # Data set of 100 normally distributed points a mean of 100.0 and a
    # variance of 10.0
    NORM_TEST = np.array([[95.370, 95.370, 1, 1, 95.370], [
        0.0, 114.011, 1, 1, 114.011
    ], [0.0, 113.246, 1, 1, 113.246], [0.0, 109.167, 1, 1, 109.167], [
        0.0, 104.227, 1, 1, 104.227
    ], [107.109, 107.109, 1, 1, 107.109], [0.0, 117.43215, 1, 1, 117.43215], [
        0.0, 94.785, 1, 1, 94.785
    ], [0.0, 83.56718, 1, 1, 83.56718], [0.0, 103.501, 1, 1, 103.501], [
        89.931, 89.931, 1, 1, 89.931
    ], [0.0, 120.455, 1, 1, 120.455], [0.0, 97.081, 1, 1, 97.081], [
        0.0, 96.813, 1, 1, 96.813
    ], [0.0, 97.571, 1, 1, 97.571], [106.757, 106.757, 1, 1, 106.757], [
        0.0, 99.335, 1, 1, 99.335
    ], [0.0, 104.538, 1, 1, 104.538], [0.0, 102.028, 1, 1, 102.028], [
        0.0, 90.032, 1, 1, 90.032
    ], [77.542, 77.542, 1, 1, 77.542], [0.0, 102.761, 1, 1, 102.761], [
        0.0, 82.485, 1, 1, 82.485
    ], [0.0, 77.743, 1, 1, 77.743], [0.0, 109.974, 1, 1, 109.974], [
        94.851, 94.851, 1, 1, 94.851
    ], [0.0, 89.771, 1, 1, 89.771], [0.0, 98.193, 1, 1, 98.193], [
        0.0, 102.165, 1, 1, 102.165
    ], [0.0, 96.783, 1, 1, 96.783], [108.865, 108.865, 1, 1, 108.865], [
        0.0, 120.462, 1, 1, 120.462
    ], [0.0, 111.592, 1, 1, 111.592], [0.0, 106.148, 1, 1, 106.148], [
        0.0, 102.946, 1, 1, 102.946
    ], [111.290, 111.290, 1, 1, 111.290], [0.0, 106.002, 1, 1, 106.002], [
        0.0, 114.617, 1, 1, 114.617
    ], [0.0, 88.229, 1, 1, 88.229], [0.0, 131.364, 1, 1, 131.364], [
        86.855, 86.855, 1, 1, 86.855
    ], [0.0, 109.927, 1, 1, 109.927], [0.0, 75.116, 1, 1, 75.116], [
        0.0, 100.465, 1, 1, 100.465
    ], [0.0, 97.783, 1, 1, 97.783], [108.169, 108.169, 1, 1, 108.169], [
        0.0, 98.851, 1, 1, 98.851
    ], [0.0, 99.310, 1, 1, 99.310], [0.0, 94.588, 1, 1, 94.588], [
        0.0, 98.123, 1, 1, 98.123
    ], [115.666, 115.666, 1, 1, 115.666], [0.0, 104.491, 1, 1, 104.491], [
        0.0, 93.490, 1, 1, 93.490
    ], [0.0, 111.794, 1, 1, 111.794], [0.0, 114.320, 1, 1, 114.320], [
        106.938, 106.938, 1, 1, 106.938
    ], [0.0, 106.450, 1, 1, 106.450], [0.0, 103.105, 1, 1, 103.105], [
        0.0, 107.781, 1, 1, 107.781
    ], [0.0, 120.846, 1, 1, 120.846], [100.102, 100.102, 1, 1, 100.102], [
        0.0, 92.930, 1, 1, 92.930
    ], [0.0, 101.246, 1, 1, 101.246], [0.0, 69.517, 1, 1, 69.517], [
        0.0, 106.276, 1, 1, 106.276
    ], [99.046, 99.046, 1, 1, 99.046], [0.0, 101.300, 1, 1, 101.300], [
        0.0, 98.588, 1, 1, 98.588
    ], [0.0, 110.022, 1, 1, 110.022], [0.0, 91.255, 1, 1, 91.255], [
        106.687, 106.687, 1, 1, 106.687
    ], [0.0, 102.443, 1, 1, 102.443], [0.0, 100.342, 1, 1, 100.342], [
        0.0, 96.635, 1, 1, 96.635
    ], [0.0, 80.909, 1, 1, 80.909], [111.080, 111.080, 1, 1, 111.080], [
        0.0, 107.005, 1, 1, 107.005
    ], [0.0, 103.043, 1, 1, 103.043], [0.0, 92.660, 1, 1, 92.660], [
        0.0, 81.526, 1, 1, 81.526
    ], [94.497, 94.497, 1, 1, 94.497], [0.0, 88.791, 1, 1, 88.791], [
        0.0, 97.913, 1, 1, 97.913
    ], [0.0, 96.120, 1, 1, 96.120], [0.0, 101.234, 1, 1, 101.234], [
        95.132, 95.132, 1, 1, 95.132
    ], [0.0, 93.939, 1, 1, 93.939], [0.0, 92.302, 1, 1, 92.302], [
        0.0, 96.536, 1, 1, 96.536
    ], [0.0, 110.747, 1, 1, 110.747], [99.888, 99.888, 1, 1, 99.888], [
        0.0, 92.780, 1, 1, 92.780
    ], [0.0, 107.678, 1, 1, 107.678], [0.0, 96.187, 1, 1, 96.187], [
        0.0, 87.938, 1, 1, 87.938
    ], [91.664, 91.664, 1, 1, 91.664], [0.0, 106.149, 1, 1, 106.149],
                          [0.0, 104.320, 1, 1,
                           104.320], [0.0, 115.681, 1, 1,
                                      115.681], [0.0, 95.920, 1, 1, 95.920]])

    # Leukemia remission times.  Data is from Example 7.2 of Lee and Wang.
    LEUK = np.array([[0.0, 1.0, 1, 1, 1.0], [0.0, 1.0, 1, 1, 1.0], [
        0.0, 2.0, 1, 1, 2.0
    ], [0.0, 2.0, 1, 1, 2.0], [0.0, 3.0, 1, 1, 3.0], [0.0, 4.0, 1, 1, 4.0], [
        0.0, 4.0, 1, 1, 4.0
    ], [0.0, 5.0, 1, 1, 5.0], [0.0, 5.0, 1, 1, 5.0], [0.0, 6.0, 1, 1, 6.0], [
        0.0, 8.0, 1, 1, 8.0
    ], [0.0, 8.0, 1, 1, 8.0], [0.0, 9.0, 1, 1, 9.0], [0.0, 10.0, 1, 1, 10.0],
                     [0.0, 10.0, 1, 1, 10.0], [0.0, 12.0, 1, 1, 12.0], [
                         0.0, 14.0, 1, 1, 14.0
                     ], [0.0, 16.0, 1, 1, 16.0], [0.0, 20.0, 1, 1, 20.0],
                     [0.0, 24.0, 1, 1, 24.0], [0.0, 34.0, 1, 1, 34.0]])

    # Cancerous mice data.  Data is from Example 7.3 in Lee and Wang.
    MICE = np.array([[0.0, 4.0, 1, 1, 4.0], [0.0, 5.0, 1, 1, 5.0], [
        0.0, 8.0, 1, 1, 8.0
    ], [0.0, 9.0, 1, 1, 9.0], [0.0, 10.0, 1, 1, 10.0], [0.0, 10.0, 1, 2, 10.0],
                     [0.0, 10.0, 1, 2, 10.0], [0.0, 10.0, 1, 2, 10.0],
                     [0.0, 10.0, 1, 2, 10.0], [0.0, 10.0, 1, 2, 10.0]])

    # Danish AIDS patients.  Data retrieved from:
    # https://encrypted.google.com/books?id=Jwf3M6TtHTkC&pg=PA33&lpg=PA33&dq=exponential+data+set+example+with+interval+censoring&source=bl&ots=_VK8lx0yqP&sig=zbUtQTK8ZHR10Y5LDA_0aZz_OqI&hl=en&sa=X&ei=ekqwU8mWBtCGqgb204LwDw&ved=0CH4Q6AEwCQ#v=onepage&q=exponential%20data%20set%20example%20with%20interval%20censoring&f=false
    AIDS = np.array([[0.0, 24.0, 24, 4, 12.0], [24.0, 39.0, 1, 4, 7.5], [
        24.0, 113.0, 4, 4, 44.5
    ], [28.0, 88.0, 1, 4, 30.0], [39.0, 113.0, 2, 4, 37.0], [
        57.0, 113.0, 1, 4, 28.0
    ], [0.0, 39.0, 2, 4, 39.0], [24.0, 57.0, 10, 4, 16.5], [
        24.0, 28.0, 4, 4, 2.0
    ], [24.0, 88.0, 3, 4, 32.0], [28.0, 39.0, 4, 4, 5.5], [
        39.0, 57.0, 3, 4, 9.0
    ], [57.0, 88.0, 5, 4, 15.5], [88.0, 113.0, 1, 4, 12.5],
                     [0.0, 88.0, 34, 2, 44.0], [0.0, 24.0, 61, 2, 12.0],
                     [0.0, 28.0, 8, 2, 24.0], [0.0, 39.0, 15, 2, 19.5],
                     [0.0, 57.0, 22, 2, 28.5], [0.0, 113.0, 92, 2, 56.5]])

    # Data set of alpha particle interarrival times.  Data is from Table 7.1 in
    # Meeker and Escobar.
    ALPHA = np.array(
        [[0.0, 100.0, 1609, 4, 50.0], [100.0, 300.0, 2424, 4, 200.0],
         [300.0, 500.0, 1770, 4, 400.0], [500.0, 700.0, 1306, 4, 600.0],
         [700.0, 1000.0, 1213, 4, 850.0], [1000.0, 2000.0, 1528, 4, 1500.0],
         [2000.0, 4000.0, 354, 4, 3000.0], [4000.0, np.inf, 16, 2, np.inf]])

    # Data is the same as that used in the ReliaSoft wiki example for
    # likelihood confidence bounds.  The data can be found at
    # http://www.reliawiki.org/index.php/The_Normal_Distribution#Likelihood_Ratio_Confidence_Bounds
    WIKI = np.array([[0.0, 12.0, 1, 1, 12.0], [0.0, 24.0, 1, 1, 24.0],
                     [0.0, 28.0, 1, 1, 28.0], [0.0, 34.0, 1, 1,
                                               34.0], [0.0, 46.0, 1, 1, 46.0]])

    def setUp(self):
        """
        Setup the test fixture for the Gaussian distribution class.
        """

        self.DUT = Gaussian()

    @attr(all=True, unit=False)
    def test01_log_pdf(self):
        """
        (TestGaussianDistribution) log_pdf should return a numpy array of floats on success
        """

        _log_pdf = self.DUT.log_pdf(
            np.array(_data[:, 2], dtype=float), 0.02222222)

        np.testing.assert_allclose(_log_pdf, [
            -3.91777369, -4.02888479, -4.13999589, -4.25110699, -4.36221809,
            -4.47332919, -4.58444029, -4.69555139, -4.91777359, -5.13999579,
            -5.36221799, -5.58444019, -5.80666239, -6.02888459
        ])

    @attr(all=True, unit=True)
    def test02_partial_derivatives_exact(self):
        """
        (TestGaussianDistribution) partial_derivatives should return a numpy array with exact data only on success.
        """

        _part_deriv = self.DUT.partial_derivatives([1.0, 1.0], self.LEUK)
        self.assertAlmostEqual(_part_deriv, 27612.0)

    @attr(all=True, unit=True)
    def test02a_partial_derivatives_right(self):
        """
        (TestGaussianDistribution) partial_derivatives should return a numpy array with exact and right censored data on success.
        """

        _part_deriv = self.DUT.partial_derivatives([1.0, 1.0], self.MICE)
        self.assertAlmostEqual(_part_deriv, 806.000001567665)

    @attr(all=True, unit=True)
    def test02b_partial_derivs_interval(self):
        """
        (TestGaussianDistribution) partial_derivatives should return a numpy array with right, and interval censored data on success.
        """

        _part_deriv = self.DUT.partial_derivatives([100.0, 30.0], self.AIDS)
        self.assertAlmostEqual(_part_deriv, -0.7378606)

    @attr(all=True, unit=True)
    def test03_maximum_likelihood_estimate_exact_times(self):
        """
        (TestGaussianDistribution) maximum_likelihood_estimate should return a numpy array of floats on success with exact failure times.
        """

        _fit = self.DUT.maximum_likelihood_estimate(self.NORM_TEST, 0.0,
                                                    10000000.0)

        self.assertAlmostEqual(_fit[0][0], 100.5283533)
        self.assertAlmostEqual(_fit[0][1], 10.5442140)
        self.assertAlmostEqual(_fit[1][0], 0.01223150)
        self.assertAlmostEqual(_fit[1][1], -0.001286301)
        self.assertAlmostEqual(_fit[1][2], 0.0001352713)
        self.assertAlmostEqual(_fit[2][0], -377.4515808)
        self.assertAlmostEqual(_fit[2][1], 758.9031615)
        self.assertAlmostEqual(_fit[2][2], 773.3238423)

    @attr(all=True, unit=True)
    def test03a_maximum_likelihood_estimate_interval_censored(self):
        """
        (TestGaussianDistribution) maximum_likelihood_estimate should return a numpy array of floats on success with interval censored failure times.
        """

        _fit = self.DUT.maximum_likelihood_estimate(self.ALPHA, 0.0,
                                                    10000000.0)

        self.assertAlmostEqual(_fit[0][0], 1228.5714286)
        self.assertAlmostEqual(_fit[0][1], 1269.0989894)
        self.assertAlmostEqual(_fit[1][0], 246072.8272910)
        self.assertAlmostEqual(_fit[1][1], -255016.0027117)
        self.assertAlmostEqual(_fit[1][2], 264284.2054322)
        self.assertAlmostEqual(_fit[2][0], -28056.0142512)
        self.assertAlmostEqual(_fit[2][1], 56116.0285024)
        self.assertAlmostEqual(_fit[2][2], 56119.8121430)

    @attr(all=True, unit=True)
    def test04_theoretical_distribution(self):
        """
        (TestGaussianDistribution) theoretical_distribution should return a numpy array of floats on success.
        """

        _para = [100.0, 10.0]

        _data = [x[1] for x in self.NORM_TEST]
        _probs = self.DUT.theoretical_distribution(np.array(_data), _para)
        np.testing.assert_almost_equal(_probs, [
            0.00115070, 0.00641597, 0.01235841, 0.01301714, 0.02812460,
            0.03234459, 0.03992991, 0.05016230, 0.09433900, 0.11387019,
            0.11957780, 0.13116522, 0.15317756, 0.15699142, 0.15943080,
            0.19092301, 0.20225321, 0.22070927, 0.23147437, 0.23514724,
            0.23978324, 0.25752324, 0.27222418, 0.29105681, 0.29418487,
            0.30100925, 0.30331145, 0.31320004, 0.32168218, 0.34163684,
            0.34900802, 0.35149033, 0.36452106, 0.36824693, 0.37383999,
            0.37497701, 0.38518154, 0.40404143, 0.41227372, 0.41734122,
            0.42555592, 0.42830153, 0.44385597, 0.45426219, 0.46199856,
            0.47249481, 0.47348988, 0.49553194, 0.50406914, 0.51364117,
            0.51854413, 0.54910482, 0.54957989, 0.55171679, 0.58035432,
            0.58570099, 0.59650076, 0.60876437, 0.61585027, 0.61955033,
            0.62190962, 0.63686817, 0.66374292, 0.66712929, 0.67332024,
            0.67501361, 0.72581352, 0.73065660, 0.73068962, 0.73486700,
            0.74053641, 0.74815657, 0.75038443, 0.75609618, 0.75819245,
            0.76142690, 0.77869699, 0.78174497, 0.79300721, 0.81232592,
            0.82035007, 0.83957191, 0.84071480, 0.84187650, 0.85874547,
            0.86606909, 0.87055108, 0.87681266, 0.88088053, 0.90734807,
            0.91940791, 0.92392809, 0.92808828, 0.94139589, 0.94157110,
            0.95935197, 0.97959721, 0.97963165, 0.98144719, 0.99914482
        ])

    @attr(all=True, unit=True)
    def test05_hazard_function(self):
        """
        (TestGaussianDistribution) hazard_function should return a dict on success.
        """

        _scale = [4.0, 5.0, 6.0]
        _shape = [0.9, 1.0, 1.1]

        _hazard = self.DUT.hazard_function(_scale, _shape, 0, 10, 1)
        self.assertEqual(
            _hazard, {
                0: [
                    2.2768757940970579e-05, 1.4867195147342979e-06,
                    1.2558515647092129e-07
                ],
                1: [
                    0.0017136433292123422, 0.00013383022576488537,
                    1.1830528275337732e-05
                ],
                2: [
                    0.037526278928078485, 0.0044318484119380075,
                    0.00048769567621990344
                ],
                3: [
                    0.23910273444781227, 0.053990966513188063,
                    0.0087977701867818243
                ],
                4: [
                    0.44326920044603635, 0.24197072451914337,
                    0.069450481622787955
                ],
                5:
                [0.23910273444781227, 0.3989422804014327, 0.23991469567611817],
                6: [
                    0.037526278928078485, 0.24197072451914337,
                    0.36267480036493877
                ],
                7: [
                    0.0017136433292123422, 0.053990966513188063,
                    0.23991469567611817
                ],
                8: [
                    2.2768757940970579e-05, 0.0044318484119380075,
                    0.069450481622787955
                ],
                9: [
                    8.8022199874779748e-08, 0.00013383022576488537,
                    0.0087977701867818243
                ]
            })

    @attr(all=True, unit=True)
    def test06_mean(self):
        """
        (TestGaussianDistribution) mean should return a dict on success.
        """

        _scale = [4.0, 5.0, 6.0]

        _hazard = self.DUT.mean(_scale, 0, 10, 1)
        self.assertEqual(
            _hazard, {
                0: _scale,
                1: _scale,
                2: _scale,
                3: _scale,
                4: _scale,
                5: _scale,
                6: _scale,
                7: _scale,
                8: _scale,
                9: _scale
            })

    @attr(all=True, unit=True)
    def test07_reliability_function(self):
        """
        (TestGaussianDistribution) reliability_function should return a dict on success.
        """

        _scale = [4.0, 5.0, 6.0]
        _shape = [0.9, 1.0, 1.1]

        _reliability = self.DUT.reliability_function(_scale, _shape, 0, 10, 1)
        self.assertEqual(
            _reliability, {
                0:
                [0.9999999754508625, 0.99999971334842808, 0.99999559403629745],
                1: [
                    0.99999725915867366, 0.99996832875816688,
                    0.99957093966680322
                ],
                2:
                [0.99986174304218089, 0.9986501019683699, 0.98686585430897888],
                3: [
                    0.99680698835864645, 0.97724986805182079,
                    0.86673973709749463
                ],
                4: [0.96548182600279242, 0.84134474606854293, 0.5],
                5: [0.81834892955655103, 0.5, 0.13326026290250537],
                6: [0.5, 0.15865525393145707, 0.013134145691021115],
                7: [
                    0.18165107044344897, 0.022750131948179209,
                    0.0004290603331967846
                ],
                8: [
                    0.03451817399720758, 0.0013498980316301035,
                    4.4059637025473108e-06
                ],
                9: [
                    0.0031930116413535492, 3.1671241833119979e-05,
                    1.3836508938602776e-08
                ]
            })

    @attr(all=True, unit=True)
    def test08_log_likelihood_ratio(self):
        """
        (TestGaussianDistribution) log_likelihood_ratio should return a float value on success.
        """

        _params = [28.8, 11.2143]
        _const = 1.642374 / 2.0

        _log_lik_ratio = self.DUT.log_likelihood_ratio(_params, self.WIKI,
                                                       _const)
        self.assertAlmostEqual(_log_lik_ratio, -20.0018180)

    @attr(all=True, unit=True)
    def test09_likelihood_bounds(self):
        """
        (TestGaussianDistribution) likelihood_bounds should return a tuple of OrderedDicts on success.
        """

        _params = [28.8, 11.2143]

        _lik_bounds = self.DUT.likelihood_bounds(_params, 0.8, self.WIKI)

        # Check the lower and upper bounds on mu and sigma.
        self.assertAlmostEqual(_lik_bounds[0], 21.8070752)
        self.assertAlmostEqual(_lik_bounds[1], 35.7929248)
        self.assertAlmostEqual(_lik_bounds[2], 7.0854939)
        self.assertAlmostEqual(_lik_bounds[3], 18.8536433)


class TestLogNormalDistribution(unittest.TestCase):
    """
    Class for testing the LogNormal distribution data model class.
    """

    # Data is the same as that used in the ReliaSoft wiki examples.
    # The table can be found at the following URL, for example.
    # http://reliawiki.org/index.php/The_Lognormal_Distribution#Rank_Regression_on_Y
    # mu = 3.516, sigma = 0.9663, and rho = 0.9754 when fit to the LNORM.
    LOGN_TEST = np.array([[5.0, 5.0, 1, 1, 5.0], [10.0, 10.0, 1, 1, 10.0], [
        15.0, 15.0, 1, 1, 15.0
    ], [20.0, 20.0, 1, 1, 20.0], [25.0, 25.0, 1, 1, 25.0], [
        30.0, 30.0, 1, 1, 30.0
    ], [35.0, 35.0, 1, 1, 35.0], [40.0, 40.0, 1, 1, 40.0],
                          [50.0, 50.0, 1, 1, 50.0], [60.0, 60.0, 1, 1, 60.0],
                          [70.0, 70.0, 1, 1,
                           70.0], [80.0, 80.0, 1, 1,
                                   80.0], [90.0, 90.0, 1, 1,
                                           90.0], [100.0, 100.0, 1, 1, 100.0]])

    # Data set of alpha particle interarrival times.  Data is from Table 7.1 in
    # Meeker and Escobar.
    ALPHA = np.array(
        [[0.0, 100.0, 1609, 4, 50.0], [100.0, 300.0, 2424, 4, 200.0],
         [300.0, 500.0, 1770, 4, 400.0], [500.0, 700.0, 1306, 4, 600.0],
         [700.0, 1000.0, 1213, 4, 850.0], [1000.0, 2000.0, 1528, 4, 1500.0],
         [2000.0, 4000.0, 354, 4, 3000.0], [4000.0, np.inf, 16, 2, np.inf]])

    # Data is the same as that used in the ReliaSoft wiki example for
    # calculating lognormal likelihood ratio bounds.  The example can be found
    # at http://www.reliawiki.org/index.php/The_Lognormal_Distribution#Likelihood_Ratio_Confidence_Bounds
    WIKI = np.array([[0.0, 45.0, 1, 1, 45.0], [0.0, 60.0, 1, 1,
                                               60.0], [0.0, 75.0, 1, 1, 75.0],
                     [0.0, 90.0, 1, 1, 90.0], [0.0, 115.0, 1, 1, 115.0]])

    def setUp(self):
        """
        Setup the test fixture for the LogNormal distribution class.
        """

        self.DUT = LogNormal()

    @attr(all=True, unit=False)
    def test01_log_pdf(self):
        """
        (TestLogNormalDistribution) log_pdf should return a numpy array of floats on success
        """

        _log_pdf = self.DUT.log_pdf(
            np.array(self.LOGN_TEST[:, 2], dtype=float), 0.02222222)

        np.testing.assert_allclose(_log_pdf, [
            -3.91777369, -4.02888479, -4.13999589, -4.25110699, -4.36221809,
            -4.47332919, -4.58444029, -4.69555139, -4.91777359, -5.13999579,
            -5.36221799, -5.58444019, -5.80666239, -6.02888459
        ])

    @attr(all=True, unit=True)
    def test02_partial_derivatives_exact(self):
        """
        (TestLogNormalDistribution) partial_derivatives should return a numpy array with exact data only on success.
        """

        _part_deriv = self.DUT.partial_derivatives([3.5158554, 0.8491908],
                                                   self.LOGN_TEST)
        self.assertAlmostEqual(_part_deriv, 2.2196636E-06)

    @attr(all=True, unit=False)
    def test02a_partial_derivatives_right(self):
        """
        (TestLogNormalDistribution) partial_derivatives should return a numpy array with exact and right censored data on success.
        """

        # Cancerous mice data.  Data is from Example 7.3 in Lee and Wang.
        _data = np.array(
            [[0.0, 4.0, 1, 1], [0.0, 5.0, 1, 1], [0.0, 8.0, 1, 1],
             [0.0, 9.0, 1, 1], [0.0, 10.0, 1, 1], [0.0, 10.0, 1, 2],
             [0.0, 10.0, 1, 2], [0.0, 10.0, 1, 2], [0.0, 10.0, 1,
                                                    2], [0.0, 10.0, 1, 2]])

        _part_deriv = self.DUT.partial_derivatives(1.0, _data)
        self.assertAlmostEqual(_part_deriv, -81.0)

    @attr(all=True, unit=False)
    def test02b_partial_derivs_interval(self):
        """
        (TestLogNormalDistribution) partial_derivatives should return a numpy array with exact, right, and interval censored data on success.
        """

        _part_deriv = self.DUT.partial_derivatives([6.2376513, 1.2489836],
                                                   self.ALPHA)
        self.assertAlmostEqual(_part_deriv, -33687.1470588)

    @attr(all=True, unit=True)
    def test03_maximum_likelihood_estimate_exact_times(self):
        """
        (TestLogNormalDistribution) maximum_likelihood_estimate should return a numpy array of floats on success with exact failure times.
        """

        _fit = self.DUT.maximum_likelihood_estimate(self.LOGN_TEST, 0.0,
                                                    10000000.0)

        # Check the mean for exact failure time data.
        self.assertAlmostEqual(_fit[0][0], 3.5158554)
        self.assertAlmostEqual(_fit[0][1], 0.8491908)
        self.assertAlmostEqual(_fit[1][0], 0.003004906)
        self.assertAlmostEqual(_fit[1][1], -0.0008767578)
        self.assertAlmostEqual(_fit[1][2], 0.0002558164)
        self.assertAlmostEqual(_fit[2][0], -66.7985190)
        self.assertAlmostEqual(_fit[2][1], 137.59703792)
        self.assertAlmostEqual(_fit[2][2], 144.15326723)

    @attr(all=True, unit=True)
    def test03a_maximum_likelihood_estimate_interval_censored(self):
        """
        (TestLogNormalDistribution) maximum_likelihood_estimate should return a numpy array of floats on success with interval censored failure times.
        """

        _fit = self.DUT.maximum_likelihood_estimate(self.ALPHA, 0.0,
                                                    10000000.0)

        # Check the log mean and log standard error for interval censored data.
        np.testing.assert_array_equal(_fit[0],
                                      [6.2376513358423553, 1.2489836256584086])

        # Check the variance-covariance matrix for interval censored data.
        np.testing.assert_array_equal(_fit[1], [
            0.014770747504309583, -0.0043861896898634333, 0.0013024838444940664
        ])

    @attr(all=True, unit=True)
    def test04_theoretical_distribution(self):
        """
        (TestLogNormalDistribution) theoretical_distribution should return a numpy array of floats on success.
        """

        _para = [3.51585540, 0.9693628]

        _data = [x[1] for x in self.LOGN_TEST]
        _probs = self.DUT.theoretical_distribution(np.array(_data), _para)
        np.testing.assert_almost_equal(_probs, [
            0.02472972, 0.10554292, 0.20252142, 0.29596331, 0.37982014,
            0.45305838, 0.51636622, 0.57093317, 0.65869163, 0.72472779,
            0.77515821, 0.81425235, 0.84498695, 0.86946088
        ])

    @attr(all=True, unit=True)
    def test05_hazard_function(self):
        """
        (TestLogNormalDistribution) hazard_function should return a dict on success.
        """

        _scale = [4.0, 5.0, 6.0]
        _shape = [0.9, 1.0, 1.1]

        _hazard = self.DUT.hazard_function(_scale, _shape, 0, 10, 1)
        self.assertEqual(_hazard[1], [
            2.2768757940970579e-05, 1.4867195147342979e-06,
            1.2558515647092129e-07
        ])
        self.assertEqual(_hazard[2], [
            0.00019493570355702791, 1.8707681970007872e-05,
            2.1655143377508431e-06
        ])
        self.assertEqual(_hazard[3], [
            0.00054786222682508148, 6.5861015705858406e-05,
            9.1666572019749187e-06
        ])
        self.assertEqual(_hazard[4], [
            0.0010322510822758279, 0.00014559713252944623,
            2.3095412489013529e-05
        ])
        self.assertEqual(_hazard[5], [
            0.0015937796453101671, 0.0002544688616707044,
            4.4674279231644493e-05
        ])
        self.assertEqual(_hazard[6], [
            0.0021903229601368535, 0.00038699388965022233,
            7.3810558361954844e-05
        ])
        self.assertEqual(_hazard[7], [
            0.0027924805860515753, 0.00053750037994856534,
            0.00010995716077455723
        ])
        self.assertEqual(_hazard[8], [
            0.0033808134787128444, 0.00070085402621117223,
            0.00015234643299858575
        ])
        self.assertEqual(_hazard[9], [
            0.003943048355831501, 0.0008726830334021109, 0.00020013009279589065
        ])

    @attr(all=True, unit=True)
    def test06_mean(self):
        """
        (TestLogNormalDistribution) mean should return a dict on success.
        """

        _scale = [4.0, 5.0, 6.0]
        _shape = [0.9, 1.0, 1.1]

        _hazard = self.DUT.mean(_scale, _shape, 0, 10, 1)
        self.assertEqual(
            _hazard, {
                0:
                [81.859142843167632, 244.69193226422038, 738.77986921169395],
                1:
                [81.859142843167632, 244.69193226422038, 738.77986921169395],
                2:
                [81.859142843167632, 244.69193226422038, 738.77986921169395],
                3:
                [81.859142843167632, 244.69193226422038, 738.77986921169395],
                4:
                [81.859142843167632, 244.69193226422038, 738.77986921169395],
                5:
                [81.859142843167632, 244.69193226422038, 738.77986921169395],
                6:
                [81.859142843167632, 244.69193226422038, 738.77986921169395],
                7:
                [81.859142843167632, 244.69193226422038, 738.77986921169395],
                8:
                [81.859142843167632, 244.69193226422038, 738.77986921169395],
                9:
                [81.859142843167632, 244.69193226422038, 738.77986921169395]
            })

    @attr(all=True, unit=True)
    def test07_reliability_function(self):
        """
        (TestLogNormalDistribution) reliability_function should return a dict on success.
        """

        _scale = [4.0, 5.0, 6.0]
        _shape = [0.9, 1.0, 1.1]

        _reliability = self.DUT.reliability_function(_scale, _shape, 0, 10, 1)
        self.assertEqual(
            _reliability, {
                0: [1.0, 1.0, 1.0],
                1:
                [0.9999999754508625, 0.99999971334842808, 0.99999559403629745],
                2: [
                    0.99999929791430298, 0.99999172031442773,
                    0.99988073989677451
                ],
                3: [
                    0.99999582109031149, 0.99995217858769636,
                    0.99936741217548297
                ],
                4: [
                    0.99998631288638873, 0.99984907412853197,
                    0.99815854970649009
                ],
                5: [
                    0.99996716058874868, 0.99965125273245459,
                    0.99604843025911194
                ],
                6:
                [0.99993479240059935, 0.9993322512266507, 0.99292830116953912],
                7: [
                    0.99988588919326771, 0.99887127770659423,
                    0.98876483336431009
                ],
                8: [
                    0.99981747727614745, 0.99825297680814196,
                    0.98357672032085075
                ],
                9:
                [0.99972695705771863, 0.99746675322444922, 0.9774158528999386]
            })

    @attr(all=True, unit=True)
    def test08_log_likelihood_ratio(self):
        """
        (TestLogNormalDistribution) log_likelihood_ratio should return a float value on success.
        """

        _params = [4.2926, 0.32361]
        _const = 1.323303 / 2.0

        _log_lik_ratio = self.DUT.log_likelihood_ratio(_params, self.WIKI,
                                                       _const)
        self.assertAlmostEqual(_log_lik_ratio, -23.5784187)

    @attr(all=True, unit=True)
    def test09_likelihood_bounds(self):
        """
        (TestLogNormalDistribution) likelihood_bounds should return a tuple of OrderedDicts on success.
        """

        _params = [4.2926, 0.32361]

        _lik_bounds = self.DUT.likelihood_bounds(_params, 0.75, self.WIKI)

        # Check the first lower and upper bounds in the OrderedDicts.
        self.assertAlmostEqual(_lik_bounds[0][0.24270750000000002], 4.2320811)
        self.assertAlmostEqual(_lik_bounds[1][0.24270750000000002], 4.3532137)


class TestWeibullDistribution(unittest.TestCase):
    """
    Class for testing the Weibull distribution data model class.
    """

    # Leukemia remission times.  Data is from Example 7.2 of Lee and Wang.
    LEUK = np.array([[0.0, 1.0, 1, 1, 1.0], [0.0, 1.0, 1, 1, 1.0], [
        0.0, 2.0, 1, 1, 2.0
    ], [0.0, 2.0, 1, 1, 2.0], [0.0, 3.0, 1, 1, 3.0], [0.0, 4.0, 1, 1, 4.0], [
        0.0, 4.0, 1, 1, 4.0
    ], [0.0, 5.0, 1, 1, 5.0], [0.0, 5.0, 1, 1, 5.0], [0.0, 6.0, 1, 1, 6.0], [
        0.0, 8.0, 1, 1, 8.0
    ], [0.0, 8.0, 1, 1, 8.0], [0.0, 9.0, 1, 1, 9.0], [0.0, 10.0, 1, 1, 10.0],
                     [0.0, 10.0, 1, 1, 10.0], [0.0, 12.0, 1, 1, 12.0], [
                         0.0, 14.0, 1, 1, 14.0
                     ], [0.0, 16.0, 1, 1, 16.0], [0.0, 20.0, 1, 1, 20.0],
                     [0.0, 24.0, 1, 1, 24.0], [0.0, 34.0, 1, 1, 34.0]])

    # Cancerous mice data.  Data is from Example 7.3 in Lee and Wang.
    MICE = np.array([[0.0, 4.0, 1, 1, 4.0], [0.0, 5.0, 1, 1, 5.0], [
        0.0, 8.0, 1, 1, 8.0
    ], [0.0, 9.0, 1, 1, 9.0], [0.0, 10.0, 1, 1, 10.0], [0.0, 10.0, 1, 2, 10.0],
                     [0.0, 10.0, 1, 2, 10.0], [0.0, 10.0, 1, 2, 10.0],
                     [0.0, 10.0, 1, 2, 10.0], [0.0, 10.0, 1, 2, 10.0]])

    # Danish AIDS patients.  Data retrieved from:
    # https://encrypted.google.com/books?id=Jwf3M6TtHTkC&pg=PA33&lpg=PA33&dq=exponential+data+set+example+with+interval+censoring&source=bl&ots=_VK8lx0yqP&sig=zbUtQTK8ZHR10Y5LDA_0aZz_OqI&hl=en&sa=X&ei=ekqwU8mWBtCGqgb204LwDw&ved=0CH4Q6AEwCQ#v=onepage&q=exponential%20data%20set%20example%20with%20interval%20censoring&f=false
    AIDS = np.array([[0.0, 24.0, 24, 4, 12.0], [24.0, 39.0, 1, 4, 7.5], [
        24.0, 113.0, 4, 4, 44.5
    ], [28.0, 88.0, 1, 4, 30.0], [39.0, 113.0, 2, 4, 37.0], [
        57.0, 113.0, 1, 4, 28.0
    ], [0.0, 39.0, 2, 4, 39.0], [24.0, 57.0, 10, 4, 16.5], [
        24.0, 28.0, 4, 4, 2.0
    ], [24.0, 88.0, 3, 4, 32.0], [28.0, 39.0, 4, 4, 5.5], [
        39.0, 57.0, 3, 4, 9.0
    ], [57.0, 88.0, 5, 4, 15.5], [88.0, 113.0, 1, 4, 12.5],
                     [0.0, 88.0, 34, 2, 44.0], [0.0, 24.0, 61, 2, 12.0],
                     [0.0, 28.0, 8, 2, 24.0], [0.0, 39.0, 15, 2, 19.5],
                     [0.0, 57.0, 22, 2, 28.5], [0.0, 113.0, 92, 2, 56.5]])

    # Data is the same as that used in the ReliaSoft wiki examples.
    # The table can be found at the following URL, for example.
    # http://reliawiki.org/index.php/The_Weibull_Distribution#Rank_Regression_on_Y
    # eta = 76.318, beta = 1.4301, and rho = 0.9956 when fit to the WEI.
    DATA = np.array([[0.0, 16.0, 1, 1, 16.0], [0.0, 34.0, 1, 1, 34.0],
                     [0.0, 53.0, 1, 1, 53.0], [0.0, 75.0, 1, 1, 75.0],
                     [0.0, 93.0, 1, 1, 93.0], [0.0, 120.0, 1, 1, 120.0]])

    # Data is the same as that used in the ReliaSoft wiki examples.
    # The table can be found at the following URL, for example.
    # http://www.reliawiki.org/index.php/Confidence_Bounds#Likelihood_Ratio_Confidence_Bounds
    # eta = 33.9428, beta = 2.2938 when fit to the WEI.
    DATA2 = np.array([[0.0, 10.0, 1, 1, 10.0], [0.0, 20.0, 1, 1,
                                                20.0], [0.0, 30.0, 1, 1, 30.0],
                      [0.0, 40.0, 1, 1, 40.0], [0.0, 50.0, 1, 1, 50.0]])

    # Data is from Wayne Nelson, Applied Life Data Analysis, Page 415.
    # 167 identical parts were inspected for cracks. The following is a table
    # of their last inspection times and times-to-failure.
    NELSON = np.array([[0.0, 6.12, 5, 3, 3.06], [6.12, 19.92, 16, 3, 13.02], [
        19.92, 29.64, 12, 3, 24.78
    ], [29.64, 35.4, 18, 3, 32.52], [35.4, 39.72, 18, 3,
                                     38.56], [39.72, 45.24, 2, 3, 42.48],
                       [45.24, 52.32, 6, 3,
                        48.78], [52.32, 63.48, 17, 3,
                                 57.9], [63.48, 63.48, 73, 2, np.inf]])

    # Data set of 100 exponentially distributed points with a mean of 100.
    WEI_TEST = np.array(
        [[1.585, 1.585, 1, 1, 1.585], [1.978, 1.978, 1, 1,
                                       1.978], [2.81, 2.81, 1, 1, 2.81],
         [3.679, 3.679, 1, 1, 3.679], [4.248, 4.248, 1, 1, 4.248], [
             5.137, 5.137, 1, 1, 5.137
         ], [5.566, 5.566, 1, 1, 5.566], [6.328, 6.328, 1, 1, 6.328],
         [7.876, 7.876, 1, 1, 7.876], [10.79, 10.79, 1, 1, 10.79], [
             12.398, 12.398, 1, 1, 12.398
         ], [13.095, 13.095, 1, 1, 13.095], [13.64, 13.64, 1, 1, 13.64], [
             14.003, 14.003, 1, 1, 14.003
         ], [14.259, 14.259, 1, 1, 14.259], [14.558, 14.558, 1, 1, 14.558], [
             14.808, 14.808, 1, 1, 14.808
         ], [14.848, 14.848, 1, 1, 14.848], [16.452, 16.452, 1, 1, 16.452], [
             17.743, 17.743, 1, 1, 17.743
         ], [18.793, 18.793, 1, 1, 18.793], [18.917, 18.917, 1, 1, 18.917], [
             19.664, 19.664, 1, 1, 19.664
         ], [20.564, 20.564, 1, 1, 20.564], [28.693, 28.693, 1, 1, 28.693], [
             34.931, 34.931, 1, 1, 34.931
         ], [35.461, 35.461, 1, 1, 35.461], [36.169, 36.169, 1, 1, 36.169], [
             37.765, 37.765, 1, 1, 37.367
         ], [38.951, 38.951, 1, 1, 38.951], [39.576, 39.576, 1, 1, 39.576], [
             40.36, 40.36, 1, 1, 40.36
         ], [41.559, 41.559, 1, 1, 41.559], [42.486, 42.486, 1, 1, 42.486], [
             46.984, 46.984, 1, 1, 46.984
         ], [48.146, 48.146, 1, 1, 48.146], [48.398, 48.398, 1, 1, 48.398], [
             49.315, 49.315, 1, 1, 49.315
         ], [49.364, 49.364, 1, 1, 49.364], [49.76, 49.76, 1, 1, 49.76], [
             49.855, 49.855, 1, 1, 49.855
         ], [52.315, 52.315, 1, 1, 52.315], [52.885, 52.885, 1, 1, 52.885], [
             53.127, 53.127, 1, 1, 53.127
         ], [53.18, 53.18, 1, 1, 53.18], [54.07, 54.07, 1, 1, 54.07], [
             58.595, 58.595, 1, 1, 58.595
         ], [61.993, 61.993, 1, 1, 61.993], [65.542, 65.542, 1, 1, 65.542], [
             66.69, 66.69, 1, 1, 66.69
         ], [66.864, 66.864, 1, 1, 66.864], [67.342, 67.342, 1, 1, 67.342], [
             69.776, 69.776, 1, 1, 69.776
         ], [71.048, 71.048, 1, 1, 71.048], [74.057, 74.057, 1, 1, 74.057], [
             75.549, 75.549, 1, 1, 75.549
         ], [77.095, 77.095, 1, 1, 77.095], [78.747, 78.747, 1, 1, 78.747], [
             80.172, 80.172, 1, 1, 80.172
         ], [82.16, 82.16, 1, 1, 82.16], [82.223, 82.223, 1, 1, 82.223], [
             86.769, 86.769, 1, 1, 86.769
         ], [87.229, 87.229, 1, 1, 87.229], [88.862, 88.862, 1, 1, 88.862], [
             89.103, 89.103, 1, 1, 89.103
         ], [94.072, 94.072, 1, 1, 94.072], [96.415, 96.415, 1, 1, 96.415], [
             101.977, 101.977, 1, 1, 101.977
         ], [111.147, 111.147, 1, 1, 111.147], [
             115.532, 115.532, 1, 1, 115.532
         ], [120.144, 120.144, 1, 1, 120.144], [
             121.963, 121.963, 1, 1, 121.963
         ], [134.763, 134.763, 1, 1, 134.763], [
             137.072, 137.072, 1, 1, 137.072
         ], [141.988, 141.988, 1, 1, 141.988], [
             143.687, 143.687, 1, 1, 143.687
         ], [143.918, 143.918, 1, 1, 143.918], [148.07, 148.07, 1, 1, 148.07],
         [158.98, 158.98, 1, 1, 158.98], [159.732, 159.732, 1, 1, 159.732], [
             163.827, 163.827, 1, 1, 163.827
         ], [169.175, 169.175, 1, 1, 169.175], [
             171.813, 171.813, 1, 1, 171.813
         ], [172.663, 172.663, 1, 1, 172.663], [
             177.992, 177.992, 1, 1, 177.992
         ], [184.263, 184.263, 1, 1, 184.263], [
             185.254, 185.254, 1, 1, 185.254
         ], [194.039, 194.039, 1, 1, 194.039], [
             212.279, 212.279, 1, 1, 212.279
         ], [222.93, 222.93, 1, 1,
             222.93], [226.918, 226.918, 1, 1, 226.918], [
                 241.044, 241.044, 1, 1, 241.044
             ], [263.548, 263.548, 1, 1,
                 263.548], [275.491, 275.491, 1, 1, 275.491], [
                     294.418, 294.418, 1, 1, 294.418
                 ], [297.467, 297.467, 1, 1,
                     297.467], [317.922, 317.922, 1, 1,
                                317.922], [323.763, 323.763, 1, 1, 323.763], [
                                    350.577, 350.577, 1, 1, 350.577
                                ], [351.347, 351.347, 1, 1, 351.347]])

    # Data set of alpha particle interarrival times.  Data is from Table 7.1 in
    # Meeker and Escobar.
    ALPHA = np.array(
        [[0.0, 100.0, 1609, 4, 50.0], [100.0, 300.0, 2424, 4, 200.0],
         [300.0, 500.0, 1770, 4, 400.0], [500.0, 700.0, 1306, 4, 600.0],
         [700.0, 1000.0, 1213, 4, 850.0], [1000.0, 2000.0, 1528, 4, 1500.0],
         [2000.0, 4000.0, 354, 4, 3000.0], [4000.0, np.inf, 16, 2, np.inf]])

    def setUp(self):
        """
        Setup the test fixture for the Weibull distribution class.
        """

        self.DUT = Weibull()

    @attr(all=True, unit=False)
    def test01_log_pdf(self):
        """
        (TestWeibullDistribution) log_pdf should return a numpy array of floats on success
        """

        _log_pdf = self.DUT.log_pdf(
            np.array(_data[:, 2], dtype=float), 0.02222222)

        np.testing.assert_allclose(_log_pdf, [
            -3.91777369, -4.02888479, -4.13999589, -4.25110699, -4.36221809,
            -4.47332919, -4.58444029, -4.69555139, -4.91777359, -5.13999579,
            -5.36221799, -5.58444019, -5.80666239, -6.02888459
        ])

    @attr(all=True, unit=True)
    def test02_partial_derivatives_exact(self):
        """
        (TestWeibullDistribution) partial_derivatives should return a numpy array with exact data only on success.
        """

        _part_deriv = self.DUT.partial_derivatives([1.0, 1.0], self.LEUK)
        self.assertAlmostEqual(_part_deriv, -79736.1447497)

    @attr(all=True, unit=True)
    def test02a_partial_derivatives_right(self):
        """
        (TestWeibullDistribution) partial_derivatives should return a numpy array with exact and right censored data on success.
        """

        _part_deriv = self.DUT.partial_derivatives([1.0, 1.0], self.MICE)
        self.assertAlmostEqual(_part_deriv, -14060.2264530)

    @attr(all=True, unit=True)
    def test02b_partial_derivs_interval(self):
        """
        (TestWeibullDistribution) partial_derivatives should return a numpy array with exact, right, and interval censored data on success.
        """

        _part_deriv = self.DUT.partial_derivatives([1.0, 1.0], self.AIDS)
        self.assertAlmostEqual(_part_deriv, -1452769512.6979916)

    @attr(all=True, unit=True)
    def test03_maximum_likelihood_estimate_exact_times(self):
        """
        (TestWeibullDistribution) maximum_likelihood_estimate should return a numpy array of floats on success with exact failure times.
        """

        _fit = self.DUT.maximum_likelihood_estimate(self.DATA, 0.0, 10000000.0)

        # Check the mean for exact failure time data.
        self.assertAlmostEqual(_fit[0][0], 73.5260622)
        self.assertAlmostEqual(_fit[0][1], 1.9326764)
        self.assertAlmostEqual(_fit[1][0], 241.3390782)
        self.assertAlmostEqual(_fit[1][1], 1.166965e-02)
        self.assertAlmostEqual(_fit[1][2], 1.6781965)
        self.assertAlmostEqual(_fit[2][0], -29.5849216)
        self.assertAlmostEqual(_fit[2][1], 63.1698432)
        self.assertAlmostEqual(_fit[2][2], 66.3368811)
        self.assertAlmostEqual(_fit[3], 0)
        self.assertAlmostEqual(_fit[4], 6.0)

    @attr(all=True, unit=True)
    def test03a_maximum_likelihood_estimate_interval_censored(self):
        """
        (TestWeibullDistribution) maximum_likelihood_estimate should return a numpy array of floats on success with interval censored failure times.
        """

        _fit = self.DUT.maximum_likelihood_estimate(self.NELSON, 0.0,
                                                    10000000.0)

        # Check the scale and shape parameters for interval censored failure time data.
        self.assertAlmostEqual(_fit[0][0], 68.4519239)
        self.assertAlmostEqual(_fit[0][1], 1.8118217)
        self.assertAlmostEqual(_fit[1][0], 159.6371163)
        self.assertAlmostEqual(_fit[1][1], 0.01626650)
        self.assertAlmostEqual(_fit[1][2], 1.6133607)
        self.assertAlmostEqual(_fit[2][0], -383.8327766)
        self.assertAlmostEqual(_fit[2][1], 771.6655532)
        self.assertAlmostEqual(_fit[2][2], 776.4544515)
        self.assertAlmostEqual(_fit[3], 73.0)
        self.assertAlmostEqual(_fit[4], 94.0)

    @attr(all=True, unit=True)
    def test04_theoretical_distribution(self):
        """
        (TestWeibullDistribution) theoretical_distribution should return a numpy array of floats on success.
        """

        _para = [76.3454154, 1.4269671]

        _data = [x[1] for x in self.WEI_TEST]
        _probs = self.DUT.theoretical_distribution(np.array(_data), _para)
        np.testing.assert_almost_equal(_probs, [
            0.00396191, 0.00543068, 0.00894684, 0.01311430, 0.01607735,
            0.02103208, 0.02355218, 0.02821701, 0.03835868, 0.05945336,
            0.07200798, 0.07762049, 0.08207479, 0.08507205, 0.08719995,
            0.08969964, 0.09180128, 0.09213850, 0.10586740, 0.11718375,
            0.12654165, 0.12765516, 0.13439830, 0.14259771, 0.21922922,
            0.27940212, 0.28451269, 0.29133348, 0.30667514, 0.31803657,
            0.32400771, 0.33148024, 0.34286626, 0.35163095, 0.39359384,
            0.40426006, 0.40656280, 0.41490977, 0.41535434, 0.41894165,
            0.41980077, 0.44184265, 0.44689168, 0.44902846, 0.44949589,
            0.45731530, 0.49616338, 0.52427934, 0.55262089, 0.56155801,
            0.56290262, 0.56658284, 0.58501193, 0.59443456, 0.61614971,
            0.62661584, 0.63724941, 0.64837412, 0.65777284, 0.67058012,
            0.67098019, 0.69891557, 0.70164032, 0.71116325, 0.71254891,
            0.74000189, 0.75221912, 0.77941278, 0.81896562, 0.83570443,
            0.85189600, 0.85790149, 0.89458735, 0.90024929, 0.91142858,
            0.91502854, 0.91550794, 0.92372806, 0.94205279, 0.94315728,
            0.94884721, 0.95550522, 0.95849193, 0.95941487, 0.96478918,
            0.97027892, 0.97107105, 0.97729255, 0.98646928, 0.99008920,
            0.99119437, 0.99424834, 0.99714569, 0.99805292, 0.99895336,
            0.99905451, 0.99952729, 0.99961357, 0.99984979, 0.99985388
        ])

    @attr(all=True, unit=True)
    def test05_hazard_function(self):
        """
        (TestWeibullDistribution) hazard_function should return a dict on success.
        """

        _scale = [66.3454154, 76.3454154, 86.3454154]
        _shape = [1.3269671, 1.4269671, 1.5269671]

        _hazard = self.DUT.hazard_function(_scale, _shape, 0, 10, 1)
        self.assertEqual(
            _hazard, {
                0: [0.0, 0.0, 0.0],
                1: [
                    0.005074310112434645, 0.002935922696392235,
                    0.0016875474641446346
                ],
                2: [
                    0.006365080637055861, 0.003947067201069606,
                    0.00243158189191776
                ],
                3: [
                    0.007267414955123511, 0.004693098774346077,
                    0.0030108089657996254
                ],
                4: [
                    0.007984189105222972, 0.005306454256749979,
                    0.003503658784554106
                ],
                5: [
                    0.008588497638287788, 0.005836894075283974,
                    0.003940852614881705
                ],
                6: [
                    0.009116053451079383, 0.006309422338116832,
                    0.004338265273606873
                ],
                7: [
                    0.009587298749506397, 0.0067386620346698055,
                    0.004705381710209659
                ],
                8: [
                    0.010015156021251479, 0.007134020107726916,
                    0.005048411044425698
                ],
                9: [
                    0.010408374529678119, 0.007501960502173291,
                    0.005371683357738421
                ]
            })

    @attr(all=True, unit=True)
    def test06_mean(self):
        """
        (TestWeibullDistribution) mean should return a dict on success.
        """

        _scale = [66.3454154, 76.3454154, 86.3454154]
        _shape = [1.3269671, 1.4269671, 1.5269671]

        _hazard = self.DUT.mean(_scale, _shape, 0, 10, 1)
        self.assertEqual(
            _hazard, {
                0:
                [61.030206749219012, 69.381805121273075, 77.785684088594323],
                1:
                [61.030206749219012, 69.381805121273075, 77.785684088594323],
                2:
                [61.030206749219012, 69.381805121273075, 77.785684088594323],
                3:
                [61.030206749219012, 69.381805121273075, 77.785684088594323],
                4:
                [61.030206749219012, 69.381805121273075, 77.785684088594323],
                5:
                [61.030206749219012, 69.381805121273075, 77.785684088594323],
                6:
                [61.030206749219012, 69.381805121273075, 77.785684088594323],
                7:
                [61.030206749219012, 69.381805121273075, 77.785684088594323],
                8:
                [61.030206749219012, 69.381805121273075, 77.785684088594323],
                9:
                [61.030206749219012, 69.381805121273075, 77.785684088594323]
            })

    @attr(all=True, unit=True)
    def test07_reliability_function(self):
        """
        (TestWeibullDistribution) reliability_function should return a dict on success.
        """

        _scale = [66.3454154, 76.3454154, 86.3454154]
        _shape = [1.3269671, 1.4269671, 1.5269671]

        _reliability = self.DUT.reliability_function(_scale, _shape, 0, 10, 1)
        self.assertEqual(
            _reliability, {
                0: [1.0, 1.0, 1.0],
                1:
                [0.99889544751808501, 0.99794465863991877, 0.9961833112443863],
                2: [
                    0.99682021454755243, 0.99448316712080143,
                    0.99045244366545393
                ],
                3: [
                    0.99410218801703698, 0.99018192718749565,
                    0.98370410624090121
                ],
                4: [
                    0.99086390421613801, 0.98523530625620048,
                    0.97621983054287942
                ],
                5: [
                    0.98717871887512199, 0.97975562801344362,
                    0.96815664522168388
                ],
                6: [
                    0.98309787489269929, 0.97381944516723418,
                    0.95961890423741114
                ],
                7: [
                    0.97866033325361712, 0.96748382991224402,
                    0.95068281812092714
                ],
                8: [
                    0.97389736979356656, 0.96079383124840101,
                    0.94140745845970919
                ],
                9:
                [0.96883505989725838, 0.9537864420601545, 0.9318405249350149]
            })

    @attr(all=True, unit=True)
    def test08_log_likelihood_ratio(self):
        """
        (TestWeibullDistribution) log_likelihood_ratio should return a float value on success.
        """

        _params = [68.4519239, 1.8118217]
        _const = 3.8414588 / 2.0

        _log_lik_ratio = self.DUT.log_likelihood_ratio(_params, self.NELSON,
                                                       _const)
        self.assertAlmostEqual(_log_lik_ratio, -313.7674954)

    @attr(all=True, unit=True)
    def test09_likelihood_bounds(self):
        """
        (TestWeibullDistribution) likelihood_bounds should return a tuple of OrderedDicts on success.
        """

        _params = [33.9428, 2.2938]

        _lik_bounds = self.DUT.likelihood_bounds(_params, 0.9, self.DATA2)

        # Check the first lower and upper bounds on eta and beta.
        self.assertAlmostEqual(_lik_bounds[0], 33.8007446)
        self.assertAlmostEqual(_lik_bounds[1], 36.1394417)
        self.assertAlmostEqual(_lik_bounds[2], 1.1469000)
        self.assertAlmostEqual(_lik_bounds[3], 3.9240973)


class TestTBF(unittest.TestCase):
    """
    Class to test time between failure calculations.
    """

    DATA = {
        0: (59, '', 719163, 16.0, 16.0, 1, 1, 16.0, 1, 0, 719163, 719163, 0.0,
            0.0, 0.0, 0, 0, 0, 'None', 'None', 'None'),
        1: (59, '', 719163, 34.0, 34.0, 1, 1, 18.0, 1, 0, 719163, 719163, 0.0,
            0.0, 0.0, 0, 0, 0, 'None', 'None', 'None'),
        2: (59, '', 719163, 53.0, 53.0, 1, 1, 19.0, 1, 0, 719163, 719163, 0.0,
            0.0, 0.0, 0, 0, 0, 'None', 'None', 'None'),
        3: (59, '', 719163, 5.0, 75.0, 1, 3, 22.0, 1, 0, 719163, 719163, 0.0,
            0.0, 0.0, 0, 0, 0, 'None', 'None', 'None'),
        4: (59, '', 719163, 93.0, 93.0, 2, 1, 18.0, 1, 0, 719163, 719163, 0.0,
            0.0, 0.0, 0, 0, 0, 'None', 'None', 'None')
    }

    def setUp(self):
        """
        Setup the test fixture for the Exponential distribution class.
        """

        self.record1 = Record()
        self.record1.set_attributes(self.DATA[0])
        self.record2 = Record()
        self.record2.set_attributes(self.DATA[1])
        self.record3 = Record()
        self.record3.set_attributes(self.DATA[2])
        self.record4 = Record()
        self.record4.set_attributes(self.DATA[3])
        self.record5 = Record()
        self.record5.set_attributes(self.DATA[4])

    @attr(all=True, unit=True)
    def test01_exact_failure_times(self):
        """
        (TestTBF) Test of the time between failure calculation for exact failure times.
        """

        # Test exact failure time records.
        self.assertEqual(
            time_between_failures(self.record1, self.record2), 18.0)

        self.assertEqual(
            time_between_failures(self.record2, self.record3), 19.0)

    @attr(all=True, unit=True)
    def test02_right_censored_times(self):
        """
        (TestTBF) Test of the time between failure calculation for right censored failure times.
        """

        # Test right censored records.
        self.assertEqual(
            time_between_failures(self.record4, self.record5), 1E+99)

    @attr(all=True, unit=True)
    def test03_interval_censored_times(self):
        """
        (TestTBF) Test of the time between failure calculation for interval censored failure times.
        """

        # Test interval censored records.
        self.assertEqual(
            time_between_failures(self.record3, self.record4), 22.0)
