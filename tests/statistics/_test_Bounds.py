#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.statistics.TestBounds.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing statistical bound algorithms and models."""

import unittest
from nose.plugins.attrib import attr
import numpy as np

import ramstk.dao.DAO as _dao
from ramstk.statistics.Bounds import *

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Doyle "weibullguy" Rowland'


class TestStatisticalBounds(unittest.TestCase):
    """Class for testing the Statistical Bound functions."""

    @attr(all=True, unit=False)
    def test_calculate_variance_covariance(self):
        """
        (TestStatisticalBounds) calculate_variance_covariance should return a list of lists
        """

        _var_covar = calculate_variance_covariance(22, 620.0, 0.4239, 0.6142)
        self.assertAlmostEqual(_var_covar[0][0], 0.1351777)
        self.assertAlmostEqual(_var_covar[0][1], -0.04660735)
        self.assertAlmostEqual(_var_covar[1][0], -0.04660735)
        self.assertAlmostEqual(_var_covar[1][1], 0.01710296)
        self.assertEqual(_var_covar[0][1], _var_covar[1][0])

    @attr(all=True, unit=False)
    def test_calculate_variance_covariance_zero_division_scale(self):
        """
        (TestStatisticalBounds) calculate_variance_covariance should return a list of lists when the estimated scale parameter is zero
        """

        _var_covar = calculate_variance_covariance(22, 620.0, 0.0, 0.6142)
        self.assertAlmostEqual(_var_covar[0][0], -0.0005236216)
        self.assertAlmostEqual(_var_covar[0][1], 0.002995667)
        self.assertAlmostEqual(_var_covar[1][0], 0.002995667)
        self.assertAlmostEqual(_var_covar[1][1], 8.9787221E-06)

    @attr(all=True, unit=False)
    def test_calculate_variance_covariance_zero_division_shape(self):
        """
        (TestStatisticalBounds) calculate_variance_covariance should return a list of lists when the estimated shape parameter is zero
        """

        _var_covar = calculate_variance_covariance(22, 620.0, 0.4239, 0.0)
        self.assertAlmostEqual(_var_covar[0][0], 0.006105992)
        self.assertAlmostEqual(_var_covar[0][1], 0.03925982)
        self.assertAlmostEqual(_var_covar[1][0], 0.03925982)
        self.assertAlmostEqual(_var_covar[1][1], -0.7475704)

    @attr(all=True, unit=False)
    def test_calculate_nhpp_mean_variance_cum_mean(self):
        """
        (TestStatisticalBounds) calculate_nhpp_mean_variance should return a float value equal to the variance of the cumulative mean of the NHPP model
        """

        _mean_var = calculate_nhpp_mean_variance(46, 3000.0, 0.332, 0.616)
        self.assertAlmostEqual(_mean_var, 92.3421144)

    @attr(all=True, unit=False)
    def test_calculate_nhpp_mean_variance_inst_mean(self):
        """
        (TestStatisticalBounds) calculate_nhpp_mean_variance should return a float value equal to the variance of the instantaneous mean of the NHPP model
        """

        _mean_var = calculate_nhpp_mean_variance(46, 3000.0, 0.332, 0.616, 2)
        self.assertAlmostEqual(_mean_var, 489.07164965)

    @attr(all=True, unit=False)
    def test_calculate_fisher_bounds(self):
        """
        (TestStatisticalBounds) calculate_fisher_bounds should return a tuple of float values with the lower and upper alpha bounds
        """

        _bounds = calculate_fisher_bounds(0.03548, 0.00005721408, 0.9)
        self.assertAlmostEqual(_bounds[0], 0.02699778)
        self.assertAlmostEqual(_bounds[1], 0.04662719)

    @attr(all=True, unit=False)
    def test_calculate_fisher_bounds_alpha(self):
        """
        (TestStatisticalBounds) calculate_fisher_bounds should return a tuple of float values with the lower and upper alpha bounds with alpha greater than one
        """

        _bounds = calculate_fisher_bounds(0.03548, 0.00005721408, 90.0)
        self.assertAlmostEqual(_bounds[0], 0.02699778)
        self.assertAlmostEqual(_bounds[1], 0.04662719)

    @attr(all=True, unit=False)
    def test_calculate_crow_bounds_cum_failure_rate_type2(self):
        """
        (TestStatisticalBounds) calculate_crow_bounds should return a tuple of float values with the lower and upper alpha bounds for the cumulative failure intensity for Type II tests
        """

        _bounds = calculate_crow_bounds(22, 620.0, 0.4239, 0.6142, 0.9, 3, 2)
        self.assertAlmostEqual(_bounds[0], 0.02402216)
        self.assertAlmostEqual(_bounds[1], 0.04877491)

    @attr(all=True, unit=False)
    def test_calculate_crow_bounds_shape_parameter_type2(self):
        """
        (TestStatisticalBounds) calculate_crow_bounds should return a tuple of float values with the lower and upper alpha bounds for the shape parameter for Type II tests
        """

        _bounds = calculate_crow_bounds(22, 620.0, 0.4239, 0.6142, 0.9, 1, 2)
        self.assertAlmostEqual(_bounds[0], 0.4527305)
        self.assertAlmostEqual(_bounds[1], 0.9349943)

    @attr(all=True, unit=False)
    def test_calculate_crow_bounds_scale_parameter_type2(self):
        """
        (TestStatisticalBounds) calculate_crow_bounds should return a tuple of float values with the lower and upper alpha bounds for the scale parameter for Type II tests
        """

        _bounds = calculate_crow_bounds(22, 620.0, 0.4239, 0.6142, 0.9, 2, 2)
        self.assertAlmostEqual(_bounds[0], 0.2870230)
        self.assertAlmostEqual(_bounds[1], 0.5827754)

    @attr(all=True, unit=False)
    def test_calculate_crow_bounds_cum_failure_rate_type1(self):
        """
        (TestStatisticalBounds) calculate_crow_bounds should return a tuple of float values with the lower and upper alpha bounds for the cumulative failure intensity for Type I tests
        """

        _bounds = calculate_crow_bounds(22, 620.0, 0.4239, 0.6142, 0.9, 3, 1)
        self.assertAlmostEqual(_bounds[0], 0.02402216)
        self.assertAlmostEqual(_bounds[1], 0.05255707)

    @attr(all=True, unit=False)
    def test_calculate_crow_bounds_shape_parameter_type1(self):
        """
        (TestStatisticalBounds) calculate_crow_bounds should return a tuple of float values with the lower and upper alpha bounds for the shape parameter for Type I tests
        """

        _bounds = calculate_crow_bounds(22, 620.0, 0.4239, 0.6142, 0.9, 1, 1)
        self.assertAlmostEqual(_bounds[0], 0.4356064)
        self.assertAlmostEqual(_bounds[1], 0.8844610)

    @attr(all=True, unit=False)
    def test_calculate_crow_bounds_scale_parameter_type1(self):
        """
        (TestStatisticalBounds) calculate_crow_bounds should return a tuple of float values with the lower and upper alpha bounds for the scale parameter for Type I tests
        """

        _bounds = calculate_crow_bounds(22, 620.0, 0.4239, 0.6142, 0.9, 2, 1)
        self.assertAlmostEqual(_bounds[0], 0.2870230)
        self.assertAlmostEqual(_bounds[1], 0.6279656)

    @attr(all=True, unit=False)
    def test_calculate_crow_bounds_scale_parameter_alpha(self):
        """
        (TestStatisticalBounds) calculate_crow_bounds should return a tuple of float values with the lower and upper alpha bounds for the scale parameter when passed an alpha parameter greater than one
        """

        _bounds = calculate_crow_bounds(22, 620.0, 0.4239, 0.6142, 90.0, 2, 2)
        self.assertAlmostEqual(_bounds[0], 0.2870230)
        self.assertAlmostEqual(_bounds[1], 0.5827754)

    @attr(all=True, unit=True)
    def test_beta_bounds(self):
        """(TestStatisticalBounds) calculate_beta_bounds should return a tuple of float values with the lower bound, point estimate, upper bound, and standard error."""
        self.assertAlmostEqual(
            calculate_beta_bounds(10.0, 20.0, 40.0, 0.9)[0], 13.44239853)
        self.assertAlmostEqual(
            calculate_beta_bounds(10.0, 20.0, 40.0, 0.9)[1], 21.66666666)
        self.assertAlmostEqual(
            calculate_beta_bounds(10.0, 20.0, 40.0, 0.9)[2], 29.89093480)
        self.assertAlmostEqual(
            calculate_beta_bounds(10.0, 20.0, 40.0, 0.9)[3], 5.0)
        self.assertAlmostEqual(
            calculate_beta_bounds(10.0, 20.0, 40.0, 90.0)[0], 13.44239853)
        self.assertAlmostEqual(
            calculate_beta_bounds(10.0, 20.0, 40.0, 90.0)[1], 21.66666666)
        self.assertAlmostEqual(
            calculate_beta_bounds(10.0, 20.0, 40.0, 90.0)[2], 29.89093480)
        self.assertAlmostEqual(
            calculate_beta_bounds(10.0, 20.0, 40.0, 90.0)[3], 5.0)
