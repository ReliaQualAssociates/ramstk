#!/usr/bin/env python
"""
Contains functions for performing calculations associated with the Crow-AMSAA
model.
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.statistics.CrowAMSAA.py is part of The RTK Project
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

# Import modules for mathematics.
from math import log
import numpy as np
from scipy.optimize import fsolve

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

_ = gettext.gettext


# These are the Cramer-von Mises critical values for Crow-AMSAA GoF tests.
CVM_TABLE = {2: {0.2: 0.138, 0.15: 0.149, 0.1: 0.162, 0.05: 0.175,
                 0.01: 0.186},
             3: {0.2: 0.121, 0.15: 0.135, 0.1: 0.154, 0.05: 0.184,
                 0.01: 0.23},
             4: {0.2: 0.121, 0.15: 0.134, 0.1: 0.155, 0.05: 0.191,
                 0.01: 0.28},
             5: {0.2: 0.121, 0.15: 0.137, 0.1: 0.160, 0.05: 0.199,
                 0.01: 0.30},
             6: {0.2: 0.123, 0.15: 0.139, 0.1: 0.162, 0.05: 0.204,
                 0.01: 0.31},
             7: {0.2: 0.124, 0.15: 0.140, 0.1: 0.165, 0.05: 0.208,
                 0.01: 0.32},
             8: {0.2: 0.124, 0.15: 0.141, 0.1: 0.165, 0.05: 0.210,
                 0.01: 0.32},
             9: {0.2: 0.125, 0.15: 0.142, 0.1: 0.167, 0.05: 0.212,
                 0.01: 0.32},
             10: {0.2: 0.125, 0.15: 0.142, 0.1: 0.167, 0.05: 0.212,
                  0.01: 0.32},
             11: {0.2: 0.126, 0.15: 0.143, 0.1: 0.169, 0.05: 0.214,
                  0.01: 0.32},
             12: {0.2: 0.126, 0.15: 0.144, 0.1: 0.169, 0.05: 0.214,
                  0.01: 0.32},
             13: {0.2: 0.126, 0.15: 0.144, 0.1: 0.169, 0.05: 0.214,
                  0.01: 0.33},
             14: {0.2: 0.126, 0.15: 0.144, 0.1: 0.169, 0.05: 0.214,
                  0.01: 0.33},
             15: {0.2: 0.126, 0.15: 0.144, 0.1: 0.169, 0.05: 0.215,
                  0.01: 0.33},
             16: {0.2: 0.127, 0.15: 0.145, 0.1: 0.171, 0.05: 0.216,
                  0.01: 0.33},
             17: {0.2: 0.127, 0.15: 0.145, 0.1: 0.171, 0.05: 0.217,
                  0.01: 0.33},
             18: {0.2: 0.127, 0.15: 0.146, 0.1: 0.171, 0.05: 0.217,
                  0.01: 0.33},
             19: {0.2: 0.127, 0.15: 0.146, 0.1: 0.171, 0.05: 0.217,
                  0.01: 0.33},
             20: {0.2: 0.128, 0.15: 0.146, 0.1: 0.172, 0.05: 0.217,
                  0.01: 0.33},
             30: {0.2: 0.128, 0.15: 0.146, 0.1: 0.172, 0.05: 0.218,
                  0.01: 0.33},
             60: {0.2: 0.128, 0.15: 0.147, 0.1: 0.173, 0.05: 0.220,
                  0.01: 0.33},
             100: {0.2: 0.129, 0.15: 0.147, 0.1: 0.173, 0.05: 0.220,
                   0.01: 0.34}}


def beta_grouped(beta, fails, times, logt):
    """
    Function for estimating the beta value from grouped data.

    :param float beta: guess for the Crow-AMSAA shape parameter.
    :param ndarray fails: number of failures occurring in each interval of
                          time.
    :param ndarray times: end time for each interval.
    :param ndarray logt: the natural log of the end time for each interval.
    """

    _beta = sum(fails[1:] * ((times[1:]**beta * logt[1:] -
                              times[:-1]**beta * logt[:-1]) /
                             (times[1:]**beta - times[:-1]**beta) -
                             log(max(times))))

    return _beta


def calculate_crow_amsaa_parameters(n_failures, fail_times, t_star=0.0,
                                    grouped=False):
    """
    Function to estimate the parameters of the Crow-AMSAA model.  This is also
    used when MLE is used to estimated the NHPP Power Law model parameters.
    The form of the Crow-AMSAA model used in RTK:

    .. hlist::
    :columns: 1

        * cumulative failure intensity = lambda_c = alpha * T^(beta - 1)
        * cumulative MTBF = MTBFc = (1 / alpha) * T^(1- beta)
        * instantaneous failure intensity = lambda_i = alpha * beta * T^(beta - 1)
        * instantaneous MTBF = MTBFi = 1 / lambda_i

    :param list n_failures: list of failure counts at each failure time.
    :param list fail_times: list of failure times.
    :param float t_star: the termination time for time terminated (Type I)
                         tests.
    :param bool grouped: indicates whether or not the failure times are
                         exact (default) or grouped.
    :return: (_alpha_hat, _beta_hat); estimates of the Crow-AMSAA scale
             parameter and shape parameter
    :rtype: tuple
    """

    # Validate that the failure time and failure count lists are not empty.
    # If they are, raise an error and return 0.0 for both parameters.
# TODO: Move this to the view module.
    if n_failures == [] or fail_times == []:
        #Widgets.rtk_error(_(u"The list of failure times and/or the list of "
        #                  u"failure counts is empty.  Cannot estimate "
        #                  u"Crow-AMSAA parameters without both."))
        return 0.0, 0.0

    # If a termination time is not provided, assume a failure terminated
    # test and set the termination time equal to the last failure time.
    if t_star <= 0.0:
        t_star = max(fail_times)

    # Calculate the logarithm (base e) of the failure times.
    _logT = [log(x) for x in fail_times]
    if not grouped:
        _beta_hat = [sum(n_failures) /
                     (sum(n_failures) * log(t_star) - sum(_logT))]

    elif grouped:
        # Convert our Python lists to numpy arrays.  We need to insert a
        # zero in the first position for the _beta_grouped() function to
        # work properly.
        __failures = np.array([0.0] + n_failures)
        __times = np.array([0.0] + fail_times)
        __logt = np.array([0.0] + _logT)

        _initial_guess = sum(n_failures) / (sum(n_failures) *
                                            log(t_star) - sum(_logT))
        _beta_hat, _info, _ier, __ = fsolve(beta_grouped, _initial_guess,
                                            args=(__failures, __times,
                                                  __logt),
                                            full_output=True)
# TODO: Move this to the view module.
        if _ier != 1:
            #Widgets.rtk_information(_(u"The solution for the shape parameter "
            #                        u"did not converge in %d iterations.  Try "
            #                        u"using regression.") % _info['nfev'])
            return 1.0, 1.0

    _beta_hat = _beta_hat[0]
    _alpha_hat = sum(n_failures) / t_star**_beta_hat

    return _alpha_hat, _beta_hat


def calculate_crow_amsaa_mean(est_time, alpha, beta): # pylint: disable=C0103
    """
    Function to calculate the Crow-AMSAA model cumulative and instantaneous
    mean values (e.g., MTBF) given the Crow-AMSAA parameters and a time.  The
    Crow-AMSAA model used is:

    .. math::
    cumulative mean &= mean_c = (1 / alpha) * T^((1 - beta) \\
    instantaneous mean &= mean_i = 1 / (alpha * beta * T^(beta - 1))

    :param float est_time: the time at which to calculate the means.
    :param float alpha: the scale parameter used to calculate the means.
    :param float beta: the shape parameter used to calculate the means.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    try:
        _cum_mean = (1.0 / alpha) * est_time**(1.0 - beta)
    except ZeroDivisionError:
        _cum_mean = np.inf

    try:
        _instantaneous_mean = 1.0 / (alpha * beta *
                                     est_time**(beta - 1.0))
    except ZeroDivisionError:
        _instantaneous_mean = np.inf

    return _cum_mean, _instantaneous_mean


def calculate_cramer_vonmises(n_failures, fail_times, beta, t_star=0.0,
                              type2=True):
    """
    Function to calculate the Cramer-von Mises GoF statistic to test whether or
    not a set of data fits to the Crow-AMSAA model.  This is used when failure
    times are exact.

    .. note:: The null hypothesis is rejected if the statistic exceeds the
              critical value for a chosen significance level.

    :param int n_failures: list of failure counts at each failure time.
    :param float fail_times: list of failure times.
    :param float beta: the point estimate of the Crow-AMSAA beta parameter.
    :param float t_star: termination time for Type I tests.
    :param bool type2: whether or not the test is time terminated (Type I) or
                       failure terminated (Type II).
    :return: the Cramer-vonMises test statistic
    :rtype: float
    """

    _m = len(fail_times)
    _N = np.sum(n_failures)

    # If the test was failure terminated (Type II), set the termination
    # time equal to the last failure time and unbias the beta estimate.
    if type2:
        t_star = fail_times[-1]
        _beta_bar = (_N - 1) * beta / _N
        _M = _N - 1
    else:
        _beta_bar = beta
        _M = _N

    _ei = sum([(((fail_times[i] / t_star)**_beta_bar) - ((2.0 * i - 1.0) / (2.0 * _M)))**2.0 for i in range(_m)])

    _Cvm = _ei + (1.0 / (12.0 * _M))

    return _Cvm


def calculate_crow_amsaa_chi_square(n_failures, fail_times, beta, ttt,
                                    grouped=True):
    """
    Function to calculate the chi-square statistic for GoF.  This is used when
    failure times are grouped.  The test statistic is calculated as follows:

    .. hlist::
    :columns: 1

        * theta_i = lambda * (T_i^beta - T_i-1^beta)
        * chi-square = sum((Ni - theta_i)^2 / theta_i)

    Where theta_i is the expected number of failures in the interval (i, i-1)
    and Ni is the observed number of failures.  The null hypothesis is rejected
    if the statistic exceeds the critical value for a chosen significance
    level.

    :param int n_failures: list of failure counts at each failure time.
    :param float fail_times: list of failure times.
    :param float beta: the point estimate of the Crow-AMSAA beta parameter.
    :param float ttt: the total time on test.
    :param bool grouped: indictes whether data is grouped (default) or exact.
    :return: the chi-squared test statistic
    :rtype: float
    """

    _N = sum(n_failures)

    if not grouped:
        _chi_square = 2.0 * _N / beta

    elif grouped:
        fail_times = [0.0] + fail_times

        _theta = [_N * (fail_times[i] - fail_times[i - 1]) / ttt
                  for i in range(1, len(fail_times))]
        _chi_square = sum([((n_failures[i] - _theta[i])**2.0 / _theta[i])
                           for i in range(len(_theta))])

    return _chi_square


def cramer_vonmises_critical_value(df, confidence):
    """
    Method to find the Cramer-von Mises critical value from a dictionary of
    values.

    :param int df: the degrees of freedom for the critical value.
    :param float confidence: the statistical confidence for the critical
                             value.
    :return: _cvm, the critical value.
    :rtype: float
    """

    _conf = float('{0:0.2f}'.format(1.0 - confidence / 100.0))

    # Get the proper entry from the Cramer-von Mises dictionary of critical
    # values.  If the degrees of freedom (i.e., number of failures) is a key,
    # get the exact record.  If the degrees of freedom are not a key,
    # interpolate between the two records on either side.
    _keys = CVM_TABLE.keys()
    _k = min(range(len(_keys)), key=lambda i: abs(_keys[i] - df))
    _lower = CVM_TABLE[_keys[_k]]
    _upper = CVM_TABLE[_keys[_k + 1]]
    try:
        _diccvm = CVM_TABLE[df]
    except KeyError:                        # Need to interpolate
        if _lower == _upper:
            _diccvm = _lower
        else:
            _diccvm = {}
            for _k in _lower.keys():
                _diccvm[_k] = _lower[_k] + ((_upper[_k] - _lower[_k]) / 2.0)

    # Get the critical value depending on the desired confidence level.  If
    # the confidence level is a key, get the exact critical value otherwise
    # interpolate.
    try:
        _cvm = _diccvm[_conf]
    except KeyError:                        # Interpolate the critical value.
        _keys = sorted(_lower.keys())
        _k = min(range(len(_keys)), key=lambda i: abs(_keys[i] - _conf))
        if _conf > max(_keys):
            _cvm = _diccvm[max(_keys)]
        else:
            _m = (_upper[_keys[_k + 1]] - _lower[_keys[_k]]) / \
                 (_keys[_k + 1] - _keys[_k])
            _b = _lower[_keys[_k]] - _m * _lower[_keys[_k]]
            _cvm = _b + _m * _conf

    return _cvm
