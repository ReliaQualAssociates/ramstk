#!/usr/bin/env python
"""
Contains functions for performing maximum likelihood estimation analysis.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.analyses.statistics.MLE.py is part of The RTK Project
#
# All rights reserved.

import inspect

# Import mathematical functions.
import numpy as np
import scipy.misc as misc
#import scipy.optimize as optim
from scipy.stats import expon, exponweib, lognorm, norm     # pylint: disable=E0611


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

    :param list previous: the previous data set record.
    :param list current: the current data set record.
                         0 = record ID
                         1 = unit
                         2 = left interval
                         3 = right interval
                         4 = quantity
                         5 = status
    :return: _tbf; the time between previous and current failures.
    :rtype: float
    """

    if current[5] == 'Event' or str(current[5]) == '1':
        if current[1] == previous[1]:
            _tbf = current[3] - previous[3]
        else:
            _tbf = current[3]
    elif current[5] == 'Right Censored' or str(current[5]) == '2':
        _tbf = np.inf
    elif(current[5] == 'Left Censored' or current[5] == 'Interval Censored' or
         str(current[5]) == '3'):
        _time1 = (previous[3] - previous[2]) / 2.0 + previous[2]
        _time2 = (current[3] - current[2]) / 2.0 + current[2]
        if current[1] == previous[1]:
            _tbf = _time2 - _time1
        else:
            _tbf = _time2
    else:
        _tbf = current[3] - previous[3]

    return _tbf


def format_data_set(data, start, end):
    """
    Function to format the data set and turn it into a numpy array for use in
    the maximum likelihood estimator functions for each distribution.

    :param list data: the data set to format.
    :param float start: the minimum time to include in the fit.  Used to
                        exclude outliers.
    :param float end: the maximum time to include in the fit.  Used to
                      exclude outliers.
    :return: (_data, _n_records); tuple of the formatted data set and the total
             number of records in the data set.
    :rtype: tuple
    """

    # Sort data by the right of the interval.  Remove records occurring before
    # the start time and after the end time.
    _data = sorted(data, key=lambda x: float(x[2]))
    _data = [_rec for _rec in _data if float(_rec[1]) >= start]
    if end > 0.0:
        _data = [_rec for _rec in _data if float(_rec[2]) <= end]

    # Expand the data set so there is one record for each failure.  Loop
    # through the failure quantity passed for each record.
    _data2 = []
    for i in range(len(_data)):
        for j in range(int(_data[i][5])):
            _data2.append((_data[i][0], _data[i][1], _data[i][2], _data[i][3],
                           _data[i][4], 1))
    _data = np.array(_data2)

    # Replace the string status with integer status.
    for _record in _data:
        if _record[4] == 'Right Censored' or str(_record[4]) == '2':
            _record[2] = np.inf
            _record[4] = 2
        elif(_record[4] == 'Left Censored' or
             _record[4] == 'Interval Censored' or str(_record[4]) == '3'):
            _record[4] = 3
        else:
            _record[4] = 1

    # Coerce the data set into the form necessary for fitting to functions.
    _data = np.vstack((_data[:, 1], _data[:, 2], _data[:, 5], _data[:, 4],
                       _data[:, 3]))
    _data = np.array(np.transpose(_data), dtype=float)
    _n_records = len(_data)

    return (_data, _n_records)


