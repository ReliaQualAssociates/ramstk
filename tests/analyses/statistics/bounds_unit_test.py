# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.statistics.test_bounds.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing statistical bound algorithms and models."""

# Third Party Imports
import numpy as np
import pytest
from scipy.stats import expon

# RAMSTK Package Imports
from ramstk.analyses.statistics.bounds import (
    do_calculate_beta_bounds,
    do_calculate_fisher_information,
)


def log_pdf(data, theta, loc=0.0):
    """Calculate the logarithm of the exponential pdf."""
    return np.log(theta) - theta * (data - loc)


class TestBetaBounds:
    """Class for beta bounds test suite."""

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_calculate_beta_bounds_fractional_alpha(self):
        """do_calculate_beta_bounds() should return a tuple of mean, standard
        error, and bounds on success when passed an alpha < 1.0."""
        _meanll, _mean, _meanul, _sd = do_calculate_beta_bounds(10.0, 20.0, 40.0, 0.95)

        assert _meanll == pytest.approx(11.86684674)
        assert _mean == pytest.approx(21.66666666)
        assert _meanul == pytest.approx(31.46648659)
        assert _sd == pytest.approx(5.0)

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_calculate_beta_bounds_whole_alpha(self):
        """do_calculate_beta_bounds() should return a tuple of mean, standard
        error, and bounds on success when passed an alpha > 1.0."""
        _meanll, _mean, _meanul, _sd = do_calculate_beta_bounds(10.0, 20.0, 40.0, 95.0)

        assert _meanll == pytest.approx(11.86684674)
        assert _mean == pytest.approx(21.66666666)
        assert _meanul == pytest.approx(31.46648659)
        assert _sd == pytest.approx(5.0)


