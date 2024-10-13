# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.test_similaritem.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the similar item assessment module."""

# Standard Library Imports
from collections import OrderedDict

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses import similaritem

TEST_SIA = OrderedDict(
    {
        _key: None
        for _key in [
            "hr",
            "pi1",
            "pi2",
            "pi3",
            "pi3",
            "pi4",
            "pi5",
            "pi6",
            "pi7",
            "pi8",
            "pi9",
            "pi10",
            "uf1",
            "uf2",
            "uf3",
            "uf4",
            "uf5",
            "ui1",
            "ui2",
            "ui3",
            "ui4",
            "ui5",
            "equation1",
            "equation2",
            "equation3",
            "equation4",
            "equation5",
            "res1",
            "res2",
            "res3",
            "res4",
            "res5",
        ]
    }
)
TEST_SIA["hr"] = 0.0003825

test_user_functions = [
    "hr*pi1*pi2*uf1",
    "ui1+ui2",
    "res2*pi4",
    "res1-uf3",
    "hr*(pi3+pi5)",
]


@pytest.mark.unit
def test_calculate_topic_633():
    """calculate_topic_633() should return a tuple of change factors and the result of
    the calculation on success."""
    environment = {"from": 4, "to": 6}
    quality = {"from": 2, "to": 3}
    temperature = {"from": 38.0, "to": 27.5}

    (
        _change_factor_1,
        _change_factor_2,
        _change_factor_3,
        _result_1,
    ) = similaritem.calculate_topic_633(environment, quality, temperature, 0.000003335)
    assert _change_factor_1 == pytest.approx(0.6)
    assert _change_factor_2 == pytest.approx(3.3)
    assert _change_factor_3 == pytest.approx(1.1)
    assert _result_1 == pytest.approx(1.5312213e-06)


@pytest.mark.unit
def test_calculate_topic_633_quality_key_error():
    """calculate_topic_633() should raise a KeyError when passed a quality dict that is
    missing a from or to key."""
    environment = {"from": 4, "to": 6}
    quality = {"from": 2}
    temperature = {"from": 38.0, "to": 27.5}

    with pytest.raises(KeyError):
        (
            _change_factor_1,
            _change_factor_2,
            _change_factor_3,
            _result_1,
        ) = similaritem.calculate_topic_633(
            environment, quality, temperature, 0.000003335
        )

    quality = {"from": 2, "to": "3"}

    with pytest.raises(KeyError):
        (
            _change_factor_1,
            _change_factor_2,
            _change_factor_3,
            _result_1,
        ) = similaritem.calculate_topic_633(
            environment, quality, temperature, 0.000003335
        )


@pytest.mark.unit
def test_calculate_topic_633_environment_key_error():
    """calculate_topic_633() should raise a KeyError when passed an environment dict
    that is missing a from or to key."""
    environment = {"to": 6}
    quality = {"from": 2, "to": 4}
    temperature = {"from": 38.0, "to": 27.5}

    with pytest.raises(KeyError):
        (
            _change_factor_1,
            _change_factor_2,
            _change_factor_3,
            _result_1,
        ) = similaritem.calculate_topic_633(
            environment, quality, temperature, 0.000003335
        )

    environment = {"from": "4", "to": 6}

    with pytest.raises(KeyError):
        (
            _change_factor_1,
            _change_factor_2,
            _change_factor_3,
            _result_1,
        ) = similaritem.calculate_topic_633(
            environment, quality, temperature, 0.000003335
        )


@pytest.mark.unit
def test_calculate_topic_633_temperature_key_error():
    """calculate_topic_633() should raise a KeyError when passed a temperature dict that
    is missing a from or to key."""
    environment = {"from": 4, "to": 6}
    quality = {"from": 2, "to": 4}
    temperature = {"from": 38.0}

    with pytest.raises(KeyError):
        (
            _change_factor_1,
            _change_factor_2,
            _change_factor_3,
            _result_1,
        ) = similaritem.calculate_topic_633(
            environment, quality, temperature, 0.000003335
        )


