#!/usr/bin/env python
"""
Contains functions for performing calculations associated with statistical
bounds.
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.statistics.Bounds.py is part of The RTK Project
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

# Add NLS support.
import gettext

# Import mathematical functions.
from math import exp, log, sqrt
import numpy as np
from numpy.linalg import inv
from scipy.stats import chi2, norm          # pylint: disable=E0611

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

_ = gettext.gettext


def calculate_variance_covariance(n_failures, max_time, alpha, beta):
    """
    Function to calculate the variance-covariance matrix for the:

        * NHPP - Power Law model parameters
        * Crow-AMSAA model model parameters

    :param int n_failures: total number of failures in the data set.
    :param float max_time: total observation time or maximum failure time.
    :param float alpha: the point estimate of the alpha (scale) parameter.
    :param float beta: the point estimate of the beta (shape) parameter.
    :return: the variance-covariance matrix for alpha and beta.  It has the
             form:
                    [[Var(alpha), Cov(alpha, beta)],
                     [Cov(alpha, beta), Var(beta)]]
    :rtype: list of lists
    """

    try:
        _del_alpha = -n_failures / alpha**2.0
    except ZeroDivisionError:
        _del_alpha = 1.0

    try:
        _del_beta = -n_failures / beta**2.0 - \
                    alpha * max_time**beta * log(max_time)**2.0
    except ZeroDivisionError:
        _del_beta = 1.0

    _del_beta_alpha = -max_time**beta * log(max_time)

    _var_covar = inv(np.array([[-_del_alpha, -_del_beta_alpha],
                               [-_del_beta_alpha, -_del_beta]]))

    return _var_covar


def calculate_nhpp_mean_variance(n_failures, max_time, alpha, beta, metric=1):
    """
    Function to calculate the variance for the:

        * NHPP - Power Law model cumulative or instantaneous means
        * Crow-AMSAA model

    :param int n_failures: total number of failures in the data set.
    :param float max_time: total observation time or maximum failure time.
    :param float alpha: the point estimate of the alpha (scale) parameter.
    :param float beta: the point estimate of the beta (shape) parameter.
    :param int metric: the metric to calculate the variance for.
                       - 1 = Cumulative MTBF.
                       - 2 = Instantaneous MTBF.
    :return: the variance of the selected mean.
    :rtype: float
    """

    _var_covar = calculate_variance_covariance(n_failures, max_time,
                                               alpha, beta)

    if metric == 1:
        _del_mean_beta = -(1.0 / alpha) * max_time**(1.0 - beta) * \
                         log(max_time)
        _del_mean_alpha = -(1.0 / alpha**2.0) * max_time**(1.0 - beta)
    elif metric == 2:
        _del_mean_beta = -(1.0 / (alpha * beta**2.0)) * \
                           max_time**(1.0 - beta) - (1.0 / (alpha * beta)) * \
                           max_time**(1.0 - beta) * log(max_time)
        _del_mean_alpha = -(1.0 / (alpha**2.0 * beta)) * max_time**(1.0 - beta)

    _variance = _del_mean_beta**2.0 * _var_covar[1][1] + \
                _del_mean_alpha**2.0 * _var_covar[0][0] + \
                2.0 * _del_mean_beta * _del_mean_alpha * _var_covar[0][1]

    return _variance


def calculate_fisher_bounds(metric, variance, alpha):
    """
    Function to calculate the Fisher Information Matrix based confidence
    bounds.

    :param float metric: the point estimate of the metric to calculate bounds
                         for.
    :param float variance: the variance of the metric to calculate bounds for.
    :param float alpha: the confidence level of the calculated bounds.
    :return: _fisher_l, _fisher_u; the lower and upper Fisher bounds.
    :rtype: tuple of floats
    """

    # Ensure the confidence level is expressed as a decimal, then find the
    # standard normal value for constructing the confidence bounds.
    if alpha > 1.0:
        alpha = alpha / 100.0
    _z_norm = norm.ppf(alpha)

    if metric == 0.0:
        _fisher_l = 0.0
        _fisher_u = 0.0
    else:
        _fisher_l = metric * exp(-_z_norm * sqrt(variance) / metric)
        _fisher_u = metric * exp(_z_norm * sqrt(variance) / metric)

    return _fisher_l, _fisher_u


def calculate_crow_bounds(n_failures, t_star, _lambda, beta, alpha, metric,
                          data=2):
    """
    Function to calculate confidence bounds based on Dr. Larry Crow's methods.

    :param int n_failures: the total number of failures in the data set.
    :param float t_star: termination time.
    :param float _lambda: the estimated scale parameter.
    :param float beta: the estimated shape parameter.
    :param float alpha: the desired confidence level of the bounds.
    :param int metric: indicates which metric the bounds are being calculated
                       for.
                        1 = shape (beta)
                        2 = scale (lambda)
                        3 = cumulative failure intensity
                        4 = instantaneous MTBF (future)
    :param int data: the type of data set being passed.
                        1 = Type I or time terminated test
                        2 = Type II or failure terminated test (default)
    :return: _crow_l, _crow_u; the lower and upper bound on the metric.
    :rtype: tuple of floats
    """
# WARNING: Refactor calculate_crow_bounds; current McCabe Complexity metric=11.
    # Set default values so a value is returned in case something goes wrong.
    _crow_l = 1.0
    _crow_u = 1.0

    # Ensure the confidence level is expressed as a decimal.
    if alpha > 1.0:
        alpha = alpha / 100.0

    _alpha_l = (1.0 - alpha) / 2.0          # For lower bounds.
    _alpha_u = 1.0 - _alpha_l               # For upper bounds.

    if metric == 1:                         # Shape
        if data == 1:
            _chi2 = chi2.ppf(_alpha_l, 2.0 * n_failures)
            _crow_l = beta * (_chi2 / (2.0 * (n_failures - 1)))

            _chi2 = chi2.ppf(_alpha_u, 2.0 * n_failures)
            _crow_u = beta * (_chi2 / (2.0 * (n_failures - 1)))

        elif data == 2:
            _chi2 = chi2.ppf(_alpha_l, 2.0 * (n_failures - 1))
            _crow_l = beta * ((n_failures * _chi2) /
                              (2.0 * (n_failures - 1) * (n_failures - 2)))

            _chi2 = chi2.ppf(_alpha_u, 2.0 * (n_failures - 1))
            _crow_u = beta * ((n_failures * _chi2) /
                              (2.0 * (n_failures - 1) * (n_failures - 2)))

    elif metric == 2:                       # Scale
        # Calculate the lower bound.  It is the same regardless of the type.
        _chi2 = chi2.ppf(_alpha_l, 2.0 * n_failures)
        _crow_l = _chi2 / (2.0 * t_star**beta)

        if data == 1:
            _chi2 = chi2.ppf(_alpha_u, 2.0 * (n_failures + 2))
            _crow_u = _chi2 / (2.0 * t_star**beta)
        elif data == 2:
            _chi2 = chi2.ppf(_alpha_u, 2.0 * n_failures)
            _crow_u = _chi2 / (2.0 * t_star**beta)

    elif metric == 3:                       # Cum. failure intensity
        # Calculate the lower bound.  It is the same regardless of the type.
        _chi2 = chi2.ppf(_alpha_l, 2.0 * n_failures)
        _crow_l = _chi2 / (2.0 * t_star)

        if data == 1:
            _chi2 = chi2.ppf(_alpha_u, 2.0 * (n_failures + 2))
            _crow_u = _chi2 / (2.0 * t_star)
        elif data == 2:
            _chi2 = chi2.ppf(_alpha_u, 2.0 * n_failures)
            _crow_u = _chi2 / (2.0 * t_star)

    return _crow_l, _crow_u


def calculate_beta_bounds(a, m, b, alpha):            # pylint: disable=C0103
    """
    Function to calculate the mean, standard error, and bounds on the mean of
    a beta distribution.  These are the project management estimators, not
    exact calculations.

    :param float a: the minimum expected value.
    :param float m: most likely value.
    :param float b: the maximum expected value.
    :param float alpha: the desired confidence level.
    :return: _meanll, _mean, _meanul, _sd; the calculated mean, bounds, and
                                           standard error.
    :rtype: tuple of floats
    """

    if alpha < 0.0:
# TODO: Move to the view module.
        #Widgets.rtk_information(_(u"Confidence level take a value between 0 and "
        #                        u"100 inclusive [0, 100].  Please select and "
        #                        u"appropriate confidence level and try "
        #                        u"again."))
        return a, m, b, 0.0
    elif alpha > 1.0:
        _z_norm = norm.ppf(1.0 - ((1.0 - alpha / 100.0) / 2.0))
    else:
        _z_norm = norm.ppf(1.0 - ((1.0 - alpha) / 2.0))

    _mean = (a + 4.0 * m + b) / 6.0
    _sd = (b - a) / 6.0

    _meanll = _mean - _z_norm * _sd
    _meanul = _mean + _z_norm * _sd

    return _meanll, _mean, _meanul, _sd