class TestFisherInformation:
    """Class for Fisher information matrix test suite."""

    EXP_TEST = np.array(
        [
            [0.0, 1.585, 1, 1, 1.585],
            [0.0, 1.978, 1, 1, 1.978],
            [0.0, 2.81, 1, 1, 2.81],
            [0.0, 3.679, 1, 1, 3.679],
            [0.0, 4.248, 1, 1, 4.248],
            [0.0, 5.137, 1, 1, 5.137],
            [0.0, 5.566, 1, 1, 5.566],
            [0.0, 6.328, 1, 1, 6.328],
            [0.0, 7.876, 1, 1, 7.876],
            [0.0, 10.79, 1, 1, 10.79],
            [0.0, 12.398, 1, 1, 12.398],
            [0.0, 13.095, 1, 1, 13.095],
            [0.0, 13.64, 1, 1, 13.64],
            [0.0, 14.003, 1, 1, 14.003],
            [0.0, 14.259, 1, 1, 14.259],
            [0.0, 14.558, 1, 1, 14.558],
            [0.0, 14.808, 1, 1, 14.808],
            [0.0, 14.848, 1, 1, 14.848],
            [0.0, 16.452, 1, 1, 16.452],
            [0.0, 17.743, 1, 1, 17.743],
            [0.0, 18.793, 1, 1, 18.793],
            [0.0, 18.917, 1, 1, 18.917],
            [0.0, 19.664, 1, 1, 19.664],
            [0.0, 20.564, 1, 1, 20.564],
            [0.0, 28.693, 1, 1, 28.693],
            [0.0, 34.931, 1, 1, 34.931],
            [0.0, 35.461, 1, 1, 35.461],
            [0.0, 36.169, 1, 1, 36.169],
            [0.0, 37.765, 1, 1, 37.367],
            [0.0, 38.951, 1, 1, 38.951],
            [0.0, 39.576, 1, 1, 39.576],
            [0.0, 40.36, 1, 1, 40.36],
            [0.0, 41.559, 1, 1, 41.559],
            [0.0, 42.486, 1, 1, 42.486],
            [0.0, 46.984, 1, 1, 46.984],
            [0.0, 48.146, 1, 1, 48.146],
            [0.0, 48.398, 1, 1, 48.398],
            [0.0, 49.315, 1, 1, 49.315],
            [0.0, 49.364, 1, 1, 49.364],
            [0.0, 49.76, 1, 1, 49.76],
            [0.0, 49.855, 1, 1, 49.855],
            [0.0, 52.315, 1, 1, 52.315],
            [0.0, 52.885, 1, 1, 52.885],
            [0.0, 53.127, 1, 1, 53.127],
            [0.0, 53.18, 1, 1, 53.18],
            [0.0, 54.07, 1, 1, 54.07],
            [0.0, 58.595, 1, 1, 58.595],
            [0.0, 61.993, 1, 1, 61.993],
            [0.0, 65.542, 1, 1, 65.542],
            [0.0, 66.69, 1, 1, 66.69],
            [0.0, 66.864, 1, 1, 66.864],
            [0.0, 67.342, 1, 1, 67.342],
            [0.0, 69.776, 1, 1, 69.776],
            [0.0, 71.048, 1, 1, 71.048],
            [0.0, 74.057, 1, 1, 74.057],
            [0.0, 75.549, 1, 1, 75.549],
            [0.0, 77.095, 1, 1, 77.095],
            [0.0, 78.747, 1, 1, 78.747],
            [0.0, 80.172, 1, 1, 80.172],
            [0.0, 82.16, 1, 1, 82.16],
            [0.0, 82.223, 1, 1, 82.223],
            [0.0, 86.769, 1, 1, 86.769],
            [0.0, 87.229, 1, 1, 87.229],
            [0.0, 88.862, 1, 1, 88.862],
            [0.0, 89.103, 1, 1, 89.103],
            [0.0, 94.072, 1, 1, 94.072],
            [0.0, 96.415, 1, 1, 96.415],
            [0.0, 101.977, 1, 1, 101.977],
            [0.0, 111.147, 1, 1, 111.147],
            [0.0, 115.532, 1, 1, 115.532],
            [0.0, 120.144, 1, 1, 120.144],
            [0.0, 121.963, 1, 1, 121.963],
            [0.0, 134.763, 1, 1, 134.763],
            [0.0, 137.072, 1, 1, 137.072],
            [0.0, 141.988, 1, 1, 141.988],
            [0.0, 143.687, 1, 1, 143.687],
            [0.0, 143.918, 1, 1, 143.918],
            [0.0, 148.07, 1, 1, 148.07],
            [0.0, 158.98, 1, 1, 158.98],
            [0.0, 159.732, 1, 1, 159.732],
            [0.0, 163.827, 1, 1, 163.827],
            [0.0, 169.175, 1, 1, 169.175],
            [0.0, 171.813, 1, 1, 171.813],
            [0.0, 172.663, 1, 1, 172.663],
            [0.0, 177.992, 1, 1, 177.992],
            [0.0, 184.263, 1, 1, 184.263],
            [0.0, 185.254, 1, 1, 185.254],
            [0.0, 194.039, 1, 1, 194.039],
            [0.0, 212.279, 1, 1, 212.279],
            [0.0, 222.93, 1, 1, 222.93],
            [0.0, 226.918, 1, 1, 226.918],
            [0.0, 241.044, 1, 1, 241.044],
            [0.0, 263.548, 1, 1, 263.548],
            [0.0, 275.491, 1, 1, 275.491],
            [0.0, 294.418, 1, 1, 294.418],
            [0.0, 297.467, 1, 1, 297.467],
            [0.0, 317.922, 1, 1, 317.922],
            [0.0, 323.763, 1, 1, 323.763],
            [0.0, 350.577, 1, 1, 350.577],
            [0.0, 351.347, 1, 1, 351.347],
        ]
    )

    @pytest.mark.skip
    def test_calculate_fisher_information(self):
        """do_calculate_fisher_information() should return a list of lists on
        success."""
        _p0 = [0.010623498434893014, 0.0]
        _fisher = do_calculate_fisher_information(log_pdf, _p0, self.EXP_TEST[:, 1])

        assert _fisher[0][0] == pytest.approx(7.56458685e05)
        assert _fisher[0][1] == pytest.approx(5.16408922e-07)
        assert _fisher[1][0] == pytest.approx(5.16408922e-07)
        assert _fisher[1][1] == pytest.approx(1.12858719e-02)
