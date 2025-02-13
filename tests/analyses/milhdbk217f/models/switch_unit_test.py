# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.test_switch.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the switch module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f.models import switch
from ramstk.constants.switch import (
    PART_COUNT_LAMBDA_B,
    PART_COUNT_LAMBDA_B_BREAKER,
    PART_COUNT_PI_Q,
    PART_STRESS_LAMBDA_B_BREAKER,
    PART_STRESS_LAMBDA_B_TOGGLE,
    PART_STRESS_PI_Q,
    PI_E,
)


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5],
)
def test_set_default_construction_id(
    subcategory_id,
):
    """Returns the default construction ID for the selected subcategory ID."""
    _construction_id = switch._set_default_construction_id(0, subcategory_id)

    assert (
        _construction_id
        == {
            1: 1,
            2: 1,
            3: 0,
            4: 0,
            5: 0,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5],
)
def test_set_default_contact_form_id(
    subcategory_id,
):
    """Returns the default contact form ID for the selected subcategory ID."""
    _contact_form_id = switch._set_default_contact_form_id(0, subcategory_id)

    assert (
        _contact_form_id
        == {
            1: 2,
            2: 0,
            3: 0,
            4: 0,
            5: 3,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5],
)
def test_set_default_cycle_rate(
    subcategory_id,
):
    """Returns the default cycling rate for the selected subcategory ID."""
    _n_cycles = switch._set_default_cycle_rate(0.0, subcategory_id)

    assert (
        _n_cycles
        == {
            1: 1.0,
            2: 1.0,
            3: 30.0,
            4: 1.0,
            5: 0.0,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5],
)
def test_set_default_active_contacts(
    subcategory_id,
):
    """Returns the default active contacts for the selected subcategory ID."""
    _n_elements = switch._set_default_active_contacts(0.0, subcategory_id)

    assert (
        _n_elements
        == {
            1: 0,
            2: 1,
            3: 24,
            4: 6,
            5: 0,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_set_default_values(
    test_attributes_switch,
):
    """Sets default values for each parameter <= 0.0."""
    test_attributes_switch["application_id"] = -1
    test_attributes_switch["construction_id"] = 0
    test_attributes_switch["contact_form_id"] = -2
    test_attributes_switch["current_ratio"] = -0.4
    test_attributes_switch["n_cycles"] = 0.0
    test_attributes_switch["n_elements"] = 0
    test_attributes_switch["quality_id"] = 0
    test_attributes_switch["subcategory_id"] = 2
    _attributes = switch.set_default_values(test_attributes_switch)

    assert isinstance(_attributes, dict)
    assert _attributes["application_id"] == 1
    assert _attributes["construction_id"] == 1
    assert _attributes["contact_form_id"] == 0
    assert _attributes["current_ratio"] == 0.5
    assert _attributes["n_cycles"] == 1.0
    assert _attributes["n_elements"] == 1
    assert _attributes["quality_id"] == 1


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_set_default_values_none_needed(
    test_attributes_switch,
):
    """Makes no changes to each parameter > 0.0."""
    test_attributes_switch["application_id"] = 3
    test_attributes_switch["construction_id"] = 1
    test_attributes_switch["contact_form_id"] = 2
    test_attributes_switch["current_ratio"] = 0.4
    test_attributes_switch["n_cycles"] = 0.3
    test_attributes_switch["n_elements"] = 12
    test_attributes_switch["quality_id"] = 2
    test_attributes_switch["subcategory_id"] = 2
    _attributes = switch.set_default_values(test_attributes_switch)

    assert isinstance(_attributes, dict)
    assert _attributes["application_id"] == 3
    assert _attributes["construction_id"] == 1
    assert _attributes["contact_form_id"] == 2
    assert _attributes["current_ratio"] == 0.4
    assert _attributes["n_cycles"] == 0.3
    assert _attributes["n_elements"] == 12
    assert _attributes["quality_id"] == 2


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4])
@pytest.mark.usefixtures("test_attributes_switch")
def test_get_part_count_lambda_b(
    environment_active_id,
    subcategory_id,
    test_attributes_switch,
):
    """Returns a float value for the part count base hazard rate on success."""
    test_attributes_switch["environment_active_id"] = environment_active_id
    test_attributes_switch["subcategory_id"] = subcategory_id
    _lambda_b = switch.get_part_count_lambda_b(test_attributes_switch)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == PART_COUNT_LAMBDA_B[subcategory_id][environment_active_id - 1]


