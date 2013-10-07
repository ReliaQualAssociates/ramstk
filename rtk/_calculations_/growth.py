#!/usr/bin/env python
""" Contains functions for performing calculations associated with
    reliability growth. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

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
from math import ceil, exp, floor, log, sqrt

# Import other RTK modules.
import configuration as _conf
import utilities as _util


def idealized_growth_curve(MTBFI, MTBFF, TTT, t1, AvgMS, AvgGR=0.3, Prob=0.8,
                           AvgFEF=0.7, FixProb=False, FixMS=False,
                           FixTTFF=False, FixTTT=False, FixMTBFI=False,
                           FixMTBFG=False, FixGR=False):
    """
    Function to calculate the idealized growth curve for a reliability growth
    progams.

    Keyword Arguments:
    MTBFI    -- the starting MTBF.
    MTBFF    -- the final MTBF.
    TTT      -- the total time on test.  Summed across all phases.
    AvgGR    -- the average growth rate for the program.
    t1       -- the growth start time.  The time the first fix is implemented.
    AvgMS    -- the average management strategy across the entire program.
    Prob     -- the probability of observing at least one failure.
    AvgFEF   -- the average fix effectiveness factor across the program.
    FixProb  --
    FixMS    --
    FixTTFF  --
    FixTTT   --
    FixMTBFI --
    FixMTBFG --
    FixGR    --
    """

    MTBFGP = MTBFI / (1.0 - AvgMS * AvgFEF)

# Calculate the probability of seeing at least one failure.
    if(not FixProb):
        try:
            Prob = 1.0 - exp(-1.0 * (t1 * AvgMS / MTBFI))
        except(ValueError, ZeroDivisionError):
            Prob = 0.0
            print "You must provide three of the four inputs: ti, MI, MS, Prob"

# Calculate the management strategy.
    if(not FixMS):
        try:
            AvgMS = log(1.0 - Prob) * MTBFI / (-1.0 * t1)
        except(ValueError, ZeroDivisionError):
            AvgMS = 0.0
            print "You must provide three of the four inputs: ti, MI, MS, Prob"

# Calculate the minimum length of the first test phase.
    if(not FixTTFF):
        try:
            t1 = log(1.0 - Prob) * MTBFI / (-1.0 * AvgMS)
        except(ValueError, ZeroDivisionError):
            t1 = 0.0
            print "You must provide three of the four inputs: ti, MI, MS, Prob"

# Calculate total test time.
    if(not FixTTT):
        try:
            TTT = exp(log(t1) + 1.0 / AvgGR * (log(MTBFF /MTBFI) + log(1.0 - AvgGR)))
        except(ValueError, ZeroDivisionError):
            TTT = 0.0
            print "You must provide four of the five inputs: GR, TI, ti, MI, MF"

# Calculate initial MTBF.
    if(not FixMTBFI):
        try:
            MTBFI = (-1.0 * t1 * AvgMS) / log(1.0 - Prob)
        except (ValueError, ZeroDivisionError):
            try:
                MTBFI = MTBFF / exp(AvgGR * (0.5 * AvgGR + log(TTT / t1) + 1.0))
            except (ValueError, ZeroDivisionError):
                MTBFI = 0.0
                #try:
                #    MTBFI = (t1 * (TTT / t1)**(1.0 - AvgGR)) / N
                #except (ValueError, ZeroDivisionError):
                #    MTBFI = 0.0

# Calculate final MTBF.
    if(not FixMTBFG):
        try:
            MTBFF = MTBFI * exp(AvgGR * (0.5 * AvgGR + log(TTT / t1) + 1.0))
        except(ValueError, ZeroDivisionError):
            MTBFF = 0.0
            print "You must provide four of the five inputs: GR, TI, ti, MI, MF"

# Calculate the growth rate.
    if(not FixGR):
        try:
            AvgGR = -log(TTT / t1) - 1.0 + sqrt((1.0 + log(TTT / t1))**2.0 + 2.0 * log(MTBFF / MTBFI))
        except(ValueError, ZeroDivisionError):
            AvgGR = 0.0
            print "You must provide four of the five inputs: GR, TI, ti, MI, MF"

    return(MTBFGP, Prob, AvgMS, t1, TTT, MTBFI, MTBFF, AvgGR)


def calculate_rg_phase(model, row, GR, MS, FEF, Prob, ti):
    """
    Function to calculate the planning values for an individual reliability
    growth phase.

    Keyword Arguments:
    model -- the gtk.TreeModel containing the RG phase information.
    row   -- the selected gtk.Iter containning the specific RG phase
             information.
    MS    -- the management strategy for this program.
    FEF   -- the average FEF for this program.
    Prob  -- the probability of seeing one failure.
    ti    -- the growth start time; time to first fix for this program.
    """

# Read the RG phase-specific values.
    TTTi = model.get_value(row, 4)
    MTBFi = model.get_value(row, 6)
    MTBFf = model.get_value(row, 7)
    MTBFa = model.get_value(row, 8)

# Calculate the average growth rate for the phase.
    if(GR == 0.0 or GR == '' or GR is None):
        try:
            GRi = -log(TTTi / ti) - 1.0 + sqrt((1.0 + log(TTTi / ti))**2.0 + 2.0 * log(MTBFf / MTBFi))
        except(ValueError, ZeroDivisionError):
            GRi = 0.0
    else:
        GRi = GR

    model.set_value(row, 5, GRi)

# Calculate initial MTBF for the phase.
    if(MTBFi == 0.0 or MTBFi == '' or MTBFi is None):
        try:
            MTBFi = (-1.0 * ti * MS) / log(1.0 - Prob)
        except(ValueError, ZeroDivisionError):
            try:
                MTBFi = MTBFf / exp(GRi * (0.5 * GRi + log(TTTi / ti) + 1.0))
            except(ValueError, ZeroDivisionError):
                try:
                    MTBFi = (ti * (TTTi / ti)**(1.0 - GRi)) / Ni
                except(ValueError, ZeroDivisionError):
                    MTBFi = 0.0
        model.set_value(row, 6, MTBFi)

# Calculate final MTBF for the phase.
    if(MTBFf == 0.0 or MTBFf == '' or MTBFf is None):
        try:
            MTBFf = MTBFi * exp(GRi * (0.5 * GRi + log(TTTi / ti) + 1.0))
        except (ValueError, ZeroDivisionError):
            MTBFf = 0.0
        model.set_value(row, 7, MTBFf)

# Calculate total test time for the phase.
    if(TTTi == 0.0 or TTTi == '' or TTTi is None):
        try:
            TTTi = exp(log(ti) + 1.0 / GRi * (log(MTBFf /MTBFi) + log(1.0 - GRi)))
        except(ValueError, ZeroDivisionError):
            TTTi = 0.0
        model.set_value(row, 4, TTTi)

    return(GRi, TTTi)


def power_law(_F_, _X_, _fitmeth_, _type_, _conf_=0.75, _T_star_=0.0):
    """
    Function to estimate the parameters (beta and alpha) of the NHPP power law
    model.

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

    from scipy.stats import chi2, norm, t

