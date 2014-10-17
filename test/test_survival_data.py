#!/usr/bin/env python -O
"""
This is the test class for testing survival analysis algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       test_survival_data.py is part of The RTK Project
#
# All rights reserved.

import unittest

import os
import sys
sys.path.insert(0, os.path.abspath(".."))

import numpy as np

from rtk.calculations import beta_bounds
from rtk._calculations_.survival import *


class TestMedianRanks(unittest.TestCase):
    """
    Class for testing functions used to calculate median ranks.
    """

    DATA_EXACT = np.array([[0.0, 10.0, 1, 1], [0.0, 30.0, 1, 1],
                           [0.0, 45.0, 1, 1], [0.0, 49.0, 1, 1],
                           [0.0, 82.0, 1, 1], [0.0, 90.0, 1, 1],
                           [0.0, 96.0, 1, 1], [0.0, 100.0, 1, 1]])

    DATA_SUSPENSIONS = np.array([[0.0, 10.0, 1, 2], [0.0, 30.0, 1, 1],
                                 [0.0, 45.0, 1, 3], [0.0, 49.0, 1, 1],
                                 [0.0, 82.0, 1, 1], [0.0, 90.0, 1, 1],
                                 [0.0, 96.0, 1, 1], [0.0, 100.0, 1, 2]])

    DATA_INTERVAL = np.array([[0.0, 100.0, 7, 3], [100.0, 200.0, 5, 3],
                              [200.0, 300.0, 3, 3], [300.0, 400.0, 2, 3],
                              [400.0, 500.0, 1, 3], [500.0, 600.0, 2, 3]])

    def test_adjusted_rank(self):
        """
        Test of the adjust rank function.
        """

        # Test with exact data.
        np.testing.assert_equal(adjusted_rank(self.DATA_EXACT),
                                [1, 2, 3, 4, 5, 6, 7, 8])

        # Test with suspended data.
        np.testing.assert_equal(adjusted_rank(self.DATA_SUSPENSIONS),
                                [-1, 1.125, -1, 2.4375,
                                 3.75, 5.0625, 6.375, -1])

    def test_bernards_approximation(self):
        """
        Test of Bernard's approximation function.
        """

        # Test with exact data.  Fails as not equal, why?
        np.testing.assert_equal(bernard_ranks(self.DATA_EXACT),
                                [0.083333333333333329, 0.20238095238095236,
                                 0.32142857142857145, 0.44047619047619047,
                                 0.55952380952380953, 0.6785714285714286,
                                 0.79761904761904756, 0.91666666666666663])

        # Test with right censored data.
        np.testing.assert_equal(bernard_ranks(self.DATA_SUSPENSIONS),
                                [np.nan, 0.098214285714285698, np.nan,
                                 0.2544642857142857, 0.4107142857142857,
                                 0.5669642857142857, 0.7232142857142857,
                                 np.nan])

        # Test with interval censored data.
        np.testing.assert_equal(bernard_ranks(self.DATA_INTERVAL,
                                              grouped=True),
                                [0.32843137254901966, 0.57352941176470584,
                                 0.72058823529411764, 0.81862745098039214,
                                 0.86764705882352944, 0.96568627450980393])


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

    def test_exact_failure_times(self):
        """
        Test of the time between failure calculation for exact failure times.
        """

        # Test exact failure time records.
        self.assertEqual(time_between_failures(self.DATA[-1],
                                               self.DATA[0]),
                         50.0)

        self.assertEqual(time_between_failures(self.DATA[0],
                                               self.DATA[1]),
                         150.0)

    def test_right_censored_times(self):
        """
        Test of the time between failure calculation for right censored failure times.
        """

        # Test right censored records.
        self.assertEqual(time_between_failures(self.DATA[1],
                                               self.DATA[2]),
                         np.inf)

        self.assertEqual(time_between_failures(self.DATA[5],
                                               self.DATA[6]),
                         np.inf)

    def test_interval_censored_times(self):
        """
        Test of the time between failure calculation for interval censored failure times.
        """

        # Test interval censored records.
        self.assertEqual(time_between_failures(self.DATA[2],
                                               self.DATA[3]),
                         25.0)

        self.assertEqual(time_between_failures(self.DATA[3],
                                               self.DATA[4]),
                         50.0)

        self.assertEqual(time_between_failures(self.DATA[4],
                                               self.DATA[5]),
                         100.0)

class TestExponential(unittest.TestCase):
    """
    Class to test exponential distribution algorithms.
    """

    # TODO: Add test for generating a theoretical exp(theta)

    # Data is the same as that used in the ReliaSoft wiki examples.
    # The table can be found at the following URL, for example.
    # http://reliawiki.org/index.php/The_Lognormal_Distribution#Rank_Regression_on_Y
    # lambda = 0.02711 and rho = -0.9679 when fit to the EXP.
    DATA = np.array([['', 0.0, 5.0, 0, 1, 1], ['', 0.0, 10.0, 0, 1, 1],
                     ['', 0.0, 15.0, 0, 1, 1], ['', 0.0, 20.0, 0, 1, 1],
                     ['', 0.0, 25.0, 0, 1, 1], ['', 0.0, 30.0, 0, 1, 1],
                     ['', 0.0, 35.0, 0, 1, 1], ['', 0.0, 40.0, 0, 1, 1],
                     ['', 0.0, 50.0, 0, 1, 1], ['', 0.0, 60.0, 0, 1, 1],
                     ['', 0.0, 70.0, 0, 1, 1], ['', 0.0, 80.0, 0, 1, 1],
                     ['', 0.0, 90.0, 0, 1, 1], ['', 0.0, 100.0, 0, 1, 1]])

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
                (u'', 19.664, 19.664, 19.664, 1, 1),  (u'', 96.415, 96.415, 96.415, 1, 1),
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

    def test_exponential_partial_derivs_exact(self):
        """
        Test of the exponential log likelihood partial derivative with exact data only.
        """

        self.assertAlmostEqual(exponential_partial_derivs(1.0, self.LEUK),
                               -177.0)

    def test_exponential_partial_derivs_right(self):
        """
        Test of the exponential log likelihood partial derivative with exact and right censored data.
        """

        self.assertAlmostEqual(exponential_partial_derivs(1.0, self.MICE),
                               -81.0)

    def test_exponential_partial_derivs_interval(self):
        """
        Test of the exponential log likelihood partial derivative with exact, right, and interval censored data.
        """

        # Parameter is 0.0034 for exponential.
        self.assertAlmostEqual(exponential_partial_derivs(0.0034, self.AIDS),
                               -33687.147058823532)


    def test_exponential_log_pdf(self):
        """
        Test of the exponential log pdf function.
        """

        np.testing.assert_allclose(exponential_log_pdf(np.array(self.DATA[:, 2], dtype=float),
                                                       0.02222222),
                                   [-3.91777369, -4.02888479, -4.13999589, -4.25110699,
                                    -4.36221809, -4.47332919, -4.58444029, -4.69555139,
                                    -4.91777359, -5.13999579, -5.36221799, -5.58444019,
                                    -5.80666239, -6.02888459])

    def test_exponential_mle_fit(self):
        """
        Test of maximum likelihood estimate (MLE) fit of the exponential
        parameters.
        """

        # Check the mean for exact failure time data.
        self.assertAlmostEqual(parametric_fit(self.EXP_TEST, 0.0,
                                              10000000.0, 1)[0][0],
                               0.01062394396240946)

        # Check the mean for interval-censored failure time data.
        self.assertAlmostEqual(parametric_fit(self.ALPHA, 0.0,
                                              10000000.0, 1)[0][0],
                               0.001584005)

        # Check the variance.
        self.assertAlmostEqual(parametric_fit(self.EXP_TEST, 0.0,
                                              10000000.0, 1)[1][0],
                               1.3219492619921581e-06)

    def test_exponential_regression_fit(self):
        """
        Test of rank regression on y (RRY) fit of the exponential parameters.
        """

        # Test the parameter estimation.
        self.assertAlmostEqual(parametric_fit(self.EXP_TEST, 0.0,
                                              10000000.0, 2)[0][0],
                               0.0108368)

        # Test the variance estimation.
        self.assertAlmostEqual(parametric_fit(self.EXP_TEST, 0.0,
                                              10000000.0, 2)[1][0],
                               2.8792752e-08)

        # Test the correlation coefficient.
        self.assertAlmostEqual(parametric_fit(self.EXP_TEST, 0.0,
                                              10000000.0, 2)[3],
                               -0.9881986,
                               msg='FAIL: Exponential correlation coefficient test using RRY.')

    def test_theoretical_exponential(self):
        """
        Test of the theoretical distribution function for the exponential.
        """

        _para = [0.0106235]
        np.testing.assert_equal(theoretical_distribution(np.array(self.EXP_TEST),
                                                            'exponential', _para)[99],
                                0.9760679054934378)



class TestLogNormal(unittest.TestCase):
    """
    Class for testing lognormal distribution algorithms.
    """

    # TODO: Add test for generating a theoretical lnorm(mu, sigma)

    # Data is the same as that used in the ReliaSoft wiki examples.
    # The table can be found at the following URL, for example.
    # http://reliawiki.org/index.php/The_Lognormal_Distribution#Rank_Regression_on_Y
    # mu = 3.516, sigma = 0.9663, and rho = 0.9754 when fit to the LNORM.
    DATA = np.array([['', 5.0, 5.0, 5.0, 1, 1], ['', 10.0, 10.0, 5.0, 1, 1],
                     ['', 15.0,	15.0, 5.0, 1, 1], ['', 20.0, 20.0, 5.0, 1, 1],
                     ['', 25.0, 25.0, 5.0, 1, 1], ['', 30.0, 30.0, 5.0, 1, 1],
                     ['', 35.0, 35.0, 5.0, 1, 1], ['', 40.0, 40.0, 5.0, 1, 1],
                     ['', 50.0, 50.0, 10.0, 1, 1], ['', 60.0, 60.0, 10.0, 1, 1],
                     ['', 70.0, 70.0, 10.0, 1, 1], ['', 80.0, 80.0, 10.0, 1, 1],
                     ['', 90.0, 90.0, 10.0, 1, 1], ['', 100.0, 100.0, 10.0, 1, 1]])

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

    def test_lognormal_mle_fit(self):
        """
        Test of maximum likelihood estimate (MLE) fit of the lognormal parameters.
        """

        # Check the mean.
        self.assertAlmostEqual(parametric_fit(self.DATA, 0.0,
                                              10000000.0, 1,
                                              dist='lognormal')[0][0],
                               3.5158550,
                               msg='FAIL: Lognormal scale parameter (mu) test using MLE.')

        # Check the standard deviation.
        self.assertAlmostEqual(parametric_fit(self.DATA, 0.0,
                                              10000000.0, 1,
                                              dist='lognormal')[0][1],
                               0.8491917,
                               msg='FAIL: Lognormal shape parameter (sigma) test using MLE.')

    def test_lognormal_regression_fit(self):
        """
        Test of rank regression on y (RRY) fit of the lognormal parameters.
        """

        # Check the mean.
        self.assertAlmostEqual(parametric_fit(self.DATA, 0.0,
                                              10000000.0, 2,
                                              dist='lognormal')[0][0],
                              3.51585540,
                               msg='FAIL: Lognormal scale parameter (mu) test using RRY.')

        # Check the standard deviation.
        self.assertAlmostEqual(parametric_fit(self.DATA, 0.0,
                                              10000000.0, 2,
                                              dist='lognormal')[0][1],
                               0.9693628,
                               msg='FAIL: Lognormal shape parameter (sigma) test using RRY.')

        # Check the variance on the mean.
        self.assertAlmostEqual(parametric_fit(self.DATA, 0.0,
                                              10000000.0, 2,
                                              dist='lognormal')[1][0],
                               0.004542255,
                               msg='FAIL: Lognormal scale paramter (mu) variance test using RRY.')

        # Check the variance on the standard deviation.
        self.assertAlmostEqual(parametric_fit(self.DATA, 0.0,
                                              10000000.0, 2,
                                              dist='lognormal')[1][2],
                               0.05942344,
                               msg='FAIL: Lognormal shape parameter (sigma) variance test using RRY.')

        # Check the covariance of the mean and standard deviation.
        self.assertAlmostEqual(parametric_fit(self.DATA, 0.0,
                                              10000000.0, 2,
                                              dist='lognormal')[1][1],
                               -0.0159699,
                               msg='FAIL: Lognormal covariance test using RRY.')

        # Check the correlation coefficient.
        self.assertAlmostEqual(parametric_fit(self.DATA, 0.0,
                                              10000000.0, 2,
                                              dist='lognormal')[3],
                               0.9753344,
                               msg='FAIL: Lognormal correlation coefficient test using RRY.')

    def test_theoretical_lognormal(self):
        """
        Test of the theoretical distribution function for the lognormal.
        """

        _para = [3.51585540, 0.9693628]
        np.testing.assert_equal(theoretical_distribution(np.array(self.DATA),
                                                         'lognormal', _para)[13],
                                0.86946087881485745)



class TestGaussian(unittest.TestCase):
    """
    Class for testing Gaussian distribution algorithms.
    """

    # TODO: Add test for generating a theoretical norm(mu, sigma)

    # Data is the same as that used in the ReliaSoft wiki examples.
    # The table can be found at the following URL, for example.
    # http://reliawiki.org/index.php/The_Lognormal_Distribution#Rank_Regression_on_Y
    # mu = 45.0000, sigma = 33.5367 and rho = 0.9790 when fit to the GAU.
    DATA = np.array([['', 0.0, 5.0, 0, 1, 1], ['', 0.0, 10.0, 0, 1, 1],
                     ['', 0.0,	15.0, 0, 1, 1], ['', 0.0, 20.0, 0, 1, 1],
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

    def test_gaussian_log_likelihood_exact(self):
        """
        Test of the Gaussian log likelihood partial derivatives with exact data only.
        """

        np.testing.assert_equal(gaussian_partial_derivs([1.0, 1.0], self.LEUK),
                                [177.0, 156.0])

    def test_gaussian_log_likelihood_right(self):
        """
        Test of the Gaussian log likelihood partial derivatives with exact and right censored data.
        """

        np.testing.assert_equal(gaussian_partial_derivs([1.0, 1.0], self.MICE),
                                [31.000000005139885, 26.000000046258979])

    def test_gaussian_log_likelihood_interval(self):
        """
        Test of the Gaussian log likelihood partial derivatives with exact, right, and interval censored data.
        """

        np.testing.assert_equal(gaussian_partial_derivs([1.0, 1.0], self.AIDS),
                                [-2280.5, -2215.5])

    def test_guassian_mle_fit(self):
        """
        Test of maximum likelihood estimate (MLE) fit of the Gaussian parameters.
        """

        # Check the mean.
        self.assertAlmostEqual(parametric_fit(self.NORM_TEST, 0.0,
                                              10000000.0, 1,
                                              dist='normal')[0][0],
                               100.5283533,
                               msg='FAIL: Gaussian scale parameter (mu) test using MLE.')

        # Check the standard deviation.
        self.assertAlmostEqual(parametric_fit(self.NORM_TEST, 0.0,
                                              10000000.0, 1,
                                              dist='normal')[0][1],
                               10.5442140,
                               msg='FAIL: Gaussian shape parameter (sigma) test using MLE.')

    def test_gaussian_regression_fit(self):
        """
        Test of rank regression on y (RRY) fit of the Gaussian parameters.
        """

        # Check the mean.
        self.assertAlmostEqual(parametric_fit(self.NORM_TEST, 0.0,
                                              10000000.0, 2,
                                              dist='normal')[0][0],
                               100.5283533,
                               msg='FAIL: Gaussian scale parameter (mu) test using RRY.')

        # Check the standard deviation.
        self.assertAlmostEqual(parametric_fit(self.NORM_TEST, 0.0,
                                              10000000.0, 2,
                                              dist='normal')[0][1],
                               10.8427617,
                               msg='FAIL: Gaussian shape parameter (sigma) test using RRY.')

        # Check the variance on the mean.
        self.assertAlmostEqual(parametric_fit(self.NORM_TEST, 0.0,
                                              10000000.0, 2,
                                              dist='normal')[1][0],
                               0.0000011825642,
                               msg='FAIL: Gaussian scale parameter (mu) variance test using RRY.')

        # Check the variance on the standard deviation.
        self.assertAlmostEqual(parametric_fit(self.NORM_TEST, 0.0,
                                              10000000.0, 2,
                                              dist='normal')[1][2],
                               0.0120824,
                               msg='FAIL: Gaussian shape parameeter (sigma) variance test using RRY.')

        # Check the covariance of the mean and standard deviation.
        self.assertAlmostEqual(parametric_fit(self.NORM_TEST, 0.0,
                                              10000000.0, 2,
                                              dist='normal')[1][1],
                               -0.0001189,
                               msg='FAIL: Gaussian covariance test using RRY.')

        # Check the correlation coefficient.
        self.assertAlmostEqual(parametric_fit(self.NORM_TEST, 0.0,
                                              10000000.0, 2,
                                              dist='normal')[3],
                               0.9932564,
                               msg='FAIL: Gaussian correlation coefficient test using RRY.')

    def test_theoretical_gaussian(self):
        """
        Test of the theoretical distribution function for the Gaussian.
        """

        _para = [100.5283533, 10.8427617]
        np.testing.assert_equal(theoretical_distribution(np.array(self.NORM_TEST),
                                                         'normal', _para)[99],
                                0.99777169466234183)



class TestWeibull(unittest.TestCase):
    """
    Class for testing Weibull dsitribution algorithms.
    """

    # TODO: Add test for generating a theoretical wei(eta, beta)

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
                (u'', 82.223, 82.223, 0.0, 1, 1),  (u'', 40.360, 40.360, 0.0, 1, 1),
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
                (u'', 19.664, 19.664, 0.0, 1, 1),  (u'', 96.415, 96.415, 0.0, 1, 1),
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
                (u'', 323.763, 323.763, 0.0, 1, 1), (u'', 275.491, 275.491, 0.0, 1,1 ),
                (u'', 49.315, 49.315, 0.0, 1, 1), (u'', 1.585, 1.585, 0.0, 1, 1),
                (u'', 317.922, 317.922, 0.0, 1, 1), (u'', 12.398, 12.398, 0.0, 1, 1),
                (u'', 222.930, 222.930, 0.0, 1, 1), (u'', 6.328, 6.328, 0.0, 1, 1),
                (u'', 143.687, 143.687, 0.0, 1, 1), (u'', 134.763, 134.763, 0.0, 1, 1),
                (u'', 88.862, 88.862, 0.0, 1, 1), (u'', 143.918, 143.918, 0.0, 1, 1)]

    def test_weibull_log_likelihood_exact(self):
        """
        Test of the Weibull log likelihood partial derivatives with exact data only.
        """

        np.testing.assert_equal(weibull_partial_derivs([1.0, 1.0], self.LEUK),
                                [177.0,-450.4866935010138])

    def test_weibull_log_likelihood_right(self):
        """
        Test of the Weibull log likelihood partial derivatives with exact and right censored data.
        """

        np.testing.assert_equal(weibull_partial_derivs([1.0, 1.0], self.MICE),
                                [-19.0, -173.5830426301934])

    def test_weibull_log_likelihood_interval(self):
        """
        Test of the Weibull log likelihood partial derivatives with exact, right, and interval censored data.
        """

        # Paramaters are 0.0025 and 0.8119 for Weibull.
        np.testing.assert_equal(weibull_partial_derivs([1.0, 1.0], self.AIDS),
                                [-14634.5, -83800.438465226223])

    def test_weibull_mle_fit(self):
        """
        Test of maximum likelihood estimate (MLE) fit of the Weibull parameters.
        """

        # Check the scale parameter (eta).
        self.assertAlmostEqual(parametric_fit(self.DATA, 0.0,
                                              10000000.0, 1,
                                              dist='weibull')[0][0],
                               73.5260326,
                               msg='FAIL: Weibull scale parameter (eta) test using MLE.')

        # Check the shape parameter (beta).
        self.assertAlmostEqual(parametric_fit(self.DATA, 0.0,
                                              10000000.0, 1,
                                              dist='weibull')[0][1],
                               1.932677032,
                               msg='FAIL: Weibull shape parameter (beta) test using MLE.')

    def test_weibull_regression_fit(self):
        """
        Test of rank regression on y (RRY) fit of the Weibull parameters.
        """

        # Check the scale parameter (eta).
        self.assertAlmostEqual(parametric_fit(self.DATA, 0.0,
                                              10000000.0, 2,
                                              dist='weibull')[0][0],
                               76.3454154,
                               msg='FAIL: Weibull scale parameter (eta) test using RRY.')

        # Check the shape parameter (beta).
        self.assertAlmostEqual(parametric_fit(self.DATA, 0.0,
                                              10000000.0, 2,
                                              dist='weibull')[0][1],
                               1.4269671,
                               msg='FAIL: Weibull shape parameter (beta) test using RRY.')

        # Check the variance on the scale parameter (eta).
        self.assertAlmostEqual(parametric_fit(self.DATA, 0.0,
                                              10000000.0, 2,
                                              dist='weibull')[1][0],
                               0.0045293,
                               msg='FAIL: Weibull scale parameter (eta) variance test using RRY.')

        # Check the variance on the shape parameter (beta).
        self.assertAlmostEqual(parametric_fit(self.DATA, 0.0,
                                              10000000.0, 2,
                                              dist='weibull')[1][2],
                               0.0739709,
                               msg='FAIL: Weibull shape parameter (beta) variance test using RRY.')

        # Check the covariance of eta and beta.
        self.assertAlmostEqual(parametric_fit(self.DATA, 0.0,
                                              10000000.0, 2,
                                              dist='weibull')[1][1],
                               -0.0180467,
                               msg='FAIL: Weibull covariance test using RRY.')

        # Check the correlation coefficient.
        self.assertAlmostEqual(parametric_fit(self.DATA, 0.0,
                                              10000000.0, 2,
                                              dist='weibull')[3],
                               0.9955808,
                               msg='FAIL: Weibull correlation coefficient test using RRY.')

    def test_theoretical_weibull(self):
        """
        Test of the theoretical distribution function for the Weibull.
        """

        _para = [76.3454154, 1.4269671]
        np.testing.assert_equal(theoretical_distribution(np.array(self.EXP_TEST),
                                                         'weibull', _para)[99],
                               0.99985387582459118)



class TestMCF(unittest.TestCase):
    """
    Class to test mean cumulative function (MCF) algorithms.
    """

    # Data is from Table 16.2 in Meeker and Escobar, "Statistical Methods for
    # Reliability Data"
    SIM_SYS = {1: [5, 8, '12+'], 2: ['16+'], 3: [1, 8, 16, '20+']}
    SIM_SYS_NO_CENSOR = {1: [5, 8], 3: [1, 8, 16]}

    # Data is from Table C.8 in Meeker and Escobar, "Statistical Methods for
    # Reliability Data.
    VALVE_SEATS = {251: ['761+'], 252: ['759+'], 327: [98, '667+'],
                   328: [326, 653, 653, '667+'], 329: ['665+'],
                   330: [84, '667+'], 331: [87, '663+'], 389: [646, '653+'],
                   390: [92, '653+'], 391: ['651+'], 392: [258, 328, 377, 621, '650+'],
                   393: [61, 539, '648+'], 394: [254, 276, 298, 640, '644+'],
                   395: [76, 538, '642+'], 396: [635, '641+'], 397: [349, 404, 561, '649+'],
                   398: ['631+'], 399: ['596+'], 400: [120, 479, '614+'],
                   401: [323, 449, '582+'], 402: [139, 139, '589+'], 403: ['593+'],
                   404: [573, '589+'], 405: [165, 408, 604, '606+'], 406: [249, '594+'],
                   407: [344, 497, '613+'], 408: [265, 586, '595+'],
                   409: [166, 206, 348, '389+'], 410: ['601+'], 411: [410, 581, '601+'],
                   412: ['611+'], 413: ['608+'], 414: ['587+'], 415: [367, '603+'],
                   416: [202, 563, 570, '585+'], 417: ['587+'], 418: ['578+'],
                   419: ['578+'], 420: ['586+'], 421: ['585+'], 422: ['582+']}

    # Data is from Meeker and Escobar.
    GRAMPUS_FAILS = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1]
    GRAMPUS_TIMES = [0.860, 1.258, 1.317, 1.442, 1.897, 2.011, 2.122,
                     2.439, 3.203, 3.298, 3.902, 3.910, 4.000, 4.247,
                     4.411, 4.456, 4.517, 4.899, 4.910, 5.676, 5.755,
                     6.137, 6.221, 6.311, 6.613, 6.975, 7.335, 8.158,
                     8.498, 8.690, 9.042, 9.330, 9.394, 9.426, 9.872,
                     10.191, 11.511, 11.575, 12.1, 12.126, 12.368,
                     12.681, 12.795, 13.399, 13.668, 13.78, 13.877,
                     14.007, 14.028, 14.035, 14.173, 14.173, 14.449,
                     14.587, 14.610, 15.07, 16.0]

    # Data used to test Duane algorithms.
    # See http://www.reliawiki.org/index.php/Duane_Model
    # Data is from least squares example 3.
    DUANE_FAILS = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1, 1]
    DUANE_TIMES = [9.2, 15.8, 36.5, 198.5, 40.0, 410.0, 206.0, 94.0,
                   210.0, 1310.0, 820.0, 850.0, 210.0, 580.0, 580.0,
                   2740.0, 220.0, 670.0, 1300.0, 1600.0, 1300.0,
                   1200.0, 7400.0]

    def setUp(self):
        """
        Method to set up the test fixtures.
        """

        _times = reduce(lambda x, y: x+y, self.SIM_SYS.values())
        self.F1 = set([float(f) for f in _times if isinstance(f, int)])
        self.F1 = sorted(list(self.F1))

        _times = reduce(lambda x, y: x+y, self.SIM_SYS_NO_CENSOR.values())
        self.F2 = set([float(f) for f in _times if isinstance(f, int)])
        self.F2 = sorted(list(self.F2))

        self.no_gui = True

    def test_mcf_build_d_matrix(self):
        """
        Test of the MCF d-matrix function with censoring.
        """

        np.testing.assert_equal(d_matrix(self.SIM_SYS, self.F1),
                                [[0, 0, 1],
                                 [1, 0, 0],
                                 [1, 0, 1],
                                 [0, 0, 1]])

    def test_mcf_build_d_matrix_no_censoring(self):
        """
        Test of the MCF d-matrix function with no censoring.
        """

        np.testing.assert_equal(d_matrix(self.SIM_SYS_NO_CENSOR, self.F2),
                                [[0.,  1.],
                                 [1.,  0.],
                                 [1.,  1.],
                                 [0.,  1.]])

    def test_mcf_build_delta_matrix(self):
        """
        Test of the MCF delta-matrix function with censoring.
        """

        np.testing.assert_equal(delta_matrix(self.SIM_SYS, self.F1),
                                [[1, 1, 1],
                                 [1, 1, 1],
                                 [1, 1, 1],
                                 [0, 1, 1]])

    def test_mcf_build_delta_matrix_no_censoring(self):
        """
        Test of the MCF delta-matrix function with no censored values.
        """

        np.testing.assert_equal(delta_matrix(self.SIM_SYS_NO_CENSOR, self.F2),
                                [[1.,  1.],
                                 [1.,  1.],
                                 [1.,  1.],
                                 [0.,  1.]])

    def test_mcf_variance(self):
        """
        Test of the MCF variance function.
        """

        _times = reduce(lambda x, y: x+y, self.SIM_SYS.values())
        _times = set([float(f) for f in _times if isinstance(f, int)])
        _times = sorted(list(_times))

        _d_matrix = d_matrix(self.SIM_SYS, _times)
        _delta_matrix = delta_matrix(self.SIM_SYS, _times)

        _delta_dot = _delta_matrix.sum(axis=1)
        _d_dot = _d_matrix.sum(axis=1)

        _d_bar = _d_dot / _delta_dot

        np.testing.assert_allclose(mcf_variance(_delta_matrix, _d_matrix,
                                                _delta_dot, _d_bar),
                                   [[0.07407407],
                                    [0.07407407],
                                    [0.07407407],
                                    [0.125]])

    def test_mean_cumulative_function(self):
        """
        Test of the mean cumulative function algorithms.
        """

        np.testing.assert_allclose(mean_cumulative_function(self.SIM_SYS,
                                                            conf=0.90),
                                   [[1.0, 1.0, 0.08701893,  0.33333333,  1.27686145],
                                    [5.0, 1.0, 0.34062477,  0.66666667,  1.30479191],
                                    [8.0, 2.0, 0.95306491,  1.33333333,  1.86532708],
                                    [16.0, 1.0, 1.33499856,  1.83333333,  2.51768893]])

        #np.testing.assert_allclose(mean_cumulative_function(self.VALVE_SEATS),
        #                           [[0.33333333],
        #                            [0.66666667],
        #                            [1.33333333],
        #                            [1.83333333]])

    def test_mil_handbook(self):
        """
        Test of the MIL-HBDK-189 statistic for trend function.
        """

        self.assertEqual(mil_handbook(self.GRAMPUS_TIMES),
                         98.67226125807468)

    def test_laplace(self):
        """
        Test of the Laplace statistic for trend function.
        """

        self.assertEqual(laplace(self.GRAMPUS_TIMES, sum(self.GRAMPUS_FAILS)),
                         0.6232938719595844)

    def test_lewis_robinson(self):
        """
        Test of the Lewis-Robinson statistic for trend function.
        """

        self.assertEqual(lewis_robinson(self.GRAMPUS_TIMES,
                                        sum(self.GRAMPUS_FAILS)),
                         0.63904094805166545)

    #def test_serial_correlation(self):
    #    """
    #    Test of the serial-correlation coefficient function.
    #    """

    #    self.assertEqual(serial_correlation(self.GRAMPUS_TIMES,
    #                                        sum(self.GRAMPUS_FAILS)),
    #                     -0.7)