@pytest.mark.unit
def test_calculate_topic_633_temperature_string_value():
    """calculate_topic_633() should raise a TypeError when passed a string for one or
    more temperature values."""
    environment = {"from": 4, "to": 6}
    quality = {"from": 2, "to": 4}
    temperature = {"from": "38.0", "to": 27.5}

    with pytest.raises(TypeError):
        (
            _change_factor_1,
            _change_factor_2,
            _change_factor_3,
            _result_1,
        ) = similaritem.calculate_topic_633(
            environment, quality, temperature, 0.000003335
        )


@pytest.mark.unit
def test_set_user_defined_change_factors():
    """set_user_defined_change_factors() should return an updated similar item
    assessment dict on success."""
    _sia = similaritem.set_user_defined_change_factors(
        TEST_SIA, [1.2, 3.4, 5.6, 7.8, 9.10, 11.12, 13.14, 15.16, 17.18, 19.2]
    )

    assert isinstance(_sia, dict)
    assert _sia["pi1"] == pytest.approx(1.2)
    assert _sia["pi2"] == pytest.approx(3.4)
    assert _sia["pi3"] == pytest.approx(5.6)
    assert _sia["pi4"] == pytest.approx(7.8)
    assert _sia["pi5"] == pytest.approx(9.10)
    assert _sia["pi6"] == pytest.approx(11.12)
    assert _sia["pi7"] == pytest.approx(13.14)
    assert _sia["pi8"] == pytest.approx(15.16)
    assert _sia["pi9"] == pytest.approx(17.18)
    assert _sia["pi10"] == pytest.approx(19.20)


@pytest.mark.unit
def test_set_user_defined_change_factors_set_unused_none():
    """set_user_defined_change_factors() should set unused factors to None."""
    _sia = similaritem.set_user_defined_change_factors(
        TEST_SIA, [1.2, 3.4, 5.6, 7.8, 9.10]
    )

    assert isinstance(_sia, dict)
    assert _sia["pi1"] == pytest.approx(1.2)
    assert _sia["pi2"] == pytest.approx(3.4)
    assert _sia["pi3"] == pytest.approx(5.6)
    assert _sia["pi4"] == pytest.approx(7.8)
    assert _sia["pi5"] == pytest.approx(9.10)
    assert _sia["pi6"] == pytest.approx(0.0)
    assert _sia["pi7"] == pytest.approx(0.0)
    assert _sia["pi8"] == pytest.approx(0.0)
    assert _sia["pi9"] == pytest.approx(0.0)
    assert _sia["pi10"] == pytest.approx(0.0)


@pytest.mark.unit
def test_set_user_defined_floats():
    """set_user_defined_floats() should return an updated similar item assessment dict
    on success."""
    _sia = similaritem.set_user_defined_floats(TEST_SIA, [3.4, 7.8, 11.12, 15.16, 19.2])

    assert isinstance(_sia, dict)
    assert _sia["uf1"] == pytest.approx(3.4)
    assert _sia["uf2"] == pytest.approx(7.8)
    assert _sia["uf3"] == pytest.approx(11.12)
    assert _sia["uf4"] == pytest.approx(15.16)
    assert _sia["uf5"] == pytest.approx(19.2)


@pytest.mark.unit
def test_set_user_defined_floats_set_unused_none():
    """set_user_defined_floats() should set unused floats to None."""
    _sia = similaritem.set_user_defined_floats(TEST_SIA, [3.4, 7.8])

    assert isinstance(_sia, dict)
    assert _sia["uf1"] == pytest.approx(3.4)
    assert _sia["uf2"] == pytest.approx(7.8)
    assert _sia["uf3"] == pytest.approx(0.0)
    assert _sia["uf4"] == pytest.approx(0.0)
    assert _sia["uf5"] == pytest.approx(0.0)


@pytest.mark.unit
def test_set_user_defined_ints():
    """set_user_defined_ints() should return an updated similar item assessment dict on
    success."""
    _sia = similaritem.set_user_defined_ints(TEST_SIA, [3.4, 7.8, 11.12, 15.16, 19.2])

    assert isinstance(_sia, dict)
    assert _sia["ui1"] == 3
    assert _sia["ui2"] == 7
    assert _sia["ui3"] == 11
    assert _sia["ui4"] == 15
    assert _sia["ui5"] == 19


