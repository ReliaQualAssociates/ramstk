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


def power_law(_F_, _X_, _T_=0.0):
    """
    Function to estimate the parameters (beta and alpha) of the NHPP power law
    model.

    Keyword Arguments:
    F -- list of failure counts.
    X -- list of individual failures times.
    T -- the end of the observation period.
    """

    _typeii_ = False

# Sort the failure times ascending.
    _X_.sort()

# If no observation time was passed, use the maximum failure time.
    if(_T_ == 0.0):
        _T_ = max(_X_)
        _typeii_ = True

    if(not _typeii_):
        _N_ = len(_X_) - 1
    else:
        _N_ = len(_X_)

    _log_t_ = 0.0
    _mu_ = [_X_[0] / _F_[0]]
    for i in range(1, _N_):
# Find the total number of failures to date.
        _r_ = sum(_F_[0:i])

# Estimate the reliability growth slope.
        _log_t_ += log(_T_ / _X_[i])
        _beta_hat_ = 1 - ((_r_ - 1) / _log_t_)

# Estimate the scale parameter.
        try:
            _alpha_hat_ = _r_ / _T_**(1 - _beta_hat_)
        except OverflowError:
            print _r_, _T_, _beta_hat_

# Estimate the MTBF at the end of the test or observation period.
        try:
            _mu_.append(sum(_X_[0:i]) / _r_)
        except ZeroDivisionError:
            print i, _T_, _r_, _beta_hat_

    _mu_.append(_T_ / _r_ * (1 - _beta_hat_))

    return(_beta_hat_, _alpha_hat_, _mu_)


def crow_amsaa_continuous(F, X, I, _grouped=False):
    """
    Function to estimate the parameters (beta and lambda) of the AMSAA-Crow
    continous model using either the Option for Individual Failure Data
    (default) or the Option for Grouped Failure Data.

    Keyword Arguments:
    F        -- list of failure counts.
    X        -- list of individual failures times.
    I        -- the grouping interval width.
    _grouped -- whether or not to use grouped data.
    """

    from scipy.optimize import fsolve

# Define the function that will be set equal to zero and solved for beta.
    def _beta(b, f, t, logt):
        """ Function for estimating the beta value from grouped data. """

        return(sum(f[1:] * ((t[1:]**b * logt[1:] - t[:-1]**b * logt[:-1]) / (t[1:]**b - t[:-1]**b) - log(max(t)))))

# Find the total time on test.
    TTT = X[len(X) - 1:][0]
    FFF = sum(F)

    _rho = []
    _mu = []

    if(not _grouped):
        for i in range(len(X)):
            try:
                _iters = int(X[i] - X[i - 1])
            except IndexError:
                _iters = int(X[i])

# Estimate the failure rate of this interval.
            for j in range(_iters - 1):
                _rho.append(np.nan)

            try:
                _rho_ = F[i] / (X[i] - X[i - 1])
            except IndexError:
                _rho_ = F[i] / X[i]
            except ZeroDivisionError:
                _rho_ = _rho[i - 1]

            if(_rho_ < 0):
                _rho_ = 0.0
            _rho.append(_rho_)

# Estimate the MTBF of this interval.
            for j in range(_iters - 1):
                _mu.append(np.nan)

            try:
                _mu_ = (X[i] - X[i - 1]) / F[i]
            except IndexError:
                _mu_ = X[i] / F[i]
            except ZeroDivisionError:
                _mu_ = _mu[i - 1]

            if(_mu_ < 0):
                _mu_ = 0.0

            _mu.append(_mu_)

        logX = [log(x) for x in X]

        _beta_hat = (FFF / (FFF * log(TTT) - sum(logX)))
        _lambda_hat = FFF / TTT**_beta_hat

    elif(_grouped):
# Calculate the number of intervals we need, then create a list of zeros the
# same length as the number of intervals.
        _num_intervals = int(ceil(TTT / I))
        _cum_fails = [0] * _num_intervals

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
