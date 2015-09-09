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

import unittest
from nose.plugins.attrib import attr
import numpy as np

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

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
        self.DUANE_FAILS = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                            1, 1, 1, 1, 1, 1]
        self.DUANE_TIMES = [9.2, 25, 61.5, 260, 300, 710, 916, 1010, 1220,
                            2530, 3350, 4200, 4410, 4990, 5570, 8310, 8530,
                            9200, 10500, 12100, 13400, 14600, 22000]

        self.CROW_EXACT_FAILS = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                 1, 1, 1, 1, 1, 1, 1]
        self.CROW_EXACT_TIMES = [2.7, 10.3, 12.5, 30.6, 57.0, 61.3, 80.0,
                                 109.5, 125.0, 128.6, 143.8, 167.9, 229.2,
                                 296.7, 320.6, 328.2, 366.2, 396.7, 421.1,
                                 438.2, 501.2, 620.0]

    @attr(all=True, unit=True)
    def test_nhpp_power_law_regression_models(self):
        """
        (TestNHPP) power_law should return a list of parameter estimates when using regression and Fisher bounds.
        """

        # Check the value of alpha (scale) and beta (shape) for exact failure
        # times using regression and 90% two-sided confidence bounds.
        self.assertEqual(power_law(self.DUANE_FAILS, self.DUANE_TIMES,
                                   2, fitmeth=2, conftype=3, alpha=0.90)[0],
                         [1.4557332904506253,
                          1.6306995597672382,
                          1.826695227531624])
        self.assertEqual(power_law(self.DUANE_FAILS, self.DUANE_TIMES,
                                   2, fitmeth=2, conftype=3, alpha=0.90)[1],
                         [1.9311200103035631,
                          1.945662956921184,
                          1.9602059035388051])

    @attr(all=True, unit=True)
    def test_nhpp_power_law_mle_model_fisher_bounds(self):
        """
        (TestNHPP) power_law should return a list of parameter estimates when using MLE and Fisher bounds.
        """

        # Check the value of beta and alpha for exact failure times using MLE
        # and 90% two-sided confidence bounds.
        self.assertEqual(power_law(self.CROW_EXACT_FAILS,
                                   self.CROW_EXACT_TIMES,
                                   3, fitmeth=1, conftype=3, alpha=0.90)[0],
                         [0.13928340594382735,
                          0.42394221488057504,
                          1.2903690884062031])

        self.assertEqual(power_law(self.CROW_EXACT_FAILS,
                                   self.CROW_EXACT_TIMES,
                                   3, fitmeth=1, conftype=3, alpha=0.90)[1],
                         [0.46736466889703443,
                          0.6142103999317297,
                          0.8071949817571866])

    @attr(all=True, unit=True)
    def test_nhpp_power_law_mle_model_crow_bounds(self):
        """
        (TestNHPP) power_law should return a list of parameter estimates when using MLE and Crow bounds.
        """

        # Check the value of beta and alpha for exact failure times using MLE
        # and 90% two-sided confidence bounds.
        self.assertEqual(power_law(self.CROW_EXACT_FAILS,
                                   self.CROW_EXACT_TIMES,
                                   3, fitmeth=1, conftype=1, alpha=0.90)[0],
                         [0.13928340594382735,
                          0.42394221488057504,
                          1.2903690884062031])

        self.assertEqual(power_law(self.CROW_EXACT_FAILS,
                                   self.CROW_EXACT_TIMES,
                                   3, fitmeth=1, conftype=1, alpha=0.90)[1],
                         [0.46736466889703443,
                          0.6142103999317297,
                          0.8071949817571866])
