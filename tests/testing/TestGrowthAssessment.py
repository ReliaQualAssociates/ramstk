#!/usr/bin/env python -O
"""
This is the test class for testing Growth Assessment module algorithms and
models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tests.testing.TestGrowth.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr
import numpy as np

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from testing.growth.Assessment import Model


class TestGrowthAssessmentModel(unittest.TestCase):
    """
    Class for testing the Reliability Growth Assessment data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Reliability Growth Assessment class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_assessment_create(self):
        """
        (TestGrowthAssessment) __init__ should return a Reliability Growth Assessment model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.lst_n_failures, [])
        self.assertEqual(self.DUT.lst_test_time, [])
        self.assertEqual(self.DUT.lst_fail_times, [])

        self.assertEqual(self.DUT.rg_assess_model, 0)
        self.assertEqual(self.DUT.grouped, 0)
        self.assertEqual(self.DUT.group_interval, 0.0)
        self.assertEqual(self.DUT.alpha_hat, 0.0)
        self.assertEqual(self.DUT.beta_hat, 0.0)
        self.assertEqual(self.DUT.cum_mean, 0.0)
        self.assertEqual(self.DUT.instantaneous_mean, 0.0)
        self.assertEqual(self.DUT.ttt, 0.0)
        self.assertEqual(self.DUT.se_alpha, 0.0)
        self.assertEqual(self.DUT.se_lnbeta, 0.0)
        self.assertEqual(self.DUT.cramer_vonmises, 0.0)
        self.assertEqual(self.DUT.chi_square, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestGrowthAssessment) set_attributes should return a 0 error code on success
        """

        _values = (0, 0, 1, 'Testing', 'Description', 'Attachment', 2, 40.2,
                   2.0, 0.9, 2, 1, 50.0, 5.2, 0.2, 123.5, 63.1, 500.0, 0.008,
                   0.065, 0.043, 15.4)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestGrowthAssessment) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (0, 0, 1, 'Testing', 'Description', 'Attachment', 2, 40.2,
                   2.0, 0.9, 2, 1, 50.0, 5.2, 0.2, None, 63.1, 500.0, 0.008,
                   0.065, 0.043, 15.4)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestGrowthAssessment) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 0, 1, 'Testing', 'Description', 'Attachment', 2, 40.2,
                   2.0, 0.9, 2, 1, 50.0, 5.2, 0.2, 123.5, 500.0, 0.008, 0.065,
                   0.043, 15.4)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestGrowthAssessment) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (None, None, 0, '', '', '', 0, 0.0, 0.0, 0.75, 0, 0,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestGrowthAssessment) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 0, 1, 'Testing', 'Description', 'Attachment', 2, 40.2,
                   2.0, 0.9, 2, 1, 50.0, 5.2, 0.2, 123.5, 63.1, 500.0, 0.008,
                   0.065, 0.043, 15.4)

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)
