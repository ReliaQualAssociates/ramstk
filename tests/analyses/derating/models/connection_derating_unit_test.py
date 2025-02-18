# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.derating.models.connection_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the connection derating module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.derating import connection


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_no_stresses(
    environment_id,
    test_stress_limits,
):
    """Returns 0 and an empty reason string when not exceeding limits."""
    _overstress, _reason = connection.do_derating_analysis(
        environment_id,
        test_stress_limits["connection"],
        current_ratio=0.5,
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
    """Returns 1 and the reason string when exceeding the current limit."""
    _overstress, _reason = connection.do_derating_analysis(
        environment_id,
        test_stress_limits["connection"],
        current_ratio=1.5,
    )

    assert _overstress == 1
    assert _reason == "Current ratio of 1.5 exceeds the allowable limit of 1.0.\n"


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_environment_id(
    test_stress_limits,
):
    """Raises am IndexError when passed an invalid environment ID."""
    with pytest.raises(
        IndexError, match="do_derating_analysis: Invalid connection environment ID 5."
    ):
        connection.do_derating_analysis(
            5,
            test_stress_limits["connection"],
            current_ratio=0.9,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_current_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed a string current ratio."""
    with pytest.raises(
        TypeError,
        match="do_derating_analysis: Invalid connection current ratio type <class "
        "'str'>.  Should be <type 'float'>.",
    ):
        connection.do_derating_analysis(
            1,
            test_stress_limits["connection"],
            current_ratio="0.9",
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_none_current_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed NOne for the current ratio."""
    with pytest.raises(
        TypeError,
        match="do_derating_analysis: Invalid connection current ratio type "
        "<class 'NoneType'>.  Should be <type 'float'>.",
    ):
        connection.do_derating_analysis(
            1,
            test_stress_limits["connection"],
            current_ratio=None,
        )
