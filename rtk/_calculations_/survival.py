#!/usr/bin/env python
""" Contains functions for performing non-parametric and parametric
    survival analyses. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

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
from math import ceil, exp, floor, log, sqrt

# Import other RTK modules.
import configuration as _conf
import utilities as _util


def mean_cumulative_function(units, times, data, _conf_=0.75):
    """ This function estimates the mean cumulative function for a population
        of items.

        Keyword Argumesnts:
        units  -- list of unique unit ID's in the dataset.
        times  -- list of unique failure times in the dataset.
        data   -- a data.frame or matrix where:
                  Column 0 is the failed unit id.
                  Column 1 is the left of the interval.
                  Column 2 is the right of the interval.
                  Column 3 is the interarrival time.
        _conf_ -- the confidence level of the KM estimates (default is 75%).
    """

    from scipy.stats import norm

# Determine the confidence bound z-value.
    _z_norm_ = norm.ppf(_conf_)

    _m_ = len(units)
    _n_ = len(times)

    datad = []

    for i in range(len(data)):
        datad.append(data[i])
    data = np.asarray(data)
    datad = np.asarray(datad)

    _d_ = np.zeros(shape=(_m_, _n_))
    _delta_ = np.zeros(shape=(_m_, _n_))

    for i in range(_n_):
        k = np.where(data[:, 2] == str(times[i]))    # Array of indices with failure times equal to the current unique failure time.
        _u_ = np.array(data[k, 0])[0].tolist()       # List of units whose failure time is equal to the current unique failure time.
        for j in range(len(_u_)):
            k = [a for a, x in enumerate(units) if x == _u_[j]]     #
            _delta_[k, 0:i+1] = 1

    for i in range(_n_):
        k = np.where(datad[:, 2] == str(times[i]))   # Array of indices with failure times equal to the current unique failure time.
        _u_ = np.array(datad[k, 0])[0].tolist()      # List of units whose failure time is equal to the current unique failure time.
        _q_ = np.array(datad[k, 4], dtype=int)[0].tolist()   # Quantity of failure times equal to the current unique failure time.
        for j in range(len(_u_)):
            k = [a for a, x in enumerate(units) if x == _u_[j]]     #
            if(max(_q_) > 1):
                _d_[k, i] = _q_[j]
            else:
                _d_[k, i] += _q_[j]

    _delta_ = _delta_.transpose()
    _d_ = _d_.transpose()

    _delta_dot = _delta_.sum(axis=1)
    _d_dot = (_d_ * _delta_).sum(axis=1)
    _d_bar = _d_dot / _delta_dot

    _MCF_ = []
    _x_ = (_delta_.transpose() / _delta_dot).transpose()
    _y_ = (_d_.transpose() - _d_bar).transpose()
    muhatp = 0.0
    _llp_ = 0.0
    _ulp_ = 0.0
    for i in range(len(times)):
        muhat = _d_bar[0:i+1].sum(axis=0)

# Estimate the variance.
        _z_ = (_x_[0:i+1] * _y_[0:i+1])
        _var_ = ((_z_.sum(axis=0))**2).sum(axis=0)

# Calculate the lower and upper bound on the MCF.
        _ll_ = muhat - _z_norm_ * sqrt(_var_)
        _ul_ = muhat + _z_norm_ * sqrt(_var_)

# Estimate the cumulative MTBF.
        _mtbfc_ = times[i] / muhat
        _mtbfcll_ = times[i] / _ul_
        _mtbfcul_ = times[i] / _ll_

# Estimate the instantaneous MTBF.
        if(i > 0):
            _mtbfi_ = (times[i] - times[i - 1]) / (muhat - muhatp)
            _mtbfill_ = (times[i] - times[i - 1]) / (_ul_ - _ulp_)
            _mtbfiul_ = (times[i] - times[i - 1]) / (_ll_ - _llp_)
        else:
            _mtbfi_ = times[i] / (muhat - muhatp)
            _mtbfill_ = times[i] / (_ul_ - _ulp_)
            _mtbfiul_ = times[i] / (_ll_ - _llp_)

        muhatp = muhat
        _llp_ = _ll_
        _ulp_ = _ul_

        _MCF_.append([times[i], _delta_[i], _d_[i], _delta_dot[i], _d_dot[i],
                      _d_bar[i], _var_, _ll_, _ul_, muhat, _mtbfc_, _mtbfcll_,
                      _mtbfcul_, _mtbfi_, _mtbfill_, _mtbfiul_])

    return(_MCF_)


def kaplan_meier(_dataset_, _reltime_, _conf_=0.75, _type_=3):
    """
    Function to calculate the Kaplan-Meier survival function estimates.

    Keyword Arguments:
    _dataset_  -- list of tuples where each tuple is in the form of:
                  (Left of Interval, Right of Interval, Event Status, Quantity)
                  and event status are:
                  0 = right censored
                  1 = event at time
                  2 = left censored
                  3 = interval censored
    _reltime_  -- time at which to stop analysis (helps eliminate stretched
                  plots due to small number of events at high hours).
    _conf_     -- the confidence level of the KM estimates (default is 75%).
    _type_     -- the confidence interval type for the KM estimates.
    """

    from scipy.stats import norm

    # Eliminate zero time failures and failures occurring after any
    # user-supplied upper limit.
    _dataset_ = [i for i in _dataset_ if i[0] >= 0.0]
    if(_reltime_ != 0.0):
        _dataset_ = [i for i in _dataset_ if i[0] <= _reltime_]
        times = [i[0] for i in _dataset_ if i[0] <= _reltime_]
        times2 = [i[1] for i in _dataset_ if i[0] <= _reltime_]
        status = [i[2] for i in _dataset_ if i[0] <= _reltime_]
        _quant_ = [i[3] for i in _dataset_ if i[0] <= _reltime_]

    for i in range(len(status)):
# If left and right times are the same, set the status to "Event".
        if(times[i] == times2[i]):
            status[i] = 1
# If left time is 0, set the status to "Left Censored".
        if(times[i] == 0.0):
            status[i] = 2

        if(status[i] == "Right Censored"):
            status[i] = 0
        elif(status[i] == "Left Censored"):
            status[i] = 2
        elif(status[i] == "Interval Censored"):
            status[i] = 3
        else:
            status[i] = 1

    for i in range(len(_quant_)):
        for j in range(len(_quant_[i])):
            times.append(times[i])
            times2.append(times2[i])
            status.append(status[i])

    # If Rpy2 is available, we will use that to perform the KM estimations.
    # Returns an object with the following fields:
    #    0 = total number of subjects in each curve.
    #    1 = the time points at which the curve has a step.
    #    2 = the number of subjects at risk at t.
    #    3 = the number of events that occur at time t.
    # 4 = the boolean inverse of three.
    #    5 = the estimate of survival at time t+0. This may be a vector or a
    #        matrix.
    #    6 = type of survival censoring.
    #    7 = the standard error of the cumulative hazard or -log(survival).
    #    8 = upper confidence limit for the survival curve.
    #    9 = lower confidence limit for the survival curve.
    #   10 = the approximation used to compute the confidence limits.
    #   11 = the level of the confidence limits, e.g. 90 or 95%.
    #   12 = the returned value from the na.action function, if any.
    #        It will be used in the printout of the curve, e.g., the number of
    #        observations deleted due to missing values.
    if(__USE_RPY__):
        print "Probably using Windoze."

    elif(__USE_RPY2__):
        survival = importr('survival')

        times = robjects.FloatVector(times)
        times2 = robjects.FloatVector(times2)
        status = robjects.IntVector(status)

        surv = survival.Surv(times, times2, type='interval2')
        robjects.globalenv['surv'] = surv
        fmla = robjects.Formula('surv ~ 1')
        _KM_ = survival.survfit(fmla)

        # Every subject must have a censored time to use survrec.
        #survrec = importr('survrec')
        #units = robjects.StrVector(units)
        #survr = survrec.Survr(units, times2, status2)
        #fit = survrec.wc_fit(survr)

        return(_KM_)

    else:

# Determine the confidence bound z-value.
        _z_norm_ = norm.ppf(_conf_)

# Get the total number of events.
        _n_ = len(_dataset_)
        N = _n_

        _KM_ = []
        _Sh_ = 1.0
        muhat = 0.0
        var = 0.0
        z = 0.0
        ti = float(_dataset_[0][0])
        tj = 0.0
        i = 0

        while (_n_ > 0):
# Find the total number of failures and suspensions in interval [i - 1, i].
            _d_ = sum([t for t in _dataset_ if (t[0] == _dataset_[i][0] and t[1] == 1)])
            _s_ = sum([t for t in _dataset_ if (t[0] == _dataset_[i][0] and t[1] == 0)])

# Estimate the probability of failing in interval [i - 1, i].
            _Si_ = 1.0 - (float(_d_) / float(_n_))

# Estimate the probability of survival up to time i [S(ti)].
            _Sh_ = _Si_ * _Sh_

# Calculate the standard error for S(ti).
            z = z + 1.0 / ((_n_ - _d_ + 1) * _n_)
            _se_ = sqrt(_Si_ * _Si_ * z)

# Calculate confidence bounds for S(ti).
            _ll_ = _Sh_ - _z_norm_ * _se_
            _ul_ = _Sh_ + _z_norm_ * _se_
            if(_type_ == 1 or _ul_ > 1.0):
                _ul_ = _Sh_
            if(_type_ == 2 or _ll_ < 0.0):
                _ll_ = _Sh_

# Calculate the cumulative hazard rate.
            try:
                _H_ = -log(_Sh_)
            except ValueError:
                _H_ = _H_

# Calculate the mean.
            muhat = muhat + _Sh_ * (ti - tj)
            tj = ti
            ti = _dataset_[i][0]

            _KM_.append([ti, _n_, _d_, _Si_, _Sh_, _se_, _ll_, _ul_, _H_, muhat, var])
            #if(_s_ > 0):
            #    _KM_.append([str(_dataset_[i][0]) + '+', _n_, _s_, '-', _Sh_,
            #                 _se_, _ll_, _ul_, _H_])

            _n_ = _n_ - _d_ - _s_
            i = i + _d_ + _s_

        return(_KM_)


def turnbull_tau(_dataset_):
    """
    This function creates a list of lists where each inner list is a unique
    pair of left and right interval values.

    Keyword Arguments:
    _dataset_ -- a list of the left times and right times of the interval
                 censored data.
    """

    import operator

    _tau_ = []
    for i in range(len(_dataset_)):
        _tau_.append([_dataset_[i][1], _dataset_[i][2], 3])

# Sort the list of left, right pairs.
    _tau_ = list(set(map(tuple, _tau_)))
    _tau_.sort(key=operator.itemgetter(0, 1))

# Convert each tuple to a list.
    _tau_ = [list(_row_) for _row_ in _tau_]

    return(_tau_)


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
        _fmla_ = robjects.Formula('surv ~ 1')
        _ekm_ = survival.survfit(_fmla_)

    _So_ = []
    for i in range(len(_ekm_)):
        _So_.append(_ekm_[i][5])

    _p_ = []
    for i in range(len(_So_) - 1):
        _p_.append(_So_[i + 1] - _So_[i])

    return(_p_)


#def interv(x, inf, sup):

#    if(x[0] >= inf and x[1] <= sup):
#        _interv_ = 1
#    else:
#        _interv_ = 0

#    return(_interv_)


#def turnbull_A(_dataset_, _tau_):

#    tau12 <- cbind(tau[-length(tau)], tau[-1])
#    A <- apply(tau12, 1, interv, inf=as.numeric(data[, 2]), sup=as.numeric(data[, 3]))
#    id.lin.zero <- which(apply(A==0, 1, all))

#    if(length(id.lin.zero)>0) A <- A[-id.lin.zero, ]

#    return(A)


#def turnbull(p, A, _dataset_, eps=1E-13, iter_max=200, _conf_=0.75):
    """
    Keyword Arguments:
    _dataset_ --
    _conf_    -- the confidence level of the estimates.
    """

#    _tau_ = turnbull_tau(_dataset_)
#    _p_ = turnbull_s(_tau_)


#    return


def parametric_fit(_dataset_, _starttime_, _reltime_,
                   _fitmeth_, _dist_='exponential'):
    """
    Function to fit data to a parametric distribution and estimate the
    parameters.

    Keyword Arguments:
    _dataset_ -- the dataset to fit.  This is a
    _reltime_ -- the maximum time to include in the fit.  Used to exclude
                 outliers.
    _fitmeth_ -- method used to fit data to the selected distribution.
                 1 = rank regression
                 2 = maximum likelihood estimation (MLE)
    _dist_    -- the noun name of the distribution to fit.  Defaults to
                 the exponential distribution.
    """

# Eliminate zero time failures and failures occurring after any user-supplied
# upper limit.
    _dataset_ = [i for i in _dataset_ if i[2] > _starttime_]
    _dataset_ = [i for i in _dataset_ if i[2] <= _reltime_]

    if(__USE_RPY__):
        print "Probably using Windoze."

    elif(__USE_RPY2__):

        Rbase = importr('base')

        if(_fitmeth_ == 1):                 # MLE
            if(_dist_ == 'exponential'):
                _dist_ = 'exp'
            elif(_dist_ == 'lognormal'):
                _dist_ = 'lnorm'
            elif(_dist_ == 'normal'):
                _dist_ = 'norm'

            left = [i[1] for i in _dataset_]
            right = [i[2] for i in _dataset_]
            for i in range(len(_dataset_)):
                if(_dataset_[i][4] == 0):
                    right[i] = 'NA'
                elif(_dataset_[i][4] == 1):
                    left[i] = right[i]
                elif(_dataset_[i][4] == 2):
                    left[i] = 'NA'

            od = rlc.OrdDict([('left', robjects.FloatVector(left)),
                              ('right', robjects.FloatVector(right))])

            censdata = robjects.DataFrame(od)
            n_row = Rbase.nrow(censdata)
            if(n_row[0] > 1):
                fitdistrplus = importr('fitdistrplus')
                try:
                    fit = fitdistrplus.fitdistcens(censdata, _dist_)
                except ri.RRuntimeError:
                    return True

                #para=R.list(scale=fit[0][1], shape=fit[0][0])
                #fitdistrplus.plotdistcens(censdata, _dist_, para)
            else:
                return True

        elif(_fitmeth_ == 2):               # Regression
            if(_dist_ == 'normal'):
                _dist_ = 'gaussian'

            if(_reltime_ != 0.0):
                time = [i[1] + 0.01 for i in _dataset_ if i[2] <= _reltime_]
                time2 = [i[2] + 0.01 for i in _dataset_ if i[2] <= _reltime_]
                status = [i[4] for i in _dataset_ if i[2] <= _reltime_]

            survival = importr('survival')

            for i in range(len(status)):
                if(status[i] == 'Right Censored'):
                    status[i] = 0
                elif(status[i] == 'Event'):
                    status[i] = 1
                elif(status[i] == 'Left Censored'):
                    status[i] = 2
                else:
                    status[i] = 3

            time = robjects.FloatVector(time)
            time2 = robjects.FloatVector(time2)
            status = robjects.IntVector(status)

            surv = survival.Surv(time, time2, status, type='interval')
            robjects.globalenv['surv'] = surv
            formula = robjects.Formula('surv ~ 1')

            fit = survival.survreg(formula, dist=_dist_)

    else:
        print "No R"

    return(fit)


def theoretical_distribution(_data_, _distr_, _para_):

    Rbase = importr('base')

# Create the R density and probabilty distribution names.
    ddistname = R.paste('d', _distr_, sep='')
    pdistname = R.paste('p', _distr_, sep='')

# Calculate the minimum and maximum values for x.
    xminleft = min([i[0] for i in _data_ if i[0] != 'NA'])
    xminright = min([i[1] for i in _data_ if i[1] != 'NA'])
    xmin = min(xminleft, xminright)

    xmaxleft = max([i[0] for i in _data_ if i[0] != 'NA'])
    xmaxright = max([i[1] for i in _data_ if i[1] != 'NA'])
    xmax = max(xmaxleft, xmaxright)

    xrange = xmax - xmin
    xmin = xmin - 0.3 * xrange
    xmax = xmax + 0.3 * xrange

# Creat a list of probabilities for the theoretical distribution with the
# estimated parameters.
    den = float(len(_data_))
    densfun = R.get(ddistname, mode='function')
    nm = R.names(_para_)
    f = R.formals(densfun)
    args = R.names(f)
    m = R.match(nm, args)
    s = R.seq(xmin, xmax, by=(xmax - xmin) / den)
    theop = Rbase.do_call(pdistname, R.c(R.list(s), _para_))

    return(theop)
