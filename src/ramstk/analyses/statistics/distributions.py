# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.statistics.distributions.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Exponential Module."""

# Standard Library Imports
from typing import Optional

# Third Party Imports
from scipy.stats import expon, lognorm, norm, weibull_min


def calculate_hazard_rate(
    time: float,
    location: float = 0.0,
    scale: Optional[float] = None,
    shape: Optional[float] = None,
    dist_type: str = "exponential",
) -> float:
    """Calculate the hazard rate for a given distribution."""
    if time <= 0.0:
        return 0.0

    # Exponential distribution doesn't use the `shape` parameter.
    if dist_type == "exponential":
        return 1.0 / expon.mean(loc=location, scale=scale)

    # Lognormal distribution uses `shape`, `location`, and `scale`.
    elif dist_type == "lognormal":
        return lognorm.pdf(time, shape, loc=location, scale=scale) / lognorm.cdf(
            time, shape, loc=location, scale=scale
        )

    # Normal distribution uses 'scale' and 'location'.
    elif dist_type == "normal":
        return norm.pdf(time, loc=location, scale=scale) / norm.sf(
            time, loc=location, scale=scale
        )

    # Weibull distribution uses `shape`, `location`, and `scale`.
    elif dist_type == "weibull":
        return (
            0.0
            if time <= 0.0
            else weibull_min.pdf(time, shape, loc=location, scale=scale)
            / weibull_min.cdf(time, shape, loc=location, scale=scale)
        )

    else:
        raise ValueError(f"Unsupported distribution: {dist_type}")


def calculate_mtbf(
    shape: float = None,
    location: float = 0.0,
    scale: float = 1.0,
    dist_type: str = "exponential",
) -> float:
    """Calculate the MTBF for a given distribution.

    :param shape: the shape parameter.
    :param location: the location parameter.
    :param scale: the scale (MTBF) parameter.
    :param dist_type: the type of distribution.
    :return: the MTBF value.
    :rtype: float
    """
    if dist_type == "exponential":
        return expon.mean(loc=location, scale=scale)
    elif dist_type == "lognormal":
        return lognorm.mean(shape, loc=location, scale=scale)
    elif dist_type == "normal":
        return norm.mean(loc=location, scale=scale)
    elif dist_type == "weibull":
        return weibull_min.mean(shape, loc=location, scale=scale)
    else:
        raise ValueError(f"Unsupported distribution type: {dist_type}")


def calculate_survival(
    shape: float = None,
    time: float = 0.0,
    location: float = 0.0,
    scale: float = 1.0,
    dist_type: str = "exponential",
) -> float:
    """Calculate the survival function at time T for a given distribution.

    :param shape: the shape parameter.
    :param time: the time at which to calculate the survival function.
    :param location: the location parameter.
    :param scale: the scale parameter.
    :param dist_type: the type of distribution.
    :return: the survival function value at time T.
    :rtype: float
    """
    if dist_type == "exponential":
        return expon.sf(time, loc=location, scale=scale)
    elif dist_type == "lognormal":
        return lognorm.sf(time, shape, loc=location, scale=scale)
    elif dist_type == "normal":
        return norm.sf(time, location, scale)
    elif dist_type == "weibull":
        return weibull_min.sf(time, shape, loc=location, scale=scale)
    else:
        raise ValueError(f"Unsupported distribution type: {dist_type}")
