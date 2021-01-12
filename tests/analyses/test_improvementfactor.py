# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.test_improvementfactor.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the improvement factor module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses import improvementfactor


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_improvementfactor():
    """calculate_improvement() should return a tuple of improvement factor and weight."""
    _improvement, _weight = improvementfactor.calculate_improvement(3, 2, 4, user_float_1=2.6)

    assert _improvement == 1.2
    assert _weight == 12.48
