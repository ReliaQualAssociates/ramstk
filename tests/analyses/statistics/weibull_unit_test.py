# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.statistics.weibull_unit_test.py is part of The RAMSTK Project
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
from ramstk.analyses.statistics import weibull


@pytest.fixture(scope="function")
def test_data():
    """Data set of Weibull distributed points.

    Data is the same as that used in the ReliaSoft wiki examples.
    The table can be found at the following URL, for example.
    http://reliawiki.org/index.php/The_Weibull_Distribution#Rank_Regression_on_Y

    eta = 76.318 and beta = 1.4301 when fit to the WEI.
    """
    yield np.array(
        [
            16.0,
            34.0,
            53.0,
            75.0,
            93.0,
            120.0,
        ]
    )


@pytest.mark.unit
def test_get_hazard_rate_defaults():
    """should calculate the (WEI) hazard rate when using default confidence level."""
    assert weibull.get_hazard_rate(0.8, 525.0, 105.0) == pytest.approx(0.006616111)
    assert weibull.get_hazard_rate(1.0, 525.0, 105.0) == pytest.approx(0.008603153)
    assert weibull.get_hazard_rate(2.5, 525.0, 105.0) == pytest.approx(0.0235972)


@pytest.mark.unit
def test_get_hazard_rate_specified_location():
    """should calculate the (WEI) hazard rate when specifying the location."""
    assert weibull.get_hazard_rate(0.8, 525.0, 105.0, location=18.5) == pytest.approx(
        0.008198783
    )
    assert weibull.get_hazard_rate(1.0, 525.0, 105.0, location=18.5) == pytest.approx(
        0.01063445
    )
    assert weibull.get_hazard_rate(2.5, 525.0, 105.0, location=18.5) == pytest.approx(
        0.02874279
    )


@pytest.mark.unit
def test_get_hazard_rate_zero_shape():
    """should return nan when passed a shape=0.0."""
    assert math.isnan(weibull.get_hazard_rate(0.0, 525.0, 105.0))


@pytest.mark.unit
def test_get_hazard_rate_zero_scale():
    """should return nan when passed a scale=0.0."""
    assert math.isnan(weibull.get_hazard_rate(2.5, 0.0, 105.0))


@pytest.mark.unit
def test_get_hazard_rate_zero_time():
    """should return zero when passed a time=0.0."""
    assert weibull.get_hazard_rate(2.5, 525.0, 0.0) == 0.0


@pytest.mark.unit
def test_get_mtbf_defaults():
    """should calculate the WEI MTBF when using default confidence level."""
    assert weibull.get_mtbf(2.5, 525.0) == pytest.approx(465.8135042)


@pytest.mark.unit
def test_get_mtbf_specified_location():
    """should calculate the WEI MTBF when specifying the location."""
    assert weibull.get_mtbf(2.5, 525.0, location=18.5) == pytest.approx(484.3135042)


@pytest.mark.unit
def test_get_mtbf_zero_shape():
    """should return nan when passed a shape=0.0."""
    assert math.isnan(weibull.get_mtbf(0.0, 525.0))


@pytest.mark.unit
def test_get_mtbf_zero_scale():
    """should return nan when passed a shape=0.0."""
    assert math.isnan(weibull.get_mtbf(2.5, 0.0))


@pytest.mark.unit
def test_get_survival_defaults():
    """should calculate the value of the survival function at time T."""
    assert weibull.get_survival(2.5, 525.0, 105.0) == pytest.approx(0.9822705)


@pytest.mark.unit
def test_get_survival_specified_location():
    """should calculate the value of the survival when specifying the location."""
    assert weibull.get_survival(2.5, 525.0, 105.0, location=18.5) == pytest.approx(
        0.9890415
    )


@pytest.mark.unit
def test_get_survival_zero_shape():
    """should return 1.0 when passed a shape=0.0."""
    assert math.isnan(weibull.get_survival(0.0, 525.0, 105.0))


@pytest.mark.unit
def test_get_survival_zero_scale():
    """should return nan when passed a scale=0.0."""
    assert math.isnan(weibull.get_survival(2.5, 0.0, 105.0))


@pytest.mark.unit
def test_get_survival_zero_time():
    """should return nan when passed a time=0.0."""
    assert weibull.get_survival(2.5, 525.0, 0.0) == 1.0


@pytest.mark.unit
def test_do_fit_defaults(test_data):
    """should estimate the scale, shape, and location parameters for the data."""
    _shape, _location, _scale = weibull.do_fit(test_data)

    assert _shape == pytest.approx(0.3982693)
    assert _location == pytest.approx(16.0)
    assert _scale == pytest.approx(9.7800320)


@pytest.mark.unit
def test_do_fit_no_floc(test_data):
    """should estimate the scale and shape parameters for the data."""
    _shape, _location, _scale = weibull.do_fit(test_data, floc=0.0)

    assert _shape == pytest.approx(1.9326793)
    assert _location == 0.0
    assert _scale == pytest.approx(73.5260822)


@pytest.mark.unit
@pytest.mark.skipif(scipy.__version__ < "1.7.1", reason="requires scipy>=1.7.1")
def test_do_fit_mm_method(test_data):
    """should estimate the scale, shape, and location parameters using the MM
    method."""
    _shape, _location, _scale = weibull.do_fit(test_data, method="MM")

    assert _shape == pytest.approx(0.1891056)
    assert _location == pytest.approx(0.002784309)
    assert _scale == pytest.approx(0.003346282)


@pytest.mark.unit
@pytest.mark.skipif(scipy.__version__ < "1.7.1", reason="requires scipy>=1.7.1")
def test_do_fit_mm_method_no_floc(test_data):
    """should estimate the scale and shape parameters using the MM method."""
    _shape, _location, _scale = weibull.do_fit(test_data, method="MM", floc=0.0)

    assert _shape == pytest.approx(0.166558)
    assert _location == 0.0
    assert _scale == pytest.approx(0.00337509)
