# -*- coding: utf-8 -*-
#
#       ramstk.analyses.statistics.distributions.exponential.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for the exponential distribution."""

# Standard Library Imports
from collections import OrderedDict
from typing import Any, Dict, List, Tuple, Union

# Third Party Imports
import numpy as np
import scipy.optimize as optimize
from scipy.stats import chi2, expon

# RAMSTK Package Imports
from ramstk.analyses.statistics.bounds import do_calculate_fisher_information


# pylint: disable=unsubscriptable-object
def hazard_function(rate: List[float], start_time: float, end_time: float,
                    step_time: float) -> OrderedDict[int, List[float]]:
    """Calculate the hazard function for the exponential distribution.

    This method calculates the point estimate as well as the bounding
    values at each time step.  The start and end times bound the hazard
    function.

    :param rate: a list of rate parameter (lambda) for the exponential
        distribution to calculate the hazard function for.  This list is
        lower bound, point, upper bound estimates of lambda.
    :param start_time: the first time to calculate the hazard function.
    :param end_time: the last time to calculate the hazard function.
    :param step_time: the interval of time between start_time and end_time to
        calculate the hazard function.
    :return: _hazard; a dict of lists where the key is the time at which the
        hazard functions was calculated and the value is a list of the lower
        bound, point estimate, and upper bound.  Because this is the
        exponential distribution, this function simply returns rate for each
        time (key).
    :rtype: dict
    """
    _hazard = OrderedDict()

    for _time in range(int(start_time), int(end_time), int(step_time)):
        _hazard[_time] = rate

    return _hazard


def likelihood_bounds(theta: float, loc: float, confidence: float,
                      data: np.ndarray) -> Tuple[float, float]:
    """Method to calculate the likelihood ratio confidence bounds.

    Likelihood confidence bounds are calculated by finding values for theta
    that satisfy:

        L(theta) = L(theta_hat) * exp(-scipy.chi2.ppf(alpha, 1) / 2.0)

    Taking logarithms (base e) of the equation above results in:

        log[L(theta)] = log[L(theta_hat)] - scipy.chi2.ppf(alpha, 1) / 2.0

    The same values of theta will minimize both, but logarithms are easier
    to work with.

    :param theta: the scale parameter at which to evaluate the log-likelihood.
    :param loc: the location parameter at which to evaluate the log-likelihood.
    :param confidence: the confidence level at which to calculate the bounds.
    :param data: the data set to calculate the log-likelihood for.  Each record
        in the data set must have the following information, in order:

        * 0 - left of the observation time interval
        * 1 - right of the observation time interval
        * 2 - number of events occurring at the observation time
        * 3 - status, where status is:
            * 1 - event
            * 2 - right censored
            * 3 - left censored
            * 4 - interval censored
        * 4 - interarrival time or time between failures

    :return: _lower, _upper; the lower an upper confidence bounds on the
        parameters.
    :rtype: tuple
    """
    _constant = chi2.ppf(confidence, 1) / 2.0
    _log_lik_ratio = log_likelihood_ratio(theta, loc, data, _constant)

    # To find the lower bound, we provide root with a starting value for
    # theta less than the point estimate; in this case 1/100 the value.
    _lower = optimize.root(log_likelihood_ratio,
                           theta / 100.0,
                           args=(loc, data, _constant)).x[0]

    # To find the upper bound, we provide root with a starting value for
    # theta greater than the point estimate; in this case 1.01 times the
    # value.
    _upper = optimize.root(log_likelihood_ratio,
                           theta * 1.01,
                           args=(loc, data, _constant)).x[0]

    return _lower, _upper