@pytest.mark.unit
def test_set_user_defined_ints_set_unused_none():
    """set_user_defined_ints() should set unused ints to None."""
    _sia = similaritem.set_user_defined_ints(TEST_SIA, [3.4, 7.8, 11.12])

    assert isinstance(_sia, dict)
    assert _sia["ui1"] == 3
    assert _sia["ui2"] == 7
    assert _sia["ui3"] == 11
    assert _sia["ui4"] == 0
    assert _sia["ui5"] == 0


@pytest.mark.unit
def test_set_user_defined_functions():
    """set_user_defined_functions() should return an updated similar item assessment
    dict on success."""
    _sia = similaritem.set_user_defined_functions(TEST_SIA, test_user_functions)

    assert isinstance(_sia, dict)
    assert _sia["equation1"] == test_user_functions[0]
    assert _sia["equation2"] == test_user_functions[1]
    assert _sia["equation3"] == test_user_functions[2]
    assert _sia["equation4"] == test_user_functions[3]
    assert _sia["equation5"] == test_user_functions[4]


@pytest.mark.unit
def test_set_user_defined_functions_set_unused_none():
    """set_user_defined_functions() should set unused functiosn to None."""
    _sia = similaritem.set_user_defined_functions(TEST_SIA, test_user_functions[:2])

    assert isinstance(_sia, dict)
    assert _sia["equation1"] == test_user_functions[0]
    assert _sia["equation2"] == test_user_functions[1]
    assert _sia["equation3"] == ""
    assert _sia["equation4"] == ""
    assert _sia["equation5"] == ""


@pytest.mark.unit
def test_set_user_defined_results():
    """set_user_defined_results() should return an updated similar item assessment dict
    on success."""
    _sia = similaritem.set_user_defined_results(
        TEST_SIA, [3.4, 7.8, 11.12, 15.16, 19.2]
    )

    assert isinstance(_sia, dict)
    assert _sia["res1"] == pytest.approx(3.4)
    assert _sia["res2"] == pytest.approx(7.8)
    assert _sia["res3"] == pytest.approx(11.12)
    assert _sia["res4"] == pytest.approx(15.16)
    assert _sia["res5"] == pytest.approx(19.2)


@pytest.mark.unit
def test_set_user_defined_results_set_unused_none():
    """set_user_defined_results() should set unused results to None."""
    _sia = similaritem.set_user_defined_results(TEST_SIA, [3.4, 7.8, 11.12, 15.16])

    assert isinstance(_sia, dict)
    assert _sia["res1"] == pytest.approx(3.4)
    assert _sia["res2"] == pytest.approx(7.8)
    assert _sia["res3"] == pytest.approx(11.12)
    assert _sia["res4"] == pytest.approx(15.16)
    assert _sia["res5"] == pytest.approx(0.0)


@pytest.mark.unit
def test_calculate_user_defined():
    """calculate_user_defined() should return an updated similar item assessment dict on
    success."""
    _sia = similaritem.set_user_defined_change_factors(
        TEST_SIA, [1.2, 3.4, 5.6, 7.8, 9.10, 11.12, 13.14, 15.16, 17.18, 19.2]
    )
    _sia = similaritem.set_user_defined_functions(_sia, test_user_functions)
    _sia = similaritem.calculate_user_defined(_sia)

    assert isinstance(_sia, dict)
    assert _sia["res1"] == pytest.approx(0.00530604)
    assert _sia["res2"] == pytest.approx(10.0)
    assert _sia["res3"] == pytest.approx(78.0)
    assert _sia["res4"] == pytest.approx(0.00530604)
    assert _sia["res5"] == pytest.approx(0.00562275)


@pytest.mark.unit
def test_calculate_topic_633_invalid_temperature():
    with pytest.raises(TypeError):
        similaritem.calculate_topic_633(
            environment={"from": 1, "to": 2},
            quality={"from": 1, "to": 2},
            temperature={"from": "hot", "to": 30},  # Invalid string value
            hazard_rate=0.01,
        )


@pytest.mark.unit
def test_calculate_user_defined_empty_equation():
    TEST_SIA["equation1"] = ""
    TEST_SIA["equation2"] = "pi1 + pi2"

    updated_sia = similaritem.calculate_user_defined(TEST_SIA)
    assert updated_sia["equation1"] == "0.0"
