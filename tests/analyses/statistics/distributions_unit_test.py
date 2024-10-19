# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.statistics.distributions_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the Exponential distribution module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.statistics import distributions


@pytest.mark.unit
def test_calculate_hazard_rate_invalid_distribution():
    """Should raise a ValueError when an unsupported distribution type is provided."""
    with pytest.raises(ValueError):
        distributions.calculate_hazard_rate(100.0, dist_type="unsupported")


@pytest.mark.unit
def test_calculate_mtbf_invalid_distribution():
    """Should raise a ValueError when an unsupported distribution type is provided."""
    with pytest.raises(ValueError):
        distributions.calculate_mtbf(dist_type="unsupported")


@pytest.mark.unit
def test_calculate_survival_invalid_distribution():
    """Should raise a ValueError when an unsupported distribution type is provided."""
    with pytest.raises(ValueError):
        distributions.calculate_survival(time=1000.0, dist_type="unsupported")
