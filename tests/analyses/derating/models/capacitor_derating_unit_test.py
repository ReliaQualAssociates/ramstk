# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.derating.models.capacitor_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the capacitor derating module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.derating import capacitor


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15, 16, 17, 18, 19],
)
def test_get_subcategory_name_without_specification_id(
    subcategory_id,
):
    """Returns a string name for the capacitor subcategory on success."""
    _subcategory = capacitor._get_subcategory_name(subcategory_id, 1)

    assert isinstance(_subcategory, str)
    assert (
        _subcategory
        == {
            1: "paper",
            2: "paper",
            3: "plastic",
            4: "metallized",
            5: "metallized",
            6: "metallized",
            7: "mica",
            8: "mica_button",
            9: "glass",
            10: "ceramic_fixed",
            13: "tantalum_wet",
            14: "aluminum",
            15: "aluminum_dry",
            16: "ceramic_variable",
            17: "piston",
            18: "trimmer",
            19: "vacuum",
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize("specification_id", [1, 2])
@pytest.mark.parametrize("subcategory_id", [11, 12])
def test_get_subcategory_name_with_specification_id(
    specification_id,
    subcategory_id,
):
    """Returns a string name for the capacitor subcategory on success."""
    _subcategory = capacitor._get_subcategory_name(subcategory_id, specification_id)

    assert isinstance(_subcategory, str)
    assert (
        _subcategory
        == {
            11: {
                1: "temp_comp_ceramic",
                2: "ceramic_chip",
            },
            12: {
                1: "tantalum_solid",
                2: "tantalum_chip",
            },
        }[subcategory_id][specification_id]
    )


@pytest.mark.unit
def test_get_subcategory_name_invalid_subcategory_id():
    """Returns an empty string when passed an invalid subcategory ID."""
    assert capacitor._get_subcategory_name(99, None) == ""


@pytest.mark.unit
def test_get_subcategory_name_invalid_specification_id():
    """Returns and empty string when passed an invalid specification_id."""
    assert capacitor._get_subcategory_name(11, 99) == ""


@pytest.mark.unit
def test_get_subcategory_name_missing_specification_id():
    """Returns an empty string when the specification ID is required but missing."""
    assert capacitor._get_subcategory_name(11, None) == ""


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_no_stresses(
    environment_id,
    test_stress_limits,
):
    """Returns 0 and an empty string when capacitor is not exceeding any limit."""
    _overstress, _reason = capacitor.do_derating_analysis(
        environment_id,
        11,
        test_stress_limits["capacitor"],
        specification_id=2,
        temperature_case=46.3,
        temperature_rated_max=70.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_case_temperature(
    environment_id,
    test_stress_limits,
):
    """Returns 1 and reason string when exceeding the case temperature limit."""
    _overstress, _reason = capacitor.do_derating_analysis(
        environment_id,
        11,
        test_stress_limits["capacitor"],
        specification_id=2,
        temperature_case=79.3,
        temperature_rated_max=85.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 1
    assert (
        _reason == "Temperature of 79.3C exceeds the derated maximum temperature "
        "of 10.0C less than maximum rated temperature of 85.0C.\n"
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_borderline_temperature(
    test_stress_limits,
):
    """Returns 0 and empty reason string when case temperature is on the boundary."""
    _overstress, _reason = capacitor.do_derating_analysis(
        1,
        11,
        test_stress_limits["capacitor"],
        specification_id=2,
        temperature_case=60.0,  # Exactly at the boundary
        temperature_rated_max=70.0,
        voltage_ratio=0.5,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_voltage(
    environment_id,
    test_stress_limits,
):
    """Returns 1 and reason string when exceeding the voltage limit."""
    _overstress, _reason = capacitor.do_derating_analysis(
        environment_id,
        11,
        test_stress_limits["capacitor"],
        specification_id=2,
        temperature_case=59.3,
        temperature_rated_max=85.0,
        voltage_ratio=0.95,
    )

    assert _overstress == 1
    assert _reason == "Voltage ratio of 0.95 exceeds the allowable limit of 0.6.\n"


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_borderline_voltage(
    test_stress_limits,
):
    """Returns 0 and empty reason string when the voltage ratio is on the boundary."""
    _overstress, _reason = capacitor.do_derating_analysis(
        1,
        11,
        test_stress_limits["capacitor"],
        specification_id=2,
        temperature_case=46.3,
        temperature_rated_max=70.0,
        voltage_ratio=0.6,  # Exactly at the voltage limit
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_all_stresses(
    test_stress_limits,
):
    """Returns 1 and reason string when exceeding both limits."""
    _overstress, _reason = capacitor.do_derating_analysis(
        1,
        11,
        test_stress_limits["capacitor"],
        specification_id=2,
        temperature_case=79.3,
        temperature_rated_max=85.0,
        voltage_ratio=0.95,
    )

    assert _overstress == 1
    assert (
        _reason == "Temperature of 79.3C exceeds the derated maximum temperature "
        "of 10.0C less than maximum rated temperature of 85.0C.\nVoltage ratio of 0.95 "
        "exceeds the allowable limit of 0.6.\n"
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_environment_id(
    test_stress_limits,
):
    """Raises am IndexError when passed an invalid environment ID."""
    with pytest.raises(
        IndexError, match=r"do_derating_analysis: Invalid capacitor environment ID 5."
    ):
        capacitor.do_derating_analysis(
            5,
            10,
            test_stress_limits["capacitor"],
            specification_id=2,
            temperature_case=46.3,
            temperature_rated_max=70.0,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_subcategory_id(
    test_stress_limits,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    with pytest.raises(
        KeyError,
        match=r"do_derating_analysis: Invalid capacitor specification ID 2 or "
        r"subcategory ID 21.",
    ):
        capacitor.do_derating_analysis(
            1,
            21,
            test_stress_limits["capacitor"],
            specification_id=2,
            temperature_case=46.3,
            temperature_rated_max=70.0,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_specification_id(
    test_stress_limits,
):
    """Raises a KeyError when passed an invalid specification ID."""
    with pytest.raises(
        KeyError,
        match=r"_do_derating_analysis: Invalid capacitor specification ID 22 or "
        r"subcategory ID 11.",
    ):
        capacitor.do_derating_analysis(
            1,
            11,
            test_stress_limits["capacitor"],
            specification_id=22,
            temperature_case=46.3,
            temperature_rated_max=70.0,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_case_temperature(
    test_stress_limits,
):
    """Raises a TypeError when passed a string case temperature."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid capacitor case temperature type "
        r"<class 'str'> or voltage ratio type <class 'float'>.  Both should be "
        r"<class 'float'>.",
    ):
        capacitor.do_derating_analysis(
            1,
            1,
            test_stress_limits["capacitor"],
            specification_id=2,
            temperature_case="128.3",
            temperature_rated_max=70.0,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_none_case_temperature(
    test_stress_limits,
):
    """Raises a TypeError when passed None for case temperature."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid capacitor case temperature type "
        r"<class 'NoneType'> or voltage ratio type <class 'float'>.  Both should "
        r"be <class 'float'>.",
    ):
        capacitor.do_derating_analysis(
            1,
            1,
            test_stress_limits["capacitor"],
            specification_id=2,
            temperature_case=None,
            temperature_rated_max=70.0,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_voltage_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed a string voltage ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid capacitor case temperature type "
        r"<class 'float'> or voltage ratio type <class 'str'>.  Both should be "
        r"<class 'float'>.",
    ):
        capacitor.do_derating_analysis(
            1,
            11,
            test_stress_limits["capacitor"],
            specification_id=2,
            temperature_case=46.3,
            temperature_rated_max=70.0,
            voltage_ratio="0.9",
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_none_voltage_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed None for the voltage ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid capacitor case temperature type "
        r"<class 'float'> or voltage ratio type <class 'NoneType'>.  Both should "
        r"be <class 'float'>.",
    ):
        capacitor.do_derating_analysis(
            1,
            11,
            test_stress_limits["capacitor"],
            specification_id=2,
            temperature_case=46.3,
            temperature_rated_max=70.0,
            voltage_ratio=None,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_specification_id(
    test_stress_limits,
):
    """Raises a KeyError when passed a string for the specification ID."""
    with pytest.raises(
        KeyError,
        match=r"_do_derating_analysis: Invalid capacitor specification ID 1 or "
        r"subcategory ID 11.",
    ):
        capacitor.do_derating_analysis(
            1,
            11,
            test_stress_limits["capacitor"],
            specification_id="1",
            temperature_case=46.3,
            temperature_rated_max=70.0,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_none_specification_id(
    test_stress_limits,
):
    """Raises a ValueError when passed None for the specification ID."""
    with pytest.raises(
        KeyError,
        match=r"_do_derating_analysis: Invalid capacitor specification ID None or "
        r"subcategory ID 11.",
    ):
        capacitor.do_derating_analysis(
            1,
            11,
            test_stress_limits["capacitor"],
            specification_id=None,
            temperature_case=46.3,
            temperature_rated_max=70.0,
            voltage_ratio=0.2,
        )
