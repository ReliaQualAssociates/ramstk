#!/usr/bin/env python
"""
Contains functions for performing non-parametric and parametric survival
analyses.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       survival.py is part of The RTK Project
#
# All rights reserved.

import sys
import inspect
from os import name

# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

# Add NLS support.
import gettext
_ = gettext.gettext

# Import mathematical functions.
import numpy as np
import scipy.integrate as integ
import scipy.misc as misc
import scipy.optimize as optim
import lifelines as nonpar
from scipy.stats import chi2, expon, exponweib, lognorm, norm, tvar
from math import ceil, exp, floor, log, sqrt

# Import other RTK modules.
try:
    import configuration as _conf
    import utilities as _util
except ImportError:
    import rtk.configuration as _conf
    import rtk.utilities as _util


# +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
# Following are the functions for mean cumulative function calculations.  #
# +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
def d_matrix(data, times):
    """
    Function to create d.(tk) array for use in calculating the mean cumulative
    function.  The d.(tk) array is the total number of system recurrences at
    time tk.

    :param data: a dictionary containing the failure/censoring data for a
                 population of systems.
    :type data: dictionary with the system id as the key and a list of the
                failure/censoring times as the value.
    :param times: a list of unique and sorted failures times.
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

    :param data: a dictionary containing the failure/censoring data for a
                 population of systems.
    :type data: dictionary with the system id as the key and a list of the
                failure/censoring times as the value.
    :param times: a list of unique and sorted failures times.
    :type times: list of floats
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

    :param data: a dictionary where the key is the system id and the value is a
                 list of failure/censoring times.  The last entry in this list
                 is the censoring time.  Failures times are float or integer
                 and the censoring time is a string.  For example:
                 [88., 92., 227., '350+']
    :type data: dictionary.
    :param conf: the confidence level of the MCF estimates (default is 75%).
    :type conf: float
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

    _diff_times = np.diff(_times)
    _times = np.matrix(_times).transpose().tolist()

    _mcf = np.concatenate((_times, _d_dot), axis=1)
    _mcf = np.concatenate((_mcf, _mu_hat_ll), axis=1)
    _mcf = np.concatenate((_mcf, _mu_hat), axis=1)
    _mcf = np.concatenate((_mcf, _mu_hat_ul), axis=1)

    return _mcf


def mcf_variance(delta, d, delta_dot, d_bar):
    """
    Function to calculate the variance of d(tk) for the MCF.

    :param delta: the matrix of indicator variables for operating systems.
    :type delta: numpy matrix
    :param d: the matrix of the number of system recurrences.
    :type d: numpy matrix
    :param delta_dot: an array containing the risk population at each observed
                      failure time.
    :type delta_dot: numpy array
    :param d_bar: an array containing the fraction of the risk population that
                  failed at each observed failure time.
    :type d_bar: numpy array
    :return: _variance_mu; an array containing the variance of the MCF at each
             observed failure time.
    :rtype: numpy array
    """

    _temp1 = np.divide(delta, delta_dot)
    _temp2 = np.subtract(d, d_bar)

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

    :param times: an array of failure times,
    :type times: numpy array
    :return: _mhb; the MIL-HDBK test statistic
    :rtype: float
    """

    _T = max(times)
    _mhb = -2.0 * sum([log(t / _T) for t in times])

    return _mhb


def laplace(times, N):
    """
    Function to calculate the Laplace statistic for trend.  The test statistic
    is calculated as follows:

        Zlp = (SUM[t / T] - N / 2) / SQRT(N / 12)

    where T is the maximum failure time in the data set and N is the total
    number of failures observed.

    The null hypothesis is rejected if the statistic exceeds the critical value
    for a chosen significance level.

    :param times: an array of failure times,
    :type times: numpy array
    :param N: the total number of failures.
    :type N: integer
    :return: _zlp; the Laplace test statistic
    :rtype: float
    """

    _T = max(times)

    _zlp = (sum([(t / _T) for t in times]) - N / 2.0) / sqrt(N / 12.0)

    return _zlp


def lewis_robinson(times, N):
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
    :param N: the total number of failures.
    :type N: integer
    :return: _zlr; the Lewis-Robinson test statistic
    :rtype: float
    """

    # Calculate the Laplace statistic.
    _zlp = laplace(times, N)

    # Find the interarrival times.  We need to add a zero to the times array
    # to get the first interarrival time.
    _tbf = np.diff(np.insert(times, 0, 0))

    # Calculate the statistic.
    _zlr = _zlp * np.mean(_tbf) / np.std(_tbf)

    return _zlr


def serial_correlation(times, N, k=1):
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
    :param N: the total number of failures.
    :type N: integer
    :param k: the desired order of the serial-correlation.
    :type k: integer
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

    _rho = sqrt(N - k) * _numerator / sqrt(_temp1 * _temp2)

    return _rho


# +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
# Following are the functions for Kaplan-Meier calculations.              #
# +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
def kaplan_meier(data, start, end, conf=0.75, conftype=3):
    """
    Function to calculate the Kaplan-Meier survival function estimates.

    :param array-like data: the data set to fit.  This is a list of tuples
                            where each tuple contains the following, in order:
                            * 0 = Observed unit ID
                            * 1 = Interval start time
                            * 2 = Interval end time
                            * 3 = Time between failures or interarrival time
                            * 4 = Status of observation
                            * 5 = Quantity of observations
                            * 6 = Date of observation
    :param float endtime: time at which to stop analysis (helps eliminate
                          stretched plots due to small number of events at
                          high hours).
    :param float conf: the confidence level of the KM estimates.
    :param int conftype: the confidence interval type for the KM estimates.
                         Confidence type is one of:
                         * 1 = lower one-sided
                         * 2 = upper one-sided
                         * 3 = two-sided (default)
    :return: _kaplan_meier; the matrix of results where each row in the matrix
             contains the following, in order:
             * Time of observation
             * Lower bound on S(t)
             * Point estimate of S(t)
             * Upper bound on S(t)
    :rtype: ndarray
    """

    _kmf = nonpar.KaplanMeierFitter(alpha=conf)

    # Sort data by the right if the interval.  Remove records occurring before
    # the start time and after the end time.
    _data = sorted(data, key=lambda x: (float(x[2]), float(x[1])))
    _data = [_rec for _rec in _data if float(_rec[1]) >= start]
    _data = [_rec for _rec in _data if float(_rec[2]) <= end]
    _data = np.array(_data)

    # Replace the string status with integer status.
    for _record in _data:
        if _record[4] == 'Right Censored' or _record[4] == '2':
            _record[4] = 0
        elif (_record[4] == 'Left Censored' or
              _record[4] == 'Interval Censored' or
              _record[4] == '3'):
            _record[4] = 3
        else:
            _record[4] = 1

    # Coerce the data set into the form necessary for fitting functions.
    _data = np.vstack((_data[:, 1], _data[:, 2], _data[:, 5], _data[:, 4]))
    _data = np.array(np.transpose(_data), dtype=float)

    # For those records with more than one observation, append the record
    # n - 1 times to the data set to account for the multiple observations.
    for _row in _data:
        if _row[2] > 1:
            for i in range(int(_row[2]) - 1):
                _data = np.vstack((_data, _row))

    # Adjust the interval-censored times so they can be passed to the
    # fit method.
    _interval_lt = _data[np.where(_data[:, 3] == 3)][:, 0]
    _interval_rt = _data[np.where(_data[:, 3] == 3)][:, 1]
    _interval_t = (_interval_lt + _interval_rt) / 2.0
    _data[np.where(_data[:, 3] == 3), 1] = _interval_t
    _data[np.where(_data[:, 3] == 3), 3] = 1

    # Estimate the Kaplan-Meier survival function.
    _fit = _kmf.fit(_data[:, 1], event_observed=_data[:, 3])
    _kaplan_meier = np.vstack((np.unique(_fit.durations),
                               _fit.confidence_interval_.values[1:, 1],
                               _fit.survival_function_.values[1:, 0],
                               _fit.confidence_interval_.values[1:, 0]))
    _kaplan_meier = np.transpose(_kaplan_meier)

    _r = np.where(_fit.event_observed == 1)[0] + 1

    return _kaplan_meier, _r


