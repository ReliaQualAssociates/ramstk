# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.statistics.normal_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the Exponential distribution module."""

# Standard Library Imports
import math

# Third Party Imports
import numpy as np
import pytest

# RAMSTK Package Imports
from ramstk.analyses.statistics import normal


@pytest.fixture(scope="function")
def test_data():
    """Data set of 100 normally distributed points with mean=100 and variance=10.0."""
    yield np.array(
        [
            95.370,
            114.011,
            113.246,
            109.167,
            104.227,
            107.109,
            117.43215,
            94.785,
            83.56718,
            103.501,
            89.931,
            120.455,
            97.081,
            96.813,
            97.571,
            106.757,
            99.335,
            104.538,
            102.028,
            90.032,
            77.542,
            102.761,
            82.485,
            77.743,
            109.974,
            94.851,
            89.771,
            98.193,
            102.165,
            96.783,
            108.865,
            120.462,
            111.592,
            106.148,
            102.946,
            111.290,
            106.002,
            114.617,
            88.229,
            131.364,
            86.855,
            109.927,
            75.116,
            100.465,
            97.783,
            108.169,
            98.851,
            99.310,
            94.588,
            98.123,
            115.666,
            104.491,
            93.490,
            111.794,
            114.320,
            106.938,
            106.450,
            103.105,
            107.781,
            120.846,
            100.102,
            92.930,
            101.246,
            69.517,
            106.276,
            99.046,
            101.300,
            98.588,
            110.022,
            91.255,
            106.687,
            102.443,
            100.342,
            96.635,
            80.909,
            111.080,
            107.005,
            103.043,
            92.660,
            81.526,
            94.497,
            88.791,
            97.913,
            96.120,
            101.234,
            95.132,
            93.939,
            92.302,
            96.536,
            110.747,
            99.888,
            92.780,
            107.678,
            96.187,
            87.938,
            91.664,
            106.149,
            104.320,
            115.681,
            95.920,
        ]
    )


@pytest.mark.unit
def test_get_hazard_rate_defaults():
    """should calculate the (NORM) hazard rate when using default confidence level."""
    assert normal.get_hazard_rate(100.0, 10.0, 85.0) == pytest.approx(0.01387898)


@pytest.mark.unit
def test_get_hazard_rate_zero_location():
    """should return nan when passed a location=0.0."""
    assert normal.get_hazard_rate(0.0, 10.0, 85.0) == pytest.approx(0.8614595)


@pytest.mark.unit
def test_get_hazard_rate_zero_scale():
    """should return nan when passed a scale=0.0."""
    assert math.isnan(normal.get_hazard_rate(100.0, 0.0, 85.0))


@pytest.mark.unit
def test_get_hazard_rate_zero_time():
    """should return zero when passed a time=0.0."""
    assert normal.get_hazard_rate(100.0, 10.0, 0.0) == pytest.approx(0.0)


@pytest.mark.unit
def test_get_mtbf_defaults():
    """should calculate the NORM MTBF when using default confidence level."""
    assert normal.get_mtbf(100.0, 10.0) == 100.0


@pytest.mark.unit
def test_get_mtbf_zero_location():
    """should calculate the NORM MTBF when passed location=0.0."""
    assert normal.get_mtbf(0.0, 10.0) == 0.0


@pytest.mark.unit
def test_get_mtbf_zero_scale():
    """should return nan when passed a scale=0.0."""
    assert math.isnan(normal.get_mtbf(100.0, 0.0))


@pytest.mark.unit
def test_get_survival_defaults():
    """should calculate the value of the survival function at time T."""
    assert normal.get_survival(100.0, 10.0, 85.0) == pytest.approx(0.9331928)


@pytest.mark.unit
def test_get_survival_zero_location():
    """should calculate the value of the survival function when passed location=0.0."""
    assert normal.get_survival(0.0, 10.0, 85.0) == pytest.approx(9.4795348e-18)


@pytest.mark.unit
def test_get_survival_zero_scale():
    """should return nan when passed a scale=0.0."""
    assert math.isnan(normal.get_survival(100.0, 0.0, 85.0))


@pytest.mark.unit
def test_do_fit_defaults(test_data):
    """should estimate the scale, shape, and location parameters for the data."""
    _location, _scale = normal.do_fit(test_data)

    assert _location == pytest.approx(100.5283533)
    assert _scale == pytest.approx(10.544214)


@pytest.mark.unit
def test_do_fit_no_floc(test_data):
    """should estimate the scale and shape parameters for the data."""
    _location, _scale = normal.do_fit(test_data, floc=0.0)

    assert _location == 0.0
    assert _scale == pytest.approx(101.0798213)


@pytest.mark.unit
def test_do_fit_mm_method(test_data):
    """should estimate the scale, shape, and location parameters using the MM
    method."""
    _location, _scale = normal.do_fit(test_data, method="MM")

    assert _location == pytest.approx(100.528356)
    assert _scale == pytest.approx(10.5441855)


@pytest.mark.unit
def test_do_fit_mm_method_no_floc(test_data):
    """should estimate the scale and shape parameters using the MM method."""
    _location, _scale = normal.do_fit(test_data, method="MM", floc=0.0)

    assert _location == 0.0
    assert _scale == 0.00025
