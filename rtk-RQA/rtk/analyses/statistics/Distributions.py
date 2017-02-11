#!/usr/bin/env python
"""
######################################
Statistics Package Distribution Module
######################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.statistics.Distributions.py is part of The RTK Project
#
# All rights reserved.

import inspect
from collections import OrderedDict

# Import mathematical functions.
import numpy as np
import scipy.misc as misc
import scipy.optimize as optimize
from scipy.special import gamma
from scipy.stats import chi2, expon, exponweib, lognorm, norm     # pylint: disable=E0611

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


# WARNING: Refactor all distributions to accept Survival data model dicRecords as data input.
def fisher_information(model, p0, X, noise=1.0):    # pylint: disable=C0103
    """
    Function to calculate the Fisher information matrix for model sampled on
    grid X with parameters p0. Assumes samples are not correlated and have
    equal variance noise^2.

    :param callable model: the model function, f(x, ...). It must take the
                           independent variable as the first argument and the
                           parameters as separate remaining arguments.
    :param list p0: point in parameter space where Fisher information matrix is
                    evaluated.  Passed as:
                    [scale, shape, location]
    :param ndarray X: the data set to use for calculating the information
                      matrix.
    :param float noise: squared variance of the noise in data.
    :returns: _fisher; the Fisher information matrix.
    :rtype: ndarray
    """

    # TODO: Write test for this function.
    _labels = inspect.getargspec(model)[0][2:]
    _p0dict = dict(zip(_labels, p0))

    _D = np.zeros((len(p0), X.size))

    for i, argname in enumerate(_labels):
        _D[i, :] = [misc.derivative(
            lambda p: model(x, **dict(_p0dict, **{argname: p})),
            _p0dict[argname], dx=1.0e-6) for x in X]

    _fisher = 1.0 / noise**2 * np.einsum('mk, nk', _D, _D)

    return _fisher


def time_between_failures(previous, current):
    """
    Function to calculate times between failure (interarrival times).

    :param dict previous: the previous data set Record.
    :param dict current: the current data set Record.
    :return: _tbf; the time between previous and current failures.
    :rtype: float
    """
# TODO: Consider re-writing time_between_failures; current McCabe Complexity metric=10.
    if current.status == 'Event' or str(current.status) == '1':
        if current.left_interval == 0.0:
            _tbf = current.right_interval
        elif current.assembly_id == previous.assembly_id:
            _tbf = current.right_interval - previous.right_interval
        else:
            _tbf = current.right_interval
    elif current.status == 'Right Censored' or str(current.status) == '2':
        _tbf = 1E99
    elif(current.status == 'Left Censored' or str(current.status) == '3' or
         current.status == 'Interval Censored' or str(current.status) == '4'):
        _time1 = ((previous.right_interval -
                   previous.left_interval) / 2.0) + previous.left_interval
        _time2 = ((current.right_interval -
                   current.left_interval) / 2.0) + current.left_interval
        if current.assembly_id == previous.assembly_id:
            _tbf = _time2 - _time1
        else:
            _tbf = _time2
    else:
        _tbf = current.right_interval - previous.right_interval

    return _tbf


def format_data_set(data, start, end):
    """
    Function to format the data set and turn it into a numpy array for use in
    the maximum likelihood estimator functions for each distribution.

    :param list data: the data set to format.  This is a list of tuples where
                      each tuple has the following:
                            * 0 - Unit ID
                            * 1 - left of interval
                            * 2 - right of interval
                            * 3 - time between failure
                            * 4 - status of observation
                                    * 1 - event
                                    * 2 - right censored
                                    * 3 - interval censored
                            * 5 - quantity
    :param float start: the minimum time to include in the fit.  Used to
                        exclude outliers.
    :param float end: the maximum time to include in the fit.  Used to
                      exclude outliers.
    :return: (_data, _n_records); tuple of the formatted data set and the total
             number of records in the data set.
    :rtype: tuple
    """
# WARNING: Refactor format_data_set; current McCabe Complexity metric=12.
    # Sort data by the right of the interval.  Remove records occurring before
    # the start time and after the end time.
    _data = sorted(data, key=lambda x: float(x[2]))
    _data = [_rec for _rec in _data if float(_rec[1]) >= start]
    if end > 0.0:
        _data = [_rec for _rec in _data if float(_rec[2]) <= end]

    # Expand the data set so there is one record for each failure.  Loop
    # through the failure quantity passed for each record.
    _data2 = []
    for __, _record in enumerate(_data):
        for __ in range(int(_record[5])):
            _data2.append((_record[0], _record[1], _record[2], _record[3],
                           _record[4], 1))
    _data = np.array(_data2)

    # Replace the string status with integer status.
    _n_suspensions = 0
    _n_failures = 0
    for _record in _data:
        if _record[4] == 'Right Censored' or str(_record[4]) == '2':
            _record[2] = np.inf
            _record[4] = 2
            _n_suspensions += 1
        elif(_record[4] == 'Left Censored' or
             _record[4] == 'Interval Censored' or str(_record[4]) == '3'):
            _record[4] = 3
            _n_failures += 1
        else:
            _record[4] = 1
            _n_failures += 1

    # Coerce the data set into the form necessary for fitting to functions.
    _data = np.vstack((_data[:, 1], _data[:, 2], _data[:, 5], _data[:, 4],
                       _data[:, 3]))
    _data = np.array(np.transpose(_data), dtype=float)
    _n_records = len(_data)

    return(_data, _n_records, _n_suspensions, _n_failures)


class Exponential(object):
    """
    Class for the Exponential distribution.
    """

    def log_pdf(self, data, theta, loc=0.0):  # pylint: disable=C0103, R0201
        """
        Method to calculate the logarithm of the exponential probability
        density function (pdf).

        :param ndarray data: the data points at which to calculate the
                             logarithm of the pdf.
        :param float theta: the scale parameter.
        :param float loc: the location parameter.
        :return: the value(s) of the logarithm of the pdf.
        :rtype: ndarray
        """

        return np.log(theta) - theta * (data - loc)

    def log_likelihood(self, theta, loc, data):   # pylint: disable=C0103, R0201, W0613
        """
        Method to calculate the value of the log likelihood function for the
        exponential distribution.

        :param float theta: the scale parameter at which to evaluate the
                            log-likelihood.
        :param float loc: the location parameter at which to evaluate the
                          log-likelihood.
        :param ndarray data: the data set to calculate the log-likelihood for.
                             * 0 - left of the observation time interval
                             * 1 - right of the observation time interval
                             * 2 - number of events occurring at the
                                   observation time
                             * 3 - status, where status is:
                                * 1 - event
                                * 2 - right censored
                                * 3 - left censored
                                * 4 - interval censored
                             * 4 - interarrival time or time between failures
        """

# TODO: Extend this to the two-parameter Exponential
        # Calculate the value of the log-likelihood for the event observations.
        _event_t = data[np.where(data[:, 3] == 1)][:, 1]
        _event_n = data[np.where(data[:, 3] == 1)][:, 2]
        _event_ll = np.sum(_event_n *
                           np.log((theta * np.exp(-theta * _event_t))))

        # Calculate the value of the log-likelihood for the right-censored
        # observations.
        _right_t = data[np.where(data[:, 3] == 2)][:, 1]
        _right_n = data[np.where(data[:, 3] == 2)][:, 2]
        _right_ll = np.sum(_right_n * theta * _right_t)

        # Calculate the value of the log-likelihood for the left- and interval-
        # censored observations.
        _interval_lt = data[np.where(np.logical_or(data[:, 3] == 3,
                                                   data[:, 3] == 4))][:, 0]
        _interval_rt = data[np.where(np.logical_or(data[:, 3] == 3,
                                                   data[:, 3] == 4))][:, 1]
        _interval_n = data[np.where(np.logical_or(data[:, 3] == 3,
                                                  data[:, 3] == 4))][:, 2]

        _interval_ll = np.sum(_interval_n *
                              ((-theta * _interval_lt) -
                               (-theta * _interval_rt)))

        _logLik = _event_ll - _right_ll + _interval_ll

        return _logLik

    def log_likelihood_ratio(self, theta, loc, data, const=0.0):
        """
        Method to minimize when finding likelihood ratio confidence bounds.

        The equation this method calculates is:

            log[L(theta)] - chi2(alpha, 1) / 2.0

        where the keyword const is the chi2(alpha, 1) / 2.0 part.

        :param float theta: the scale parameter at which to evaluate the
                            log-likelihood.
        :param float loc: the location parameter at which to evaluate the
                          log-likelihood.
        :param ndarray data: the data set to calculate the log-likelihood for.
                             * 0 - left of the observation time interval
                             * 1 - right of the observation time interval
                             * 2 - number of events occurring at the
                                   observation time
                             * 3 - status, where status is:
                                * 1 - event
                                * 2 - right censored
                                * 3 - left censored
                                * 4 - interval censored
        :keyword float const: constant value to subtract from the
                              log-likelihood.  It is chi2(alpha, 1) / 2.0
        :return: _log_lik_ratio
        :rtype: float
        """

        _log_lik_ratio = self.log_likelihood(theta, loc, data) - const

        return _log_lik_ratio

    def likelihood_bounds(self, theta, loc, confidence, data):
        """
        Method to calculate the likelihood ratio confidence bounds.

        Likelihood confidence bounds are calculated by finding values for theta
        that satisfy:

            L(theta) = L(theta_hat) * exp(-chi2(alpha, 1) / 2.0)

        Taking logarithms (base e) of the equation above results in:

            log[L(theta)] = log[L(theta_hat)] - chi2(alpha, 1) / 2.0

        The same values of theta will minimize both, but logarithms are easier
        to work with.

        :param float theta: the scale parameter at which to evaluate the
                            log-likelihood.
        :param float loc: the location parameter at which to evaluate the
                          log-likelihood.
        :param float confidence: the confidence level at which to calculate the
                                 bounds.
        :param ndarray data: the data set to calculate the log-likelihood for.
                             * 0 - left of the observation time interval
                             * 1 - right of the observation time interval
                             * 2 - number of events occurring at the
                                   observation time
                             * 3 - status, where status is:
                                * 1 - event
                                * 2 - right censored
                                * 3 - interval censored
        :return: (_lower, _upper)
        :rtype: tuple
        """

        _log_lik_ratio = self.log_likelihood_ratio(theta, loc, data)
        _const = _log_lik_ratio - (chi2.ppf(confidence, 1) / 2.0)

        # To find the lower bound, we provide root with a starting value for
        # theta less than the point estimate; in this case 1/10 the value.
        _lower = optimize.root(self.log_likelihood_ratio, theta / 10.0,
                               args=(loc, data, _const)).x[0]

        # To find the upper bound, we provide root with a starting value for
        # theta equal to the point estimate.
        _upper = optimize.root(self.log_likelihood_ratio, theta,
                               args=(loc, data, _const)).x[0]

        return(_lower, _upper)

    def partial_derivatives(self, theta, data):     # pylint: disable=R0201
        """
        Method to calculate the value of the partial derivative of the
        exponential log-likelihood function with respect to theta.  This
        method is passed as an argument to scipy.optimize.fsolve() to find the
        value of theta that minimizes the partial.

        :param float theta: the scale parameter value at which to evaluate the
                            partial derivative.
        :param ndarray data: the data set to calculate the log-likelihood for.
                             * 0 - left of the observation time interval
                             * 1 - right of the observation time interval
                             * 2 - number of events occurring at the
                                   observation time
                             * 3 - status, where status is:
                                * 1 - event
                                * 2 - right censored
                                * 3 - left censored
                                * 4 - interval censored
        """

        # Calculate the value of the log-likelihood for the event observations.
        _event_t = data[np.where(data[:, 3] == 1)][:, 1]
        _event_n = data[np.where(data[:, 3] == 1)][:, 2]
        _event_ll = np.sum(_event_n * ((1.0 / theta) - _event_t))

        # Calculate the value of the log-likelihood for the right-censored
        # observations.
        _right_t = data[np.where(data[:, 3] == 2)][:, 1]
        _right_n = data[np.where(data[:, 3] == 2)][:, 2]
        _right_ll = np.sum(_right_n * _right_t)

        # Calculate the value of the log-likelihood for the left- and interval-
        # censored observations.  Use the midpoint of the interval as an
        # approximation.
        _interval_lt = data[np.where(np.logical_or(data[:, 3] == 3,
                                                   data[:, 3] == 4))][:, 0]
        _interval_rt = data[np.where(np.logical_or(data[:, 3] == 3,
                                                   data[:, 3] == 4))][:, 1]
        _interval_n = data[np.where(np.logical_or(data[:, 3] == 3,
                                                  data[:, 3] == 4))][:, 2]

        # Following are the exact equations for the interval censored
        # observations.
        _n = (_interval_lt * np.exp(-theta * _interval_lt)) - \
             (_interval_rt * np.exp(-theta * _interval_rt))
        _d = np.exp(-theta * _interval_lt) - np.exp(-theta * _interval_rt)
        _interval_ll = np.sum(_interval_n * (_n / _d))

        _del_theta = _event_ll - _right_ll - _interval_ll

        return _del_theta

    def maximum_likelihood_estimate(self, data, start, end):
        """
        Method to fit data to a parametric distribution and find point
        estimates of the parameters.  It is up to the calling function to
        calculate bounding values.

        :param ndarray data: the data set to fit.  This is a numpy array where
                             each record contains the following, in order:
                                * 0 = Interval start time
                                * 1 = Interval end time
                                * 2 = Quantity of observations
                                * 3 = Status of observation
                                * 4 = Time between failures or interarrival
                                      time
        :param float start: the minimum time to include in the fit.  Used to
                            exclude outliers.
        :param float end: the maximum time to include in the fit.  Used to
                          exclude outliers.
        :return: _fit; [[scale estimate, shape estimate, location estimate],
                        [scale variance, covariance, shape variance],
                        [MLE, AIC, BIC], correlation coeff.]
        :rtype: list
        """

        # _error_function = lambda s, x, y: ((s[0] + s[1] * x) - y)

        # Initialize lists to hold results.
        _parameters = [0.0, 0.0]            # Scale and location parameters.
        _variance = [0.0, 0.0, 0.0]         # Scale variance, covariance,
                                            # location variance.
        _gof = [0.0, 0.0, 0.0]              # MLE, AIC, BIC

        # Sort data by the right of the interval.  Remove records occurring
        # before the start time and after the end time.
        _data = sorted(data, key=lambda x: float(x[1]))
        _data = [_rec for _rec in _data if float(_rec[0]) >= start]
        _data = [_rec for _rec in _data if float(_rec[1]) <= end]
        _data = np.array(_data)

        # Count the number of suspensions, failures, and records.
        _n_suspensions = sum(x[2] for x in _data if x[3] == 2)
        _n_failures = sum(x[2] for x in _data
                          if x[3] == 1 or x[3] == 3 or x[3] == 4)
        _n_records = len(_data)

        # Estimate the initial guess for the scale parameter using the fit
        # function from scipy.stats.  Then minimize the partial derivitive of
        # the likelihood function to find the final theta value.
        _theta = 1.0 / expon.fit(_data[:, 1])[1]
        _parameters[0] = optimize.fsolve(self.partial_derivatives, _theta,
                                         args=(_data))[0]

        _fI = fisher_information(self.log_pdf, _parameters, _data[:, 3])
        _variance[0] = 1.0 / _fI[0, 0]

        _gof[0] = self.log_likelihood(_parameters[0], _parameters[1], _data)
        _gof[1] = -2.0 * _gof[0] + 2.0
        _gof[2] = -2.0 * _gof[0] + (np.log(_n_records) - np.log(np.pi))

        _fit = [_parameters, _variance, _gof, _n_suspensions, _n_failures]

        return _fit

    def theoretical_distribution(self, data, params):   # pylint: disable=R0201
        """
        Method to create a data set from the theoretical distribution given the
        parameters.

        :param ndarray data: the data set that the theoretical distribution
                             will be created for.  This is a zero-based list of
                             lists or list of tuples where index 1 is the left
                             of the interval and index 2 is the right of the
                             interval.  The other indices are not used.
        :param list params: list with the values of the distribution
                            parameters.
        :return: _y; the probabilities of the theoretical distribution with
                 parameters para.
        :rtype: ndarray
        """

        _x = np.sort(np.array(data, dtype=float))
        _y = 1.0 - np.exp(-params[0] * _x)

        return _y

    def hazard_function(self, scale, start_time, end_time, step_time):  # pylint: disable=R0201
        """
        Method to calculate the hazard function for the Exponential
        distribution between start_time and end_time in intervals of step_time.
        This method calculates the point estimate as well as the bounding
        values at each time step.

        :param float scale: the scale parameter (lambda) for the Exponential
                            distribution to calculate the hazard function for.
        :param float start_time: the first time to calculate the hazard
                                 function.
        :param float end_time: the last time to calculate the hazard function.
        :param int step_time: the interval of time between start_time and
                              end_time to calculate the hazard function.
        :return: _hazard; a dict of lists where the key is the time at which
                 the hazard functions was calculated and the value is a list
                 of the lower bound, point estimate, and upper bound.
        :rtype: dict
        """

        _hazard = OrderedDict()

        for _time in range(int(start_time), int(end_time), int(step_time)):
            _hazard[_time] = scale

        return _hazard

    def mean(self, scale, start_time, end_time, step_time):     # pylint: disable=R0201
        """
        Method to calculate the hazard function for the Exponential
        distribution between start_time and end_time in intervals of step_time.
        This method calculates the point estimate as well as the bounding
        values at each time step.

        :param float scale: the scale parameter (lambda) for the Exponential
                            distribution to calculate the means for.
        :param float start_time: the first time to calculate the mean.
        :param float end_time: the last time to calculate the mean.
        :param int step_time: the interval of time between start_time and
                              end_time to calculate the mean.
        :return: _mean; a dict of lists where the key is the time at which
                 the means were calculated and the value is a list of the lower
                 bound, point estimate, and upper bound.
        :rtype: dict
        """

        _mean = {}

        for _time in range(int(start_time), int(end_time), int(step_time)):
            _values = [0.0, 0.0, 0.0]

            _values[0] = 1.0 / scale[2]
            _values[1] = 1.0 / scale[1]
            _values[2] = 1.0 / scale[0]

            _mean[_time] = _values

        return _mean

    def reliability_function(self, scale, start_time, end_time, step_time):     # pylint: disable=R0201
        """
        Method to calculate the reliability function for the Exponential
        distribution between start_time and end_time in intervals of step_time.
        This method calculates the point estimate as well as the bounding
        values at each time step.

        :param float scale: the scale parameter (lambda) for the Exponential
                            distribution to calculate the reliability function
                            for.
        :param float start_time: the first time to calculate the mean.
        :param float end_time: the last time to calculate the mean.
        :param int step_time: the interval of time between start_time and
                              end_time to calculate the mean.
        :return: _reliability; a dict of lists where the key is the time at
                 which the reliability function was calculated and the value is
                 a list of the lower bound, point estimate, and upper bound.
        :rtype: dict
        """

        _reliability = OrderedDict()

        for _time in range(int(start_time), int(end_time), int(step_time)):
            _values = [0.0, 0.0, 0.0]

            _values[0] = np.exp(-scale[0] * _time)
            _values[1] = np.exp(-scale[1] * _time)
            _values[2] = np.exp(-scale[2] * _time)

            _reliability[_time] = _values

        return _reliability


class Gaussian(object):
    """
    Class for the Gaussian distribution.
    """

    def log_pdf(self, data, mu, sigma):     # pylint: disable=C0103, R0201
        """
        Method to calculate the logarithm of the gaussian probability density
        function (pdf).

        :param ndarray data: the data points at which to calculate the
                             logarithm of the pdf.
        :param float mu: the value of the scale parameter.
        :param float sigma: the value of the shape parameter.
        :return: the value(s) of the logarithm of the pdf.
        :rtype: ndarray
        """

        _log_pdf = (1.0 / sigma * np.sqrt(2.0 * np.pi)) - \
                   (0.5 * ((np.log(data) - mu) / sigma)**2.0)

        return _log_pdf

    def log_likelihood(self, x, data):      # pylint: disable=C0103, R0201
        """
        Method to calculate the value of the log likelihood function for the
        Gaussian distribution.

        :param list x: the parameter values at which to evaluate the
                       log-likelihood.
        :param ndarray data: the data set to calculate the log-likelihood for.
                             * 0 - left of the observation time interval
                             * 1 - right of the observation time interval
                             * 2 - number of events occurring at the
                                   observation time.
                            * 3 - status, where status is:
                                * 1 - event
                                * 2 - right censored
                                * 3 - interval censored
        """

        # Calculate the value of the log-likelihood for the event observations.
        _event_t = data[np.where(data[:, 3] == 1)][:, 1]
        _event_n = data[np.where(data[:, 3] == 1)][:, 2]
        _event_ll = np.sum(_event_n *
                           np.log((1.0 / x[1]) *
                                  norm.pdf((_event_t - x[0]) / x[1])))

        # Calculate the value of the log-likelihood for the right-censored
        # observations.
        _right_t = data[np.where(data[:, 3] == 2)][:, 1]
        _right_n = data[np.where(data[:, 3] == 2)][:, 2]
        _right_ll = np.sum(_right_n *
                           np.log((1.0 - norm.cdf((np.log(_right_t) - x[0]) /
                                                  x[1]))))

        # Calculate the value of the log-likelihood for the left- and interval-
        # censored observations.
        _interval_lt = data[np.where(np.logical_or(data[:, 3] == 3,
                                                   data[:, 3] == 4))][:, 0]
        _interval_rt = data[np.where(np.logical_or(data[:, 3] == 3,
                                                   data[:, 3] == 4))][:, 1]
        _interval_n = data[np.where(np.logical_or(data[:, 3] == 3,
                                                  data[:, 3] == 4))][:, 2]

        _interval_ll = np.sum(_interval_n *
                              np.log(norm.cdf((_interval_rt - x[0]) / x[1]) -
                                     norm.cdf((_interval_lt - x[0]) / x[1])))

        _logLik = _event_ll - _right_ll + _interval_ll

        return _logLik

    def log_likelihood_ratio(self, pars, data, const=0.0):
        """
        Method to minimize when finding likelihood ratio confidence bounds.

        The equation this method calculates is:

            log[L(mu, sigma)] - chi2(alpha, 1) / 2.0

        where the keyword const is the chi2(alpha, 1) / 2.0 part.

        :param float pars: the parameter values at which to evaluate the
                           log-likelihood.
        :param ndarray data: the data set to calculate the log-likelihood for.
                             * 0 - left of the observation time interval
                             * 1 - right of the observation time interval
                             * 2 - number of events occurring at the
                                   observation time
                             * 3 - status, where status is:
                                * 1 - event
                                * 2 - right censored
                                * 3 - left censored
                                * 4 - interval censored
        :keyword float const: constant value to subtract from the
                              log-likelihood.  It is chi2(alpha, 1) / 2.0
        :return: _log_lik_ratio
        :rtype: float
        """

        _log_lik_ratio = self.log_likelihood(pars, data) - const

        return _log_lik_ratio

    def likelihood_bounds(self, pars, confidence, data):
        """
        Method to calculate the likelihood ratio confidence bounds for the
        parameters.

        Likelihood confidence bounds are calculated by finding values for mu,
        while holding sigma constant, that satisfy:

            L(mu, sigma) = L(mu_hat, sig_hat) * exp(-chi2(alpha, 1) / 2.0)

        Taking logarithms (base e) of the equation above results in:

            log[L(mu, sigma)] = log[L(mu_hat, sig_hat)] - chi2(alpha, 1) / 2.0

        The same values of theta will minimize both, but logarithms are easier
        to work with.

        :param list of float pars: the parameter values at which to evaluate
                                   the log-likelihood.
        :param float confidence: the confidence level at which to calculate the
                                 bounds.
        :param ndarray data: the data set to calculate the log-likelihood for.
                             * 0 - left of the observation time interval
                             * 1 - right of the observation time interval
                             * 2 - number of events occurring at the
                                   observation time
                             * 3 - status, where status is:
                                * 1 - event
                                * 2 - right censored
                                * 3 - left censored
                                * 4 - interval censored
        :return: (_lower, _upper)
        :rtype: tuple
        """
# TODO: Consider re-writing Gaussian.likelihood_bounds; current McCabe Complexity metric=10.
        def _shadow_func(pars, data, const):
            """
            Shadow function used to minimize the log-likelihood ratio.  It's a
            hack to ensure the correct number of arguments are returned.
            """

            return [self.log_likelihood_ratio(pars, data, const), 0.0]

        def _sigma_mu_func(x_var, m1, m2, intercept):
            """
            Function describing the relationship between mu and sigma.  This
            relationship parabolic for both upper and lower limits.
            """

            return m1 * x_var**2.0 + m2 * x_var + intercept

        def _sigma_limits(lower, upper):
            """
            Function to find the two sigma values at which mu is the same.
            Used to find the limits on sigma over which the parabolic
            relationship exists.
            """

            for _keyl in lower.keys():
                for _keyu in upper.keys():
                    if(abs(upper[_keyu] - lower[_keyl]) < 1.0E-6 and
                       _keyl < _keyu):
                        return(_keyl, _keyu)

        _lower = OrderedDict()
        _upper = OrderedDict()

        _log_lik_ratio = self.log_likelihood_ratio(pars, data)
        _const = _log_lik_ratio - (chi2.ppf(confidence, 1) / 2.0)

        for _index in range(100):
            # Set the sigma step value for this iteration.
            _sigma = pars[1] * (0.5 + (0.5 * _index / 25))

            # To find the lower bound, we provide root with a starting value
            # for mu less than the point estimate; in this case 1/10 the value.
            _lower[_sigma] = optimize.root(_shadow_func,
                                           [pars[0] / 10.0, _sigma],
                                           args=(data, _const)).x[0]

            # To find the upper bound, we provide root with a starting value
            # for mu greater than the point estimate; in this case double.
            _upper[_sigma] = optimize.root(_shadow_func,
                                           [2.0 * pars[0], _sigma],
                                           args=(data, _const)).x[0]

        # Find the values of sigma where the difference between the lower and
        # upper limits is less than 1.0E-6.  There will be two points found and
        # these are considered the mu values between which sigma is
        # well-behaved.  Only the key-value pairs falling between these values
        # will be kept and used to find the limits.
        _sigma = _sigma_limits(_lower, _upper)
        _upper.values = [_upper[y] for y in _upper.keys()
                         if y >= _sigma[0] and y <= _sigma[1]]
        _upper.keys = [y for y in _upper.keys()
                       if y >= _sigma[0] and y <= _sigma[1]]
        _lower.values = [_lower[y] for y in _lower.keys()
                         if y >= _sigma[0] and y <= _sigma[1]]
        _lower.keys = [y for y in _lower.keys()
                       if y >= _sigma[0] and y <= _sigma[1]]

        # Find the slope and intercept for the lower bounds assuming the
        # sigma-mu relationship is parabolic.
        _poptl, __ = optimize.curve_fit(_sigma_mu_func, _upper.keys,
                                        _upper.values)
        _mu_l = min(_lower.values)

        # Find the slope and intercept for the upper bounds assuming the
        # sigma-mu relationship is parabolic.
        _poptu, __ = optimize.curve_fit(_sigma_mu_func, _lower.keys,
                                        _lower.values)
        _mu_u = max(_upper.values)

        _sigma = np.roots([_poptu[0] - _poptl[0],
                           _poptu[1] - _poptl[1],
                           _poptu[2] - _poptl[2]])

        return(_mu_l, _mu_u, _sigma[1], _sigma[0])

    def partial_derivatives(self, pars, data):         # pylint: disable=C0103, R0201, R0914
        """
        Method to calculate the value of the partial derivatives of the
        gaussian log-likelihood function with respect to mu and sigma.  This
        function is passed as an argument to scipy.optimize.fsolve() to find
        the values of mu and sigma that simultaneously minimizes the partials.

        :param list pars: the values of mu and sigma at which to calculate the
                          partials.
        :param ndarray data: the data set to calculate the log-likelihood for.
                             * 0 - left of the observation time interval
                             * 1 - right of the observation time interval
                             * 2 - number of events occurring at the
                                   observation time
                             * 3 - status, where status is:
                                * 1 - event
                                * 2 - right censored
                                * 3 - left censored
                                * 4 - interval censored
        """

        # Calculate the value of the log-likelihood for the event observations.
        _event_t = data[np.where(data[:, 3] == 1)][:, 1]
        _event_n = data[np.where(data[:, 3] == 1)][:, 2]
        _event_sigma = np.sum(_event_n *
                              (((_event_t - pars[0]) / pars[1]**3.0) -
                               (1.0 / pars[1])))
        _event_mu = (1.0 / pars[1]**2.0) * np.sum(_event_n *
                                                  (_event_t - pars[0]))

        # Calculate the value of the log-likelihood for the right-censored
        # observations.
        _right_t = data[np.where(data[:, 3] == 2)][:, 1]
        _right_n = data[np.where(data[:, 3] == 2)][:, 2]

        _norm = (_right_t - pars[0]) / pars[1]
        _cdf = norm.cdf(_norm)
        _right_mu = (1.0 / pars[1]) * \
            np.sum(_right_n * (norm.pdf(_norm) / (1.000000001 - _cdf)))
        _right_sigma = (1.0 / pars[1]) * \
            np.sum(_right_n *
                   ((_norm * norm.pdf(_norm)) / (1.000000001 - _cdf)))

        # Calculate the value of the log-likelihood for the left- and interval-
        # censored observations.  Use the midpoint of the interval as an
        # approximation.
        _interval_lt = data[np.where(np.logical_or(data[:, 3] == 3,
                                                   data[:, 3] == 4))][:, 0]
        _interval_rt = data[np.where(np.logical_or(data[:, 3] == 3,
                                                   data[:, 3] == 4))][:, 1]
        _interval_n = data[np.where(np.logical_or(data[:, 3] == 3,
                                                  data[:, 3] == 4))][:, 2]

        # Following are the exact equations for the interval censored
        # observations.
        _norm_r = (_interval_rt - pars[0]) / pars[1]
        _pdf_r = norm.pdf(_norm_r)
        _cdf_r = norm.cdf(_norm_r)

        _norm_l = (_interval_lt - pars[0]) / pars[1]
        _pdf_l = norm.pdf(_norm_l)
        _cdf_l = norm.cdf(_norm_l)

        _n = _pdf_r - _pdf_l
        _d = _cdf_r - _cdf_l
        _interval_mu = (1.0 / pars[1]) * np.sum(_interval_n * _n / _d)

        _n = (_norm_r * _pdf_r) - (_norm_l * _pdf_l)
        _interval_sigma = (1.0 / pars[1]) * np.sum(_interval_n * _n / _d)

        _del_mu = _event_mu + _right_mu - _interval_mu
        _del_sigma = _event_sigma + _right_sigma - _interval_sigma

        return _del_mu * _del_sigma

    def maximum_likelihood_estimate(self, data, start, end):    # pylint: disable=R0914
        """
        Method to fit data to a parametric distribution and find point
        estimates of the parameters.  It is up to the calling function to
        calculate bounding values.

        :param ndarray data: the data set to fit.  This is a numpy array where
                             each record contains the following, in order:
                                * 0 = Interval start time
                                * 1 = Interval end time
                                * 2 = Quantity of observations
                                * 3 = Status of observation
                                * 4 = Time between failures or interarrival
                                      time
        :param float start: the minimum time to include in the fit.  Used to
                            exclude outliers.
        :param float end: the maximum time to include in the fit.  Used to
                          exclude outliers.
        :return: _fit; [[scale estimate, shape estimate, location estimate],
                        [scale variance, covariance, shape variance],
                        [MLE, AIC, BIC], correlation coeff.]
        :rtype: list
        """

        def _shadow_func(pars, data):
            """
            Shadow function used to ensure the correct number of values are
            returned when finding roots.
            """

            return [self.partial_derivatives(pars, data), 0.0]

        # Initialize lists to hold results.
        _parameters = [0.0, 0.0]            # Scale and location parameters.
        _variance = [0.0, 0.0, 0.0]         # Scale variance, covariance,
                                            # location variance.
        _gof = [0.0, 0.0, 0.0]              # MLE, AIC, BIC

        # Sort data by the right of the interval.  Remove records occurring
        # before the start time and after the end time.
        _data = sorted(data, key=lambda x: float(x[1]))
        _data = [_rec for _rec in _data if float(_rec[0]) >= start]
        _data = [_rec for _rec in _data if float(_rec[1]) <= end]
        _data = np.array(_data)

        # Count the number of suspensions, failures, and records.
        _n_suspensions = sum(x[2] for x in _data if x[3] == 2)
        _n_failures = sum(x[2] for x in _data
                          if x[3] == 1 or x[3] == 3 or x[3] == 4)
        _n_records = len(_data)

        # Adjust the right-censored times to be the mid-point between the
        # censored time and the maximum oberserved time in the data set.
        _adj_right = (max(_data[:, 1]) +
                      _data[np.where(_data[:, 3] == 2), 1]) / 2.0
        _data[np.where(_data[:, 3] == 2), 1] = _adj_right

        # Adjust the interval-censored times so they can be passed to the
        # fit method.
        _interval_lt = _data[np.where(_data[:, 3] == 3)][:, 0]
        _interval_rt = _data[np.where(_data[:, 3] == 3)][:, 1]
        _interval_t = (_interval_lt + _interval_rt) / 2.0
        _data[np.where(_data[:, 3] == 3), 1] = _interval_t

        # Provide an estimate of mu and sigma assuming no suspensions and
        # using the right of the interval.  Use these as the starting
        # values to scipy.optimize.fsolve.
        (_mu, _sigma) = norm.fit(np.array(_data[:, 1], dtype=float))
        _params = optimize.fsolve(_shadow_func, [_mu, _sigma],
                                  args=(data))

        _parameters[0] = _params[0]
        _parameters[1] = _params[1]

        _fI = fisher_information(self.log_pdf, _parameters, _data[:, 3])
        _variance[0] = 1.0 / np.diag(_fI)[0]
        _variance[1] = 1.0 / _fI[0][1]
        _variance[2] = 1.0 / np.diag(_fI)[1]

        # Calculate the MLE, AIC, and BIC
        _gof[0] = self.log_likelihood([_parameters[0], _parameters[1]], _data)
        _gof[1] = -2.0 * _gof[0] + 4.0
        _gof[2] = -2.0 * _gof[0] + 4.0 * np.log(_n_records)

        _fit = [_parameters, _variance, _gof, _n_suspensions, _n_failures]

        return _fit

    def theoretical_distribution(self, data, params):   # pylint: disable=R0201
        """
        Method to create a data set from the theoretical distribution given the
        parameters.

        :param ndarray data: the data set that the theoretical distribution
                             will be created for.  This is a zero-based list of
                             lists or list of tuples where index 1 is the left
                             of the interval and index 2 is the right of the
                             interval.  The other indices are not used.
        :param list params: list with the values of the distribution
                            parameters.
        :return: _y; the probabilities of the theoretical distribution with
                 parameters params.
        :rtype: ndarray
        """

        _x = np.sort(np.array(data, dtype=float))

        _x = (_x - params[0]) / params[1]
        _y = norm.cdf(_x)

        return _y

    def hazard_function(self, scale, shape, start_time, end_time, step_time):   # pylint: disable=R0201
        """
        Method to calculate the hazard function for the Exponential
        distribution between start_time and end_time in intervals of step_time.
        This method calculates the point estimate as well as the bounding
        values at each time step.

        :param float scale: the list scale parameters (mu) for the Gaussian
                            distribution to calculate the hazard function for.
        :param float shape: the list shape parameters (sigma) for the Gaussian
                            distribution to calculate the hazard function for.
        :param float start_time: the first time to calculate the hazard
                                 function.
        :param float end_time: the last time to calculate the hazard function.
        :param int step_time: the interval of time between start_time and
                              end_time to calculate the hazard function.
        :return: _hazard; a dict of lists where the key is the time at which
                 the hazard functions was calculated and the value is a list
                 of the lower bound, point estimate, and upper bound.
        :rtype: dict
        """

        _hazard = OrderedDict()

        for _time in range(int(start_time), int(end_time), int(step_time)):
            _values = [0.0, 0.0, 0.0]
            try:
                _values[0] = np.exp(-0.5 * ((_time - scale[0]) /
                                            shape[0])**2.0) / \
                             (shape[0] * np.sqrt(2.0 * np.pi))
            except ZeroDivisionError:
                _values[0] = 0.0
            try:
                _values[1] = np.exp(-0.5 * ((_time - scale[1]) /
                                            shape[1])**2.0) / \
                             (shape[1] * np.sqrt(2.0 * np.pi))
            except ZeroDivisionError:
                _values[1] = 0.0
            try:
                _values[2] = np.exp(-0.5 * ((_time - scale[2]) /
                                            shape[2])**2.0) / \
                             (shape[2] * np.sqrt(2.0 * np.pi))
            except ZeroDivisionError:
                _values[2] = 0.0

            _hazard[_time] = _values

        return _hazard

    def mean(self, scale, start_time, end_time, step_time):     # pylint: disable=R0201
        """
        Method to calculate the means for the Gaussian distribution between
        start_time and end_time in intervals of step_time.  This method
        calculates the point estimate as well as the bounding values at each
        time step.

        :param float scale: the scale parameter (lambda) for the Gaussian
                            distribution to calculate the means for.
        :param float start_time: the first time to calculate the mean.
        :param float end_time: the last time to calculate the mean.
        :param int step_time: the interval of time between start_time and
                              end_time to calculate the mean.
        :return: _mean; a dict of lists where the key is the time at which
                 the means were calculated and the value is a list of the lower
                 bound, point estimate, and upper bound.
        :rtype: dict
        """

        _mean = {}

        for _time in range(int(start_time), int(end_time), int(step_time)):
            _mean[_time] = scale

        return _mean

    def reliability_function(self, scale, shape, start_time, end_time,
                             step_time):    # pylint: disable=R0201
        """
        Method to calculate the reliability function for the Gaussian
        distribution between start_time and end_time in intervals of step_time.
        This method calculates the point estimate as well as the bounding
        values at each time step.

        :param float scale: the scale parameter (mu) for the Gaussian
                            distribution to calculate the reliability function
                            for.
        :param float shape: the list shape parameters (sigma) for the Gaussian
                            distribution to calculate the hazard function for.
        :param float start_time: the first time to calculate the mean.
        :param float end_time: the last time to calculate the mean.
        :param int step_time: the interval of time between start_time and
                              end_time to calculate the mean.
        :return: _reliability; a dict of lists where the key is the time at
                 which the reliability function was calculated and the value is
                 a list of the lower bound, point estimate, and upper bound.
        :rtype: dict
        """

        _reliability = OrderedDict()

        for _time in range(int(start_time), int(end_time), int(step_time)):
            _values = [0.0, 0.0, 0.0]

            _values[0] = 1.0 - norm.cdf((_time - scale[2]) / shape[2])
            _values[1] = 1.0 - norm.cdf((_time - scale[1]) / shape[1])
            _values[2] = 1.0 - norm.cdf((_time - scale[0]) / shape[0])

            _reliability[_time] = _values

        return _reliability


class LogNormal(object):
    """
    Class for the LogNormal distribution.
    """

    def log_pdf(self, data, mu, sigma):     # pylint: disable=C0103, R0201
        """
        Method to calculate the logarithm of the lognormal probability density
        function (pdf).

        :param ndarray data: the data points at which to calculate the
                             logarithm of the pdf.
        :param float mu: the value of the scale parameter.
        :param float sigma: the value of the shape parameter.
        :return: the value(s) of the logarithm of the pdf.
        :rtype: ndarray
        """

        _log_pdf = (1.0 / sigma * np.sqrt(2.0 * np.pi)) - \
                   (0.5 * ((np.log(data) - mu) / sigma)**2.0)

        return _log_pdf

    def log_likelihood(self, pars, data):      # pylint: disable=C0103, R0201
        """
        Method to calculate the value of the log likelihood function for the
        lognormal distribution.

        :param float pars: the parameter values at which to evaluate the
                           log-likelihood.
        :param ndarray data: the data set to calculate the log-likelihood for.
                             * 0 - left of the observation time interval
                             * 1 - right of the observation time interval
                             * 2 - number of events occurring at the
                                   observation time.
                            * 3 - status, where status is:
                                * 1 - event
                                * 2 - right censored
                                * 3 - interval censored
        """

        # Calculate the value of the log-likelihood for the event observations.
        _event_t = data[np.where(data[:, 3] == 1)][:, 1]
        _event_n = data[np.where(data[:, 3] == 1)][:, 2]
        _event_ll = np.sum(_event_n *
                           np.log((1.0 / (_event_t * pars[1])) *
                                  norm.pdf((np.log(_event_t) - pars[0]) /
                                           pars[1])))

        # Calculate the value of the log-likelihood for the right-censored
        # observations.
        _right_t = data[np.where(data[:, 3] == 2)][:, 1]
        _right_n = data[np.where(data[:, 3] == 2)][:, 2]
        _right_ll = np.sum(_right_n *
                           (1.0 - norm.cdf((np.log(_right_t) - pars[0]) /
                                           pars[1])))

        # Calculate the value of the log-likelihood for the left- and interval-
        # censored observations.
        _interval_lt = data[np.where(np.logical_or(data[:, 3] == 3,
                                                   data[:, 3] == 4))][:, 0]
        _interval_rt = data[np.where(np.logical_or(data[:, 3] == 3,
                                                   data[:, 3] == 4))][:, 1]
        _interval_n = data[np.where(np.logical_or(data[:, 3] == 3,
                                                  data[:, 3] == 4))][:, 2]

        _interval_ll = np.sum(_interval_n *
                              np.log(norm.cdf(
                                  (np.log(_interval_rt) - pars[0]) / pars[1]) -
                                     norm.cdf(
                                         (np.log(_interval_lt) - pars[0]) /
                                         pars[1])))

        _logLik = _event_ll - _right_ll + _interval_ll

        return _logLik

    def log_likelihood_ratio(self, pars, data, const=0.0):
        """
        Method to minimize when finding likelihood ratio confidence bounds.

        The equation this method calculates is:

            log[L(mu, sigma)] - chi2(alpha, 1) / 2.0

        where the keyword const is the chi2(alpha, 1) / 2.0 part.

        :param float pars: the parameter values at which to evaluate the
                           log-likelihood.
        :param ndarray data: the data set to calculate the log-likelihood for.
                             * 0 - left of the observation time interval
                             * 1 - right of the observation time interval
                             * 2 - number of events occurring at the
                                   observation time
                             * 3 - status, where status is:
                                * 1 - event
                                * 2 - right censored
                                * 3 - left censored
                                * 4 - interval censored
        :keyword float const: constant value to subtract from the
                              log-likelihood.  It is chi2(alpha, 1) / 2.0
        :return: _log_lik_ratio
        :rtype: float
        """

        _log_lik_ratio = self.log_likelihood(pars, data) - const

        return _log_lik_ratio

    def likelihood_bounds(self, pars, confidence, data):
        """
        Method to calculate the likelihood ratio confidence bounds for the
        parameters.

        Likelihood confidence bounds are calculated by finding values for mu,
        while holding sigma constant, that satisfy:

            L(mu, sigma) = L(mu_hat, sig_hat) * exp(-chi2(alpha, 1) / 2.0)

        Taking logarithms (base e) of the equation above results in:

            log[L(mu, sigma)] = log[L(mu_hat, sig_hat)] - chi2(alpha, 1) / 2.0

        The same values of theta will minimize both, but logarithms are easier
        to work with.

        :param list of float pars: the parameter values at which to evaluate
                                   the log-likelihood.
        :param float confidence: the confidence level at which to calculate the
                                 bounds.
        :param ndarray data: the data set to calculate the log-likelihood for.
                             * 0 - left of the observation time interval
                             * 1 - right of the observation time interval
                             * 2 - number of events occurring at the
                                   observation time
                             * 3 - status, where status is:
                                * 1 - event
                                * 2 - right censored
                                * 3 - left censored
                                * 4 - interval censored
        :return: (_lower, _upper)
        :rtype: tuple
        """

        def _shadow_func(pars, data, const):
            """
            Shadow function used to minimize the log-likelihood ratio.  It's a
            hack to ensure the correct number of arguments are returned.
            """

            return [self.log_likelihood_ratio(pars, data, const), 0.0]

        _lower = OrderedDict()
        _upper = OrderedDict()

        _log_lik_ratio = self.log_likelihood_ratio(pars, data)
        _const = _log_lik_ratio - (chi2.ppf(confidence, 1) / 2.0)

        _step = confidence / 50.0
        for _index in range(100):
            # Set the sigma step value for this iteration.
            _sigma = pars[1] * (confidence + (_index * _step))

            # To find the lower bound, we provide root with a starting value
            # for mu less than the point estimate; in this case 1/10 the value.
            _lower[_sigma] = optimize.root(_shadow_func,
                                           [pars[0] / 10.0, _sigma],
                                           args=(data, _const)).x[0]

            # To find the upper bound, we provide root with a starting value
            # for mu greater than the point estimate; in this case double.
            _upper[_sigma] = optimize.root(_shadow_func,
                                           [2.0 * pars[0], _sigma],
                                           args=(data, _const)).x[0]

        return(_lower, _upper)

    def partial_derivatives(self, pars, data):         # pylint: disable=C0103, R0201, R0914
        """
        Method to calculate the value of the partial derivatives of the
        lognormal log-likelihood function with respect to mu and sigma.  This
        function is passed as an argument to scipy.optimize.fsolve() to find
        the values of mu and sigma that simultaneously minimizes the partials.

        :param list pars: the values of mu and sigma at which to calculate the
                          partials.
        :param ndarray data: the data set to calculate the log-likelihood for.
                             * 0 - left of the observation time interval
                             * 1 - right of the observation time interval
                             * 2 - number of events occurring at the
                                   observation time
                             * 3 - status, where status is:
                                * 1 - event
                                * 2 - right censored
                                * 3 - left censored
                                * 4 - interval censored
        """

        # Calculate the value of the log-likelihood for the event observations.
        _event_t = data[np.where(data[:, 3] == 1)][:, 1]
        _event_n = data[np.where(data[:, 3] == 1)][:, 2]
        _event_sigma = np.sum(_event_n *
                              (((np.log(_event_t) - pars[0]) / pars[1]**3.0) -
                               (1.0 / pars[1])))
        _event_mu = (1.0 / pars[1]**2.0) * np.sum(_event_n *
                                                  (np.log(_event_t) - pars[0]))

        # Calculate the value of the log-likelihood for the right-censored
        # observations.
        _right_t = data[np.where(data[:, 3] == 2)][:, 1]
        _right_n = data[np.where(data[:, 3] == 2)][:, 2]

        _norm = (np.log(_right_t) - pars[0]) / pars[1]
        _cdf = norm.cdf(_norm)
        _right_mu = (1.0 / pars[1]) * \
            np.sum(_right_n * (norm.pdf(_norm) / (1.000000001 - _cdf)))
        _right_sigma = (1.0 / pars[1]) * \
            np.sum(_right_n *
                   ((_norm * norm.pdf(_norm)) / (1.000000001 - _cdf)))

        # Calculate the value of the log-likelihood for the left- and interval-
        # censored observations.  Use the midpoint of the interval as an
        # approximation.
        _interval_lt = data[np.where(np.logical_or(data[:, 3] == 3,
                                                   data[:, 3] == 4))][:, 0]
        _interval_rt = data[np.where(np.logical_or(data[:, 3] == 3,
                                                   data[:, 3] == 4))][:, 1]
        _interval_n = data[np.where(np.logical_or(data[:, 3] == 3,
                                                  data[:, 3] == 4))][:, 2]

        # Following are the exact equations for the interval censored
        # observations.
        _norm_r = (np.log(_interval_rt) - pars[0]) / pars[1]
        _pdf_r = norm.pdf(_norm_r)
        _cdf_r = norm.cdf(_norm_r)

        _norm_l = (np.log(_interval_lt) - pars[0]) / pars[1]
        _pdf_l = norm.pdf(_norm_l)
        _cdf_l = norm.cdf(_norm_l)

        _n = _pdf_r - _pdf_l
        _d = _cdf_r - _cdf_l
        _interval_mu = np.sum(_interval_n * _n / _d * pars[1])

        _n = (_norm_r * _pdf_r) - (_norm_l * _pdf_l)
        _interval_sigma = (1.0 / pars[1]) * np.sum(_interval_n * _n / _d)

        _del_mu = _event_mu + _right_mu - _interval_mu
        _del_sigma = _event_sigma + _right_sigma - _interval_sigma

        return _del_mu * _del_sigma

    def maximum_likelihood_estimate(self, data, start, end):    # pylint: disable=R0914
        """
        Method to fit data to a parametric distribution and find point
        estimates of the parameters.  It is up to the calling function to
        calculate bounding values.

        :param ndarray data: the data set to fit.  This is a numpy array where
                             each record contains the following, in order:
                                * 0 = Interval start time
                                * 1 = Interval end time
                                * 2 = Quantity of observations
                                * 3 = Status of observation
                                * 4 = Time between failures or interarrival
                                      time
        :param float start: the minimum time to include in the fit.  Used to
                            exclude outliers.
        :param float end: the maximum time to include in the fit.  Used to
                          exclude outliers.
        :return: _fit; [[scale estimate, shape estimate, location estimate],
                        [scale variance, covariance, shape variance],
                        [MLE, AIC, BIC], correlation coeff.]
        :rtype: list
        """

        def _shadow_func(pars, data):
            """
            Shadow function used to ensure the correct number of values are
            returned when finding roots.
            """

            return [self.partial_derivatives(pars, data), 0.0]

        # Initialize lists to hold results.
        _parameters = [0.0, 0.0]            # Scale and shape parameters.
        _variance = [0.0, 0.0, 0.0]         # Scale variance, covariance,
                                            # shape variance.
        _gof = [0.0, 0.0, 0.0]              # MLE, AIC, BIC

        # Sort data by the right of the interval.  Remove records occurring
        # before the start time and after the end time.
        _data = sorted(data, key=lambda x: float(x[1]))
        _data = [_rec for _rec in _data if float(_rec[0]) >= start]
        _data = [_rec for _rec in _data if float(_rec[1]) <= end]
        _data = np.array(_data)

        # Count the number of suspensions, failures, and records.
        _n_suspensions = sum(x[2] for x in _data if x[3] == 2)
        _n_failures = sum(x[2] for x in _data
                          if x[3] == 1 or x[3] == 3 or x[3] == 4)
        _n_records = len(_data)

        # Adjust the right-censored times to be the mid-point between the
        # censored time and the maximum observed time in the data set.
        _adj_right = (max(_data[:, 1]) +
                      _data[np.where(_data[:, 3] == 2), 1]) / 2.0
        _data[np.where(_data[:, 3] == 2), 1] = _adj_right

        # Adjust the interval-censored times so they can be passed to the
        # fit method.
        _interval_lt = _data[np.where(_data[:, 3] == 4)][:, 0]
        _interval_rt = _data[np.where(_data[:, 3] == 4)][:, 1]
        _interval_t = (_interval_lt + _interval_rt) / 2.0
        _data[np.where(_data[:, 3] == 4), 1] = _interval_t

        # Provide an estimate of mu and sigma assuming no suspensions and
        # using the right of the interval.  Use these as the starting
        # values to scipy.optimize.fsolve.
        (_sigma, __,
         _mu) = lognorm.fit(np.array(_data[:, 1], dtype=float), floc=0)
        _params = optimize.fsolve(_shadow_func, [np.log(_mu), _sigma],
                                  args=(_data))

        _parameters[0] = _params[0]
        _parameters[1] = _params[1]

        _fI = fisher_information(self.log_pdf, _parameters, _data[:, 3])
        _variance[0] = 1.0 / np.diag(_fI)[0]
        _variance[1] = 1.0 / _fI[0][1]
        _variance[2] = 1.0 / np.diag(_fI)[1]

        # Calculate the MLE, AIC, and BIC.
        _gof[0] = self.log_likelihood([_parameters[0], _parameters[1]], _data)
        _gof[1] = -2.0 * _gof[0] + 4.0
        _gof[2] = -2.0 * _gof[0] + 4.0 * np.log(_n_records)

        _fit = [_parameters, _variance, _gof, _n_suspensions, _n_failures]

        return _fit

    def theoretical_distribution(self, data, params):   # pylint: disable=R0201
        """
        Method to create a data set from the theoretical distribution given the
        parameters.

        :param ndarray data: the data set that the theoretical distribution
                             will be created for.  This is a zero-based list of
                             lists or list of tuples where index 1 is the left
                             of the interval and index 2 is the right of the
                             interval.  The other indices are not used.
        :param list params: list with the values of the distribution
                            parameters.
        :return: _y; the probabilities of the theoretical distribution with
                 parameters params.
        :rtype: ndarray
        """

        _x = np.sort(np.array(data, dtype=float))

        _x = (np.log(_x + 0.01) - params[0]) / params[1]
        _y = norm.cdf(_x)

        return _y

    def hazard_function(self, scale, shape, start_time, end_time, step_time):   # pylint: disable=R0201
        """
        Method to calculate the hazard function for the LogNormal
        distribution between start_time and end_time in intervals of step_time.
        This method calculates the point estimate as well as the bounding
        values at each time step.

        :param float scale: the list scale parameters (mu) for the LogNormal
                            distribution to calculate the hazard function for.
        :param float shape: the list shape parameters (sigma) for the LogNormal
                            distribution to calculate the hazard function for.
        :param float start_time: the first time to calculate the hazard
                                 function.
        :param float end_time: the last time to calculate the hazard function.
        :param int step_time: the interval of time between start_time and
                              end_time to calculate the hazard function.
        :return: _hazard; a dict of lists where the key is the time at which
                 the hazard functions was calculated and the value is a list
                 of the lower bound, point estimate, and upper bound.
        :rtype: dict
        """

        _hazard = OrderedDict()

        for _time in range(int(start_time), int(end_time), int(step_time)):
            _values = [0.0, 0.0, 0.0]
            try:
                _values[0] = np.exp(-0.5 * (np.log(_time) - scale[0] /
                                            shape[0])**2.0) / \
                             (_time * shape[0] * np.sqrt(2.0 * np.pi))
            except ZeroDivisionError:
                _values[0] = 0.0
            try:
                _values[1] = np.exp(-0.5 * (np.log(_time) - scale[1] /
                                            shape[1])**2.0) / \
                             (_time * shape[1] * np.sqrt(2.0 * np.pi))
            except ZeroDivisionError:
                _values[1] = 0.0
            try:
                _values[2] = np.exp(-0.5 * (np.log(_time) - scale[2] /
                                            shape[2])**2.0) / \
                             (_time * shape[2] * np.sqrt(2.0 * np.pi))
            except ZeroDivisionError:
                _values[2] = 0.0

            _hazard[_time] = _values

        return _hazard

    def mean(self, scale, shape, start_time, end_time, step_time):  # pylint: disable=R0201
        """
        Method to calculate the means for the LogNormal distribution between
        start_time and end_time in intervals of step_time.  This method
        calculates the point estimate as well as the bounding values at each
        time step.

        :param float scale: the scale parameter (mu) for the LogNormal
                            distribution to calculate the means for.
        :param float shape: the list shape parameters (sigma) for the LogNormal
                            distribution to calculate the hazard function for.
        :param float start_time: the first time to calculate the mean.
        :param float end_time: the last time to calculate the mean.
        :param int step_time: the interval of time between start_time and
                              end_time to calculate the mean.
        :return: _mean; a dict of lists where the key is the time at which
                 the means were calculated and the value is a list of the lower
                 bound, point estimate, and upper bound.
        :rtype: dict
        """

        _mean = {}

        for _time in range(int(start_time), int(end_time), int(step_time)):
            _values = [0.0, 0.0, 0.0]

            _values[0] = np.exp(scale[0] + 0.5 * shape[0]**2.0)
            _values[1] = np.exp(scale[1] + 0.5 * shape[1]**2.0)
            _values[2] = np.exp(scale[2] + 0.5 * shape[2]**2.0)

            _mean[_time] = _values

        return _mean

    def reliability_function(self, scale, shape, start_time, end_time,
                             step_time):    # pylint: disable=R0201
        """
        Method to calculate the reliability function for the LogNormal
        distribution between start_time and end_time in intervals of step_time.
        This method calculates the point estimate as well as the bounding
        values at each time step.

        :param float scale: the scale parameter (mu) for the LogNormal
                            distribution to calculate the reliability function
                            for.
        :param float shape: the list shape parameters (sigma) for the LogNormal
                            distribution to calculate the hazard function for.
        :param float start_time: the first time to calculate the mean.
        :param float end_time: the last time to calculate the mean.
        :param int step_time: the interval of time between start_time and
                              end_time to calculate the mean.
        :return: _reliability; a dict of lists where the key is the time at
                 which the reliability function was calculated and the value is
                 a list of the lower bound, point estimate, and upper bound.
        :rtype: dict
        """

        _reliability = OrderedDict()

        for _time in range(int(start_time), int(end_time), int(step_time)):
            _values = [0.0, 0.0, 0.0]

            _values[0] = 1.0 - norm.cdf((np.log(_time) - scale[2]) / shape[2])
            _values[1] = 1.0 - norm.cdf((np.log(_time) - scale[1]) / shape[1])
            _values[2] = 1.0 - norm.cdf((np.log(_time) - scale[0]) / shape[0])

            _reliability[_time] = _values

        return _reliability


class Weibull(object):
    """
    Class for the Weibull distribution.
    """

    def log_pdf(self, data, eta, beta):     # pylint: disable=C0103, R0201
        """
        Method to calculate the logarithm of the weibull probability density
        function (pdf).

        :param ndarray data: the data points at which to calculate the
                             logarithm of the pdf.
        :param float eta: the value of the scale parameter.
        :param float beta: the value of the shape parameter.
        :return: the value(s) of the logarithm of the pdf.
        :rtype: ndarray
        """

        _log_pdf = np.log(beta / eta) + \
            (beta - 1.0) * np.log(data / eta) - (data / eta)**beta

        return _log_pdf

    def log_likelihood(self, pars, data):   # pylint: disable=C0103, R0201
        """
        Method to calculate the value of the log likelihood function for the
        weibull distribution.

        :param float pars: the parameter [eta, beta] values at which to
                           evaluate the log-likelihood.
        :param ndarray data: the data set to calculate the log-likelihood for.
                             * 0 - left of the observation time interval
                             * 1 - right of the observation time interval
                             * 2 - number of events occurring at the
                                   observation time.
                            * 3 - status, where status is:
                                * 1 - event
                                * 2 - right censored
                                * 3 - interval censored
        """

        # Calculate the value of the log-likelihood for the event observations.
        _event_t = data[np.where(data[:, 3] == 1)][:, 1]
        _event_n = data[np.where(data[:, 3] == 1)][:, 2]
        _event_ll = np.sum(_event_n *
                           np.log((pars[1] / pars[0]) *
                                  ((_event_t / pars[0])**(pars[1] - 1.0)) *
                                  np.exp(-(_event_t / pars[0])**pars[1])))

        # Calculate the value of the log-likelihood for the right-censored
        # observations.
        _right_t = data[np.where(data[:, 3] == 2)][:, 1]
        _right_n = data[np.where(data[:, 3] == 2)][:, 2]
        _right_ll = np.sum(_right_n * (_right_t / pars[0])**pars[1])

        # Calculate the value of the log-likelihood for the left- and interval-
        # censored observations.
        _interval_lt = data[np.where(np.logical_or(data[:, 3] == 3,
                                                   data[:, 3] == 4))][:, 0]
        _interval_rt = data[np.where(np.logical_or(data[:, 3] == 3,
                                                   data[:, 3] == 4))][:, 1]
        _interval_n = data[np.where(np.logical_or(data[:, 3] == 3,
                                                  data[:, 3] == 4))][:, 2]

        _interval_ll = np.sum(_interval_n *
                              np.log(np.exp(-(_interval_lt /
                                              pars[0])**pars[1]) -
                                     np.exp(-(_interval_rt /
                                              pars[0])**pars[1])))

        _logLik = _event_ll - _right_ll + _interval_ll

        return _logLik

    def log_likelihood_ratio(self, pars, data, const=0.0):
        """
        Method to minimize when finding likelihood ratio confidence bounds.

        The equation this method calculates is:

            log[L(eta, beta)] - chi2(alpha, 1) / 2.0

        where the keyword const is the chi2(alpha, 1) / 2.0 part.

        :param float pars: the parameter values at which to evaluate the
                           log-likelihood.
        :param ndarray data: the data set to calculate the log-likelihood for.
                             * 0 - left of the observation time interval
                             * 1 - right of the observation time interval
                             * 2 - number of events occurring at the
                                   observation time
                             * 3 - status, where status is:
                                * 1 - event
                                * 2 - right censored
                                * 3 - left censored
                                * 4 - interval censored
        :keyword float const: constant value to subtract from the
                              log-likelihood.  It is chi2(alpha, 1) / 2.0
        :return: _log_lik_ratio
        :rtype: float
        """

        _log_lik_ratio = self.log_likelihood(pars, data) - const

        return _log_lik_ratio

    def likelihood_bounds(self, pars, confidence, data):
        """
        Method to calculate the likelihood ratio confidence bounds for the
        parameters.

        Likelihood confidence bounds are calculated by finding values for eta,
        while holding beta constant, that satisfy:

            L(eta, beta) = L(eta_hat, beta_hat) * exp(-chi2(alpha, 1) / 2.0)

        Taking logarithms (base e) of the equation above results in:

            log[L(eta, beta)] = log[L(eta_hat, beta_hat)] - chi2(alpha, 1) / 2.0

        The same values of theta will minimize both, but logarithms are easier
        to work with.

        :param list of float pars: the parameter values at which to evaluate
                                   the log-likelihood.
        :param float confidence: the confidence level at which to calculate the
                                 bounds.
        :param ndarray data: the data set to calculate the log-likelihood for.
                             * 0 - left of the observation time interval
                             * 1 - right of the observation time interval
                             * 2 - number of events occurring at the
                                   observation time
                             * 3 - status, where status is:
                                * 1 - event
                                * 2 - right censored
                                * 3 - left censored
                                * 4 - interval censored
        :return: (_lower, _upper)
        :rtype: tuple
        """

        def _shadow_func(pars, data, const):
            """
            Shadow function used to minimize the log-likelihood ratio.  It's a
            hack to ensure the correct number of arguments are returned.
            """

            return [self.log_likelihood_ratio(pars, data, const), 0.0]

        def _beta_eta_func(x_var, m1, m2, intercept):
            """
            Function describing the relationship between mu and sigma.  This
            relationship parabolic for both upper and lower limits.
            """

            return m1 * x_var**2.0 + m2 * x_var + intercept

        def _beta_limits(lower, upper):
            """
            Function to find the two sigma values at which mu is the same.
            Used to find the limits on sigma over which the parabolic
            relationship exists.
            """

            for _keyl in lower.keys():
                for _keyu in upper.keys():
                    if(abs(upper[_keyu] - lower[_keyl]) < 1.0E-6 and
                       _keyl < _keyu):
                        return(_keyl, _keyu)

        _lower = OrderedDict()
        _upper = OrderedDict()

        _log_lik_ratio = self.log_likelihood_ratio(pars, data)
        _const = _log_lik_ratio - (chi2.ppf(confidence, 1) / 2.0)

        _betal = 0.5 * pars[1]
        _betau = 2.0 * pars[1]
        for _index in range(200):
            # Find the lower bound.
            _temp = optimize.root(_shadow_func, [pars[0], _betal],
                                  args=(data, _const)).x
            _lower[_betal] = _temp[0]
            _betal = _temp[1]

            # Find the upper bound.
            _temp = optimize.root(_shadow_func, [pars[0], _betau],
                                  args=(data, _const)).x
            _upper[_betau] = _temp[0]
            _betau = _temp[1]

        _beta_l = max(_lower.keys())
        _beta_u = min(_upper.keys())
        _eta_l = optimize.fsolve(_shadow_func, [pars[0] / 10.0, _beta_l],
                                 args=(data, 0.0))[0]
        _eta_u = _upper[_beta_u]

        return(_eta_l, _eta_u, _beta_l, _beta_u)

    def partial_derivatives(self, x, data):     # pylint: disable=C0103, R0201, R0914
        """
        Method to calculate the value of the partial derivatives of the
        weibull log-likelihood function with respect to mu and sigma.  This
        function is passed as an argument to scipy.optimize.fsolve() to find
        the values of mu and sigma that simultaneously minimizes the partials.

        :param list x: the values of eta and beta at which to calculate the
                       partials.
        :param ndarray data: the data set to calculate the log-likelihood for.
                             * 0 - left of the observation time interval
                             * 1 - right of the observation time interval
                             * 2 - number of events occurring at the
                                   observation time
                             * 3 - status, where status is:
                                * 1 - event
                                * 2 - right censored
                                * 3 - left censored
                                * 4 - interval censored
        """

        # Calculate the value of the log-likelihood for the event observations.
        _event_t = data[np.where(data[:, 3] == 1)][:, 1]
        _event_n = data[np.where(data[:, 3] == 1)][:, 2]
        _event_ll_beta = np.sum(_event_n) / x[1] + \
            np.sum(_event_n * np.log(_event_t / x[0])) - \
            np.sum(_event_n * (_event_t / x[0])**x[1] *
                   np.log(_event_t / x[0]))
        _event_ll_eta = (-x[1] / x[0]) * np.sum(_event_n) + \
                        (x[1] / x[0]) * np.sum(_event_n *
                                               (_event_t / x[0])**x[1])

        # Calculate the value of the log-likelihood for the right-censored
        # observations.
        _right_t = data[np.where(data[:, 3] == 2)][:, 1]
        _right_n = data[np.where(data[:, 3] == 2)][:, 2]
        _right_ll_beta = np.sum(_right_n * (_right_t / x[0])**x[1] *
                                np.log(_right_t / x[0]))
        _right_ll_eta = (x[1] / x[0]) * \
                        np.sum(_right_n * (_right_t / x[0])**x[1])

        # Calculate the value of the log-likelihood for the left- and interval-
        # censored observations.  Use the midpoint of the interval as an
        # approximation.
        _interval_lt = data[np.where(np.logical_or(data[:, 3] == 3,
                                                   data[:, 3] == 4))][:, 0]
        _interval_rt = data[np.where(np.logical_or(data[:, 3] == 3,
                                                   data[:, 3] == 4))][:, 1]
        _interval_n = data[np.where(np.logical_or(data[:, 3] == 3,
                                                  data[:, 3] == 4))][:, 2]

        # Following are the exact equations for the interval censored
        # observations.
        _nr = _interval_rt / x[0]
        _nr_b = (_nr + 0.000001)**x[1]
        _nr_exp = np.exp(-(_nr_b))

        _nl = _interval_lt / x[0]
        _nl_b = (_nl + 0.000001)**x[1]
        _nl_exp = np.exp(-(_nl_b))

        _n = (-_nl_b * np.log(_nl_b) * _nl_exp) + \
             (_nr_b * np.log(_nr_b) * _nr_exp)
        _d = _nl_exp - _nr_exp
        _interval_ll_beta = np.sum(_interval_n * _n / _d)

        _n = ((x[1] / x[0]) * _nl_b * _nl_exp) - \
             ((x[1] / x[0]) * _nr_b * _nr_exp)
        _interval_ll_eta = np.sum(_interval_n * _n / _d)

        _del_beta = _event_ll_beta - _right_ll_beta + _interval_ll_beta
        _del_eta = _event_ll_eta + _right_ll_eta + _interval_ll_eta

        return _del_eta * _del_beta

    def maximum_likelihood_estimate(self, data, start, end):
        """
        Method to fit data to a parametric distribution and find point
        estimates of the parameters.  It is up to the calling function to
        calculate bounding values.

        :param ndarray data: the data set to fit.  This is a numpy array where
                             each record contains the following, in order:
                                * 0 = Interval start time
                                * 1 = Interval end time
                                * 2 = Quantity of observations
                                * 3 = Status of observation
                                * 4 = Time between failures or interarrival
                                      time
        :param float start: the minimum time to include in the fit.  Used to
                            exclude outliers.
        :param float end: the maximum time to include in the fit.  Used to
                          exclude outliers.
        :return: _fit; [[scale estimate, shape estimate, location estimate],
                        [scale variance, covariance, shape variance],
                        [MLE, AIC, BIC], correlation coeff.]
        :rtype: list
        """

        def _shadow_func(pars, data):
            """
            Shadow function used to ensure the correct number of values are
            returned when finding roots.
            """

            return [self.partial_derivatives(pars, data), 0.0]

        # Initialize lists to hold results.
        _parameters = [0.0, 0.0, 0.0]       # Scale, shape, and location
                                            # parameters.
        _variance = [0.0, 0.0, 0.0]         # Scale variance, covariance,
                                            # location variance.
        _gof = [0.0, 0.0, 0.0]              # MLE, AIC, BIC

        # Sort data by the right of the interval.  Remove records occurring
        # before the start time and after the end time.
        _data = sorted(data, key=lambda x: float(x[1]))
        _data = [_rec for _rec in _data if float(_rec[0]) >= start]
        _data = [_rec for _rec in _data if float(_rec[1]) <= end]
        _data = np.array(_data)

        # Count the number of suspensions, failures, and records.
        _n_suspensions = sum(x[2] for x in _data if x[3] == 2)
        _n_failures = sum(x[2] for x in _data
                          if x[3] == 1 or x[3] == 3 or x[3] == 4)
        _n_records = len(_data)

        # Adjust the right-censored times to be the mid-point between the
        # censored time and the maximum oberserved time in the data set.
        _adj_right = (max(_data[:, 1]) +
                      _data[np.where(_data[:, 3] == 2), 1]) / 2.0
        _data[np.where(_data[:, 3] == 2), 1] = _adj_right

        # Adjust the interval-censored times so they can be passed to the
        # fit method.
        _interval_lt = _data[np.where(_data[:, 3] == 3)][:, 0]
        _interval_rt = _data[np.where(_data[:, 3] == 3)][:, 1]
        _interval_t = (_interval_lt + _interval_rt) / 2.0
        _data[np.where(_data[:, 3] == 3), 1] = _interval_t

        # Provide an estimate of eta and beta assuming no suspensions and
        # using the right of the interval.  Use these as the starting
        # values to scipy.optimize.fsolve.
        (__, _beta,
         __, _eta) = exponweib.fit(np.array(_data[:, 4], dtype=float),
                                   f0=1, floc=0)
        _params = optimize.fsolve(_shadow_func, [_eta, _beta], args=(data))

        _parameters[0] = _params[0]
        _parameters[1] = _params[1]

        _fI = fisher_information(self.log_pdf, _parameters, _data[:, 3])
        _variance[0] = 1.0 / np.diag(_fI)[0]
        _variance[1] = 1.0 / np.diag(_fI)[1]
        _variance[2] = 1.0 / _fI[0, 1]

        # Calculate the MLE, AIC, and BIC.
        _gof[0] = self.log_likelihood([_parameters[0], _parameters[1]], _data)
        _gof[1] = -2.0 * _gof[0] + 4.0
        _gof[2] = -2.0 * _gof[0] + 4.0 * np.log(_n_records)

        _fit = [_parameters, _variance, _gof, _n_suspensions, _n_failures]

        return _fit

    def theoretical_distribution(self, data, params):   # pylint: disable=R0201
        """
        Method to create a data set from the theoretical distribution given the
        parameters.

        :param ndarray data: the data set that the theoretical distribution
                             will be created for.  This is a zero-based list of
                             lists or list of tuples where index 1 is the left
                             of the interval and index 2 is the right of the
                             interval.  The other indices are not used.
        :param list params: list with the values of the distribution
                            parameters.
        :return: _y; the probabilities of the theoretical distribution with
                 parameters params.
        :rtype: ndarray
        """

        _x = np.sort(np.array(data, dtype=float))

        _y = 1.0 - np.exp(-(_x / params[0])**params[1])

        return _y

    def hazard_function(self, scale, shape, start_time, end_time, step_time):   # pylint: disable=R0201
        """
        Method to calculate the hazard function for the Weibull distribution
        between start_time and end_time in intervals of step_time.  This method
        calculates the point estimate as well as the bounding values at each
        time step.

        :param float scale: the list scale parameters (eta) for the Weibull
                            distribution to calculate the hazard function for.
        :param float shape: the list shape parameters (beta) for the Weibull
                            distribution to calculate the hazard function for.
        :param float start_time: the first time to calculate the hazard
                                 function.
        :param float end_time: the last time to calculate the hazard function.
        :param int step_time: the interval of time between start_time and
                              end_time to calculate the hazard function.
        :return: _hazard; a dict of lists where the key is the time at which
                 the hazard functions was calculated and the value is a list
                 of the lower bound, point estimate, and upper bound.
        :rtype: dict
        """

        _hazard = OrderedDict()

        for _time in range(int(start_time), int(end_time), int(step_time)):
            _values = [0.0, 0.0, 0.0]
            try:
                _values[0] = (shape[0] / scale[0]) * \
                             (_time / scale[0])**(shape[0] - 1.0)
            except ZeroDivisionError:
                _values[0] = 0.0
            try:
                _values[1] = (shape[1] / scale[1]) * \
                             (_time / scale[1])**(shape[1] - 1.0)
            except ZeroDivisionError:
                _values[1] = 0.0
            try:
                _values[2] = (shape[2] / scale[2]) * \
                             (_time / scale[2])**(shape[2] - 1.0)
            except ZeroDivisionError:
                _values[2] = 0.0

            _hazard[_time] = _values

        return _hazard

    def mean(self, scale, shape, start_time, end_time, step_time):  # pylint: disable=R0201
        """
        Method to calculate the means for the Weibull distribution between
        start_time and end_time in intervals of step_time.  This method
        calculates the point estimate as well as the bounding values at each
        time step.

        :param float scale: the scale parameter (eta) for the Weibull
                            distribution to calculate the means for.
        :param float shape: the list shape parameters (beta) for the Weibull
                            distribution to calculate the hazard function for.
        :param float start_time: the first time to calculate the mean.
        :param float end_time: the last time to calculate the mean.
        :param int step_time: the interval of time between start_time and
                              end_time to calculate the mean.
        :return: _mean; a dict of lists where the key is the time at which
                 the means were calculated and the value is a list of the lower
                 bound, point estimate, and upper bound.
        :rtype: dict
        """

        _mean = {}

        for _time in range(int(start_time), int(end_time), int(step_time)):
            _values = [0.0, 0.0, 0.0]
            try:
                _values[0] = scale[0] * gamma((1.0 / shape[0]) + 1)
            except ZeroDivisionError:
                _values[0] = 0.0
            try:
                _values[1] = scale[1] * gamma((1.0 / shape[1]) + 1)
            except ZeroDivisionError:
                _values[1] = 0.0
            try:
                _values[2] = scale[2] * gamma((1.0 / shape[2]) + 1)
            except ZeroDivisionError:
                _values[2] = 0.0

            _mean[_time] = _values

        return _mean

    def reliability_function(self, scale, shape, start_time, end_time,
                             step_time):    # pylint: disable=R0201
        """
        Method to calculate the reliability function for the Weibull
        distribution between start_time and end_time in intervals of step_time.
        This method calculates the point estimate as well as the bounding
        values at each time step.

        :param float scale: the scale parameter (eta) for the Weibull
                            distribution to calculate the reliability function
                            for.
        :param float shape: the list shape parameters (beta) for the Weibull
                            distribution to calculate the hazard function for.
        :param float start_time: the first time to calculate the mean.
        :param float end_time: the last time to calculate the mean.
        :param int step_time: the interval of time between start_time and
                              end_time to calculate the mean.
        :return: _reliability; a dict of lists where the key is the time at
                 which the reliability function was calculated and the value is
                 a list of the lower bound, point estimate, and upper bound.
        :rtype: dict
        """

        _reliability = OrderedDict()

        for _time in range(int(start_time), int(end_time), int(step_time)):
            _values = [0.0, 0.0, 0.0]

            _values[0] = np.exp(-(_time / scale[2])**shape[2])
            _values[1] = np.exp(-(_time / scale[1])**shape[1])
            _values[2] = np.exp(-(_time / scale[0])**shape[0])

            _reliability[_time] = _values

        return _reliability
