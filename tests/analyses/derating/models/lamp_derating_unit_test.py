# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.derating.models.lamp_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the lamp derating module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.derating import lamp


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_no_stresses(
    environment_id,
    test_stress_limits,
):
    """Returns 0 and an empty reason string when the lamp is not exceeding any limit."""
    _overstress, _reason = lamp.do_derating_analysis(
        environment_id,
        4,
        test_stress_limits["miscellaneous"],
        current_ratio=0.05,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_current(
    environment_id,
    test_stress_limits,
):
    """Returns 1 and the reason string when the lamp is exceeding the current limit."""
    _overstress, _reason = lamp.do_derating_analysis(
        environment_id,
        4,
        test_stress_limits["miscellaneous"],
        current_ratio=0.95,
    )

    assert _overstress == 1
    assert (
        _reason
        == {
            0: "Current ratio of 0.95 exceeds the allowable limit of 0.2.\n",
            1: "Current ratio of 0.95 exceeds the allowable limit of 0.1.\n",
            2: "Current ratio of 0.95 exceeds the allowable limit of 0.1.\n",
        }[environment_id]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_environment_id(
    test_stress_limits,
):
    """Raises an IndexError when passed an invalid environment ID."""
    with pytest.raises(
        IndexError, match=r"do_derating_analysis: Invalid lamp environment ID 5."
    ):
        lamp.do_derating_analysis(
            5,
            4,
            test_stress_limits["miscellaneous"],
            current_ratio=0.02,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_subcategory_id(
    test_stress_limits,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    with pytest.raises(
        KeyError, match=r"do_derating_analysis: Invalid lamp subcategory ID 21."
    ):
        lamp.do_derating_analysis(
            1,
            21,
            test_stress_limits["miscellaneous"],
            current_ratio=0.025,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_current_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed a string current ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid lamp current ratio type <class 'str'>.  "
        r"Should be <type 'float'>.",
    ):
        lamp.do_derating_analysis(
            1,
            4,
            test_stress_limits["miscellaneous"],
            current_ratio="0.9",
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_none_current_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed None for the current ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid lamp current ratio type "
        r"<class 'NoneType'>.  Should be <type 'float'>.",
    ):
        lamp.do_derating_analysis(
            1,
            4,
            test_stress_limits["miscellaneous"],
            current_ratio=None,
        )
