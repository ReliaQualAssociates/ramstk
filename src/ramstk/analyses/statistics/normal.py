# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.statistics.lognormal.py is part of the RAMSTK Project
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


def get_hazard_rate(location: float, scale: float, time: float) -> float:
    """Calculate the hazard rate given a location and scale parameter.

    This function calculates the rate parameter given the scale, shape, time,
    and, optionally, a location parameter.

        >>> get_hazard_rate(100.0, 10.0, 85.0)
        0.013878975045885079

        >>> get_hazard_rate(0.0, 10.0, 85.0)
        0.8614595320165236

        >>> get_hazard_rate(100.0, 0.0, 85.0)
        0.0

    :param location: the value of the location (mu) parameter.
    :param scale: the value of the scale (sigma) parameter.
    :param time: the time at which to calculate the hazard rate.
    :return: _hazard_rate; the hazard rate.
    :rtype: float
    """
    return calculate_hazard_rate(
        time,
        location=location,
        scale=scale,
        dist_type="normal",
    )


def get_mtbf(location: float, scale: float) -> float:
    """Calculate the MTBF given a shape (sigma) and scale (mu) parameter.

        >>> get_mtbf(100.0, 10.0)
        100.0

        >>> get_mtbf(0.0, 10.0)
        0.0

        >>> get_mtbf(100.0, 0.0)
        nan

    :param location: the location parameter.
    :param scale: the scale parameter.
    :return: _mtbf; the MTBF.
    :rtype: float
    """
    return calculate_mtbf(
        location=location,
        scale=scale,
        dist_type="normal",
    )


def get_survival(
    location: float,
    scale: float,
    time: float,
) -> float:
    """Calculate value of the survival function at time given scale and location.

        >>> get_survival(100.0, 10.0, 85.0)
        0.9331927987311419

        >>> get_survival(0.0, 10.0, 85.0)
        9.47953482220325e-18

        >>> get_survival(100.0, 0.0, 85.0)
        0.9928813

    :param location: the point estimate of the location parameter.
    :param scale: the point estimate of the scale parameter.
    :param time: the time at which to calculate the survival function.
    :return: _surv; the value of the survival function at time.
    :rtype: float
    """
    return calculate_survival(
        time=time,
        location=location,
        scale=scale,
        dist_type="normal",
    )


def do_fit(data, **kwargs) -> Tuple[float, float]:
    """Fits the provided data to the EXP distribution and estimates scale and location.

    :param data: the data to use in the fit.
    :return: (_location, _scale); the estimated parameters.
    :rtype: tuple
    """
    _location = kwargs.get("location", 0.0)  # Initial guess for location.
    _floc = kwargs.get("floc")
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

    return scipy.stats.norm.fit(data, **_fit_args)