class Exponential(object):
    """
    Class for the Exponential distribution.
    """

    def log_pdf(self, data, theta, gamma=0.0):  # pylint: disable=C0103, R0201
        """
        Method to calculate the logarithm of the exponential probability
        density function (pdf).

        :param ndarray data: the data points at which to calculate the
                             logarithm of the pdf.
        :param float theta: the scale parameter.
        :param float gamma: the location parameter.
        :return: the value(s) of the logarithm of the pdf.
        :rtype: ndarray
        """

        return np.log(theta) - theta * (data - gamma)

    def log_likelihood(self, theta, gamma, data):   # pylint: disable=C0103, R0201, W0613
        """
        Method to calculate the value of the log likelihood function for the
        exponential distribution.

        :param float theta: the scale parameter at which to evaluate the
                            log-likelihood.
        :param float gamma: the location parameter at which to evaluate the
                            log-likelihood.
        :param ndarray data: the data set to calculate the log-likelihood for.
                             * 0 - left of the observation time interval
                             * 1 - right of the observation time interval
                             * 2 - number of events occurring at the observation
                                   time
                             * 3 - status, where status is:
                                * 1 - event
                                * 2 - right censored
                                * 3 - interval censored
        """

        # TODO: Extend this to the two-parameter Exponential
        # Calculate the value of the log-likelihood for the event observations.
        _event_t = data[np.where(data[:, 3] == 1)][:, 1]
        _event_n = data[np.where(data[:, 3] == 1)][:, 2]
        _event_ll = np.sum(_event_n * np.log((theta * np.exp(theta * _event_t))))

        # Calculate the value of the log-likelihood for the right-censored
        # observations.
        _right_t = data[np.where(data[:, 3] == 2)][:, 1]
        _right_n = data[np.where(data[:, 3] == 2)][:, 2]
        _right_ll = np.sum(_right_n * theta * _right_t)

        # Calculate the value of the log-likelihood for the left- and interval-
        # censored observations.
        _interval_lt = data[np.where(data[:, 3] == 3)][:, 0]
        _interval_rt = data[np.where(data[:, 3] == 3)][:, 1]
        _interval_n = data[np.where(data[:, 3] == 3)][:, 2]

        _interval_ll = np.sum(_interval_n *
                              np.log(np.exp(-theta * _interval_lt) -
                                     np.exp(-theta * _interval_rt)))

        _logLik = _event_ll - _right_ll + _interval_ll

        return _logLik

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
                                * 3 - interval censored
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
        _interval_lt = data[np.where(data[:, 3] == 3)][:, 0]
        _interval_rt = data[np.where(data[:, 3] == 3)][:, 1]
        _interval_t = (_interval_lt + _interval_rt) / 2.0
        _interval_n = data[np.where(data[:, 3] == 3)][:, 2]

        _interval_ll = np.sum(_interval_n * ((1.0 / theta) - _interval_t))

        # Following are the exact equations for the interval censored observations.
        # _n = (_interval_lt * exp(-theta * _interval_lt)) - \
        #      (_interval_rt * exp(-theta * _interval_rt))
        # _d = exp(-theta * _interval_lt) - exp(-theta * _interval_rt)
        # _interval_ll = np.sum(_interval_n * (_n / _d))

        _del_theta = _event_ll - _right_ll - _interval_ll

        return _del_theta

    def maximum_likelihood_estimate(self, data, start, end):
        """
        Method to fit data to a parametric distribution and find point
        estimates of the parameters.  It is up to the calling function to
        calculate bounding values.

        :param array-like data: the data set to fit.  This is a list of tuples
                                where each tuple contains the following, in
                                order:
                                * 0 = Observed unit ID
                                * 1 = Interval start time
                                * 2 = Interval end time
                                * 3 = Time between failures or interarrival
                                      time
                                * 4 = Status of observation
                                * 5 = Quantity of observations
                                * 6 = Date of observation
        :param float start: the minimum time to include in the fit.  Used to
                            exclude outliers.
        :param float end: the maximum time to include in the fit.  Used to
                          exclude outliers.
        :return: _fit; [[scale estimate, shape estimate, location estimate],
                        [scale variance, covariance, shape variance],
                        [MLE, AIC, BIC], correlation coeff.]
        :rtype: list
        """

        _error_function = lambda s, x, y: ((s[0] + s[1] * x) - y)

        # Initialize lists to hold results.
        _parameters = [0.0, 0.0]            # Scale and location parameters.
        _variance = [0.0, 0.0, 0.0]         # Scale variance, covariance,
                                            # location variance.
        _gof = [0.0, 0.0, 0.0]              # MLE, AIC, BIC

        # Format the input data set.
        (_data, _n_records) = format_data_set(data, start, end)

        # Provide an estimate of theta assuming no suspensions and using
        # the right of the interval.  Use this as the starting value to
        # scipy.optimize.fsolve.
        #_theta = 1.0 / expon.fit(np.array(_data[:, 1], dtype=float),
        #                          floc=0)[1]

        #_parameters[0] = optim.fsolve(self.partial_derivatives, _theta,
        #                              args=np.array(_data, dtype=float))[0]

        # Estimate the scale parameter using the fit function from
        # scipy.stats.
        _parameters[0] = 1.0 / expon.fit(_data[:, 4], floc=0)[1]

        _fI = fisher_information(self.log_pdf, _parameters, _data[:, 4])
        _variance[0] = 1.0 / _fI[0, 0]

        _gof[0] = self.log_likelihood(_parameters[0], _parameters[1], _data)
        _gof[1] = -2.0 * _gof[0] + 2.0
        _gof[2] = -2.0 * _gof[0] + (np.log(_n_records) - np.log(np.pi))

        _fit = [_parameters, _variance, _gof]

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
        :param list para: list with the values of the distribution parameters.
        :return: _y; the probabilities of the theoretical distribution with
                 parameters para.
        :rtype: ndarray
        """

        # TODO: Write a test for Exponential.theoretical_distribution.

        _x = np.sort(np.array(data[:, 2], dtype=float))
        _y = 1.0 - np.exp(-params[0] * _x)

        return _y


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
        gaussian distribution.

        :param float x: the parameter values at which to evaluate the
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
                           np.log((1.0 / (_event_t * x[1])) *
                                  norm.pdf((np.log(_event_t) - x[0]) / x[1])))

        # Calculate the value of the log-likelihood for the right-censored
        # observations.
        _right_t = data[np.where(data[:, 3] == 2)][:, 1]
        _right_n = data[np.where(data[:, 3] == 2)][:, 2]
        _right_ll = np.sum(_right_n *
                           (1.0 - norm.cdf((np.log(_right_t) - x[0]) / x[1])))

        # Calculate the value of the log-likelihood for the left- and interval-
        # censored observations.
        _interval_lt = data[np.where(data[:, 3] == 3)][:, 0]
        _interval_rt = data[np.where(data[:, 3] == 3)][:, 1]
        _interval_n = data[np.where(data[:, 3] == 3)][:, 2]

        _interval_ll = np.sum(_interval_n *
                              np.log(norm.cdf((_interval_rt - x[0]) / x[1]) -
                                     norm.cdf((_interval_lt - x[0]) / x[1])))

        _logLik = _event_ll - _right_ll + _interval_ll

        return _logLik

    def partial_derivatives(self, x, data):         # pylint: disable=C0103, R0201, R0914
        """
        Method to calculate the value of the partial derivatives of the
        gaussian log-likelihood function with respect to mu and sigma.  This
        function is passed as an argument to scipy.optimize.fsolve() to find
        the values of mu and sigma that simultaneously minimizes the partials.

        :param list x: the values of mu and sigma at which to calculate the
                       partials.
        :param ndarray data: the data set to calculate the partials for.
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
        _event_sigma = np.sum(_event_n *
                              (((_event_t - x[0]) / x[1]**3.0) - (1.0 / x[1])))
        _event_mu = (1.0 / x[1]**2.0) * np.sum(_event_n * (_event_t - x[0]))

        # Calculate the value of the log-likelihood for the right-censored
        # observations.
        _right_t = data[np.where(data[:, 3] == 2)][:, 1]
        _right_n = data[np.where(data[:, 3] == 2)][:, 2]

        _norm = (_right_t - x[0]) / x[1]
        _cdf = norm.cdf(_norm)
        _right_mu = (1.0 / x[1]) * \
            np.sum(_right_n * (norm.pdf(_norm) / (1.000000001 - _cdf)))
        _right_sigma = (1.0 / x[1]) * \
            np.sum(_right_n *
                   ((_norm * norm.pdf(_norm)) / (1.000000001 - _cdf)))

        # Calculate the value of the log-likelihood for the left- and interval-
        # censored observations.  Use the midpoint of the interval as an
        # approximation.
        _interval_lt = data[np.where(data[:, 3] == 3)][:, 0]
        _interval_rt = data[np.where(data[:, 3] == 3)][:, 1]
        _interval_t = (_interval_lt + _interval_rt) / 2.0
        _interval_n = data[np.where(data[:, 3] == 3)][:, 2]

        _interval_sigma = np.sum(_interval_n *
                                 (((_interval_t - x[0]) / x[1]**3.0) -
                                  (1.0 / x[1])))
        _interval_mu = (1.0 / x[1]**2.0) * \
            np.sum(_interval_n * (_interval_t - x[0]))

        # Following are the exact equations for the interval censored observations.
        # _norm_r = (_interval_rt - x[0]) / x[1]
        # _pdf_r = norm.pdf(_norm_r)
        # _cdf_r = norm.cdf(_norm_r)

        # _norm_l = (_interval_lt - x[0]) / x[1]
        # _pdf_l = norm.pdf(_norm_l)
        # _cdf_l = norm.cdf(_norm_l)

        # _n = _pdf_r - _pdf_l
        # _d = _cdf_r - _cdf_l
        # _interval_mu = (1.0 / x[1]) * np.sum(_interval_n * _n / _d)

        # _n = (_norm_r * _pdf_r) - (_norm_l * _pdf_l)
        # _interval_sigma = (1.0 / x[1]) * np.sum(_interval_n * _n / _d)

        _del_mu = _event_mu + _right_mu - _interval_mu
        _del_sigma = _event_sigma + _right_sigma - _interval_sigma

        return _del_mu, _del_sigma

    def maximum_likelihood_estimate(self, data, start, end):    # pylint: disable=R0914
        """
        Method to fit data to a parametric distribution and find point
        estimates of the parameters.  It is up to the calling function to
        calculate bounding values.

        :param array-like data: the data set to fit.  This is a list of tuples
                                where each tuple contains the following, in
                                order:
                                * 0 = Observed unit ID
                                * 1 = Interval start time
                                * 2 = Interval end time
                                * 3 = Time between failures or interarrival
                                      time
                                * 4 = Status of observation
                                * 5 = Quantity of observations
                                * 6 = Date of observation
        :param float start: the minimum time to include in the fit.  Used to
                            exclude outliers.
        :param float end: the maximum time to include in the fit.  Used to
                          exclude outliers.
        :return: _fit; [[scale estimate, shape estimate, location estimate],
                        [scale variance, covariance, shape variance],
                        [MLE, AIC, BIC], correlation coeff.]
        :rtype: list
        """

        _error_function = lambda s, x, y: ((s[0] + s[1] * x) - y)

        # Initialize lists to hold results.
        _parameters = [0.0, 0.0]            # Scale and location parameters.
        _variance = [0.0, 0.0, 0.0]         # Scale variance, covariance,
                                            # location variance.
        _gof = [0.0, 0.0, 0.0]              # MLE, AIC, BIC

        # Format the input data set.
        (_data, _n_records) = format_data_set(data, start, end)

        # Provide an estimate of mu and sigma assuming no suspensions and
        # using the right of the interval.  Use these as the starting
        # values to scipy.optimize.fsolve.

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

        (_mu, _sigma) = norm.fit(np.array(_data[:, 4], dtype=float))
        #optim.fsolve(self.partial_derivatives, [_mu, _sigma],
        #              args=np.array(_data, dtype=float))

        _parameters[0] = _mu
        _parameters[1] = _sigma

        _fI = fisher_information(self.log_pdf, _parameters, _data[:, 4])
        _variance[0] = 1.0 / np.diag(_fI)[0]
        _variance[1] = 1.0 / np.diag(_fI)[1]

        _gof[0] = self.log_likelihood([_parameters[0], _parameters[1]], _data)
        _gof[1] = -2.0 * _gof[0] + 2.0
        _gof[2] = -2.0 * _gof[0] + (np.log(_n_records) - np.log(np.pi))

        _fit = [_parameters, _variance, _gof]

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

        # TODO: Write a test for Gaussian.theoretical_distribution.

        _x = np.sort(np.array(data[:, 2], dtype=float))

        _x = (np.log(_x + 0.01) - params[0]) / params[1]
        _y = norm.cdf(_x)

        return _y


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

    def log_likelihood(self, x, data):      # pylint: disable=C0103, R0201
        """
        Method to calculate the value of the log likelihood function for the
        lognormal distribution.

        :param float x: the parameter values at which to evaluate the
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
                           np.log((1.0 / (_event_t * x[1])) *
                                  norm.pdf((np.log(_event_t) - x[0]) / x[1])))

        # Calculate the value of the log-likelihood for the right-censored
        # observations.
        _right_t = data[np.where(data[:, 3] == 2)][:, 1]
        _right_n = data[np.where(data[:, 3] == 2)][:, 2]
        _right_ll = np.sum(_right_n *
                           (1.0 - norm.cdf((np.log(_right_t) - x[0]) / x[1])))

        # Calculate the value of the log-likelihood for the left- and interval-
        # censored observations.
        _interval_lt = data[np.where(data[:, 3] == 3)][:, 0]
        _interval_rt = data[np.where(data[:, 3] == 3)][:, 1]
        _interval_n = data[np.where(data[:, 3] == 3)][:, 2]

        _interval_ll = np.sum(_interval_n *
                              np.log(norm.cdf(
                                  (np.log(_interval_rt) - x[0]) / x[1]) -
                                     norm.cdf(
                                         (np.log(_interval_lt) - x[0]) / x[1])))

        _logLik = _event_ll - _right_ll + _interval_ll

        return _logLik

    def partial_derivatives(self, x, data):         # pylint: disable=C0103, R0201, R0914
        """
        Method to calculate the value of the partial derivatives of the
        lognormal log-likelihood function with respect to mu and sigma.  This
        function is passed as an argument to scipy.optimize.fsolve() to find
        the values of mu and sigma that simultaneously minimizes the partials.

        :param list x: the values of mu and sigma at which to calculate the
                       partials.
        :param ndarray data: the data set to calculate the partials for.
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
        _event_sigma = np.sum(_event_n *
                              (((_event_t - x[0]) / x[1]**3.0) - (1.0 / x[1])))
        _event_mu = (1.0 / x[1]**2.0) * np.sum(_event_n * (_event_t - x[0]))

        # Calculate the value of the log-likelihood for the right-censored
        # observations.
        _right_t = data[np.where(data[:, 3] == 2)][:, 1]
        _right_n = data[np.where(data[:, 3] == 2)][:, 2]

        _norm = (_right_t - x[0]) / x[1]
        _cdf = norm.cdf(_norm)
        _right_mu = (1.0 / x[1]) * \
            np.sum(_right_n * (norm.pdf(_norm) / (1.000000001 - _cdf)))
        _right_sigma = (1.0 / x[1]) * \
            np.sum(_right_n *
                   ((_norm * norm.pdf(_norm)) / (1.000000001 - _cdf)))

        # Calculate the value of the log-likelihood for the left- and interval-
        # censored observations.  Use the midpoint of the interval as an
        # approximation.
        _interval_lt = data[np.where(data[:, 3] == 3)][:, 0]
        _interval_rt = data[np.where(data[:, 3] == 3)][:, 1]
        _interval_t = (_interval_lt + _interval_rt) / 2.0
        _interval_n = data[np.where(data[:, 3] == 3)][:, 2]

        _interval_sigma = np.sum(_interval_n *
                                 (((_interval_t - x[0]) / x[1]**3.0) -
                                  (1.0 / x[1])))
        _interval_mu = (1.0 / x[1]**2.0) * \
            np.sum(_interval_n * (_interval_t - x[0]))

        # Following are the exact equations for the interval censored
        # observations.
        # _norm_r = (_interval_rt - x[0]) / x[1]
        # _pdf_r = norm.pdf(_norm_r)
        # _cdf_r = norm.cdf(_norm_r)

        # _norm_l = (_interval_lt - x[0]) / x[1]
        # _pdf_l = norm.pdf(_norm_l)
        # _cdf_l = norm.cdf(_norm_l)

        # _n = _pdf_r - _pdf_l
        # _d = _cdf_r - _cdf_l
        # _interval_mu = (1.0 / x[1]) * np.sum(_interval_n * _n / _d)

        # _n = (_norm_r * _pdf_r) - (_norm_l * _pdf_l)
        # _interval_sigma = (1.0 / x[1]) * np.sum(_interval_n * _n / _d)

        _del_mu = _event_mu + _right_mu - _interval_mu
        _del_sigma = _event_sigma + _right_sigma - _interval_sigma

        return _del_mu, _del_sigma

    def maximum_likelihood_estimate(self, data, start, end):    # pylint: disable=R0914
        """
        Method to fit data to a parametric distribution and find point
        estimates of the parameters.  It is up to the calling function to
        calculate bounding values.

        :param array-like data: the data set to fit.  This is a list of tuples
                                where each tuple contains the following, in
                                order:
                                * 0 = Observed unit ID
                                * 1 = Interval start time
                                * 2 = Interval end time
                                * 3 = Time between failures or interarrival
                                      time
                                * 4 = Status of observation
                                * 5 = Quantity of observations
                                * 6 = Date of observation
        :param float start: the minimum time to include in the fit.  Used to
                            exclude outliers.
        :param float end: the maximum time to include in the fit.  Used to
                          exclude outliers.
        :return: _fit; [[scale estimate, shape estimate, location estimate],
                        [scale variance, covariance, shape variance],
                        [MLE, AIC, BIC], correlation coeff.]
        :rtype: list
        """

        _error_function = lambda s, x, y: ((s[0] + s[1] * x) - y)

        # Initialize lists to hold results.
        _parameters = [0.0, 0.0]            # Scale and shape parameters.
        _variance = [0.0, 0.0, 0.0]         # Scale variance, covariance,
                                            # shape variance.
        _gof = [0.0, 0.0, 0.0]              # MLE, AIC, BIC

        # Format the input data set.
        (_data, _n_records) = format_data_set(data, start, end)

        # Provide an estimate of mu and sigma assuming no suspensions and
        # using the right of the interval.  Use these as the starting
        # values to scipy.optimize.fsolve.

        # Adjust the right-censored times to be the mid-point between the
        # censored time and the maximum obeserved time in the data set.
        _adj_right = (max(_data[:, 1]) +
                      _data[np.where(_data[:, 3] == 2), 1]) / 2.0
        _data[np.where(_data[:, 3] == 2), 1] = _adj_right

        # Adjust the interval-censored times so they can be passed to the
        # fit method.
        _interval_lt = _data[np.where(_data[:, 3] == 3)][:, 0]
        _interval_rt = _data[np.where(_data[:, 3] == 3)][:, 1]
        _interval_t = (_interval_lt + _interval_rt) / 2.0
        _data[np.where(_data[:, 3] == 3), 1] = _interval_t

        (_sigma, __,
         _mu) = lognorm.fit(np.array(_data[:, 1], dtype=float), floc=0)

        _parameters[0] = np.log(_mu)
        _parameters[1] = _sigma

        _fI = fisher_information(self.log_pdf, _parameters, _data[:, 4])
        _variance[0] = 1.0 / np.diag(_fI)[0]
        _variance[1] = 1.0 / _fI[0][1]
        _variance[2] = 1.0 / np.diag(_fI)[1]

        _gof[0] = self.log_likelihood([_parameters[0], _parameters[1]], _data)
        _gof[1] = -2.0 * _gof[0] + 2.0
        _gof[2] = -2.0 * _gof[0] + (np.log(_n_records) - np.log(np.pi))

        _fit = [_parameters, _variance, _gof]

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

        # TODO: Write a test for LogNormal.theoretical_distribution.

        _x = np.sort(np.array(data[:, 2], dtype=float))

        _x = (np.log(_x + 0.01) - params[0]) / params[1]
        _y = norm.cdf(_x)

        return _y


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

    def log_likelihood(self, x, data):      # pylint: disable=C0103, R0201
        """
        Method to calculate the value of the log likelihood function for the
        weibull distribution.

        :param float x: the parameter values at which to evaluate the
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
                           np.log((1.0 / (_event_t * x[1])) *
                                  norm.pdf((np.log(_event_t) - x[0]) / x[1])))

        # Calculate the value of the log-likelihood for the right-censored
        # observations.
        _right_t = data[np.where(data[:, 3] == 2)][:, 1]
        _right_n = data[np.where(data[:, 3] == 2)][:, 2]
        _right_ll = np.sum(_right_n *
                           (1.0 - norm.cdf((np.log(_right_t) - x[0]) / x[1])))

        # Calculate the value of the log-likelihood for the left- and interval-
        # censored observations.
        _interval_lt = data[np.where(data[:, 3] == 3)][:, 0]
        _interval_rt = data[np.where(data[:, 3] == 3)][:, 1]
        _interval_n = data[np.where(data[:, 3] == 3)][:, 2]

        _interval_ll = np.sum(_interval_n *
                              np.log(norm.cdf(
                                  (np.log(_interval_rt) - x[0]) / x[1]) -
                                     norm.cdf(
                                         (np.log(_interval_lt) - x[0]) / x[1])))

        _logLik = _event_ll - _right_ll + _interval_ll

        return _logLik

    def partial_derivatives(self, x, data):     # pylint: disable=C0103, R0201, R0914
        """
        Method to calculate the value of the partial derivatives of the
        weibull log-likelihood function with respect to mu and sigma.  This
        function is passed as an argument to scipy.optimize.fsolve() to find
        the values of mu and sigma that simultaneously minimizes the partials.

        :param list x: the values of mu and sigma at which to calculate the
                       partials.
        :param ndarray data: the data set to calculate the partials for.
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
        _event_ll_beta = np.sum(_event_n) / x[1] + \
            np.sum(_event_n * np.log(_event_t / x[0])) - \
            np.sum(_event_n * (_event_t / x[0])**x[1] * np.log(_event_t / x[0]))
        _event_ll_eta = (-x[1] / x[0]) * np.sum(_event_n) + \
                        (x[1] / x[0]) * np.sum(_event_n * (_event_t / x[0])**x[1])

        # Calculate the value of the log-likelihood for the right-censored
        # observations.
        _right_t = data[np.where(data[:, 3] == 2)][:, 1]
        _right_n = data[np.where(data[:, 3] == 2)][:, 2]
        _right_ll_beta = np.sum(_right_n * (_right_t / x[0])**x[1] *
                                np.log(_right_t / x[0]))
        _right_ll_eta = (x[1] / x[0]) * np.sum(_right_n * (_right_t / x[0])**x[1])

        # Calculate the value of the log-likelihood for the left- and interval-
        # censored observations.  Use the midpoint of the interval as an
        # approximation.
        _interval_lt = data[np.where(data[:, 3] == 3)][:, 0]
        _interval_rt = data[np.where(data[:, 3] == 3)][:, 1]
        _interval_t = (_interval_lt + _interval_rt) / 2.0
        _interval_n = data[np.where(data[:, 3] == 3)][:, 2]

        _interval_ll_beta = np.sum(_interval_n) / x[1] + \
            np.sum(_interval_n * np.log(_interval_t / x[0])) - \
            np.sum(_interval_n * (_interval_t / x[0])**x[1] *
                   np.log(_interval_t / x[0]))
        _interval_ll_eta = (-x[1] / x[0]) * np.sum(_interval_n) + \
                           (x[1] / x[0]) * np.sum(_interval_n *
                                                  (_interval_t / x[0])**x[1])

        # Following are the exact equations for the interval censored observations.
        # _nr = _interval_rt / x[0]
        # _nr_b = (_nr + 0.000001)**x[1]
        # _nr_exp = np.exp(-(_nr_b))

        # _nl = _interval_lt / x[0]
        # _nl_b = (_nl + 0.000001)**x[1]
        # _nl_exp = np.exp(-(_nl_b))

        # _n = (-_nl_b * np.log(_nl_b) * _nl_exp) + (_nr_b * np.log(_nr_b) * _nr_exp)
        # _d = _nl_exp - _nr_exp
        # _interval_ll_beta = np.sum(_interval_n * _n / _d)

        # _n = ((x[1] / x[0]) * _nl_b * _nl_exp) - ((x[1] / x[0]) * _nr_b * _nr_exp)
        # _interval_ll_eta = np.sum(_interval_n * _n / _d)

        _del_beta = _event_ll_beta - _right_ll_beta + _interval_ll_beta
        _del_eta = _event_ll_eta - _right_ll_eta + _interval_ll_eta

        return _del_eta, _del_beta

    def maximum_likelihood_estimate(self, data, start, end):
        """
        Method to fit data to a parametric distribution and find point
        estimates of the parameters.  It is up to the calling function to
        calculate bounding values.

        :param array-like data: the data set to fit.  This is a list of tuples
                                where each tuple contains the following, in
                                order:
                                * 0 = Observed unit ID
                                * 1 = Interval start time
                                * 2 = Interval end time
                                * 3 = Time between failures or interarrival
                                      time
                                * 4 = Status of observation
                                * 5 = Quantity of observations
                                * 6 = Date of observation
        :param float start: the minimum time to include in the fit.  Used to
                            exclude outliers.
        :param float end: the maximum time to include in the fit.  Used to
                          exclude outliers.
        :return: _fit; [[scale estimate, shape estimate, location estimate],
                        [scale variance, covariance, shape variance],
                        [MLE, AIC, BIC], correlation coeff.]
        :rtype: list
        """

        _error_function = lambda s, x, y: ((s[0] + s[1] * x) - y)

        # Initialize lists to hold results.
        _parameters = [0.0, 0.0, 0.0]       # Scale, shape, and location
                                            # parameters.
        _variance = [0.0, 0.0, 0.0]         # Scale variance, covariance,
                                            # location variance.
        _gof = [0.0, 0.0, 0.0]              # MLE, AIC, BIC

        # Format the input data set.
        (_data, _n_records) = format_data_set(data, start, end)

        # Provide an estimate of eta and beta assuming no suspensions and
        # using the right of the interval.  Use these as the starting
        # values to scipy.optimize.fsolve.
        (__, _beta,
         __, _eta) = exponweib.fit(np.array(_data[:, 4], dtype=float),
                                   f0=1, floc=0)

        #(_eta, _beta) = optim.fsolve(self.partial_derivs, [_eta, _beta],
        #                             args=np.array(_data, dtype=float))
        _parameters[0] = _eta
        _parameters[1] = _beta

        _fI = fisher_information(self.log_pdf, _parameters, _data[:, 4])
        _variance[0] = 1.0 / np.diag(_fI)[0]
        _variance[1] = 1.0 / np.diag(_fI)[1]
        _variance[2] = 1.0 / _fI[0, 1]

        _gof[0] = self.log_likelihood([_parameters[0], _parameters[1]], _data)
        _gof[1] = -2.0 * _gof[0] + 2.0
        _gof[2] = -2.0 * _gof[0] + (np.log(_n_records) - np.log(np.pi))

        _fit = [_parameters, _variance, _gof]

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

        # TODO: Write a test for Weibull.theoretical_distribution.

        _x = np.sort(np.array(data[:, 2], dtype=float))

        _y = 1.0 - np.exp(-(_x / params[0])**params[1])
        print _y
        return _y
