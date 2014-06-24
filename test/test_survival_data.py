#!/usr/bin/env python
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
import numpy as np

import os
import sys
sys.path.insert(0, os.path.abspath(".."))
from rpy2 import robjects
from rpy2.robjects import r as R
from rtk.calculations import beta_bounds, moving_average
from rtk._calculations_.survival import *

class TestSurvivalModels(unittest.TestCase):

    # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
    # The following data is used to test the Mean Cumulative Function         #
    # algorithms                                                              #
    # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
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

    # Data used to test Duane algorithms.
    # See http://www.reliawiki.org/index.php/Duane_Model
    # Data is from least squares example 3.
    DUANE_FAILS = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1, 1]
    DUANE_TIMES = [9.2, 15.8, 36.5, 198.5, 40.0, 410.0, 206.0, 94.0,
                   210.0, 1310.0, 820.0, 850.0, 210.0, 580.0, 580.0,
                   2740.0, 220.0, 670.0, 1300.0, 1600.0, 1300.0,
                   1200.0, 7400.0]

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
                     (44.0, '44.0+', u'Right Censored', 21)]

    TURNBULL = [(0.0, 1.0, u'Event', 12),
                (0.0, 1.0, u'Right Censored', 3),
                (0.0, 1.0, u'Left Censored', 2),
                (1.0, 2.0, u'Event', 6),
                (1.0, 2.0, u'Right Censored', 2),
                (1.0, 2.0, u'Left Censored', 4),
                (2.0, 3.0, u'Event', 2),
                (2.0, 3.0, u'Right Censored', 0),
                (2.0, 3.0, u'Left Censored', 2),
                (3.0, 4.0, u'Event', 3),
                (3.0, 4.0, u'Right Censored', 3),
                (3.0, 4.0, u'Left Censored', 5)]

    # Data is from Lee and Wang, page 69, example 4.2.
    REMISSION = [(3.0, 3.0, u'Event', 1),
                 (4.0, 4.0, u'Right Censored', 1),
                 (5.7, 5.7, u'Right Censored', 1),
                 (6.5, 6.5, u'Event', 1),
                 (6.5, 6.5, u'Event', 1),
                 (8.4, 8.4, u'Right Censored', 1),
                 (10.0, 10.0, u'Event', 1),
                 (10.0, 10.0, u'Right Censored', 1),
                 (12.0, 12.0, u'Event', 1),
                 (15.0, 15.0, u'Event', 1)]

    # This data is the result of the Kaplan-Meier function using the TURNBULL
    # data set.
    KAPLAN_MEIER_TURNBULL = np.matrix([[1.00000000e+00, 4.40000000e+01, 2.03470206e+01, 1.39823815e-01, 7.07052113e-01, 5.37567715e-01, 4.08709687e-01],
                                       [2.00000000e+00, 2.06529794e+01, 9.33488066e+00, 2.43896693e-01, 4.75148308e-01, 2.94594033e-01, 1.82649591e-01],
                                       [3.00000000e+00, 9.31809879e+00, 2.68331943e+00, 3.20762342e-01, 3.93329500e-01, 2.09760215e-01, 1.11863839e-01],
                                       [4.00000000e+00, 6.63477935e+00, 3.63477935e+00, 5.34322843e-01, 2.70292701e-01, 9.48457532e-02, 3.32813904e-02]])

    # Data used to test NHPP power law and NHPP loglinear algorithms.
    # Data is from the book
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

    # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
    # The following data is used to test the parametric model fitting         #
    # function for various distributions.                                     #
    # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
    # Data set of 100 exponentially distributed points with a mean of 100.
    EXP_TEST = [(u'', 48.146, 48.146, 0.0, 1), (u'', 20.564, 20.564, 0.0, 1),
                (u'', 94.072, 94.072, 0.0, 1), (u'', 177.992, 177.992, 0.0, 1),
                (u'', 89.103, 89.103, 0.0, 1), (u'', 350.577, 350.577, 0.0, 1),
                (u'', 82.223, 82.223, 0.0, 1),  (u'', 40.360, 40.360, 0.0, 1),
                (u'', 39.576, 39.576, 0.0, 1), (u'', 53.127, 53.127, 0.0, 1),
                (u'', 159.732, 159.732, 0.0, 1), (u'', 48.398, 48.398, 0.0, 1),
                (u'', 46.984, 46.984, 0.0, 1), (u'', 36.169, 36.169, 0.0, 1),
                (u'', 351.347, 351.347, 0.0, 1), (u'', 18.917, 18.917, 0.0, 1),
                (u'', 101.977, 101.977, 0.0, 1), (u'', 141.988, 141.988, 0.0, 1),
                (u'', 241.044, 241.044, 0.0, 1), (u'', 61.993, 61.993, 0.0, 1),
                (u'', 171.813, 171.813, 0.0, 1), (u'', 78.747, 78.747, 0.0, 1),
                (u'', 54.070, 54.070, 0.0, 1), (u'', 87.229, 87.229, 0.0, 1),
                (u'', 158.980, 158.980, 0.0, 1), (u'', 185.254, 185.254, 0.0, 1),
                (u'', 16.452, 16.452, 0.0, 1), (u'', 120.144, 120.144, 0.0, 1),
                (u'', 294.418, 294.418, 0.0, 1), (u'', 13.640, 13.640, 0.0, 1),
                (u'', 115.532, 115.532, 0.0, 1), (u'', 58.595, 58.595, 0.0, 1),
                (u'', 7.876, 7.876, 0.0, 1), (u'', 10.790, 10.790, 0.0, 1),
                (u'', 67.342, 67.342, 0.0, 1), (u'', 14.848, 14.848, 0.0, 1),
                (u'', 82.160, 82.160, 0.0, 1), (u'', 14.558, 14.558, 0.0, 1),
                (u'', 18.793, 18.793, 0.0, 1), (u'', 69.776, 69.776, 0.0, 1),
                (u'', 65.542, 65.542, 0.0, 1), (u'', 194.039, 194.039, 0.0, 1),
                (u'', 41.559, 41.559, 0.0, 1), (u'', 75.549, 75.549, 0.0, 1),
                (u'', 14.808, 14.808, 0.0, 1), (u'', 184.263, 184.263, 0.0, 1),
                (u'', 2.810, 2.810, 0.0, 1), (u'', 13.095, 13.095, 0.0, 1),
                (u'', 52.885, 52.885, 0.0, 1), (u'', 49.855, 49.855, 0.0, 1),
                (u'', 263.548, 263.548, 0.0, 1), (u'', 4.248, 4.248, 0.0, 1),
                (u'', 66.864, 66.864, 0.0, 1), (u'', 172.663, 172.663, 0.0, 1),
                (u'', 226.918, 226.918, 0.0, 1), (u'', 169.175, 169.175, 0.0, 1),
                (u'', 148.070, 148.070, 0.0, 1), (u'', 3.679, 3.679, 0.0, 1),
                (u'', 28.693, 28.693, 0.0, 1), (u'', 34.931, 34.931, 0.0, 1),
                (u'', 297.467, 297.467, 0.0, 1), (u'', 137.072, 137.072, 0.0, 1),
                (u'', 53.180, 53.180, 0.0, 1), (u'', 49.760, 49.760, 0.0, 1),
                (u'', 19.664, 19.664, 0.0, 1),  (u'', 96.415, 96.415, 0.0, 1),
                (u'', 14.003, 14.003, 0.0, 1), (u'', 17.743, 17.743, 0.0, 1),
                (u'', 212.279, 212.279, 0.0, 1), (u'', 38.951, 38.951, 0.0, 1),
                (u'', 74.057, 74.057, 0.0, 1), (u'', 86.769, 86.769, 0.0, 1),
                (u'', 37.765, 37.765, 0.0, 1), (u'', 5.566, 5.566, 0.0, 1),
                (u'', 71.048, 71.048, 0.0, 1), (u'', 5.137, 5.137, 0.0, 1),
                (u'', 35.461, 35.461, 0.0, 1), (u'', 121.963, 121.963, 0.0, 1),
                (u'', 42.486, 42.486, 0.0, 1), (u'', 52.315, 52.315, 0.0, 1),
                (u'', 77.095, 77.095, 0.0, 1), (u'', 14.259, 14.259, 0.0, 1),
                (u'', 111.147, 111.147, 0.0, 1), (u'', 49.364, 49.364, 0.0, 1),
                (u'', 1.978, 1.978, 0.0, 1), (u'', 163.827, 163.827, 0.0, 1),
                (u'', 66.690, 66.690, 0.0, 1), (u'', 80.172, 80.172, 0.0, 1),
                (u'', 323.763, 323.763, 0.0, 1), (u'', 275.491, 275.491, 0.0, 1),
                (u'', 49.315, 49.315, 0.0, 1), (u'', 1.585, 1.585, 0.0, 1),
                (u'', 317.922, 317.922, 0.0, 1), (u'', 12.398, 12.398, 0.0, 1),
                (u'', 222.930, 222.930, 0.0, 1), (u'', 6.328, 6.328, 0.0, 1),
                (u'', 143.687, 143.687, 0.0, 1), (u'', 134.763, 134.763, 0.0, 1),
                (u'', 88.862, 88.862, 0.0, 1), (u'', 143.918, 143.918, 0.0, 1)]

    # Data set of 100 normally distributed points a mean of 100.0 and a variance
    # of 10.0
    NORM_TEST = [(u'', 95.370, 95.370, 0.0, 1), (u'', 0.0, 114.011, 0.0, 1),
                 (u'', 0.0, 113.246, 0.0, 1), (u'', 0.0, 109.167, 0.0, 1),
                 (u'', 0.0, 104.227, 0.0, 1), (u'', 107.109, 107.109, 0.0, 1),
                 (u'', 0.0, 117.43215, 0.0, 1), (u'', 0.0, 94.785, 0.0, 1),
                 (u'', 0.0, 83.56718, 0.0, 1), (u'', 0.0, 103.501, 0.0, 1),
                 (u'', 89.931, 89.931, 0.0, 1), (u'', 0.0, 120.455, 0.0, 1),
                 (u'', 0.0, 97.081, 0.0, 1), (u'', 0.0, 96.813, 0.0, 1),
                 (u'', 0.0, 97.571, 0.0, 1), (u'', 106.757, 106.757, 0.0, 1),
                 (u'', 0.0, 99.335, 0.0, 1), (u'', 0.0, 104.538, 0.0, 1),
                 (u'', 0.0, 102.028, 0.0, 1), (u'', 0.0, 90.032, 0.0, 1),
                 (u'', 77.542, 77.542, 0.0, 1), (u'', 0.0, 102.761, 0.0, 1),
                 (u'', 0.0, 82.485, 0.0, 1), (u'', 0.0, 77.743, 0.0, 1),
                 (u'', 0.0, 109.974, 0.0, 1), (u'', 94.851, 94.851, 0.0, 1),
                 (u'', 0.0, 89.771, 0.0, 1), (u'', 0.0, 98.193, 0.0, 1),
                 (u'', 0.0, 102.165, 0.0, 1), (u'', 0.0, 96.783, 0.0, 1),
                 (u'', 108.865, 108.865, 0.0, 1), (u'', 0.0, 120.462, 0.0, 1),
                 (u'', 0.0, 111.592, 0.0, 1), (u'', 0.0, 106.148, 0.0, 1),
                 (u'', 0.0, 102.946, 0.0, 1), (u'', 111.290, 111.290, 0.0, 1),
                 (u'', 0.0, 106.002, 0.0, 1), (u'', 0.0, 114.617, 0.0, 1),
                 (u'', 0.0, 88.229, 0.0, 1), (u'', 0.0, 131.364, 0.0, 1),
                 (u'', 86.855, 86.855, 0.0, 1), (u'', 0.0, 109.927, 0.0, 1),
                 (u'', 0.0, 75.116, 0.0, 1), (u'', 0.0, 100.465, 0.0, 1),
                 (u'', 0.0, 97.783, 0.0, 1), (u'', 108.169, 108.169, 0.0, 1),
                 (u'', 0.0, 98.851, 0.0, 1), (u'', 0.0, 99.310, 0.0, 1),
                 (u'', 0.0, 94.588, 0.0, 1), (u'', 0.0, 98.123, 0.0, 1),
                 (u'', 115.666, 115.666, 0.0, 1), (u'', 0.0, 104.491, 0.0, 1),
                 (u'', 0.0, 93.490, 0.0, 1), (u'', 0.0, 111.794, 0.0, 1),
                 (u'', 0.0, 114.320, 0.0, 1), (u'', 106.938, 106.938, 0.0, 1),
                 (u'', 0.0, 106.450, 0.0, 1), (u'', 0.0, 103.105, 0.0, 1),
                 (u'', 0.0, 107.781, 0.0, 1), (u'', 0.0, 120.846, 0.0, 1),
                 (u'', 100.102, 100.102, 0.0, 1), (u'', 0.0, 92.930, 0.0, 1),
                 (u'', 0.0, 101.246, 0.0, 1), (u'', 0.0, 69.517, 0.0, 1),
                 (u'', 0.0, 106.276, 0.0, 1), (u'', 99.046, 99.046, 0.0, 1),
                 (u'', 0.0, 101.300, 0.0, 1), (u'', 0.0, 98.588, 0.0, 1),
                 (u'', 0.0, 110.022, 0.0, 1), (u'', 0.0, 91.255, 0.0, 1),
                 (u'', 106.687, 106.687, 0.0, 1), (u'', 0.0, 102.443, 0.0, 1),
                 (u'', 0.0, 100.342, 0.0, 1), (u'', 0.0, 96.635, 0.0, 1),
                 (u'', 0.0, 80.909, 0.0, 1), (u'', 111.080, 111.080, 0.0, 1),
                 (u'', 0.0, 107.005, 0.0, 1), (u'', 0.0, 103.043, 0.0, 1),
                 (u'', 0.0, 92.660, 0.0, 1), (u'', 0.0, 81.526, 0.0, 1),
                 (u'', 94.497, 94.497, 0.0, 1), (u'', 0.0, 88.791, 0.0, 1),
                 (u'', 0.0, 97.913, 0.0, 1), (u'', 0.0, 96.120, 0.0, 1),
                 (u'', 0.0, 101.234, 0.0, 1), (u'', 95.132, 95.132, 0.0, 1),
                 (u'', 0.0, 93.939, 0.0, 1), (u'', 0.0, 92.302, 0.0, 1),
                 (u'', 0.0, 96.536, 0.0, 1), (u'', 0.0, 110.747, 0.0, 1),
                 (u'', 99.888, 99.888, 0.0, 1), (u'', 0.0, 92.780, 0.0, 1),
                 (u'', 0.0, 107.678, 0.0, 1), (u'', 0.0, 96.187, 0.0, 1),
                 (u'', 0.0, 87.938, 0.0, 1), (u'', 91.664, 91.664, 0.0, 1),
                 (u'', 0.0, 106.149, 0.0, 1), (u'', 0.0, 104.320, 0.0, 1),
                 (u'', 0.0, 115.681, 0.0, 1), (u'', 0.0, 95.920, 0.0, 1)]

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

        np.testing.assert_allclose(mean_cumulative_function(self.SIM_SYS, conf=0.90),
                                   [[0.08701893,  0.33333333,  1.27686145],
                                    [0.34062477,  0.66666667,  1.30479191],
                                    [0.95306491,  1.33333333,  1.86532708],
                                    [1.33499856,  1.83333333,  2.51768893]])

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

    def test_kaplan_meier(self):
        """
        Test of the Kaplan-Meier function.
        """

        np.testing.assert_allclose(kaplan_meier(self.TURNBULL, 0.0),
                                   [[1.00000000e+00, 4.40000000e+01,
                                     2.03470206e+01, 1.39823815e-01,
                                     4.08709687e-01, 5.37567715e-01,
                                     7.07052113e-01],
                                    [2.00000000e+00, 2.06529794e+01,
                                     9.33488066e+00, 2.43896693e-01,
                                     1.82649591e-01, 2.94594033e-01,
                                     4.75148308e-01],
                                    [3.00000000e+00, 9.31809879e+00,
                                     2.68331943e+00, 3.20762342e-01,
                                     1.11863839e-01, 2.09760215e-01,
                                     3.93329500e-01],
                                    [4.00000000e+00, 6.63477935e+00,
                                     3.63477935e+00, 5.34322843e-01,
                                     3.32813904e-02, 9.48457532e-02,
                                     2.70292701e-01]])

        #np.testing.assert_allclose(kaplan_meier(self.REMISSION, 0.0),
        #                           [[3.0, 11.0, 1.10000006, 0.10050378, 1.0, 0.89999999, 0.73908354],
        #                            [4.0, 9.89999994, 0.0, 0.10050378, 1.0, 0.89999999, 0.73908354],
        #                            [5.7, 8.89999994, 0.0, 0.10050378, 1.0, 0.89999999, 0.73908354],
        #                            [6.5, 7.89999994, 2.25714278, 0.24644253, 1.0, 0.64285715, 0.39659042],
        #                            [8.4, 5.64285717, 0.0, 0.24644253, 1.0, 0.64285715, 0.39659042],
        #                            [10.0, 4.64285717, 1.16071465, 0.36404508, 0.98412764, 0.48214281, 0.23621091],
        #                            [12.0, 2.48214252, 1.24107126, 0.73171482, 1.0, 0.24107141, 0.0574525],
        #                            [15.0, 1.24107126, 1.24107126, inf, nan, 0.0, nan]])

    def test_kaplan_meier_mean(self):
        """
        Test of the Kaplan-Meier mean value function.
        """

        np.testing.assert_allclose(kaplan_meier_mean(self.KAPLAN_MEIER_TURNBULL, 0.90),
                                   [[44.185608360483513, 44.294594033,
                                     44.403579705516492,
                                     0.007232137023267089],
                                    [44.349687582776561, 44.504354248000006,
                                     44.659020913223451,
                                     0.014565361656074794],
                                    [44.422256662888984, 44.5992000012,
                                     44.776143339511023,
                                     0.019063220106112447]])

    def test_kaplan_meier_hazard(self):
        """
        Test of the Kaplan-Meier hazard rate function.
        """

        np.testing.assert_allclose(kaplan_meier_hazard(self.KAPLAN_MEIER_TURNBULL),
                                   [[0.34665091, 0.62070055, 0.89475019,
                                     0.34665091, 0.62070055, 0.89475019,
                                     -1.05943704, -0.47690653, -0.11121072],
                                    [0.37206415, 0.61107851, 0.85009288,
                                     0.7441283, 1.22215703, 1.70018576,
                                     -0.29554182, 0.20061735, 0.53073752],
                                    [0.31103587, 0.52059674, 0.73015762,
                                     0.9331076, 1.56179023, 2.19047287,
                                     -0.06923476, 0.44583275, 0.78411744],
                                    [0.32706246, 0.58887584, 0.85068922,
                                     1.30824983, 2.35550336, 3.40275689,
                                     0.26869024, 0.85675444, 1.22458595]])

    def test_exponential_mle_fit(self):
        """
        Test of the parametric function fitting to the exponential using MLE.
        """

        self.assertAlmostEqual(parametric_fit(self.EXP_TEST, 0.0,
                                              10000000.0, 1)[0][0],
                               0.0106235)

    def test_exponential_regression_fit(self):
        """
        Test of the parametric function fitting to the exponential using
        regression.
        """

        self.assertAlmostEqual(parametric_fit(self.EXP_TEST, 0.0,
                                              10000000.0, 2)[0][0],
                               4.5446869,
                               msg='Exponential rate check failed')

    def test_guassian_mle_fit(self):
        """
        Test of the parametric function fitting to the Gaussian using MLE.
        """

        # Check the mean.
        self.assertAlmostEqual(parametric_fit(self.NORM_TEST, 0.0,
                                              10000000.0, 1,
                                              dist='normal')[0][0],
                               100.5283533,
                               msg='Gaussian mean check failed.')

        # Check the variance.
        self.assertAlmostEqual(parametric_fit(self.NORM_TEST, 0.0,
                                              10000000.0, 1,
                                              dist='normal')[0][1],
                               10.5442140,
                               msg='Gaussian variance check failed.')

    def test_theoretical_exponential(self):
        """
        Test of the theoretical distribution function for the exponential.
        """

        _para = R.list(rate=0.01)
        np.testing.assert_allclose(theoretical_distribution(self.EXP_TEST,
                                                            'exp', _para),
                                   [0.00000000, 0.00000000, 0.00000000,
                                    0.00000000, 0.00000000, 0.00000000,
                                    0.00000000, 0.00000000, 0.00000000,
                                    0.00000000, 0.00000000, 0.00000000,
                                    0.00000000, 0.00000000, 0.00000000,
                                    0.00000000, 0.00000000, 0.00000000,
                                    0.00000000, 0.02939965, 0.08222443,
                                    0.13217424, 0.17940553, 0.22406627,
                                    0.26629635, 0.30622807, 0.34398651,
                                    0.37968995, 0.41345023, 0.44537312,
                                    0.47555861, 0.50410126, 0.53109048,
                                    0.55661081, 0.58074220, 0.60356025,
                                    0.62513643, 0.64553832, 0.66482985,
                                    0.68307144, 0.70032023, 0.71663026,
                                    0.73205261, 0.74663561, 0.76042493,
                                    0.77346377, 0.78579297, 0.79745116,
                                    0.80847485, 0.81889858, 0.82875500,
                                    0.83807498, 0.84688773, 0.85522084,
                                    0.86310043, 0.87055117, 0.87759640,
                                    0.88425820, 0.89055743, 0.89651383,
                                    0.90214605, 0.90747174, 0.91250757,
                                    0.91726934, 0.92177194, 0.92602949,
                                    0.93005533, 0.93386205, 0.93746160,
                                    0.94086525, 0.94408365, 0.94712689,
                                    0.95000450, 0.95272550, 0.95529840,
                                    0.95773128, 0.96003175, 0.96220702,
                                    0.96426390, 0.96620883, 0.96804791,
                                    0.96978690, 0.97143124, 0.97298609,
                                    0.97445632, 0.97584653, 0.97716108,
                                    0.97840408, 0.97957944, 0.98069082,
                                    0.98174172, 0.98273543, 0.98367505,
                                    0.98456353, 0.98540366, 0.98619806,
                                    0.98694923, 0.98765952, 0.98833115,
                                    0.98896622, 0.98956673])

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
        if not self.no_gui:
            self.assertEqual(beta_bounds(1.0, 1.0, 1.0, -90.0),
                             (1.0, 1.0, 1.0, 0.0))

if __name__ == '__main__':
    unittest.main()
