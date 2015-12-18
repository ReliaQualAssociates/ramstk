#!/usr/bin/env python
"""
###################################################
Non-Homogoneous Poisson Process Calculations Module
###################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.statistics.NHPP.py is part of The RTK Project
#
# All rights reserved.

# Import module for NLS support.
import gettext

# Import modules for mathematics support.
import numpy as np
from scipy.optimize import fsolve
from scipy.stats import t                   # pylint: disable=E0611

# Import other RTK modules.
try:
    from analyses.statistics.Bounds import calculate_crow_bounds, \
                                           calculate_fisher_bounds, \
                                           calculate_variance_covariance
    from analyses.statistics.CrowAMSAA import calculate_crow_amsaa_parameters
    from analyses.statistics.Duane import calculate_duane_parameters, \
                                          calculate_duane_standard_error
except ImportError:
    from rtk.analyses.statistics.Bounds import calculate_crow_bounds, \
                                               calculate_fisher_bounds, \
                                               calculate_variance_covariance
    from rtk.analyses.statistics.CrowAMSAA import \
                calculate_crow_amsaa_parameters
    from rtk.analyses.statistics.Duane import calculate_duane_parameters, \
                                              calculate_duane_standard_error

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

_ = gettext.gettext


def power_law(F, X, confmeth, fitmeth=1, conftype=3, alpha=0.75, t_star=0.0):   # pylint: disable=C0103, R0913, R0914
    """
    Function to estimate the parameters (alpha and beta) of the NHPP power law
    model.  The NHPP power law model used in RTK is:

    .. hlist::
       :columns: 1

        * cumulative MTBF = m(t) = (1.0 / alpha) * t^(1 - beta)
        * cumulative failure intensity = lambda(t) = alpha * t^(beta - 1)

    :param list F: list of failure counts.
    :param list X: list of individual failures times.
    :param int confmeth: the method for calculating confidence bounds.
    :param int fitmeth: method used to fit the data
                        1 = MLE (default)
                        2 = regression
    :param int conftype: the confidence level type
                         1 = lower one-sided
                         2 = upper one-sided
                         3 = two-sided (default)
    :param float alpha: the confidence level.
    :param float t_star: the end of the observation period for time terminated,
                         or Type I, tests.  Defaults to 0.0.
    :return: [_alpha_lower, _alpha_hat, _alpha_upper],
             [_beta_lower, _beta_hat, _beta_upper]
    :rtype: tuple of lists
    """

    # Initialize local variables.
    _typeii = False

    # Ensure failure times are of type float.
    X = [float(x) for x in X]

    # Ensure the confidence level is expressed as a decimal, then find the
    # standard normal and student-t critical values for constructing
    # confidence bounds on the parameters.
    if alpha > 1.0:
        alpha = alpha / 100.0
    _critical_value_t = abs(t.ppf((1.0 - alpha) / 2.0, sum(F) - 2))

    # If no observation time was passed, use the maximum failure time and set
    # the _typeii variable True to indicate this is a failure truncated
    # dataset.
    if t_star == 0.0:
        t_star = max(X)
        _typeii = True

    if not _typeii:
        _N = sum(F) - 1
    else:
        _N = sum(F) - 2

# TODO: Add support for one-sided bounds.
    if fitmeth == 1:                        # MLE
        # Estimate the Crow-AMASAA parameters using exact failure time data.
        _alpha_hat, _beta_hat = calculate_crow_amsaa_parameters(F, X, t_star)

        if confmeth == 1:                   # Crow bounds.
            # Calculate the bounding values for the alpha (scale) parameter.
            (_alpha_lower,
             _alpha_upper) = calculate_crow_bounds(_N, t_star, _alpha_hat,
                                                   _beta_hat, alpha, 2)

            # Calculate the bounding values for the beta (shape) parameter.
            (_beta_lower,
             _beta_upper) = calculate_crow_bounds(_N, t_star, _alpha_hat,
                                                  _beta_hat, alpha, 1)

        elif confmeth == 3:                 # Fisher matrix bounds.
            # Calculate the variance-covariance matrix for the NHPP - Power Law
            # parameters.
            _var_covar = calculate_variance_covariance(sum(F), t_star,
                                                       _alpha_hat, _beta_hat)

            # Calculate the bounding values for the alpha (scale) parameter.
            (_alpha_lower,
             _alpha_upper) = calculate_fisher_bounds(_alpha_hat,
                                                     _var_covar[0][0], alpha)

            # Calculate the bounding values for the beta (shape) parameter.
            (_beta_lower,
             _beta_upper) = calculate_fisher_bounds(_beta_hat,
                                                    _var_covar[1][1], alpha)

    elif fitmeth == 2:                      # Regression
        # Estimate the Duane parameters and transform to the NHPP - Power Law
        # parameters.  Parameters are returned scale, shape.
        _b_hat, _a_hat = calculate_duane_parameters(F, X)

        # Convert Duane parameters to Crow-AMSAA parameters.
        try:
            _alpha_hat = 1.0 / _b_hat
        except ZeroDivisionError:
            _alpha_hat = 1.0

        _beta_hat = 1.0 - _a_hat

        # Calculate the standard errors on the parameter estimates.
        _se_beta, _se_lnb = calculate_duane_standard_error(F, X, _a_hat,
                                                           _b_hat)

        # Calculate the bounding values for the beta (shape) parameter.
        try:
            _beta_lower = 1.0 - (_a_hat + _critical_value_t * _se_beta)
        except (OverflowError, ZeroDivisionError):
            _beta_lower = _beta_hat
        try:
            _beta_upper = 1.0 - (_a_hat - _critical_value_t * _se_beta)
        except (OverflowError, ZeroDivisionError):
            _beta_upper = _beta_hat

        # Calculate the bounding values for the alpha (scale) parameter.
        _alpha_lower = _alpha_hat * np.exp(-_critical_value_t * _se_lnb)
        _alpha_upper = _alpha_hat * np.exp(_critical_value_t * _se_lnb)

    return ([_alpha_lower, _alpha_hat, _alpha_upper],
            [_beta_lower, _beta_hat, _beta_upper])


def loglinear(F, X, confmeth, conftype=1, alpha=0.75, t_star=0.0):   # pylint: disable=C0103
    """
    Function to estimate the parameters (gamma0 and gamma1) of the NHPP
    loglinear model.  There is no regression function for this model.

    :param list F: list of failure counts.
    :param list X: list of individual failures times.
    :param int confmeth: the method for calculating confidence bounds.
    :param int conftype: the confidence level type
                         1 = lower one-sided
                         2 = upper one-sided
                         3 = two-sided (default)
    :param float alpha: the confidence level.
    :param float t_star: the end of the observation period for time terminated,
                         or Type I, tests.  Defaults to 0.0.
    :return: [_gamma0_lower, _gamma0_hat, _gamma0_upper],
             [_gamma1_lower, _gamma1_hat, _gamma1_upper]
    :rtype: tuple of lists
    """

    # Define the function that will be set equal to zero and solved for gamma1.
    def _gamma1(gamma1, T, r, Ta):          # pylint: disable=C0103
        """
        Function for estimating the gamma1 value.

        :param float gamma1:
        :param float T: the sum of individual failure times.
        :param int r: the total number of failures observed.
        :param float Ta: the latest observed failure time.
        :return: _g1; the starting estimate of the gamma1 parameter.
        :rtype: float
        """

        # Calculate interim values.
        _a = r / gamma1
        _b = r * Ta * np.exp(gamma1 * Ta)
        _c = np.exp(gamma1 * Ta) - 1.0

        _g1 = T + _a - (_b / _c)

        return _g1

    # Initialize variables.
    _g0 = [0.0, 0.0, 0.0]
    _g1 = [0.0, 0.0, 0.0]
    _typeii = False

    # Ensure failure times are of type float.
    X = [float(x) for x in X]

    # Ensure the confidence level is expressed as a decimal, then find the
    # standard normal and student-t critical values for constructing
    # confidence bounds on the parameters.
    if alpha > 1.0:
        alpha = alpha / 100.0

    # If no observation time was passed, use the maximum failure time and set
    # the _typeii variable True to indicate this is a failure truncated
    # dataset.
    if t_star == 0.0:
        t_star = sum(X)
        _typeii = True

    if not _typeii:
        _N = sum(F) - 1
    else:
        _N = sum(F) - 2

    _T = sum(X)

    # Calculate the Loglinear parameters.
    _g1[1] = fsolve(_gamma1, 0.001, args=(_T, _N, t_star))[0]
    _g0[1] = np.log((_N * _g1[1]) / (np.exp(_g1[1] * t_star) - 1.0))

# TODO: Add support for one-sided bounds.
    #if confmeth == 1:                       # Crow bounds.

    #elif confmeth == 3:                     # Fisher matrix bounds.

    print _g0, _g1
    return(_g0, _g1)