# Initialize variables.
    _n_ = 0.0
    _T_ = 0.0
    _M_ = 0.0
    _logT_ = 0.0
    _logT2_ = 0.0
    _logM_ = 0.0
    _logTlogM_ = 0.0
    _SSE_ = 0.0

    _typeii_ = False

    _power_law_ = []

    _z_norm_ = norm.ppf(_conf_)

# If no observation time was passed, use the maximum failure time and set the
# _typeii_ variable True to indicate this is a failure truncated dataset.
    if(_T_star_ == 0.0):
        _T_star_ = sum(_X_)
        _typeii_ = True

    if(not _typeii_):
        _N_ = len(_X_) - 1
    else:
        _N_ = len(_X_) - 2

    for i in range(len(_X_)):

# Increment the total number of failures and the total time on test then
# calculate the cumulative MTBF.
        _n_ += float(_F_[i])
        _T_ += float(_X_[i])
        _M_ = _T_ / _n_

# Calculate interim values.
        _logT_ += log(_T_)
        _logT2_ += log(_T_)**2.0
        _logM_ += log(_M_)
        _logTlogM_ += log(_T_) * log(_M_)

# Calculate the Duane parameters.
        if(_fitmeth_ == 1):             # MLE
            try:
                _beta_hat_ = _n_ / (_n_ * log(_T_star_) - _logT_)
            except ZeroDivisionError:
                _beta_hat_ = 1.0
            _alpha_hat_ = 1.0 - _beta_hat_
            _lambda_hat_ = _n_ / _T_**_beta_hat_
            _b_hat_ = 1.0 / _lambda_hat_

        elif(_fitmeth_ == 2):           # Regression
            try:
                _alpha_hat_ = (_n_ * _logTlogM_ - _logT_ * _logM_) / (_n_ * _logT2_ - _logT_**2.0)
            except ZeroDivisionError:
                _alpha_hat_ = 0.0
            _b_hat_ = exp((1.0 / _n_) * (_logM_ - _alpha_hat_ * _logT_))

