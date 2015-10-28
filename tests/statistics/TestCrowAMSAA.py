#!/usr/bin/env python -O
"""
This is the test class for testing Crow-AMSAA model algorithms.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tests.statistics.TestCrowAMSAA.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr
import numpy as np

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from analyses.statistics.CrowAMSAA import *


class TestDuane(unittest.TestCase):
    """
    Class for testing the Crow-AMSAA model functions.
    """

    def setUp(self):
        """
        Setup the test fixture for the Crow-AMSAA model functions.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

    @attr(all=True, unit=True)
    def test_calculate_crow_amsaa_parameters_exact(self):
        """
        (TestCrowAMSAA) calculate_crow_amsaa_parameters should return 0 when encountering no errors using exact failure times
        """

        # See http://reliawiki.org/index.php/Crow-AMSAA_%28NHPP%29 for example
        # data.
        n_failures = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1]
        fail_times = [2.7, 10.3, 12.5, 30.6, 57.0, 61.3, 80.0, 109.5, 125.0,
                      128.6, 143.8, 167.9, 229.2, 296.7, 320.6, 328.2, 366.2,
                      396.7, 421.1, 438.2, 501.2, 620.0]

        _alpha_hat, _beta_hat = calculate_crow_amsaa_parameters(n_failures,
                                                                fail_times)
        self.assertAlmostEqual(_alpha_hat, 0.4239422)
        self.assertAlmostEqual(_beta_hat, 0.6142104)

    @attr(all=True, unit=True)
    def test_calculate_crow_amsaa_parameters_grouped(self):
        """
        (TestCrowAMSAA) calculate_crow_amsaa_parameters should return 0 when encountering no errors using grouped data
        """

        # See http://reliawiki.org/index.php/Crow-AMSAA_%28NHPP%29 for example
        # data.  (Helicopter example data)
        n_failures = [12, 6, 15, 3, 18, 16]
        fail_times = [62.0, 100.0, 187.0, 210.0, 350.0, 500.0]

        _alpha_hat, _beta_hat = calculate_crow_amsaa_parameters(n_failures,
                                                                fail_times,
                                                                grouped=True)
        self.assertAlmostEqual(_alpha_hat, 0.4458543)
        self.assertAlmostEqual(_beta_hat, 0.8136085)

    @attr(all=True, unit=True)
    def test_calculate_crow_amsaa_parameters_no_failures(self):
        """
        (TestCrowAMSAA) calculate_crow_amsaa_parameters should return 1 when passed an empty list of failure counts
        """

        n_failures = []
        fail_times = [62.0, 100.0, 187.0, 210.0, 350.0, 500.0]

        _alpha_hat, _beta_hat = calculate_crow_amsaa_parameters(n_failures,
                                                                fail_times,
                                                                grouped=True)
        self.assertAlmostEqual(_alpha_hat, 0.0)
        self.assertAlmostEqual(_beta_hat, 0.0)

    @attr(all=True, unit=True)
    def test_calculate_crow_amsaa_mean(self):
        """
        (TestCrowAMSAA) calculate_crow_amsaa_mean should return False
        """

        # See http://reliawiki.org/index.php/Crow-AMSAA_%28NHPP%29 for example
        # data.  (Helicopter example data)
        _time = 500.0
        _alpha = 0.44585
        _beta = 0.81361

        _cum_mean, _instantaneous_mean = calculate_crow_amsaa_mean(_time,
                                                                   _alpha,
                                                                   _beta)
        self.assertAlmostEqual(_cum_mean, 7.1428618)
        self.assertAlmostEqual(_instantaneous_mean, 8.7792208)

    @attr(all=True, unit=True)
    def test_calculate_cramer_vonmises(self):
        """
        (TestCrowAMSAA) calculate_cramer_vonmises should return False
        """

        # See MIL-HDBK-189, 5.3.4, Example 1 for example data.
        n_failures = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1]
        fail_times = [2.4, 24.9, 52.5, 53.4, 54.7, 57.2, 118.6, 140.2, 185.0,
                      207.6, 293.9, 322.3, 365.9, 366.8, 544.8, 616.8, 627.5,
                      646.8, 664.0, 738.1, 764.7, 765.1, 779.6, 799.9, 852.9,
                      1116.3, 1161.1, 1257.1, 1276.3, 1308.9, 1340.3, 1437.3,
                      1482.0, 1489.9, 1715.1, 1828.9, 1971.5, 2303.4, 2429.7,
                      2457.4, 2535.2, 2609.9, 2674.2, 2704.8, 2849.6, 2923.5]
        alpha = 0.332
        beta = 0.616

        _Cvm = calculate_cramer_vonmises(n_failures, fail_times, beta, 3000.0,
                                         False)
        self.assertAlmostEqual(_Cvm, 0.04909242)

    @attr(all=True, unit=True)
    def test_cramer_vonmises_critical_value_exact(self):
        """
        (TestCrowAMSAA) cramer_vonmises_critical_value should return the critical value when the degrees of freedom is a key
        """

        _Cvm = cramer_vonmises_critical_value(16, 90.0)
        self.assertAlmostEqual(_Cvm, 0.171)

    @attr(all=True, unit=True)
    def test_cramer_vonmises_critical_value_interpolate_df(self):
        """
        (TestCrowAMSAA) cramer_vonmises_critical_value should return the critical value when the degrees of freedom is not a key
        """

        _Cvm = cramer_vonmises_critical_value(26, 90.0)
        self.assertAlmostEqual(_Cvm, 0.1725)

    @attr(all=True, unit=True)
    def test_cramer_vonmises_critical_value_interpolate_confidence(self):
        """
        (TestCrowAMSAA) cramer_vonmises_critical_value should return the critical value when the confidence level is not a key
        """

        _Cvm = cramer_vonmises_critical_value(16, 75.0)
        self.assertAlmostEqual(_Cvm, 0.127)

    @attr(all=True, unit=True)
    def test_calculate_crow_amsaa_chi_square_exact(self):
        """
        (TestCrowAMSAA) calculate_crow_amsaa_chi_square should return the chi-square test statistic when using exact data
        """

        # See MIL-HDBK-189, 5.3.5.1, Example 2 for example data.
        n_failures = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1]
        fail_times = [2.4, 24.9, 52.5, 53.4, 54.7, 57.2, 118.6, 140.2, 185.0,
                      207.6, 293.9, 322.3, 365.9, 366.8, 544.8, 616.8, 627.5,
                      646.8, 664.0, 738.1, 764.7, 765.1, 779.6, 799.9, 852.9,
                      1116.3, 1161.1, 1257.1, 1276.3, 1308.9, 1340.3, 1437.3,
                      1482.0, 1489.9, 1715.1, 1828.9, 1971.5, 2303.4, 2429.7,
                      2457.4, 2535.2, 2609.9, 2674.2, 2704.8, 2849.6, 2923.5]
        ttt = 3000.0
        beta = 0.616

        _chi_square = calculate_crow_amsaa_chi_square(n_failures, fail_times,
                                                      beta, ttt, False)
        self.assertAlmostEqual(_chi_square, 149.3506494)

    @attr(all=True, unit=True)
    def test_calculate_crow_amsaa_chi_square_grouped(self):
        """
        (TestCrowAMSAA) calculate_crow_amsaa_chi_square should return the chi-square test statistic when using grouped data
        """

        # See MIL-HDBK-189, 5.3.5.3, Example 3 for example data.
        n_failures = [12, 6, 7, 5, 4, 3, 1, 4, 4]
        fail_times = [330.0, 660.0, 990.0, 1320.0, 1650.0, 1980.0, 2310.0,
                      2640.0, 3000.0]
        ttt = 3000.0
        beta = 0.616

        _chi_square = calculate_crow_amsaa_chi_square(n_failures, fail_times,
                                                      beta, ttt)
        self.assertAlmostEqual(_chi_square, 15.1745191)