# noinspection PyUnusedLocal
# pylint: disable=unused-argument
def log_likelihood(theta: float, loc: float, data: np.ndarray) -> np.ndarray:
    """Calculate the value of the exponential log likelihood function.

    :param data: the data set to calculate the log-likelihood for.  Each record
        in the data set must have the following information, in order:

        * 0 - left of the observation time interval
        * 1 - right of the observation time interval
        * 2 - number of events occurring at the observation time
        * 3 - status, where status is:
            * 1 - event
            * 2 - right censored
            * 3 - left censored
            * 4 - interval censored
        * 4 - interarrival time or time between failures

    :param theta: the scale parameter at which to evaluate the log-likelihood.
    :param loc: the location parameter at which to evaluate the log-likelihood.
    """
    # ISSUE: Extend log_likelihood() function to the two-parameter Exponential
    #
    # Extend the log_likelihood() function in th exponential distribution
    # module to handle location data.  This will allows the estimation of the
    # location parameter of the two-parameter exponential.

    # Calculate the value of the log-likelihood for the event observations.
    _event_t = data[np.where(data[:, 3] == 1)][:, 1]
    _event_n = data[np.where(data[:, 3] == 1)][:, 2]
    _event_ll = np.sum(_event_n * np.log((theta * np.exp(-theta * _event_t))))

    # Calculate the value of the log-likelihood for the right-censored
    # observations.
    _right_t = data[np.where(data[:, 3] == 2)][:, 1]
    _right_n = data[np.where(data[:, 3] == 2)][:, 2]
    _right_ll = np.sum(_right_n * theta * _right_t)

    # Calculate the value of the log-likelihood for the left- and interval-
    # censored observations.
    _interval_lt = data[np.where(
        np.logical_or(data[:, 3] == 3, data[:, 3] == 4))][:, 0]
    _interval_rt = data[np.where(
        np.logical_or(data[:, 3] == 3, data[:, 3] == 4))][:, 1]
    _interval_n = data[np.where(np.logical_or(data[:, 3] == 3,
                                              data[:, 3] == 4))][:, 2]

    _interval_ll = np.sum(_interval_n * ((-theta * _interval_lt) -
                                         (-theta * _interval_rt)))

    _logLik = _event_ll - _right_ll + _interval_ll

    return _logLik


def log_likelihood_ratio(theta: float,
                         loc: float,
                         data: np.ndarray,
                         const=0.0) -> float:
    """Minimize when finding likelihood ratio confidence bounds.

    The equation this method calculates is:

        log[L(theta)] - scipy.chi2.ppf(alpha, 1) / 2.0

    where the keyword const is the scipy.chi2.ppf(alpha, 1) / 2.0 part.

    :param theta: the scale parameter at which to evaluate the log-likelihood.
    :param loc: the location parameter at which to evaluate the log-likelihood.
    :param data: the data set to calculate the log-likelihood for.  Each record
        in the data set must have the following information, in order:

        * 0 - left of the observation time interval
        * 1 - right of the observation time interval
        * 2 - number of events occurring at the observation time
        * 3 - status, where status is:
            * 1 - event
            * 2 - right censored
            * 3 - left censored
            * 4 - interval censored
        * 4 - interarrival time or time between failures

    :param const: constant value to subtract from the log-likelihood.  It is
        the value of scipy.chi2.ppf(alpha, 1) / 2.0 which should be calculated
        by the calling function based on the desired alpha.
    :return: _log_lik_ratio
    :rtype: float
    """
    return log_likelihood(theta, loc, data) - const


def log_pdf(data: np.ndarray, theta: float, loc: float = 0.0) -> np.ndarray:
    """Calculate the logarithm of the exponential pdf.

    Assumes the engineering parameterization:

    f(x; theta) = (1 / theta)exp(-x / theta)

    Without a location parameter:

    >>> data=np.array([5.,10.,15.,20.,25.,30.,35.,40.,50.,60.,70.,80.,90.,100.])
    >>> theta=0.02222222
    >>> log_pdf(data, theta)
    array([-3.91777369, -4.02888479, -4.13999589, -4.25110699, -4.36221809,
           -4.47332919, -4.58444029, -4.69555139, -4.91777359, -5.13999579,
           -5.36221799, -5.58444019, -5.80666239, -6.02888459])

    With a location parameter:

    >>> data=np.array([5.,10.,15.,20.,25.,30.,35.,40.,50.,60.,70.,80.,90.,100.])
    >>> theta=0.02222222
    >>> loc=10.0
    >>> log_pdf(data, theta, loc)
    array([-3.69555149, -3.80666259, -3.91777369, -4.02888479, -4.13999589,
           -4.25110699, -4.36221809, -4.47332919, -4.69555139, -4.91777359,
           -5.13999579, -5.36221799, -5.58444019, -5.80666239])

    :param data: the data points at which to calculate the logarithm of the
        pdf.
    :param theta: the scale parameter.
    :param loc: the location parameter.
    :return: the value(s) of the logarithm of the pdf.
    :rtype: ndarray
    :raises: RuntimeWarning when np.log encounters a value of theta <= 0.0.
    """
    return np.log(theta) - theta * (data - loc)


