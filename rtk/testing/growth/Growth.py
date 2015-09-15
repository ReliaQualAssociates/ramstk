#!/usr/bin/env python
"""
##############################################
Testing Package Reliability Growth Data Module
##############################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.testing.growth.Growth.py is part of The RTK Project
#
# All rights reserved.

# Import modules for localization support.
import gettext
import locale

# Import modules for mathematics.
import numpy as np
from math import exp, log, sqrt
from scipy.optimize import fsolve
from scipy.stats import chi2                # pylint: disable=E0611

# Import other RTK modules.
try:
    import configuration as _conf
    import analyses.statistics.CrowAMSAA as CrowAMSAA
    import analyses.statistics.Bounds as Bounds
    from testing.Testing import Model as Testing
    from testing.Testing import Testing as dtcTesting
except ImportError:                         # pragma: no cover
    import rtk.configuration as _conf
    import rtk.analyses.statistics.CrowAMSAA as CrowAMSAA
    import rtk.analyses.statistics.Bounds as Bounds
    from rtk.testing.Testing import Model as Testing
    from rtk.testing.Testing import Testing as dtcTesting

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _error_handler(message):
    """
    Function to convert string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:   # Type error
        _error_code = 10
    elif 'index out of range' in message[0]:   # Index error
        _error_code = 40
    else:                                   # Unhandled error
        _error_code = 1000                  # pragma: no cover

    return _error_code


