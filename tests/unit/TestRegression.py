#!/usr/bin/env python -O
"""
This is the test class for testing regression module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.statistics.TestRegression.py is part of The RTK Project
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

from analyses.statistics.Regression import adjusted_rank, bernard_ranks, \
                                           regression

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestRegression(unittest.TestCase):
    """
    Class for testing the Regression data model class.
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

    # Data set of 100 normally distributed points a mean of 100.0 and a
    # variance of 10.0
    NORM_TEST = [
        [95.370, 95.370, 1, 1, 95.370], [0.0, 114.011, 1, 1, 114.011], [
            0.0, 113.246, 1, 1, 113.246
        ], [0.0, 109.167, 1, 1, 109.167], [0.0, 104.227, 1, 1, 104.227],
        [107.109, 107.109, 1, 1, 107.109], [0.0, 117.43215, 1, 1, 117.43215], [
            0.0, 94.785, 1, 1, 94.785
        ], [0.0, 83.56718, 1, 1, 83.56718], [0.0, 103.501, 1, 1, 103.501],
        [89.931, 89.931, 1, 1,
         89.931], [0.0, 120.455, 1, 1, 120.455], [0.0, 97.081, 1, 1, 97.081], [
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
         ], [91.664, 91.664, 1, 1, 91.664], [0.0, 106.149, 1, 1, 106.149], [
             0.0, 104.320, 1, 1, 104.320
         ], [0.0, 115.681, 1, 1, 115.681], [0.0, 95.920, 1, 1, 95.920]
    ]

    # Data is the same as that used in the ReliaSoft wiki examples.
    # The table can be found at the following URL, for example.
    # http://reliawiki.org/index.php/The_Weibull_Distribution#Rank_Regression_on_Y
    # eta = 76.318, beta = 1.4301, and rho = 0.9956 when fit to the WEI.
    WEI_TEST = np.array([[0.0, 16.0, 1, 1, 16.0], [0.0, 34.0, 1, 1, 34.0],
                         [0.0, 53.0, 1, 1, 53.0], [0.0, 75.0, 1, 1, 75.0],
                         [0.0, 93.0, 1, 1, 93.0], [0.0, 120.0, 1, 1, 120.0]])

    @attr(all=True, unit=True)
    def test01_adjusted_rank_exact_data(self):
        """
        (TestRegression) adjusted_rank should return a numpy matrix of integers on success with exact data
        """

        _data = np.array([[0.0, 10.0, 1, 1], [0.0, 30.0, 1, 1], [
            0.0, 45.0, 1, 1
        ], [0.0, 49.0, 1, 1], [0.0, 82.0, 1, 1], [0.0, 90.0, 1, 1],
                          [0.0, 96.0, 1, 1], [0.0, 100.0, 1, 1]])

        _adj_rank = adjusted_rank(_data)
        self.assertTrue(np.array_equal(_adj_rank, [1, 2, 3, 4, 5, 6, 7, 8]))

    @attr(all=True, unit=True)
    def test01a_adjusted_rank_suspended_data(self):
        """
        (TestRegression) adjusted_rank should return a numpy matrix of floats on success with suspended data
        """

        _data = np.array([[0.0, 10.0, 1, 2], [0.0, 30.0, 1, 1], [
            0.0, 45.0, 1, 3
        ], [0.0, 49.0, 1, 1], [0.0, 82.0, 1, 1], [0.0, 90.0, 1, 1],
                          [0.0, 96.0, 1, 1], [0.0, 100.0, 1, 2]])

        _adj_rank = adjusted_rank(_data)
        self.assertTrue(
            np.array_equal(_adj_rank,
                           [-1, 1.125, -1, 2.4375, 3.75, 5.0625, 6.375, -1]))

    @attr(all=True, unit=True)
    def test02_bernards_rank_exact_data(self):
        """
        (TestRegression) bernard_ranks should return a numpy matrix of floats on success with exact data
        """

        _data = np.array([[0.0, 10.0, 1, 1], [0.0, 30.0, 1, 1], [
            0.0, 45.0, 1, 1
        ], [0.0, 49.0, 1, 1], [0.0, 82.0, 1, 1], [0.0, 90.0, 1, 1],
                          [0.0, 96.0, 1, 1], [0.0, 100.0, 1, 1]])

        _bernards = bernard_ranks(_data)
        self.assertTrue(
            np.array_equal(_bernards, [
                0.083333333333333329, 0.20238095238095236, 0.32142857142857145,
                0.44047619047619047, 0.55952380952380953, 0.6785714285714286,
                0.79761904761904756, 0.91666666666666663
            ]))

    @attr(all=True, unit=True)
    def test02a_bernards_rank_right_censored(self):
        """
        (TestRegression) bernard_ranks should return a numpy matrix of floats on success with right censored data
        """

        _data = np.array([[0.0, 10.0, 1, 2], [0.0, 30.0, 1, 1], [
            0.0, 45.0, 1, 3
        ], [0.0, 49.0, 1, 1], [0.0, 82.0, 1, 1], [0.0, 90.0, 1, 1],
                          [0.0, 96.0, 1, 1], [0.0, 100.0, 1, 2]])

        _bernards = bernard_ranks(_data)
        np.testing.assert_array_almost_equal(_bernards, [
            np.nan, 0.202381, np.nan, 0.440476, 0.559524, 0.678571, 0.797619,
            np.nan
        ])

    @attr(all=True, unit=True)
    def test02b_bernards_rank_interval_censored(self):
        """
        (TestRegression) bernard_ranks should return a numpy matrix of floats on success with interval censored data
        """

        _data = np.array([[0.0, 100.0, 7, 3], [100.0, 200.0, 5, 3],
                          [200.0, 300.0, 3, 3], [300.0, 400.0, 2, 3],
                          [400.0, 500.0, 1, 3], [500.0, 600.0, 2, 3]])

        _bernards = bernard_ranks(_data, grouped=True)
        np.testing.assert_array_equal(_bernards, [
            0.32843137254901966, 0.57352941176470584, 0.72058823529411764,
            0.81862745098039214, 0.86764705882352944, 0.96568627450980393
        ])

    @attr(all=True, unit=True)
    def test03_exponential_regression_fit_exact(self):
        """
        (TestRegression) regression should return a numpy array of rank regression on y (RRY) fit of the exponential parameters using exact failure times
        """

        _fit = regression(self.EXP_TEST, 0.0, 10000000.0)

        # Test the parameter estimation.
        self.assertAlmostEqual(_fit[0][0], 0.0108368)

        # Test the variance estimation.
        self.assertAlmostEqual(_fit[1][0], 2.8792752e-08)

        # Test the correlation coefficient.
        self.assertAlmostEqual(_fit[3], -0.9881986)

        return False

    @attr(all=True, unit=True)
    def test04_lognormal_regression_fit(self):
        """
        (TestRegression) regression should return a numpy array of rank regression on y (RRY) fit of the lognormal parameters
        """

        _fit = regression(self.LOGN_TEST, 0.0, 10000000.0, dist='lognormal')

        # Check the mean.
        self.assertAlmostEqual(
            _fit[0][0],
            3.51585540,
            msg='FAIL: Lognormal scale parameter (mu) test using RRY.')

        # Check the standard deviation.
        self.assertAlmostEqual(
            _fit[0][1],
            0.9693628,
            msg='FAIL: Lognormal shape parameter (sigma) test using RRY.')

        # Check the variance on the mean.
        self.assertAlmostEqual(
            _fit[1][0],
            0.004542255,
            msg='FAIL: Lognormal scale paramter (mu) variance test using RRY.')

        # Check the variance on the standard deviation.
        self.assertAlmostEqual(
            _fit[1][2],
            0.05942344,
            msg=
            'FAIL: Lognormal shape parameter (sigma) variance test using RRY.')

        # Check the covariance of the mean and standard deviation.
        self.assertAlmostEqual(
            _fit[1][1],
            -0.0159699,
            msg='FAIL: Lognormal covariance test using RRY.')

        # Check the correlation coefficient.
        self.assertAlmostEqual(
            _fit[3],
            0.9753344,
            msg='FAIL: Lognormal correlation coefficient test using RRY.')

    @attr(all=True, unit=True)
    def test05_gaussian_regression_fit(self):
        """
        (TestRegression) regression should return a numpy array of rank regression on y (RRY) fit of the Gaussian parameters
        """

        _fit = regression(self.NORM_TEST, 0.0, 10000000.0, dist='normal')

        # Check the mean.
        self.assertAlmostEqual(
            _fit[0][0],
            100.5283533,
            msg='FAIL: Gaussian scale parameter (mu) test using RRY.')

        # Check the standard deviation.
        self.assertAlmostEqual(
            _fit[0][1],
            10.8427617,
            msg='FAIL: Gaussian shape parameter (sigma) test using RRY.')

        # Check the variance on the mean.
        self.assertAlmostEqual(
            _fit[1][0],
            0.0000011825642,
            msg='FAIL: Gaussian scale parameter (mu) variance test using RRY.')

        # Check the variance on the standard deviation.
        self.assertAlmostEqual(
            _fit[1][2],
            0.0120824,
            msg=
            'FAIL: Gaussian shape parameeter (sigma) variance test using RRY.')

        # Check the covariance of the mean and standard deviation.
        self.assertAlmostEqual(
            _fit[1][1],
            -0.0001189,
            msg='FAIL: Gaussian covariance test using RRY.')

        # Check the correlation coefficient.
        self.assertAlmostEqual(
            _fit[3],
            0.9932564,
            msg='FAIL: Gaussian correlation coefficient test using RRY.')

    @attr(all=True, unit=True)
    def test06_weibull_regression_fit(self):
        """
        (TestRegression) regression should return a numpy array of rank regression on y (RRY) fit of the Weibull parameters
        """

        _fit = regression(self.WEI_TEST, 0.0, 10000000.0, dist='weibull')

        # Check the scale parameter (eta).
        self.assertAlmostEqual(
            _fit[0][0],
            76.3454154,
            msg='FAIL: Weibull scale parameter (eta) test using RRY.')

        # Check the shape parameter (beta).
        self.assertAlmostEqual(
            _fit[0][1],
            1.4269671,
            msg='FAIL: Weibull shape parameter (beta) test using RRY.')

        # Check the variance on the scale parameter (eta).
        self.assertAlmostEqual(
            _fit[1][0],
            0.0045293,
            msg='FAIL: Weibull scale parameter (eta) variance test using RRY.')

        # Check the variance on the shape parameter (beta).
        self.assertAlmostEqual(
            _fit[1][2],
            0.0739709,
            msg='FAIL: Weibull shape parameter (beta) variance test using RRY.'
        )

        # Check the covariance of eta and beta.
        self.assertAlmostEqual(
            _fit[1][1],
            -0.0180467,
            msg='FAIL: Weibull covariance test using RRY.')

        # Check the correlation coefficient.
        self.assertAlmostEqual(
            _fit[3],
            0.9955808,
            msg='FAIL: Weibull correlation coefficient test using RRY.')
