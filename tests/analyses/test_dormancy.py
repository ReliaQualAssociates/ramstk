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
@pytest.mark.parametrize("category_id", [1, 2])
@pytest.mark.parametrize("subcategory_id", [1, 3])
def test_dormant_hazard_rate(category_id, subcategory_id):
    """do_calculate_dormant_hazard_rate() should return a float value for the dormant hazard rate on success."""
    _hr_dormant = Dormancy.do_calculate_dormant_hazard_rate(
        category_id, subcategory_id, 3, 2, 0.008642374)

    assert isinstance(_hr_dormant, float)
    assert _hr_dormant == pytest.approx({
        1: [0.00069138992, 0.00034569496],
        3: [0.00069138992, 0.0004321187]
    }[subcategory_id][category_id - 1])


@pytest.mark.unit
@pytest.mark.calculation
def test_dormant_hazard_rate_bad_index():
    """do_calculate_dormant_hazard_rate() should raise an IndexError when a bad index value is passed."""
    with pytest.raises(IndexError):
        _hr_dormant = Dormancy.do_calculate_dormant_hazard_rate(
            4, 5, 3, 12, 0.008642374)
