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
from scipy.stats import lognorm


def get_hazard_rate(
    shape: float, time: float, location: float = 0.0, scale: float = 1.0
) -> float:
    """Calculates the hazard rate given a scale, shape, and location parameter.

    This function calculates the rate parameter given the scale, shape, time, and,
    optionally, a location parameter.

        >>> get_hazard_rate(0.9663, 4, scale=33.65)
        0.6610467490673426

        >>> get_hazard_rate(0.9663, 4, location=1.85, scale=33.65)
        1.5117773383839221

        >>> get_hazard_rate(0, 4, scale=33.65)
        nan

        >>> get_hazard_rate(0.9663, 0, scale=33.65)
        0.0

    The relationship to scipy parameters is:
        sigma = s
        mu = log(scale)

    :param scale: the value of the scale parameter.
    :param shape: the value of the shape parameter.
    :param time: the time at which to calculate the hazard rate.
    :param location: the value of the location parameter.
    :return: _hazard_rate; the hazard rate.
    :rtype: float
    """
    return (
        0.0
        if time <= 0.0
        else lognorm.pdf(time, shape, loc=location, scale=scale)
        / lognorm.cdf(time, shape, loc=location, scale=scale)
    )


def get_mtbf(shape: float, location: float = 0.0, scale: float = 1.0) -> float:
    """Calculate the MTBF given a shape (sigma) and scale (mu) parameter.

        >>> get_mtbf(0.9663, scale=33.65)
        53.671433807942236

        >>> get_mtbf(0.0, scale=33.65)
        nan

    :param shape: the shape parameter.
    :param location: the location parameter.
    :param scale: the scale parameter.
    :return: _mtbf; the MTBF.
    :rtype: float
    """
    return lognorm.mean(
        shape,
        loc=location,
        scale=scale,
    )


def get_survival(
    shape: float,
    time: float,
    location: float = 0.0,
    scale: float = 1.0,
) -> float:
    """Calculate value of the survival function at time given scale and location.

    This function returns the lower and upper alpha bounds as well as the point
    estimate of the survival function at time.

        >>> get_survival(0.9663, 5.0, scale=33.65)
        0.9757561

        >>> get_survival(0.9663, 5.0, location=1.85, scale=33.65)
        0.9928813

    :param scale: the point estimate of the scale parameter.
    :param time: the time at which to calculate the survival function.
    :param location: the point estimate of the location parameter.
    :return: _surv; the value of the survival function at time.
    :rtype: float
    """
    return lognorm.sf(time, shape, loc=location, scale=scale)


def do_fit(data, **kwargs) -> Tuple[float, float, float]:
    """Fits the provided data to the LOGN distribution and estimates scale and
    location.

    :param data: the data to use in the fit.
    :return: (_shape, _location, _scale); the estimated parameters.
    :rtype: tuple
    """
    _location = kwargs.get("location", 0.0)  # Initial guess for location.
    _floc = kwargs.get("floc", None)  # Value to fix location parameter.
    _scale = kwargs.get("scale", 0.0)  # Initial guess for scale.
    _method = kwargs.get("method", "MLE")  # One of MLE or MM.

    if _floc is None:
        if scipy.__version__ >= "1.7.1":
            _shape, _location, _scale = lognorm.fit(
                data,
                loc=_location,
                scale=_scale,
                method=_method,
            )
        else:
            _shape, _location, _scale = lognorm.fit(
                data,
                loc=_location,
                scale=_scale,
            )
    else:
        if scipy.__version__ >= "1.7.1":
            _shape, _location, _scale = lognorm.fit(
                data,
                loc=_location,
                scale=_scale,
                floc=_floc,
                method=_method,
            )
        else:
            _shape, _location, _scale = lognorm.fit(
                data,
                loc=_location,
                scale=_scale,
                floc=_floc,
            )

    return _shape, _location, _scale
