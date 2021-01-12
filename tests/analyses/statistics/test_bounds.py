# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.statistics.test_bounds.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing statistical bound algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.statistics.bounds import do_calculate_beta_bounds


class TestBetaBounds():
    """Class for beta bounds test suite."""
    @pytest.mark.unit
    @pytest.mark.calculation
    def test_calculate_beta_bounds_fractional_alpha(self):
        """do_calculate_beta_bounds() should return a tuple of mean, standard error, and bounds on success when passed an alpha < 1.0."""
        _meanll, _mean, _meanul, _sd = do_calculate_beta_bounds(10.0, 20.0, 40.0, 0.95)

        assert _meanll == pytest.approx(11.86684674)
        assert _mean == pytest.approx(21.66666666)
        assert _meanul == pytest.approx(31.46648659)
        assert _sd == pytest.approx(5.0)

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_calculate_beta_bounds_whole_alpha(self):
        """do_calculate_beta_bounds() should return a tuple of mean, standard error, and bounds on success when passed an alpha > 1.0."""
        _meanll, _mean, _meanul, _sd = do_calculate_beta_bounds(10.0, 20.0, 40.0, 95.0)

        assert _meanll == pytest.approx(11.86684674)
        assert _mean == pytest.approx(21.66666666)
        assert _meanul == pytest.approx(31.46648659)
        assert _sd == pytest.approx(5.0)