@pytest.mark.unit
@pytest.mark.parametrize("construction_id", [1, 2])
@pytest.mark.parametrize(
    "environment_active_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
@pytest.mark.usefixtures("test_attributes_switch")
def test_get_part_count_lambda_b_breaker(
    construction_id,
    environment_active_id,
    test_attributes_switch,
):
    """Returns a float value for the part count base hazard rate on success."""
    test_attributes_switch["environment_active_id"] = environment_active_id
    test_attributes_switch["subcategory_id"] = 5
    test_attributes_switch["construction_id"] = construction_id
    _lambda_b = switch.get_part_count_lambda_b(test_attributes_switch)

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == PART_COUNT_LAMBDA_B_BREAKER[construction_id][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_get_part_count_lambda_b_invalid_environment_id(
    test_attributes_switch,
):
    """Raises an IndexError when passed an invalid environment ID."""
    test_attributes_switch["environment_active_id"] = 33
    test_attributes_switch["subcategory_id"] = 2
    with pytest.raises(
        IndexError, match="get_part_count_lambda_b: Invalid switch environment ID 33."
    ):
        switch.get_part_count_lambda_b(test_attributes_switch)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_get_part_count_lambda_b_invalid_subcategory_id(
    test_attributes_switch,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_switch["environment_active_id"] = 3
    test_attributes_switch["subcategory_id"] = 27
    with pytest.raises(
        KeyError,
        match=r"get_part_count_lambda_b: Invalid switch construction ID 1 or "
        r"subcategory ID 27.",
    ):
        switch.get_part_count_lambda_b(test_attributes_switch)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_get_part_count_lambda_b_invalid_construction_id(
    test_attributes_switch,
):
    """Raises a KeyError when passed an invalid construction ID."""
    test_attributes_switch["construction_id"] = -1
    test_attributes_switch["subcategory_id"] = 5
    with pytest.raises(
        KeyError,
        match=r"get_part_count_lambda_b: Invalid switch construction ID -1 or "
        r"subcategory ID 5.",
    ):
        switch.get_part_count_lambda_b(test_attributes_switch)


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2])
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5])
@pytest.mark.usefixtures("test_attributes_switch")
def test_get_part_count_quality_factor(
    quality_id,
    subcategory_id,
    test_attributes_switch,
):
    """Returns a float value for the part count quality factor (piQ) on success."""
    test_attributes_switch["quality_id"] = quality_id
    test_attributes_switch["subcategory_id"] = subcategory_id
    _pi_q = switch.get_part_count_quality_factor(test_attributes_switch)

    assert isinstance(_pi_q, float)
    assert _pi_q == PART_COUNT_PI_Q[subcategory_id][quality_id - 1]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_get_part_count_quality_factor_invalid_quality_id(
    test_attributes_switch,
):
    """Raises an IndexError when passed an invalid quality ID."""
    test_attributes_switch["quality_id"] = 12
    test_attributes_switch["subcategory_id"] = 1
    with pytest.raises(
        IndexError,
        match=r"get_part_count_quality_factor: Invalid switch quality ID 12.",
    ):
        switch.get_part_count_quality_factor(test_attributes_switch)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_get_part_count_quality_factor_invalid_subcategory_id(
    test_attributes_switch,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_switch["quality_id"] = 1
    test_attributes_switch["subcategory_id"] = 21
    with pytest.raises(
        KeyError,
        match=r"get_part_count_quality_factor: Invalid switch subcategory ID 21.",
    ):
        switch.get_part_count_quality_factor(test_attributes_switch)


@pytest.mark.unit
@pytest.mark.parametrize("construction_id", [1, 2])
@pytest.mark.parametrize("quality_id", [1, 2])
@pytest.mark.parametrize("subcategory_id", [2, 3, 4])
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_part_stress_lambda_b(
    construction_id,
    quality_id,
    subcategory_id,
    test_attributes_switch,
):
    """Returns a float value for the part stress base hazard rate on success."""
    test_attributes_switch["application_id"] = 1
    test_attributes_switch["construction_id"] = construction_id
    test_attributes_switch["n_elements"] = 8
    test_attributes_switch["quality_id"] = quality_id
    test_attributes_switch["subcategory_id"] = subcategory_id
    _lambda_b = switch.calculate_part_stress_lambda_b(test_attributes_switch)

    assert isinstance(_lambda_b, float)
    if subcategory_id == 4:
        assert _lambda_b == pytest.approx({1: 0.5027, 2: 0.798}[quality_id])
    else:
        assert _lambda_b == pytest.approx(
            {
                2: {1: [0.1036, 1.94], 2: [0.1072, 5.14]},
                3: {1: [0.00694, 0.26], 2: [0.00694, 0.58]},
            }[subcategory_id][construction_id][quality_id - 1]
        )


@pytest.mark.unit
@pytest.mark.parametrize("application_id", [1, 2, 3])
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_part_stress_lambda_b_breaker(
    application_id,
    test_attributes_switch,
):
    """Returns a float value for the part stress base hazard rate on success."""
    test_attributes_switch["application_id"] = application_id
    test_attributes_switch["n_elements"] = 8
    test_attributes_switch["subcategory_id"] = 5
    _lambda_b = switch.calculate_part_stress_lambda_b(test_attributes_switch)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == PART_STRESS_LAMBDA_B_BREAKER[application_id - 1]


@pytest.mark.unit
@pytest.mark.parametrize("construction_id", [1, 2])
@pytest.mark.parametrize("quality_id", [1, 2])
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_part_stress_lambda_b_toggle_switch(
    construction_id,
    quality_id,
    test_attributes_switch,
):
    """Returns a float value for the part stress base hazard rate on success."""
    test_attributes_switch["construction_id"] = construction_id
    test_attributes_switch["quality_id"] = quality_id
    test_attributes_switch["subcategory_id"] = 1
    _lambda_b = switch.calculate_part_stress_lambda_b(test_attributes_switch)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == PART_STRESS_LAMBDA_B_TOGGLE[construction_id][quality_id - 1]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_part_stress_lambda_b_invalid_application_id(
    test_attributes_switch,
):
    """Raises an IndexError when passed an invalid application ID."""
    test_attributes_switch["application_id"] = 21
    test_attributes_switch["subcategory_id"] = 5
    with pytest.raises(
        IndexError,
        match=r"calculate_part_stress_lambda_b: Invalid switch application ID 21 or "
        r"quality ID 1.",
    ):
        switch.calculate_part_stress_lambda_b(test_attributes_switch)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_part_stress_lambda_b_invalid_quality_id(
    test_attributes_switch,
):
    """Raises an IndexError when passed an invalid quality ID."""
    test_attributes_switch["construction_id"] = 1
    test_attributes_switch["quality_id"] = 21
    test_attributes_switch["subcategory_id"] = 1
    with pytest.raises(
        IndexError,
        match=r"calculate_part_stress_lambda_b: Invalid switch application ID 1 or "
        r"quality ID 21.",
    ):
        switch.calculate_part_stress_lambda_b(test_attributes_switch)

    test_attributes_switch["subcategory_id"] = 2
    with pytest.raises(
        IndexError,
        match=r"calculate_part_stress_lambda_b: Invalid switch application ID 1 or "
        r"quality ID 21.",
    ):
        switch.calculate_part_stress_lambda_b(test_attributes_switch)

    test_attributes_switch["subcategory_id"] = 4
    with pytest.raises(
        IndexError,
        match=r"calculate_part_stress_lambda_b: Invalid switch application ID 1 or "
        r"quality ID 21.",
    ):
        switch.calculate_part_stress_lambda_b(test_attributes_switch)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_part_stress_lambda_b_invalid_construction_id(
    test_attributes_switch,
):
    """Raises a KeyError when passed an invalid construction ID."""
    test_attributes_switch["subcategory_id"] = 1
    test_attributes_switch["construction_id"] = 41
    with pytest.raises(
        KeyError,
        match=r"calculate_part_stress_lambda_b: Invalid switch construction ID 41 or "
        r"subcategory ID 1.",
    ):
        switch.calculate_part_stress_lambda_b(test_attributes_switch)


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5])
@pytest.mark.usefixtures("test_attributes_switch")
def test_get_environment_factor(
    environment_active_id,
    subcategory_id,
    test_attributes_switch,
):
    """Returns a float value for the environment factor on success."""
    test_attributes_switch["environment_active_id"] = environment_active_id
    test_attributes_switch["subcategory_id"] = subcategory_id
    _pi_e = switch.get_environment_factor(test_attributes_switch)

    assert isinstance(_pi_e, float)
    assert _pi_e == PI_E[subcategory_id][environment_active_id - 1]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_get_environment_factor_invalid_environment_id(
    test_attributes_switch,
):
    """Raises an IndexError when passed an invalid environment ID."""
    test_attributes_switch["environment_active_id"] = 121
    test_attributes_switch["subcategory_id"] = 1
    with pytest.raises(
        IndexError, match=r"get_environment_factor: Invalid switch environment ID 121."
    ):
        switch.get_environment_factor(test_attributes_switch)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_get_environment_factor_invalid_subcategory_id(
    test_attributes_switch,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_switch["subcategory_id"] = 121
    with pytest.raises(
        KeyError, match=r"get_environment_factor: Invalid switch subcategory ID 121."
    ):
        switch.get_environment_factor(test_attributes_switch)


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2])
@pytest.mark.usefixtures("test_attributes_switch")
def test_get_part_stress_quality_factor(
    quality_id,
    test_attributes_switch,
):
    """Returns a float value for the quality factor on success."""
    test_attributes_switch["quality_id"] = quality_id
    test_attributes_switch["subcategory_id"] = 5
    _pi_q = switch.get_part_stress_quality_factor(test_attributes_switch)

    assert isinstance(_pi_q, float)
    assert _pi_q == PART_STRESS_PI_Q[quality_id - 1]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_get_quality_factor_invalid_quality_id(
    test_attributes_switch,
):
    """Raises an IndexError when passed an invalid quality ID."""
    test_attributes_switch["quality_id"] = 121
    test_attributes_switch["subcategory_id"] = 5
    with pytest.raises(
        IndexError,
        match=r"get_part_stress_quality_factor: Invalid switch quality ID 121.",
    ):
        switch.get_part_stress_quality_factor(test_attributes_switch)


