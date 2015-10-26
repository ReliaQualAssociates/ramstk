#!/usr/bin/env python
"""
Contains functions for performing Kaplan-Meier survival analysis.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.analyses.survival.KaplanMeier.py is part of The RTK Project
#
# All rights reserved.

# Import mathematical functions.
import lifelines as nonpar
import numpy as np
from scipy.stats import norm                # pylint: disable=E0611
from math import sqrt


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
             _r; the array of observations during which an event occurred.
    :rtype: ndarray, ndarray
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
            for i in range(int(_row[2]) - 1):   # pylint: disable=W0612
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

    :param ndarray data: the Kaplan-Meier data set.  This is a matrix where
                         each row contains the following, in order:
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
    _indices = np.where(_x != 0)

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

    :param ndarray data: the Kaplan-Meier data set.  This is a matrix where
                         each row contains the following, in order:
                         * Time point (t) at which the curve has a step.
                         * Number of subjects at risk at time t.
                         * Number of events that occur at time t.
                         * Standard error of the survival function at time t.
                         * Lower bound on the survival function at time t.
                         * Point eStimate of the survival function at time t.
                         * Upper bound on the survival function at time t.
    :type data: numpy matrix
    :return: _hazard; matrix of hazard function related results.  There is one
             row for each observation time where each row contains the
             following, in order:
             * Lower bound on the hazard rate.
             * Point estimate of the hazard rate.
             * Upper bound on the hazard rate.
             * Lower bound on the cumulative hazard rate.
             * Point estimate of the cumulative hazard rate.
             * Upper bound on the cumulative hazard rate.
             * Lower bound on the logarithm of the cum. hazard rate.
             * Point estimate of the logarithm of the cum. hazard rate.
             * Upper bound on the logarithm of the cum. hazard rate.
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
