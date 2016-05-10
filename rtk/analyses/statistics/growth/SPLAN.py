#!/usr/bin/env python
"""
Contains functions for calculating various parameters of the SPLAN model.
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.statistics.growth.SPLAN.py is part of The RTK Project
#
# All rights reserved.

# Add NLS support.
import gettext

# Import modules for mathematics.
from math import exp
import numpy as np

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'

_ = gettext.gettext


def calculate_management_strategy(fef, mtbfa, mtbfgp):
    """
    Function to calculate the minimum required management strategy for the
    entire program or a test phase.

    :param float fef: the average fix effectiveness factor over the period to
                      calculate the management strategy.
    :param float mtbfa: the average MTBF over the first test phase.
    :param float mtbfgp: the growth protential MTBF.
    :return: _avg_ms
    :rtype: float
    """

    try:
        _avg_ms = (1.0 - (mtbfa / mtbfgp)) / fef
    except ZeroDivisionError:
        _avg_ms = 1.0

    return _avg_ms


def calculate_fef(ms, mtbfa, mtbfgp):
    """
    Function to calculate the minimum required average fix effectiveness factor
    for the entire program or a test phase.

    :param float ms: the management strategy over the period to calculate the
                     fix effectiveness factor.
    :param float mtbfa: the average MTBF over the period to calculate the fix
                        effectiveness factor.
    :param float mtbfgp: the growth potential MTBF.
    :return: _avg_fef
    :rtype: float
    """

    try:
        _avg_fef = (mtbfgp - mtbfa) / (ms * mtbfgp)
    except ZeroDivisionError:
        _avg_fef = 1.0

    return _avg_fef


def calculate_probability(test_time, ms, mtbfi):
    """
    Function to calculate the probability of observing at least one failure.

    :param float test_time: the total test time during which a failure may
                            be surfaced.
    :param float ms: the management strategy over the test time.
    :param float mtbfi: the initial MTBF at the beginning of the test time.
    :return: _prob
    :rtype: float
    """

    try:
        _prob = 1.0 - exp(-test_time * ms / mtbfi)
    except ZeroDivisionError:
        _prob = 0.0

    return _prob


def calculate_growth_potential(mtbfa, ms, fef):
    """
    Function to calculate the growth potential MTBF.

    :param float mtbfa: the average MTBF over the first test phase.
    :param float ms: the average management strategy over the test program.
    :param float fef: the average fix effectiveness factor over the test
                      program.
    :return: _mtbfgp
    :rtype: float
    """

    try:
        _mtbfgp = mtbfa / (1.0 - ms * fef)
    except ZeroDivisionError:
        _mtbfgp = np.inf

    return _mtbfgp