def _gr(gr, mi, mf, ttt, t1):
    """
    Function used to calculate the growth rate necessary to have the ideal
    growth curve end at the final MTBF and to calculate the optimum growth rate
    for a test phase.
    """

    return (ttt / t1)**gr + (mf / mi) * (gr - 1)


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

    :ivar dict dic_test_data: default value: {}

    :ivar list lst_p_growth_rate: default value: []
    :ivar list lst_p_ms: default value: []
    :ivar list lst_p_fef: default value: []
    :ivar list lst_p_prob: default value: []
    :ivar list lst_p_mtbfi: default value: []
    :ivar list lst_p_mtbff: default value: []
    :ivar list lst_p_mtbfa: default value: []
    :ivar list lst_p_test_time: default value: []
    :ivar list lst_p_n_failures: default value: []
    :ivar list lst_p_start_date: default value: []
    :ivar list lst_p_end_date: default value: []
    :ivar list lst_p_weeks: default value: []
    :ivar list lst_p_n_test_units: default value: []
    :ivar list lst_p_tpu: default value: []
    :ivar list lst_p_tpupw: default value: []

    :ivar list lst_o_growth_rate: default value: []
    :ivar list lst_o_ms: default value: []
    :ivar list lst_o_fef: default value: []
    :ivar list lst_o_mtbfi: default value: []
    :ivar list lst_o_mtbff: default value: []
    :ivar list lst_o_mtbfa: default value: []
    :ivar list lst_o_test_time: default value: []

    :ivar list alpha_hat: default value: [0.0, 0.0, 0.0]
    :ivar list beta_hat: default value: [0.0, 0.0, 0.0]
    :ivar list cum_mean: default value: [0.0, 0.0, 0.0]
    :ivar list instantaneous_mean: default value: [0.0, 0.0, 0.0]

    :ivar int rg_plan_model: default value: 0
    :ivar int rg_assess_model: default value: 0
    :ivar float alpha_hat: default value: 0.0
    :ivar float beta_hat: default value: 0.0
    :ivar float cum_mean: default value: 0.0
    :ivar float instantaneous_mean: default value: 0.0
    :ivar float se_scale: default value: 0.0
    :ivar float se_shape: default value: 0.0
    :ivar float se_cum_mean: default value: 0.0
    :ivar float se_inst_mean: default value: 0.0
    :ivar float cramer_vonmises: default value: 0.0
    :ivar float chi_square: default value: 0.0
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
        # The following lists are used for holding planned growth data for each
        # test phase.
        self.lst_p_growth_rate = [0.0] * n_phases
        self.lst_p_ms = [0.0] * n_phases            # Planned management strategy.
        self.lst_p_fef = [0.0] * n_phases           # Planned fix effectiveness factor.
        self.lst_p_prob = [0.0] * n_phases
        self.lst_p_mtbfi = [0.0] * n_phases
        self.lst_p_mtbff = [0.0] * n_phases
        self.lst_p_mtbfa = [0.0] * n_phases
        self.lst_p_test_time = [0.0] * n_phases     # Planned test time.
        self.lst_p_n_failures = [0] * n_phases      # Expected number of failures.
        self.lst_p_start_date = [0] * n_phases
        self.lst_p_end_date = [0] * n_phases
        self.lst_p_weeks = [0.0] * n_phases
        self.lst_p_n_test_units = [0] * n_phases
        self.lst_p_tpu = [0.0] * n_phases   # Test time per unit.
        self.lst_p_tpupw = [0.0] * n_phases # Test time per unit per week.

        # The following lists are used for holding observed growth data for
        # each test phase.
        self.lst_o_growth_rate = [0.0, 0.0, 0.0]
        self.lst_o_ms = [0.0] * n_phases
        self.lst_o_fef = [0.0] * n_phases
        self.lst_o_mtbfi = [0.0] * n_phases
        self.lst_o_mtbff = [0.0] * n_phases
        self.lst_o_mtbfa = [0.0] * n_phases
        self.lst_o_test_time = [0.0] * n_phases # Actual test time.

        self.lst_fixed_values = [False, False, False, False,
                                 False, False, False, False]

        # The following lists are used for holding model parameter estimates.
        # The format is [lower bound, point estimate, upper bound].
        self.alpha_hat = [0.0, 0.0, 0.0]
        self.beta_hat = [0.0, 0.0, 0.0]
        self.cum_mean = [[0.0, 0.0, 0.0]]
        self.instantaneous_mean = [[0.0, 0.0, 0.0]]
        self.growth_rate = [0.0, 0.0, 0.0]

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
        self.chi2_critical_value = [0.0, 0.0]

    def set_attributes(self, values):
        """
        Method to set the Reliability Growth data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Testing.set_attributes(self, values[:12])

        try:
            self.rg_plan_model = int(values[12])
            self.rg_assess_model = int(values[13])
            self.tr = float(values[14])
            self.mtbfg = float(values[15])
            self.mtbfgp = float(values[16])
            self.n_phases = int(values[17])
            self.ttt = float(values[18])
            self.avg_growth = float(values[19])
            self.avg_ms = float(values[20])
            self.avg_fef = float(values[21])
            self.probability = float(values[22])
            self.ttff = float(values[23])
            self.grouped = int(values[24])
            self.group_interval = float(values[25])
            self.se_scale = float(values[26])
            self.se_shape = float(values[27])
            self.se_cum_mean = float(values[28])
            self.se_inst_mean = float(values[29])
            self.cramer_vonmises = float(values[30])
            self.chi_square = float(values[31])
            self.alpha_hat[0] = float(values[32])
            self.alpha_hat[1] = float(values[33])
            self.alpha_hat[2] = float(values[34])
            self.beta_hat[0] = float(values[35])
            self.beta_hat[1] = float(values[36])
            self.beta_hat[2] = float(values[37])
            self.cum_mean[-1][0] = float(values[38])
            self.cum_mean[-1][1] = float(values[39])
            self.cum_mean[-1][2] = float(values[40])
            self.instantaneous_mean[-1][0] = float(values[41])
            self.instantaneous_mean[-1][1] = float(values[42])
            self.instantaneous_mean[-1][2] = float(values[43])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def set_phase_attributes(self, values, phase):
        """
        Method to set the Reliability Growth data model growth phase
        attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :param int phase: the growth phase to assign or update the value.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.lst_p_growth_rate[phase] = float(values[2])
            self.lst_p_ms[phase] = float(values[3])
            self.lst_p_fef[phase] = float(values[4])
            self.lst_p_prob[phase] = float(values[5])
            self.lst_p_mtbfi[phase] = float(values[6])
            self.lst_p_mtbff[phase] = float(values[7])
            self.lst_p_mtbfa[phase] = float(values[8])
            self.lst_p_test_time[phase] = float(values[9])
            self.lst_p_n_failures[phase] = int(values[10])
            self.lst_p_start_date[phase] = int(values[11])
            self.lst_p_end_date[phase] = int(values[12])
            self.lst_p_weeks[phase] = int(values[13])
            self.lst_p_n_test_units[phase] = int(values[14])
            self.lst_p_tpu[phase] = float(values[15])
            self.lst_p_tpupw[phase] = float(values[16])
            self.lst_o_growth_rate[phase] = float(values[17])
            self.lst_o_ms[phase] = float(values[18])
            self.lst_o_fef[phase] = float(values[19])
            self.lst_o_mtbfi[phase] = float(values[20])
            self.lst_o_mtbff[phase] = float(values[21])
            self.lst_o_mtbfa[phase] = float(values[22])
            self.lst_o_test_time[phase] = float(values[23])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Reliability Growth Test data
        model attributes.

        :return: (rg_plan_model, rg_assess_model, tr, mtbfg, mtbfgp, n_phases,
                  ttt, avg_growth, avg_ms, avg_fef, probability, ttff, grouped,
                  group_interval, se_scale, se_shape, se_cum_mean,
                  se_inst_mean, cramer_vonmises, chi_square, alpha_hat_ll,
                  alpha_hat, alpha_hat_ul, beta_hat_ll, beta_hat, beta_hat_ul)
        :rtype: tuple
        """

        _values = Testing.get_attributes(self)

        _values = _values + (self.rg_plan_model, self.rg_assess_model,
                             self.tr, self.mtbfg, self.mtbfgp, self.n_phases,
                             self.ttt, self.avg_growth, self.avg_ms,
                             self.avg_fef, self.probability, self.ttff,
                             self.grouped, self.group_interval, self.se_scale,
                             self.se_shape, self.se_cum_mean,
                             self.se_inst_mean, self.cramer_vonmises,
                             self.chi_square, self.alpha_hat[0],
                             self.alpha_hat[1], self.alpha_hat[2],
                             self.beta_hat[0], self.beta_hat[1],
                             self.beta_hat[2])

        return _values

    def get_phase_attributes(self):
        """
        Retrieves the current values of the Reliability Growth Test phase data
        model attributes.

        :return: (lst_p_growth_rate, lst_p_ms, lst_p_fef, lst_p_prob,
                  lst_p_mtbfi, lst_p_mtbff, lst_p_mtbfa, lst_p_test_time,
                  lst_p_n_failures, lst_p_start_date, lst_p_end_date,
                  lst_p_weeks, lst_p_n_test_units, lst_p_tpu, lst_p_tpupw,
                  lst_o_growth_rate, lst_o_ms, lst_o_fef, lst_o_mtbfi,
                  lst_o_mtbff, lst_o_mtbfa, lst_o_test_time, cum_mean,
                  instantaneous_mean)
        :rtype: tuple
        """

        _values = (self.lst_p_growth_rate, self.lst_p_ms, self.lst_p_fef,
                   self.lst_p_prob, self.lst_p_mtbfi, self.lst_p_mtbff,
                   self.lst_p_mtbfa, self.lst_p_test_time,
                   self.lst_p_n_failures, self.lst_p_start_date,
                   self.lst_p_end_date, self.lst_p_weeks,
                   self.lst_p_n_test_units, self.lst_p_tpu, self.lst_p_tpupw,
                   self.lst_o_growth_rate, self.lst_o_ms, self.lst_o_fef,
                   self.lst_o_mtbfi, self.lst_o_mtbff, self.lst_o_mtbfa,
                   self.lst_o_test_time, self.cum_mean,
                   self.instantaneous_mean)

        return _values
#TODO: Return error codes from each calculate method rather than False/True.
    def calculate_initial_mtbf(self, phase=None):
        """
        Method to calculate the initial MTBF for the entire test program or for
        a single test phase.

        :param int phase: the test phase to calculate the initial MTBF for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if phase is None or phase == 0:
            if self.avg_growth <= 0.0:
                self.avg_growth = sum(self.lst_p_growth_rate) / \
                                  len(self.lst_p_growth_rate)
            if self.ttt <= 0.0:
                self.ttt = sum(self.lst_p_test_time)

            try:
                self.lst_p_mtbfi[0] = (self.lst_p_mtbff[self.n_phases - 1] *
                                       (1.0 - self.avg_growth)) / \
                                      (self.ttt /
                                       self.lst_p_test_time[0])**self.avg_growth
            except(ValueError, ZeroDivisionError, IndexError):
                self.lst_p_mtbfi[0] = 0.0
                return True
        else:
            try:
                self.lst_p_mtbfi[phase] = self.lst_p_mtbff[phase - 1] #* \
                                          #(1.0 - self.lst_p_growth_rate[phase]) / \
                                          #(self.lst_p_test_time[phase] /
                                          # self.lst_p_test_time[0])**self.lst_p_growth_rate[phase]
            except(ValueError, ZeroDivisionError, IndexError):
                self.lst_p_mtbfi[phase] = 0.0
                return True

        return False

    def calculate_final_mtbf(self, phase=None):
        """
        Method to calculate the final MTBF for the entire test program or for
        a single test phase.

        :param int phase: the test phase to calculate the final MTBF for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if phase is None:
            if self.avg_growth <= 0.0:
                self.avg_growth = sum(self.lst_p_growth_rate) / \
                                  len(self.lst_p_growth_rate)
            if self.ttt <= 0.0:
                self.ttt = sum(self.lst_p_test_time)

            try:
                self.lst_p_mtbff[self.n_phases - 1] = (self.lst_p_mtbfi[0] *
                                                       (self.ttt /
                                                        self.lst_p_test_time[0])**self.avg_growth) / \
                                                       (1.0 - self.avg_growth)
            except(ValueError, ZeroDivisionError, IndexError):
                self.lst_p_mtbff[self.n_phases - 1] = 0.0
                return True
        else:
            try:
                self.lst_p_mtbff[phase] = (self.lst_p_mtbfi[0] *
                                           (sum(self.lst_p_test_time[:phase + 1]) /
                                            self.lst_p_test_time[0])**self.lst_p_growth_rate[phase]) / \
                                          (1.0 - self.lst_p_growth_rate[phase])
            except(ValueError, ZeroDivisionError, IndexError):
                self.lst_p_mtbff[phase] = 0.0
                return True

            # Set the next phase initial MTBF equal to the current phase's
            # calculated final MTBF if the initial MTBF is not already
            # specified.
            try:
                if(phase <= self.n_phases - 1 and
                   self.lst_p_mtbfi[phase + 1] <= 0.0):
                    self.lst_p_mtbfi[phase + 1] = self.lst_p_mtbff[phase]
            except IndexError:
                pass

        return False

    def calculate_average_mtbf(self, phase=0):
        """
        Method to calculate the average MTBF over a test phase.

        :param int phase: the test phase to calculate the average MTBF for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if self.avg_growth <= 0.0:
            self.avg_growth = sum(self.lst_p_growth_rate) / \
                              len(self.lst_p_growth_rate)

        # First calculate the expected number of failures in the test phase.
        self.lst_p_n_failures[phase] = ((1.0 / self.lst_p_mtbfi[0]) *
                                        self.lst_p_test_time[0] *
                                        (sum(self.lst_p_test_time[:phase + 1]) /
                                         self.lst_p_test_time[0])**(1.0 - self.avg_growth)) - \
                                       sum(self.lst_p_n_failures[:phase])

        # Then calculate the average MTBF over the test phase.
        if phase == 0:
            self.lst_p_mtbfa[phase] = (self.lst_p_mtbfi[phase] +
                                       self.lst_p_mtbff[phase]) / 2.0
        else:
            try:
                self.lst_p_mtbfa[phase] = self.lst_p_test_time[phase] / \
                                          self.lst_p_n_failures[phase]
            except ZeroDivisionError:
                self.lst_p_mtbfa[phase] = self.lst_p_mtbfi[phase]

        return False

    def calculate_total_time(self, phase=None):
        """
        Method to calculate the total test time required.  This method can be
        used to calculate the total time required for the entire test program
        or the total time required for a single test phase.

        :param int phase: the test phase to calculate the total test time for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if phase is None:
            if self.lst_p_mtbff[-1] / self.lst_p_mtbfi[0] == 1.0:
                self.ttt = 0.0
            else:
                if self.avg_growth <= 0.0:
                    self.avg_growth = sum(self.lst_p_growth_rate) / \
                                      len(self.lst_p_growth_rate)

                self.ttt = self.lst_p_test_time[0] * \
                           (self.lst_p_mtbff[-1] * (1.0 - self.avg_growth) /
                            self.lst_p_mtbfi[0])**(1.0 / self.avg_growth)
        else:
            try:
                _time = ((self.lst_p_mtbff[phase] / self.lst_p_mtbfi[0]) * \
                         (1.0 - self.lst_p_growth_rate[phase]))**(1.0 / self.lst_p_growth_rate[phase]) * \
                        self.lst_p_test_time[0]
                self.lst_p_test_time[phase] = _time - \
                                              sum(self.lst_p_test_time[:phase])
            except IndexError:
                return True

        return False

    def calculate_growth_rate(self, phase=None):
        """
        Method to calculate the minimum required growth rate for a test phase
        or over the entire test program.

        :param int phase: the test phase to calculate the growth rate for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if phase is None:
            if self.ttt <= 0.0:
                self.ttt = sum(self.lst_p_test_time)

            try:
                self.avg_growth = -log(self.ttt / self.lst_p_test_time[0]) - \
                                       1.0 + sqrt((1.0 +
                                                   log(self.ttt /
                                                       self.lst_p_test_time[0]))**2.0 +
                                                  2.0 * log(self.lst_p_mtbff[-1] /
                                                            self.lst_p_mtbfi[0]))
            except(ValueError, ZeroDivisionError):
                self.avg_growth = 0.0
        else:
            try:
                _ttt = sum(self.lst_p_test_time[:phase + 1])
                self.lst_p_growth_rate[phase] = -log(_ttt /
                                                     self.lst_p_test_time[0]) - \
                                                1.0 + sqrt((1.0 +
                                                            log(_ttt /
                                                                self.lst_p_test_time[phase]))**2.0 +
                                                           2.0 * log(self.lst_p_mtbff[phase] /
                                                                     self.lst_p_mtbfi[0]))
            except(ValueError, ZeroDivisionError):
                self.lst_p_growth_rate[phase] = 0.0
                return True

        return False

    def calculate_minimum_first_phase_time(self):
        """
        Method to calculate the minimum length of the first reliability growth
        phase.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        try:
            if self.avg_growth <= 0.0:
                self.avg_growth = sum(self.lst_p_growth_rate) / \
                                      len(self.lst_p_growth_rate)
            if self.ttt <= 0.0:
                self.ttt = sum(self.lst_p_test_time)

            self.lst_p_test_time[0] = exp(log(self.ttt) -
                                          (log((1.0 - self.avg_growth) *
                                               (self.lst_p_mtbff[-1] /
                                                self.lst_p_mtbfi[0])) /
                                           self.avg_growth))
        except(ValueError, ZeroDivisionError):
            self.lst_p_test_time[0] = 0.0
            return True

        return False

    def calculate_management_strategy(self, phase=None):
        """
        Method to calculate the minimum required management strategy.

        :param int phase: the test phase to calculate the management strategy
                          for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if phase is None:
            try:
                self.avg_ms = (1.0 - (self.lst_p_mtbfi[0] / self.mtbfgp)) / \
                              self.avg_fef
            except ZeroDivisionError:
                self.avg_ms = 100.0
                return True
        else:
            if self.lst_p_fef[phase] == 0.0:
                self.lst_p_fef[phase] = self.avg_fef

            try:
                self.lst_p_ms[phase] = (1.0 - (self.lst_p_mtbfi[phase] /
                                               self.mtbfgp)) / \
                                       self.lst_p_fef[phase]
            except(ValueError, ZeroDivisionError):
                self.lst_p_ms[phase] = 100.0
                return True

        return False

    def calculate_probability(self, phase=0):
        """
        Method to calculate the probability of observing at least one failure.

        :param int phase: the test phase to calculate the probability for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        try:
            self.lst_p_prob[phase] = 1.0 - exp(-self.lst_p_test_time[phase] *
                                               self.lst_p_ms[phase] /
                                               self.lst_p_mtbfi[phase])
        except(ValueError, ZeroDivisionError):
            self.lst_p_prob[phase] = 0.0
            return True

        return False

    def calculate_growth_potential(self):
        """
        Method to calculate the growth potential MTBF.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # If the management strategy and/or fix effectiveness factor are zero,
        # tell the user
        if self.avg_ms * self.avg_fef == 0.0:
            self.mtbfgp = self.lst_p_mtbfi[0]
            return True

        try:
            self.mtbfgp = self.lst_p_mtbfi[0] / \
                          (1.0 - self.avg_ms * self.avg_fef)
        except ZeroDivisionError:
            self.mtbfgp = self.lst_p_mtbfi[0]
            return True

        return False

    def calculate_idealized_growth_curve(self, mtbf=True):
        """
        Method to calculate the values for the idealized growth curve.

        :param bool mtbf: indicates whether to calculate MTBF (default) or
                          failure intensity values.
        :return: _ideal
        :rtype: list of floats
        """

        _ideal_gr = fsolve(_gr, 0.01, (self.lst_p_mtbfi[0],
                                       self.lst_p_mtbff[-1], self.ttt,
                                       self.lst_p_test_time[0]))[0]

        _ideal = []

        # Build the idealized curve.  If the time is less than the time to
        # first fix, the idealized value is the initial MTBF.  If the time
        # is equal to the time to first fix, the idealized value is set to
        # numpy's not a number to force a jump in the plot.  If the time is
        # greater than the time to first failure, the idealized value is
        # calculated from the inputs read above.
        if mtbf:
            for _time in range(int(self.ttt)):
                if _time < int(self.lst_p_test_time[0]):
                    _ideal.append(self.lst_p_mtbfi[0])
                elif _time == int(self.lst_p_test_time[0]):
                    _ideal.append(np.nan)
                else:
                    _ideal.append((self.lst_p_mtbfi[0] *
                                   (float(_time) /
                                    self.lst_p_test_time[0])**_ideal_gr) /
                                  (1.0 - _ideal_gr))
        else:
            for _time in range(int(self.ttt)):
                if _time < int(self.lst_p_test_time[0]):
                    _ideal.append(1.0 / self.lst_p_mtbfi[0])
                elif _time == int(self.lst_p_test_time[0]):
                    _ideal.append(np.nan)
                else:
                    _ideal.append((1.0 - _ideal_gr) /
                                  (self.lst_p_mtbfi[0] *
                                   (float(_time) /
                                    self.lst_p_test_time[0])**_ideal_gr))

        return _ideal

    def calculate_planned_growth_curve(self):
        """
        Method to calculate the necessary values for each reliability growth
        test phase.  These are the start and end points of the planned growth
        curve.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Set the length of first test phase.  If it is supplied use that,
        # otherwise use the growth start time.  If the length of the first test
        # phase is less than the growth start time, issue an information dialog
        # and return.
#        if self.lst_p_test_time[0] <= 0.0:
#            self.lst_p_test_time[0] = self.t1
#        elif self.lst_p_test_time[0] < self.t1:
# TODO: Move the information dialog to the view module
            #_util.rtk_information(_(u"The length of the first test phase must be "
            #                        u"equal to or longer than the growth start "
            #                        u"time.  You have entered the following:\n\n"
            #                        u"1. Growth start time: %f\n"
            #                        u"2. Length of first test phase: %f\n\n"
            #                        u"Please correct your inputs and try again.") %
            #                      (self.t1, self.lst_p_test_time[0]))
#            return True

        # Initialize some variables used to track cumulative values.
        for i in range(self.n_phases):
            if self.lst_p_mtbfi[i] <= 0.0:
                self.calculate_initial_mtbf(i)

            if self.lst_p_mtbff[i] <= 0.0:
                self.calculate_final_mtbf(i)

            if self.lst_p_test_time[i] <= 0.0:
                self.calculate_total_time(i)

            if self.lst_p_growth_rate[i] <= 0.0:
                self.lst_p_growth_rate[i] = fsolve(_gr, 0.01,
                                                   (self.lst_p_mtbfi[i],
                                                    self.lst_p_mtbff[i],
                                                    self.ttt,
                                                    self.lst_p_test_time[0])
                                                  )[0]

            # Set the next phase initial MTBF to equal the current phase's
            # final MTBF.  Just continue if it's the last phase.
            try:
                if self.lst_p_mtbfi[i + 1] <= 0.0:
                    self.lst_p_mtbfi[i + 1] = self.lst_p_mtbff[i]
            except IndexError:
                self.calculate_average_mtbf(i)
                continue

            # Calculate the expected number of failures for the phase and the
            # average MTBF for the phase.  Even if mtbfa > 0.0, we need to
            # calculate the number of failures for possible use with subsequent
            # test phases.
            self.calculate_average_mtbf(i)

        return False

    def create_planned_values(self, phase, mtbf=True):
        """
        Method to create the planned growth curve values.  These are used for
        plotting the planned growth curve.

        :param int phase: the test phase to create the planned values for.
        :param boolean mtbf: indicates whether to calculate MTBF or failure
                             rates.
        :return: _plan
        :rtype: list of floats
        """

        _time = 0.0
        _plan = []

        while _time < (self.lst_p_test_time[phase] - 1.0):
            if mtbf:
                _plan.append(self.lst_p_mtbfa[phase])
            else:
                _plan.append(1.0 / self.lst_p_mtbfa[phase])

            _time += 1.0

        _plan.append(np.nan)                # pylint: disable=E1101

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

        _results = [False, False, 0, 0]
        for i in range(self.n_phases):
            _weeks = (self.lst_p_end_date[i] - self.lst_p_start_date[i]) / 7.0

            try:
                self.lst_p_tpu[i] = self.lst_p_test_time[i] / \
                                    self.lst_p_n_test_units[i]
            except ZeroDivisionError:
                _results[0] = True
                _results[2] = i + 1
                self.lst_p_tpu[i] = 0.0

            try:
                self.lst_p_tpupw[i] = self.lst_p_tpu[i] / _weeks
            except ZeroDivisionError:
                _results[1] = True
                _results[3] = i + 1
                self.lst_p_tpupw[i] = 0.0

        return _results

    def estimate_crow_amsaa(self):
        """
        Method to estimate the parameters of the Crow-AMSAA reliability growth
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _times = [x[2] for x in self.dic_test_data.values()]
        _failures = [x[3] for x in self.dic_test_data.values()]

        self.cum_time = _times[-1]
        self.cum_failures = sum(_failures)

        (self.alpha_hat[1],
         self.beta_hat[1]) = CrowAMSAA.calculate_crow_amsaa_parameters(
             _failures, _times, 0.0, self.grouped)

        (self.beta_hat[0],
         self.beta_hat[2]) = Bounds.calculate_crow_bounds(
             sum(_failures), _times[-1], self.alpha_hat[1], self.beta_hat[1],
             self.confidence, 1)

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

        _times = [x[2] for x in self.dic_test_data.values()]
        _failures = [x[3] for x in self.dic_test_data.values()]

        _n_fail_times = len(_times)

        self.cum_mean = []
        self.instantaneous_mean = []

        for i in range(_n_fail_times):
            (_cum_mean,
             _instantaneous_mean) = CrowAMSAA.calculate_crow_amsaa_mean(
                 _times[i], self.alpha_hat[1], self.beta_hat[1])

            (_lower, _upper) = Bounds.calculate_crow_bounds(
                sum(_failures[:i+1]), _times[i], self.alpha_hat[1],
                self.beta_hat[1], self.confidence, 3)

            _cum_mean_ll = 1.0 / _upper
            _cum_mean_ul = 1.0 / _lower

            _i_mean_ll = 1.0 / (self.alpha_hat[2] * self.beta_hat[2] * \
                _times[-1]**(self.beta_hat[2] - 1.0))
            _i_mean_ul = 1.0 / (self.alpha_hat[0] * self.beta_hat[0] * \
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

        _times = [x[2] for x in self.dic_test_data.values()]
        _failures = [x[3] for x in self.dic_test_data.values()]

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

        _times = [x[2] for x in self.dic_test_data.values()]
        _failures = [x[3] for x in self.dic_test_data.values()]

        self.cum_failures = sum(_failures)
        self.chi_square = CrowAMSAA.calculate_crow_amsaa_chi_square(
            _failures, _times, self.beta_hat[1], self.ttt, self.grouped)

        _alpha_half = (1.0 - self.confidence) / 2.0

        self.chi2_critical_value[0] = chi2.ppf(_alpha_half,
                                               2 * self.cum_failures)
        self.chi2_critical_value[1] = chi2.ppf(self.confidence + _alpha_half,
                                               2 * self.cum_failures)

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
        Initializes a Growth data controller instance.
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
        Reads the RTK Project database and retrieves all the test records
        associated with the selected Test.

        :param int test_id: the Growth Test ID to select data for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _test = self.dicTests[test_id]

        _query = "SELECT fld_record_id, fld_request_date, \
                         fld_left_interval, fld_right_interval, \
                         fld_quantity \
                  FROM rtk_survival_data \
                  WHERE fld_dataset_id=%d \
                  ORDER BY fld_request_date" % test_id
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        _test.dic_test_data = {}
        try:
            _n_records = len(_results)
        except TypeError:
            _n_records = 0

        for i in range(_n_records):
            _test.dic_test_data[_results[i][0]] = [
                _results[i][1], _results[i][2], _results[i][3], _results[i][4]]

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
                  WHERE fld_record_id=%d \
                  AND fld_dataset_id=%d" % (record_id, dataset_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)

    def request_calculate(self, test_id):
        """
        Method to request the various calculate methods of the Reliability
        Growth test data model.

        :param int test_id: the ID of the stakeholder input to save.
        :return: _results
        :rtype: list
        """

        _test = self.dicTests[test_id]
        _results = [False, False, False, False, False, False, False, False,
                    False]

        if not _test.lst_fixed_values[0]:   # MTBFI is not fixed.
            _results[0] = _test.calculate_initial_mtbf()
        if not _test.lst_fixed_values[1]:   # MTBFG is not fixed.
            _results[1] = _test.calculate_final_mtbf()
        if not _test.lst_fixed_values[2]:   # TTFF is not fixed.
            _results[2] = _test.calculate_minimum_first_phase_time()
        if not _test.lst_fixed_values[3]:   # TTT is not fixed.
            _results[3] = _test.calculate_total_time()
        if not _test.lst_fixed_values[4]:   # Average GR is not fixed.
            _results[4] = _test.calculate_growth_rate()
        #if not _test.lst_fixed_values[5]:   # Average FEF is not fixed.
        #    _results[5] = _test.calculate_fef()
        if not _test.lst_fixed_values[6]:   # Average MS is not fixed.
            _results[6] = _test.calculate_management_strategy()
        if not _test.lst_fixed_values[7]:   # Probability is not fixed.
            _results[7] = _test.calculate_probability()

        # Calculate phase values.
        _test.calculate_final_mtbf(0)
        _test.calculate_average_mtbf(0)
        _test.calculate_management_strategy(0)
        for i in range(1, _test.n_phases):
            _test.calculate_initial_mtbf(i)
            _test.calculate_final_mtbf(i)
            _test.calculate_average_mtbf(i)
            _test.calculate_management_strategy(i)

        _results[8] = _test.calculate_growth_potential()

        return _results

    def save_test(self, test_id):
        """
        Saves the Reliability Growth Testing attributes to the RTK Project
        database.

        :param int test_id: the ID of the stakeholder input to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _test = self.dicTests[test_id]

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
                          fld_o_ttff={22:f} \
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
                          _test.lst_o_mtbfa[i], _test.ttff)
            (_results, _error_code, __) = self._dao.execute(_query,
                                                            commit=True)

        # Save the actual test data.
        _n_records = len(_test.dic_test_data.keys())
        for i in range(_n_records):
            _query = "UPDATE rtk_survival_data \
                      SET fld_request_date={2:d}, fld_left_interval={3:f}, \
                          fld_right_interval={4:f}, fld_quantity={5:d} \
                      WHERE fld_dataset_id={0:d} \
                      AND fld_record_id={1:d}".format(
                          _test.test_id, i, _test.dic_test_data[i][0],
                          _test.dic_test_data[i][1], _test.dic_test_data[i][2],
                          _test.dic_test_data[i][3])
            (_results, _error_code, __) = self._dao.execute(_query,
                                                            commit=True)

        return(_results, _error_code)

    def save_all_tests(self):
        """
        Saves all Testing data models managed by the controller.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _test in self.dicTests.values():
            (_results, _error_code) = self.save_test(_test.test_id)

        return False
