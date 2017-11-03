#!/usr/bin/env python
"""
Contains functions for performing Mean Cumulative Function survival analysis
and testing for trend.
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.survival.MCF.py is part of The RTK Project
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

# Import modules for mathematics.
from math import log, sqrt
import numpy as np
from scipy.stats import norm                # pylint: disable=E0611

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


def format_data(data):
    """
    Helper function to coerce the dataset into the proper format for passing to
    the mean_cumulative_function.

    :param dict data: an ordered dictionary of dataset records.
    :return: _data; a dictionary with Assembly ID being the key and a list of
                    failure and censoring times as the value.
    :rtype: dict
    """

    _data = {}

    _unique_assemblies = list(set([x.assembly_id for x in data.values()]))
    for _id in _unique_assemblies:
        _times = []

        # Add the failure times.
        _records = [x for x in data.values()
                    if x.assembly_id == _id and x.status == 1]
        for _record in _records:
            _times.extend([_record.right_interval] * _record.n_failures)

        # Add the censoring times.
        _records = [x for x in data.values()
                    if x.assembly_id == _id and x.status == 2]
        for _record in _records:
            _times.extend([str(_record.right_interval) + '+'] *
                          _record.n_failures)

        _data[_id] = _times     # pylint: disable=W0631

    return _data


def d_matrix(data, times):
    """
    Function to create d.(tk) array for use in calculating the mean cumulative
    function.  The d.(tk) array is the total number of system recurrences at
    time tk.

    :param dict data: a dictionary with the system id as the key and a list of
                      the failure times as the value.
    :param float times: a list of unique and sorted failures times.
    :return: _d_matrix; matrix of total number of system recurrences at each
             unique failure time.
    :rtype: numpy 1-D matrix of integers
    """

    _d_matrix = []
    _N = len(times)

    # Iterate through:
    #   --> Each key (unique system)
    #       --> Each failure time for that key (unique system)
    #           --> Each unique failure time
    # If the system failure time is equal to the unique failure time, set the
    # count of system recurrences for that system/failure time cell to one.
    for key in data.iterkeys():
        _d_row = [0] * _N
        for _fail_time in data[key]:
            for i in range(_N):
                if _fail_time == times[i]:
                    _d_row[i] = 1

        _d_matrix.append(_d_row)

    # Transform to a numpy matrix and transpose so the rows are unique failure
    # times and the columns are unique systems.  The row-column intersection
    # (cell) is the count of failures for a system at a failure time.
    _d_matrix = np.matrix(_d_matrix, dtype=float).transpose()

    return _d_matrix


def delta_matrix(data, times):
    """
    Function to create delta.(tk) array for use in calculating the mean
    cumulative function.  The delta.(tk) array contains the indicator variable
    for system operating at time tk.

    :param dict data: a dictionary containing the failure/censoring data for a
                      population of systems.  The system id is the key and a
                      list of the failure/censoring times is the value.
    :param list times: a list of unique and sorted failures times.
    :return: _delta_matrix; matrix of indicator variables.
    :rtype: numpy 1-D matrix of integers
    """

    _delta_matrix = []
    _N = len(times)

    # Iterate through:
    #   --> Each key (unique system)
    #       --> Each unique failure time
    # If the system censoring time is greater than or equal to the unique
    # failure time, set the system operating indicator variable for that
    # system/failure time cell to one.
    for key in data.iterkeys():
        _delta_row = [0] * _N
        try:
            _censor_time = data[key][-1].rstrip('+')
        except AttributeError:
            _censor_time = data[key][-1]
        for i in range(_N):
            if float(_censor_time) >= times[i]:
                _delta_row[i] = 1

        _delta_matrix.append(_delta_row)

    # Transform to a numpy matrix and transpose so the rows are unique failure
    # times and the columns are unique systems.  The row-column intersection
    # (cell) is the count of failures for a system at a failure time.
    _delta_matrix = np.matrix(_delta_matrix, dtype=float).transpose()

    return _delta_matrix


def mean_cumulative_function(data, conf=0.75):
    """
    This function estimates the mean cumulative function for a population of
    items.

    :param dict data: a dictionary where the key is the system id and the value
                      is a list of failure/censoring times.  The last entry in
                      this list is the censoring time.  Failures times are
                      float or integer and the censoring time is a string.
                      For example: [88., 92., 227., '350+']
    :param float conf: the confidence level of the MCF estimates (default
                       is 75%).
    :return: _mcf; matrix of lists containing MCF values.  There is one row
             for each unique failure time.  Each row contains the following:
             - Unique failure time (t).
             - Number of failures at time t.
             - Lower bound on the MCF at time t.
             - Point estimate of the MCF at time t.
             - Upper bound on the MCF at time t.
             - Lower bound on the cumulative MTBF at time t.
             - Point estimate of the cumulative MTBF at time t.
             - Upper bound on the cumulative MTBF at time t.
             - Lower bound on the instantaneous MTBF at time t.
             - Point estimate of the instantaneous MTBF at time t.
             - Upper bound on the instantaneous MTBF at time t.
    :rtype: numpy matrix
    """

    # Find the standard normal critical value.
    _conf = 1.0 - ((1.0 - conf) / 2.0)
    _z_norm = norm.ppf(_conf)

    # Create the d matrix and the delta matrix for the data set.
    _times = reduce(lambda x, y: x + y, data.values())
    _times = set([float(f) for f in _times
                  if isinstance(f, float) or isinstance(f, int)])
    _times = sorted(list(_times))

    _d_matrix = d_matrix(data, _times)
    _delta_matrix = delta_matrix(data, _times)

    _delta_dot = _delta_matrix.sum(axis=1)
    _d_dot = _d_matrix.sum(axis=1)

    _d_bar = _d_dot / _delta_dot

    # Calculate the MCF at each unique failure time.
    _mu_hat = _d_bar.cumsum(axis=0)

    # Calculate the variance and standard error of the MCF at each unique
    # failure time.
    _mu_var = mcf_variance(_delta_matrix, _d_matrix, _delta_dot, _d_bar)
    _mu_se = np.sqrt(_mu_var)

    # Calculate the lower and upper bounds on the MCF at each unique failure
    # time.
    _w = np.exp(np.divide(np.multiply(_mu_se, _z_norm), _mu_hat))

    _mu_hat_ll = np.divide(_mu_hat, _w)
    _mu_hat_ul = np.multiply(_mu_hat, _w)

    _times = np.matrix(_times).transpose().tolist()

    _mcf = np.concatenate((_times, _d_dot), axis=1)
    _mcf = np.concatenate((_mcf, _mu_hat_ll), axis=1)
    _mcf = np.concatenate((_mcf, _mu_hat), axis=1)
    _mcf = np.concatenate((_mcf, _mu_hat_ul), axis=1)

    return _mcf


def mcf_variance(delta, d_mat, delta_dot, d_bar):
    """
    Function to calculate the variance of d(tk) for the MCF.

    :param numpy matrix delta: the matrix of indicator variables for operating
                               systems.
    :param numpy matrix d_mat: the matrix of the number of system recurrences.
    :param numpy array delta_dot: an array containing the risk population at
                                  each observed failure time.
    :param numpy array d_bar: an array containing the fraction of the risk
                              population that failed at each observed failure
                              time.
    :return: _variance_mu; an array containing the variance of the MCF at each
             observed failure time.
    :rtype: numpy array
    """

    _temp1 = np.divide(delta, delta_dot)
    _temp2 = np.subtract(d_mat, d_bar)

    _variance = np.multiply(_temp1, _temp2)
    _variance = np.power(_variance, 2.0)
    _variance = np.sum(_variance, axis=1)

    return _variance


def mil_handbook(times):
    """
    Function to calculate the MIL-HDBK statistic for trend.  The test statistic
    is calculated as follows:

        MHB = -2.0 * SUM[log(t / T)]

    where T is the maximum failure time in the data set.

    The null hypothesis is rejected if the statistic exceeds the critical value
    for a chosen significance level.

    :param numpy array times: an array of failure times.
    :return: _mhb; the MIL-HDBK test statistic
    :rtype: float
    """

    _T = max(times)
    _mhb = -2.0 * sum([log(t / _T) for t in times])

    return _mhb


def laplace(times, n_failures):
    """
    Function to calculate the Laplace statistic for trend.  The test statistic
    is calculated as follows:

        Zlp = (SUM[t / T] - N / 2) / SQRT(N / 12)

    where T is the maximum failure time in the data set and N is the total
    number of failures observed.

    The null hypothesis is rejected if the statistic exceeds the critical value
    for a chosen significance level.

    :param numpy array times: an array of failure times.
    :param int n_failures: the total number of failures.
    :return: _zlp; the Laplace test statistic
    :rtype: float
    """

    _T = max(times)
    _zlp = (sum([(t / _T) for t in times]) - n_failures / 2.0) / \
           sqrt(n_failures / 12.0)

    return _zlp


def lewis_robinson(times, n_failures):
    """
    Function to calculate the Lewis-Robinson statistic for trend.  The test
    statistic is calculated as follows:

        Zlr = Zlp * Tau / S

    where Zlp is the Laplace statistic, Tau is the mean interarrival time, and
    S is the standard error of the interarrival times.

    The null hypothesis is rejected if the statistic exceeds the critical value
    for a chosen significance level.

    :param times: an array of failure times,
    :type times: numpy array
    :param int n_failures: the total number of failures.
    :return: _zlr; the Lewis-Robinson test statistic
    :rtype: float
    """

    # Calculate the Laplace statistic.
    _zlp = laplace(times, n_failures)

    # Find the interarrival times.  We need to add a zero to the times array
    # to get the first interarrival time.
    _tbf = np.diff(np.insert(times, 0, 0))

    # Calculate the statistic.
    _zlr = _zlp * np.mean(_tbf) / np.std(_tbf)

    return _zlr


def serial_correlation(times, n_failures, k=1):
    """
    Function to calculate the serial correlation coefficient to test for
    independent interarrival times.  The test statistic is calculated as
    follows:

        rhok = SUM[(t_j - t_bar)(t_j+k - t_bar)] / SQRT(SUM[(t_j - t_bar)^2] * SUM[(t_j+k - t_bar)^2])

    where t_bar is mean interarrival time, N is the total number of failures,
    and k is the order of the serial-correlation.  The sums are over the range
    j = 1 to N - k.

    The null hypothesis is rejected if the statistic exceeds the critical value
    for a chosen significance level.

    :param times: an array of failure times,
    :type times: numpy array
    :param int n_failures: the total number of failures.
    :param int k: the desired order of the serial-correlation.
    :return: _rho; the serial-correlation coefficient.
    :rtype: float
    """

    # Find the interarrival times.  We need to add a zero to the times array
    # to get the first interarrival time.
    _tbf = np.diff(np.insert(times, 0, 0))
    _r = len(_tbf)

    _t_bar = np.mean(_tbf)

    _temp1 = [t - _t_bar for t in _tbf[:_r - k]]
    _temp2 = [t - _t_bar for t in _tbf[k:]]
    _numerator = sum([_temp1[i] * _temp2[i] for i, __ in enumerate(_temp1)])

    _temp1 = sum([(t - _t_bar)**2.0 for t in _tbf[:_r - k]])
    _temp2 = sum([(t - _t_bar)**2.0 for t in _tbf[k:]])

    try:
        _rho = sqrt(n_failures - k) * _numerator / sqrt(_temp1 * _temp2)
    except ZeroDivisionError:
        _rho = 0.0

    return _rho
