#!/usr/bin/env python -O
"""
This is the test class for testing Duane model algorithms.
"""

# -*- coding: utf-8 -*-
#
#       tests.statistics.TestDuane.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr
import numpy as np

import dao.DAO as _dao
from analyses.statistics.Duane import *

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestDuane(unittest.TestCase):
    """
    Class for testing the Duane model functions.
    """

    @attr(all=True, unit=True)
    def test_calculate_duane_parameters(self):
        """
        (TestDuane) calculate_duane_parameters should return a tuple of floats
        """

        # See http://reliawiki.org/index.php/Duane_Model for example data.
        n_failures = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1]
        fail_times = [9.2, 25.0, 61.5, 260.0, 300.0, 710.0, 916.0, 1010.0,
                      1220.0, 2530.0, 3350.0, 4200.0, 4410.0, 4990.0, 5570.0,
                      8310.0, 8530.0, 9200.0, 10500.0, 12100.0, 13400.0,
                      14600.0, 22000.0]

        _alpha, _beta = calculate_duane_parameters(n_failures, fail_times)
        self.assertAlmostEqual(_alpha, 1.9456630)
        self.assertAlmostEqual(_beta, 0.6132337)

    @attr(all=True, unit=True)
    def test_calculate_duane_parameters_zero_division(self):
        """
        (TestDuane) calculate_duane_parameters should return a tuple of floats with alpha=0.0 when encountering a zero division error
        """

        # See http://reliawiki.org/index.php/Duane_Model for example data.
        n_failures = []
        fail_times = [9.2, 25.0, 61.5, 260.0, 300.0, 710.0, 916.0, 1010.0,
                      1220.0, 2530.0, 3350.0, 4200.0, 4410.0, 4990.0, 5570.0,
                      8310.0, 8530.0, 9200.0, 10500.0, 12100.0, 13400.0,
                      14600.0, 22000.0]

        _alpha, _beta = calculate_duane_parameters(n_failures, fail_times)
        self.assertAlmostEqual(_alpha, 0.0)
        self.assertAlmostEqual(_beta, 1.0)

    @attr(all=True, unit=True)
    def test_calculate_duane_standard_error(self):
        """
        (TestDuane) calculate_duane_standard_error should return tuple of floats with the estimated standard errors of alpha and beta
        """

        # See http://reliawiki.org/index.php/Duane_Model for example data.
        n_failures = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1]
        fail_times = [9.2, 25.0, 61.5, 260.0, 300.0, 710.0, 916.0, 1010.0,
                      1220.0, 2530.0, 3350.0, 4200.0, 4410.0, 4990.0, 5570.0,
                      8310.0, 8530.0, 9200.0, 10500.0, 12100.0, 13400.0,
                      14600.0, 22000.0]
        _alpha = 0.6132337
        _beta = 1.9456630

        _se_alpha, _se_lnbeta = calculate_duane_standard_error(n_failures,
                                                               fail_times,
                                                               _alpha, _beta)
        self.assertAlmostEqual(_se_alpha, 0.008451551)
        self.assertAlmostEqual(_se_lnbeta, 0.06595950)

    @attr(all=True, unit=True)
    def test_calculate_duane_standard_error_two_failures(self):
        """
        (TestDuane) calculate_duane_standard_error should return a tuple of floats with the estimated standard errors of alpha and beta when there are less than three failures
        """

        # See http://reliawiki.org/index.php/Duane_Model for example data.
        n_failures = [1, 1]
        fail_times = [9.2, 25.0]
        _alpha = 0.6132337
        _beta = 1.9456630

        _se_alpha, _se_lnbeta = calculate_duane_standard_error(n_failures,
                                                               fail_times,
                                                               _alpha, _beta)
        self.assertAlmostEqual(_se_alpha, 0.3166068)
        self.assertAlmostEqual(_se_lnbeta, 0.8752911)

    @attr(all=True, unit=True)
    def test_calculate_duane_mean(self):
        """
        (TestDuane) calculate_duane_mean should return a tuple of floats with the estimated cumulative and instantaneous mean
        """

        # See http://reliawiki.org/index.php/Duane_Model for example data.
        _est_time = 22000.0
        _alpha = 0.6132337
        _beta = 1.9456630

        _cum_mean, _instantaneous_mean = calculate_duane_mean(_est_time,
                                                              _alpha, _beta)
        self.assertAlmostEqual(_cum_mean, 895.3390935)
        self.assertAlmostEqual(_instantaneous_mean, 2314.9356434)
