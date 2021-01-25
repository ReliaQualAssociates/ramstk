# -*- coding: utf-8 -*-
#
#       ramstk.analyses.statistics.bounds.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Functions for performing calculations associated with statistical bounds."""

# Standard Library Imports
import inspect
from typing import Callable, List, Tuple

# Third Party Imports
import numpy as np
import scipy.misc as misc
from scipy.stats import norm


def do_calculate_beta_bounds(
        minimum: float, likely: float, maximum: float,
        alpha: float) -> Tuple[float, float, float, float]:
    """Calculate the mean, standard error, and bounds of the beta distribution.

    These are the project management estimators, not exact calculations.

    :param minimum: the minimum expected value.
    :param likely: most likely value.
    :param maximum: the maximum expected value.
    :param alpha: the desired confidence level.
    :return: _meanll, _mean, _meanul, _sd; the calculated mean, bounds, and
                                           standard error.
    :rtype: tuple of floats
    """
    if alpha > 1.0:
        _z_norm = norm.ppf(1.0 - ((1.0 - alpha / 100.0) / 2.0))
    else:
        _z_norm = norm.ppf(1.0 - ((1.0 - alpha) / 2.0))

    _mean = (minimum + 4.0 * likely + maximum) / 6.0
    _sd = (maximum - minimum) / 6.0

    _meanll = _mean - _z_norm * _sd
    _meanul = _mean + _z_norm * _sd

    return _meanll, _mean, _meanul, _sd


def do_calculate_fisher_information(model: Callable,
                                    p0: List[float],
                                    data: np.ndarray,
                                    noise=1.0) -> np.ndarray:
    """Calculate the Fisher information matrix for model.

    Sampled on grid X with parameters p0.  Assumes samples are not correlated
    and have equal variance noise^2.  This function is called, for example:

    >>> _data = np.array([[0.0, 1.585, 1, 1, 1.585],
                          [0.0, 1.978, 1, 1, 1.978],
                          ...
                          [0.0, 350.577, 1, 1, 350.577],
                          [0.0, 351.347, 1, 1, 351.347]])
    >>> _p0 = [0.010623498434893014, 0.0]
    >>> _model = log_pdf(data, theta, loc = 0.0)
    >>> do_calculate_fisher_information(_model, _p0, _data)
        array([[8.67337390e+05, 9.89376513e+01],
               [9.89376513e+01, 1.12858721e-02]])

    :param model: the model function, f(x, ...). This function must take the
        data set as the first argument.  The remaining arguments of the
        function should be the scale, shape, and location parameters.
    :param p0: point in parameter space where Fisher information matrix is
        evaluated.  Passed as a list in the same order as the parameter
        arguments to the model.  See the example above.
    :param data: the data set to use for calculating the information matrix.
    :param noise: squared variance of the noise in data.
    :returns: _fisher; the Fisher information matrix.
    :rtype: ndarray
    """
    _labels = inspect.getfullargspec(model)[0][1:]
    _p0dict = dict(zip(_labels, p0))

    _D = np.zeros((len(p0), data.size))

    for i, argname in enumerate(_labels):
        # pylint: disable=cell-var-from-loop
        _D[i, :] = [
            misc.derivative(
                lambda p: model(_record, **dict(_p0dict, **{argname: p})),
                _p0dict[argname],
                dx=1.0e-6) for _record in data
        ]

    _fisher = 1.0 / noise**2 * np.einsum('mk, nk', _D, _D)

    return _fisher
