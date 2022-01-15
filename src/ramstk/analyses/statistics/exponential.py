# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.statistics.exponential.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Exponential Module."""

# Standard Library Imports
from typing import Tuple

# Third Party Imports
import scipy
from scipy.stats import expon


def get_hazard_rate(scale: float, location: float = 0.0) -> float:
    """Calculates the hazard rate given a scale and location parameter.

    This function calculates the rate parameter (lambda) given the scale (MTBF)
    and, optionally, a location parameter.

        >>> get_hazard_rate(10000.0)
        0.0001

        >>> get_hazard_rate(0.0)
        nan

    :param scale: the scale (MTBF) parameter.
    :param location: the location parameter.
    :return: _hazard_rate; the hazard rate.
    :rtype: float
    """
    return 1.0 / expon.mean(
        loc=location,
        scale=scale,
    )


def get_mtbf(rate: float, location: float = 0.0) -> float:
    """Calculate the MTBF (scale) given a hazard rate (lambda) and location parameter.

        >>> get_mtbf(0.0008691)
        1150.6155793349442

        >>> get_mtbf(0.0)
        0.0

    :param rate: the rate (lambda) parameter.
    :param location: the location parameter.
    :return: _mtbf; the MTBF.
    :rtype: float
    """
    try:
        _mtbf = expon.mean(
            loc=location,
            scale=1.0 / rate,
        )
    except ZeroDivisionError:
        _mtbf = 0.0

    return _mtbf


def get_survival(scale: float, time: float, location: float = 0.0) -> float:
    """Calculate value of the survival function at time given scale and location.

    This function returns the lower and upper alpha bounds as well as the point
    estimate of the survival function at time.

        >>> get_survival(10000.0, 4.0)
        0.9996000799893344

        >>> get_survival(10000.0, 4.0, location=1.0)
        0.9997000449955004

    :param scale: the point estimate of the scale parameter.
    :param time: the time at which to calculate the survival function.
    :param location: the point estimate of the location parameter.
    :return: _surv; the value of the survival function at time.
    :rtype: float
    """
    return expon.sf(time, loc=location, scale=scale)


def do_fit(data, **kwargs) -> Tuple[float, float]:
    """Fits the provided data to the EXP distribution and estimates scale and location.

    :param data: the data to use in the fit.
    :return: (_location, _scale); the estimated parameters.
    :rtype: tuple
    """
    _location = kwargs.get("location", 0.0)  # Initial guess for location.
    _floc = kwargs.get("floc", None)  # Value to fix location parameter.
    _scale = kwargs.get("scale", 0.0)  # Initial guess for scale.
    _method = kwargs.get("method", "MLE")  # One of MLE or MM.

    # method is not an argument to fit() until scipy-1.7.1.
    if _floc is None:
        if scipy.__version__ >= "1.7.1":
            _location, _scale = expon.fit(
                data,
                loc=_location,
                scale=_scale,
                method=_method,
            )
        else:
            _location, _scale = expon.fit(
                data,
                loc=_location,
                scale=_scale,
            )
    else:
        if scipy.__version__ >= "1.7.1":
            _location, _scale = expon.fit(
                data,
                loc=_location,
                floc=_floc,
                scale=_scale,
                method=_method,
            )
        else:
            _location, _scale = expon.fit(
                data,
                loc=_location,
                floc=_floc,
                scale=_scale,
            )

    return _location, _scale
