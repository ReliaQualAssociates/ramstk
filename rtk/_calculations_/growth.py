#!/usr/bin/env python
"""
Contains functions for performing calculations associated with reliability
growth.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       growth.py is part of The RTK Project
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

# Import mathematical functions.
import numpy as np
from numpy.linalg import inv
from math import ceil, exp, floor, log, sqrt
from scipy.stats import chi2, norm, t       #pylint: disable=E0611
from scipy.optimize import fsolve, root     #pylint: disable=E0611

# Import other RTK modules.
try:
    import configuration as _conf
    import utilities as _util
except ImportError:
    import rtk.configuration as _conf
    import rtk.utilities as _util


# +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
# Following are the functions for building the RG plan.                   #
# +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
def initial_mtbf(ttt, t1, mtbff, gr, ms, prob):
    """
    Function to calculate the initial MTBF.  This function is used to calculate
    the initial MTBF for the entire test program only.

    :param ttt: the total time on test.  Summed across all phases.
    :type ttt: float
    :param t1: the length of the first test phase.
    :type t1: float
    :param mtbff: the final MTBF.
    :type mtbff: float
    :param float gr: the average growth rate.
    :type gr: float
    :param ms: the average management strategy.
    :type ms: float
    :param prob: the probability of observing at least one failure.
    :type prob: float
    :return: _mtbfi; the initial MTBF.
    :rtype: float
    """

    try:
        _mtbfi = (-t1 * ms) / log(1.0 - prob)
    except (ValueError, ZeroDivisionError):
        try:
            _mtbfi = mtbff / exp(gr * (0.5 * gr + log(ttt / t1) + 1.0))
        except (ValueError, ZeroDivisionError):
            _mtbfi = 0.0
            _util.rtk_error(_(u"To calculate the minimum inital MTBF, you "
                              u"must provide the following inputs with "
                              u"values greater than zero:\n\n"
                              u"1. Total test time (TTT): %f\n"
                              u"2. Length of first test phase (t1): %f\n"
                              u"3. Final MTBF (MTBFF): %f\n"
                              u"4. Growth rate (GR): %f")
                            % (ttt, t1, mtbff, gr))

    return _mtbfi


def final_mtbf(ttt, t1, mtbfi, gr):
    """
    Function to calculate the final MTBF.  This function can be used to
    calculate the final MTBF for the entire test program or the final MTBF for
    a single test phase.

    :param ttt: the total time on test.
    :type ttt: float
    :param t1: the length of the first test phase.
    :type t1: float
    :param mtbfi: the initial program MTBF.
    :type mtbfi: float
    :param float gr: the average growth rate.
    :type gr: float
    :return: _mtbff; the final MTBF.
    :rtype: float
    """

    # Try to calculate the final MTBF based on the model.
    try:
        _mtbff = mtbfi * exp(gr * (0.5 * gr + log(ttt / t1) + 1.0))
    except(ValueError, ZeroDivisionError):
        _mtbff = 0.0
        _util.rtk_error(_(u"To calculate the final MTBF, you must provide the "
                          u"following inputs with values greater than "
                          u"zero:\n\n"
                          u"1. Total test time (TTT): %f\n"
                          u"2. Length of the first test phase (t1): %f\n"
                          u"3. Intial program MTBF (MI): %f\n"
                          u"4. Growth rate (GR): %f")
                        % (ttt, t1, mtbfi, gr))

    return _mtbff


def average_mtbf(ttt, t1, mtbfi, gr, T, N):
    """
    Function to calculate the average growth rate over a test phase.

    :param float ttt: the total test time for the test phase.
    :param float t1: the length of the first test phase.
    :param float mtbfi: the initial MTBF for the test program.
    :param float gr: the average growth rate for the test phase.
    :param float T: total test time for previous test phase.
    :param int N: cumulative number of failures over previous i - 1 test phases.
    :return: _mtbfa; the average MTBF over the test phase.
    :rtype: float
    """

    # First calculate the expected number of failures in the test phase.
    _n_failures = (1.0 / mtbfi) * t1 * (ttt / t1)**(1.0 - gr) - N

    # The calculate the average MTBF over the test phase.
    _mtbfa = (ttt - T) / _n_failures

    return _n_failures, _mtbfa


def total_time(t1, mtbfi, mtbff, gr, mtbfa, num_fails, cum_time):
    """
    Function to calculate the total test time required.  This function can be
    used to calculate the total time required for the entire test program or
    the total time required for a single test phase.

    :param t1: the length of the first test phase.
    :type t1: float
    :param mtbfi: the initial program MTBF.
    :type mtbfi: float
    :param mtbff: the final MTBF.
    :type mtbff: float
    :param float gr: the average growth rate.
    :type avegr: float
    :param mtbfa: the average MTBF.
    :type mtbfa: float
    :param num_fails: the number of failures expected during the test phase.
    :type num_fails: integer
    :param cum_time: the cumulative test time up to, but not including, the
                     current test phase.
    :type cum_time: float
    :return: _ttt; the minimum required total time test.
    :rtype: float
    """

    # First attempt to calculate the test time required based on the model.  If
    # that fails, try to calculate it based on the average MTBF.
    try:
        _ttt = t1 * (((1.0 - gr) * mtbff / mtbfi)**(1.0 / gr))
        if mtbff / mtbfi == 1.0:
            _ttt = t1
    except(ValueError, ZeroDivisionError):
        _ttt = (mtbfa * num_fails) + cum_time

    return _ttt


def growth_rate(ttt, t1, mtbfi, mtbff):
    """
    Function to calculate the minimum required growth rate.

    :param ttt: the total time on test.
    :type ttt: float
    :param t1: the length of the first test phase.
    :type t1: float
    :param mtbfi: the initial MTBF.
    :type mtbfi: float
    :param mtbff: the final MTBF.
    :type mtbff: float
    :return: _gr: the minimum required average growth rate.
    :rtype: float
    """

    try:
        _gr = -log(ttt / t1) - 1.0 + sqrt((1.0 + log(ttt / t1))**2.0 + 2.0 * log(mtbff / mtbfi))
    except(ValueError, ZeroDivisionError):
        _util.rtk_error(_(u"To calculate the minimum required program growth "
                          u"rate, you must provide the following inputs with "
                          u"values greater than zero:"
                          u"1. Total test time (TTT): %f"
                          u"2. Length of the first test phase (t1): %f"
                          u"3. Initial program MTBF (MI): %f"
                          u"4. Final program MTBF (MF): %f")
                        % (ttt, t1, mtbfi, mtbff))

    return _gr


def minimum_first_phase_time(ttt, mtbff, mtbfa, gr):
    """
    Function to calculate the minimum length of the first reliability growth
    phase.

    :param mtbfi: the initial MTBF.
    :type mtbfi: float
    :param ms: the average management strategy.
    :type ms: float
    :param prob: the probability of observing a failure.
    :type prob: float
    :return: _t1; the minimum required length of the first test phase.
    :rtype: float
    """

    try:
        _t1 = exp(log(ttt) - (log((1 - gr) * (mtbff / mtbfa)) / gr))
    except(ValueError, ZeroDivisionError):
        _t1 = 0.0
        _util.rtk_error(_(u"To calculate the minimum length of the first "
                          u"phase, you must provide the following inputs "
                          u"with values greater than zero: "
                          u"1. Initial MTBF (MI): %f"
                          u"2. Average management strategy (MS): %f"
                          u"3. Probability of observing a failure: %f")
                        % (mtbfi, avems, prob))

    return _t1


def management_strategy(mtbfi, mtbfgp, avefef):
    """
    Function to calculate the minimum required management strategy.

    :param mtbfi: the initial MTBF.
    :type mtbfi: float
    :param mtbfgp: the growth potential MTBF.
    :type mtbfgp: float
    :param avefef: the average fix effectiveness factor.
    :type avefef: float
    :return: _avems: the minimum required average management strategy.
    :rtype: float
    """

    try:
        _avems = (1.0 - (mtbfi / mtbfgp)) / avefef
    except(ValueError, ZeroDivisionError):
        _avems = 100.0
        _util.rtk_error(_(u"To calculate the required management strategy, "
                          u"you must provide the following inputs with values "
                          u"greater than zero: "
                          u"1. Initial MTBF (MI): %f"
                          u"2. Growth Potential MTBF (MGP): %f"
                          u"3. Fix Effectiveness Factor (FEF): %f")
                        % (mtbfi, mtbfgp, avefef))

    return _avems


def prob(t1, mtbfi, avems):
    """
    Function to calculate the probability of observing at least one failure.

    :param t1: the growth start time.  The time the first fix is implemented.
    :type t1: float
    :param mtbfi: the starting MTBF.
    :type mtbfi: float
    :param avems: the average management strategy across the entire program.
    :type avems: float
    :return: _prob; the probability of seeing at least one failure.
    :rtype: float
    """

    try:
        _prob = 1.0 - exp(-t1 * avems / mtbfi)
    except(ValueError, ZeroDivisionError):
        _prob = 0.0
        _util.rtk_error(_(u"To calculate the probability of observing a "
                          u"failure, you must provide the following "
                          u"inputs with values greater than zero: "
                          u"1. Growth start time (ti): %f"
                          u"2. Initial MTBF (MI): %f"
                          u"3. Management strategy (MS): %f")
                        % (t1, mtbfi, avems))

    return _prob


def growth_potential(mtbfi, avems, avefef):
    """
    Function to calculate the growth potential MTBF.

    :param float mtbfi: the initial MTBF.
    :param float avems: the management strategy.
    :param float avefef: the fix effectiveness factor.
    :return: _mtbfgp: the growth potnetial MTBF.
    :rtype: float
    """

    # If the management strategy and/or fix effectiveness factor are zero,
    # tell the user
    if avems * avefef == 0.0:
        _mtbfgp = mtbfi
        _util.rtk_error(_(u"To calculate the growth potential MTBF, "
                          u"you must provide the following inputs with "
                          u"values greater than zero:\n\n"
                          u"1. Initial MTBF (MI): %f\n"
                          u"2. Management strategy (MS): %f\n"
                          u"3. Fix Effectiveness Factor (FEF): %f\n\n")
                        % (mtbfi, avems, avefef))
        return True

    try:
        return mtbfi / (1.0 - avems * avefef)
    except(ValueError, ZeroDivisionError):
        _util.rtk_error(_(u"To calculate the growth potential MTBF, "
                          u"you must provide the following inputs with "
                          u"values greater than zero:"
                          u"1. Initial MTBF (MI): %f"
                          u"2. Management strategy (MS): %f"
                          u"3. Fix Effectiveness Factor (FEF): %f")
                        % (mtbfi, avems, avefef))
        return True


def planned_growth_curve(model, row, t1, mtbfi, gr):
    """
    Function to calculate the necessary values for each reliability growth
    test phase.  This is a wrapper function forthe growth_phase() function that
    allows the use of gtk.TreeModel().foreach()

    :param gtk.TreeModel model: the gtk.TreeModel() that called this function.
    :param gtk.TreeIter row: the first gtk.TreeIter().
    :param float t1: the length of the first test phase.
    :param float mtbfi: the initial program MTBF.
    :param float gr: the overall, average program growth rate.
    :return: False if successful or True if an error is encountered.
    :rtype: boolean
    """

    # Function to calculate the optimum growth rate for a test phase.
    _gr = lambda gr, mi, mf, ttt, t1: (ttt / t1)**gr + (mf / mi) * (gr - 1)

    # Set the length of first test phase.  If it is supplied use that,
    # otherwise use the growth start time.  If the length of the first test
    # phase is less than the growth start time, issue an information dialog
    # and return.
    _t1 = model.get_value(row, 4)
    if _t1 <= 0.0:
        _t1 = t1
    elif _t1 < t1:
        _util.rtk_information(_(u"The length of the first test phase must be "
                                u"equal to or longer than the growth start "
                                u"time.  You have entered the following:\n\n"
                                u"1. Growth start time: %f\n"
                                u"2. Length of first test phase: %f\n\n"
                                u"Please correct your inputs and try again.") %
                              (t1, _t1))

        _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)
        return True

    # This will be used to set the initial MTBF of phase i equal to the final
    # MTBF of phase i - 1.
    _mtbfi = mtbfi

    # Initialize some variables used to track cumulative values.
    i = 1
    _cum_failures = 0
    _previous_time = 0.0
    while row is not None:
        # Read user-supplied values, if any.
        _ttti = model.get_value(row, 4)         # Test time for phase i.
        _gri = model.get_value(row, 5)          # Growth rate for phase i.
        _ni = model.get_value(row, 6)           # Num of failures for phase i.
        _mtbfai = model.get_value(row, 7)       # Average MTBF for phase i.
        #_mtbfi = model.get_value(row, 8)        # Starting MTBF for phase i.
        _mtbff = model.get_value(row, 9)        # Final MTBF for phase i.

        # First make sure only one missing value exists for the test phase.
        # If not, inform the user and continue to the next test phase.
        if [_ttti, _t1, mtbfi, _mtbff, _gri, _ni, _mtbfai].count(0.0) > 3:
            _util.rtk_information(_(u"At least four of the following are "
                                    u"required to be provided for a test "
                                    u"phase.  The remaining values will be "
                                    u"calculated for the test phase.  For "
                                    u"test phase %d, you have entered:\n\n"
                                    u"1. Total test time: %f\n"
                                    u"2. Length of the first test phase: %f\n"
                                    u"3. Initial program MTBF: %f\n"
                                    u"4. Final phase MTBF: %f\n"
                                    u"5. Growth rate: %f\n"
                                    u"6. Number of phase failures: %d\n"
                                    u"7. Average phase MTBF: %f\n\n"
                                    u"Please correct your inputs and try "
                                    u"again.") %
                                  (i, _ttti, _t1, mtbfi, _mtbff, _gri,
                                   _ni, _mtbfai))
            i += 1
            row = model.iter_next(row)
            continue

        if _ttti <= 0.0:
            _ttti = total_time(_t1, _mtbfi, _mtbff, _gri, _mtbfai, _ni,
                               _previous_time)

        if _gri <= 0.0:
            _gri = fsolve(_gr, 0.01, (_mtbfi, _mtbff, _ttti, _t1))[0]

        if _mtbff <= 0.0:
           _mtbff = final_mtbf(_ttti, _t1, _mtbfi, _gri)

        # Calculate the expected number of failures for the phase and the
        # average MTBF for the phase.  Even if _mtbfa > 0.0, we need to
        # calculate the number of failures for possible use with subsequent
        # test phases.
        _ni, _mtbfa = average_mtbf(_ttti, _t1, mtbfi, _gri,
                                   _previous_time, _cum_failures)

        _previous_time = _ttti
        _cum_failures += _ni
        if _mtbfai <= 0.0:
            _mtbfai = _mtbfa
        i += 1

        # Update the gtk.TreeModel().
        model.set_value(row, 4, _ttti)
        model.set_value(row, 5, _gri)
        model.set_value(row, 6, ceil(_ni))  # No fractional failures.
        model.set_value(row, 7, _mtbfai)
        model.set_value(row, 8, _mtbfi)
        model.set_value(row, 9, _mtbff)

        _mtbfi = _mtbff

        row = model.iter_next(row)

    return False


def idealized_values(ttt, ti, mtbfi, mtbff, gr, mtbf=True):
    """
    Function to calculate the values for the idealized growth curve.

    :param float ttt: the total time on test for the program.
    :param float ti: the growth start time (i.e., the time the first fix is
                     implemented on a test article).
    :param float mtbfi: the initial MTBF for the test program.
    :param float mtbff: the final MTBF for the test program.
    :param float gr: the average growth rate across the entire test program.
    :param bool mtbf: indicates whether to calculate MTBF (default) or failure
                      intensity values.
    :return: _ideal
    :rtype: list of floats
    """

    # Function to calculate the growth rate necessary to have the ideal growth
    # curve end at the final MTBF.
    _gr = lambda gr, mi, mf, ttt, t1: (ttt / t1)**gr + (mf / mi) * (gr - 1)

    _ideal_gr = fsolve(_gr, 0.01, (mtbfi, mtbff, ttt, ti))[0]

    _time = 0.0
    _ideal = []

    # Build the idealized curve.  If the time is less than the time to
    # first fix, the idealized value is the initial MTBF.  If the time
    # is equal to the time to first fix, the idealized value is set to
    # numpy's not a number to force a jump in the plot.  If the time is
    # greater than the time to first failure, the idealized value is
    # calculated from the inputs read above.
    if mtbf:
        for i in range(int(ttt)):
            if _time < int(ti):
                _ideal.append(mtbfi)
            elif _time == int(ti):
                _ideal.append(np.nan)
            else:
                _ideal.append((mtbfi * (_time / ti) ** _ideal_gr) /
                              (1.0 - _ideal_gr))

            _time += 1.0
    else:
        for i in range(int(ttt)):
            if _time < int(ti):
                _ideal.append(1.0 / mtbfi)
            elif _time == int(ti):
                _ideal.append(np.nan)
            else:
                _ideal.append((1.0 - _ideal_gr) /
                              (mtbfi * (_time / ti) ** _ideal_gr))

            _time += 1.0

    return _ideal


def planned_values(ttt, mtbfa, mtbf=True):  # pylint: disable=C0103
    """
    Function to create the planned growth curve values.

    :param float ttt: the total test time.
    :param float mtbfa: the average MTBF for the test phase.
    :param boolean mtbf: indicates whether to calculate MTBF or failure rates.
    :return: _plan
    :rtype: list of floats
    """

    _time = 0.0
    _plan = []

    while _time < (ttt - 1.0):
        if mtbf:
            _plan.append(mtbfa)
        else:
            _plan.append(1.0 / mtbfa)

        _time += 1.0

    _plan.append(np.nan)                    # pylint: disable=E1101

    return _plan


# +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
# Following are the functions for the Duane model.                        #
# +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
def duane_parameters(F, X):
    """
    Function to estimate the parameters of the Duane model.  This is also used
    when regression is used to estimated the NHPP Power Law model parameters.
    The form of the Duane model used in RTK:

    .. note:: cumulative failure intensity = lambda_c = (1 / b) * T^-alpha
    .. note:: cumulative MTBF = MTBFc = b * T^alpha
    .. note:: instantaneous failure intensity = lambda_i = (1 - alpha) * lambda_c
    .. note:: instantaneous MTBF = MTBFi = MTBFc / (1 - alpha)

    :param int F: list of the number of failures at each failure time.
    :param float X: list of failure times
    :return: _b_hat, _alpha_hat
    :rtype: tuple of floats
    """

    _mtbfi = [X[i]/sum(F[:i+1]) for i in range(len(X))]
    _logT = sum([log(x) for x in X])
    _logT2 = sum([log(x)**2.0 for x in X])
    _logM = sum([log(m) for m in _mtbfi])
    _logTlogM = sum([log(X[i]) * log(_mtbfi[i]) for i in range(len(X))])

    try:
        _alpha_hat = (_logTlogM - (_logT * _logM / sum(F))) / \
                     (_logT2 - (_logT**2.0 / sum(F)))
    except ZeroDivisionError:
        _alpha_hat = 0.0

    try:
        _b_hat = exp((1.0 / sum(F)) * (_logM - _alpha_hat * _logT))
    except OverflowError:
        _b_hat = 1.0

    return _b_hat, _alpha_hat


def duane_standard_error(F, X, b, alpha):
    """
    Function to calculate the standard error of the Duane model parameters,
    b (scale) and alpha (shape), given the failure counts, failure times, and
    point estimates of the parameters.

    :param F: list of the number of failures at each failure time.
    :type F: list of integers
    :param X: list of failure times
    :type X: list of floats
    :param b: the point estimate of the alpha (shape) parameter.
    :type b: float
    :param alpha: the point estimate of the b (scale) parameter.
    :type alpha: float
    :return: _se_lnb, _se_beta; the variance of the parameters.
    :rtype: tuple of floats
    """

    _logT = sum([log(x) for x in X])
    _logT2 = sum([log(x)**2.0 for x in X])
    _mtbfi = [X[i]/sum(F[:i+1]) for i in range(len(X))]

    _SSE = sum([((log(b) + alpha * log(X[i])) - log(X[i] / sum(F[:i+1])))**2.0 for i in range(len(X))])
    if sum(F) > 2:
        _sigma2 = _SSE / (sum(F) - 2)
    else:
        _sigma2 = _SSE

    try:
        _Sxx = _logT2 - (_logT**2.0 / sum(F))
    except ZeroDivisionError:
        _Sxx = 1.0

    # Calculate the standard error of the b (scale) parameter.
    try:
        _se_lnb = sqrt(_sigma2) * sqrt(_logT2 / (sum(F) * _Sxx))
    except ZeroDivisionError:
        _se_lnb = 0.0

    try:
        _se_beta = sqrt(_sigma2) / sqrt(_Sxx)
    except ZeroDivisionError:
        _se_beta = 0.0

    # Calculate the cumulative MTBF confidence bounds multiplier.
    #_cum_cb_multiplier = _z_norm * sqrt(_sigma2)

    return _sigma2, _se_lnb, _se_beta


def duane_mean(b, alpha, T):
    """
    Function to calculate the Duane model cumulative and instantaneous mean
    values (e.g., MTBF) given the Duane parameters and a time.  The Duane model
    used is:

    cumulative mean = mean_c = b * T^alpha
    instantaneous mean = mean_i = mean_c / (1 - alpha)

    :param b: the Duane model scale parameter.
    :type b: float
    :param alpha: the Duane model shape parameter.
    :type alpha: float
    :param T: the time at which to calculate the means.
    :type T: float
    :return: _mean_c, _mean_i; the cumulative and instantaneous means at
                               time T.
    :rtype: tuple of floats
    """

    _mean_c = b * T**alpha
    _mean_i = _mean_c / (1.0 - alpha)

    return _mean_c, _mean_i


# +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
# Following are the functions for the Crow-AMSAA model.                   #
# +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
def beta_grouped(b, f, t, logt):
    """
    Function for estimating the beta value from grouped data.

    :param float b: guess for the Crow-AMSAA shape parameter.
    :param ndarray f:
    :param ndarray t:
    :param ndarray logt:
    """

    _beta = sum(f[1:] * ((t[1:]**b * logt[1:] - t[:-1]**b * logt[:-1]) /
                         (t[1:]**b - t[:-1]**b) - log(max(t))))

    return _beta


def crow_amsaa_parameters(F, X, T_star=0.0, grouped=False):
    """
    Function to estimate the parameters of the Crow-AMSAA model.  This is also
    used when MLE is used to estimated the NHPP Power Law model parameters.
    The form of the Crow-AMSAA model used in RTK:

    .. hlist::
       :columns: 1

        * cumulative failure intensity = lambda_c = lambda * T^(beta - 1)
        * cumulative MTBF = MTBFc = (1 / lambda) * T^(1- beta)
        * instantaneous failure intensity = lambda_i = lambda * beta * T^(beta - 1)
        * instantaneous MTBF = MTBFi = 1 / lambda_i

    :param F: list of the number of failures at each failure time.
    :type F: list of integers
    :param X: list of failure times
    :type X: list of floats
    :param T_star: the termination time for time terminated (Type I) tests.
    :type T_star: float
    :param grouped: indicates whether or not the failure times are exact
                    (default) or grouped.
    :type grouped: boolean
    :return: _lambda_hat, _beta_hat; point estimates of the Crow-AMSAA
             parameters.
    :rtype: tuple of floats
    """

    # Validate that the failure time and failure count lists are not empty.
    # If they are, raise an error and return 0.0 for both parameters.
    if F == [] or X == []:
        _util.rtk_error(_(u"The list of failure times and/or the list of "
                          u"failure counts is empty.  Cannot estimate "
                          u"Crow-AMSAA parameters without both."))
        return 0.0, 0.0

    # If a termination time is not provided, assume a failure terminated test
    # and set the termination time equal to the last failure time.
    if T_star <= 0.0:
        T_star = max(X)

    # Calculate the logarithm (base e) of the failure times.
    _logT = [log(x) for x in X]
    if not grouped:
        _beta_hat = [sum(F) / (sum(F) * log(T_star) - sum(_logT))]

    elif grouped:
        # Convert our Python lists to numpy arrays.  We need to insert a zero
        # in the first position for the _beta_grouped() function to work
        # properly.
        __failures = np.array([0.0] + F)
        __times = np.array([0.0] + X)
        __logt = np.array([0.0] + _logT)

        _initial_guess = sum(F) / (sum(F) * log(T_star) - sum(_logT))
        _beta_hat, _info, _ier, __ = fsolve(beta_grouped, _initial_guess,
                                            args=(__failures, __times, __logt),
                                            full_output=True)
        if _ier != 1:
            _util.rtk_information(_(u"The solution for the shape parameter "
                                    u"did not converge in %d iterations.  Try "
                                    u"using regression.") % _info['nfev'])
            return 0.0, 0.0

    _lambda_hat = sum(F) / T_star**_beta_hat[0]

    return _lambda_hat, _beta_hat[0]


def crow_amsaa_mean(_lambda, beta, T):
    """
    Function to calculate the Crow-AMSAA model cumulative and instantaneous
    mean values (e.g., MTBF) given the Crow-AMSAA parameters and a time.  The
    Crow-AMSAA model used is:

    .. math::
    cumulative mean &= mean_c = (1 / lambda) * T^((1 - beta) \\
    instantaneous mean &= mean_i = 1 / (lambda * beta * T^(beta - 1))

    :param _lambda: the Crow-AMSAA model scale parameter.
    :type _lambda: float
    :param beta: the Crow-AMSAA model shape parameter.
    :type beta: float
    :param T: the time at which to calculate the means.
    :type T: float
    :return: _mean_c, _mean_i; the cumulative and instantaneous means at
                               time T.
    :rtype: tuple of floats
    """

    try:
        _mean_c = (1.0 / _lambda) * T**(1.0 - beta)
    except ZeroDivisionError:
        _mean_c = np.inf
    try:
        _mean_i = 1.0 / (_lambda * beta * T**(beta - 1.0))
    except ZeroDivisionError:
        _mean_i = np.inf

    return _mean_c, _mean_i


def cramer_von_mises(X, beta, T_star=0.0, type2=True):
    """
    Function to calculate the Cramer-von Mises GoF statistic to test whether or
    not a set of data fits to the Crow-AMSAA model.  This is used when failure
    times are exact.

    .. note:: The null hypothesis is rejected if the statistic exceeds the
              critical value for a chosen significance level.

    :param float X: list of failure times
    :param float beta: the Crow-AMSAA model shape parameter.
    :param float T_star: termination time.
    :param boolean type2: whether or not the test is time terminated (Type I)
                          or failure terminated (Type II).
    :return: _Cvm, the Cramer-von Mises GoF statistic.
    :rtype: float
    """

    # If the test was failure terminated (Type II), set the termination time
    # equal to the last failure time and unbias the beta estimate.
    if type2:
        T_star = X[-1]
        _M = len(X) - 1
    else:
        _M = len(X)

    _ei = sum([(((X[i] / T_star)**beta) - (((2.0 * (i + 1)) - 1.0) / (2.0 * _M)))**2.0 for i in range(_M)])

    _Cvm = _ei / (12.0 * _M)

    return _Cvm


def crow_amsaa_chi_square(F, X, _lambda, beta, grouped=True):
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

    :param F: list of the number of failures at each failure time.
    :type F: list of integers
    :param X: list of failure times
    :type X: list of floats
    :param _lambda: the Crow-AMSAA model scale parameter.
    :type _lambda: float
    :param beta: the Crow-AMSAA model shape parameter.
    :type beta: float
    :param grouped: indictes whether data is exact (default) or grouped.
    :type grouped: boolean
    :return: _chi-square; the chi-square statistic
    :rtype: float
    """

    if not grouped:
        _chi_square = 2.0 * sum(F) / beta

    elif grouped:
        _X = [0.0] + X
        _theta = [_lambda* (_X[i]**beta - _X[i - 1]**beta) for i in range(1, len(_X))]

        _chi_square = sum([((F[i] - _theta[i])**2.0 / _theta[i]) for i in range(len(_theta))])

    return _chi_square


# +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
# Following are the functions for confidence bounds.                      #
# +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
def var_covar(N, T, alpha, beta):
    """
    Function to calculate the variance-covariance matrix for the NHPP - Power
    Law model parameters.  Used for Crow-AMSAA models too.

    :param int N: total number of failures in the data set.
    :param float T: total observation time or maximum failure time.
    :param float alpha: the point estimate of the alpha (scale) parameter.
    :param float beta: the point estimate of the beta (shape) parameter.
    :return: the variance-covariance matrix for alpha and beta.  It has the
             form:
                    [[Var(alpha), Cov(alpha, beta)],
                     [Cov(alpha, beta), Var(beta)]]
    :rtype: list of lists
    """

    try:
        _del_alpha = -N / alpha**2.0
    except ZeroDivisionError:
        _del_alpha = 1.0

    try:
        _del_beta = -N / beta**2.0 - alpha * T**beta * log(T)**2.0
    except ZeroDivisionError:
        _del_beta = 1.0

    _del_beta_alpha = -T**beta * log(T)

    _var_covar = inv(np.array([[-_del_alpha, -_del_beta_alpha],
                               [-_del_beta_alpha, -_del_beta]]))

    return _var_covar


def nhpp_mean_variance(N, T, alpha, beta, metric=1):
    """
    Function to calculate the variance for the NHPP - Power Law model
    cumulative or instantaneous means.  Used for Crow-AMSAA models too.

    :param N: total number of failures in the data set.
    :type N: integer
    :param T: total observation time or maximum failure time.
    :type T: float
    :param alpha: the point estimate of the alpha (scale) parameter.
    :type alpha: float
    :param beta: the point estimate of the beta (shape) parameter.
    :type beta: float
    :param metric: the metric to calculate the variance for.
                   - 1 = Cumulative MTBF.
                   - 2 = Instantaneous MTBF.
    :type metric: integer
    :return: the variance of the selected mean.
    :rtype: float
    """

    _var_covar = var_covar(N, T, alpha, beta)

    if metric == 1:
        _del_mean_beta = -(1.0 / alpha) * T**(1.0 - beta) * log(T)
        _del_mean_alpha = -(1.0 / alpha**2.0) * T**(1.0 - beta)
    elif metric == 2:
        _del_mean_beta = -(1.0 / (alpha * beta**2.0)) * T**(1.0 - beta) - \
                         (1.0 / (alpha * beta)) * T**(1.0 - beta) * log(T)
        _del_mean_alpha = -(1.0 / (alpha**2.0 * beta)) * T**(1.0 - beta)

    _variance = _del_mean_beta**2.0 * _var_covar[1][1] + \
                _del_mean_alpha**2.0 * _var_covar[0][0] + \
                2.0 * _del_mean_beta * _del_mean_alpha * _var_covar[0][1]

    return _variance


def fisher_bounds(metric, variance, alpha):
    """
    Function to calculate the Fisher Information Matrix based confidence
    bounds.

    :param metric: the point estimate of the metric to calculate bounds for.
    :type metric: float
    :param variance: the variance of the metric to calculate bounds for.
    :type variance: float
    :param alpha: the confidence level of the calculated bounds.
    :type alpha: float
    :return: _fisher_l, _fisher_u; the lower and upper Fisher bounds.
    :rtype: tuple of floats
    """

    # Ensure the confidence level is expressed as a decimal, then find the
    # standard normal value for constructing the confidence bounds.
    if alpha > 1.0:
        alpha = alpha / 100.0
    _z_norm = norm.ppf(alpha)

    _fisher_l = metric * exp(-_z_norm * sqrt(variance) / metric)
    _fisher_u = metric * exp(_z_norm * sqrt(variance) / metric)

    return _fisher_l, _fisher_u


def crow_bounds(N, T_star, _lambda, beta, alpha, metric, type=2):
    """
    Function to calculate confidence bounds based on Dr. Larry Crow's methods.

    :param N: the total number of failures in the data set.
    :type N: integer
    :param T_star: termination time.
    :type T_star: float
    :param _lambda: the estimated scale parameter.
    :type _lambda: float
    :param beta: the estimated shape parameter.
    :type beta: float
    :param alpha: the desired confidence level of the bounds.
    :param alpha: float
    :param metric: indicates which metric the bounds are being calculated for.
                    1 = shape (beta)
                    2 = scale (lambda)
                    3 = cumulative failure intensity
                    4 = instantaneous MTBF (future)
    :type metric: integer
    :param type: the type of data set being passed.
                    1 = Type I or time terminated test
                    2 = Type II or failure terminated test
    :type type: integer
    :return: _crow_l, _crow_u; the lower and upper bound on the metric.
    :rtype: tuple of floats
    """

    # Set default values so a value is returned in case something goes wrong.
    _crow_l = 1.0
    _crow_u = 1.0

    # Ensure the confidence level is expressed as a decimal.
    if alpha > 1.0:
        alpha = alpha / 100.0

    _alpha_l = (1.0 - alpha) / 2.0          # For lower bounds.
    _alpha_u = 1.0 - _alpha_l               # For upper bounds.

    if metric == 1:                         # Shape
        if type == 1:
            _chi2 = chi2.ppf(_alpha_l, 2.0 * N)
            _crow_l = beta * (_chi2 / (2.0 * (N - 1)))

            _chi2 = chi2.ppf(_alpha_u, 2.0 * N)
            _crow_u = beta * (_chi2 / (2.0 * (N - 1)))

        elif type == 2:
            _chi2 = chi2.ppf(_alpha_l, 2.0 * (N - 1))
            _crow_l = beta * ((N * _chi2) / (2.0 * (N - 1) * (N - 2)))

            _chi2 = chi2.ppf(_alpha_u, 2.0 * (N - 1))
            _crow_u = beta * ((N * _chi2) / (2.0 * (N - 1) * (N - 2)))

    elif metric == 2:                       # Scale
        # Calculate the lower bound.  It is the same regardless of the type.
        _chi2 = chi2.ppf(_alpha_l, 2.0 * N)
        _crow_l = _chi2 / (2.0 * T_star**beta)

        if type == 1:
            _chi2 = chi2.ppf(_alpha_u, 2.0 * (N + 2))
            _crow_u = _chi2 / (2.0 * T_star**beta)
        elif type == 2:
            _chi2 = chi2.ppf(_alpha_u, 2.0 * N)
            _crow_u = _chi2 / (2.0 * T_star**beta)

    elif metric == 3:                       # Cum. failure intensity
        # Calculate the lower bound.  It is the same regardless of the type.
        _chi2 = chi2.ppf(_alpha_l, 2.0 * N)
        _crow_l = _chi2 / (2.0 * T_star)

        if type == 1:
            _chi2 = chi2.ppf(_alpha_u, 2.0 * (N + 2))
            _crow_u = _chi2 / (2.0 * T_star)
        elif type == 2:
            _chi2 = chi2.ppf(_alpha_u, 2.0 * N)
            _crow_u = _chi2 / (2.0 * T_star)

    return _crow_l, _crow_u


# +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
# Following are the functions for NHPP models.                            #
# +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
def power_law(F, X, confmeth, fitmeth=1, conftype=3,
              alpha=0.75, T_star=0.0):
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
    :param float T_star: the end of the observation period for time terminated,
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
    if T_star == 0.0:
        T_star = max(X)
        _typeii = True

    if not _typeii:
        _N = sum(F) - 1
    else:
        _N = sum(F) - 2

    if fitmeth == 1:                        # MLE
        # Estimate the Crow-AMASAA parameters using exact failure time data.
        _alpha_hat, _beta_hat = crow_amsaa_parameters(F, X, T_star)

        if confmeth == 1:                   # Crow bounds.
            # Calculate the bounding values for the alpha (scale) parameter.
            _alpha_lower, _alpha_upper = crow_bounds(_N, T_star, _alpha_hat,
                                                     _beta_hat, alpha, 2)

            # Calculate the bounding values for the beta (shape) parameter.
            _beta_lower, _beta_upper = crow_bounds(_N, T_star, _alpha_hat,
                                                   _beta_hat, alpha, 1)

        elif confmeth == 3:                 # Fisher matrix bounds.
            # Calculate the variance-covariance matrix for the NHPP - Power Law
            # parameters.

            _var_covar = var_covar(sum(F), T_star, _alpha_hat, _beta_hat)

            # Calculate the bounding values for the alpha (scale) parameter.
            _alpha_lower, _alpha_upper = fisher_bounds(_alpha_hat,
                                                       _var_covar[0][0],
                                                       alpha)

            # Calculate the bounding values for the beta (shape) parameter.
            _beta_lower, _beta_upper = fisher_bounds(_beta_hat,
                                                     _var_covar[1][1],
                                                     alpha)

    elif fitmeth == 2:                        # Regression
        # Estimate the Duane parameters and transform to the NHPP - Power Law
        # parameters.
        _b_hat, _beta_hat = duane_parameters(F, X)
        _alpha_hat = 1.0 / _b_hat

        # Calculate the standard errors on the parameter estimates.
        _sigma2, _se_lnb, _se_beta = duane_standard_error(F, X, _b_hat,
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
