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

# Import R library.
try:
    from rpy2 import robjects
    from rpy2.robjects import r as R
    from rpy2.robjects.packages import importr
    import rpy2.rlike.container as rlc
    import rpy2.rinterface as ri
    __USE_RPY__ = False
    __USE_RPY2__ = True
except ImportError:
    __USE_RPY__ = False
    __USE_RPY2__ = False

# Import mathematical functions.
import numpy as np
from scipy.stats import chi2, expon, norm, tvar
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
def kaplan_meier(data, endtime, conf=0.75, conftype=3):
    """
    Function to calculate the Kaplan-Meier survival function estimates.

    :param data: the data to use in estimating the KM values.
    :type data: list of tuples where each tuple is in the form of
                (Left of Interval, Right of Interval, Event Status, Quantity)
                Event status is one of:
                - 0 = right censored
                - 1 = event at time
                - 2 = left censored
                - 3 = interval censored
    :param endtime: time at which to stop analysis (helps eliminate stretched
                    plots due to small number of events at high hours).
    :param conf: the confidence level of the KM estimates.
    :param conftype: the confidence interval type for the KM estimates.
                     Confidence type is one of:
                     - 1 = lower one-sided
                     - 2 = upper one-sided
                     - 3 = two-sided
    :return: _kaplan_meier; the matrix of results where each row in the matrix
             contains the following, in order:
             - Observation time
             - Number at risk
             - Number failing
             - se of S(t)
             - Lower bound on S(t)
             - Point estimate of S(t)
             - Upper bound on S(t)
    :rtype: numpy matrix
    """

    # Eliminate zero time failures and failures occurring after any
    # user-supplied upper limit.
    data = [x for x in data if x[0] >= 0.0]
    if endtime != 0.0:
        data = [x for x in data if x[1] <= endtime]

    _times = [x[0] for x in data]
    _times2 = [x[1] for x in data]
    _status = [x[2] for x in data]
    _quant = [x[3] for x in data]

    _M = len(_times)

    # Get the unique time (intervals).
    _l_times = np.matrix([x for x in list(set(_times))])
    _r_times = np.matrix([x for x in list(set(_times2))])

    # Convert right censoring times to numeric values.
    for i, x in enumerate(_times2):
        if isinstance(x, str):
            _times2[i] = float(x.rstrip('+'))

    # Convert status to a numeric indicator variable.
    for i, __ in enumerate(_status):
        if _status[i] == "Right Censored":
            _status[i] = 0
        elif _status[i] == "Left Censored":
            _status[i] = 2
        elif _status[i] == "Interval Censored":
            _status[i] = 3
        else:
            _status[i] = 1

    # Estimate the Kaplan-Meier survival function.  Prefer the use of R to
    # perform the calculations.  Otherwise, use the built-in RTK function.
    if __USE_RPY2__:
        _r_survival = importr('survival')

        _times = robjects.FloatVector(_times)
        _times2 = robjects.FloatVector(_times2)
        _status = robjects.IntVector(_status)
        _quant = robjects.IntVector(_quant)

        _tdata = robjects.DataFrame({'time': _times,
                                     'status': _status,
                                     'n': _quant})

        robjects.globalenv['surv'] = _r_survival.Surv(_times2, _times2,
                                                      _status, type='interval')

        _km = _r_survival.survfit(robjects.Formula('surv ~ 1'),
                                  data=_tdata, weight=_quant)

        # Every subject must have a censored time to use survrec.
        #survrec = importr('survrec')
        #units = robjects.StrVector(units)
        #survr = survrec.Survr(units, times2, status2)
        #fit = survrec.wc_fit(survr)

        # Create the numpy matrix of results.
        _kaplan_meier = np.concatenate((np.matrix(_km[1]).transpose(),
                                        np.matrix(_km[2]).transpose()), axis=1)
        _kaplan_meier = np.concatenate((_kaplan_meier,
                                        np.matrix(_km[3]).transpose()), axis=1)
        _kaplan_meier = np.concatenate((_kaplan_meier,
                                        np.matrix(_km[7]).transpose()), axis=1)
        _kaplan_meier = np.concatenate((_kaplan_meier,
                                        np.matrix(_km[8]).transpose()), axis=1)
        _kaplan_meier = np.concatenate((_kaplan_meier,
                                        np.matrix(_km[5]).transpose()), axis=1)
        _kaplan_meier = np.concatenate((_kaplan_meier,
                                        np.matrix(_km[9]).transpose()), axis=1)

    else:

        # Determine the confidence bound z-value.
        _z_norm = norm.ppf(conf)

        # Get the total number of events.
        N = sum(_quant)

        _kaplan_meier = []
        _Sh = 1.0

        # Find the total number of failures and suspensions in interval [i - 1, i].
        _d = np.matrix([x[3] for i, x in enumerate(data)
                        if (x[0] == data[i][0] and
                            (_status[i] == 1 or _status[i] == 3))],
                       dtype=float)
        _rs = np.matrix([x[3] for i, x in enumerate(data)
                         if (x[0] == data[i][0] and _status[i] == 0)],
                        dtype=float)
        _ls = np.matrix([x[3] for i, x in enumerate(data)
                         if (x[0] == data[i][0] and _status[i] == 2)],
                        dtype=float)

        # Estimate the probability of failing in interval [i - 1, i].
        _Si = 1.0 - np.divide(_d.transpose(), _n.transpose())

        # Estimate the probability of survival up to time i [S(ti)].
        _Sh = np.cumprod(_Si).transpose()

        # Calculate the standard error for S(ti).
        _z = np.cumsum(1.0 / np.multiply((_n - _d + 1), _n))
        _se = np.multiply(np.power(_Si, 2.0), _z.transpose())

        # Calculate confidence bounds for S(ti).
        _mean_ll = _Sh - _z_norm * _se
        _mean_ul = _Sh + _z_norm * _se
        if conftype == 1:
            _mean_ul = _Sh
        if conftype == 2:
            _mean_ll = _Sh

    return _kaplan_meier


