#!/usr/bin/env python -O
"""
This is the test class for testing the statistical distributions module
algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tests.statistics.TestDistributions.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr
import numpy as np

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

from analyses.statistics.Distributions import Exponential, Gaussian, LogNormal, Weibull, time_between_failures


class TestExponentialDistribution(unittest.TestCase):
    """
    Class for testing the Exponential distribution data model class.
    """

    # Data set of 100 exponentially distributed points with a mean of 100.
    EXP_TEST = [(u'', 48.146, 48.146, 48.146, 1, 1), (u'', 20.564, 20.564, 20.564, 1, 1),
                (u'', 94.072, 94.072, 94.072, 1, 1), (u'', 177.992, 177.992, 177.992, 1, 1),
                (u'', 89.103, 89.103, 89.103, 1, 1), (u'', 350.577, 350.577, 350.577, 1, 1),
                (u'', 82.223, 82.223, 82.223, 1, 1), (u'', 40.360, 40.360, 40.360, 1, 1),
                (u'', 39.576, 39.576, 39.576, 1, 1), (u'', 53.127, 53.127, 53.127, 1, 1),
                (u'', 159.732, 159.732, 159.732, 1, 1), (u'', 48.398, 48.398, 48.398, 1, 1),
                (u'', 46.984, 46.984, 46.984, 1, 1), (u'', 36.169, 36.169, 36.169, 1, 1),
                (u'', 351.347, 351.347, 351.347, 1, 1), (u'', 18.917, 18.917, 18.917, 1, 1),
                (u'', 101.977, 101.977, 101.977, 1, 1), (u'', 141.988, 141.988, 141.988, 1, 1),
                (u'', 241.044, 241.044, 241.044, 1, 1), (u'', 61.993, 61.993, 61.993, 1, 1),
                (u'', 171.813, 171.813, 171.813, 1, 1), (u'', 78.747, 78.747, 78.747, 1, 1),
                (u'', 54.070, 54.070, 54.070, 1, 1), (u'', 87.229, 87.229, 87.229, 1, 1),
                (u'', 158.980, 158.980, 158.980, 1, 1), (u'', 185.254, 185.254, 185.254, 1, 1),
                (u'', 16.452, 16.452, 16.452, 1, 1), (u'', 120.144, 120.144, 120.144, 1, 1),
                (u'', 294.418, 294.418, 294.418, 1, 1), (u'', 13.640, 13.640, 13.640, 1, 1),
                (u'', 115.532, 115.532, 115.532, 1, 1), (u'', 58.595, 58.595, 58.595, 1, 1),
                (u'', 7.876, 7.876, 7.876, 1, 1), (u'', 10.790, 10.790, 10.790, 1, 1),
                (u'', 67.342, 67.342, 67.342, 1, 1), (u'', 14.848, 14.848, 14.848, 1, 1),
                (u'', 82.160, 82.160, 82.160, 1, 1), (u'', 14.558, 14.558, 14.558, 1, 1),
                (u'', 18.793, 18.793, 18.793, 1, 1), (u'', 69.776, 69.776, 69.776, 1, 1),
                (u'', 65.542, 65.542, 65.542, 1, 1), (u'', 194.039, 194.039, 194.039, 1, 1),
                (u'', 41.559, 41.559, 41.559, 1, 1), (u'', 75.549, 75.549, 75.549, 1, 1),
                (u'', 14.808, 14.808, 14.808, 1, 1), (u'', 184.263, 184.263, 184.263, 1, 1),
                (u'', 2.810, 2.810, 2.810, 1, 1), (u'', 13.095, 13.095, 13.095, 1, 1),
                (u'', 52.885, 52.885, 52.885, 1, 1), (u'', 49.855, 49.855, 49.855, 1, 1),
                (u'', 263.548, 263.548, 263.548, 1, 1), (u'', 4.248, 4.248, 4.248, 1, 1),
                (u'', 66.864, 66.864, 66.864, 1, 1), (u'', 172.663, 172.663, 172.663, 1, 1),
                (u'', 226.918, 226.918, 226.918, 1, 1), (u'', 169.175, 169.175, 169.175, 1, 1),
                (u'', 148.070, 148.070, 148.070, 1, 1), (u'', 3.679, 3.679, 3.679, 1, 1),
                (u'', 28.693, 28.693, 28.693, 1, 1), (u'', 34.931, 34.931, 34.931, 1, 1),
                (u'', 297.467, 297.467, 297.467, 1, 1), (u'', 137.072, 137.072, 137.072, 1, 1),
                (u'', 53.180, 53.180, 53.180, 1, 1), (u'', 49.760, 49.760, 49.760, 1, 1),
                (u'', 19.664, 19.664, 19.664, 1, 1), (u'', 96.415, 96.415, 96.415, 1, 1),
                (u'', 14.003, 14.003, 14.003, 1, 1), (u'', 17.743, 17.743, 17.743, 1, 1),
                (u'', 212.279, 212.279, 212.279, 1, 1), (u'', 38.951, 38.951, 38.951, 1, 1),
                (u'', 74.057, 74.057, 74.057, 1, 1), (u'', 86.769, 86.769, 86.769, 1, 1),
                (u'', 37.765, 37.765, 37.367, 1, 1), (u'', 5.566, 5.566, 5.566, 1, 1),
                (u'', 71.048, 71.048, 71.048, 1, 1), (u'', 5.137, 5.137, 5.137, 1, 1),
                (u'', 35.461, 35.461, 35.461, 1, 1), (u'', 121.963, 121.963, 121.963, 1, 1),
                (u'', 42.486, 42.486, 42.486, 1, 1), (u'', 52.315, 52.315, 52.315, 1, 1),
                (u'', 77.095, 77.095, 77.095, 1, 1), (u'', 14.259, 14.259, 14.259, 1, 1),
                (u'', 111.147, 111.147, 111.147, 1, 1), (u'', 49.364, 49.364, 49.364, 1, 1),
                (u'', 1.978, 1.978, 1.978, 1, 1), (u'', 163.827, 163.827, 163.827, 1, 1),
                (u'', 66.690, 66.690, 66.690, 1, 1), (u'', 80.172, 80.172, 80.172, 1, 1),
                (u'', 323.763, 323.763, 323.763, 1, 1), (u'', 275.491, 275.491, 275.491, 1, 1),
                (u'', 49.315, 49.315, 49.315, 1, 1), (u'', 1.585, 1.585, 1.585, 1, 1),
                (u'', 317.922, 317.922, 317.922, 1, 1), (u'', 12.398, 12.398, 12.398, 1, 1),
                (u'', 222.930, 222.930, 222.930, 1, 1), (u'', 6.328, 6.328, 6.328, 1, 1),
                (u'', 143.687, 143.687, 143.687, 1, 1), (u'', 134.763, 134.763, 134.763, 1, 1),
                (u'', 88.862, 88.862, 88.862, 1, 1), (u'', 143.918, 143.918, 143.918, 1, 1)]

    # Data set of alpha particle interarrival times.
    # Data is from Table 7.1 in Meeker and Excobar.
    ALPHA = [(u'', 0.0, 100.0, 50.0, 3, 1609, 3),
             (u'', 100.0, 300.0, 200.0, 3, 2424, 3),
             (u'', 300.0, 500.0, 400.0, 3, 1770, 3),
             (u'', 500.0, 700.0, 600.0, 3, 1306, 3),
             (u'', 700.0, 1000.0, 850.0, 3, 1213, 3),
             (u'', 1000.0, 2000.0, 1500.0, 3, 1528, 3),
             (u'', 2000.0, 4000.0, 3000.0, 3, 354, 3),
             (u'', 4000.0, 0.0, np.inf, 2, 16, 2)]

    def setUp(self):
        """
        Setup the test fixture for the Exponential distribution class.
        """

        self.DUT = Exponential()

    @attr(all=True, unit=True)
    def test_log_pdf(self):
        """
        (TestExponentialDistribution) log_pdf should return a numpy array of floats on success
        """

        # Data is the same as that used in the ReliaSoft wiki examples.
        # The table can be found at the following URL, for example.
        # http://reliawiki.org/index.php/The_Lognormal_Distribution#Rank_Regression_on_Y
        # lambda = 0.02711 and rho = -0.9679 when fit to the EXP.
        _data = np.array([['', 0.0, 5.0, 0, 1, 1], ['', 0.0, 10.0, 0, 1, 1],
                          ['', 0.0, 15.0, 0, 1, 1], ['', 0.0, 20.0, 0, 1, 1],
                          ['', 0.0, 25.0, 0, 1, 1], ['', 0.0, 30.0, 0, 1, 1],
                          ['', 0.0, 35.0, 0, 1, 1], ['', 0.0, 40.0, 0, 1, 1],
                          ['', 0.0, 50.0, 0, 1, 1], ['', 0.0, 60.0, 0, 1, 1],
                          ['', 0.0, 70.0, 0, 1, 1], ['', 0.0, 80.0, 0, 1, 1],
                          ['', 0.0, 90.0, 0, 1, 1], ['', 0.0, 100.0, 0, 1, 1]])

        _log_pdf = self.DUT.log_pdf(np.array(_data[:, 2], dtype=float),
                                    0.02222222, 0.0)

        np.testing.assert_allclose(_log_pdf, [-3.91777369, -4.02888479,
                                              -4.13999589, -4.25110699,
                                              -4.36221809, -4.47332919,
                                              -4.58444029, -4.69555139,
                                              -4.91777359, -5.13999579,
                                              -5.36221799, -5.58444019,
                                              -5.80666239, -6.02888459])

    @attr(all=True, unit=True)
    def test_partial_derivatives_exact(self):
        """
        (TestExponentialDistribution) partial_derivatives should return a numpy array with exact data only on success.
        """

        # Leukemia remission times.  Data is from Example 7.2 of Lee and Wang.
        _data = np.array([[0.0, 1.0, 1, 1], [0.0, 1.0, 1, 1],
                          [0.0, 2.0, 1, 1], [0.0, 2.0, 1, 1],
                          [0.0, 3.0, 1, 1], [0.0, 4.0, 1, 1],
                          [0.0, 4.0, 1, 1], [0.0, 5.0, 1, 1],
                          [0.0, 5.0, 1, 1], [0.0, 6.0, 1, 1],
                          [0.0, 8.0, 1, 1], [0.0, 8.0, 1, 1],
                          [0.0, 9.0, 1, 1], [0.0, 10.0, 1, 1],
                          [0.0, 10.0, 1, 1], [0.0, 12.0, 1, 1],
                          [0.0, 14.0, 1, 1], [0.0, 16.0, 1, 1],
                          [0.0, 20.0, 1, 1], [0.0, 24.0, 1, 1],
                          [0.0, 34.0, 1, 1]])

        _part_deriv = self.DUT.partial_derivatives(1.0, _data)
        self.assertAlmostEqual(_part_deriv, -177.0)

    @attr(all=True, unit=True)
    def test_partial_derivatives_right(self):
        """
        (TestExponentialDistribution) partial_derivatives should return a numpy array with exact and right censored data on success.
        """

        # Cancerous mice data.  Data is from Example 7.3 in Lee and Wang.
        _data = np.array([[0.0, 4.0, 1, 1], [0.0, 5.0, 1, 1],
                          [0.0, 8.0, 1, 1], [0.0, 9.0, 1, 1],
                          [0.0, 10.0, 1, 1], [0.0, 10.0, 1, 2],
                          [0.0, 10.0, 1, 2], [0.0, 10.0, 1, 2],
                          [0.0, 10.0, 1, 2], [0.0, 10.0, 1, 2]])

        _part_deriv = self.DUT.partial_derivatives(1.0, _data)
        self.assertAlmostEqual(_part_deriv, -81.0)

    @attr(all=True, unit=True)
    def test_partial_derivs_interval(self):
        """
        (TestExponentialDistribution) partial_derivatives should return a numpy array with exact, right, and interval censored data on success.
        """

        # Danish AIDS patients.  Data retrieved from:
        # https://encrypted.google.com/books?id=Jwf3M6TtHTkC&pg=PA33&lpg=PA33&dq=exponential+data+set+example+with+interval+censoring&source=bl&ots=_VK8lx0yqP&sig=zbUtQTK8ZHR10Y5LDA_0aZz_OqI&hl=en&sa=X&ei=ekqwU8mWBtCGqgb204LwDw&ved=0CH4Q6AEwCQ#v=onepage&q=exponential%20data%20set%20example%20with%20interval%20censoring&f=false
        _data = np.array([[0.0, 24.0, 24, 3], [24.0, 39.0, 1, 3],
                          [24.0, 113.0, 4, 3], [28.0, 88.0, 1, 3],
                          [39.0, 113.0, 2, 3], [57.0, 113.0, 1, 3],
                          [0.0, 39.0, 2, 3], [24.0, 57.0, 10, 3],
                          [24.0, 28.0, 4, 3], [24.0, 88.0, 3, 3],
                          [28.0, 39.0, 4, 3], [39.0, 57.0, 3, 3],
                          [57.0, 88.0, 5, 3], [88.0, 113.0, 1, 3],
                          [0.0, 88.0, 34, 2], [0.0, 24.0, 61, 2],
                          [0.0, 28.0, 8, 2], [0.0, 39.0, 15, 2],
                          [0.0, 57.0, 22, 2], [0.0, 113.0, 92, 2]])

        # Parameter is 0.0034 for exponential.
        _part_deriv = self.DUT.partial_derivatives(0.0034, _data)
        self.assertAlmostEqual(_part_deriv, -33687.1470588)

    @attr(all=True, unit=True)
    def test_maximum_likelihood_estimate_exact_times(self):
        """
        (TestExponentialDistribution) maximum_likelihood_estimate should return a numpy array of floats on success with exact failure times.
        """

        _fit = self.DUT.maximum_likelihood_estimate(self.EXP_TEST, 0.0,
                                                    10000000.0)

        # Check the mean for exact failure time data.
        np.testing.assert_array_equal(_fit, [[0.010623949536239687, 0.0],
                                             [1.3218705847856434e-06, 0.0, 0.0],
                                             [-354.46019736384773,
                                              710.92039472769545,
                                              712.38083502783411]])

    @attr(all=True, unit=True)
    def test_maximum_likelihood_estimate_interval_censored(self):
        """
        (TestExponentialDistribution) maximum_likelihood_estimate should return a numpy array of floats on success with interval censored failure times.
        """

        _fit = self.DUT.maximum_likelihood_estimate(self.ALPHA, 0.0,
                                                    10000000.0)

        # Check the mean for exact failure time data.
        np.testing.assert_array_equal(_fit[0], [0.0015840045243129197, 0.0])

    @attr(all=True, unit=True)
    def test_theoretical_distribution(self):
        """
        (TestExponentialDistribution) theoretical_distribution should return a numpy array of floats on success.
        """

        _para = [0.0106235]

        _probs = self.DUT.theoretical_distribution(np.array(self.EXP_TEST),
                                                   _para)
        np.testing.assert_almost_equal(_probs,
                                       [0.01669728, 0.02079404, 0.02941086,
                                        0.03832994, 0.04412548, 0.05311054,
                                        0.05741615, 0.06501567, 0.08026591,
                                        0.10830182, 0.12340496, 0.12987181,
                                        0.13489513, 0.13822483, 0.14056535,
                                        0.14329095, 0.14556324, 0.14592625,
                                        0.16035645, 0.17179350, 0.18098054,
                                        0.18205874, 0.18852403, 0.19624570,
                                        0.26274399, 0.31001780, 0.31389180,
                                        0.31903296, 0.33048150, 0.33886416,
                                        0.34323935, 0.34868668, 0.35693022,
                                        0.36323208, 0.39294418, 0.40039192,
                                        0.40199499, 0.40779232, 0.40810052,
                                        0.41058535, 0.41117991, 0.42636869,
                                        0.42983176, 0.43129571, 0.43161583,
                                        0.43696453, 0.46339015, 0.48241558,
                                        0.50156667, 0.50760853, 0.50851787,
                                        0.51100731, 0.52348941, 0.52988523,
                                        0.54467532, 0.55183544, 0.55913595,
                                        0.56680563, 0.57331415, 0.58223105,
                                        0.58251057, 0.60219386, 0.60413312,
                                        0.61094146, 0.61193628, 0.63189015,
                                        0.64093963, 0.66154112, 0.69295782,
                                        0.70693305, 0.72094595, 0.72628666,
                                        0.76108674, 0.76687591, 0.77873839,
                                        0.78269619, 0.78322880, 0.79258251,
                                        0.81528183, 0.81675164, 0.82455262,
                                        0.83424270, 0.83882353, 0.84027239,
                                        0.84906379, 0.85879153, 0.86027036,
                                        0.87272094, 0.89514176, 0.90635993,
                                        0.91024427, 0.92275174, 0.93917791,
                                        0.94642532, 0.95618371, 0.95758023,
                                        0.96586542, 0.96791916, 0.97587134,
                                        0.97606791])


class TestGaussianDistribution(unittest.TestCase):
    """
    Class for testing the Gaussian distribution data model class.
    """

    # Data is the same as that used in the ReliaSoft wiki examples.
    # The table can be found at the following URL, for example.
    # http://reliawiki.org/index.php/The_Lognormal_Distribution#Rank_Regression_on_Y
    # mu = 45.0000, sigma = 33.5367 and rho = 0.9790 when fit to the GAU.
    DATA = np.array([['', 0.0, 5.0, 0, 1, 1], ['', 0.0, 10.0, 0, 1, 1],
                     ['', 0.0, 15.0, 0, 1, 1], ['', 0.0, 20.0, 0, 1, 1],
                     ['', 0.0, 25.0, 0, 1, 1], ['', 0.0, 30.0, 0, 1, 1],
                     ['', 0.0, 35.0, 0, 1, 1], ['', 0.0, 40.0, 0, 1, 1],
                     ['', 0.0, 50.0, 0, 1, 1], ['', 0.0, 60.0, 0, 1, 1],
                     ['', 0.0, 70.0, 0, 1, 1], ['', 0.0, 80.0, 0, 1, 1],
                     ['', 0.0, 90.0, 0, 1, 1], ['', 0.0, 100.0, 0, 1, 1]])

    DATA3 = np.array([['', 0.0, 24.0, 0.0, 3, 24], ['', 24.0, 39.0, 0.0, 3, 1],
                      ['', 24.0, 113.0, 0.0, 3, 4], ['', 28.0, 88.0, 0.0, 3, 1],
                      ['', 39.0, 113.0, 0.0, 3, 2], ['', 57.0, 113.0, 0.0, 3, 1],
                      ['', 0.0, 39.0, 0.0, 3, 2], ['', 24.0, 57.0, 0.0, 3, 10],
                      ['', 24.0, 28.0, 0.0, 3, 4], ['', 24.0, 88.0, 0.0, 3, 3],
                      ['', 28.0, 39.0, 0.0, 3, 4], ['', 39.0, 57.0, 0.0, 3, 3],
                      ['', 57.0, 88.0, 0.0, 3, 5], ['', 88.0, 113.0, 0.0, 3, 1],
                      ['', 0.0, 88.0, 0.0, 2, 34], ['', 0.0, 24.0, 0.0, 2, 61],
                      ['', 0.0, 28.0, 0.0, 2, 8], ['', 0.0, 39.0, 0.0, 2, 15],
                      ['', 0.0, 57.0, 0.0, 2, 22], ['', 0.0, 113.0, 0.0, 2, 92]])

    # Leukemia remission times.  Data is from Example 7.2 of Lee and Wang.
    LEUK = np.array([[0.0, 1.0, 1, 1], [0.0, 1.0, 1, 1],
                     [0.0, 2.0, 1, 1], [0.0, 2.0, 1, 1],
                     [0.0, 3.0, 1, 1], [0.0, 4.0, 1, 1],
                     [0.0, 4.0, 1, 1], [0.0, 5.0, 1, 1],
                     [0.0, 5.0, 1, 1], [0.0, 6.0, 1, 1],
                     [0.0, 8.0, 1, 1], [0.0, 8.0, 1, 1],
                     [0.0, 9.0, 1, 1], [0.0, 10.0, 1, 1],
                     [0.0, 10.0, 1, 1], [0.0, 12.0, 1, 1],
                     [0.0, 14.0, 1, 1], [0.0, 16.0, 1, 1],
                     [0.0, 20.0, 1, 1], [0.0, 24.0, 1, 1],
                     [0.0, 34.0, 1, 1]])

    # Cancerous mice data.  Data is from Example 7.3 in Lee and Wang.
    MICE = np.array([[0.0, 4.0, 1, 1], [0.0, 5.0, 1, 1],
                     [0.0, 8.0, 1, 1], [0.0, 9.0, 1, 1],
                     [0.0, 10.0, 1, 1], [0.0, 10.0, 1, 2],
                     [0.0, 10.0, 1, 2], [0.0, 10.0, 1, 2],
                     [0.0, 10.0, 1, 2], [0.0, 10.0, 1, 2]])

    # Danish AIDS patients.  Data retrieved from:
    # https://encrypted.google.com/books?id=Jwf3M6TtHTkC&pg=PA33&lpg=PA33&dq=exponential+data+set+example+with+interval+censoring&source=bl&ots=_VK8lx0yqP&sig=zbUtQTK8ZHR10Y5LDA_0aZz_OqI&hl=en&sa=X&ei=ekqwU8mWBtCGqgb204LwDw&ved=0CH4Q6AEwCQ#v=onepage&q=exponential%20data%20set%20example%20with%20interval%20censoring&f=false
    AIDS = np.array([[0.0, 24.0, 24, 3], [24.0, 39.0, 1, 3],
                     [24.0, 113.0, 4, 3], [28.0, 88.0, 1, 3],
                     [39.0, 113.0, 2, 3], [57.0, 113.0, 1, 3],
                     [0.0, 39.0, 2, 3], [24.0, 57.0, 10, 3],
                     [24.0, 28.0, 4, 3], [24.0, 88.0, 3, 3],
                     [28.0, 39.0, 4, 3], [39.0, 57.0, 3, 3],
                     [57.0, 88.0, 5, 3], [88.0, 113.0, 1, 3],
                     [0.0, 88.0, 34, 2], [0.0, 24.0, 61, 2],
                     [0.0, 28.0, 8, 2], [0.0, 39.0, 15, 2],
                     [0.0, 57.0, 22, 2], [0.0, 113.0, 92, 2]])

    # Data set of 100 normally distributed points a mean of 100.0 and a
    # variance of 10.0
    NORM_TEST = [(u'', 95.370, 95.370, 95.370, 1, 1), (u'', 0.0, 114.011, 114.011, 1, 1),
                 (u'', 0.0, 113.246, 113.246, 1, 1), (u'', 0.0, 109.167, 109.167, 1, 1),
                 (u'', 0.0, 104.227, 104.227, 1, 1), (u'', 107.109, 107.109, 107.109, 1, 1),
                 (u'', 0.0, 117.43215, 117.43215, 1, 1), (u'', 0.0, 94.785, 94.785, 1, 1),
                 (u'', 0.0, 83.56718, 83.56718, 1, 1), (u'', 0.0, 103.501, 103.501, 1, 1),
                 (u'', 89.931, 89.931, 89.931, 1, 1), (u'', 0.0, 120.455, 120.455, 1, 1),
                 (u'', 0.0, 97.081, 97.081, 1, 1), (u'', 0.0, 96.813, 96.813, 1, 1),
                 (u'', 0.0, 97.571, 97.571, 1, 1), (u'', 106.757, 106.757, 106.757, 1, 1),
                 (u'', 0.0, 99.335, 99.335, 1, 1), (u'', 0.0, 104.538, 104.538, 1, 1),
                 (u'', 0.0, 102.028, 102.028, 1, 1), (u'', 0.0, 90.032, 90.032, 1, 1),
                 (u'', 77.542, 77.542, 77.542, 1, 1), (u'', 0.0, 102.761, 102.761, 1, 1),
                 (u'', 0.0, 82.485, 82.485, 1, 1), (u'', 0.0, 77.743, 77.743, 1, 1),
                 (u'', 0.0, 109.974, 109.974, 1, 1), (u'', 94.851, 94.851, 94.851, 1, 1),
                 (u'', 0.0, 89.771, 89.771, 1, 1), (u'', 0.0, 98.193, 98.193, 1, 1),
                 (u'', 0.0, 102.165, 102.165, 1, 1), (u'', 0.0, 96.783, 96.783, 1, 1),
                 (u'', 108.865, 108.865, 108.865, 1, 1), (u'', 0.0, 120.462, 120.462, 1, 1),
                 (u'', 0.0, 111.592, 111.592, 1, 1), (u'', 0.0, 106.148, 106.148, 1, 1),
                 (u'', 0.0, 102.946, 102.946, 1, 1), (u'', 111.290, 111.290, 111.290, 1, 1),
                 (u'', 0.0, 106.002, 106.002, 1, 1), (u'', 0.0, 114.617, 114.617, 1, 1),
                 (u'', 0.0, 88.229, 88.229, 1, 1), (u'', 0.0, 131.364, 131.364, 1, 1),
                 (u'', 86.855, 86.855, 86.855, 1, 1), (u'', 0.0, 109.927, 109.927, 1, 1),
                 (u'', 0.0, 75.116, 75.116, 1, 1), (u'', 0.0, 100.465, 100.465, 1, 1),
                 (u'', 0.0, 97.783, 97.783, 1, 1), (u'', 108.169, 108.169, 108.169, 1, 1),
                 (u'', 0.0, 98.851, 98.851, 1, 1), (u'', 0.0, 99.310, 99.310, 1, 1),
                 (u'', 0.0, 94.588, 94.588, 1, 1), (u'', 0.0, 98.123, 98.123, 1, 1),
                 (u'', 115.666, 115.666, 115.666, 1, 1), (u'', 0.0, 104.491, 104.491, 1, 1),
                 (u'', 0.0, 93.490, 93.490, 1, 1), (u'', 0.0, 111.794, 111.794, 1, 1),
                 (u'', 0.0, 114.320, 114.320, 1, 1), (u'', 106.938, 106.938, 106.938, 1, 1),
                 (u'', 0.0, 106.450, 106.450, 1, 1), (u'', 0.0, 103.105, 103.105, 1, 1),
                 (u'', 0.0, 107.781, 107.781, 1, 1), (u'', 0.0, 120.846, 120.846, 1, 1),
                 (u'', 100.102, 100.102, 100.102, 1, 1), (u'', 0.0, 92.930, 92.930, 1, 1),
                 (u'', 0.0, 101.246, 101.246, 1, 1), (u'', 0.0, 69.517, 69.517, 1, 1),
                 (u'', 0.0, 106.276, 106.276, 1, 1), (u'', 99.046, 99.046, 99.046, 1, 1),
                 (u'', 0.0, 101.300, 101.300, 1, 1), (u'', 0.0, 98.588, 98.588, 1, 1),
                 (u'', 0.0, 110.022, 110.022, 1, 1), (u'', 0.0, 91.255, 91.255, 1, 1),
                 (u'', 106.687, 106.687, 106.687, 1, 1), (u'', 0.0, 102.443, 102.443, 1, 1),
                 (u'', 0.0, 100.342, 100.342, 1, 1), (u'', 0.0, 96.635, 96.635, 1, 1),
                 (u'', 0.0, 80.909, 80.909, 1, 1), (u'', 111.080, 111.080, 111.080, 1, 1),
                 (u'', 0.0, 107.005, 107.005, 1, 1), (u'', 0.0, 103.043, 103.043, 1, 1),
                 (u'', 0.0, 92.660, 92.660, 1, 1), (u'', 0.0, 81.526, 81.526, 1, 1),
                 (u'', 94.497, 94.497, 94.497, 1, 1), (u'', 0.0, 88.791, 88.791, 1, 1),
                 (u'', 0.0, 97.913, 97.913, 1, 1), (u'', 0.0, 96.120, 96.120, 1, 1),
                 (u'', 0.0, 101.234, 101.234, 1, 1), (u'', 95.132, 95.132, 95.132, 1, 1),
                 (u'', 0.0, 93.939, 93.939, 1, 1), (u'', 0.0, 92.302, 92.302, 1, 1),
                 (u'', 0.0, 96.536, 96.536, 1, 1), (u'', 0.0, 110.747, 110.747, 1, 1),
                 (u'', 99.888, 99.888, 99.888, 1, 1), (u'', 0.0, 92.780, 92.780, 1, 1),
                 (u'', 0.0, 107.678, 107.678, 1, 1), (u'', 0.0, 96.187, 96.187, 1, 1),
                 (u'', 0.0, 87.938, 87.938, 1, 1), (u'', 91.664, 91.664, 91.664, 1, 1),
                 (u'', 0.0, 106.149, 106.149, 1, 1), (u'', 0.0, 104.320, 104.320, 1, 1),
                 (u'', 0.0, 115.681, 115.681, 1, 1), (u'', 0.0, 95.920, 95.920, 1, 1)]

    # Data set of alpha particle interarrival times.
    # Data is from Table 7.1 in Meeker and Excobar.
    ALPHA = [(u'', 0.0, 100.0, 50.0, 3, 1609, 3),
             (u'', 100.0, 300.0, 200.0, 3, 2424, 3),
             (u'', 300.0, 500.0, 400.0, 3, 1770, 3),
             (u'', 500.0, 700.0, 600.0, 3, 1306, 3),
             (u'', 700.0, 1000.0, 850.0, 3, 1213, 3),
             (u'', 1000.0, 2000.0, 1500.0, 3, 1528, 3),
             (u'', 2000.0, 4000.0, 3000.0, 3, 354, 3),
             (u'', 4000.0, 0.0, np.inf, 2, 16, 2)]

    def setUp(self):
        """
        Setup the test fixture for the Gaussian distribution class.
        """

        self.DUT = Gaussian()

    @attr(all=True, unit=False)
    def test_log_pdf(self):
        """
        (TestGaussianDistribution) log_pdf should return a numpy array of floats on success
        """

        _log_pdf = self.DUT.log_pdf(np.array(_data[:, 2], dtype=float),
                                    0.02222222)

        np.testing.assert_allclose(_log_pdf, [-3.91777369, -4.02888479,
                                              -4.13999589, -4.25110699,
                                              -4.36221809, -4.47332919,
                                              -4.58444029, -4.69555139,
                                              -4.91777359, -5.13999579,
                                              -5.36221799, -5.58444019,
                                              -5.80666239, -6.02888459])

    @attr(all=True, unit=True)
    def test_partial_derivatives_exact(self):
        """
        (TestGaussianDistribution) partial_derivatives should return a numpy array with exact data only on success.
        """

        _part_deriv = self.DUT.partial_derivatives([1.0, 1.0], self.LEUK)
        np.testing.assert_array_equal(_part_deriv, [177.0, 156.0])

    @attr(all=True, unit=True)
    def test_partial_derivatives_right(self):
        """
        (TestGaussianDistribution) partial_derivatives should return a numpy array with exact and right censored data on success.
        """

        _part_deriv = self.DUT.partial_derivatives([1.0, 1.0], self.MICE)
        np.testing.assert_array_equal(_part_deriv,
                                      [31.000000005139885, 26.000000046258979])

    @attr(all=True, unit=True)
    def test_partial_derivs_interval(self):
        """
        (TestGaussianDistribution) partial_derivatives should return a numpy array with exact, right, and interval censored data on success.
        """

        _part_deriv = self.DUT.partial_derivatives([1.0, 1.0], self.AIDS)
        np.testing.assert_array_equal(_part_deriv, [-2280.5, -2215.5])

    @attr(all=True, unit=True)
    def test_maximum_likelihood_estimate_exact_times(self):
        """
        (TestGaussianDistribution) maximum_likelihood_estimate should return a numpy array of floats on success with exact failure times.
        """

        _fit = self.DUT.maximum_likelihood_estimate(self.NORM_TEST, 0.0,
                                                    10000000.0)

        self.assertAlmostEqual(_fit, [[100.52835329999998, 10.544214011396397],
                                      [0.013433998289642346,
                                       0.00016325951747108081, 0.0],
                                      [-4925.9514001639964, 9853.9028003279927,
                                       9855.3632406281322]])

    @attr(all=True, unit=False)
    def test_maximum_likelihood_estimate_interval_censored(self):
        """
        (TestGaussianDistribution) maximum_likelihood_estimate should return a numpy array of floats on success with interval censored failure times.
        """

        _fit = self.DUT.maximum_likelihood_estimate(self.ALPHA, 0.0,
                                                    10000000.0)

        self.assertAlmostEqual(_fit, [[100.52835329999998, 10.544214011396397],
                                      [0.013433998289642346,
                                       0.00016325951747108081, 0.0],
                                      [-4925.9514001639964, 9853.9028003279927,
                                       9855.3632406281322]])

    @attr(all=True, unit=True)
    def test_theoretical_distribution(self):
        """
        (TestGaussianDistribution) theoretical_distribution should return a numpy array of floats on success.
        """

        _para = [3.51585540, 0.9693628]

        _probs = self.DUT.theoretical_distribution(np.array(self.NORM_TEST),
                                                   _para)
        np.testing.assert_almost_equal(_probs,
                                       [0.77301140, 0.79636301, 0.80551501,
                                        0.80624920, 0.81735471, 0.81942240,
                                        0.82257652, 0.82605078, 0.83608092,
                                        0.83922062, 0.84005099, 0.84163904,
                                        0.84435988, 0.84479835, 0.84507431,
                                        0.84836621, 0.84944693, 0.85111299,
                                        0.85203744, 0.85234566, 0.85272977,
                                        0.85415243, 0.85528031, 0.85666638,
                                        0.85689079, 0.85737507, 0.85753684,
                                        0.85822295, 0.85880074, 0.86012441,
                                        0.86060177, 0.86076122, 0.86158798,
                                        0.86182135, 0.86216929, 0.86223968,
                                        0.86286644, 0.86400292, 0.86449086,
                                        0.86478895, 0.86526870, 0.86542813,
                                        0.86632323, 0.86691495, 0.86735151,
                                        0.86793960, 0.86799512, 0.86921549,
                                        0.86968384, 0.87020654, 0.87047337,
                                        0.87212572, 0.87215129, 0.87226626,
                                        0.87380341, 0.87409002, 0.87466902,
                                        0.87532714, 0.87570796, 0.87590704,
                                        0.87603407, 0.87684149, 0.87830426,
                                        0.87849002, 0.87883063, 0.87892403,
                                        0.88178762, 0.88206840, 0.88207032,
                                        0.88231385, 0.88264647, 0.88309757,
                                        0.88323038, 0.88357289, 0.88369935,
                                        0.88389529, 0.88495985, 0.88515122,
                                        0.88586842, 0.88714058, 0.88768691,
                                        0.88904682, 0.88913022, 0.88921532,
                                        0.89049046, 0.89106983, 0.89143317,
                                        0.89195297, 0.89229887, 0.89474384,
                                        0.89600337, 0.89650663, 0.89698740,
                                        0.89866273, 0.89868643, 0.90140525,
                                        0.90588223, 0.90589229, 0.90644214,
                                        0.92002587])


class TestLogNormalDistribution(unittest.TestCase):
    """
    Class for testing the LogNormal distribution data model class.
    """

    # Data is the same as that used in the ReliaSoft wiki examples.
    # The table can be found at the following URL, for example.
    # http://reliawiki.org/index.php/The_Lognormal_Distribution#Rank_Regression_on_Y
    # mu = 3.516, sigma = 0.9663, and rho = 0.9754 when fit to the LNORM.
    LOGN_TEST = np.array([['', 5.0, 5.0, 5.0, 1, 1],
                          ['', 10.0, 10.0, 5.0, 1, 1],
                          ['', 15.0, 15.0, 5.0, 1, 1],
                          ['', 20.0, 20.0, 5.0, 1, 1],
                          ['', 25.0, 25.0, 5.0, 1, 1],
                          ['', 30.0, 30.0, 5.0, 1, 1],
                          ['', 35.0, 35.0, 5.0, 1, 1],
                          ['', 40.0, 40.0, 5.0, 1, 1],
                          ['', 50.0, 50.0, 10.0, 1, 1],
                          ['', 60.0, 60.0, 10.0, 1, 1],
                          ['', 70.0, 70.0, 10.0, 1, 1],
                          ['', 80.0, 80.0, 10.0, 1, 1],
                          ['', 90.0, 90.0, 10.0, 1, 1],
                          ['', 100.0, 100.0, 10.0, 1, 1]])

    DATA3 = np.array([['', 0.0, 24.0, 0.0, 3, 24],
                      ['', 24.0, 39.0, 0.0, 3, 1],
                      ['', 24.0, 113.0, 0.0, 3, 4],
                      ['', 28.0, 88.0, 0.0, 3, 1],
                      ['', 39.0, 113.0, 0.0, 3, 2],
                      ['', 57.0, 113.0, 0.0, 3, 1],
                      ['', 0.0, 39.0, 0.0, 3, 2],
                      ['', 24.0, 57.0, 0.0, 3, 10],
                      ['', 24.0, 28.0, 0.0, 3, 4],
                      ['', 24.0, 88.0, 0.0, 3, 3],
                      ['', 28.0, 39.0, 0.0, 3, 4],
                      ['', 39.0, 57.0, 0.0, 3, 3],
                      ['', 57.0, 88.0, 0.0, 3, 5],
                      ['', 88.0, 113.0, 0.0, 3, 1],
                      ['', 0.0, 88.0, 0.0, 2, 34],
                      ['', 0.0, 24.0, 0.0, 2, 61],
                      ['', 0.0, 28.0, 0.0, 2, 8],
                      ['', 0.0, 39.0, 0.0, 2, 15],
                      ['', 0.0, 57.0, 0.0, 2, 22],
                      ['', 0.0, 113.0, 0.0, 2, 92]])

    # Data set of alpha particle interarrival times.
    # Data is from Table 7.1 in Meeker and Excobar.
    ALPHA = [(u'', 0.0, 100.0, 50.0, 3, 1609, 3),
             (u'', 100.0, 300.0, 200.0, 3, 2424, 3),
             (u'', 300.0, 500.0, 400.0, 3, 1770, 3),
             (u'', 500.0, 700.0, 600.0, 3, 1306, 3),
             (u'', 700.0, 1000.0, 850.0, 3, 1213, 3),
             (u'', 1000.0, 2000.0, 1500.0, 3, 1528, 3),
             (u'', 2000.0, 4000.0, 3000.0, 3, 354, 3),
             (u'', 4000.0, 0.0, np.inf, 2, 16, 2)]

    def setUp(self):
        """
        Setup the test fixture for the LogNormal distribution class.
        """

        self.DUT = LogNormal()

    @attr(all=True, unit=False)
    def test_log_pdf(self):
        """
        (TestLogNormalDistribution) log_pdf should return a numpy array of floats on success
        """

        # Data is the same as that used in the ReliaSoft wiki examples.
        # The table can be found at the following URL, for example.
        # http://reliawiki.org/index.php/The_Lognormal_Distribution#Rank_Regression_on_Y
        # lambda = 0.02711 and rho = -0.9679 when fit to the EXP.
        _data = np.array([['', 0.0, 5.0, 0, 1, 1], ['', 0.0, 10.0, 0, 1, 1],
                          ['', 0.0, 15.0, 0, 1, 1], ['', 0.0, 20.0, 0, 1, 1],
                          ['', 0.0, 25.0, 0, 1, 1], ['', 0.0, 30.0, 0, 1, 1],
                          ['', 0.0, 35.0, 0, 1, 1], ['', 0.0, 40.0, 0, 1, 1],
                          ['', 0.0, 50.0, 0, 1, 1], ['', 0.0, 60.0, 0, 1, 1],
                          ['', 0.0, 70.0, 0, 1, 1], ['', 0.0, 80.0, 0, 1, 1],
                          ['', 0.0, 90.0, 0, 1, 1], ['', 0.0, 100.0, 0, 1, 1]])

        _log_pdf = self.DUT.log_pdf(np.array(_data[:, 2], dtype=float),
                                    0.02222222)

        np.testing.assert_allclose(_log_pdf, [-3.91777369, -4.02888479,
                                              -4.13999589, -4.25110699,
                                              -4.36221809, -4.47332919,
                                              -4.58444029, -4.69555139,
                                              -4.91777359, -5.13999579,
                                              -5.36221799, -5.58444019,
                                              -5.80666239, -6.02888459])

    @attr(all=True, unit=False)
    def test_partial_derivatives_exact(self):
        """
        (TestLogNormalDistribution) partial_derivatives should return a numpy array with exact data only on success.
        """

        # Leukemia remission times.  Data is from Example 7.2 of Lee and Wang.
        _data = np.array([[0.0, 1.0, 1, 1], [0.0, 1.0, 1, 1],
                          [0.0, 2.0, 1, 1], [0.0, 2.0, 1, 1],
                          [0.0, 3.0, 1, 1], [0.0, 4.0, 1, 1],
                          [0.0, 4.0, 1, 1], [0.0, 5.0, 1, 1],
                          [0.0, 5.0, 1, 1], [0.0, 6.0, 1, 1],
                          [0.0, 8.0, 1, 1], [0.0, 8.0, 1, 1],
                          [0.0, 9.0, 1, 1], [0.0, 10.0, 1, 1],
                          [0.0, 10.0, 1, 1], [0.0, 12.0, 1, 1],
                          [0.0, 14.0, 1, 1], [0.0, 16.0, 1, 1],
                          [0.0, 20.0, 1, 1], [0.0, 24.0, 1, 1],
                          [0.0, 34.0, 1, 1]])

        _part_deriv = self.DUT.partial_derivatives(1.0, _data)
        self.assertAlmostEqual(_part_deriv, -177.0)

    @attr(all=True, unit=False)
    def test_partial_derivatives_right(self):
        """
        (TestLogNormalDistribution) partial_derivatives should return a numpy array with exact and right censored data on success.
        """

        # Cancerous mice data.  Data is from Example 7.3 in Lee and Wang.
        _data = np.array([[0.0, 4.0, 1, 1], [0.0, 5.0, 1, 1],
                          [0.0, 8.0, 1, 1], [0.0, 9.0, 1, 1],
                          [0.0, 10.0, 1, 1], [0.0, 10.0, 1, 2],
                          [0.0, 10.0, 1, 2], [0.0, 10.0, 1, 2],
                          [0.0, 10.0, 1, 2], [0.0, 10.0, 1, 2]])

        _part_deriv = self.DUT.partial_derivatives(1.0, _data)
        self.assertAlmostEqual(_part_deriv, -81.0)

    @attr(all=True, unit=False)
    def test_partial_derivs_interval(self):
        """
        (TestLogNormalDistribution) partial_derivatives should return a numpy array with exact, right, and interval censored data on success.
        """

        # Danish AIDS patients.  Data retrieved from:
        # https://encrypted.google.com/books?id=Jwf3M6TtHTkC&pg=PA33&lpg=PA33&dq=lognormal+data+set+example+with+interval+censoring&source=bl&ots=_VK8lx0yqP&sig=zbUtQTK8ZHR10Y5LDA_0aZz_OqI&hl=en&sa=X&ei=ekqwU8mWBtCGqgb204LwDw&ved=0CH4Q6AEwCQ#v=onepage&q=lognormal%20data%20set%20example%20with%20interval%20censoring&f=false
        _data = np.array([[0.0, 24.0, 24, 3], [24.0, 39.0, 1, 3],
                          [24.0, 113.0, 4, 3], [28.0, 88.0, 1, 3],
                          [39.0, 113.0, 2, 3], [57.0, 113.0, 1, 3],
                          [0.0, 39.0, 2, 3], [24.0, 57.0, 10, 3],
                          [24.0, 28.0, 4, 3], [24.0, 88.0, 3, 3],
                          [28.0, 39.0, 4, 3], [39.0, 57.0, 3, 3],
                          [57.0, 88.0, 5, 3], [88.0, 113.0, 1, 3],
                          [0.0, 88.0, 34, 2], [0.0, 24.0, 61, 2],
                          [0.0, 28.0, 8, 2], [0.0, 39.0, 15, 2],
                          [0.0, 57.0, 22, 2], [0.0, 113.0, 92, 2]])

        # Parameter is 0.0034 for lognormal.
        _part_deriv = self.DUT.partial_derivatives(0.0034, _data)
        self.assertAlmostEqual(_part_deriv, -33687.1470588)

    @attr(all=True, unit=True)
    def test_maximum_likelihood_estimate_exact_times(self):
        """
        (TestLogNormalDistribution) maximum_likelihood_estimate should return a numpy array of floats on success with exact failure times.
        """

        _fit = self.DUT.maximum_likelihood_estimate(self.LOGN_TEST, 0.0,
                                                    10000000.0)

        # Check the mean for exact failure time data.
        np.testing.assert_array_equal(_fit, [[3.5158562951854764,
                                              0.84919082792737277],
                                             [0.013718125432992872,
                                              0.018092667346311871, 0.0],
                                             [-66.798518958197803,
                                              135.59703791639561,
                                              135.09136536016146]])

    @attr(all=True, unit=True)
    def test_maximum_likelihood_estimate_interval_censored(self):
        """
        (TestLogNormalDistribution) maximum_likelihood_estimate should return a numpy array of floats on success with interval censored failure times.
        """

        _fit = self.DUT.maximum_likelihood_estimate(self.ALPHA, 0.0,
                                                    10000000.0)

        # Check the log mean and log standard error for interval censored data.
        np.testing.assert_array_equal(_fit[0], [5.9082393480724802,
                                                1.1314062486429797])

        # Check the variance-covariance matrix for interval censored data.
        np.testing.assert_array_equal(_fit[2], [-25771.349714664608,
                                                51544.699429329215,
                                                51550.78680130712])

    @attr(all=True, unit=True)
    def test_theoretical_distribution(self):
        """
        (TestLogNormalDistribution) theoretical_distribution should return a numpy array of floats on success.
        """

        _para = [3.51585540, 0.9693628]

        _probs = self.DUT.theoretical_distribution(np.array(self.LOGN_TEST),
                                                   _para)
        np.testing.assert_almost_equal(_probs,
                                       [0.02472972, 0.10554292, 0.20252142,
                                        0.29596331, 0.37982014, 0.45305838,
                                        0.51636622, 0.57093317, 0.65869163,
                                        0.72472779, 0.77515821, 0.81425235,
                                        0.84498695, 0.86946088])


class TestWeibullDistribution(unittest.TestCase):
    """
    Class for testing the Weibull distribution data model class.
    """

    # Data is the same as that used in the ReliaSoft wiki examples.
    # The table can be found at the following URL, for example.
    # http://reliawiki.org/index.php/The_Weibull_Distribution#Rank_Regression_on_Y
    # eta = 76.318, beta = 1.4301, and rho = 0.9956 when fit to the WEI.
    DATA = np.array([['', 0.0, 16.0, 16.0, 1, 1], ['', 0.0, 34.0, 34.0, 1, 1],
                     ['', 0.0, 53.0, 53.0, 1, 1], ['', 0.0, 75.0, 75.0, 1, 1],
                     ['', 0.0, 93.0, 93.0, 1, 1], ['', 0.0, 120.0, 120.0, 1, 1]])

    DATA3 = np.array([['', 0.0, 24.0, 0.0, 24, 3], ['', 24.0, 39.0, 0.0, 1, 3],
                      ['', 24.0, 113.0, 0.0, 4, 3], ['', 28.0, 88.0, 0.0, 1, 3],
                      ['', 39.0, 113.0, 0.0, 2, 3], ['', 57.0, 113.0, 0.0, 1, 3],
                      ['', 0.0, 39.0, 0.0, 2, 3], ['', 24.0, 57.0, 0.0, 10, 3],
                      ['', 24.0, 28.0, 0.0, 4, 3], ['', 24.0, 88.0, 0.0, 3, 3],
                      ['', 28.0, 39.0, 0.0, 4, 3], ['', 39.0, 57.0, 0.0, 3, 3],
                      ['', 57.0, 88.0, 0.0, 5, 3], ['', 88.0, 113.0, 0.0, 1, 3],
                      ['', 0.0, 88.0, 0.0, 34, 2], ['', 0.0, 24.0, 0.0, 61, 2],
                      ['', 0.0, 28.0, 0.0, 8, 2], ['', 0.0, 39.0, 0.0, 15, 2],
                      ['', 0.0, 57.0, 0.0, 22, 2], ['', 0.0, 113.0, 0.0, 92, 2]])

    # Leukemia remission times.  Data is from Example 7.2 of Lee and Wang.
    LEUK = np.array([[0.0, 1.0, 1, 1], [0.0, 1.0, 1, 1],
                     [0.0, 2.0, 1, 1], [0.0, 2.0, 1, 1],
                     [0.0, 3.0, 1, 1], [0.0, 4.0, 1, 1],
                     [0.0, 4.0, 1, 1], [0.0, 5.0, 1, 1],
                     [0.0, 5.0, 1, 1], [0.0, 6.0, 1, 1],
                     [0.0, 8.0, 1, 1], [0.0, 8.0, 1, 1],
                     [0.0, 9.0, 1, 1], [0.0, 10.0, 1, 1],
                     [0.0, 10.0, 1, 1], [0.0, 12.0, 1, 1],
                     [0.0, 14.0, 1, 1], [0.0, 16.0, 1, 1],
                     [0.0, 20.0, 1, 1], [0.0, 24.0, 1, 1],
                     [0.0, 34.0, 1, 1]])

    # Cancerous mice data.  Data is from Example 7.3 in Lee and Wang.
    MICE = np.array([[0.0, 4.0, 1, 1], [0.0, 5.0, 1, 1],
                     [0.0, 8.0, 1, 1], [0.0, 9.0, 1, 1],
                     [0.0, 10.0, 1, 1], [0.0, 10.0, 1, 2],
                     [0.0, 10.0, 1, 2], [0.0, 10.0, 1, 2],
                     [0.0, 10.0, 1, 2], [0.0, 10.0, 1, 2]])

    # Danish AIDS patients.  Data retrieved from:
    # https://encrypted.google.com/books?id=Jwf3M6TtHTkC&pg=PA33&lpg=PA33&dq=exponential+data+set+example+with+interval+censoring&source=bl&ots=_VK8lx0yqP&sig=zbUtQTK8ZHR10Y5LDA_0aZz_OqI&hl=en&sa=X&ei=ekqwU8mWBtCGqgb204LwDw&ved=0CH4Q6AEwCQ#v=onepage&q=exponential%20data%20set%20example%20with%20interval%20censoring&f=false
    AIDS = np.array([[0.0, 24.0, 24, 3], [24.0, 39.0, 1, 3],
                     [24.0, 113.0, 4, 3], [28.0, 88.0, 1, 3],
                     [39.0, 113.0, 2, 3], [57.0, 113.0, 1, 3],
                     [0.0, 39.0, 2, 3], [24.0, 57.0, 10, 3],
                     [24.0, 28.0, 4, 3], [24.0, 88.0, 3, 3],
                     [28.0, 39.0, 4, 3], [39.0, 57.0, 3, 3],
                     [57.0, 88.0, 5, 3], [88.0, 113.0, 1, 3],
                     [0.0, 88.0, 34, 2], [0.0, 24.0, 61, 2],
                     [0.0, 28.0, 8, 2], [0.0, 39.0, 15, 2],
                     [0.0, 57.0, 22, 2], [0.0, 113.0, 92, 2]])

    # Data set of 100 exponentially distributed points with a mean of 100.
    EXP_TEST = [(u'', 48.146, 48.146, 0.0, 1, 1), (u'', 20.564, 20.564, 0.0, 1, 1),
                (u'', 94.072, 94.072, 0.0, 1, 1), (u'', 177.992, 177.992, 0.0, 1, 1),
                (u'', 89.103, 89.103, 0.0, 1, 1), (u'', 350.577, 350.577, 0.0, 1, 1),
                (u'', 82.223, 82.223, 0.0, 1, 1), (u'', 40.360, 40.360, 0.0, 1, 1),
                (u'', 39.576, 39.576, 0.0, 1, 1), (u'', 53.127, 53.127, 0.0, 1, 1),
                (u'', 159.732, 159.732, 0.0, 1, 1), (u'', 48.398, 48.398, 0.0, 1, 1),
                (u'', 46.984, 46.984, 0.0, 1, 1), (u'', 36.169, 36.169, 0.0, 1, 1),
                (u'', 351.347, 351.347, 0.0, 1, 1), (u'', 18.917, 18.917, 0.0, 1, 1),
                (u'', 101.977, 101.977, 0.0, 1, 1), (u'', 141.988, 141.988, 0.0, 1, 1),
                (u'', 241.044, 241.044, 0.0, 1, 1), (u'', 61.993, 61.993, 0.0, 1, 1),
                (u'', 171.813, 171.813, 0.0, 1, 1), (u'', 78.747, 78.747, 0.0, 1, 1),
                (u'', 54.070, 54.070, 0.0, 1, 1), (u'', 87.229, 87.229, 0.0, 1, 1),
                (u'', 158.980, 158.980, 0.0, 1, 1), (u'', 185.254, 185.254, 0.0, 1, 1),
                (u'', 16.452, 16.452, 0.0, 1, 1), (u'', 120.144, 120.144, 0.0, 1, 1),
                (u'', 294.418, 294.418, 0.0, 1, 1), (u'', 13.640, 13.640, 0.0, 1, 1),
                (u'', 115.532, 115.532, 0.0, 1, 1), (u'', 58.595, 58.595, 0.0, 1, 1),
                (u'', 7.876, 7.876, 0.0, 1, 1), (u'', 10.790, 10.790, 0.0, 1, 1),
                (u'', 67.342, 67.342, 0.0, 1, 1), (u'', 14.848, 14.848, 0.0, 1, 1),
                (u'', 82.160, 82.160, 0.0, 1, 1), (u'', 14.558, 14.558, 0.0, 1, 1),
                (u'', 18.793, 18.793, 0.0, 1, 1), (u'', 69.776, 69.776, 0.0, 1, 1),
                (u'', 65.542, 65.542, 0.0, 1, 1), (u'', 194.039, 194.039, 0.0, 1, 1),
                (u'', 41.559, 41.559, 0.0, 1, 1), (u'', 75.549, 75.549, 0.0, 1, 1),
                (u'', 14.808, 14.808, 0.0, 1, 1), (u'', 184.263, 184.263, 0.0, 1, 1),
                (u'', 2.810, 2.810, 0.0, 1, 1), (u'', 13.095, 13.095, 0.0, 1, 1),
                (u'', 52.885, 52.885, 0.0, 1, 1), (u'', 49.855, 49.855, 0.0, 1, 1),
                (u'', 263.548, 263.548, 0.0, 1, 1), (u'', 4.248, 4.248, 0.0, 1, 1),
                (u'', 66.864, 66.864, 0.0, 1, 1), (u'', 172.663, 172.663, 0.0, 1, 1),
                (u'', 226.918, 226.918, 0.0, 1, 1), (u'', 169.175, 169.175, 0.0, 1, 1),
                (u'', 148.070, 148.070, 0.0, 1, 1), (u'', 3.679, 3.679, 0.0, 1, 1),
                (u'', 28.693, 28.693, 0.0, 1, 1), (u'', 34.931, 34.931, 0.0, 1, 1),
                (u'', 297.467, 297.467, 0.0, 1, 1), (u'', 137.072, 137.072, 0.0, 1, 1),
                (u'', 53.180, 53.180, 0.0, 1, 1), (u'', 49.760, 49.760, 0.0, 1, 1),
                (u'', 19.664, 19.664, 0.0, 1, 1), (u'', 96.415, 96.415, 0.0, 1, 1),
                (u'', 14.003, 14.003, 0.0, 1, 1), (u'', 17.743, 17.743, 0.0, 1, 1),
                (u'', 212.279, 212.279, 0.0, 1, 1), (u'', 38.951, 38.951, 0.0, 1, 1),
                (u'', 74.057, 74.057, 0.0, 1, 1), (u'', 86.769, 86.769, 0.0, 1, 1),
                (u'', 37.765, 37.765, 0.0, 1, 1), (u'', 5.566, 5.566, 0.0, 1, 1),
                (u'', 71.048, 71.048, 0.0, 1, 1), (u'', 5.137, 5.137, 0.0, 1, 1),
                (u'', 35.461, 35.461, 0.0, 1, 1), (u'', 121.963, 121.963, 0.0, 1, 1),
                (u'', 42.486, 42.486, 0.0, 1, 1), (u'', 52.315, 52.315, 0.0, 1, 1),
                (u'', 77.095, 77.095, 0.0, 1, 1), (u'', 14.259, 14.259, 0.0, 1, 1),
                (u'', 111.147, 111.147, 0.0, 1, 1), (u'', 49.364, 49.364, 0.0, 1, 1),
                (u'', 1.978, 1.978, 0.0, 1, 1), (u'', 163.827, 163.827, 0.0, 1, 1),
                (u'', 66.690, 66.690, 0.0, 1, 1), (u'', 80.172, 80.172, 0.0, 1, 1),
                (u'', 323.763, 323.763, 0.0, 1, 1), (u'', 275.491, 275.491, 0.0, 1, 1),
                (u'', 49.315, 49.315, 0.0, 1, 1), (u'', 1.585, 1.585, 0.0, 1, 1),
                (u'', 317.922, 317.922, 0.0, 1, 1), (u'', 12.398, 12.398, 0.0, 1, 1),
                (u'', 222.930, 222.930, 0.0, 1, 1), (u'', 6.328, 6.328, 0.0, 1, 1),
                (u'', 143.687, 143.687, 0.0, 1, 1), (u'', 134.763, 134.763, 0.0, 1, 1),
                (u'', 88.862, 88.862, 0.0, 1, 1), (u'', 143.918, 143.918, 0.0, 1, 1)]

    # Data set of alpha particle interarrival times.
    # Data is from Table 7.1 in Meeker and Excobar.
    ALPHA = [(u'', 0.0, 100.0, 50.0, 3, 1609, 3),
             (u'', 100.0, 300.0, 200.0, 3, 2424, 3),
             (u'', 300.0, 500.0, 400.0, 3, 1770, 3),
             (u'', 500.0, 700.0, 600.0, 3, 1306, 3),
             (u'', 700.0, 1000.0, 850.0, 3, 1213, 3),
             (u'', 1000.0, 2000.0, 1500.0, 3, 1528, 3),
             (u'', 2000.0, 4000.0, 3000.0, 3, 354, 3),
             (u'', 4000.0, 0.0, np.inf, 2, 16, 2)]

    def setUp(self):
        """
        Setup the test fixture for the Weibull distribution class.
        """

        self.DUT = Weibull()

    @attr(all=True, unit=False)
    def test_log_pdf(self):
        """
        (TestWeibullDistribution) log_pdf should return a numpy array of floats on success
        """

        _log_pdf = self.DUT.log_pdf(np.array(_data[:, 2], dtype=float),
                                    0.02222222)

        np.testing.assert_allclose(_log_pdf, [-3.91777369, -4.02888479,
                                              -4.13999589, -4.25110699,
                                              -4.36221809, -4.47332919,
                                              -4.58444029, -4.69555139,
                                              -4.91777359, -5.13999579,
                                              -5.36221799, -5.58444019,
                                              -5.80666239, -6.02888459])

    @attr(all=True, unit=True)
    def test_partial_derivatives_exact(self):
        """
        (TestWeibullDistribution) partial_derivatives should return a numpy array with exact data only on success.
        """

        _part_deriv = self.DUT.partial_derivatives([1.0, 1.0], self.LEUK)
        np.testing.assert_array_equal(_part_deriv, [177.0, -450.4866935010138])

    @attr(all=True, unit=True)
    def test_partial_derivatives_right(self):
        """
        (TestWeibullDistribution) partial_derivatives should return a numpy array with exact and right censored data on success.
        """

        _part_deriv = self.DUT.partial_derivatives([1.0, 1.0], self.MICE)
        np.testing.assert_array_equal(_part_deriv,
                                      [-19.0, -173.5830426301934])

    @attr(all=True, unit=True)
    def test_partial_derivs_interval(self):
        """
        (TestWeibullDistribution) partial_derivatives should return a numpy array with exact, right, and interval censored data on success.
        """

        _part_deriv = self.DUT.partial_derivatives([1.0, 1.0], self.AIDS)
        np.testing.assert_array_equal(_part_deriv,
                                      [-14634.5, -83800.438465226223])

    @attr(all=True, unit=True)
    def test_maximum_likelihood_estimate_exact_times(self):
        """
        (TestWeibullDistribution) maximum_likelihood_estimate should return a numpy array of floats on success with exact failure times.
        """

        _fit = self.DUT.maximum_likelihood_estimate(self.DATA, 0.0,
                                                    10000000.0)

        # Check the mean for exact failure time data.
        np.testing.assert_array_equal(_fit, [[73.526132273502554,
                                              1.9326764449560938, 0.0],
                                             [318.97182199677735,
                                              0.67677512433323617,
                                              62.586199984304315],
                                             [-3917.8639405196277,
                                              7837.7278810392554,
                                              7836.3749106226342]])

    @attr(all=True, unit=True)
    def test_maximum_likelihood_estimate_interval_censored(self):
        """
        (TestWeibullDistribution) maximum_likelihood_estimate should return a numpy array of floats on success with interval censored failure times.
        """

        _fit = self.DUT.maximum_likelihood_estimate(self.ALPHA, 0.0,
                                                    10000000.0)

        # Check the scale and shape parameters for interval censored failure time data.
        np.testing.assert_array_equal(_fit[0], [635.02289090239196,
                                                1.0134226728030167, 0.0])

    @attr(all=True, unit=True)
    def test_theoretical_distribution(self):
        """
        (TestWeibullDistribution) theoretical_distribution should return a numpy array of floats on success.
        """

        _para = [76.3454154, 1.4269671]

        _probs = self.DUT.theoretical_distribution(np.array(self.EXP_TEST),
                                                   _para)
        np.testing.assert_almost_equal(_probs,
                                       [0.00396191, 0.00543068, 0.00894684,
                                        0.01311430, 0.01607735, 0.02103208,
                                        0.02355218, 0.02821701, 0.03835868,
                                        0.05945336, 0.07200798, 0.07762049,
                                        0.08207479, 0.08507205, 0.08719995,
                                        0.08969964, 0.09180128, 0.09213850,
                                        0.10586740, 0.11718375, 0.12654165,
                                        0.12765516, 0.13439830, 0.14259771,
                                        0.21922922, 0.27940212, 0.28451269,
                                        0.29133348, 0.30667514, 0.31803657,
                                        0.32400771, 0.33148024, 0.34286626,
                                        0.35163095, 0.39359384, 0.40426006,
                                        0.40656280, 0.41490977, 0.41535434,
                                        0.41894165, 0.41980077, 0.44184265,
                                        0.44689168, 0.44902846, 0.44949589,
                                        0.45731530, 0.49616338, 0.52427934,
                                        0.55262089, 0.56155801, 0.56290262,
                                        0.56658284, 0.58501193, 0.59443456,
                                        0.61614971, 0.62661584, 0.63724941,
                                        0.64837412, 0.65777284, 0.67058012,
                                        0.67098019, 0.69891557, 0.70164032,
                                        0.71116325, 0.71254891, 0.74000189,
                                        0.75221912, 0.77941278, 0.81896562,
                                        0.83570443, 0.85189600, 0.85790149,
                                        0.89458735, 0.90024929, 0.91142858,
                                        0.91502854, 0.91550794, 0.92372806,
                                        0.94205279, 0.94315728, 0.94884721,
                                        0.95550522, 0.95849193, 0.95941487,
                                        0.96478918, 0.97027892, 0.97107105,
                                        0.97729255, 0.98646928, 0.99008920,
                                        0.99119437, 0.99424834, 0.99714569,
                                        0.99805292, 0.99895336, 0.99905451,
                                        0.99952729, 0.99961357, 0.99984979,
                                        0.99985388])


class TestTBF(unittest.TestCase):
    """
    Class to test time between failure calculations.
    """

    DATA = [[0, u'A', 50.0, 50.0, 1, 'Event'],
            [1, u'A', 200.0, 200.0, 1, 1],
            [2, u'A', 200, 0.0, 1, 2],
            [3, u'B', 0.0, 50.0, 1, 'Interval Censored'],
            [4, u'B', 50.0, 100.0, 1, 3],
            [5, u'C', 0.0, 200.0, 1, 'Left Censored'],
            [6, u'C', 200.0, 0.0, 1, 'Right Censored']]

    @attr(all=True, unit=True)
    def test_exact_failure_times(self):
        """
        Test of the time between failure calculation for exact failure times.
        """

        # Test exact failure time records.
        self.assertEqual(time_between_failures(self.DATA[-1], self.DATA[0]),
                         50.0)

        self.assertEqual(time_between_failures(self.DATA[0], self.DATA[1]),
                         150.0)

    @attr(all=True, unit=True)
    def test_right_censored_times(self):
        """
        Test of the time between failure calculation for right censored failure times.
        """

        # Test right censored records.
        self.assertEqual(time_between_failures(self.DATA[1], self.DATA[2]),
                         np.inf)

        self.assertEqual(time_between_failures(self.DATA[5], self.DATA[6]),
                         np.inf)

    @attr(all=True, unit=True)
    def test_interval_censored_times(self):
        """
        Test of the time between failure calculation for interval censored failure times.
        """

        # Test interval censored records.
        self.assertEqual(time_between_failures(self.DATA[2], self.DATA[3]),
                         25.0)

        self.assertEqual(time_between_failures(self.DATA[3], self.DATA[4]),
                         50.0)

        self.assertEqual(time_between_failures(self.DATA[4],
                                               self.DATA[5]),
                         100.0)
