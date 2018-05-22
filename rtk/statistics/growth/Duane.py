#!/usr/bin/env python
"""
Contains functions for performing calculations associated with the Duane model.
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.statistics.Duane.py is part of The RTK Project
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

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

_ = gettext.gettext


def calculate_duane_parameters(n_failures, fail_times):
    """
    Function to estimate the parameters of the Duane model.  This is also used
    when regression is used to estimated the NHPP Power Law model parameters.
    The form of the Duane model used in RTK:

    .. note:: cumulative failure intensity = lambda_c = (1 / b) * T^-alpha
    .. note:: cumulative MTBF = MTBFc = b * T^alpha
    .. note:: instantaneous failure intensity = lambda_i = (1 - alpha) * lambda_c
    .. note:: instantaneous MTBF = MTBFi = MTBFc / (1 - alpha)

    :param list n_failures: list of failure counts at each failure time.
    :param list fail_times: list of failure times.
    :return: _b_hat, _alpha_hat
    :rtype: tuple
    """

    _n = len(n_failures)

    if _n <= 0:
        return 0.0, 1.0

    _mtbf = [
        fail_times[i] / sum(n_failures[:i + 1])
        for i in range(len(fail_times))
    ]
    _logT = sum([log(x) for x in fail_times])
    _logT2 = sum([log(x)**2.0 for x in fail_times])
    _logM = sum([log(m) for m in _mtbf])
    _logTlogM = sum(
        [log(fail_times[i]) * log(_mtbf[i]) for i in range(len(fail_times))])

    # Estimate the shape parameter.
    try:
        _alpha_hat = (_logTlogM - (_logT * _logM / _n)) / \
                     (_logT2 - (_logT**2.0 / _n))
    except ZeroDivisionError:
        _alpha_hat = 0.0

    # Estimate the scale parameter.
    try:
        _b_hat = exp((1.0 / _n) * (_logM - _alpha_hat * _logT))
    except OverflowError:
        _b_hat = 1.0

    return _b_hat, _alpha_hat


def calculate_duane_standard_error(n_failures, fail_times, alpha, beta):
    """
    Function to calculate the standard error of the Duane model parameters,
    beta (scale) and alpha (shape), given the failure counts, failure
    times, and point estimates of the parameters.

    :param int n_failures: list of failure counts at each failure time.
    :param float fail_times: list of failure times.
    :param float alpha: the point estimate of the Duane alpha (shape)
                        parameter.
    :param float beta: the point estimate of the Duane b (scale) parameter.
    :return: estimates of the standard error for alpha and the log of beta.
    :rtype: tuple
    """

    _logT = sum([log(x) for x in fail_times])
    _logT2 = sum([log(x)**2.0 for x in fail_times])

    _SSE = sum([((log(beta) + alpha * log(fail_times[i])) - log(
        fail_times[i] / sum(n_failures[:i + 1])))**2.0
                for i in range(len(fail_times))])
    if sum(n_failures) > 2:
        _sigma2 = _SSE / (sum(n_failures) - 2)
    else:
        _sigma2 = _SSE

    try:
        _Sxx = _logT2 - (_logT**2.0 / sum(n_failures))
    except ZeroDivisionError:
        _Sxx = 1.0

    # Calculate the standard error of the log of b (scale) parameter.
    try:
        _se_lnb = sqrt(_sigma2) * sqrt(_logT2 / (sum(n_failures) * _Sxx))
    except ZeroDivisionError:
        _se_lnb = 0.0

    try:
        _se_alpha = sqrt(_sigma2) / sqrt(_Sxx)
    except ZeroDivisionError:
        _se_alpha = 0.0

    return _se_alpha, _se_lnb


def calculate_duane_mean(est_time, alpha, beta):  # pylint: disable=C0103
    """
    Method to calculate the Duane model cumulative and instantaneous mean
    values (e.g., MTBF) given the Duane parameters and a time.  The Duane
    model used is:

    .. note:: cumulative mean = cum_mean = beta * T^alpha
    .. note:: instantaneous mean = inst_mean = cum_mean / (1 - alpha)

    :param float est_time: the time at which to calculate the means.
    :param float alpha: the point estimate of the Duane alpha (shape)
                        parameter.
    :param float beta: the point estimate of the Duane b (scale) parameter.
    :return: estimate of the cumulative mean and instantaneous mean.
    :rtype: tuple
    """

    _cum_mean = beta * est_time**alpha

    try:
        _instantaneous_mean = _cum_mean / (1.0 - alpha)
    except ZeroDivisionError:
        _instantaneous_mean = _cum_mean

    return _cum_mean, _instantaneous_mean