# Calculate the cumulative and instantaneous MTBF from the model.
        _mc_hat_ = _b_hat_ * _T_**_alpha_hat_
        _mi_hat_ = _mc_hat_ / (1.0 - _alpha_hat_)

# Calculate the cumulative and instantaneous failure intensity.
        _lc_hat_ = (1.0 / _b_hat_) * _T_**-_alpha_hat_
        _li_hat_ = (1.0 - _alpha_hat_) * _lc_hat_

# Calculate bounds on the Duane parameters.
        if(_n_ >= 2):
            _critical_value_t_ = t.ppf(_conf_, _n_ - 2)
        else:
            _critical_value_t_ = 0.0

        _SSE_ += (log(_mc_hat_) - log(_M_))**2.0
        try:
            _sigma2_ = _SSE_ / (_n_ - 2.0)
            _Sxx_ = _logT2_ - (_logT_**2.0 / _n_)
            _se_alpha_ = sqrt(_sigma2_) / sqrt(_Sxx_)
            _se_b_ = sqrt(_sigma2_) * sqrt(_logT2_ / (_n_ * _Sxx_))
        except ZeroDivisionError:
            _sigma2_ = 1.0
            _Sxx_ = 1.0
            _se_alpha_ = 1.0
            _se_b_ = 1.0

        _alpha_lower_ = _alpha_hat_ - _critical_value_t_ * _se_alpha_
        _alpha_upper_ = _alpha_hat_ + _critical_value_t_ * _se_alpha_

        _b_lower_ = _b_hat_ * exp(-_critical_value_t_ * _se_b_)
        _b_upper_ = _b_hat_ * exp(_critical_value_t_ * _se_b_)

# Calculate bounds on the MTBF.
        _mc_lower_ = _mc_hat_ * exp(-_z_norm_ * sqrt(_sigma2_))
        _mc_upper_ = _mc_hat_ * exp(_z_norm_ * sqrt(_sigma2_))

        _mi_lower_ = _mc_lower_ / (1.0 - _alpha_hat_)
        _mi_upper_ = _mc_upper_ / (1.0 - _alpha_hat_)

# Calculate bounds on the failure intensity.
        _lc_lower_ = 1.0 / _mc_upper_
        _lc_upper_ = 1.0 / _mc_lower_
        _li_lower_ = 1.0 / _mi_upper_
        _li_upper_ = 1.0 / _mi_lower_

        _power_law_.append([_T_, _n_, _M_,
                            _alpha_lower_, _alpha_hat_, _alpha_upper_,
                            _b_lower_, _b_hat_, _b_upper_,
                            _mc_lower_, _mc_hat_, _mc_upper_,
                            _mi_lower_, _mi_hat_, _mi_upper_,
                            _lc_lower_, _lc_hat_, _lc_upper_,
                            _li_lower_, _li_hat_, _li_upper_])

    return(_power_law_)


def crow_amsaa_continuous(_F_, _X_, _I_, _grouped_=False):
    """
    Function to estimate the parameters (beta and lambda) of the AMSAA-Crow
    continous model using either the Option for Individual Failure Data
    (default) or the Option for Grouped Failure Data.

    Keyword Arguments:
    _F_        -- list of failure counts.
    _X_        -- list of individual failures times.
    _I_        -- the grouping interval width.
    _grouped_ -- whether or not to use grouped data.
    """

    from scipy.stats import chi2, norm, t
    from scipy.optimize import fsolve

# Initialize variables.
    _n_ = 0.0
    _T_ = 0.0
    _M_ = 0.0
    _logT_ = 0.0
    _logT2_ = 0.0
    _logM_ = 0.0
    _logTlogM_ = 0.0
    _SSE_ = 0.0

    _typeii_ = False

    _power_law_ = []

    _t_norm_ = t.ppf(_conf_, _n_ - 2)
    _z_norm_ = norm.ppf(_conf_)