class TestKaplanMeier(unittest.TestCase):

    # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
    # The following data used to test Kaplan-Meier algorithms                 #
    # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
    # Data is from
    TURBINE_WHEEL = [(0.0, 8.0, u'Interval Censored', 0),
                     (8.0, 12.0, u'Interval Censored', 4),
                     (12.0, 16.0, u'Interval Censored', 2),
                     (16.0, 20.0, u'Interval Censored', 7),
                     (20.0, 24.0, u'Interval Censored', 5),
                     (24.0, 28.0, u'Interval Censored', 9),
                     (28.0, 32.0, u'Interval Censored', 9),
                     (32.0, 36.0, u'Interval Censored', 6),
                     (36.0, 40.0, u'Interval Censored', 22),
                     (40.0, 44.0, u'Interval Censored', 21),
                     (44.0, 44.0, u'Right Censored', 21)]

    TURNBULL = [('', 0.0, 1.0, 0.0, u'Event', 12),
                ('', 0.0, 1.0, 0.0, u'Right Censored', 3),
                ('', 0.0, 1.0, 0.0, u'Left Censored', 2),
                ('', 1.0, 2.0, 0.0, u'Event', 6),
                ('', 1.0, 2.0, 0.0, u'Right Censored', 2),
                ('', 1.0, 2.0, 0.0, u'Left Censored', 4),
                ('', 2.0, 3.0, 0.0, u'Event', 2),
                ('', 2.0, 3.0, 0.0, u'Right Censored', 0),
                ('', 2.0, 3.0, 0.0, u'Left Censored', 2),
                ('', 3.0, 4.0, 0.0, u'Event', 3),
                ('', 3.0, 4.0, 0.0, u'Right Censored', 3),
                ('', 3.0, 4.0, 0.0, u'Left Censored', 5)]

    # Data is from Lee and Wang, page 69, example 4.2.
    REMISSION = [('', 3.0, 3.0, 0.0, u'Event', 1),
                 ('', 4.0, 4.0, 0.0, u'Right Censored', 1),
                 ('', 5.7, 5.7, 0.0, u'Right Censored', 1),
                 ('', 6.5, 6.5, 0.0, u'Event', 1),
                 ('', 6.5, 6.5, 0.0, u'Event', 1),
                 ('', 8.4, 8.4, 0.0, u'Right Censored', 1),
                 ('', 10.0, 10.0, 0.0, u'Event', 1),
                 ('', 10.0, 10.0, 0.0, u'Right Censored', 1),
                 ('', 12.0, 12.0, 0.0, u'Event', 1),
                 ('', 15.0, 15.0, 0.0, u'Event', 1)]

    # This data is the result of the Kaplan-Meier function using the
    # REMISSION data set.
    KM_REMISSION = np.array([[3.0, 0.71671928, 0.9, 0.96722054],
                             [4.0, 0.71671928, 0.9, 0.96722054],
                             [5.7, 0.71671928, 0.9, 0.96722054],
                             [6.5, 0.41797166, 0.64285714, 0.79948773],
                             [8.4, 0.41797166, 0.64285714, 0.79948773],
                             [10.0, 0.25976276, 0.48214286, 0.67381139],
                             [12.0, 0.06504527, 0.24107143, 0.47680147],
                             [15.0, 0.0, 0.0, 0.0]])

    def test_kaplan_meier(self):
        """
        Test of the Kaplan-Meier function.
        """

        np.testing.assert_allclose(kaplan_meier(self.REMISSION,
                                                0.0, 100000.0)[0],
                                   [[3.0, 0.71671928, 0.9, 0.96722054],
                                    [4.0, 0.71671928, 0.9, 0.96722054],
                                    [5.7, 0.71671928, 0.9, 0.96722054],
                                    [6.5, 0.41797166, 0.64285714, 0.79948773],
                                    [8.4, 0.41797166, 0.64285714, 0.79948773],
                                    [10.0, 0.25976276, 0.48214286, 0.67381139],
                                    [12.0, 0.06504527, 0.24107143, 0.47680147],
                                    [15.0, 0.0, 0.0, 0.0]])

        np.testing.assert_allclose(kaplan_meier(self.REMISSION,
                                                0.0, 100000.0)[1],
                                   [1, 4, 5, 7, 9, 10])

    def test_kaplan_meier_mean(self):
        """
        Test of the Kaplan-Meier mean value function.
        """

        _rank = [1, 4, 5, 7, 9, 10]
        np.testing.assert_allclose(kaplan_meier_mean(self.KM_REMISSION,
                                                     _rank, 0.90),
                                   [8.14115869673, 10.0875, 12.0338413033])

    def test_kaplan_meier_hazard(self):
        """
        Test of the Kaplan-Meier hazard rate function.
        """

        np.testing.assert_almost_equal(kaplan_meier_hazard(self.KM_REMISSION),
                                      [[0.11102368, 0.08326776, 0.05843351, 0.13420641, 0.1038502, 0.13479865, 0.22772265, -0.0],
                                       [0.03512017, 0.02634013, 0.0184843, 0.06797427, 0.05259914, 0.07295148, 0.11855517, -0.0],
                                       [0.01110958, 0.00833219, 0.00584715, 0.03442832, 0.02664096, 0.0394805, 0.06172126, -0.0],
                                       [0.33307104, 0.33307104, 0.33307104, 0.87234165, 0.87234165, 1.34798653, 2.73267179,-0.0],
                                       [0.10536052, 0.10536052, 0.10536052, 0.44183276, 0.44183276, 0.72951482, 1.422662, -0.0],
                                       [0.03332874, 0.03332874, 0.03332874, 0.22378409, 0.22378409, 0.39480504, 0.74065508, -0.0],
                                       [-1.09939949, -1.09939949, -1.09939949, -0.13657413, -0.13657413, 0.29861202, 1.00527981, -0.0],
                                       [-2.25036733, -2.25036733, -2.25036733, -0.81682385, -0.81682385, -0.3153756, 0.35252976, -0.0],
                                       [-3.40133509, -3.40133509, -3.40133509, -1.49707356, -1.49707356, -0.9293632, -0.30022024, -0.0]])

    def test_beta_bounds(self):
        """
        Method to test parametric models.
        """

        # Test all positive values using confidence levels expressed as
        # a whole number.
        self.assertEqual(beta_bounds(1.0, 1.0, 1.0, 90.0),
                         (1.0, 1.0, 1.0, 0.0))
        self.assertEqual(beta_bounds(1.0, 2.0, 3.0, 90.0),
                         (1.4517154576828426, 2.0, 2.5482845423171572,
                          0.3333333333333333))

        # Test all positive values using confidence levels expressed as
        # a decimal.
        self.assertEqual(beta_bounds(1.0, 1.0, 1.0, 0.90),
                         (1.0, 1.0, 1.0, 0.0))
        self.assertEqual(beta_bounds(1.0, 2.0, 3.0, 0.90),
                         (1.4517154576828426, 2.0, 2.5482845423171572,
                          0.3333333333333333))

        # Test all negative values using confidence levels expressed as
        # a whole number.
        self.assertEqual(beta_bounds(-1.0, -1.0, -1.0, 0.90),
                         (-1.0, -1.0, -1.0, 0.0))

        # This test will raise an error indicating the confidence level is
        # outside the bounds of [0, 1],
        #if not self.no_gui:
        #    self.assertEqual(beta_bounds(1.0, 1.0, 1.0, -90.0),
        #                     (1.0, 1.0, 1.0, 0.0))


if __name__ == '__main__':
    unittest.main()