def kaplan_meier_mean(data, rank, conf=0.75):
    """
    Function to calculate the MTBF from a Kaplan-Meier data set.  This function
    uses the algorithm found in Lee and Wang, "Statistical Methods for Survival
    Data Analysis", page 74.

    :param ndarray data: the Kaplan-Meier data set.  This is a matrix where each row
                 contains the following, in order:
              * Time point (t) at which the curve has a step.
              * Number of subjects at risk at time t.
              * Number of events that occur at time t.
              * Standard error of the survival function at time t.
              * Lower bound on the survival function at time t.
              * Point estimate of the survival function at time t.
              * Upper bound on the survival function at time t.
    :param float conf: the desired confidence for the bounding values.
    :return: _mtbf; matrix of mean values where each row contains the
             following, in order:
              * Lower bound on the mean value.
              * Point estimate of the mean value.
              * Upper bound on the mean value.
              * Variance of the mean value.
    :rtype: list of lists
    """

    # Determine the confidence bound z-value.
    _z_norm = norm.ppf(conf)

    _x = np.insert(np.diff(data[:, 2]), 0, 1)

    _failures = data[np.where(_x != 0)]
    _indices =  np.where(_x != 0)

    _A = _failures[:-1, 2] * (_failures[1:, 0] - _failures[:-1, 0])
    _mtbf = np.sum(_A) + _failures[0, 0]

    _N = max(rank)
    _rank = [_N - r for r in rank][:len(_A)]

    _var = np.sum(_A**2. / _rank)
    _mtbf_ll = _mtbf - sqrt(_var) * _z_norm
    _mtbf_ul = _mtbf + sqrt(_var) * _z_norm

    return _mtbf_ll, _mtbf, _mtbf_ul


def kaplan_meier_hazard(data):
    """
    Function to calculate the Kaplan-Meier cumulative hazard rate, hazard rate,
    and log hazard rate.  This function uses the algorithm found in
    Peterson "Expressing the Kaplan-Meier estimator as a function of empirical
    subsurvival functions." Journal of the American Statistical Association
    1977;72:854-858.

    :param ndarray data: the Kaplan-Meier data set.  This is a matrix where each row
                 contains the following, in order:
                 - Time point (t) at which the curve has a step.
                 - Number of subjects at risk at time t.
                 - Number of events that occur at time t.
                 - Standard error of the survival function at time t.
                 - Lower bound on the survival function at time t.
                 - Point estimate of the survival function at time t.
                 - Upper bound on the survival function at time t.
    :type data: numpy matrix
    :return: _hazard; matrix of hazard function related results.  There is one
             row for each observation time where each row contains the
             following, in order:
             - Lower bound on the hazard rate.
             - Point estimate of the hazard rate.
             - Upper bound on the hazard rate.
             - Lower bound on the cumulative hazard rate.
             - Point estimate of the cumulative hazard rate.
             - Upper bound on the cumulative hazard rate.
             - Lower bound on the logarithm of the cum. hazard rate.
             - Point estimate of the logarithm of the cum. hazard rate.
             - Upper bound on the logarithm of the cum. hazard rate.
    :rtype: numpy matrix
    """

    _times = data[:, 0]

    # Cumulative hazard rates.
    _H_ll = -np.ma.log(data[:, 1])
    _H = -np.ma.log(data[:, 2])
    _H_ul = -np.ma.log(data[:, 3])

    # Log cumulative hazard rates.
    _logH_ll = np.ma.log(_H_ll)
    _logH = np.ma.log(_H)
    _logH_ul = np.ma.log(_H_ul)

    # Calculate the hazard rates.
    _h_ll = np.ma.divide(_H_ll, _times)
    _h = np.ma.divide(_H, _times)
    _h_ul = np.ma.divide(_H_ul, _times)

    # Combine the results together into a single numpy matrix.
    _hazard = np.vstack((_h_ll, _h, _h_ul,
                         _H_ll, _H, _H_ul,
                         _logH_ll, _logH, _logH_ul))

    return _hazard


def turnbull_s(_tau_):
    """

    Keyword Arguments:
    _tau_ --
    """

    m = len(_tau_)
    _status_ = []

    for i in range(m - 1):
        _status_.append(1)

    #survival = importr('survival')

    #_times_ = robjects.FloatVector(_tau_[:m-1])
    #_status_ = robjects.IntVector(_status_)

    #_surv_ = survival.Surv(_times_, _status_)
    #robjects.globalenv['surv'] = _surv_
    #_ekm_ = survival.survfit(robjects.Formula('surv ~ 1'))

    _So_ = []
    #for i in range(len(_ekm_[5])):
    #    _So_.append(_ekm_[5][i])

    _p_ = []
    for i in range(len(_So_) - 1):
        _p_.append([_So_[i] - _So_[i + 1]])

    return(_p_)


def interv(x, inf, sup):

    if(x[0] >= inf and x[1] <= sup):
        _interv_ = 1
    else:
        _interv_ = 0

    return(_interv_)


