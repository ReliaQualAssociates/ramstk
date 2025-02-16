# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.semiconductor_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the semiconductor module."""

# Standard Library Imports
import copy

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f.models import semiconductor
from ramstk.constants.semiconductor import (
    PART_COUNT_PI_Q,
    PART_COUNT_PI_Q_HF_DIODE,
    PART_STRESS_PI_Q,
    PART_STRESS_PI_Q_HF_DIODE,
    PI_E,
)


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [2, 3, 4, 7, 8],
)
def test_set_default_application_id(
    subcategory_id,
):
    """Should return the default application ID for the selected subcategory ID."""
    _application_id = semiconductor._set_default_application_id(0, subcategory_id, 1)

    assert (
        _application_id
        == {
            2: 0,
            3: 2,
            4: 2,
            7: 2,
            8: 1,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [2, 3, 6, 7, 8],
)
def test_set_default_rated_power(
    subcategory_id,
):
    """Should return the default rated power for the selected subcategory ID."""
    _power_rated = semiconductor._set_default_rated_power(0.0, subcategory_id, 1)

    assert (
        _power_rated
        == {
            2: 0.0,
            3: 0.5,
            6: 0.5,
            7: 100.0,
            8: 0.0,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 3, 6, 13],
)
def test_set_default_voltage_ratio(
    subcategory_id,
):
    """Should return the default voltage ratio for the selected subcategory ID."""
    _voltage_ratio = semiconductor._set_default_voltage_ratio(0.0, subcategory_id, 1)

    assert (
        _voltage_ratio
        == {
            1: 0.7,
            3: 0.5,
            6: 0.7,
            13: 0.5,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_set_default_values(
    test_attributes_semiconductor,
):
    """Should set default values for each parameter <= 0.0."""
    test_attributes_semiconductor["application_id"] = 0
    test_attributes_semiconductor["construction_id"] = 0
    test_attributes_semiconductor["power_rated"] = 0.0
    test_attributes_semiconductor["subcategory_id"] = 4
    test_attributes_semiconductor["type_id"] = 0
    test_attributes_semiconductor["voltage_ratio"] = -2.5
    _attributes = semiconductor.set_default_values(test_attributes_semiconductor)

    assert isinstance(_attributes, dict)
    assert _attributes["application_id"] == 2
    assert _attributes["type_id"] == 1
    assert _attributes["power_rated"] == 0.0
    assert _attributes["voltage_ratio"] == 1.0

    test_attributes_semiconductor["subcategory_id"] = 1
    _attributes = semiconductor.set_default_values(test_attributes_semiconductor)

    assert isinstance(_attributes, dict)
    assert _attributes["construction_id"] == 1


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_set_default_values_none_needed(
    test_attributes_semiconductor,
):
    """Should set default values for each parameter <= 0.0."""
    test_attributes_semiconductor["application_id"] = 2
    test_attributes_semiconductor["construction_id"] = 4
    test_attributes_semiconductor["power_rated"] = 0.5
    test_attributes_semiconductor["subcategory_id"] = 4
    test_attributes_semiconductor["type_id"] = 2
    test_attributes_semiconductor["voltage_ratio"] = 0.45
    _attributes = semiconductor.set_default_values(test_attributes_semiconductor)

    assert isinstance(_attributes, dict)
    assert _attributes["application_id"] == 2
    assert _attributes["type_id"] == 2
    assert _attributes["power_rated"] == 0.5
    assert _attributes["voltage_ratio"] == 0.45

    test_attributes_semiconductor["subcategory_id"] = 1
    _attributes = semiconductor.set_default_values(test_attributes_semiconductor)

    assert isinstance(_attributes, dict)
    assert _attributes["construction_id"] == 4


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 4])
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_get_part_count_lambda_b(
    subcategory_id,
    test_attributes_semiconductor,
):
    """Returns a float value for the part count base hazard rate on success."""
    test_attributes_semiconductor["environment_active_id"] = 1
    test_attributes_semiconductor["subcategory_id"] = subcategory_id
    test_attributes_semiconductor["type_id"] = 1
    _lambda_b = semiconductor.get_part_count_lambda_b(test_attributes_semiconductor)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == {1: 0.0036, 4: 0.014}[subcategory_id]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_get_part_count_lambda_b_invalid_environment_id(
    test_attributes_semiconductor,
):
    """Raises an IndexError if passed an invalid active environment ID."""
    test_attributes_semiconductor["environment_active_id"] = 32
    test_attributes_semiconductor["subcategory_id"] = 1
    test_attributes_semiconductor["type_id"] = 1
    with pytest.raises(
        IndexError,
        match=r"get_part_count_lambda_b: Invalid semiconductor environment ID 32.",
    ):
        semiconductor.get_part_count_lambda_b(test_attributes_semiconductor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_get_part_count_lambda_b_invalid_subcategory_id(
    test_attributes_semiconductor,
):
    """Raises a KeyError if passed an invalid subcategory ID."""
    test_attributes_semiconductor["environment_active_id"] = 3
    test_attributes_semiconductor["subcategory_id"] = 47
    test_attributes_semiconductor["type_id"] = 1
    with pytest.raises(
        KeyError,
        match=r"get_part_count_lambda_b: Invalid semiconductor subcategory ID 47 or "
        r"type ID 1.",
    ):
        semiconductor.get_part_count_lambda_b(test_attributes_semiconductor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_get_part_count_lambda_b_invalid_type_id(
    test_attributes_semiconductor,
):
    """Raises a KeyError if passed an invalid type ID."""
    test_attributes_semiconductor["environment_active_id"] = 3
    test_attributes_semiconductor["subcategory_id"] = 1
    test_attributes_semiconductor["type_id"] = 31
    with pytest.raises(
        KeyError,
        match=r"get_part_count_lambda_b: Invalid semiconductor subcategory ID 1 or "
        r"type ID 31.",
    ):
        semiconductor.get_part_count_lambda_b(test_attributes_semiconductor)


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2, 3, 4, 5])
@pytest.mark.parametrize("subcategory_id", [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_get_part_count_quality_factor(
    quality_id,
    subcategory_id,
    test_attributes_semiconductor,
):
    """Returns a float value for the quality factor (piQ) on success."""
    # There are only three quality levels for subcategory ID 13 semiconductors.
    if subcategory_id < 13 or (subcategory_id == 13 and quality_id < 4):
        test_attributes_semiconductor["quality_id"] = quality_id
        test_attributes_semiconductor["subcategory_id"] = subcategory_id
        _pi_q = semiconductor.get_part_count_quality_factor(
            test_attributes_semiconductor
        )

        assert isinstance(_pi_q, float)
        assert _pi_q == PART_COUNT_PI_Q[subcategory_id][quality_id - 1]


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2, 3, 4, 5])
@pytest.mark.parametrize("type_id", [1, 5])
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_get_part_count_quality_factor_hf_diode(
    quality_id,
    type_id,
    test_attributes_semiconductor,
):
    """Returns a float value for the quality factor (piQ) on success."""
    test_attributes_semiconductor["quality_id"] = quality_id
    test_attributes_semiconductor["subcategory_id"] = 2
    test_attributes_semiconductor["type_id"] = type_id
    if type_id == 1:
        _pi_q = semiconductor.get_part_count_quality_factor(
            test_attributes_semiconductor
        )

        assert isinstance(_pi_q, float)
        assert _pi_q == PART_COUNT_PI_Q_HF_DIODE[0][quality_id - 1]
    elif type_id == 2 and quality_id < 5:
        _pi_q = semiconductor.get_part_count_quality_factor(
            test_attributes_semiconductor
        )

        assert isinstance(_pi_q, float)
        assert _pi_q == PART_COUNT_PI_Q_HF_DIODE[1][quality_id - 1]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_get_part_count_quality_factor_invalid_quality_id(
    test_attributes_semiconductor,
):
    """Raises an IndexError when passed an invalid quality ID."""
    test_attributes_semiconductor["quality_id"] = 31
    test_attributes_semiconductor["subcategory_id"] = 2
    test_attributes_semiconductor["type_id"] = 1
    with pytest.raises(
        IndexError,
        match=r"get_part_count_quality factor: Invalid semiconductor quality ID 31.",
    ):
        semiconductor.get_part_count_quality_factor(test_attributes_semiconductor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_get_part_count_quality_factor_invalid_subcategory_id(
    test_attributes_semiconductor,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_semiconductor["quality_id"] = 1
    test_attributes_semiconductor["subcategory_id"] = 28
    test_attributes_semiconductor["type_id"] = 1
    with pytest.raises(
        KeyError,
        match=r"get_part_count_quality_factor: Invalid semiconductor subcategory "
        r"ID 28.",
    ):
        semiconductor.get_part_count_quality_factor(test_attributes_semiconductor)


@pytest.mark.unit
@pytest.mark.parametrize("application_id", [1, 2])
@pytest.mark.parametrize("frequency_operating", [0.5, 5.0])
@pytest.mark.parametrize("subcategory_id", [1, 3, 7, 8, 12])
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_part_stress_lambda_b(
    application_id,
    frequency_operating,
    subcategory_id,
    test_attributes_semiconductor,
):
    """Returns a float value for the part stress base hazard rate on success."""
    test_attributes_semiconductor["application_id"] = application_id
    test_attributes_semiconductor["frequency_operating"] = frequency_operating
    test_attributes_semiconductor["n_elements"] = 8
    test_attributes_semiconductor["power_operating"] = 0.05
    test_attributes_semiconductor["subcategory_id"] = subcategory_id
    test_attributes_semiconductor["type_id"] = 1
    _lambda_b = semiconductor.calculate_part_stress_lambda_b(
        test_attributes_semiconductor
    )

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1:
        assert _lambda_b == 0.0038
    elif subcategory_id == 3:
        assert _lambda_b == 0.00074
    elif subcategory_id == 7 and frequency_operating == 0.5:
        assert _lambda_b == pytest.approx(0.038206853)
    elif subcategory_id == 8 and frequency_operating == 0.5:
        assert _lambda_b == pytest.approx(0.011808438)
    elif subcategory_id == 8 and frequency_operating == 5.0:
        assert _lambda_b == 0.052
    elif subcategory_id == 12 and application_id == 1:
        assert _lambda_b == 0.003483
    elif subcategory_id == 12 and application_id == 2:
        assert _lambda_b == 0.00344


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_part_stress_lambda_b_invalid_type_id(
    test_attributes_semiconductor,
):
    """Raises an IndexError if passed an invalid type ID."""
    test_attributes_semiconductor["application_id"] = 1
    test_attributes_semiconductor["frequency_operating"] = 1.5
    test_attributes_semiconductor["n_elements"] = 8
    test_attributes_semiconductor["power_operating"] = 0.055
    test_attributes_semiconductor["subcategory_id"] = 1
    test_attributes_semiconductor["type_id"] = 11
    with pytest.raises(
        IndexError,
        match=r"calculate_part_stress_lambda_b: Invalid semiconductor type ID 11.",
    ):
        semiconductor.calculate_part_stress_lambda_b(test_attributes_semiconductor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_part_stress_lambda_b_invalid_subcategory_id(
    test_attributes_semiconductor,
):
    """Raises a KeyError if passed an invalid subcategory ID."""
    test_attributes_semiconductor["application_id"] = 1
    test_attributes_semiconductor["frequency_operating"] = 1.5
    test_attributes_semiconductor["n_elements"] = 8
    test_attributes_semiconductor["power_operating"] = 0.055
    test_attributes_semiconductor["subcategory_id"] = 21
    test_attributes_semiconductor["type_id"] = 1
    with pytest.raises(
        KeyError,
        match=r"calculate_part_stress_lambda_b: Invalid semiconductor subcategory ID 21.",
    ):
        semiconductor.calculate_part_stress_lambda_b(test_attributes_semiconductor)


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_get_environment_factor(
    environment_active_id,
    subcategory_id,
    test_attributes_semiconductor,
):
    """Returns a float value for the environment factor on success."""
    test_attributes_semiconductor["environment_active_id"] = environment_active_id
    test_attributes_semiconductor["subcategory_id"] = subcategory_id
    _pi_e = semiconductor.get_environment_factor(test_attributes_semiconductor)

    assert isinstance(_pi_e, float)
    assert _pi_e == PI_E[subcategory_id][environment_active_id - 1]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_get_environment_factor_invalid_environment_id(
    test_attributes_semiconductor,
):
    """Raises an IndexError when passed an invalid environment ID."""
    test_attributes_semiconductor["environment_active_id"] = 28
    test_attributes_semiconductor["subcategory_id"] = 1
    with pytest.raises(
        IndexError,
        match=r"get_environment_factor: Invalid semiconductor environment ID 28.",
    ):
        semiconductor.get_environment_factor(test_attributes_semiconductor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_get_environment_factor_invalid_subcategory_id(
    test_attributes_semiconductor,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_semiconductor["environment_active_id"] = 2
    test_attributes_semiconductor["subcategory_id"] = 19
    with pytest.raises(
        KeyError,
        match=r"get_environment_factor: Invalid semiconductor subcategory ID 19.",
    ):
        semiconductor.get_environment_factor(test_attributes_semiconductor)


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2, 3, 4, 5])
@pytest.mark.parametrize("subcategory_id", [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_get_part_stress_quality_factor(
    quality_id,
    subcategory_id,
    test_attributes_semiconductor,
):
    """Returns a float value for the part stress quality factor (piQ) on success."""
    test_attributes_semiconductor["quality_id"] = quality_id
    test_attributes_semiconductor["subcategory_id"] = subcategory_id
    test_attributes_semiconductor["type_id"] = 1
    if (
        subcategory_id in [1, 3, 4, 5, 10, 11, 12]
        or (subcategory_id in [6, 7, 8, 9] and quality_id < 5)
        or (subcategory_id == 13 and quality_id < 4)
    ):
        _pi_q = semiconductor.get_part_stress_quality_factor(
            test_attributes_semiconductor
        )

        assert isinstance(_pi_q, float)
        assert _pi_q == PART_STRESS_PI_Q[subcategory_id][quality_id - 1]


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2, 3, 4, 5])
@pytest.mark.parametrize("type_id", [1, 3, 4, 5, 6])
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_get_part_stress_quality_factor_hf_diode(
    quality_id,
    type_id,
    test_attributes_semiconductor,
):
    """Returns a float value for the part stress quality factor (piQ) on success."""
    test_attributes_semiconductor["quality_id"] = quality_id
    test_attributes_semiconductor["subcategory_id"] = 2
    test_attributes_semiconductor["type_id"] = type_id
    if type_id != 5 or (type_id == 5 and quality_id < 5):
        _pi_q = semiconductor.get_part_stress_quality_factor(
            test_attributes_semiconductor
        )

        assert isinstance(_pi_q, float)
        assert _pi_q == PART_STRESS_PI_Q_HF_DIODE[type_id][quality_id - 1]


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_get_part_stress_quality_factor_invalid_quality_id(
    subcategory_id,
    test_attributes_semiconductor,
):
    """Raises an IndexError when passed an invalid quality ID."""
    test_attributes_semiconductor["quality_id"] = 8
    test_attributes_semiconductor["subcategory_id"] = subcategory_id
    test_attributes_semiconductor["type_id"] = 1
    with pytest.raises(
        IndexError,
        match=r"get_part_stress_quality_factor: Invalid semiconductor quality ID 8.",
    ):
        semiconductor.get_part_stress_quality_factor(test_attributes_semiconductor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_get_part_stress_quality_factor_invalid_subcategory_id(
    test_attributes_semiconductor,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_semiconductor["quality_id"] = 1
    test_attributes_semiconductor["subcategory_id"] = 22
    test_attributes_semiconductor["type_id"] = 1
    with pytest.raises(
        KeyError,
        match=r"get_part_stress_quality_factor: Invalid semiconductor subcategory ID 22 or type ID 1.",
    ):
        semiconductor.get_part_stress_quality_factor(test_attributes_semiconductor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_get_part_stress_quality_factor_invalid_type(
    test_attributes_semiconductor,
):
    """Raises a KeyError when passed an invalid type ID."""
    test_attributes_semiconductor["quality_id"] = 1
    test_attributes_semiconductor["subcategory_id"] = 2
    test_attributes_semiconductor["type_id"] = 21
    with pytest.raises(
        KeyError,
        match=r"get_part_stress_quality_factor: Invalid semiconductor subcategory "
        r"ID 2 or type ID 21.",
    ):
        semiconductor.get_part_stress_quality_factor(test_attributes_semiconductor)


@pytest.mark.unit
def test_calculate_junction_temperature():
    """Returns a float value for the junction temperature on success."""
    _temperature_junction = semiconductor.calculate_junction_temperature(
        1,
        2,
        38.2,
        105.0,
        0.05,
    )

    assert isinstance(_temperature_junction, float)
    assert _temperature_junction == 43.45


@pytest.mark.unit
def test_calculate_junction_temperature_zero_case_temp():
    """Returns a float value for the junction temperature when passed a case temperature
    <=0.0."""
    _temperature_junction = semiconductor.calculate_junction_temperature(
        1,
        2,
        -38.2,
        105.0,
        0.05,
    )

    assert isinstance(_temperature_junction, float)
    assert _temperature_junction == 40.25


@pytest.mark.unit
def test_calculate_junction_temperature_zero_theta_jc():
    """Returns a float value for the junction temperature when passed a theta_jc
    <=0.0."""
    _temperature_junction = semiconductor.calculate_junction_temperature(
        1,
        2,
        38.2,
        0.0,
        0.05,
    )

    assert isinstance(_temperature_junction, float)
    assert _temperature_junction == 38.7


@pytest.mark.unit
def test_calculate_junction_temperature_zero_case_temp_invalid_environment_id():
    """Raises an IndexError when passed a case temperature <=0.0 and an invalid active
    environment_id."""
    with pytest.raises(
        IndexError,
        match=r"calculate_junction_temperature: Invalid semiconductor environment "
        r"ID 31 or package ID 1.",
    ):
        semiconductor.calculate_junction_temperature(
            31,
            1,
            0.0,
            105.0,
            0.05,
        )


@pytest.mark.unit
def test_calculate_junction_temperature_zero_theta_jc_invalid_package_id():
    """Raises an IndexError when passed a theta_jc <=0.0 and an invalid package ID."""
    with pytest.raises(
        IndexError,
        match=r"calculate_junction_temperature: Invalid semiconductor environment "
        r"ID 1 or package ID 128",
    ):
        semiconductor.calculate_junction_temperature(
            1,
            128,
            38.2,
            -10.0,
            0.05,
        )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 3, 7])
@pytest.mark.parametrize("voltage_ratio", [0.4, 0.8])
def test_calculate_temperature_factor(
    subcategory_id,
    voltage_ratio,
):
    """Returns a float value for the temperature factor (piT) on success."""
    _pi_t = semiconductor.calculate_temperature_factor(
        subcategory_id,
        1,
        voltage_ratio,
        52.8,
    )

    assert isinstance(_pi_t, float)
    if subcategory_id == 1:
        assert _pi_t == pytest.approx(2.42314826)
    elif subcategory_id == 3:
        assert _pi_t == pytest.approx(1.83183169)
    elif subcategory_id == 7 and voltage_ratio == 0.4:
        assert _pi_t == pytest.approx(0.229615567)
    elif subcategory_id == 7 and voltage_ratio == 0.8:
        assert _pi_t == pytest.approx(2.06654010)


@pytest.mark.unit
def test_calculate_temperature_factor_invalid_type_id():
    """Raises an IndexError if passed an invalid type ID."""
    with pytest.raises(
        IndexError,
        match=r"calculate_temperature_factor: Invalid semiconductor type ID 17",
    ):
        semiconductor.calculate_temperature_factor(
            2,
            17,
            0.5,
            52.8,
        )


@pytest.mark.unit
def test_calculate_temperature_factor_invalid_subcategory_id():
    """Raises a KeyError if passed an invalid subcategory ID."""
    with pytest.raises(
        KeyError,
        match=r"calculate_temperature_factor: Invalid semiconductor subcategory ID 27.",
    ):
        semiconductor.calculate_temperature_factor(
            27,
            1,
            0.5,
            52.8,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
@pytest.mark.parametrize("subcategory_id", [2, 3, 4, 7, 13])
@pytest.mark.parametrize("application_id", [1, 2])
def test_calculate_application_factor(
    subcategory_id,
    application_id,
    test_attributes_semiconductor,
):
    """Returns a float value for the application factor (piA) on success."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = subcategory_id
    _attributes["application_id"] = application_id
    _attributes["duty_cycle"] = 65.0

    _attributes = semiconductor.calculate_application_factor(_attributes)

    assert isinstance(_attributes["piA"], float)
    if subcategory_id == 2 and application_id == 1:
        assert _attributes["piA"] == 0.5
    elif subcategory_id == 2 and application_id == 2:
        assert _attributes["piA"] == 2.5
    elif subcategory_id == 7 and application_id == 1:
        assert _attributes["piA"] == 7.6
    elif subcategory_id == 7 and application_id == 2:
        assert _attributes["piA"] == 0.439
    elif subcategory_id == 13 and application_id == 1:
        assert _attributes["piA"] == 4.4
    elif subcategory_id == 13 and application_id == 2:
        assert _attributes["piA"] == pytest.approx(0.80622577)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_application_factor_type_6(
    test_attributes_semiconductor,
):
    """Returns a float value for the application factor (piA) on success."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = 2
    _attributes["application_id"] = 1
    _attributes["type_id"] = 6

    _attributes = semiconductor.calculate_application_factor(_attributes)

    assert isinstance(_attributes["piA"], float)
    assert _attributes["piA"] == 0.5


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_application_factor_invalid_application_id(
    test_attributes_semiconductor,
):
    """Raises and IndexError when passed an invalid application ID."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = 4
    _attributes["application_id"] = 11
    _attributes["duty_cycle"] = 65.0
    with pytest.raises(
        IndexError,
        match=r"calculate_application_factor: Invalid semiconductor application ID 11.",
    ):
        semiconductor.calculate_application_factor(_attributes)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_application_factor_negative_duty_cycle(
    test_attributes_semiconductor,
):
    """Raises a ValueError when passed a negative value for the duty cycle."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = 13
    _attributes["application_id"] = 2
    _attributes["duty_cycle"] = -65.0
    with pytest.raises(
        ValueError,
        match=r"calculate_application_factor: Semiconductor duty cycle -65.0 must be "
        r"a value greater than or equal to 0.0.",
    ):
        _attributes = semiconductor.calculate_application_factor(_attributes)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
@pytest.mark.parametrize("subcategory_id", [2, 3, 10])
@pytest.mark.parametrize("type_id", [1, 4])
@pytest.mark.parametrize("power_rated", [0.075, 10.0])
def test_calculate_power_rating_factor(
    subcategory_id,
    type_id,
    power_rated,
    test_attributes_semiconductor,
):
    """Returns a float value for the power rating factor (piR) on success."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = subcategory_id
    _attributes["type_id"] = type_id
    _attributes["power_rated"] = power_rated
    _attributes["current_rated"] = 0.125
    _attributes = semiconductor.calculate_power_rating_factor(_attributes)

    assert isinstance(_attributes["piR"], float)
    if subcategory_id == 2 and type_id == 1:
        assert _attributes["piR"] == 1.0
    elif subcategory_id == 2 and type_id == 4 and power_rated == 10.0:
        assert _attributes["piR"] == pytest.approx(0.50064274)
    elif subcategory_id == 3 and power_rated == 0.075:
        assert _attributes["piR"] == 0.43
    elif subcategory_id == 3 and power_rated == 10.0:
        assert _attributes["piR"] == pytest.approx(2.34422882)
    elif subcategory_id == 10:
        assert _attributes["piR"] == pytest.approx(0.435275282)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_power_rating_factor_low_power_bjt(
    test_attributes_semiconductor,
):
    """Sets piR=0.43 for a low power BJT with rated power < 0.1W."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = 6
    _attributes["power_rated"] = 0.05

    _attributes = semiconductor.calculate_power_rating_factor(_attributes)

    assert _attributes["piR"] == 0.43


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_power_rating_factor_wrong_type(
    test_attributes_semiconductor,
):
    """Raises a TypeError when passed a string for rated current or rated power."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = 2
    _attributes["type_id"] = 4
    _attributes["power_rated"] = "10.0"
    _attributes["current_rated"] = 0.125
    with pytest.raises(
        TypeError,
        match=r"calculate_power_rating_factor: Semiconductor rated power <class 'str'> "
        r"and rated current <class 'float'> must be numerical types.",
    ):
        semiconductor.calculate_power_rating_factor(_attributes)

    _attributes["subcategory_id"] = 10
    _attributes["power_rated"] = 10.0
    _attributes["current_rated"] = "0.125"
    with pytest.raises(
        TypeError,
        match=r"calculate_power_rating_factor: Semiconductor rated power "
        r"<class 'float'> and rated current <class 'str'> must be numerical types.",
    ):
        semiconductor.calculate_power_rating_factor(_attributes)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_power_rating_factor_negative_input(
    test_attributes_semiconductor,
):
    """Raises a ValueError when passed a negative value for rated power."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = 2
    _attributes["type_id"] = 4
    _attributes["power_rated"] = -10.0
    _attributes["current_rated"] = 0.125
    with pytest.raises(
        ValueError,
        match=r"calculate_power_rating_factor: Semiconductor rated power -10.0 must "
        r"be a value greater than 0.0.",
    ):
        semiconductor.calculate_power_rating_factor(_attributes)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
@pytest.mark.parametrize("subcategory_id", [1, 3, 6, 10])
@pytest.mark.parametrize("type_id", [1, 6])
@pytest.mark.parametrize("voltage_ratio", [0.25, 0.75])
def test_calculate_electrical_stress_factor(
    subcategory_id,
    type_id,
    voltage_ratio,
    test_attributes_semiconductor,
):
    """Returns a float value for the electrical stress factor on success."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = subcategory_id
    _attributes["type_id"] = type_id
    _attributes["voltage_ratio"] = voltage_ratio
    _attributes = semiconductor.calculate_electrical_stress_factor(_attributes)

    assert isinstance(_attributes["piS"], float)
    if subcategory_id == 1 and type_id == 6:
        assert _attributes["piS"] == 1.0
    elif subcategory_id == 1 and voltage_ratio == 0.25:
        assert _attributes["piS"] == 0.054
    elif subcategory_id == 1 and voltage_ratio == 0.75:
        assert _attributes["piS"] == pytest.approx(0.49704862)
    elif subcategory_id == 3 and voltage_ratio == 0.25:
        assert _attributes["piS"] == pytest.approx(0.097676646)
    elif subcategory_id == 3 and voltage_ratio == 0.75:
        assert _attributes["piS"] == pytest.approx(0.4602006)
    elif subcategory_id == 6 and voltage_ratio == 0.25:
        assert _attributes["piS"] == pytest.approx(0.097676646)
    elif subcategory_id == 6 and voltage_ratio == 0.75:
        assert _attributes["piS"] == pytest.approx(0.4602006)
    elif subcategory_id == 10 and voltage_ratio == 0.25:
        assert _attributes["piS"] == 0.1
    elif subcategory_id == 10 and voltage_ratio == 0.75:
        assert _attributes["piS"] == pytest.approx(0.57891713)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 6, 7, 13])
def test_calculate_part_stress(
    subcategory_id,
    test_attributes_semiconductor,
):
    """Returns the semiconductor hardware attributes dict with updated values on
    success."""
    test_attributes_semiconductor["hazard_rate_active"] = 0.0038
    test_attributes_semiconductor["piE"] = 6.0
    test_attributes_semiconductor["piQ"] = 0.7
    test_attributes_semiconductor["subcategory_id"] = subcategory_id
    test_attributes_semiconductor["type_id"] = 1
    _attributes = semiconductor.calculate_part_stress(test_attributes_semiconductor)

    assert isinstance(_attributes, dict)
    if subcategory_id == 1:
        assert _attributes["temperature_junction"] == 45.7
        assert _attributes["piC"] == 1.0
        assert _attributes["piS"] == pytest.approx(0.14365026)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.004497037)
    elif subcategory_id == 2:
        assert _attributes["piA"] == 0.5
        assert _attributes["piR"] == 1.0
        assert _attributes["hazard_rate_active"] == pytest.approx(0.02511324)
    elif subcategory_id == 6:
        assert _attributes["piR"] == 1.0
        assert _attributes["piS"] == pytest.approx(0.18157386)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.004594019)
    elif subcategory_id == 7:
        assert _attributes["piM"] == 2.0
        assert _attributes["hazard_rate_active"] == pytest.approx(0.09134778)
    elif subcategory_id == 13:
        assert _attributes["piI"] == pytest.approx(0.10820637)
        assert _attributes["piP"] == pytest.approx(0.69444444)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.01449155)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_part_stress_invalid_construction_id(
    test_attributes_semiconductor,
):
    """Raises an IndexError when passed an invalid construction ID."""
    test_attributes_semiconductor["subcategory_id"] = 1
    test_attributes_semiconductor["construction_id"] = 5
    with pytest.raises(
        IndexError,
        match=r"calculate_part_stress: Invalid semiconductor construction ID 5 or "
        r"matching ID 2.",
    ):
        semiconductor.calculate_part_stress(test_attributes_semiconductor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_part_stress_no_matching(
    test_attributes_semiconductor,
):
    """Raises an IndexError when passed an invalid matching ID."""
    test_attributes_semiconductor["subcategory_id"] = 1
    test_attributes_semiconductor["construction_id"] = 1
    test_attributes_semiconductor["matching_id"] = 6
    with pytest.raises(
        IndexError,
        match=r"calculate_part_stress: Invalid semiconductor construction ID 1 "
        r"or matching ID 6.",
    ):
        semiconductor.calculate_part_stress(test_attributes_semiconductor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_part_stress_missing_attribute_key(
    test_attributes_semiconductor,
):
    """Raises a KeyError when a required attribute is missing."""
    test_attributes_semiconductor.pop("current_operating")
    with pytest.raises(
        KeyError,
        match=r"calculate_part_stress: Missing required semiconductor attribute: "
        r"'current_operating'.",
    ):
        semiconductor.calculate_part_stress(test_attributes_semiconductor)
