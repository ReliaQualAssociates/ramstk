# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.test_milhdbk217f.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the MilHdbk217f class."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses import MilHdbk217f
from ramstk.analyses.models.milhdbk217f import Capacitor

ATTRIBUTES = {
    'hardware_id': 12,
    'category_id': 4,
    'subcategory_id': 1,
    'temperature_rated_max': 105.0,
    'temperature_active': 45.0,
    'voltage_ratio': 0.54,
    'capacitance': 0.0000033,
    'construction_id': 1,
    'configuration_id': 1,
    'specification_id': 1,
    'resistance': 0.05,
    'voltage_dc_operating': 3.3,
    'voltage_ac_operating': 0.04,
    'quality_id': 2,
    'environment_active_id': 1,
    'duty_cycle': 100.0,
    'add_adj_factor': 0.0,
    'mult_adj_factor': 1.0,
    'quantity': 1,
    'hazard_rate_active': 0.0,
    'hazard_rate_method_id': 1,
}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,],
)
def test_get_capacitor_environment_factor(environment_active_id):
    """_get_environment_factor() should return a float value for a Capacitor's piE on success."""
    _pi_e = MilHdbk217f._get_environment_factor(4, environment_active_id)

    assert _pi_e == Capacitor.PI_E[environment_active_id - 1]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "quality_id",
    [1, 2, 3, 4, 5, 6, 7, ],
)
def test_get_capacitor_part_count_quality_factor(quality_id):
    """_get_part_count_quality_factor() should return a float value for a Capacitor's parts count piQ on success."""
    _pi_q = MilHdbk217f._get_part_count_quality_factor(4, 1, quality_id)

    assert _pi_q == Capacitor.PART_COUNT_PI_Q[quality_id - 1]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, ],
)
@pytest.mark.parametrize(
    "quality_id",
    [1, 2, ],
)
def test_get_capacitor_part_stress_quality_factor(subcategory_id, quality_id):
    """_get_part_stress_quality_factor() should return a float value for a Capacitor's part stress piQ on success."""
    # NOTE: We only check the first two entries so as to not raise an
    # IndexError for those subcategories with only two quality levels.
    _pi_q = MilHdbk217f._get_part_stress_quality_factor(4, subcategory_id, quality_id)

    assert _pi_q == Capacitor.PART_STRESS_PI_Q[subcategory_id][quality_id - 1]


@pytest.mark.unit
@pytest.mark.calculation
def test_get_calculate_parts_count_active_hazard_rate():
    """do_calculate_active_hazard_rate() should return a dict of component attributes with values updated from the parts count calculations on success."""
    attributes = MilHdbk217f.do_calculate_active_hazard_rate(**ATTRIBUTES)

    assert isinstance(attributes, dict)
    assert attributes['hazard_rate_active'] == 0.00036


@pytest.mark.unit
@pytest.mark.calculation
def test_get_calculate_part_stress_active_hazard_rate():
    """do_calculate_active_hazard_rate() should return a dict of component attributes with values updated from the part stresscalculations on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2

    attributes = MilHdbk217f.do_calculate_active_hazard_rate(**ATTRIBUTES)

    assert isinstance(attributes, dict)
    assert pytest.approx(attributes['hazard_rate_active'], 0.074572296)
