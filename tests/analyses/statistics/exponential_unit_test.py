# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.statistics.exponential_unit_test.py is part of The RAMSTK Project
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
from ramstk.analyses.statistics import exponential


@pytest.fixture(scope="function")
def test_data():
    """Data set of 100 exponentially distributed points with a mean of 100."""
    yield np.array(
        [
            1.585,
            1.978,
            2.81,
            3.679,
            4.248,
            5.137,
            5.566,
            6.328,
            7.876,
            10.79,
            12.398,
            13.095,
            13.64,
            14.003,
            14.259,
            14.558,
            14.808,
            14.848,
            16.452,
            17.743,
            18.793,
            18.917,
            19.664,
            20.564,
            28.693,
            34.931,
            35.461,
            36.169,
            37.765,
            38.951,
            39.576,
            40.36,
            41.559,
            42.486,
            46.984,
            48.146,
            48.398,
            49.315,
            49.364,
            49.76,
            49.855,
            52.315,
            52.885,
            53.127,
            53.18,
            54.07,
            58.595,
            61.993,
            65.542,
            66.69,
            66.864,
            67.342,
            69.776,
            71.048,
            74.057,
            75.549,
            77.095,
            78.747,
            80.172,
            82.16,
            82.223,
            86.769,
            87.229,
            88.862,
            89.103,
            94.072,
            96.415,
            101.977,
            111.147,
            115.532,
            120.144,
            121.963,
            134.763,
            137.072,
            141.988,
            143.687,
            143.918,
            148.07,
            158.98,
            159.732,
            163.827,
            169.175,
            171.813,
            172.663,
            177.992,
            184.263,
            185.254,
            194.039,
            212.279,
            222.93,
            226.918,
            241.044,
            263.548,
            275.491,
            294.418,
            297.467,
            317.922,
            323.763,
            350.577,
            351.347,
        ]
    )


@pytest.mark.unit
def test_get_hazard_rate_defaults():
    """should calculate the (EXP) hazard rate when using default confidence level."""
    assert exponential.get_hazard_rate(1000.0) == 0.001


@pytest.mark.unit
def test_get_hazard_rate_specified_location():
    """should calculate the (EXP) hazard rate when specifying the location."""
    assert exponential.get_hazard_rate(1000.0, location=100.0) == pytest.approx(
        0.0009090909
    )


@pytest.mark.unit
def test_get_hazard_rate_zero_scale():
    """should return nan when passed a scale=0.0."""
    assert math.isnan(exponential.get_hazard_rate(0.0))


@pytest.mark.unit
def test_get_mtbf_defaults():
    """should calculate the EXP MTBF when using default confidence level."""
    assert exponential.get_mtbf(0.000362) == pytest.approx(2762.4309392)


@pytest.mark.unit
def test_get_mtbf_specified_location():
    """should calculate the EXP MTBF when specifying the location."""
    assert exponential.get_mtbf(0.0001, location=0.005) == pytest.approx(10000.005)


@pytest.mark.unit
def test_get_mtbf_zero_rate():
    """should return 0.0 when passed a rate=0.0."""
    assert exponential.get_mtbf(0.0) == 0.0


@pytest.mark.unit
def test_get_survival_defaults():
    """should calculate the value of the survival function at time T."""
    assert exponential.get_survival(10000.0, 4.0) == pytest.approx(0.9996001)


@pytest.mark.unit
def test_get_survival_specified_location():
    """should calculate the value of the survival when specifying the location."""
    assert exponential.get_survival(10000.0, 4.0, location=1.0) == pytest.approx(
        0.9997000
    )


@pytest.mark.unit
def test_get_survival_zero_scale():
    """should return nan when passed a scale=0.0."""
    assert math.isnan(exponential.get_survival(0.0, 4.0))


@pytest.mark.unit
def test_fit_defaults(test_data):
    """should estimate the scale parameter for the data using default input values."""
    _location, _scale = exponential.do_fit(test_data)

    assert _location == 1.585
    assert _scale == pytest.approx(92.54595)


@pytest.mark.unit
def test_fit_no_floc(test_data):
    """should estimate the scale and location parameter for the data."""
    _location, _scale = exponential.do_fit(test_data, floc=0.0)

    assert _location == 0.0
    assert _scale == pytest.approx(94.13095)


@pytest.mark.unit
def test_fit_mm_method(test_data):
    """should estimate the scale parameter using the MM method."""
    _location, _scale = exponential.do_fit(test_data, method="MM")

    assert _location == pytest.approx(7.1563288)
    assert _scale == pytest.approx(86.9746313)


@pytest.mark.unit
def test_fit_mm_method_no_floc(test_data):
    """should estimate the scale parameter using the MM method."""
    _location, _scale = exponential.do_fit(test_data, method="MM", floc=0.0)

    assert _location == 0.0
    assert _scale == pytest.approx(94.1309375)
