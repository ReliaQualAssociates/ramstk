# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.test_dormancy.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the dormancy analysis module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses import Dormancy


@pytest.mark.unit
@pytest.mark.calculation
def test_dormant_hazard_rate():
    """do_calculate_dormant_hazard_rate() should return a float value for the dormant hazard rate on success."""
    _hr_dormant = Dormancy.do_calculate_dormant_hazard_rate(4, 5, 3, 2, 0.008642374)

    assert pytest.approx(_hr_dormant, 0.0008642374)


@pytest.mark.unit
@pytest.mark.calculation
def test_dormant_hazard_rate_bad_index():
    """do_calculate_dormant_hazard_rate() should raise an index error when a bad index value is passed."""
    with pytest.raises(IndexError):
        _hr_dormant = Dormancy.do_calculate_dormant_hazard_rate(4, 5, 3, 12, 0.008642374)