def mean(rate: List[float], start_time: float, end_time: float,
         step_time: float) -> Dict[int, List[float]]:
    """Calculate the mean for the exponential distribution.

    This function calculates the mean between start_time and end_time in
    intervals of step_time.  The point estimate as well as the bounding
    values at each time step are calculated.

    :param rate: a list of rate parameter (lambda) for the exponential
        distribution to calculate the hazard function for.  This list is
        lower bound, point, upper bound estimates of lambda.
    :param start_time: the first time to calculate the mean.
    :param end_time: the last time to calculate the mean.
    :param step_time: the interval of time between start_time and end_time to
        calculate the mean.
    :return: _mean; a dict of lists where the key is the time at which the
        means were calculated and the value is a list of the lower bound, point
        estimate, and upper bound.  Because this is the exponential
        distribution, this function simply returns inverse of the rate for
        each time (key).
    :rtype: dict
    """
    _mean = {}

    for _time in range(int(start_time), int(end_time), int(step_time)):
        _values = [0.0, 0.0, 0.0]

        _values[0] = 1.0 / rate[2]
        _values[1] = 1.0 / rate[1]
        _values[2] = 1.0 / rate[0]

        _mean[_time] = _values

    return _mean


def mle(data: np.ndarray, start: float,
        end: float) -> List[Union[List[float], Any, int]]:
    """Fit data and find point estimates of the parameters.

    It is up to the calling function to calculate bounding values.

    :param data: the data set to fit.  This is a numpy array where each record
        contains the following, in order:

        * 0 - left of the observation time interval
        * 1 - right of the observation time interval
        * 2 - number of events occurring at the observation time
        * 3 - status, where status is:
            * 1 - event
            * 2 - right censored
            * 3 - left censored
            * 4 - interval censored
        * 4 = Time between failures or interarrival time

    :param start: the minimum time to include in the fit.  Used to exclude
        outliers.
    :param end: the maximum time to include in the fit.  Used to exclude
        outliers.
    :return: _fit; [[scale estimate, shape estimate, location estimate],
                    [scale variance, covariance, shape variance],
                    [MLE, AIC, BIC], correlation coeff.]
    :rtype: list
    """
    # ISSUE: Refactor exponential.mle to reduce complexity.
    #
    # The function mle() in the exponential module has a cyclic complexity
    # score of 11 (grade of C).  Refactor this function to make it less
    # complex, more understandable, and more maintainable.

    # Initialize lists to hold results.
    # Scale and location parameters.
    _parameters = [0.0, 0.0]
    # Scale variance, covariance, location variance.
    _variance = [0.0, 0.0, 0.0]
    # MLE, AIC, BIC
    _gof = [0.0, 0.0, 0.0]

    # Sort data by the right of the interval.  Remove records occurring
    # before the start time and after the end time.
    _data = sorted(data, key=lambda x: float(x[1]))
    _data = [_record for _record in _data if float(_record[0]) >= start]
    _data = [_record for _record in _data if float(_record[1]) <= end]
    _data = np.array(_data)

    # Count the number of suspensions, failures, and records.
    _n_suspensions = sum(x[2] for x in _data if x[3] == 2)
    _n_failures = sum(x[2] for x in _data
                      if x[3] == 1 or x[3] == 3 or x[3] == 4)
    _n_records = len(_data)

    # Estimate the initial guess for the scale parameter using the fit
    # function from scipy.stats.  Then minimize the partial derivative of
    # the likelihood function to find the final theta value.
    _theta = 1.0 / expon.fit(_data[:, 1])[1]  # type: ignore
    _parameters[0] = optimize.fsolve(partial_derivatives, _theta,
                                     args=(_data))[0]

    _fI = do_calculate_fisher_information(log_pdf, _parameters,
                                          _data[:, 3])  # type: ignore
    _variance[0] = 1.0 / _fI[0, 0]

    _gof[0] = log_likelihood(_parameters[0], _parameters[1], _data)
    _gof[1] = -2.0 * _gof[0] + 2.0
    _gof[2] = -2.0 * _gof[0] + (np.log(_n_records) - np.log(np.pi))

    _fit = [_parameters, _variance, _gof, _n_suspensions, _n_failures]

    return _fit