def kaplan_meier_mean(data, conf=0.75):
    """
    Function to calculate the MTBF from a Kaplan-Meier data set.  This function
    uses the algorithm found in Lee and Wang, "Statistical Methods for Survival
    Data Analysis", page 74.

    :param data: the Kaplan-Meier data set.  This is a matrix where each row
             contains the following, in order:
              * Time point (t) at which the curve has a step.
              * Number of subjects at risk at time t.
              * Number of events that occur at time t.
              * Standard error of the survival function at time t.
              * Lower bound on the survival function at time t.
              * Point estimate of the survival function at time t.
              * Upper bound on the survival function at time t.
    :type data: numpy matrix
    :param conf: the desired confidence for the bounding values.
    :type conf: float
    :return: _mtbf; matrix of mean values where each row contains the
             following, in order:
              * Lower bound on the mean value.
              * Point estimate of the mean value.
              * Upper bound on the mean value.
              * Variance of the mean value.
    :rtype: list of lists
    """

    from operator import itemgetter

    _data = data.tolist()

    # Sort the dataset by event time asscending and only keep those records
    # with at least one failure.
    _data = sorted(_data, key=itemgetter(0))
    _data = [i for i in _data if i[2] > 0]

    _n = len(_data)
    _M = _data[0][1]
    _Var = 0.0

    _mtbf = []

    # Determine the confidence bound z-value.
    _z_norm = norm.ppf(conf)

    for i in range(1, len(_data)):
        _a = _data[i][5] * (_data[i][0] - _data[i - 1][0])
        _M += _a
        _Var += (_a**2.0) / ((_n - i) * (_n - i + 1))
        _MLL = _M - sqrt(_Var) * _z_norm
        _MUL = _M + sqrt(_Var) * _z_norm

        _mtbf.append([_MLL, _M, _MUL, _Var])

    return _mtbf


