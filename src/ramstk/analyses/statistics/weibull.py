# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.statistics.weibull.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Exponential Module."""

# Standard Library Imports
from typing import Tuple

# Third Party Imports
import scipy

# RAMSTK Local Imports
from .distributions import calculate_hazard_rate, calculate_mtbf, calculate_survival


def get_hazard_rate(
    shape: float, scale: float, time: float, location: float = 0.0
) -> float:
    """Calculate the hazard rate given a scale, shape, and location parameter.

    This function calculates the rate parameter given the scale, shape, time,
    and, optionally, a location parameter.

        >>> get_hazard_rate(2.5, 525.0, 105.0)
        0.02359719987177253

        >>> get_hazard_rate(2.5, 525.0, 105.0, location=18.5)
        0.028742792496007755

        >>> get_hazard_rate(0.0, 525.0, 105.0)
        nan

        >>> get_hazard_rate(2.5, 0.0, 105.0)
        0.0

        >>> get_hazard_rate(2.5, 525.0, 0.0)
        0.0

    The relationship to scipy parameters is:
        beta = shape
        eta = scale
        gamma = location

    :param scale: the value of the scale parameter.
    :param shape: the value of the shape parameter.
    :param time: the time at which to calculate the hazard rate.
    :param location: the value of the location parameter.
    :return: _hazard_rate; the hazard rate.
    :rtype: float
    """
    return calculate_hazard_rate(
        time=time,
        location=location,
        scale=scale,
        shape=shape,
        dist_type="weibull",
    )


def get_mtbf(shape: float, scale: float, location: float = 0.0) -> float:
    """Calculate the MTBF given a shape (sigma) and scale (mu) parameter.

        >>> get_mtbf(2.5, 525.0)
        465.8135041891145

        >>> get_mtbf(2.5, 525.0, location=18.5)
        484.3135041891145

        >>> get_mtbf(0.0, 525.0)
        nan

        >>> get_mtbf(2.5, 0.0)
        nan

    :param shape: the shape parameter.
    :param scale: the scale parameter.
    :param location: the location parameter.
    :return: _mtbf; the MTBF.
    :rtype: float
    """
    return calculate_mtbf(
        shape=shape,
        location=location,
        scale=scale,
        dist_type="weibull",
    )


def get_survival(
    shape: float,
    scale: float,
    time: float,
    location: float = 0.0,
) -> float:
    """Calculate value of the survival function at time given scale and location.

    This function returns the lower and upper alpha bounds as well as the point
    estimate of the survival function at time.

        >>> get_survival(2.5, 525.0, 105.0)
        0.9822705063757785

        >>> get_survival(2.5, 525.0, 105.0, location=18.5)
        0.9890414911478198

    :param scale: the point estimate of the scale parameter.
    :param time: the time at which to calculate the survival function.
    :param location: the point estimate of the location parameter.
    :return: _surv; the value of the survival function at time.
    :rtype: float
    """
    return calculate_survival(
        time=time,
        shape=shape,
        location=location,
        scale=scale,
        dist_type="weibull",
    )


def do_fit(data, **kwargs) -> Tuple[float, float, float]:
    """Fits the provided data to the WEI distribution and estimates scale and location.

    :param data: the data to use in the fit.
    :return: (_shape, _location, _scale); the estimated parameters.
    :rtype: tuple
    """
    _location = kwargs.get("location", 0.0)  # Initial guess for location.
    _floc = kwargs.get("floc", None)  # Value to fix location parameter.
    _scale = kwargs.get("scale", 0.0)  # Initial guess for scale.
    _method = kwargs.get("method", "MLE")  # One of MLE or MM.

    if data.size == 0:
        raise ValueError("No data provided to perform fit.")

    # method is not an argument to fit() until scipy-1.7.1.
    if scipy.__version__ >= "1.7.1":
        _fit_args = {"loc": _location, "scale": _scale, "method": _method}
    else:
        _fit_args = {"loc": _location, "scale": _scale}

    if _floc is not None:
        _fit_args["floc"] = _floc

    return scipy.stats.weibull_min.fit(
        data,
        **_fit_args,
    )