def partial_derivatives(theta: float, data: np.ndarray) -> np.ndarray:
    """Calculate the partial derivative of the exp log-likelihood function.

    This method is passed as an argument to scipy.optimize.fsolve() to find the
    value of theta that minimizes the partial.

    :param data: the data set to calculate the log-likelihood.  Each record in
        the data set must have the following information, in order:

        * 0 - left of the observation time interval
        * 1 - right of the observation time interval
        * 2 - number of events occurring at the observation time
        * 3 - status, where status is:
            * 1 - event
            * 2 - right censored
            * 3 - left censored
            * 4 - interval censored

        It is up to the calling function to ensure the data is in the above
        format.
    :param theta: the scale parameter value at which to evaluate the
        partial derivative.
    :return: _del_theta
    :rtype: np.ndarray
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
    _interval_lt = data[np.where(
        np.logical_or(data[:, 3] == 3, data[:, 3] == 4))][:, 0]
    _interval_rt = data[np.where(
        np.logical_or(data[:, 3] == 3, data[:, 3] == 4))][:, 1]
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


# pylint: disable=unsubscriptable-object
def reliability_function(rate: List[float], start_time: float, end_time: float,
                         step_time: float) -> OrderedDict[int, List[float]]:
    """Calculate the reliability function for the exponential distribution.

    This function calculates the mean between start_time and end_time in
    intervals of step_time.  The point estimate as well as the bounding
    values at each time step.

    :param rate: a list of rate parameter (lambda) for the exponential
        distribution to calculate the hazard function for.  This list is
        lower bound, point, upper bound estimates of lambda.
    :param start_time: the first time to calculate the reliability function.
    :param end_time: the last time to calculate the reliability function.
    :param step_time: the interval of time between start_time and end_time to
        calculate the reliability function.
    :return: _reliability; a dict of lists where the key is the time at which
        the reliability function was calculated and the value is a list of the
        lower bound, point estimate, and upper bound.
    :rtype: dict
    """
    _reliability = OrderedDict()

    for _time in range(int(start_time), int(end_time), int(step_time)):
        _values = [0.0, 0.0, 0.0]

        _values[0] = np.exp(-rate[0] * _time)
        _values[1] = np.exp(-rate[1] * _time)
        _values[2] = np.exp(-rate[2] * _time)

        _reliability[_time] = _values

    return _reliability


def theoretical_distribution(data: np.ndarray,
                             params: List[float]) -> np.ndarray:
    """Create data set from the theoretical distribution given parameters.

    :param data: the data set that the theoretical distribution will be
        created for.  This is a zero-based list of lists or list of tuples
        where index 1 is the left of the interval and index 2 is the right
        of the interval.  The other indices are not used.
    :param params: list with the values of the distribution parameters.
    :return: _y; the probabilities of the theoretical distribution with
        parameters para.
    :rtype: ndarray
    """
    _x = np.sort(np.array(data, dtype=float))
    _y = 1.0 - np.exp(-params[0] * _x)

    return _y