# If no observation time was passed, use the maximum failure time and set the
# _typeii_ variable True to indicate this is a failure truncated dataset.
    if(_T_star_ == 0.0):
        _T_star_ = sum(_X_)
        _typeii_ = True

    if(not _typeii_):
        _N_ = len(_X_) - 1
    else:
        _N_ = len(_X_) - 2

# Define the function that will be set equal to zero and solved for beta.
    def _beta(b, f, t, logt):
        """ Function for estimating the beta value from grouped data. """

        return(sum(f[1:] * ((t[1:]**b * logt[1:] - t[:-1]**b * logt[:-1]) / (t[1:]**b - t[:-1]**b) - log(max(t)))))

# Find the total time on test.
    TTT = X[len(X) - 1:][0]
    FFF = sum(F)

    _rho = []
    _mu = []

    if(not _grouped_):

        for i in range(len(_X_)):
# Increment the total number of failures and the total time on test then
# calculate the cumulative MTBF.
            _n_ += float(_F_[i])
            _T_ += float(_X_[i])

# Calculate interim values.
            _logT_ += log(_T_)

# Calculate the Duane parameters.
            try:
                _beta_hat_ = _n_ / (_n_ * log(_T_star_) - _logT_)
            except ZeroDivisionError:
                _beta_hat_ = 1.0
            _lambda_hat_ = _n_ / _T_**_beta_hat_

# Calculate the cumulative MTBF from the model.
            _mc_hat_ = (1.0 / _lambda_hat_) * _T_**(1.0 - _beta_hat_)
            _mi_hat_ = _beta_hat_ * _mc_hat_

# Calculate the cumulative failure intensity from teh model.
            _lc_hat_ = _lambda_hat_ * _T_**(_beta_hat_ - 1.0)
            _li_hat_ = _beta_hat_ * _lc_hat_

            _power_law_.append([_T_, _alpha_lower_, _alpha_hat_, _alpha_upper_,
                                _b_lower_, _b_hat_, _b_upper_,
                                _mc_lower_, _mc_hat_, _mc_upper_,
                                _mi_lower_, _mi_hat_, _mi_upper_,
                                _lc_lower_, _lc_hat_, _lc_upper_,
                                _li_lower_, _li_hat_, _li_upper_])

    elif(_grouped_):
# Calculate the number of intervals we need, then create a list of zeros the
# same length as the number of intervals.
        _num_intervals_ = int(ceil(TTT / I))
        _cum_fails_ = [0] * _num_intervals_

# Iterate through the data and count the nuber of failures in each interval.
        for i in range(len(X)):
            for j in range(_num_intervals):
                if(X[i] > j * I and X[i] <= (j + 1) * I):
                    _cum_fails[j] += F[i]

        for j in range(_num_intervals):
# Estimate the failure rate of this interval.
            try:
                _rho.extend([_cum_fails[j] / I] * (int(I) - 1))
            except ZeroDivisionError:
                try:
                    _rho.extend([_rho[j - 1]] * (int(I) - 1))
                except IndexError:
                    _rho.extend([0.0] * (int(I) - 1))
            _rho.append(np.nan)

# Estimate the MTBF of this interval.
            try:
                _mu.extend([I / _cum_fails[j]] * (int(I) - 1))
            except ZeroDivisionError:
                try:
                    _mu.extend([_mu[j - 1]] * (int(I) - 1))
                except IndexError:
                    _mu.extend([0.0] * (int(I) - 1))
            _mu.append(np.nan)

        f = [0]
        t = [1]
        logt = [0]
        for i in range(len(X)):
            f.append(F[i])
            t.append(X[i])
            logt.append(log(X[i]))

        f = np.array(f)
        t = np.array(t)
        logt = np.array(logt)

        _beta_hat = fsolve(_beta, 1.0, args=(f, t, logt))[0]
        _lambda_hat = FFF / TTT**_beta_hat

# Append non-plotting values to pad the failure rate and MTBF lists so they
# have the same length as everything else being plotted.
    if(len(_rho) < int(TTT)):
        for j in range(int(TTT) - len(_rho)):
            _rho.append(np.nan)
            _mu.append(np.nan)

    return(_beta_hat, _lambda_hat, _rho, _mu)