@pytest.mark.unit
def test_calculate_load_stress_resistive():
    """Returns a float when calculating resistive load stress."""
    _pi_l = switch.calculate_load_stress_factor(1, 0.2)

    assert isinstance(_pi_l, float)
    assert _pi_l == pytest.approx(1.064494459)


@pytest.mark.unit
def test_calculate_load_stress_inductive():
    """Returns a float when calculating inductive load stress."""
    _pi_l = switch.calculate_load_stress_factor(2, 0.2)

    assert isinstance(_pi_l, float)
    assert _pi_l == pytest.approx(1.284025417)


@pytest.mark.unit
def test_calculate_load_stress_capacitive():
    """Returns a float when calculating capacitive load stress."""
    _pi_l = switch.calculate_load_stress_factor(3, 0.2)

    assert isinstance(_pi_l, float)
    assert _pi_l == pytest.approx(2.718281828)


@pytest.mark.unit
def test_calculate_load_stress_invalid_application_id():
    """Returns 0.0 when passed an invalid application ID."""
    _pi_l = switch.calculate_load_stress_factor(13, 0.2)

    assert _pi_l == 0.0


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
@pytest.mark.parametrize("subcategory_id", [1, 2, 5])
def test_calculate_part_stress(
    subcategory_id,
    test_attributes_switch,
):
    """Returns the switch attributes dict with updated values on success."""
    test_attributes_switch["construction_id"] = 1
    test_attributes_switch["hazard_rate_active"] = 0.00045
    test_attributes_switch["subcategory_id"] = subcategory_id
    _attributes = switch.calculate_part_stress(test_attributes_switch)

    assert isinstance(_attributes, dict)
    if subcategory_id == 1:
        assert _attributes["piCYC"] == 2.3
        assert _attributes["piL"] == pytest.approx(1.372187594)
        assert _attributes["piC"] == 1.7
        assert _attributes["hazard_rate_active"] == pytest.approx(0.001857203)
    elif subcategory_id == 2:
        assert _attributes["piCYC"] == 2.3
        assert _attributes["piL"] == pytest.approx(1.372187594)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.001092472)
    elif subcategory_id == 5:
        assert _attributes["piC"] == 3.0
        assert _attributes["piU"] == 1.0
        assert _attributes["hazard_rate_active"] == pytest.approx(0.00135)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_part_stress_picyc_one(
    test_attributes_switch,
):
    """Sets piCYC=1.0 when n_cycles is less than or equal to 1.0."""
    test_attributes_switch["application_id"] = 1
    test_attributes_switch["hazard_rate_active"] = 0.00045
    test_attributes_switch["n_cycles"] = 1.0
    _attributes = switch.calculate_part_stress(test_attributes_switch)

    assert isinstance(_attributes, dict)
    assert _attributes["piCYC"] == 1.0
    assert _attributes["hazard_rate_active"] == pytest.approx(0.0008074796)

    test_attributes_switch["n_cycles"] = 0.05
    _attributes = switch.calculate_part_stress(test_attributes_switch)

    assert isinstance(_attributes, dict)
    assert _attributes["piCYC"] == 1.0
    assert _attributes["hazard_rate_active"] == pytest.approx(0.001448941)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_part_stress_missing_attribute_key(
    test_attributes_switch,
):
    """Raises a KeyError when a required attribute is missing."""
    test_attributes_switch["hazard_rate_active"] = 0.0045
    test_attributes_switch.pop("n_cycles")
    with pytest.raises(
        KeyError,
        match=r"calculate_part_stress: Missing required switch attribute: "
        r"'n_cycles'.",
    ):
        switch.calculate_part_stress(test_attributes_switch)
