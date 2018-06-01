#!/usr/bin/env python
"""
############################
Survival Package Data Module
############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.survival.Survival.py is part of The RTK Project
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

from collections import OrderedDict

import numpy as np
from scipy.stats import chi2  # pylint: disable=E0611

try:
    import Utilities
    import analyses.statistics.NHPP as _nhpp
    import analyses.survival.KaplanMeier as _km
    import analyses.survival.MCF as _mcf
    from survival.Record import Model as Record
    from analyses.statistics.Bounds import calculate_fisher_bounds
    from analyses.statistics.growth.CrowAMSAA import calculate_crow_amsaa_mean, \
                                                     calculate_cramer_vonmises, \
                                                     calculate_crow_amsaa_chi_square, \
                                                     cramer_vonmises_critical_value
    from analyses.statistics.Distributions import Exponential, Gaussian, \
                                                  LogNormal, Weibull, \
                                                  time_between_failures
    from analyses.statistics.Duane import calculate_duane_mean
    from analyses.statistics.Regression import regression
except ImportError:
    import rtk.Utilities as Utilities
    import rtk.analyses.statistics.NHPP as _nhpp
    import rtk.analyses.survival.KaplanMeier as _km
    import rtk.analyses.survival.MCF as _mcf
    from rtk.survival.Record import Model as Record
    from rtk.analyses.statistics.Bounds import calculate_fisher_bounds
    from rtk.analyses.statistics.growth.CrowAMSAA import calculate_crow_amsaa_mean, \
                                                         calculate_cramer_vonmises, \
                                                         calculate_crow_amsaa_chi_square, \
                                                         cramer_vonmises_critical_value
    from rtk.analyses.statistics.Distributions import Exponential, Gaussian, \
                                                      LogNormal, Weibull, \
                                                      time_between_failures
    from rtk.analyses.statistics.Duane import calculate_duane_mean
    from rtk.analyses.statistics.Regression import regression

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'


class Model(object):  # pylint: disable=R0902, R0904
    """
    The Survival data model contains the attributes and methods for an
    Survival. The attributes of an Survival model are:

    :ivar dict dicRecords: dictionary of :py:class:`rtk.survival.Record` data
                           models associated with the selected Survival
                           analysis.  The key is the Record ID and the value is
                           a pointer to the instance of the Record.
    :ivar dict dicMTBF: dictionary of MTBF values for the selected
                        s-distribution with estimate parameters over time.  Key
                        is the time at which the MTBF is calculated and the
                        value is a list of MTBF values in the format of
                        [lower bound, point estimate, upper bound].
    :ivar dict dicReliability: dictionary of reliability values for the
                               selected s-distribution with estimate parameters
                               over time.  Key is the time at which the
                               reliability is calculated and the value is a
                               list of reliability values in the format of
                               [lower bound, point estimate, upper bound].
    :ivar list scale: list of [lower bound, point estimate, upper bound] values
                      of the estimated scale parameter.
    :ivar list shape: list of [lower bound, point estimate, upper bound] values
                      of the estimated shape parameter.
    :ivar list location: list of [lower bound, point estimate, upper bound]
                          values of the estimated location parameter.
    :ivar list variance: list of variances for [scale parameter,
                         shape parameter, location parameter]
    :ivar list covariance: list of covariances for [scale-shape,
                           scale-location, shape-location]
    :ivar hazard: `numpy.ndarray <https://docs.scipy.org/doc/numpy-1.10.0/reference/arrays.ndarray.html>`_
    :ivar km: `numpy.ndarray <https://docs.scipy.org/doc/numpy-1.10.0/reference/arrays.ndarray.html>`_
    :ivar mcf: `numpy.ndarray <https://docs.scipy.org/doc/numpy-1.10.0/reference/arrays.ndarray.html>`_
    :ivar list nhpp: default value: []
    :ivar int revision_id: default value: 0
    :ivar int survival_id: default value: 0
    :ivar int assembly_id: default value: 0
    :ivar str description: default value: ''
    :ivar int source: default value: 0
    :ivar int distribution_id: default value: 0
    :ivar float confidence: default value: 0.75
    :ivar int confidence_type: default value: 0
    :ivar int confidence_method: default value: 0
    :ivar int fit_method: default value: 0
    :ivar float rel_time: default value: 100.0
    :ivar int n_rel_points: default value: 0
    :ivar int n_suspensions: default value: 0
    :ivar int n_failures: default value: 0
    :ivar float mhb: default value: 0.0
    :ivar float lp: default value: 0.0
    :ivar float lr: default value: 0.0
    :ivar float aic: default value: 0.0
    :ivar float bic: default value: 0.0
    :ivar float mle: default value: 0.0
    :ivar float start_time: default value: 0.0
    :ivar float end_time: default value: 0.0
    :ivar int start_date: default value: 0
    :ivar int end_date: default value: 0
    :ivar float chisq:
    :ivar float cvm:
    """

    def __init__(self):
        """
        Method to initialize a Survival data model instance.
        """

        # Initialize private dict attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dict attributes.
        self.dicRecords = {}
        self.dicMTBF = {}
        self.dicHazard = {}
        self.dicReliability = {}

        # Initialize public list attributes.
        self.scale = [0.0, 0.0, 0.0]
        self.shape = [0.0, 0.0, 0.0]
        self.location = [0.0, 0.0, 0.0]
        self.variance = [0.0, 0.0, 0.0]
        self.covariance = [0.0, 0.0, 0.0]
        self.chi2_critical_value = [0.0, 0.0]
        self.hazard = np.array([])
        self.km = np.array([])
        self.mcf = np.array([])
        self.nhpp = []

        # Initialize public scalar attributes.
        self.revision_id = 0
        self.survival_id = 0
        self.assembly_id = 0
        self.description = ''
        self.source = 0
        self.distribution_id = 0  # 1=MCF, 2=Kaplan-Meier,
        # 3=NHPP-Power Law,
        # 4=NHPP-LogLinear, 5=Exponential,
        # 6=Lognormal, 7=Normal, 8=Weibull,
        # 9=WeiBayes
        self.confidence = 0.75
        self.confidence_type = 0  # 1=Lower, 2=Upper, 3=Two-sided
        self.confidence_method = 0  # 1=Crow, 2=Duane, 3=Fisher,
        # 4=Likelihood, 5=Bootstrap
        self.fit_method = 0  # 1=MLE, 2=Rank Regression
        self.rel_time = 100.0
        self.n_rel_points = 0
        self.n_suspensions = 0
        self.n_failures = 0
        self.mhb = 0.0  # MIL-HDBK trend statistic
        self.lp = 0.0  # Laplace trend statistic
        self.lr = 0.0  # Lewis-Robinson trend statistic
        self.rho = 0.0  # Serial correlation coefficient
        self.aic = 0.0  # Aikake information criterion
        self.bic = 0.0  # Bayesian information criterion
        self.mle = 0.0  # Maximum likelihood estimate
        self.start_time = 0.0
        self.end_time = 0.0
        self.start_date = 0
        self.end_date = 0
        self.n_datasets = 0
        self.chi_square = 0.0  # AMSAA chi-square statistic
        self.cramer_vonmises = 0.0  # AMSAA Cramer-vonMises statistic
        self.cvm_critical_value = 0.0  # AMSAA Cramer-vonMises critical value
        self.grouped = 0

    def calculate_tbf(self, previous_id, current_id):
        """
        Method to calculate the time between failure of subsequent failures in
        a dataset.

        :param int previous_id: the Record ID of the previous failure or
                                suspension.
        :param int current_id: the Record ID of the current failure or
                               suspension.
        :return: False on success or True if an error is encountered.
        :rtype: bool
        """

        _p_record = self.dicRecords[previous_id]
        _c_record = self.dicRecords[current_id]

        _c_record.interarrival_time = time_between_failures(
            _p_record, _c_record)

        return False

    def estimate_parameters(self):
        """
        Method to fit data a parametric distribution and estimate the
        parameters of the fitted distribution.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _data = self._create_dataset()

        if self.distribution_id == 1:  # MCF
            self.estimate_mcf()
        elif self.distribution_id == 2:  # Kaplan-Meier
            self.estimate_kaplan_meier()
        elif self.distribution_id == 3:  # NHPP - Power Law
            self.estimate_nhpp_power_law()
        elif self.distribution_id == 4:  # NHPP - Log Linear
            print "NHPP - Log Linear"
        elif self.distribution_id == 5:  # Exponential
            self.estimate_exponential(_data)
        elif self.distribution_id == 6:  # LogNormal
            self.estimate_lognormal(_data)
        elif self.distribution_id == 7:  # Gaussian
            self.estimate_gaussian(_data)
        elif self.distribution_id == 8:  # Weibull
            self.estimate_weibull(_data)

        return False

    def calculate_parameter_bounds(self, data):
        """
        Method to calculate confidence bounds on estimated parameters.

        :param list data: list of data to use for regression method.  Each
                          record in the list contains:
                            * 0 = Observed unit ID
                            * 1 = Interval start time
                            * 2 = Interval end time
                            * 3 = Time between failures or interarrival time
                            * 4 = Status of observation
                            * 5 = Quantity of observations
                            * 6 = Date of observation
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # TODO: Consider refactoring calculate_parameter_bounds; current McCabe Complexity metric=15.
        if self.confidence_method == 3:  # Fisher
            (self.scale[0], self.scale[2]) = calculate_fisher_bounds(
                self.scale[1], self.variance[0], self.confidence)

            (self.shape[0], self.shape[2]) = calculate_fisher_bounds(
                self.shape[1], self.variance[1], self.confidence)

            (self.location[0], self.location[2]) = calculate_fisher_bounds(
                self.location[1], self.variance[2], self.confidence)

        elif self.confidence_method == 4:  # Likelihood ratio
            if self.distribution_id == 5:  # Exponential
                (self.scale[0],
                 self.scale[2]) = Exponential().likelihood_bounds(
                     self.scale[1], self.location[1], self.confidence, data)
            elif self.distribution_id == 6:  # LogNormal
                (_lower, _upper) = LogNormal().likelihood_bounds(
                    [self.scale[1], self.shape[1]], self.confidence, data)
                self.scale[0] = min(_lower.values())
                self.scale[2] = max(_upper.values())
                self.shape[0] = [
                    _key for _key in _lower.keys()
                    if _lower[_key] == min(_lower.values())
                ][0]
                self.shape[2] = [
                    _key for _key in _upper.keys()
                    if _upper[_key] == max(_upper.values())
                ][0]
            elif self.distribution_id == 7:  # Gaussian
                (_lower, _upper) = LogNormal().likelihood_bounds(
                    [self.scale[1], self.shape[1]], self.confidence, data)
                self.scale[0] = min(_lower.values())
                self.scale[2] = max(_upper.values())
                self.shape[0] = [
                    _key for _key in _lower.keys()
                    if _lower[_key] == min(_lower.values())
                ][0]
                self.shape[2] = [
                    _key for _key in _upper.keys()
                    if _upper[_key] == max(_upper.values())
                ][0]
            elif self.distribution_id == 8:  # Weibull
                (self.scale[0], self.scale[2], self.shape[0],
                 self.shape[2]) = Weibull().likelihood_bounds(
                     [self.scale[1], self.shape[1]], self.confidence, data)

        return False

    def theoretical_distribution(self, data):
        """
        Method to retrieve the theoretical distribution based on the estimated
        model parameter(s).

        :param ndarray data: the data set that the theoretical distribution
                             will be created for.  This is a zero-based list of
                             lists or list of tuples where index 1 is the left
                             of the interval and index 2 is the right of the
                             interval.  The other indices are not used.
        :return: _probs; the probabilities of the theoretical distribution.
        :rtype: ndarray
        """

        _probs = []

        if self.distribution_id == 5:
            _probs = Exponential().theoretical_distribution(
                data, [self.scale[1]])
        elif self.distribution_id == 6:
            _probs = LogNormal().theoretical_distribution(
                data, [self.scale[1], self.shape[1]])
        elif self.distribution_id == 7:
            _probs = Gaussian().theoretical_distribution(
                data, [self.scale[1], self.shape[1]])
        elif self.distribution_id == 8:
            _probs = Weibull().theoretical_distribution(
                data, [self.scale[1], self.shape[1]])

        return _probs

    def hazard_function(self):
        """
        Method to calculate the hazard function between start_time and
        end_time in intervals of step_time.  This method calculates the point
        estimate as well as the bounding values at each time step.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _step_time = int((self.rel_time - self.start_time) / self.n_rel_points)

        if self.distribution_id == 5:
            self.dicHazard = Exponential().hazard_function(
                self.scale, self.start_time, self.rel_time + _step_time,
                _step_time)
        elif self.distribution_id == 6:
            self.dicHazard = LogNormal().hazard_function(
                self.scale, self.shape, self.start_time,
                self.rel_time + _step_time, _step_time)
        elif self.distribution_id == 7:
            self.dicHazard = Gaussian().hazard_function(
                self.scale, self.shape, self.start_time,
                self.rel_time + _step_time, _step_time)
        elif self.distribution_id == 8:
            self.dicHazard = Weibull().hazard_function(
                self.scale, self.shape, self.start_time,
                self.rel_time + _step_time, _step_time)

        return False

    def mean(self):
        """
        Method to calculate the means between start_time and end_time in
        intervals of step_time.  This method calculates the point estimate as
        well as the bounding values at each time step.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _step_time = int((self.rel_time - self.start_time) / self.n_rel_points)

        if self.distribution_id == 5:
            self.dicMTBF = Exponential().mean(self.scale, self.start_time,
                                              self.rel_time + _step_time,
                                              _step_time)
        elif self.distribution_id == 6:
            self.dicMTBF = LogNormal().mean(
                self.scale, self.shape, self.start_time,
                self.rel_time + _step_time, _step_time)
        elif self.distribution_id == 7:
            self.dicMTBF = Gaussian().mean(self.scale, self.start_time,
                                           self.rel_time + _step_time,
                                           _step_time)
        elif self.distribution_id == 8:
            self.dicMTBF = Weibull().mean(
                self.scale, self.shape, self.start_time,
                self.rel_time + _step_time, _step_time)

        return False

    def reliability_function(self):
        """
        Method to calculate the reliability between start_time and end_time in
        intervals of step_time.  This method calculates the point estimate as
        well as the bounding values at each time step.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _step_time = int((self.rel_time - self.start_time) / self.n_rel_points)

        if self.distribution_id == 5:
            self.dicReliability = Exponential().reliability_function(
                self.scale, self.start_time, self.rel_time + _step_time,
                _step_time)
        elif self.distribution_id == 6:
            self.dicReliability = LogNormal().reliability_function(
                self.scale, self.shape, self.start_time,
                self.rel_time + _step_time, _step_time)
        elif self.distribution_id == 7:
            self.dicReliability = Gaussian().reliability_function(
                self.scale, self.shape, self.start_time,
                self.rel_time + _step_time, _step_time)
        elif self.distribution_id == 8:
            self.dicReliability = Weibull().reliability_function(
                self.scale, self.shape, self.start_time,
                self.rel_time + _step_time, _step_time)

        return False

    def estimate_mcf(self):
        """
        Method to estimate the Mean Cumulative Function.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _data = _mcf.format_data(self.dicRecords)
        self.mcf = _mcf.mean_cumulative_function(_data)

        _times = self.mcf[:, 0]
        self.n_failures = np.float(sum(self.mcf[:, 1]))

        self.mhb = _mcf.mil_handbook(_times)
        self.lp = np.float(_mcf.laplace(_times, self.n_failures))
        self.lr = np.float(_mcf.lewis_robinson(_times, self.n_failures))
        self.rho = np.float(_mcf.serial_correlation(_times, self.n_failures))

        return False

    def estimate_kaplan_meier(self):
        """
        Method to estimate the Kaplan-Meier (product limit) parameters.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_data, self.n_failures,
         self.n_suspensions) = _km.format_data(self.dicRecords)

        self.km, _rank = _km.kaplan_meier(_data, self.start_time,
                                          self.rel_time, self.confidence,
                                          self.confidence_type)

        (self.scale[0], self.scale[1], self.scale[2]) = _km.kaplan_meier_mean(
            self.km, _rank, self.confidence)

        self.hazard = _km.kaplan_meier_hazard(self.km)

        return False

    def estimate_nhpp_power_law(self):
        """
        Method to estimate the NHPP-Power Law parameters.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # TODO: Consider refactoring estimate_nhpp_power_law; current McCabe Complexity metric=11.
        self.nhpp = []

        _meanc = [0.0, 0.0, 0.0]
        _meani = [0.0, 0.0, 0.0]
        _failures = [
            _record.n_failures for _record in self.dicRecords.values()
        ]
        _times = [
            _record.right_interval for _record in self.dicRecords.values()
        ]
        _dates = [_record.failure_date for _record in self.dicRecords.values()]
        for _index, _time in enumerate(_times):
            _NHPP = _nhpp.power_law(
                _failures[:_index + 1], _times[:_index + 1],
                self.confidence_method, self.fit_method, self.confidence_type,
                self.confidence, self.rel_time)

            # Calculate the cumulative and instantaneous MTBF.
            if self.fit_method == 1:  # MLE
                _means = calculate_crow_amsaa_mean(self.rel_time, _NHPP[0][2],
                                                   _NHPP[1][2])
                _meanc[0] = _means[0]
                _meani[0] = _means[1]
                _means = calculate_crow_amsaa_mean(self.rel_time, _NHPP[0][1],
                                                   _NHPP[1][1])
                _meanc[1] = _means[0]
                _meani[1] = _means[1]
                _means = calculate_crow_amsaa_mean(self.rel_time, _NHPP[0][0],
                                                   _NHPP[1][0])
                _meanc[2] = _means[0]
                _meani[2] = _means[1]
            elif self.fit_method == 2:  # Regression
                _means = calculate_duane_mean(self.rel_time, 1.0 - _NHPP[1][2],
                                              1.0 / _NHPP[0][2])
                _meanc[0] = _means[0]
                _meani[0] = _means[1]
                _means = calculate_duane_mean(self.rel_time, 1.0 - _NHPP[1][1],
                                              1.0 / _NHPP[0][1])
                _meanc[1] = _means[0]
                _meani[1] = _means[1]
                _means = calculate_duane_mean(self.rel_time, 1.0 - _NHPP[1][0],
                                              1.0 / _NHPP[0][0])
                _meanc[2] = _means[0]
                _meani[2] = _means[1]

            self.nhpp.append([
                _time,
                sum(_failures[:_index + 1]),
                list(_NHPP[0]),
                list(_NHPP[1]),
                list(_meanc),
                list(_meani), _dates[_index]
            ])

        self.n_failures = sum(_failures)

        self.scale[0] = self.nhpp[-1][2][0]
        self.scale[1] = self.nhpp[-1][2][1]
        self.scale[2] = self.nhpp[-1][2][2]
        self.shape[0] = self.nhpp[-1][3][0]
        self.shape[1] = self.nhpp[-1][3][1]
        self.shape[2] = self.nhpp[-1][3][2]

        # Calculate trend statistic and critical values.
        _alpha_half = (1.0 - self.confidence) / 2.0

        if self.grouped == 0:  # Individual failure times.
            if self.end_time > 0.0:  # Time truncated test.
                _df = 2.0 * self.n_failures
            else:  # Failure truncated test.
                _df = 2.0 * (self.n_failures - 1)
            _upper = _alpha_half
            _lower = self.confidence + _alpha_half
        else:  # Grouped failure times.
            _df = len(_failures) - 1
            _upper = self.confidence
            _lower = 1.0 - self.confidence

        self.chi_square = calculate_crow_amsaa_chi_square(
            _failures, _times, self.shape[1], max(_times))
        self.chi2_critical_value[0] = chi2.ppf(_lower, _df)
        self.chi2_critical_value[1] = chi2.ppf(_upper, _df)

        # Calculate goodness of fit statistic and critical value.
        self.cramer_vonmises = calculate_cramer_vonmises(
            self.n_failures, _times, self.shape[1])
        self.cvm_critical_value = cramer_vonmises_critical_value(
            self.n_failures, self.confidence)

        return False

    def estimate_exponential(self, data):
        """
        Method to estimate the Exponential distribution parameters, mean,
        parameter and mean bounds, hazard function and reliability function.

        :param ndarray data: numpy array of data to use for regression method.
                             Each record in the array contains:
                            * 0 = Interval start time
                            * 1 = Interval end time
                            * 2 = Quantity of observations
                            * 3 = Status of observation
                            * 4 = Time between failures or interarrival time
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if self.fit_method == 1:
            _results = Exponential().maximum_likelihood_estimate(
                data, self.start_time, self.rel_time)

            self.n_suspensions = _results[3]
            self.n_failures = _results[4]
        elif self.fit_method == 2:
            _results = regression(data, self.start_time, self.rel_time)

            self.rho = _results[3]
            self.n_suspensions = _results[4]
            self.n_failures = _results[5]

        self.scale[1] = _results[0][0]
        self.location[1] = 0.0
        self.variance[0] = _results[1][0]
        self.variance[1] = 0.0
        self.variance[2] = 0.0
        self.covariance[0] = 0.0
        self.covariance[1] = 0.0
        self.covariance[2] = 0.0
        self.mle = _results[2][0]
        self.aic = _results[2][1]
        self.bic = _results[2][2]

        self.calculate_parameter_bounds(data)
        self.hazard_function()
        self.reliability_function()
        self.mean()

        return False

    def estimate_lognormal(self, data):
        """
        Method to estimate the LogNormal distribution parameters, mean,
        parameter and mean bounds, hazard function and reliability function.

        :param ndarray data: numpy array of data to use for regression method.
                             Each record in the array contains:
                                * 0 = Interval start time
                                * 1 = Interval end time
                                * 2 = Quantity of observations
                                * 3 = Status of observation
                                * 4 = Time between failures or interarrival
                                      time
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if self.fit_method == 1:
            _results = LogNormal().maximum_likelihood_estimate(
                data, self.start_time, self.rel_time)

            self.n_suspensions = _results[3]
            self.n_failures = _results[4]
        elif self.fit_method == 2:
            _results = regression(
                data, self.start_time, self.rel_time, dist='lognormal')

            self.rho = _results[3]
            self.n_suspensions = _results[4]
            self.n_failures = _results[5]

        self.scale[1] = _results[0][0]
        self.shape[1] = _results[0][1]
        self.variance[0] = _results[1][0]  # Scale
        self.variance[1] = _results[1][2]  # Shape
        self.covariance[0] = _results[1][1]  # Scale-Shape
        self.mle = _results[2][0]
        self.aic = _results[2][1]
        self.bic = _results[2][2]

        self.calculate_parameter_bounds(data)
        self.hazard_function()
        self.reliability_function()
        self.mean()

        return False

    def estimate_gaussian(self, data):
        """
        Method to estimate the Gaussian (Normal) distribution parameters, mean,
        parameter and mean bounds, hazard function and reliability function.

        :param ndarray data: numpy array of data to use for regression method.
                             Each record in the array contains:
                            * 0 = Interval start time
                            * 1 = Interval end time
                            * 2 = Quantity of observations
                            * 3 = Status of observation
                            * 4 = Time between failures or interarrival time
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if self.fit_method == 1:
            _results = Gaussian().maximum_likelihood_estimate(
                data, self.start_time, self.rel_time)

            self.n_suspensions = _results[3]
            self.n_failures = _results[4]
        elif self.fit_method == 2:
            _results = regression(
                data, self.start_time, self.rel_time, dist='normal')

            self.rho = _results[3]
            self.n_suspensions = _results[4]
            self.n_failures = _results[5]

        self.scale[1] = _results[0][0]
        self.shape[1] = _results[0][1]
        self.variance[0] = _results[1][0]  # Scale
        self.variance[1] = _results[1][2]  # Shape
        self.covariance[0] = _results[1][1]  # Scale-Shape
        self.mle = _results[2][0]
        self.aic = _results[2][1]
        self.bic = _results[2][2]

        self.calculate_parameter_bounds(data)
        self.hazard_function()
        self.reliability_function()
        self.mean()

        return False

    def estimate_weibull(self, data):
        """
        Method to estimate the Weibull distribution parameters, mean,
        parameter and mean bounds, hazard function and reliability function.

        :param ndarray data: numpy array of data to use for regression method.
                             Each record in the array contains:
                            * 0 = Interval start time
                            * 1 = Interval end time
                            * 2 = Quantity of observations
                            * 3 = Status of observation
                            * 4 = Time between failures or interarrival time
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if self.fit_method == 1:
            _results = Weibull().maximum_likelihood_estimate(
                data, self.start_time, self.rel_time)

            self.n_suspensions = _results[3]
            self.n_failures = _results[4]
        elif self.fit_method == 2:
            _results = regression(
                data, self.start_time, self.rel_time, dist='normal')

            self.rho = _results[3]
            self.n_suspensions = _results[4]
            self.n_failures = _results[5]

        self.scale[1] = _results[0][0]
        self.shape[1] = _results[0][1]
        self.variance[0] = _results[1][0]  # Scale
        self.variance[1] = _results[1][2]  # Shape
        self.covariance[0] = _results[1][1]  # Scale-Shape
        self.mle = _results[2][0]
        self.aic = _results[2][1]
        self.bic = _results[2][2]

        self.calculate_parameter_bounds(data)
        self.hazard_function()
        self.reliability_function()
        self.mean()

        return False

    def _create_dataset(self):
        """
        Method to create a dataset for analysis from the records in dicRecords.

        Each record in the returned array contains:
            * 0 = Interval start time
            * 1 = Interval end time
            * 2 = Quantity of observations
            * 3 = Status of observation
            * 4 = Time between failures or interarrival time

        :return: _data
        :rtype: numpy array
        """

        _data = []
        for _record_id in self.dicRecords.keys():
            # Replace any string status values with integer status values.  Set
            # right censored end point to infinity.
            if (self.dicRecords[_record_id].status == 'Right Censored'
                    or str(self.dicRecords[_record_id].status) == '2'):
                self.dicRecords[_record_id].interarrival_time = np.inf
                self.dicRecords[_record_id].status = 2
            elif (self.dicRecords[_record_id].status == 'Left Censored'
                  or self.dicRecords[_record_id].status == 'Interval Censored'
                  or str(self.dicRecords[_record_id].status) == '3'
                  or str(self.dicRecords[_record_id].status) == '4'):
                self.dicRecords[_record_id].status = 3
            else:
                self.dicRecords[_record_id].status = 1

            _data.append([
                self.dicRecords[_record_id].left_interval,
                self.dicRecords[_record_id].right_interval,
                self.dicRecords[_record_id].n_failures,
                self.dicRecords[_record_id].status,
                self.dicRecords[_record_id].interarrival_time
            ])

        # Convert the data set list of lists to a numpy array.
        _data = np.array(_data, dtype=float)

        return _data


class Survival(object):
    """
    The Survival data controller provides an interface between the Survival
    data model and an RTK view model.  A single Survival controller can
    manage one or more Survival data models.  The attributes of a
    Survival data controller are:

    :ivar _dao: the :class:`rtk.dao.DAO` to use when communicating with the RTK
                Project database.
    :ivar int _last_id: the last Survival ID used.
    :ivar dict dicSurvivals: Dictionary of the Survival data models managed.
                             Key is the Survival ID; value is a pointer to the
                             Survival data model instance.
    """

    def __init__(self):
        """
        Method to initialize a Survival data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dicSurvival = {}

    def request_survival(self, dao, revision_id):
        """
        Method to read the RTK Project database and load all the Survivals
        associated with the selected Revision.  For each Survival returned:

        #. Retrieve the inputs from the RTK Project database.
        #. Create a Survival data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Survivals being managed
           by this controller.

        :param rtk.DAO dao: the Data Access object to use for communicating
                            with the RTK Project database.
        :param int revision_id: the Revision ID to select the tasks for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._dao = dao

        self._last_id = self._dao.get_last_id('rtk_survival')[0]

        _query = "SELECT * FROM rtk_survival \
                  WHERE fld_revision_id={0:d}".format(revision_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_survivals = len(_results)
        except TypeError:
            _n_survivals = 0

        for i in range(_n_survivals):
            _survival = Model()
            _survival.set_attributes(_results[i])
            self.dicSurvival[_survival.survival_id] = _survival

        return (_results, _error_code)

    def add_survival(self, revision_id):
        """
        Adds a new Survival to the RTK Program's database.

        :param int revision_id: the Revision ID to add the new Survival to.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        try:
            _description = "New Survival Analysis " + str(self._last_id + 1)
        except TypeError:  # No tasks exist.
            _description = "New Survival Analysis 1"

        _query = "INSERT INTO rtk_survival \
                  (fld_revision_id, fld_description) \
                  VALUES (%d, '%s')" % (revision_id, _description)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # If the new Survival analysis was added successfully to the RTK
        # Project database:
        #   1. Retrieve the ID of the newly inserted Survival analysis.
        #   2. Create a new Survival model instance.
        #   3. Set the attributes of the new Survival model instance.
        #   4. Add the new Survival model to the controller dictionary.
        if _results:
            self._last_id = self._dao.get_last_id('rtk_survival')[0]

            _survival = Model()
            _survival.set_attributes(
                (revision_id, self._last_id, 0, _description, 0, 0, 0.75, 0, 2,
                 0, 100.0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0,
                 0, 0))
            self.dicSurvival[_survival.survival_id] = _survival

        return (_results, _error_code)

    def delete_survival(self, survival_id):
        """
        Method to delete the selected Survival analysis from the open RTK
        Program database.

        :param int survival_id: the ID of the Survival analysis to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "DELETE FROM rtk_survival \
                  WHERE fld_survival_id={0:d}".format(survival_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # Remove the Survival analysis from the survival dictionary.
        if _results:
            self.dicSurvival.pop(survival_id)

        return (_results, _error_code)

    def save_all_survivals(self):
        """
        Method to save all the Survival objects associated with the selected
        revision to the open RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _survival in self.dicSurvival.values():
            self.save_survival(_survival.survival_id)

        return False

    def save_survival(self, survival_id):
        """
        Method to save the Survival model information to the open RTK Program
        database.

        :param int survival_id: the ID of the Survival task to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _survival = self.dicSurvival[survival_id]

        _query = "UPDATE rtk_survival \
                  SET fld_assembly_id={2:d}, fld_description='{3:s}', \
                      fld_source={4:d}, fld_distribution_id={5:d}, \
                      fld_confidence={6:f}, fld_confidence_type={7:d}, \
                      fld_confidence_method={8:d}, fld_fit_method={9:d}, \
                      fld_rel_time={10:f}, fld_num_rel_points={11:d}, \
                      fld_num_suspension={12:d}, fld_num_failures={13:d}, \
                      fld_scale_ll={14:f}, fld_scale={15:f}, \
                      fld_scale_ul={16:f}, fld_shape_ll={17:f}, \
                      fld_shape={18:f}, fld_shape_ul={19:f}, \
                      fld_location_ll={20:f}, fld_location={21:f}, \
                      fld_location_ul={22:f}, fld_variance_1={23:f}, \
                      fld_variance_2={24:f}, fld_variance_3={25:f}, \
                      fld_covariance_1={26:f}, fld_covariance_2={27:f}, \
                      fld_covariance_3={28:f}, fld_mhb={29:f}, fld_lp={30:f}, \
                      fld_lr={31:f}, fld_aic={32:f}, fld_bic={33:f}, \
                      fld_mle={34:f}, fld_start_time={35:f}, \
                      fld_start_date={36:d}, fld_end_date={37:d} \
                  WHERE fld_revision_id={0:d} \
                  AND fld_survival_id={1:d}".format(
            _survival.revision_id, _survival.survival_id,
            _survival.assembly_id, _survival.description, _survival.source,
            _survival.distribution_id, _survival.confidence,
            _survival.confidence_type, _survival.confidence_method,
            _survival.fit_method, _survival.rel_time,
            _survival.n_rel_points, _survival.n_suspensions,
            int(_survival.n_failures), _survival.scale[0], _survival.scale[1],
            _survival.scale[2], _survival.shape[0], _survival.shape[1],
            _survival.shape[2], _survival.location[0], _survival.location[1],
            _survival.location[2], _survival.variance[0],
            _survival.variance[1], _survival.variance[2],
            _survival.covariance[0], _survival.covariance[1],
            _survival.covariance[2], _survival.mhb, _survival.lp, _survival.lr,
            _survival.aic, _survival.bic, _survival.mle, _survival.start_time,
            _survival.start_date, _survival.end_date)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # Save all the records.
        for _record_id in _survival.dicRecords.keys():
            (_results, _error_code) = self.save_record(
                survival_id, _record_id, _survival.dicRecords[_record_id])

        return (_results, _error_code)

    def request_records(self, survival_id):
        """
        Method to read the RTK Project database and load all the records
        associated with the selected Survival analysis object.

        :param int survival_id: the Survival ID the dataset is associated with.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "SELECT fld_record_id, fld_name, fld_failure_date, \
                         fld_left_interval, fld_right_interval, fld_status, \
                         fld_quantity, fld_tbf, fld_mode_type, \
                         fld_nevada_chart, fld_ship_date, fld_return_date, \
                         fld_user_float_1, fld_user_float_2, \
                         fld_user_float_3, fld_user_integer_1, \
                         fld_user_integer_2, fld_user_integer_3, \
                         fld_user_string_1, fld_user_string_2, \
                         fld_user_string_3 \
                  FROM rtk_survival_data \
                  WHERE fld_survival_id={0:d} \
                  ORDER BY fld_left_interval".format(survival_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_records = len(_results)
        except TypeError:
            _n_records = 0

        _survival = self.dicSurvival[survival_id]
        for i in range(_n_records):
            _record = Record()
            _record.set_attributes([survival_id] + list(_results[i][1:]))
            _survival.dicRecords[_results[i][0]] = _record

        _survival.dicRecords = OrderedDict(
            sorted(
                _survival.dicRecords.items(),
                key=lambda r: r[1].right_interval))

        return (_results, _error_code)

    def add_record(self, survival_id):
        """
        Method to add a Record to the selected Dataset.

        :param int survival_id: the ID of the Survival analysis the Dataset
                                belongs to.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "SELECT MAX(fld_record_id) \
                  FROM rtk_survival_data \
                  WHERE fld_survival_id={0:d}".format(survival_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        if _results[0][0] is None:
            _last_id = 1
        else:
            _last_id = _results[0][0] + 1

        _query = "INSERT INTO rtk_survival_data \
                  (fld_survival_id, fld_record_id) \
                  VALUES ({0:d}, {1:d})".format(survival_id, _last_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        if _results:
            _record = Record()
            _record.set_attributes([
                survival_id, 0, 719163, 0.0, 0.0, 0, 1, 0.0, 1, 0, 719163, 1,
                719163, 0, 0.0, 0.0, 0.0, 0, 0, 0, '', '', ''
            ])

            self.dicSurvival[survival_id].dicRecords[_last_id] = _record

        return (_results, _error_code)

    def delete_record(self, survival_id, record_id):
        """
        Method to delete the selected Record.

        :param int survival_id: the ID of the Survival analysis the Dataset
                                belongs to.
        :param int record_id: the ID of the Record to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "DELETE FROM rtk_survival_data \
                  WHERE fld_survival_id={0:d} \
                  AND fld_record_id={1:d}".format(survival_id, record_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        if _results:
            self.dicSurvival[survival_id].dicRecords.pop(record_id)

        return (_results, _error_code)

    def save_record(self, survival_id, record_id, record):
        """
        Method to save a Dataset Record to the open RTK Program database.

        :param int survival_id: the ID of the Survival analysis the Dataset
                                belongs to.
        :param int record_id: the ID of the Record to save.
        :param list record: the record values to save.
        :return: (_results, _error_code)
        :rype: tuple
        """

        _query = "UPDATE rtk_survival_data \
                  SET fld_name='{2:s}', fld_failure_date={3:d}, \
                      fld_left_interval={4:f}, fld_right_interval={5:f}, \
                      fld_status={6:d}, fld_quantity={7:d}, fld_tbf={8:f}, \
                      fld_mode_type={9:d}, fld_nevada_chart={10:d}, \
                      fld_ship_date={11:d}, fld_return_date={12:d}, \
                      fld_user_float_1={13:f}, fld_user_float_2={14:f}, \
                      fld_user_float_3={15:f}, fld_user_integer_1={16:d}, \
                      fld_user_integer_2={17:d}, fld_user_integer_3={18:d}, \
                      fld_user_string_1='{19:s}', fld_user_string_2='{20:s}', \
                      fld_user_string_3='{21:s}' \
                  WHERE fld_survival_id={0:d} \
                  AND fld_record_id={1:d}".format(
            survival_id, record_id, record.assembly_name, record.failure_date,
            record.left_interval, record.right_interval, record.status,
            record.n_failures, record.interarrival_time, record.mode_type,
            record.nevada_chart, record.ship_date, record.return_date,
            record.user_float_1, record.user_float_2, record.user_float_3,
            record.user_integer_1, record.user_integer_2,
            record.user_integer_3, record.user_string_1, record.user_string_2,
            record.user_string_3)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        if not _results:
            print survival_id, record_id

        return (_results, _error_code)

    def consolidate_dataset(self, survival_id):
        """
        Method to consolidate the dataset so there are only unique failure
        times, suspension times, and intervals with a quantity value rather
        than a single record for each failure.

        :param int survival_id: the Survival ID to consolidate records for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _query = "SELECT fld_record_id, fld_name, fld_left_interval, \
                         fld_right_interval, fld_status, fld_quantity \
                  FROM rtk_survival_data \
                  WHERE fld_survival_id={0:d} \
                  ORDER BY fld_left_interval ASC, \
                           fld_right_interval ASC, \
                           fld_status ASC".format(survival_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_records = len(_results)
        except TypeError:
            _n_records = 0

        _delete_id = []
        _keep_id = []
        _quantity = _results[0][5]
        for i in range(1, _n_records):
            # If the assemblies are the same, the left intervals are the same,
            # the right intervals are the same, and the status are the same,
            # increment the count of records with the same failure times and
            # add the previous record id to the list of records to delete.
            if (_results[i][1] == _results[i - 1][1]
                    and _results[i][2] == _results[i - 1][2]
                    and _results[i][3] == _results[i - 1][3]
                    and _results[i][4] == _results[i - 1][4]):
                _quantity += _results[i][5]
                _delete_id.append(_results[i - 1][0])
            else:
                _keep_id.append([_results[i - 1][0], _quantity])
                _quantity = _results[i][5]

        # Keep the last record.
        _keep_id.append([_results[-1][0], _quantity])

        # Update the quantity of the records to be kept.
        _n_keep = len(_keep_id)
        for i in range(_n_keep):
            _query = "UPDATE rtk_survival_data \
                      SET fld_quantity={0:d} \
                      WHERE fld_record_id={1:d}".format(
                _keep_id[i][1], _keep_id[i][0])
            self._dao.execute(_query, commit=True)

        # Delete the records that are "duplicates."
        _n_del = len(_delete_id)
        for i in range(_n_del):
            _query = "DELETE FROM rtk_survival_data \
                      WHERE fld_record_id={0:d}".format(_delete_id[i])
            self._dao.execute(_query, commit=True)

        return False

    def request_calculate(self, survival_id):
        """
        Method to request the survival analysis be performed.

        :param int survival_id: the Survival ID to consolidate records for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _survival = self.dicSurvival[survival_id]

        return _survival.estimate_parameters()

    def request_calculate_tbf(self, survival_id):
        """
        Method to request the interarrival times of a dataset be calculated.

        :param int survival_id: the Survival ID to consolidate records for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _survival = self.dicSurvival[survival_id]

        # Retrieve the first record in the record set and set it's interarrival
        # time equal to the right of the interval.
        _p_id = _survival.dicRecords.keys()[0]
        _record = _survival.dicRecords[_p_id]
        _record.interarrival_time = _record.right_interval

        # Iterate through the remaining records and calculate the interarrival
        # times.
        for _c_id in _survival.dicRecords.keys()[1:]:
            _survival.calculate_tbf(_p_id, _c_id)
            _p_id = _c_id

        return False
