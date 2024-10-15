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
from scipy import misc, stats


def do_calculate_beta_bounds(
    minimum: float, likely: float, maximum: float, alpha: float
) -> Tuple[float, float, float, float]:
    """Calculate the mean, standard error, and bounds of the beta distribution.

    These are the project management estimators, not exact calculations.

    :param minimum: The minimum expected value.
    :param likely: The most likely value.
    :param maximum: The maximum expected value.
    :param alpha: The desired confidence level (0 < alpha < 1).
    :return: A tuple containing the lower mean bound, mean, upper mean bound, and
        standard deviation.
    :rtype: Tuple[float, float, float, float]
    """
    if alpha < 0.0 or alpha > 100.0:
        raise ValueError(
            f"Confidence level (alpha) must be between 0 and 100.  alpha: {alpha}"
        )

    _z_norm = (
        stats.norm.ppf(1.0 - ((1.0 - alpha / 100.0) / 2.0))
        if alpha > 1.0
        else 1.0 - ((1.0 - alpha) / 2.0)
    )

    _mean = (minimum + 4.0 * likely + maximum) / 6.0
    _sd = (maximum - minimum) / 6.0

    _mean_lower_bound = _mean - _z_norm * _sd
    _mean_upper_bound = _mean + _z_norm * _sd

    return _mean_lower_bound, _mean, _mean_upper_bound, _sd


def do_calculate_fisher_information(
    model: Callable, p0: List[float], data: np.ndarray, noise=1.0
) -> np.ndarray:
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

    :param model: The model function f(x, ...), which takes the data set
                  as the first argument. Remaining arguments should be the
                  scale, shape, and location parameters.
    :param p0: The point in parameter space where the Fisher information
                matrix is evaluated. Passed as a list in the same order
                as the model's parameter arguments.
    :param data: The data set used for calculating the information matrix.
    :param noise: The squared variance of the noise in data (default is 1.0).
    :return: The Fisher information matrix.
    :rtype: np.ndarray
    """
    if not isinstance(data, np.ndarray):
        raise TypeError(
            f"Expected data to be of type numpy.ndarray, got {type(data)} instead."
        )

    # Get the parameter names from the model's signature
    _param_labels = inspect.getfullargspec(model)[0][1:]  # Skip the first arg (data)
    _param_dict = dict(zip(_param_labels, p0))  # Create a dictionary of parameters

    # Initialize the derivative matrix
    _num_params = len(p0)
    _num_data_points = data.shape[0]
    _D = np.zeros((_num_params, _num_data_points))

    # Calculate the derivatives for each parameter
    for i, _param_name in enumerate(_param_labels):
        for j, _record in enumerate(data):
            # Define a lambda function to evaluate the model at the current parameter
            _D[i, j] = misc.derivative(
                lambda p: model(_record, **{**_param_dict, _param_name: p}),
                _param_dict[_param_name],
                dx=1.0e-6,
            )

    return 1.0 / noise**2 * np.dot(_D, _D.T)
