# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.statistics.lognormal_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the Exponential distribution module."""

# Standard Library Imports
import math

# Third Party Imports
import numpy as np
import pytest
import scipy

# RAMSTK Package Imports
from ramstk.analyses.statistics import lognormal


@pytest.fixture(scope="function")
def test_data():
    """Data set of 100 lognormally distributed points with a mean of 100.

    Data is the same as that used in the ReliaSoft wiki examples.  The table can be
    found at the following URL, for example.
    http://reliawiki.org/index.php/The_Lognormal_Distribution#Rank_Regression_on_Y

    mu = 3.516, sigma = 0.9663, and rho = 0.9754 when fit to the LNORM.
    """
    yield np.array(
        [
            5.0,
            10.0,
            15.0,
            20.0,
            25.0,
            30.0,
            35.0,
            40.0,
            50.0,
            60.0,
            70.0,
            80.0,
            90.0,
            100.0,
        ]
    )


@pytest.mark.unit
def test_get_hazard_rate_defaults():
    """should calculate the (LOGN) hazard rate when using default confidence level."""
    assert lognormal.get_hazard_rate(0.9663, 4.0, scale=33.65) == pytest.approx(
        0.6610467
    )


@pytest.mark.unit
def test_get_hazard_rate_specified_location():
    """should calculate the (LOGN) hazard rate when specifying the location."""
    assert lognormal.get_hazard_rate(
        0.9663, 4.0, location=1.85, scale=33.65
    ) == pytest.approx(1.5117773383839221)


@pytest.mark.unit
def test_get_hazard_rate_zero_shape():
    """should return nan when passed a shape=0.0."""
    assert math.isnan(lognormal.get_hazard_rate(0.0, 4.0, scale=33.65))


@pytest.mark.unit
def test_get_hazard_rate_zero_time():
    """should return zero when passed a time=0.0."""
    assert lognormal.get_hazard_rate(0.9663, 0.0, scale=33.65) == 0.0


@pytest.mark.unit
def test_get_mtbf_defaults():
    """should calculate the LOGN MTBF when using default confidence level."""
    assert lognormal.get_mtbf(0.9663, scale=33.65) == pytest.approx(53.6714338)


@pytest.mark.unit
def test_get_mtbf_specified_location():
    """should calculate the LOGN MTBF when specifying the location."""
    assert lognormal.get_mtbf(0.9663, scale=33.65, location=0.005) == pytest.approx(
        53.6764338
    )


@pytest.mark.unit
def test_get_mtbf_zero_shape():
    """should return nan when passed a shape=0.0."""
    assert math.isnan(lognormal.get_mtbf(0.0, scale=33.65))


@pytest.mark.unit
def test_get_survival_defaults():
    """should calculate the value of the survival function at time T."""
    assert lognormal.get_survival(0.9663, 5.0, scale=33.65) == pytest.approx(0.9757561)


@pytest.mark.unit
def test_get_survival_specified_location():
    """should calculate the value of the survival when specifying the location."""
    assert lognormal.get_survival(
        0.9663, 5.0, location=1.85, scale=33.65
    ) == pytest.approx(0.9928813)


@pytest.mark.unit
def test_get_survival_zero_scale():
    """should return nan when passed a scale=0.0."""
    assert math.isnan(lognormal.get_survival(0.9963, 5.0, scale=0.0))


@pytest.mark.unit
def test_do_fit_defaults(test_data):
    """should estimate the scale, shape, and location parameters for the data."""
    _shape, _location, _scale = lognormal.do_fit(test_data)

    assert _shape == pytest.approx(0.5313182)
    assert _location == pytest.approx(-14.7769535)
    assert _scale == pytest.approx(52.3254436)


@pytest.mark.unit
def test_do_fit_no_floc(test_data):
    """should estimate the scale and shape parameters for the data."""
    _shape, _location, _scale = lognormal.do_fit(test_data, floc=0.0)

    assert _shape == pytest.approx(0.849191)
    assert _location == 0.0
    assert _scale == pytest.approx(33.6446951)


@pytest.mark.unit
@pytest.mark.skipif(scipy.__version__ < "1.7.1", reason="requires scipy>=1.7.1")
def test_do_fit_mm_method(test_data):
    """should estimate the scale, shape, and location parameters using the MM
    method."""
    _shape, _location, _scale = lognormal.do_fit(test_data, method="MM")

    assert _shape == pytest.approx(0.370874430728507)
    assert _location == pytest.approx(-25.6268595)
    assert _scale == pytest.approx(66.4965744)


@pytest.mark.unit
@pytest.mark.skipif(scipy.__version__ < "1.7.1", reason="requires scipy>=1.7.1")
def test_do_fit_mm_method_no_floc(test_data):
    """should estimate the scale and shape parameters using the MM method."""
    _shape, _location, _scale = lognormal.do_fit(test_data, method="MM", floc=0.0)

    assert _shape == pytest.approx(0.599285)
    assert _location == 0.0
    assert _scale == pytest.approx(37.6032561)
