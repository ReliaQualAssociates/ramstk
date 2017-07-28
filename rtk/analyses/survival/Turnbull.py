#!/usr/bin/env python
"""
Contains functions for performing Turnbull survival analysis.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.analyses.survival.Turnbull.py is part of The RTK Project
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

# Import mathematical functions.
import lifelines as nonpar
import numpy as np
from scipy.stats import norm                # pylint: disable=E0611
from math import sqrt


def turnbull_s(_tau_):
    """

    Keyword Arguments:
    _tau_ --
    """

    m = len(_tau_)
    _status_ = []

    for i in range(m - 1):
        _status_.append(1)

    # survival = importr('survival')

    # _times_ = robjects.FloatVector(_tau_[:m-1])
    # _status_ = robjects.IntVector(_status_)

    # _surv_ = survival.Surv(_times_, _status_)
    # robjects.globalenv['surv'] = _surv_
    # _ekm_ = survival.survfit(robjects.Formula('surv ~ 1'))

    _So_ = []
    # for i in range(len(_ekm_[5])):
    #     _So_.append(_ekm_[5][i])

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

    # surv = round(c(1, 1-cumsum(_p_)), digits=5)
    # right = data$right

    # if(any(!(is.finite(right))))
    #     t <- max(right[is.finite(right)])
    #     return(list(time=tau[tau<t],surv=surv[tau<t]))
    # else
    #     return(list(time=tau,surv=surv))

    return
