#!/usr/bin/env python
"""
Contains functions for performing calculations associated with NHPP models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.analyses.statistics.NHPP.py is part of The RTK Project
#
# All rights reserved.

# Add NLS support.
import gettext
_ = gettext.gettext

# Import mathematical functions.
import numpy as np
from numpy.linalg import inv
from math import exp, log, sqrt
from scipy.stats import chi2, norm, t        # pylint: disable=E0611

from analyses.statistics.Bounds import *
from analyses.statistics.CrowAMSAA import *
from analyses.statistics.Duane import *


def power_law(F, X, confmeth, fitmeth=1, conftype=3, alpha=0.75, t_star=0.0):
    """
    Function to estimate the parameters (alpha and beta) of the NHPP power law
    model.  The NHPP power law model used in RTK is:

    .. hlist::
       :columns: 1

        * cumulative failure intensity = m(t) = alpha * t^(-beta)

    :param int F: list of failure counts.
    :param float X: list of individual failures times.
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
    _z_norm = norm.ppf(alpha)
    _critical_value_t = abs(t.ppf((1.0 - alpha) / 2.0, sum(F) - 2))

    # If no observation time was passed, use the maximum failure time and set
    # the _typeii_ variable True to indicate this is a failure truncated
    # dataset.
    if t_star == 0.0:
        t_star = max(X)
        _typeii = True

    if not _typeii:
        _N = sum(F) - 1
    else:
        _N = sum(F) - 2

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

    elif fitmeth == 2:                        # Regression
        # Estimate the Duane parameters and transform to the NHPP - Power Law
        # parameters.
        _b_hat, _beta_hat = calculate_duane_parameters(F, X)
        _alpha_hat = 1.0 / _b_hat

        # Calculate the standard errors on the parameter estimates.
        _se_beta, _se_lnb = calculate_duane_standard_error(F, X, _b_hat,
                                                           _beta_hat)

        # Calculate the bounding values for the alpha (scale) parameter.
        try:
            _alpha_lower = 1.0 / (_b_hat * exp(_critical_value_t * _se_lnb))
        except (OverflowError, ZeroDivisionError):
            _alpha_lower = _alpha_hat
        try:
            _alpha_upper = 1.0 / (_b_hat * exp(-_critical_value_t * _se_lnb))
        except (OverflowError, ZeroDivisionError):
            _alpha_upper = _alpha_hat

        # Calculate the bounding values for the beta (shape) parameter.
        _beta_lower = _beta_hat - _critical_value_t * _se_beta
        _beta_upper = _beta_hat + _critical_value_t * _se_beta

    return ([_alpha_lower, _alpha_hat, _alpha_upper],
            [_beta_lower, _beta_hat, _beta_upper])


def loglinear(_F_, _X_, _fitmeth_, _type_, _conf_=0.75, _T_star_=0.0):
    """
    Function to estimate the parameters (gamma0 and gamma1) of the NHPP
    loglinear model.

    Keyword Arguments:
    _F_       -- list of failure counts.
    _X_       -- list of individual failures times.
    _fitmeth_ -- method used to fit the data (1=MLE, 2=regression).
    _type_    -- the confidence level type
                 (1=lower one-sided, 2=upper one-sided, 3=two-sided).
    _conf_    -- the confidence level.
    _T_star_  -- the end of the observation period for time terminated, or
                 Type I, tests.
    """

    # Initialize variables.
    _n_ = 0.0
    _T_ = 0.0
    _M_ = 0.0
    _SSE_ = 0.0

    _typeii_ = False

    _loglinear_ = []

    _z_norm_ = norm.ppf(_conf_)

    # Define the function that will be set equal to zero and solved for gamma1.
    def _gamma1(_g1_, _Tj_, _r_, _Ta_):
        """ Function for estimating the gamma1 value. """

        # Calculate interim values.
        a = _r_ / _g1_
        b = _r_ * _Ta_ * exp(_g1_ * _Ta_)
        c = exp(_g1_ * _Ta_) - 1.0

        return _Tj_ + a - (b / c)

    # If no observation time was passed, use the maximum failure time and set
    #  the typeii_ variable True to indicate this is a failure truncated
    # dataset.
    if _T_star_ == 0.0:
        _T_star_ = sum(_X_)
        _typeii_ = True

    if not _typeii_:
        _N_ = len(_X_) - 1
    else:
        _N_ = len(_X_) - 2

    for i in range(len(_X_)):

        # Increment the total number of failures and the total time on test
        # then calculate the cumulative MTBF.
        _n_ += float(_F_[i])
        _T_ += float(_X_[i])
        _M_ = _T_ / _n_

        # Calculate the Loglinear parameters.  There is no regression function
        # for this model.
        g1 = fsolve(_gamma1, 0.000001, args=(_T_, _n_, _T_star_))[0]
        g0 = log((_n_ * g1) / (exp(g1 * _T_star_) - 1.0))

        # Calculate the cumulative and instantaneous failure intensity.
        _lc_hat_ = exp(g0 + g1 * _T_)
        #_li_hat_ = (1.0 - _alpha_hat_) * _lc_hat_

        # Calculate the cumulative and instantaneous MTBF from the model.
        try:
            _mc_hat_ = 1.0 / _lc_hat_
        except ZeroDivisionError:
            print g0, g1, _T_
        #_mi_hat_ = _mc_hat_ / (1.0 - _alpha_hat_)

        _loglinear_.append([_T_, _n_, _M_, g0, g1, _mc_hat_, _lc_hat_])

    return False