def turnbull_A(_dataset_, _tau_):

    _tau2_ = []
    _A_ = []

    _n_records_ = len(_dataset_)

    _left_ = _tau_[:-1]
    _right_ = _tau_[1:]
    for i in range(_n_records_):
        _idx_start_ = _tau_.index(_dataset_[i][0])
        _idx_stop_ = _tau_.index(_dataset_[i][1]) - 1

        _a_ = [0]*(len(_left_) - 1)
        for j in range(_idx_start_, _idx_stop_):
            _a_[j] = 1

        if((_idx_stop_ - _idx_start_) == 0):
            _a_[_idx_start_] = 1

        _A_.append(_a_)

    return(_A_)


def turnbull(_dataset_, _reltime_, _conf_=0.75, eps=1E-13, iter_max=200):
    """
    Keyword Arguments:
    _dataset_ --
    _conf_    -- the confidence level of the estimates.
    """

    from numpy import amax, array, matrix

    _l_ = [i[0] for i in _dataset_]
    _r_ = [i[1] for i in _dataset_]
    _tau_ = list(set(_l_+_r_))
    _p_ = matrix(turnbull_s(_tau_))
    _A_ = matrix(turnbull_A(_dataset_, _tau_))

    _n_ = len(_dataset_)
    _m_ = len(_tau_) - 1
    _Q_ = matrix([1]*_m_)

    i = 0
    _maxdiff_ = 1
    while(_maxdiff_ >= eps and i < iter_max):

        i += 1
        _diff_ = _Q_ - _p_
        _maxdiff_ = amax(_diff_)

        _Q_ = _p_
        _C_ = _A_ * _p_
        _invC_ = matrix([1.0 / i for i in array(_C_)])
        x = (_A_.T * _invC_) / _n_
        try:
            _p_ = _p_ * x
        except ValueError:
            print i, len(_p_), len(x)

    #surv = round(c(1, 1-cumsum(_p_)), digits=5)
    #right = data$right

    #if(any(!(is.finite(right))))
    #    t <- max(right[is.finite(right)])
    #    return(list(time=tau[tau<t],surv=surv[tau<t]))
    #else
    #    return(list(time=tau,surv=surv))

    return


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
            _adj_rank = (_rev_rank * 1.0 * _prev_adj_rank + \
                         (_n_failures + 1)) / (_rev_rank + 1)
            _prev_adj_rank = _adj_rank

        _adjusted_rank.append(_adj_rank)
        _rev_rank -= 1

    return np.array(_adjusted_rank, dtype =float)


