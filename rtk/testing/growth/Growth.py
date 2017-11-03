#!/usr/bin/env python
"""
##############################################
Testing Package Reliability Growth Data Module
##############################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.testing.growth.Growth.py is part of The RTK Project
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

# Import modules for localization support.
import gettext
import locale

# Import modules for mathematics.
from math import exp, log, sqrt
import numpy as np
from scipy.optimize import fsolve
from scipy.stats import chi2                # pylint: disable=E0611

# Import other RTK modules.
try:
    import Configuration
    import Utilities
    import analyses.statistics.Bounds as Bounds
    import analyses.statistics.growth.CrowAMSAA as CrowAMSAA
    import analyses.statistics.growth.SPLAN as SPLAN
    from testing.Testing import Model as Testing
    from testing.Testing import Testing as dtcTesting
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    import rtk.analyses.statistics.Bounds as Bounds
    import rtk.analyses.statistics.growth.CrowAMSAA as CrowAMSAA
    import rtk.analyses.statistics.growth.SPLAN as SPLAN
    from rtk.testing.Testing import Model as Testing
    from rtk.testing.Testing import Testing as dtcTesting

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _gr(gr, mi, mf, ttt, t1):
    """
    Function used to calculate the growth rate necessary to have the ideal
    growth curve end at the final MTBF and to calculate the optimum growth rate
    for a test phase.
    """

    return (ttt / t1)**gr + (mf / mi) * (gr - 1.0)


def running_sum(values):
    """
    Function used to calculate the running sum of values from a list.

    :param list values: the list of values to calculate the running sum.
    """

    _total = 0
    for _item in values:
        _total += _item
        yield _total


class Model(Testing):                       # pylint: disable=R0902, R0904
    """
    The Reliability Growth data model contains the attributes and methods for
    planning and assessing a reliability growth test. The attributes of a
    Reliability Growth model are:

    :ivar dict dic_test_data: dictionary containing the test data for the
                              Growth data model.  Key is an integer from 0 to
                              n records.  Values are a list: [record_id,
                              failure date, left interval, right interval,
                              quantity]
    :ivar list lst_p_growth_rate: list of planned growth rates per test phase.
    :ivar list lst_p_ms: list of planned management strategies per test phase.
    :ivar list lst_p_fef: list of planned fix effectiveness factors per test
                          phase.
    :ivar list lst_p_prob: list of planned probabilities of observing a failure
                           per test phase.
    :ivar list lst_p_mtbfi: list of planned initial MTBF per test phase.
    :ivar list lst_p_mtbff: list of planned final MTBF per test phase.
    :ivar list lst_p_mtbfa: list of planned average MTBF per test phase.
    :ivar list lst_p_test_time: list of planned test times per test phase.
    :ivar list lst_p_n_failures: list of planned number of failures per test
                                 phase.
    :ivar list lst_p_start_date: list of planned start dates per test phase.
    :ivar list lst_p_end_date: list of planned end dates per test phase.
    :ivar list lst_p_weeks: list of planned number of weeks per test phase.
    :ivar list lst_p_n_test_units: list of planned number of test units per
                                   test phase.
    :ivar list lst_p_tpu: list of planned average test time per unit per test
                          phase.
    :ivar list lst_p_tpupw: list of planned average test time per unit per week
                            per test phase.
    :ivar list lst_o_growth_rate: list of observed growth rates per test phase.
    :ivar list lst_o_ms: list of observed management strategies per test phase.
    :ivar list lst_o_fef: list of observed fix effectiveness factors per test
                          phase.
    :ivar list lst_o_mtbfi: list of observed initial MTBF per test phase.
    :ivar list lst_o_mtbff: list of observed final MTBF per test phase.
    :ivar list lst_o_mtbfa: list of observed average MTBF per test phase.
    :ivar list lst_o_test_time: list of observed test times per test phase.
    :ivar list alpha_hat: list of scale parameters estimated from the test data
                          [lower bound, point, upper bound].
    :ivar list beta_hat: list of shape parameters estimated from the test data
                         [lower bound, point, upper bound].
    :ivar list cum_mean: list of cumulative MTBF estimated from the test data
                         [lower bound, point, upper bound].
    :ivar list instantaneous_mean: list of instantaneous MTBF estimated from
                                   the test data
                                   [lower bound, point, upper bound].
    :ivar int rg_plan_model: the index in the list of reliability growth
                             planning models.
    :ivar int rg_assess_model: the index in the list of reliability assessment
                               and projection models.
    :ivar float alpha_hat: the point estimate of the scale parameter.
    :ivar float beta_hat: the point estimate of the shape parameter.
    :ivar float cum_mean: the point estimate of the cumulative MTBF.
    :ivar float instantaneous_mean: the point estimate of the instantaneous
                                    MTBF.
    :ivar float se_scale: the estimated standard error of the scale parameter.
    :ivar float se_shape: the estimated standard error of the shape parameter.
    :ivar float se_cum_mean: the estimated standard error of the cumulative
                             MTBF.
    :ivar float se_inst_mean: the estimated standard error of the instantaneous
                              MTBF.
    :ivar float cramer_vonmises: the Cramer-von Mises test statistic.
    :ivar float chi_square: the chi-square test statistic.
    """

    def __init__(self, n_phases=1):
        """
        Method to initialize a Reliability Growth Test data model instance.

        :param int n_phases: the number of growth phases associated with the
                             Growth test.
        """

        super(Model, self).__init__()

        # Initialize private dict attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dict attributes.
        self.dic_test_data = {}

        # Initialize public list attributes.
        # The following lists are used for holding ideal growth data for each
        # test phase.
        self.lst_i_mtbfi = [0.0] * n_phases         # Initial phase MTBF.
        self.lst_i_mtbff = [0.0] * n_phases         # Final phase MTBF.
        self.lst_i_mtbfa = [0.0] * n_phases         # Average phase MTBF.
        self.lst_i_n_failures = [0] * n_phases      # Expected number of failures.

        # The following lists are used for holding planned growth data for each
        # test phase.
        self.lst_p_growth_rate = [0.0] * n_phases
        self.lst_p_ms = [0.0] * n_phases            # Planned management strategy.
        self.lst_p_fef = [0.0] * n_phases           # Planned fix effectiveness factor.
        self.lst_p_prob = [0.0] * n_phases
        self.lst_p_mtbfi = [0.0] * n_phases         # Initial phase MTBF.
        self.lst_p_mtbff = [0.0] * n_phases
        self.lst_p_mtbfa = [0.0] * n_phases
        self.lst_p_test_time = [0.0] * n_phases     # Planned test time.
        self.lst_p_n_failures = [0] * n_phases      # Expected number of failures.
        self.lst_p_start_date = [0] * n_phases
        self.lst_p_end_date = [0] * n_phases
        self.lst_p_weeks = [0.0] * n_phases
        self.lst_p_n_test_units = [0] * n_phases
        self.lst_p_tpu = [0.0] * n_phases   # Test time per unit.
        self.lst_p_tpupw = [0.0] * n_phases     # Test time per unit per week.

        # The following lists are used for holding observed growth data for
        # each test phase.
        self.lst_o_growth_rate = [0.0, 0.0, 0.0]
        self.lst_o_ms = [0.0] * n_phases
        self.lst_o_fef = [0.0] * n_phases
        self.lst_o_mtbfi = [0.0] * n_phases
        self.lst_o_mtbff = [0.0] * n_phases
        self.lst_o_mtbfa = [0.0] * n_phases
        self.lst_o_test_time = [0.0] * n_phases     # Actual test time.
        self.lst_o_n_failures = [0] * n_phases      # Observed number of failures.

        self.lst_fixed_values = [True, True, True, True, True, True, True,
                                 True]

        # The following lists are used for holding model parameter estimates.
        # The format is [lower bound, point estimate, upper bound].
        self.alpha_hat = [0.0, 0.0, 0.0]
        self.beta_hat = [0.0, 0.0, 0.0]
        self.cum_mean = [[0.0, 0.0, 0.0]]
        self.instantaneous_mean = [[0.0, 0.0, 0.0]]
        self.growth_rate = [0.0, 0.0, 0.0]
        self.chi2_critical_value = [0.0, 0.0]

        # Initialize public scalar attributes.
        self.rg_plan_model = 0
        self.rg_assess_model = 0
        self.tr = 0.0                       # Program technical requirement MTBF.
        self.mtbfg = 0.0                    # Program goal MTBF.
        self.mtbfgp = 0.0                   # Growth potential MTBF.
        self.n_phases = n_phases
        self.ttt = 0.0                      # Total time on test.
        self.avg_growth = 0.0               # Average growth rate across all test phases.
        self.avg_ms = 0.75                  # Average management strategy across all test phases.
        self.avg_fef = 0.7                  # Average fix effectiveness factor across all test phases.
        self.probability = 0.75             # Probability of observing a failure.
        self.ttff = 0.0                     # Time to first fix.
        self.grouped = 0
        self.group_interval = 0.0
        self.se_scale = 0.0
        self.se_shape = 0.0
        self.se_cum_mean = 0.0
        self.se_inst_mean = 0.0
        self.cramer_vonmises = 0.0
        self.chi_square = 0.0
        self.cvm_critical_value = 0.0

    def calculate_idealized_growth_curve(self, mtbf=True):
        """
        Method to calculate the values for the idealized growth curve.

        :keyword bool mtbf: indicates whether to calculate MTBF (default) or
                            failure intensity values.
        :return: _ideal
        :rtype: list of floats
        """
# WARNING: Refactor calculate_idealized_growth_curve; current McCabe Complexity metric=17.
        _ideal = []

        # Verify the first phase average MTBF is greater than zero.  If not,
        # attempt to calculate the average MTBF.
        if self.lst_i_mtbfa[0] <= 0.0:
            _mtbfa = CrowAMSAA.calculate_initial_mtbf(self.avg_growth,
                                                      self.mtbfg, self.ttt,
                                                      self.lst_p_test_time[0])
            self.lst_i_mtbfa[0] = _mtbfa

        # Verify the program final (goal) MTBF is greater than zero.  If not,
        # attempt to calculate the final MTBF.
        if self.mtbfg <= 0.0:
            _mtbfg = CrowAMSAA.calculate_final_mtbf(self.avg_growth,
                                                    self.lst_i_mtbfa[0],
                                                    self.ttt,
                                                    self.lst_p_test_time[0])
            self.mtbfg = _mtbfg

        # Verify the program total time on test is greater than zero.  If not,
        # attempt to calculate the total time on test.
        if self.ttt <= 0.0:
            self.ttt = CrowAMSAA.calculate_total_time(self.avg_growth,
                                                      self.lst_i_mtbfa[0],
                                                      self.mtbfg,
                                                      self.lst_p_test_time[0])

        # Verify the first phase test time is greater than zero.  If not,
        # attempt to calculate the first phase test time.
        if self.lst_p_test_time[0] <= 0.0:
            _time = CrowAMSAA.calculate_t1(self.avg_growth,
                                           self.lst_i_mtbfa[0],
                                           self.mtbfg, self.ttt)
            self.lst_p_test_time[0] = _time

        # Verify the program average growth rate is greater than zero.  If not,
        # attempt to calculate the program average growth rate.
        if self.avg_growth <= 0.0:
            _alpha = CrowAMSAA.calculate_growth_rate(self.lst_i_mtbfa[0],
                                                     self.mtbfg, self.ttt,
                                                     self.lst_p_test_time[0])
            self.avg_growth = _alpha

        # Build the idealized curve.  If the time is less than the time to
        # first fix, the idealized value is the initial MTBF.  If the time
        # is equal to the time to first fix, the idealized value is set to
        # numpy's not a number to force a jump in the plot.  If the time is
        # greater than the time to first failure, the idealized value is
        # calculated from the inputs read above.
        if(self.lst_i_mtbfa[0] > 0.0 and self.lst_p_test_time[0] > 0.0 and
           self.mtbfg > 0.0 and self.ttt > 0.0 and self.avg_growth > 0.0):
            for _time in range(int(self.ttt)):
                if _time < int(self.lst_p_test_time[0]):
                    _ideal.append(self.lst_i_mtbfa[0])
                elif _time == int(self.lst_p_test_time[0]):
                    _ideal.append(np.nan)
                else:
                    _ideal.append((self.lst_i_mtbfa[0] *
                                   (float(_time) /
                                    self.lst_p_test_time[0])**self.avg_growth) /
                                  (1.0 - self.avg_growth))

            # Convert to failure intensity if that has been called for.
            if not mtbf:
                _ideal = [1.0 / _mtbf for _mtbf in _ideal]

            # Calculate the initial MTBF, final MTBF, average MTBF, and
            # expected number of failures for each phase.
            _t1 = self.lst_p_test_time[0]
            _mtbfa = self.lst_i_mtbfa[0]
            self.lst_i_n_failures = [0.0] * self.n_phases
            for _index in range(self.n_phases):
                _time = sum(self.lst_p_test_time[:_index + 1])
                _mtbf = CrowAMSAA.calculate_final_mtbf(self.avg_growth,
                                                       _mtbfa, _time, _t1)
                if _index < self.n_phases - 1:
                    self.lst_i_mtbfi[_index + 1] = _mtbf

                if _index > 0:
                    self.lst_i_mtbff[_index] = _mtbf

                _cum_fails = sum(self.lst_i_n_failures[:_index + 1])
                _n_failures = CrowAMSAA.calculate_n_failures(self.avg_growth,
                                                             _mtbfa, _time,
                                                             _t1, _cum_fails)
                self.lst_i_n_failures[_index] = _n_failures

            for _index in range(self.n_phases):
                _time = self.lst_p_test_time[_index]
                _n_failures = self.lst_i_n_failures[_index]
                _mtbfi = self.lst_i_mtbfi[_index]
                _mtbff = self.lst_i_mtbff[_index]
                _mtbfa = CrowAMSAA.calculate_average_mtbf(_time, _n_failures,
                                                          _mtbfi, _mtbff)
                self.lst_i_mtbfa[_index] = _mtbfa

        return _ideal

    def calculate_planned_growth_curve(self):
        """
        Method to calculate the necessary values for each reliability growth
        test phase.  These are the start and end points of the planned growth
        curve.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _mtbf1 = self.lst_p_mtbfa[0]
        _t1 = self.lst_p_test_time[0]

        for i in range(self.n_phases):
            _alpha = self.lst_p_growth_rate[i]
            _mtbfa = self.lst_p_mtbfa[i]
            _mtbfi = self.lst_p_mtbfi[i]
            _mtbff = self.lst_p_mtbff[i]
            _time = self.lst_p_test_time[i]
            _cum_time = sum(self.lst_p_test_time[:i + 1])

            if _mtbff <= 0.0:
                _mtbff = CrowAMSAA.calculate_final_mtbf(_alpha, _mtbf1,
                                                        _cum_time, _t1)
                self.lst_p_mtbff[i] = _mtbff

            if _mtbfa <= 0.0:
                _mtbfa = CrowAMSAA.calculate_average_mtbf(0.0, 0, _mtbfi,
                                                          _mtbff)
                self.lst_p_mtbfa[i] = _mtbfa

            if _mtbfi <= 0.0:
                _mtbfi = 2.0 * _mtbfa - _mtbff
                self.lst_p_mtbfi[i] = _mtbfi

            if _alpha <= 0.0:
                _alpha = CrowAMSAA.calculate_growth_rate(_mtbfi, _mtbff,
                                                         _time, _t1)
                self.lst_p_growth_rate[i] = _alpha

        return False

    def create_planned_values(self, mtbf=True):
        """
        Method to create the planned growth curve values.  These are used for
        plotting the planned growth curve.  The first curve created represents
        the average MTBF values over each phase.  These will be plotted as
        horizontal lines.  The second curve created represents the
        straight-line linear change in MTBF over the phase.

        :keyword boolean mtbf: indicates whether to calculate MTBF or failure
                               rates.
        :return: _plan
        :rtype: list
        """

        _plan = []

        for _phase in range(self.n_phases):
            _time = 0.0

            while _time < (self.lst_p_test_time[_phase] - 1.0):
                if mtbf:
                    _plan.append(self.lst_p_mtbfa[_phase])
                else:
                    _plan.append(1.0 / self.lst_p_mtbfa[_phase])

                _time += 1.0

            _plan.append(np.nan)            # pylint: disable=E1101

        return _plan

    def assess_plan_feasibility(self):
        """
        Method to assess the feasibility of a test plan.  The assessment
        criteria come from MIL-HDBK-189C, section 5.1.5 and section 5.1.6.\n\n

        The criteria and acceptable ranges are:\n

        - Initial MTBF / Goal MTBF              0.15 - 0.47\n
        - Fix Effectiveness Factor              0.55 - 0.85\n
        - Goal MTBF / Growth Potential MTBF     0.60 - 0.80\n
        - Growth Rate                           0.23 - 0.64\n

        :return: _results
        :rtype: list
        """

        _results = [0.0, 0.0, -1, -1]

        # Initial MTBF to goal MTBF ratio is high enough.  Too low means growth
        # testing is probably being started too early.
        try:
            _results[0] = self.lst_p_mtbfi[0] / self.mtbfg
        except ZeroDivisionError:
            _results[0] = 0.0

        # Goal MTBF to growth potential MTBF ratio is high enough.  Too
        # high means there is a low probability of achieving the goal MTBF.
        # Too low means the system may be over designed.
        try:
            _results[1] = self.mtbfg / self.mtbfgp
        except ZeroDivisionError:
            _results[1] = 0.0

        # Calculate the test time per test unit and test time per test unit
        # per week.
        for _phase in range(self.n_phases):
            # Assess logistics of test plan.
            _weeks = (self.lst_p_end_date[_phase] -
                      self.lst_p_start_date[_phase]) / 7.0

            try:
                self.lst_p_tpu[_phase] = self.lst_p_test_time[_phase] / \
                                         self.lst_p_n_test_units[_phase]
            except ZeroDivisionError:
                _results[2] = _phase
                self.lst_p_tpu[_phase] = 0.0

            try:
                self.lst_p_tpupw[_phase] = self.lst_p_tpu[_phase] / _weeks
            except ZeroDivisionError:
                _results[3] = _phase
                self.lst_p_tpupw[_phase] = 0.0

            # Assess engineering effort and quality of test plan.
            if self.lst_p_ms[_phase] <= 0.0 or self.lst_p_ms[_phase] > 1.0:
                _fef = self.lst_p_fef[_phase]
                _mtbfa = self.lst_p_mtbfa[_phase]

                _ms = SPLAN.calculate_management_strategy(_fef, _mtbfa,
                                                          self.mtbfgp)
                self.lst_p_ms[_phase] = _ms

            if self.lst_p_fef[_phase] <= 0.0 or self.lst_p_fef[_phase] > 0.0:
                _ms = self.lst_p_ms[_phase]
                _mtbfa = self.lst_p_mtbfa[_phase]

                _fef = SPLAN.calculate_fef(_ms, _mtbfa, self.mtbfgp)
                self.lst_p_fef[_phase] = _fef

            if self.lst_p_prob[_phase] <= 0.0 or self.lst_p_prob[_phase] > 1.0:
                _time = self.lst_p_test_time[_phase]
                _ms = self.lst_p_ms[_phase]
                _mtbfi = self.lst_p_mtbfi[_phase]

                _prob = SPLAN.calculate_probability(_time, _ms, _mtbfi)
                self.lst_p_prob[_phase] = _prob

        return _results

    def estimate_crow_amsaa(self):
        """
        Method to estimate the parameters of the Crow-AMSAA reliability growth
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _times = [x[3] for x in self.dic_test_data.values()]
        _failures = [x[4] for x in self.dic_test_data.values()]

        self.cum_time = _times[-1]
        self.cum_failures = sum(_failures)

        (self.alpha_hat[1],
         self.beta_hat[1]) = CrowAMSAA.calculate_crow_amsaa_parameters(
             _failures, _times, 0.0, self.grouped)

        (self.beta_hat[0],
         self.beta_hat[2]) = Bounds.calculate_crow_bounds(
             sum(_failures), _times[-1], self.alpha_hat[1],
             self.beta_hat[1], self.confidence, 1)

        (self.alpha_hat[0],
         self.alpha_hat[2]) = Bounds.calculate_crow_bounds(
             self.cum_failures, self.cum_time, self.alpha_hat[1],
             self.beta_hat[1], self.confidence, 2)

        return False

    def calculate_crow_amsaa_mean(self):
        """
        Method to calculate the cumulative and instantaneous mean from the
        Crow-AMSAA reliability growth model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _times = [x[3] for x in self.dic_test_data.values()]
        _failures = [x[4] for x in self.dic_test_data.values()]

        _n_fail_times = len(_times)

        self.cum_mean = []
        self.instantaneous_mean = []

        for i in range(_n_fail_times):
            (_cum_mean,
             _instantaneous_mean) = CrowAMSAA.calculate_crow_amsaa_mean(
                 _times[i], self.alpha_hat[1], self.beta_hat[1])

            (_lower, _upper) = Bounds.calculate_crow_bounds(
                sum(_failures[:i + 1]), _times[i], self.alpha_hat[1],
                self.beta_hat[1], self.confidence, 3)

            _cum_mean_ll = 1.0 / _upper
            _cum_mean_ul = 1.0 / _lower

            _i_mean_ll = 1.0 / (self.alpha_hat[2] * self.beta_hat[2] *
                                _times[-1]**(self.beta_hat[2] - 1.0))
            _i_mean_ul = 1.0 / (self.alpha_hat[0] * self.beta_hat[0] *
                                _times[-1]**(self.beta_hat[0] - 1.0))

            self.cum_mean.append([_cum_mean_ll, _cum_mean, _cum_mean_ul])
            self.instantaneous_mean.append([_i_mean_ll, _instantaneous_mean,
                                            _i_mean_ul])

        return False

    def calculate_cramer_vonmises(self, t_star=0.0, type2=True):
        """
        Method to calculate the Cramer-von Mises test statistic from the
        observed reliability growth data.

            Test the hypothesis that the data fits the Crow-AMSAA model.

                Ho: the data fits the Crow-AMSAA model
                Ha: the data does not fit the Crow-AMSAA model

            Reject Ho if _CvM exceeds the critical value.

        :param float t_star: termination time for Type I tests.
        :param bool type2: whether or not the test is time terminated (Type I)
                           or failure terminated (Type II).
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _times = [x[3] for x in self.dic_test_data.values()]
        _failures = [x[4] for x in self.dic_test_data.values()]

        self.cramer_vonmises = CrowAMSAA.calculate_cramer_vonmises(
            _failures, _times, self.beta_hat[1], t_star, type2)

        self.cvm_critical_value = CrowAMSAA.cramer_vonmises_critical_value(
            self.cum_failures, self.confidence)

        return False

    def calculate_chi_square(self):
        """
        Method to calculate the chi-square test statistic from the observed
        reliability growth data.

            Test the hypothesis that the data fits the Crow-AMSAA model.

               Ho: the data fits the Crow-AMSAA model
               Ha: the data does not fit the Crow-AMSAA model

            Reject Ho if _chi2 exceeds the critical values.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Ensure the confidence level is a fraction.
        if self.confidence > 1.0:
            self.confidence = self.confidence / 100.0

        _times = [x[3] for x in self.dic_test_data.values()]
        _failures = [x[4] for x in self.dic_test_data.values()]

        self.cum_failures = sum(_failures)
        self.chi_square = CrowAMSAA.calculate_crow_amsaa_chi_square(
            _failures, _times, self.beta_hat[1], _times[-1], self.grouped)

        _alpha_half = (1.0 - self.confidence) / 2.0

        if self.grouped == 0:               # Individual failure times.
            if self.test_termination_time > 0.0:    # Time truncated test.
                _df = 2.0 * self.cum_failures
            else:                                   # Failure truncated test.
                _df = 2.0 * (self.cum_failures - 1)
            _upper = _alpha_half
            _lower = self.confidence + _alpha_half
        else:                               # Grouped failure times.
            _df = len(_failures) - 1
            _upper = self.confidence
            _lower = 1.0 - self.confidence

        self.chi2_critical_value[0] = chi2.ppf(_lower, _df)
        self.chi2_critical_value[1] = chi2.ppf(_upper, _df)

        return False

    def assess_growth_rate(self):
        """
        Method to assess the actual growth rate occuring during a Growth Test.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.lst_o_growth_rate[0] = 1.0 - self.beta_hat[2]
        self.lst_o_growth_rate[1] = 1.0 - self.beta_hat[1]
        self.lst_o_growth_rate[2] = 1.0 - self.beta_hat[0]

        return False


class Growth(dtcTesting):
    """
    The Reliability Growth data controller provides an interface between the
    Reliability Growth data model and an RTK view model.  A single Growth
    controller can manage one or more Growth data models.  The attributes of a
    Growth data controller are:

    :ivar _dao: the Data Access Object to use when communicating with the RTK
                Project database.
    :ivar dicTests: Dictionary of the Growth data models managed.  Key is the
                    Test ID; value is a pointer to the Growth data model
                    instance.
    """

    def __init__(self):                     # pylint: disable=E1002
        """
        Method to initialize a Growth data controller instance.
        """

        super(Growth, self).__init__()

        # Initialize private scalar attributes.
        self._dao = None
        self._last_id = None

    def request_tests(self, dao, growth_test):
        """
        Reads the RTK Project database and loads all the Growth Tests
        associated with the selected Revision.  For each Growth Test returned:

        #. Retrieve the inputs from the RTK Project database.
        #. Create a Growth data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Growth Tests being managed
           by this controller.

        :param rtk.DAO dao: the Data Access object to use for communicating
                            with the RTK Project database.
        :param tuple growth_test: the Growth test attributes from the RTK
                                  Project database.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._dao = dao

        self._last_id = self._dao.get_last_id('rtk_tests')[0]

        # Create an instance of a Growth data model, set it's attributes, and
        # add it to the dictionary of Growth tests controlled by this data
        # controller.
        _test = Model(growth_test[17])
        _test.set_attributes(growth_test)
        self.dicTests[_test.test_id] = _test

        # Gather the Growth model phase attributes.
        _query = "SELECT * FROM rtk_growth_testing \
                  WHERE fld_test_id={0:d}".format(growth_test[2])
        (_phases,
         _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_phases = len(_phases)
        except TypeError:
            _n_phases = 0

        for j in range(_n_phases):
            _test.set_phase_attributes(_phases[j], j)

        self._request_test_data(_test.test_id)

        return(_phases, _error_code)

    def _request_test_data(self, test_id):
        """
        Method to read the RTK Project database and retrieves all the test
        records associated with the selected Test.

        :param int test_id: the Growth Test ID to select data for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _test = self.dicTests[test_id]

        _query = "SELECT fld_record_id, fld_failure_date, \
                         fld_left_interval, fld_right_interval, \
                         fld_quantity \
                  FROM rtk_survival_data \
                  WHERE fld_dataset_id={0:d} \
                  AND fld_source=1 \
                  ORDER BY fld_right_interval".format(test_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        _test.dic_test_data = {}
        try:
            _n_records = len(_results)
        except TypeError:
            _n_records = 0

        for i in range(_n_records):
            _test.dic_test_data[i] = [_results[i][0], _results[i][1],
                                      _results[i][2], _results[i][3],
                                      _results[i][4]]

        return(_results, _error_code)

    def add_test(self, revision_id, assembly_id):
        """
        Adds a new Test to the RTK Project for the selected Revision.

        :param int revision_id: the Revision ID to add the new Test.
        :param int assembly_id: the Assembly ID to add the new Test.
        :return: (_test, _error_code)
        :rtype: tuple
        """

        _query = "INSERT INTO rtk_tests \
                  (fld_revision_id, fld_assembly_id, fld_name, fld_test_type) \
                  VALUES ({0:d}, {1:d}, 'Test Plan', 4)".format(revision_id,
                                                                assembly_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # If the new test was added successfully to the RTK Project database:
        #   1. Retrieve the ID of the newly inserted test.
        #   2. Add a single growth phase to the growth testing table.
        #   3. Create a new Testing model instance.
        #   4. Set the attributes of the new Testing model instance.
        #   5. Add the new Testing model to the controller dictionary.
        if _results:
            self._last_id = self._dao.get_last_id('rtk_tests')[0]
            (_results, _error_code) = self.add_test_phase(self._last_id)

            _test = Model()
            _test.set_attributes((revision_id, assembly_id, self._last_id, '',
                                  '', 4, '', 0.0, 0.0, 0.75, 0.0, 0.0))
            self.dicTests[_test.test_id] = _test

        return(_test, _error_code)

    def add_test_phase(self, test_id, phase_id=0):
        """
        Adds a new test phase to the RTK Project for the selected Reliability
        Growth test.

        :param int test_id: the Test ID to add the new phase.
        :param int phase_id: the Phase ID of the new phase to add.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._last_id = self._dao.get_last_id('rtk_tests')[0]
        _query = "INSERT INTO rtk_growth_testing \
                  (fld_test_id, fld_phase_id) \
                  VALUES ({0:d}, {1:d})".format(test_id, phase_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)

    def add_test_record(self, test_id, date, time, n_failures,
                        additional=False):
        """
        Method to add a new record to the selected Reliability Growth test.

        :param int test_id: the ID of the test to add the record to.
        :param int date: the ordinal date of the failure(s).
        :param float time: the operating time at failure.
        :param int n_failures: the number of failures occurring at time.
        :keyword bool additional: indicates whether or not the time is
                                  cumulative.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _test = self.dicTests[test_id]

        _query = "SELECT MAX(fld_record_id), MAX(fld_right_interval) \
                  FROM rtk_survival_data \
                  WHERE fld_dataset_id={0:d} \
                  AND fld_source=1".format(test_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        if _results[0][0] is None or _results[0][0] == '':
            _last_id = 0
        else:
            _last_id = _results[0][0] + 1

        if _results[0][1] is None or _results[0][1] == '':
            _last_time = 0.0
        else:
            _last_time = float(_results[0][1])

        if additional:
            time = time + _last_time

        _query = "INSERT INTO rtk_survival_data \
                  (fld_record_id, fld_dataset_id, fld_left_interval, \
                   fld_right_interval, fld_quantity, fld_mode_type, \
                   fld_failure_date, fld_source) \
                  VALUES ({0:d}, {1:d}, {2:f}, {3:f}, {4:d}, {5:d}, \
                          {6:d}, 1)".format(_last_id, test_id, 0.0,
                                            time, n_failures, 0, date)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        try:
            _id = max(_test.dic_test_data.keys()) + 1
        except ValueError:
            _id = 0
        _test.dic_test_data[_id] = [_last_id, date, 0.0, time, n_failures]

        return(_results, _error_code)

    def delete_test(self, test_id):
        """
        Deletes a Testing input from the RTK Project.

        :param int test_id: the Test ID to delete the phase from.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        # Delete the phase information.
        _query = "DELETE FROM rtk_growth_testing \
                  WHERE fld_test_id={0:d}".format(test_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # Then delete the growth test itself.
        _query = "DELETE FROM rtk_tests \
                  WHERE fld_test_id={0:d}".format(test_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        self.dicTests.pop(test_id)

        return(_results, _error_code)

    def delete_test_phase(self, test_id, phase_id):
        """
        Deletes the selected test phase from the RTK Project database.

        :param int test_id: the Test ID to add the new phase.
        :param int phase_id: the Phase ID to delete from the test.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "DELETE FROM rtk_growth_testing \
                  WHERE fld_test_id={0:d} \
                  AND fld_phase_id={1:d}".format(test_id, phase_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)

    def delete_test_record(self, record_id, dataset_id):
        """
        Method to delete a test record from the RTK Program database.

        :param int record_id: the ID of the record to delete.
        :param int dataset_id: the ID of the dataset to delete the record from.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "DELETE FROM rtk_survival_data \
                  WHERE fld_record_id={0:d} \
                  AND fld_dataset_id={1:d} \
                  AND fld_source=1".format(record_id, dataset_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)

    def request_calculate(self, test_id, mtbf=True):
        """
        Method to request the various calculate methods of the Reliability
        Growth test data model.

        :param int test_id: the ID of the test to calculate.
        :keyword bool mtbf: indicates whether to calculate MTBF or failure
                            intensity values.
        :return: (_ideal, _plan)
        :rtype: tuple
        """

        _test = self.dicTests[test_id]

        _ideal = _test.calculate_idealized_growth_curve()
        if not _test.calculate_planned_growth_curve():
            _plan = _test.create_planned_values(mtbf)

        return(_ideal, _plan)

    def request_assessment(self, test_id):
        """
        Method to request the various methods to assess actual test data for
        the Reliability Growth test data model.

        :param int test_id: the ID of the test to assess.
        :keyword bool mtbf: indicates whether to calculate MTBF or failure
                            intensity values.
        :return: False if successful or True if an error is encountered
        :rtype: bool
        """

        _test = self.dicTests[test_id]

        if len(_test.dic_test_data.values()) > 0:
            _test.estimate_crow_amsaa()
            _test.calculate_crow_amsaa_mean()
            _test.assess_growth_rate()
            _test.calculate_chi_square()
            _test.calculate_cramer_vonmises()

        return False

    def save_test(self, test_id):
        """
        Method to save the Reliability Growth Test attributes to the RTK
        Project database.

        :param int test_id: the ID of the Test to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _test = self.dicTests[test_id]

        # Ensure confidence is stored as a fractional value.
        if _test.confidence > 1.0:
            _test.confidence = _test.confidence / 100.0

        _query = "UPDATE rtk_tests \
                  SET fld_name='{1:s}', fld_description='{2:s}', \
                      fld_test_type={3:d}, fld_attachment='{4:s}', \
                      fld_cum_time={5:f}, fld_cum_failures={6:d}, \
                      fld_confidence={7:f}, fld_consumer_risk={8:f}, \
                      fld_producer_risk={9:f}, fld_plan_model={10:d}, \
                      fld_assess_model={11:d}, fld_tr={12:f}, fld_mg={13:f}, \
                      fld_mgp={14:f}, fld_num_phases={15:d}, fld_ttt={16:f}, \
                      fld_avg_growth={17:f}, fld_avg_ms={18:f}, \
                      fld_avg_fef={19:f}, fld_prob={20:f}, fld_ttff={21:f}, \
                      fld_grouped={22:d}, fld_group_interval={23:f}, \
                      fld_se_scale={24:f}, fld_se_shape={25:f}, \
                      fld_se_cum_mean={26:f}, fld_se_inst_mean={27:f}, \
                      fld_cramer_vonmises={28:f}, fld_chi_square={29:f}, \
                      fld_scale_ll={30:f}, fld_scale={31:f}, \
                      fld_scale_ul={32:f}, fld_shape_ll={33:f}, \
                      fld_shape={34:f}, fld_shape_ul={35:f}, \
                      fld_cum_mean_ll={36:f}, fld_cum_mean={37:f}, \
                      fld_cum_mean_ul={38:f}, fld_inst_mean_ll={39:f}, \
                      fld_inst_mean={40:f}, fld_inst_mean_ul={41:f} \
                  WHERE fld_test_id={0:d}".format(
                      _test.test_id, _test.name, _test.description,
                      _test.test_type, _test.attachment, _test.cum_time,
                      _test.cum_failures, _test.confidence,
                      _test.consumer_risk, _test.producer_risk,
                      _test.rg_plan_model, _test.rg_assess_model, _test.tr,
                      _test.mtbfg, _test.mtbfgp, _test.n_phases, _test.ttt,
                      _test.avg_growth, _test.avg_ms, _test.avg_fef,
                      _test.probability, _test.ttff, _test.grouped,
                      _test.group_interval, _test.se_scale, _test.se_shape,
                      _test.se_cum_mean, _test.se_inst_mean,
                      _test.cramer_vonmises, _test.chi_square,
                      _test.alpha_hat[0], _test.alpha_hat[1],
                      _test.alpha_hat[2], _test.beta_hat[0],
                      _test.beta_hat[1], _test.beta_hat[2],
                      _test.cum_mean[-1][0], _test.cum_mean[-1][1],
                      _test.cum_mean[-1][2], _test.instantaneous_mean[-1][0],
                      _test.instantaneous_mean[-1][1],
                      _test.instantaneous_mean[-1][2])
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # Save the phase-specific information.
        for i in range(_test.n_phases):
            _query = "UPDATE rtk_growth_testing \
                      SET fld_p_growth_rate={2:f}, fld_p_ms={3:f}, \
                          fld_p_fef_avg={4:f}, fld_p_prob={5:f}, \
                          fld_p_mi={6:f}, fld_p_mf={7:f}, fld_p_ma={8:f}, \
                          fld_p_test_time={9:f}, fld_p_num_fails={10:d}, \
                          fld_p_start_date={11:d}, fld_p_end_date={12:d}, \
                          fld_p_weeks={13:f}, fld_p_test_units={14:d}, \
                          fld_p_tpu={15:f}, fld_p_tpupw={16:f}, \
                          fld_o_ms={17:f}, fld_o_fef_avg={18:f}, \
                          fld_o_mi={19:f}, fld_o_mf={20:f}, fld_o_ma={21:f}, \
                          fld_o_ttff={22:f}, fld_i_mi={23:f}, \
                          fld_i_mf={24:f}, fld_i_ma={25:f}, \
                          fld_i_num_fails={26:d} \
                      WHERE fld_test_id={0:d} \
                      AND fld_phase_id={1:d}".format(
                          _test.test_id, i, _test.lst_p_growth_rate[i],
                          _test.lst_p_ms[i], _test.lst_p_fef[i],
                          _test.lst_p_prob[i], _test.lst_p_mtbfi[i],
                          _test.lst_p_mtbff[i], _test.lst_p_mtbfa[i],
                          _test.lst_p_test_time[i],
                          int(_test.lst_p_n_failures[i]),
                          _test.lst_p_start_date[i], _test.lst_p_end_date[i],
                          _test.lst_p_weeks[i], _test.lst_p_n_test_units[i],
                          _test.lst_p_tpu[i], _test.lst_p_tpupw[i],
                          _test.lst_o_ms[i], _test.lst_o_fef[i],
                          _test.lst_o_mtbfi[i], _test.lst_o_mtbff[i],
                          _test.lst_o_mtbfa[i], _test.ttff,
                          _test.lst_i_mtbfi[i], _test.lst_i_mtbff[i],
                          _test.lst_i_mtbfa[i], int(_test.lst_i_n_failures[i]))
            (_results, _error_code, __) = self._dao.execute(_query,
                                                            commit=True)

        return(_results, _error_code)

    def save_test_data(self, test_id):
        """
        Method to save the test data.

        :param int test_id: the ID of the Test to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _results = False
        _error_code = 0

        _test = self.dicTests[test_id]

        # Save the actual test data.
        for _key in _test.dic_test_data.keys():
            _query = "UPDATE rtk_survival_data \
                      SET fld_failure_date={2:d}, fld_left_interval={3:f}, \
                          fld_right_interval={4:f}, fld_quantity={5:d} \
                      WHERE fld_dataset_id={0:d} \
                      AND fld_record_id={1:d} \
                      AND fld_source=1".format(
                          _test.test_id, _test.dic_test_data[_key][0],
                          _test.dic_test_data[_key][1],
                          _test.dic_test_data[_key][2],
                          _test.dic_test_data[_key][3],
                          _test.dic_test_data[_key][4])
            (_results, _error_code, __) = self._dao.execute(_query,
                                                            commit=True)

        return(_results, _error_code)

    def save_all_tests(self):
        """
        Method to save all Testing data models managed by the controller.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _test in self.dicTests.values():
            (_results, _error_code) = self.save_test(_test.test_id)
            (_results, _error_code) = self.save_test_data(_test.test_id)

        return False