def kaplan_meier_hazard(data):
    """
    Function to calculate the Kaplan-Meier cumulative hazard rate, hazard rate,
    and log hazard rate.  This function uses the algorithm found in
    Peterson "Expressing the Kaplan-Meier estimator as a function of empirical
    subsurvival functions." Journal of the American Statistical Association
    1977;72:854-858.

    :param data: the Kaplan-Meier data set.  This is a matrix where each row
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

    _times = np.matrix([i[0] for i in data.tolist()])

    # Cumulative hazard rates.
    _H_ll = np.ma.getdata(np.ma.log([i[4] for i in data.tolist()]))
    _H = np.ma.getdata(np.ma.log([i[5] for i in data.tolist()]))
    _H_ul = np.ma.getdata(np.ma.log([i[6] for i in data.tolist()]))
    _H_ll = np.matrix(-_H_ll)
    _H = np.matrix(-_H)
    _H_ul = np.matrix(-_H_ul)

    # Log cumulative hazard rates.
    _logH = np.ma.log(_H)
    _logH_ll = np.ma.log(_H_ll)
    _logH_ul = np.ma.log(_H_ul)

    # Calculate the hazard rates.
    _h = np.divide(_H, _times)
    _h_ll = np.divide(_H_ll, _times)
    _h_ul = np.divide(_H_ul, _times)

    # Combine the results together into a single numpy matrix.
    _hazard = np.concatenate((_h_ll.transpose(), _h.transpose()), axis=1)
    _hazard = np.concatenate((_hazard, _h_ul.transpose()), axis=1)
    _hazard = np.concatenate((_hazard, _H_ll.transpose()), axis=1)
    _hazard = np.concatenate((_hazard, _H.transpose()), axis=1)
    _hazard = np.concatenate((_hazard, _H_ul.transpose()), axis=1)
    _hazard = np.concatenate((_hazard, _logH_ll.transpose()), axis=1)
    _hazard = np.concatenate((_hazard, _logH.transpose()), axis=1)
    _hazard = np.concatenate((_hazard, _logH_ul.transpose()), axis=1)

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

    if(__USE_RPY__):
        print "Probably using Windoze."

    elif(__USE_RPY2__):
        survival = importr('survival')

        _times_ = robjects.FloatVector(_tau_[:m-1])
        _status_ = robjects.IntVector(_status_)

        _surv_ = survival.Surv(_times_, _status_)
        robjects.globalenv['surv'] = _surv_
        _ekm_ = survival.survfit(robjects.Formula('surv ~ 1'))

    _So_ = []
    for i in range(len(_ekm_[5])):
        _So_.append(_ekm_[5][i])

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


def matrix_multiply(matrix1, matrix2):
    """
    Function to multiply two matrices.

    Keyword Arguments:
    matrix1 --
    matrix2 --
    """

# Check matrix dimensions
    if len(matrix1[0]) != len(matrix2):
        print 'Matrices must be m*n and n*p to multiply!'

    else:
# Multiply if correct dimensions
        _new_matrix_ = [[0 for row in range(len(matrix1))] for col in range(len(matrix2[0]))]
        for i in range(len(matrix1)):
            for j in range(len(matrix2[0])):
                for k in range(len(matrix2)):
                    _new_matrix_[i][j] += matrix1[i][k] * matrix2[k][j]

        return(_new_matrix_)


def parametric_fit(data, start, end, fitmeth, dist='exponential'):
    """
    Function to fit data to a parametric distribution and estimate the
    parameters.

    :param array-like data: the data set to fit.  This is a list of tuples
                            where each tuple contains the following, in order:
                            * Observed unit ID
                            * Interval start time
                            * Interval end time
                            * Time between failures or interarrival time
                            * Status of observation
                            * Quantity of observations
                            * Date of observation
    :param float start: the minimum time to include in the fit.  Used to exclude
                        outliers.
    :param float end: the maximum time to include in the fit.  Used to exclude
                      outliers.
    :param int fitmeth: method used to fit data to the selected distribution.
                        * 1 = maximum likelihood estimation (MLE)
                        * 2 = rank regression
    :param str dist: the noun name of the distribution to fit.  Defaults to
                     the exponential distribution.
    :return: an R object containing the results of the analysis.  This object
             will need to be unpacked by the calling function.  The index of
             the parameters varies depending on the distribution fit.
    :rtype: R object
    """

    # Remove and records occurring before the start time and after the end
    # time.
    _data = [i for i in data if i[1] > start]
    _data = [i for i in data if i[2] <= end]

    _left = [i[1] for i in _data]
    _right = [i[2] for i in _data]
    _status = [i[4] for i in _data]

    for i in range(len(_status)):
        if _status[i] == 'Right Censored':
            _status[i] = 0
        elif _status[i] == 'Event':
            _status[i] = 1
        elif _status[i] == 'Left Censored':
            _status[i] = 2
        elif _status[i] == 'Interval Censored':
            _status[i] = 3

    _left = robjects.FloatVector(_left)
    _right = robjects.FloatVector(_right)
    _status = robjects.IntVector(_status)

    if __USE_RPY2__:

        Rbase = importr('base')

        if fitmeth == 1:
            if dist == 'exponential':
                _dist = 'exp'
                #expon.fit(np.array(_right), floc=0)
                #np.std(np.array(_right))
            elif dist == 'lognormal':
                _dist = 'lnorm'
            elif dist == 'normal':
                _dist = 'norm'
            else:
                _dist = dist

            for i in range(len(_data)):
                if _data[i][4] == 0:
                    _right[i] = 'NA'
                elif _data[i][4] == 1:
                    _left[i] = _right[i]
                elif _data[i][4] == 2:
                    _left[i] = 'NA'

            _od = rlc.OrdDict([('left', _left),
                               ('right', _right)])

            _censdata = robjects.DataFrame(_od)
            _n_row = Rbase.nrow(_censdata)
            if _n_row[0] > 1:
                _r_fitdistrplus = importr('fitdistrplus')
                try:
                    _fit = _r_fitdistrplus.fitdistcens(_censdata, _dist)
                except ri.RRuntimeError:
                    _fit = None

                #para=R.list(scale=fit[0][1], shape=fit[0][0])
                #fitdistrplus.plotdistcens(censdata, _dist_, para)
            else:
                _fit = None

        elif fitmeth == 2:

            if dist == 'normal':
                _dist = 'gaussian'
            else:
                _dist = dist

            _r_survival = importr('survival')

            _r_surv = _r_survival.Surv(_left, _right, _status, type='interval')
            robjects.globalenv['surv'] = _r_surv
            _r_formula = robjects.Formula('surv ~ 1')

            try:
                _fit = _r_survival.survreg(_r_formula, dist=_dist)
            except ri.RRuntimeError:
                _fit = None

    else:
        _fit = None

    return _fit


def theoretical_distribution(data, dist, para):
    """
    Function to create a data set from the theoretical distribution given the
    parameters.

    :param data: the data set that the theoretical distribution will be
                 created for.  This is a zero-based list of lists or list of
                 tuples where index 1 is the left of the interval and index 2
                 is the right of the interval.  The other indices are not used.
    :type data: list of lists or list of tuples
    :param str dist: the noun name of the distribution.
    :param para: list with the names and values of the distribution parameters.
    :type para: R list
    :return: _theoretical_probs; the probabilities of the theoretical
             distribution with parameters para.
    :rtype: R object
    """

    Rbase = importr('base')

    # Create the R density and probability distribution names.
    _ddistname = R.paste('d', dist, sep='')
    _pdistname = R.paste('p', dist, sep='')

    # Calculate the minimum and maximum values for the left interval and right
    # interval times.
    _xminleft = min([i[1] for i in data if i[1] != 'NA'])
    _xminright = min([i[2] for i in data if i[2] != 'NA'])
    _xmin = min(_xminleft, _xminright)

    _xmaxleft = max([i[1] for i in data if i[1] != 'NA'])
    _xmaxright = max([i[2] for i in data if i[2] != 'NA'])
    _xmax = max(_xmaxleft, _xmaxright)

    _xrange = _xmax - _xmin
    _xmin = _xmin - 0.3 * _xrange
    _xmax = _xmax + 0.3 * _xrange

    # Creat a list of probabilities for the theoretical distribution with the
    # estimated parameters at the times created prviously.
    _den = float(len(data))
    _densfun = R.get(_ddistname, mode='function')
    _nm = R.names(para)
    _args = R.names(R.formals(_densfun))
    _m = R.match(_nm, _args)
    _s = R.seq(_xmin, _xmax, by=(_xmax - _xmin) / _den)
    _theoretical_probs = Rbase.do_call(_pdistname, R.c(R.list(_s), para))

    return _theoretical_probs
