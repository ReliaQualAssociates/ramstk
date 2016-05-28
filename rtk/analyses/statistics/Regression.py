#!/usr/bin/env python
"""
Contains functions for performing regression analysis.
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.statistics.Regression.py is part of The RTK Project
#
# All rights reserved.

# Import modules for mathematics.
import numpy as np
from scipy.stats import norm                # pylint: disable=E0611
import scipy.optimize as optim

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


def _error_function(param, x_vals, y_vals):
    """
    The error function to use with the lestsq method in scipy.optimize.

    :param list of floats param: current estimates of the intercept and slope
                                 for the least squares line.
    :param list of floats x_vals: the x-values at which to calculate the
                                  residuals.
    :param list of floats y_vals: the observed y-value at x.
    :return: _residuals
    :rtype: list of floats
    """

    _residuals = (param[0] + param[1] * x_vals) - y_vals

    return _residuals


def adjusted_rank(data):
    """
    Function to calculate adjusted ranks for data sets containing censored
    data.

    :param ndarray data: the data set to calculate adjusted ranks for.
                         * 0 - left of the observation time interval
                         * 1 - right of the observation time interval
                         * 2 - number of events occurring at the observation
                               time
                         * 3 - status, where status is:
                            * 1 - event
                            * 2 - right censored
                            * 3 - interval censored
    :return: _adjusted_rank
    :rtype: ndarray
    """

    # Initialize some local variables.
    _adjusted_rank = []
    _prev_adj_rank = 0
    _n_failures = len(data)
    _rev_rank = _n_failures

    for _record in data:
        if _record[3] != 1:
            _adj_rank = -1
        else:
            _adj_rank = (_rev_rank * 1.0 * _prev_adj_rank +
                         (_n_failures + 1)) / (_rev_rank + 1)
            _prev_adj_rank = _adj_rank

        _adjusted_rank.append(_adj_rank)
        _rev_rank -= 1

    return np.array(_adjusted_rank, dtype=float)


def bernard_ranks(data, grouped=False):
    """
    Function to calculate Bernard's approximation of median ranks.

    :param ndarray data: the data set to fit.  This is a numpy array where
                         each record contains the following, in order:
                            * 0 = Interval start time
                            * 1 = Interval end time
                            * 2 = Quantity of observations
                            * 3 = Status of observation, where status is:
                                    * 1 - event
                                    * 2 - right censored
                                    * 3 - left censored
                                    * 4 - interval censored
                            * 4 = Time between failures or interarrival
                                  time
    :param bool grouped: indicates whether the data is grouped or exact.
    :return: _mr; the median ranks.
    :rtype: ndarray of floats
    """

    # Initialize local variables.
    _mr = []

    # Calculate the adjusted ranks to account for suspended data.
    _adj_rank = np.asmatrix(adjusted_rank(data)).T
    _cum_failures = np.asmatrix(np.cumsum(data[:, 2])).T
    _data = np.concatenate((data, _adj_rank, _cum_failures), axis=1)

    if not grouped:
        _n_failures = len(data)
        _status = 1
    else:
        _n_failures = _cum_failures[-1, 0]
        _status = 3

    # Calculate Bernard's approximation.
    for _record in _data:
        if _record[0, 3] != _status:
            _mr.append(np.nan)
        else:
            _b_rank = (_record[0, 5] - 0.3) / (_n_failures + 0.4)
            _mr.append(_b_rank)

    return np.array(_mr, dtype=float)


def regression(data, start, end, dist='exponential'):  # pylint: disable=R0914
    """
    Function to fit data to a parametric distribution and find point estimates
    of the parameters using regression.  It is up to the calling function to
    calculate bounding values.

    :param ndarray data: the data set to fit.  This is a numpy array where
                             each record contains the following, in order:
                                * 0 = Interval start time
                                * 1 = Interval end time
                                * 2 = Quantity of observations
                                * 3 = Status of observation
                                * 4 = Time between failures or interarrival
                                      time
    :param float start: the minimum time to include in the fit.  Used to
                        exclude outliers.
    :param float end: the maximum time to include in the fit.  Used to exclude
                      outliers.
    :param str dist: the noun name of the distribution to fit.  Defaults to
                     the exponential distribution.
    :return: _fit; [[scale estimate, shape estimate, location estimate],
                    [scale variance, covariance, shape variance],
                    [MLE, AIC, BIC], correlation coeff.]
    :rtype: list
    """
# TODO: Re-write regression; current McCabe Complexity metric=15.
    # Initialize lists to hold results.
    _parameters = [0.0, 0.0, 0.0]           # Scale, shape, location.
    _variance = [0.0, 0.0, 0.0]             # Scale variance, covariance,
                                            # shape variance.
    _gof = [0.0, 0.0, 0.0]                  # MLE, AIC, BIC
    _rho_hat = 0.0                          # Correlation coefficient

    # Sort data by the right of the interval.  Remove records occurring before
    # the start time and after the end time.
    _data = sorted(data, key=lambda x: float(x[1]))
    _data = [_rec for _rec in _data if float(_rec[0]) >= start]
    _data = [_rec for _rec in _data if float(_rec[1]) <= end]
    _data = np.array(_data)

    # Count the number of suspensions, failures, and records.
    _n_suspensions = sum(x[2] for x in _data if x[3] == 2)
    _n_failures = sum(x[2] for x in _data
                      if x[3] == 1 or x[3] == 3 or x[3] == 4)
    _n_records = len(_data)

    # Retrieve the failure times for all non-censored data.
    _x = _data[np.where(_data[:, 3] == 1), 1]
    _x = np.array(_x.tolist()[0])

    # TODO: Move this to the View module.
    #if len(_x) == 0:
    #    Widgets.rtk_information(_(u"There are no single times-to-failure "
    #                            u"in your data set.  All of your "
    #                            u"observations are censored.  Rank "
    #                            u"regression methods cannot handle data "
    #                            u"sets containing only censored data.  It "
    #                            u"is recommended that you use maximum "
    #                            u"likelihood estimation (MLE) to fit this "
    #                            u"data set."))
    #    return False

    # Calculate median ranks.  This accounts for censored observations.
    _median_rank = bernard_ranks(_data)

    # Linearize the median ranks (probability of failure) depending on the
    # s-distribution.  Fit the linearized median ranks to a straight line using
    # the x-values from above as the independent variable.  Transform the
    # intercept and slope to the proper variable(s) for the distribution being
    # fit.  Finally, calculate the variance and covariance of the parameters.
    if dist == 'exponential':
        _df = _n_records - 1
        _y_linear = -1.0 * np.log(1.0 / (1.0 - _median_rank))

        _p, _covar, _info, __, __ = optim.leastsq(_error_function,
                                                  [1.0, 1.0],
                                                  args=(_x, _y_linear),
                                                  full_output=True)
        _parameters[0] = -_p[1]

    elif dist == 'lognormal':
        _df = _n_records - 2
        _x = np.log(_x)
        _y_linear = norm.ppf(_median_rank)

        _p, _covar, _info, __, __ = optim.leastsq(_error_function,
                                                  [1.0, 1.0],
                                                  args=(_x, _y_linear),
                                                  full_output=True)
        _parameters[1] = 1.0 / _p[1]
        _parameters[0] = -_p[0] * _parameters[1]

    elif dist == 'gaussian' or dist == 'normal':
        _df = _n_records - 2
        _y_linear = norm.ppf(_median_rank)

        _p, _covar, _info, __, __ = optim.leastsq(_error_function,
                                                  [1.0, 1.0],
                                                  args=(_x, _y_linear),
                                                  full_output=True)
        _parameters[1] = 1.0 / _p[1]
        _parameters[0] = -_p[0] * _parameters[1]

    elif dist == 'weibull':
        _df = _n_records - 2
        _x = np.log(_x)
        _y_linear = np.log(-1.0 * np.log((1.0 - _median_rank)))

        _p, _covar, _info, __, __ = optim.leastsq(_error_function,
                                                  [1.0, 1.0],
                                                  args=(_x, _y_linear),
                                                  full_output=True)
        _parameters[1] = _p[1]
        _parameters[0] = np.exp(-_p[0] / _p[1])

    _yhat = np.array([x for x in _info['fvec'] if np.logical_not(np.isnan(x))])

    # Calculate the variance and covariance of the parameters.
    _SSE = np.sum(_yhat**2.0)
    _MSE = _SSE / _df
    _cov = _MSE * _covar
    _variance[0] = _cov[1][1]               # Scale
    _variance[1] = _cov[0][1]               # Scale-Shape
    _variance[2] = _cov[0][0]               # Shape

    # Calculate the log-likelihood, AIC, and BIC.
    _s2b = _SSE / _n_records
    _gof[0] = -_n_records / 2.0 * np.log(2.0 * np.pi) - \
        _n_records / 2.0 * np.log(_s2b) - 1.0 / (2.0 * _s2b) * _SSE
    _gof[1] = -2.0 * _gof[0] + 2.0
    _gof[2] = -2.0 * _gof[0] + (np.log(_n_records) - np.log(np.pi))

    # Calculate the correlation coefficient (i.e., R)
    _rho_hat = np.corrcoef(_x, _y_linear)[0, 1]

    _fit = [_parameters, _variance, _gof, _rho_hat, _n_suspensions,
            _n_failures]

    return _fit


def rank_regression_y(x, y):                # pylint: disable=C0103
    """
    Function to perform rank regression on y.

    :param ndarray x: the x values at which the observations were made.
    :param ndarray y: the linearized survival values.  Linearization is
                      different for each s-distribution.
    :return: _a_hat, _b_hat; intercept and slope
    :rtype: tuple
    """

    # TODO: Write test for this function.

    # Calculate summations.
    _sum_x = np.sum(x)
    _sum_y = np.sum(y)
    _sum_x_sq = np.sum(x * x)
    _sum_xy = np.sum(x * y)

    _n_failures = np.size(x)

    # Calculate the slope and intercept of the regression line.
    _b_hat = (_sum_xy - (_sum_x * _sum_y / _n_failures)) / \
             (_sum_x_sq - (_sum_x**2.0 / _n_failures))
    _a_hat = (_sum_y / _n_failures) - (_b_hat * (_sum_x / _n_failures))

    return _a_hat, _b_hat
