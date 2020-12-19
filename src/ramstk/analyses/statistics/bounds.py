# -*- coding: utf-8 -*-
#
#       ramstk.analyses.statistics.bounds.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Functions for performing calculations associated with statistical bounds."""

# Standard Library Imports
from math import exp, log, sqrt

# Third Party Imports
import numpy as np
from numpy.linalg import inv
from scipy.stats import chi2, norm


def calculate_variance_covariance(n_failures, max_time, alpha, beta):
    """Calculate variance-covariance matrix for NHPP and Crow-AMSAA models.

    :param n_failures: total number of failures in the data set.
    :param max_time: total observation time or maximum failure time.
    :param alpha: the point estimate of the alpha (scale) parameter.
    :param beta: the point estimate of the beta (shape) parameter.
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
        _del_beta = -n_failures / (
            beta**2.0 - alpha * max_time**beta * log(max_time)**2.0)
    except ZeroDivisionError:
        _del_beta = 1.0

    _del_beta_alpha = -max_time**beta * log(max_time)

    _var_covar = inv(
        np.array([[-_del_alpha, -_del_beta_alpha],
                  [-_del_beta_alpha, -_del_beta]]))

    return _var_covar


def calculate_nhpp_mean_variance(n_failures, max_time, alpha, beta, metric=1):
    """Calculate the variance for the NHPP and Crow-AMSAA models.

    :param n_failures: total number of failures in the data set.
    :param max_time: total observation time or maximum failure time.
    :param alpha: the point estimate of the alpha (scale) parameter.
    :param beta: the point estimate of the beta (shape) parameter.
    :param metric: the metric to calculate the variance for.
                       - 1 = Cumulative MTBF.
                       - 2 = Instantaneous MTBF.
    :return: the variance of the selected mean.
    :rtype: float
    """
    _var_covar = calculate_variance_covariance(n_failures, max_time, alpha,
                                               beta)

    if metric == 1:
        _del_mean_beta = (-(1.0 / alpha) * max_time**(1.0 - beta)
                          * log(max_time))
        _del_mean_alpha = -(1.0 / alpha**2.0) * max_time**(1.0 - beta)
    elif metric == 2:
        _del_mean_beta = (
            -(1.0 / (alpha * beta**2.0)) * max_time**(1.0 - beta) -
            (1.0 / (alpha * beta)) * max_time**(1.0 - beta) * log(max_time))
        _del_mean_alpha = -(1.0 / (alpha**2.0 * beta)) * max_time**(1.0 - beta)

    _variance = (_del_mean_beta**2.0 * _var_covar[1][1]
                 + _del_mean_alpha**2.0 * _var_covar[0][0]
                 + 2.0 * _del_mean_beta * _del_mean_alpha * _var_covar[0][1])

    return _variance


def calculate_fisher_bounds(metric, variance, alpha):
    """Calculate the Fisher Information Matrix based confidence bounds.

    :param metric: the point estimate of the metric to calculate bounds
                         for.
    :param variance: the variance of the metric to calculate bounds for.
    :param alpha: the confidence level of the calculated bounds.
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


def calculate_crow_bounds(n_failures,
                          t_star,
                          _lambda,
                          beta,
                          alpha,
                          metric,
                          data=2):
    """Calculate confidence bounds based on Dr. Larry Crow's methods.

    :param n_failures: the total number of failures in the data set.
    :param t_star: termination time.
    :param _lambda: the estimated scale parameter.
    :param beta: the estimated shape parameter.
    :param alpha: the desired confidence level of the bounds.
    :param metric: indicates which metric the bounds are being calculated for.
                        1 = shape (beta)
                        2 = scale (lambda)
                        3 = cumulative failure intensity
                        4 = instantaneous MTBF (future)
    :param data: the type of data set being passed.
                        1 = Type I or time terminated test
                        2 = Type II or failure terminated test (default)
    :return: _crow_l, _crow_u; the lower and upper bound on the metric.
    :rtype: tuple of floats
    """
    _crow_l = 1.0
    _crow_u = 1.0

    # Ensure the confidence level is expressed as a decimal.
    if alpha > 1.0:
        alpha = alpha / 100.0

    _alpha_l = (1.0 - alpha) / 2.0  # For lower bounds.
    _alpha_u = 1.0 - _alpha_l  # For upper bounds.

    if metric == 1:  # Shape
        if data == 1:
            _chi2 = chi2.ppf(_alpha_l, 2.0 * n_failures)
            _crow_l = beta * (_chi2 / (2.0 * (n_failures - 1)))

            _chi2 = chi2.ppf(_alpha_u, 2.0 * n_failures)
            _crow_u = beta * (_chi2 / (2.0 * (n_failures - 1)))

        elif data == 2:
            _chi2 = chi2.ppf(_alpha_l, 2.0 * (n_failures - 1))
            _crow_l = beta * ((n_failures * _chi2) / (2.0 * (n_failures - 1) *
                                                      (n_failures - 2)))

            _chi2 = chi2.ppf(_alpha_u, 2.0 * (n_failures - 1))
            _crow_u = beta * ((n_failures * _chi2) / (2.0 * (n_failures - 1) *
                                                      (n_failures - 2)))

    elif metric == 2:  # Scale
        # Calculate the lower bound.  It is the same regardless of the type.
        _chi2 = chi2.ppf(_alpha_l, 2.0 * n_failures)
        _crow_l = _chi2 / (2.0 * t_star**beta)

        if data == 1:
            _chi2 = chi2.ppf(_alpha_u, 2.0 * (n_failures + 2))
            _crow_u = _chi2 / (2.0 * t_star**beta)
        elif data == 2:
            _chi2 = chi2.ppf(_alpha_u, 2.0 * n_failures)
            _crow_u = _chi2 / (2.0 * t_star**beta)

    elif metric == 3:  # Cum. failure intensity
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


def do_calculate_beta_bounds(minimum, likely, maximum, alpha):
    """Calculate the mean, standard error, and bounds of the beta distribution.

    These are the project management estimators, not exact calculations.

    :param minimum: the minimum expected value.
    :param likely: most likely value.
    :param maximum: the maximum expected value.
    :param alpha: the desired confidence level.
    :return: _meanll, _mean, _meanul, _sd; the calculated mean, bounds, and
                                           standard error.
    :rtype: tuple of floats
    """
    if alpha > 1.0:
        _z_norm = norm.ppf(1.0 - ((1.0 - alpha / 100.0) / 2.0))
    else:
        _z_norm = norm.ppf(1.0 - ((1.0 - alpha) / 2.0))

    _mean = (minimum + 4.0 * likely + maximum) / 6.0
    _sd = (maximum - minimum) / 6.0

    _meanll = _mean - _z_norm * _sd
    _meanul = _mean + _z_norm * _sd

    return _meanll, _mean, _meanul, _sd