def bernard_ranks(data, grouped=False):
    """
    Function to calculate Bernard's approximation of median ranks.

    :param ndarray data: the data to calculate median ranks for.
                         * 0 - left of the observation time interval
                         * 1 - right of the observation time interval
                         * 2 - number of events occurring at the observation
                               time
                         * 3 - status, where status is:
                            * 1 - event
                            * 2 - right censored
                            * 3 - interval censored
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
        _col = 4
        _status = 1
    else:
        _n_failures = _cum_failures[-1, 0]
        _col = 5
        _status = 3

    # Calculate Bernard's approximation.
    for _record in _data:
        if _record[0, 3] != _status:
            _mr.append(np.nan)
        else:
            _b_rank = (_record[0, _col] - 0.3) / (_n_failures + 0.4)
            _mr.append(_b_rank)

    return np.array(_mr, dtype=float)


def rank_regression_y(x, y):
    """
    Function to perform rank regression on y.

    :param ndarray x: the x values at which the observations were made.
    :param ndarray y: the linearized survival values.  Linearization is
                      different for each s-distribution.
    :return: _a_hat, _b_hat; intercept and slope
    :rtype: tuple
    """

    # Calculate summations.
    _sum_x = np.sum(x)
    _sum_y = np.sum(y)
    _sum_x_sq = np.sum(x * x)
    _sum_xy = np.sum(x * y)

    _n_failures = np.size(x)

    # Calculate the slope and intecept of the regression line.
    _b_hat = (_sum_xy - (_sum_x * _sum_y / _n_failures)) / \
             (_sum_x_sq - (_sum_x**2.0 / _n_failures))
    _a_hat = (_sum_y / _n_failures) - (_b_hat * (_sum_x / _n_failures))

    return _a_hat, _b_hat


def fisher_information(model, p0, X, noise=1.0):
    """
    Function to calculate the Fisher information matrix for model sampled on
    grid X with parameters p0. Assumes samples are not correlated and have
    equal variance noise^2.

    :param callable model: the model function, f(x, ...). It must take the
                           independent variable as the first argument and the
                           parameters as separate remaining arguments.
    :param list p0: point in parameter space where Fisher information matrix is
                    evaluated.  Passed as:
                    [scale, shape, location]
    :param ndarray X: the data set to use for calculating the information
                      matrix.
    :param float noise: squared variance of the noise in data.
    :returns: _fisher; the Fisher information matrix.
    :rtype: ndarray
    """

    labels = inspect.getargspec(model)[0][1:]
    p0dict = dict(zip(inspect.getargspec(model)[0][1:], p0))

    D = np.zeros((len(p0), X.size))

    for i, argname in enumerate(labels):
        D[i,:] = [misc.derivative(
                            lambda p: model(x, **dict(p0dict, **{argname: p})),
                            p0dict[argname],
                            dx=1.0e-6)
                  for x in X ]

    _fisher = 1.0 / noise**2 * np.einsum('mk, nk', D, D)

    return _fisher


def exponential_log_pdf(data, x):
    """
    Function to calculate the logarithm of the exponential probability density
    function (pdf).

    :param ndarray data: the data points at which to calculate the logarithm of
                         the pdf.
    :param float x: the value of the scale parameter.
    :return: the value(s) of the logarithm of the pdf.
    :rtype: ndarray
    """

    return np.log(x) - x * data


def exponential_log_likelihood(x, data):
    """
    Function to calculate the value of the log likelihood function for the
    exponential distribution.

    :param float x: the parameter values at which to evaluate the
                    log-likelihood.
    :param ndarray data: the data set to calculate the log-likelihood for.
                         * 0 - left of the observation time interval
                         * 1 - right of the observation time interval
                         * 2 - number of events occurring at the observation
                               time
                         * 3 - status, where status is:
                            * 1 - event
                            * 2 - right censored
                            * 3 - interval censored
    """

    # Calculate the value of the log-likelihood for the event observations.
    _event_t = data[np.where(data[:, 3] == 1)][:, 1]
    _event_n = data[np.where(data[:, 3] == 1)][:, 2]
    _event_ll = np.sum(_event_n * np.log((x[0] * np.exp(-x[0] * _event_t))))

    # Calculate the value of the log-likelihood for the right-censored
    # observations.
    _right_t = data[np.where(data[:, 3] == 2)][:, 1]
    _right_n = data[np.where(data[:, 3] == 2)][:, 2]
    _right_ll = np.sum(_right_n * x[0] * _right_t)

    # Calculate the value of the log-likelihood for the left- and interval-
    # censored observations.
    _interval_lt = data[np.where(data[:, 3] == 3)][:, 0]
    _interval_rt = data[np.where(data[:, 3] == 3)][:, 1]
    _interval_n = data[np.where(data[:, 3] == 3)][:, 2]

    _interval_ll = np.sum(_interval_n * \
                          np.log(np.exp(-x[0] * _interval_lt) - \
                                 np.exp(-x[0] * _interval_rt)))

    _logLik = _event_ll - _right_ll + _interval_ll

    return _logLik


def exponential_partial_derivs(theta, data):
    """
    Function to calculate the value of the partial derivative of the
    exponential log-likelihood function with respect to theta.  This function
    is passed as an argument to scipy.optimize.fsolve() to find the value of
    theta that minimizes the partial.

    :param float theta: the scale parameter value at which to evaluate the
                        partial derivative.
    :param ndarray data: the data set to calculate the log-likelihood for.
                         * 0 - left of the observation time interval
                         * 1 - right of the observation time interval
                         * 2 - number of events occurring at the observation
                               time
                         * 3 - status, where status is:
                            * 1 - event
                            * 2 - right censored
                            * 3 - interval censored
    """

    # Calculate the value of the log-likelihood for the event observations.
    _event_t = data[np.where(data[:, 3] == 1)][:, 1]
    _event_n = data[np.where(data[:, 3] == 1)][:, 2]
    _event_ll = np.sum(_event_n * ((1.0 / theta) - _event_t))

    # Calculate the value of the log-likelihood for the right-censored
    # observations.
    _right_t = data[np.where(data[:, 3] == 2)][:, 1]
    _right_n = data[np.where(data[:, 3] == 2)][:, 2]
    _right_ll = np.sum(_right_n * _right_t)

    # Calculate the value of the log-likelihood for the left- and interval-
    # censored observations.  Use the midpoint of the interval as an
    # approximation.
    _interval_lt = data[np.where(data[:, 3] == 3)][:, 0]
    _interval_rt = data[np.where(data[:, 3] == 3)][:, 1]
    _interval_t = (_interval_lt + _interval_rt) / 2.0
    _interval_n = data[np.where(data[:, 3] == 3)][:, 2]

    _interval_ll = np.sum(_interval_n * ((1.0 / theta) - _interval_t))

    # Following are the exact equations for the interval censored observations.
    #_n = (_interval_lt * exp(-theta * _interval_lt)) - \
    #     (_interval_rt * exp(-theta * _interval_rt))
    #_d = exp(-theta * _interval_lt) - exp(-theta * _interval_rt)
    #_interval_ll = np.sum(_interval_n * (_n / _d))

    _del_theta = _event_ll - _right_ll - _interval_ll

    return _del_theta


def lognormal_log_pdf(data, mu, sigma):
    """
    Function to calculate the logarithm of the lognormal probability density
    function (pdf).

    :param ndarray data: the data points at which to calculate the logarithm of
                         the pdf.
    :param float mu: the value of the scale parameter.
    :param float sigma: the value of the shape parameter.
    :return: the value(s) of the logarithm of the pdf.
    :rtype: ndarray
    """

    _log_pdf = (1.0 / sigma * np.sqrt(2.0 * np.pi)) - \
               (0.5 * ((np.log(data) - mu) / sigma)**2.0)

    return _log_pdf


def lognormal_log_likelihood(x, data):
    """
    Function to calculate the value of the log likelihood function for the
    lognormal distribution.

    :param float x: the parameter values at which to evaluate the
                    log-likelihood.
    :param ndarray data: the data set to calculate the log-likelihood for.
                         * 0 - left of the observation time interval
                         * 1 - right of the observation time interval
                         * 2 - number of events occurring at the observation
                               time
                         * 3 - status, where status is:
                            * 1 - event
                            * 2 - right censored
                            * 3 - interval censored
    """

    # Calculate the value of the log-likelihood for the event observations.
    _event_t = data[np.where(data[:, 3] == 1)][:, 1]
    _event_n = data[np.where(data[:, 3] == 1)][:, 2]
    _event_ll = np.sum(_event_n * \
                       np.log((1.0 / (_event_t * x[1])) * \
                              norm.pdf((np.log(_event_t) - x[0]) / x[1])))

    # Calculate the value of the log-likelihood for the right-censored
    # observations.
    _right_t = data[np.where(data[:, 3] == 2)][:, 1]
    _right_n = data[np.where(data[:, 3] == 2)][:, 2]
    _right_ll = np.sum(_right_n * \
                       (1.0 - norm.cdf((np.log(_right_t) - x[0]) / x[1])))

    # Calculate the value of the log-likelihood for the left- and interval-
    # censored observations.
    _interval_lt = data[np.where(data[:, 3] == 3)][:, 0]
    _interval_rt = data[np.where(data[:, 3] == 3)][:, 1]
    _interval_n = data[np.where(data[:, 3] == 3)][:, 2]

    _interval_ll = np.sum(_interval_n * \
                    np.log(norm.cdf((np.log(_interval_rt) - x[0]) / x[1]) - \
                           norm.cdf((np.log(_interval_lt) - x[0]) / x[1])))

    _logLik = _event_ll - _right_ll + _interval_ll

    return _logLik


def lognormal_partial_derivs(x, data):
    """
    Function to calculate the value of the partial derivatives of the lognormal
    log-likelihood function with respect to mu and sigma.  This function is
    passed as an argument to scipy.optimize.fsolve() to find the value of mu
    and sigma that simultaneously minimizes the partials.

    :param list x: the values of mu and sigma at which to calculate the
                   partials.
    :param ndarray data: the data set to calculate the partials for.
                         * 0 - left of the observation time interval
                         * 1 - right of the observation time interval
                         * 2 - number of events occurring at the observation
                               time
                         * 3 - status, where status is:
                            * 1 - event
                            * 2 - right censored
                            * 3 - interval censored
    """

    # Calculate the value of the log-likelihood for the event observations.
    _event_t = data[np.where(data[:, 3] == 1)][:, 1]
    _event_n = data[np.where(data[:, 3] == 1)][:, 2]
    _event_sigma = np.sum(_event_n *
                          (((_event_t - x[0]) / x[1]**3.0) - (1.0 / x[1])))
    _event_mu = (1.0 / x[1]**2.0) * np.sum(_event_n * (_event_t - x[0]))

    # Calculate the value of the log-likelihood for the right-censored
    # observations.
    _right_t = data[np.where(data[:, 3] == 2)][:, 1]
    _right_n = data[np.where(data[:, 3] == 2)][:, 2]

    _norm = (_right_t - x[0]) / x[1]
    _cdf = norm.cdf(_norm)
    _right_mu = (1.0 / x[1]) * \
                np.sum(_right_n * (norm.pdf(_norm) / (1.000000001 - _cdf)))
    _right_sigma = (1.0 / x[1]) * \
                   np.sum(_right_n * \
                          ((_norm * norm.pdf(_norm)) / (1.000000001 - _cdf)))

    # Calculate the value of the log-likelihood for the left- and interval-
    # censored observations.  Use the midpoint of the interval as an
    # approximation.
    _interval_lt = data[np.where(data[:, 3] == 3)][:, 0]
    _interval_rt = data[np.where(data[:, 3] == 3)][:, 1]
    _interval_t = (_interval_lt + _interval_rt) / 2.0
    _interval_n = data[np.where(data[:, 3] == 3)][:, 2]

    _interval_sigma = np.sum(_interval_n * \
                             (((_interval_t - x[0]) / x[1]**3.0) - \
                              (1.0 / x[1])))
    _interval_mu = (1.0 / x[1]**2.0) * \
                   np.sum(_interval_n * (_interval_t - x[0]))

    # Following are the exact equations for the interval censored observations.
    #_norm_r = (_interval_rt - x[0]) / x[1]
    #_pdf_r = norm.pdf(_norm_r)
    #_cdf_r = norm.cdf(_norm_r)

    #_norm_l = (_interval_lt - x[0]) / x[1]
    #_pdf_l = norm.pdf(_norm_l)
    #_cdf_l = norm.cdf(_norm_l)

    #_n = _pdf_r - _pdf_l
    #_d = _cdf_r - _cdf_l
    #_interval_mu = (1.0 / x[1]) * np.sum(_interval_n * _n / _d)

    #_n = (_norm_r * _pdf_r) - (_norm_l * _pdf_l)
    #_interval_sigma = (1.0 / x[1]) * np.sum(_interval_n * _n / _d)

    _del_mu = _event_mu + _right_mu - _interval_mu
    _del_sigma = _event_sigma + _right_sigma - _interval_sigma

    return _del_mu, _del_sigma


def gaussian_log_pdf(data, mu, sigma):
    """
    Function to calculate the logarithm of the Gaussian probability density
    function (pdf).

    :param ndarray data: the data points at which to calculate the logarithm of
                         the pdf.
    :param float mu: the value of the scale parameter.
    :param float sigma: the value of the shape parameter.
    :return: the value(s) of the logarithm of the pdf.
    :rtype: ndarray
    """

    _log_pdf = (1.0 / sigma * np.sqrt(2.0 * np.pi)) - \
               (0.5 * ((data - mu) / sigma)**2.0)

    return _log_pdf


def gaussian_log_likelihood(x, data):
    """
    Function to calculate the value of the log likelihood function for the
    Gaussian distribution.

    :param float x: the parameter values at which to evaluate the
                    log-likelihood.
    :param ndarray data: the data set to calculate the log-likelihood for.
                         * 0 - left of the observation time interval
                         * 1 - right of the observation time interval
                         * 2 - number of events occurring at the observation
                               time
                         * 3 - status, where status is:
                            * 1 - event
                            * 2 - right censored
                            * 3 - interval censored
    """

    # Calculate the value of the log-likelihood for the event observations.
    _event_t = data[np.where(data[:, 3] == 1)][:, 1]
    _event_n = data[np.where(data[:, 3] == 1)][:, 2]
    _event_ll = np.sum(_event_n * \
                       np.log((1.0 / (_event_t * x[1])) * \
                              norm.pdf((_event_t - x[0]) / x[1])))

    # Calculate the value of the log-likelihood for the right-censored
    # observations.
    _right_t = data[np.where(data[:, 3] == 2)][:, 1]
    _right_n = data[np.where(data[:, 3] == 2)][:, 2]
    _right_ll = np.sum(_right_n * \
                       (1.0 - norm.cdf((_right_t - x[0]) / x[1])))

    # Calculate the value of the log-likelihood for the left- and interval-
    # censored observations.
    _interval_lt = data[np.where(data[:, 3] == 3)][:, 0]
    _interval_rt = data[np.where(data[:, 3] == 3)][:, 1]
    _interval_n = data[np.where(data[:, 3] == 3)][:, 2]

    _interval_ll = np.sum(_interval_n * \
                    np.log(norm.cdf((_interval_rt - x[0]) / x[1]) - \
                           norm.cdf((_interval_lt - x[0]) / x[1])))

    _logLik = _event_ll - _right_ll + _interval_ll

    return _logLik


def gaussian_partial_derivs(x, data):
    """
    Function to calculate the value of the partial derivatives of the Gaussian
    log-likelihood function with respect to mu and sigma.  This function is
    passed as an argument to scipy.optimize.fsolve() to find the value of mu
    and sigma that simultaneously minimizes the partials.

    :param list x: the values of mu and sigma at which to calculate the
                   partials.
    :param ndarray data: the data set to calculate the partials for.
                         * 0 - left of the observation time interval
                         * 1 - right of the observation time interval
                         * 2 - number of events occurring at the observation
                               time
                         * 3 - status, where status is:
                            * 1 - event
                            * 2 - right censored
                            * 3 - interval censored
    """

    # Calculate the value of the log-likelihood for the event observations.
    _event_t = data[np.where(data[:, 3] == 1)][:, 1]
    _event_n = data[np.where(data[:, 3] == 1)][:, 2]
    _event_sigma = np.sum(_event_n *
                          (((_event_t - x[0]) / x[1]**3.0) - (1.0 / x[1])))
    _event_mu = (1.0 / x[1]**2.0) * np.sum(_event_n * (_event_t - x[0]))

    # Calculate the value of the log-likelihood for the right-censored
    # observations.
    _right_t = data[np.where(data[:, 3] == 2)][:, 1]
    _right_n = data[np.where(data[:, 3] == 2)][:, 2]

    _norm = (_right_t - x[0]) / x[1]
    _cdf = norm.cdf(_norm)
    _right_mu = (1.0 / x[1]) * \
                np.sum(_right_n * (norm.pdf(_norm) / (1.000000001 - _cdf)))
    _right_sigma = (1.0 / x[1]) * \
                   np.sum(_right_n * \
                          ((_norm * norm.pdf(_norm)) / (1.000000001 - _cdf)))

    # Calculate the value of the log-likelihood for the left- and interval-
    # censored observations.  Use the midpoint of the interval as an
    # approximation.
    _interval_lt = data[np.where(data[:, 3] == 3)][:, 0]
    _interval_rt = data[np.where(data[:, 3] == 3)][:, 1]
    _interval_t = (_interval_lt + _interval_rt) / 2.0
    _interval_n = data[np.where(data[:, 3] == 3)][:, 2]

    _interval_sigma = np.sum(_interval_n * \
                             (((_interval_t - x[0]) / x[1]**3.0) - \
                              (1.0 / x[1])))
    _interval_mu = (1.0 / x[1]**2.0) * \
                   np.sum(_interval_n * (_interval_t - x[0]))

    # Following are the exact equations for the interval censored observations.
    #_norm_r = (_interval_rt - x[0]) / x[1]
    #_pdf_r = norm.pdf(_norm_r)
    #_cdf_r = norm.cdf(_norm_r)

    #_norm_l = (_interval_lt - x[0]) / x[1]
    #_pdf_l = norm.pdf(_norm_l)
    #_cdf_l = norm.cdf(_norm_l)

    #_n = _pdf_r - _pdf_l
    #_d = _cdf_r - _cdf_l
    #_interval_mu = (1.0 / x[1]) * np.sum(_interval_n * _n / _d)

    #_n = (_norm_r * _pdf_r) - (_norm_l * _pdf_l)
    #_interval_sigma = (1.0 / x[1]) * np.sum(_interval_n * _n / _d)

    _del_mu = _event_mu + _right_mu - _interval_mu
    _del_sigma = _event_sigma + _right_sigma - _interval_sigma

    return _del_mu, _del_sigma


def weibull_log_pdf(data, eta, beta):
    """
    Function to calculate the logarithm of the Weibull probability density
    function (pdf).

    :param ndarray data: the data points at which to calculate the logarithm of
                         the pdf.
    :param float x: the value of the scale parameter.
    :return: the value(s) of the logarithm of the pdf.
    :rtype: ndarray
    """

    _log_pdf = np.log(beta / eta) + \
               (beta - 1.0) * np.log(data / eta) - (data / eta)**beta

    return _log_pdf


def weibull_log_likelihood(x, data):
    """
    Function to calculate the value of the log likelihood function for the
    Weibull distribution.

    :param float x: the parameter values at which to evaluate the
                    log-likelihood.
    :param ndarray data: the data set to calculate the log-likelihood for.
                         * 0 - left of the observation time interval
                         * 1 - right of the observation time interval
                         * 2 - number of events occurring at the observation
                               time
                         * 3 - status, where status is:
                            * 1 - event
                            * 2 - right censored
                            * 3 - interval censored
    """

    # Calculate the value of the log-likelihood for the event observations.
    _event_t = data[np.where(data[:, 3] == 1)][:, 1]
    _event_n = data[np.where(data[:, 3] == 1)][:, 2]
    _event_ll = np.sum(_event_n * np.log((x[1] / x[0]) * \
                                         (_event_t / x[0])**(x[1] - 1.0) * \
                                         np.exp(-(_event_t / x[0])**x[1])))

    # Calculate the value of the log-likelihood for the right-censored
    # observations.
    _right_t = data[np.where(data[:, 3] == 2)][:, 1]
    _right_n = data[np.where(data[:, 3] == 2)][:, 2]
    _right_ll = np.sum(_right_n * np.log((_right_t / x[0])**x[1]))

    # Calculate the value of the log-likelihood for the left- and interval-
    # censored observations.
    _interval_lt = data[np.where(data[:, 3] == 3)][:, 0]
    _interval_rt = data[np.where(data[:, 3] == 3)][:, 1]
    _interval_n = data[np.where(data[:, 3] == 3)][:, 2]

    _interval_ll = np.sum(_interval_n * \
                          np.log(np.exp(-(_interval_lt / x[0])**x[1]) - \
                          np.exp(-(_interval_rt / x[0])**x[1])))

    _logLik = _event_ll - _right_ll + _interval_ll

    return _logLik


def weibull_partial_derivs(x, data):
    """
    Function to calculate the value of the partial derivatives of the Weibull
    log-likelihood function with respect to eta and beta.  This function is
    passed as an argument to scipy.optimize.fsolve() to find the value of eta
    and beta that simultaneously minimizes the partials.

    :param list x: the values of eta and beta at which to calculate the
                   partials.
    :param ndarray data: the data set to calculate the partials for.
                         * 0 - left of the observation time interval
                         * 1 - right of the observation time interval
                         * 2 - number of events occurring at the observation
                               time
                         * 3 - status, where status is:
                            * 1 - event
                            * 2 - right censored
                            * 3 - interval censored
    """

    # Calculate the value of the log-likelihood for the event observations.
    _event_t = data[np.where(data[:, 3] == 1)][:, 1]
    _event_n = data[np.where(data[:, 3] == 1)][:, 2]
    _event_ll_beta = np.sum(_event_n) / x[1] + \
                     np.sum(_event_n * np.log(_event_t / x[0])) - \
                     np.sum(_event_n * (_event_t / x[0])**x[1] * \
                            np.log(_event_t / x[0]))
    _event_ll_eta = (-x[1] / x[0]) * np.sum(_event_n) + \
                    (x[1] / x[0]) * np.sum(_event_n * (_event_t / x[0])**x[1])

    # Calculate the value of the log-likelihood for the right-censored
    # observations.
    _right_t = data[np.where(data[:, 3] == 2)][:, 1]
    _right_n = data[np.where(data[:, 3] == 2)][:, 2]
    _right_ll_beta = np.sum(_right_n * (_right_t / x[0])**x[1] * \
                            np.log(_right_t / x[0]))
    _right_ll_eta = (x[1] / x[0]) * np.sum(_right_n * (_right_t / x[0])**x[1])

    # Calculate the value of the log-likelihood for the left- and interval-
    # censored observations.  Use the midpoint of the interval as an
    # approximation.
    _interval_lt = data[np.where(data[:, 3] == 3)][:, 0]
    _interval_rt = data[np.where(data[:, 3] == 3)][:, 1]
    _interval_t = (_interval_lt + _interval_rt) / 2.0
    _interval_n = data[np.where(data[:, 3] == 3)][:, 2]

    _interval_ll_beta = np.sum(_interval_n) / x[1] + \
                        np.sum(_interval_n * np.log(_interval_t / x[0])) - \
                        np.sum(_interval_n * (_interval_t / x[0])**x[1] * \
                               np.log(_interval_t / x[0]))
    _interval_ll_eta = (-x[1] / x[0]) * np.sum(_interval_n) + \
                       (x[1] / x[0]) * np.sum(_interval_n * \
                       (_interval_t / x[0])**x[1])

    # Following are the exact equations for the interval censored observations.
    #_nr = _interval_rt / x[0]
    #_nr_b = (_nr + 0.000001)**x[1]
    #_nr_exp = np.exp(-(_nr_b))

    #_nl = _interval_lt / x[0]
    #_nl_b = (_nl + 0.000001)**x[1]
    #_nl_exp = np.exp(-(_nl_b))

    #_n = (-_nl_b * np.log(_nl_b) * _nl_exp) + (_nr_b * np.log(_nr_b) * _nr_exp)
    #_d = _nl_exp - _nr_exp
    #_interval_ll_beta = np.sum(_interval_n * _n / _d)

    #_n = ((x[1] / x[0]) * _nl_b * _nl_exp) - ((x[1] / x[0]) * _nr_b * _nr_exp)
    #_interval_ll_eta = np.sum(_interval_n * _n / _d)

    _del_beta = _event_ll_beta - _right_ll_beta + _interval_ll_beta
    _del_eta = _event_ll_eta - _right_ll_eta + _interval_ll_eta

    return _del_eta, _del_beta


def parametric_fit(data, start, end, fitmeth, dist='exponential'):
    """
    Function to fit data to a parametric distribution and find point estimates
    of the parameters.  It is up to the calling function to calculate bounding
    values.  In the case of regression fitting, the correlation coefficient is
    also returned.

    :param array-like data: the data set to fit.  This is a list of tuples
                            where each tuple contains the following, in order:
                            * 0 = Observed unit ID
                            * 1 = Interval start time
                            * 2 = Interval end time
                            * 3 = Time between failures or interarrival time
                            * 4 = Status of observation
                            * 5 = Quantity of observations
                            * 6 = Date of observation
    :param float start: the minimum time to include in the fit.  Used to
                        exclude outliers.
    :param float end: the maximum time to include in the fit.  Used to exclude
                      outliers.
    :param int fitmeth: method used to fit data to the selected distribution.
                        * 1 = maximum likelihood estimation (preferred)
                        * 2 = rank regression
    :param str dist: the noun name of the distribution to fit.  Defaults to
                     the exponential distribution.
    :return: _fit; [[scale estimate, shape estimate, location estimate],
                    [scale variance, covariance, shape variance],
                    [MLE, AIC, BIC], correlation coeff.]
    :rtype: list
    """

    _error_function = lambda s, x, y: ((s[0] + s[1] * _x) - y)

    # Initialize lists to hold results.
    _parameters = [0.0, 0.0, 0.0]           # Scale, shape, location.
    _variance = [0.0, 0.0, 0.0]             # Scale variance, covariance,
                                            # shape variance.
    _gof = [0.0, 0.0, 0.0]                  # MLE, AIC, BIC
    _rho_hat = 0.0                          # Correlation coefficient

    # Sort data by the right of the interval.  Remove records occurring before
    # the start time and after the end time.
    _data = sorted(data, key=lambda x: float(x[2]))
    _data = [_rec for _rec in _data if float(_rec[1]) >= start]
    _data = [_rec for _rec in _data if float(_rec[2]) <= end]
    _data = np.array(_data)

    # Replace the string status with integer status.
    for _record in _data:
        if _record[4] == 'Right Censored' or _record[4] == '2':
            _record[4] = 2
        elif (_record[4] == 'Left Censored' or
              _record[4] == 'Interval Censored' or
              _record[4] == '3'):
            _record[4] = 3
        else:
            _record[4] = 1

    # Coerce the data set into the form necessary for fitting to functions.
    _data = np.vstack((_data[:, 1], _data[:, 2], _data[:, 5], _data[:, 4]))
    _data = np.array(np.transpose(_data), dtype=float)
    _n_records = len(_data)

    if fitmeth == 1:
        if dist == 'exponential':
            # Provide an estimate of theta assuming no suspensions and using
            # the right of the interval.  Use this as the starting value to
            # scipy.optimize.fsolve.
            _theta = 1.0 / expon.fit(np.array(_data[:, 1], dtype=float),
                                     floc=0)[1]

            _parameters[0] = optim.fsolve(exponential_partial_derivs, _theta,
                                          args=np.array(_data, dtype=float))[0]

            _fI = fisher_information(exponential_log_pdf,
                                     _parameters, _data[:, 1])
            _variance[0] = 1.0 / _fI[0, 0]

            _gof[0] = exponential_log_likelihood([_parameters[0]], _data)
            _gof[1] = -2.0 * _gof[0] + 2.0
            _gof[2] = -2.0 * _gof[0] + (np.log(_n_records) - np.log(np.pi))

        elif dist == 'lognormal':
            # Provide an estimate of mu and sigma assuming no suspensions and
            # using the right of the interval.  Use these as the starting
            # values to scipy.optimize.fsolve.

            # Adjust the right-censored times to be the mid-point between the
            # censored time and the maximum oberserved time in the data set.
            _adj_right = (max(_data[:, 1]) + \
                          _data[np.where(_data[:, 3] == 2), 1]) / 2.0
            _data[np.where(_data[:, 3] == 2), 1] = _adj_right

            # Adjust the interval-censored times so they can be passed to the
            # fit method.
            _interval_lt = _data[np.where(_data[:, 3] == 3)][:, 0]
            _interval_rt = _data[np.where(_data[:, 3] == 3)][:, 1]
            _interval_t = (_interval_lt + _interval_rt) / 2.0
            _data[np.where(_data[:, 3] == 3), 1] = _interval_t

            (_sigma, __,
             _mu) = lognorm.fit(np.array(_data[:, 1], dtype=float), floc=0)

            _parameters[0] = np.log(_mu)
            _parameters[1] = _sigma

            _fI = fisher_information(lognormal_log_pdf,
                                     _parameters, _data[:, 1])
            _variance[0] = 1.0 / np.diag(_fI)[0]
            _variance[1] = 1.0 / np.diag(_fI)[1]

            _gof[0] = lognormal_log_likelihood([_parameters[0],
                                                _parameters[1]], _data)
            _gof[1] = -2.0 * _gof[0] + 2.0
            _gof[2] = -2.0 * _gof[0] + (np.log(_n_records) - np.log(np.pi))

        elif dist == 'normal':
            # Provide an estimate of mu and sigma assuming no suspensions and
            # using the right of the interval.  Use these as the starting
            # values to scipy.optimize.fsolve.

            # Adjust the right-censored times to be the mid-point between the
            # censored time and the maximum oberserved time in the data set.
            _adj_right = (max(_data[:, 1]) + \
                          _data[np.where(_data[:, 3] == 2), 1]) / 2.0
            _data[np.where(_data[:, 3] == 2), 1] = _adj_right

            # Adjust the interval-censored times so they can be passed to the
            # fit method.
            _interval_lt = _data[np.where(_data[:, 3] == 3)][:, 0]
            _interval_rt = _data[np.where(_data[:, 3] == 3)][:, 1]
            _interval_t = (_interval_lt + _interval_rt) / 2.0
            _data[np.where(_data[:, 3] == 3), 1] = _interval_t

            (_mu, _sigma) = norm.fit(np.array(_data[:, 1], dtype=float))
            #optim.fsolve(gaussian_partial_derivs,
            #                              [_mu, _sigma],
            #                              args=np.array(_data, dtype=float))

            _parameters[0] = _mu
            _parameters[1] = _sigma

            _fI = fisher_information(gaussian_log_pdf,
                                     _parameters, _data[:, 1])
            _variance[0] = 1.0 / np.diag(_fI)[0]
            _variance[1] = 1.0 / np.diag(_fI)[1]

            _gof[0] = gaussian_log_likelihood([_parameters[0],
                                               _parameters[1]], _data)
            _gof[1] = -2.0 * _gof[0] + 2.0
            _gof[2] = -2.0 * _gof[0] + (np.log(_n_records) - np.log(np.pi))

        elif dist == 'weibull':
            # Provide an estimate of eta and beta assuming no suspensions and
            # using the right of the interval.  Use these as the starting
            # values to scipy.optimize.fsolve.
            (__, _beta,
            __, _eta) = exponweib.fit(np.array(_data[:, 1], dtype=float),
                                     f0=1, floc=0)

            (_eta, _beta) = optim.fsolve(weibull_partial_derivs, [_eta, _beta],
                                         args=np.array(_data, dtype=float))
            _parameters[0] = _eta
            _parameters[1] = _beta

            _fI = fisher_information(weibull_log_pdf,
                                     _parameters, _data[:, 1])
            _variance[0] = 1.0 / np.diag(_fI)[0]
            _variance[1] = 1.0 / np.diag(_fI)[1]
            _variance[2] = 1.0 / _fI[0, 1]

            _gof[0] = weibull_log_likelihood([_parameters[0],
                                              _parameters[1]], _data)
            _gof[1] = -2.0 * _gof[0] + 2.0
            _gof[2] = -2.0 * _gof[0] + (np.log(_n_records) - np.log(np.pi))

    else:
        # Retrieve the failure times for all non-censored data.
        _x = _data[np.where(_data[:, 3] == 1), 1]
        _x = np.array(_x.tolist()[0])

        if len(_x) == 0:
            _util.rtk_information(_(u"There are no single times-to-failure "
                                    u"in your data set.  All of your "
                                    u"observations are censored.  Rank "
                                    u"regression methods cannot handle data "
                                    u"sets containing only censored data.  It "
                                    u"is recommended that you use maximum "
                                    u"likelihood estimation (MLE) to fit this "
                                    u"data set."))
            return False

        # Calculate median ranks.  This accounts for censored observations.
        _median_rank = bernard_ranks(_data)

        # Linearize the median ranks (probability of failure) depending on
        # the s-distribution.  Fit the linearized median ranks to a straight
        # line using the x-values from above as the independent variable.
        # Transform the intercept and slope to the proper variable(s) for the
        # distribution being fit.  Finally, calculate the variance and
        # covariance of the parameters.
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

        elif dist == 'normal':
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
            _y_linear = np.log(-1.0 * np.log(1.0 - _median_rank))

            _p, _covar, _info, __, __ = optim.leastsq(_error_function,
                                                      [1.0, 1.0],
                                                      args=(_x, _y_linear),
                                                      full_output=True)
            _parameters[1] = _p[1]
            _parameters[0] = np.exp(-_p[0] / _p[1])

        # Calculate the variance and covariance of the parameters.
        _RSS = np.sum(_info['fvec']**2.0)
        _MSE = _RSS / _df
        _cov = _MSE * _covar
        _variance[0] = _cov[1][1]
        _variance[1] = _cov[0][1]
        _variance[2] = _cov[0][0]

        # Calculate MLE, AIC, and BIC.
        _s2b = _RSS / _n_records
        _gof[0] = -_n_records / 2.0 * np.log(2.0 * np.pi) - \
                  _n_records / 2.0 * np.log(_s2b) - 1.0 / (2.0 * _s2b) * _RSS
        _gof[1] = -2.0 * _gof[0] + 2.0
        _gof[2] = -2.0 * _gof[0] + (np.log(_n_records) - np.log(np.pi))

        # Calculate the correlation coefficient (i.e., R)
        _rho_hat = np.corrcoef(_x, _y_linear)[0, 1]

    _fit = [_parameters, _variance, _gof, _rho_hat]

    return _fit


def theoretical_distribution(data, dist, params):
    """
    Function to create a data set from the theoretical distribution given the
    parameters.

    :param ndarray data: the data set that the theoretical distribution will be
                         created for.  This is a zero-based list of lists or list of
                 tuples where index 1 is the left of the interval and index 2
                 is the right of the interval.  The other indices are not used.
    :param str dist: the noun name of the distribution.
    :param list para: list with the values of the distribution parameters.
    :return: _theoretical_probs; the probabilities of the theoretical
             distribution with parameters para.
    :rtype: ndarray
    """

    _x = np.sort(np.array(data[:, 2], dtype=float))

    if dist == 'exponential':
        _y = 1.0 - np.exp(-params[0] * _x)
    elif dist == 'lognormal':
        _x = (np.log(_x + 0.01) - params[0]) / params[1]
        _y = norm.cdf(_x)
    elif dist == 'normal':
        _x = (_x - params[0]) / params[1]
        _y = norm.cdf(_x)
    elif dist == 'weibull':
        _y = 1.0 - np.exp(-(_x / params[0])**params[1])

    return _y
