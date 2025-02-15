# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.test_milhdbk217f.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the milhdbk217f class."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import milhdbk217f


@pytest.mark.unit
@pytest.mark.parametrize("category_id", [1, 3, 4, 5, 6, 7, 8, 9, 10])
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.usefixtures("test_attributes")
def test_get_part_count_quality_factor(
    category_id,
    subcategory_id,
    test_attributes,
):
    """Returns a float value for the quality factor (piQ) on success."""
    test_attributes["category_id"] = category_id
    test_attributes["hazard_rate_method_id"] = 1
    test_attributes["subcategory_id"] = subcategory_id
    test_attributes["type_id"] = 1
    _pi_q = milhdbk217f._get_quality_factor(test_attributes)

    assert isinstance(_pi_q, float)
    if category_id == 6 and subcategory_id == 1:
        assert _pi_q == 3.0
    elif category_id == 6 and subcategory_id == 2:
        assert _pi_q == 1.0
    elif category_id == 7 and subcategory_id == 1:
        assert _pi_q == 20.0
    elif category_id == 7 and subcategory_id == 2:
        assert _pi_q == 20.0
    elif category_id == 9 and subcategory_id == 1:
        assert _pi_q == 1.0
    elif category_id == 9 and subcategory_id == 2:
        assert _pi_q == 3.4
    elif category_id == 10 and subcategory_id == 1:
        assert _pi_q == 3.4
    elif category_id == 10 and subcategory_id == 2:
        assert _pi_q == 2.9
    else:
        assert (
            _pi_q
            == {
                1: 1.0,
                3: 0.1,
                4: 0.1,
                5: 1.0,
                8: 2.0,
            }[category_id]
        )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5, 6, 7, 8, 9])
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_count_integrated_circuit(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 1
    test_attributes["technology_id"] = 2
    if subcategory_id in [1, 2, 9]:
        test_attributes["n_elements"] = 1000
    elif subcategory_id == 3:
        test_attributes["n_elements"] = 256000
    elif subcategory_id == 4:
        test_attributes["n_elements"] = 16
    elif subcategory_id in [5, 6, 7, 8]:
        test_attributes["n_elements"] = 64000
    test_attributes["subcategory_id"] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(test_attributes)

    assert isinstance(attributes, dict)
    assert (
        attributes["lambda_b"]
        == {
            1: 0.033,
            2: 0.01,
            3: 0.0061,
            4: 0.093,
            5: 0.0059,
            6: 0.0061,
            7: 0.0055,
            8: 0.014,
            9: 0.0085,
        }[attributes["subcategory_id"]]
    )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_count_semiconductor(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 2
    test_attributes["type_id"] = 1
    test_attributes["quality_id"] = 2
    test_attributes["subcategory_id"] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(test_attributes)

    assert isinstance(attributes, dict)
    assert (
        attributes["lambda_b"]
        == {
            1: 0.0036,
            2: 0.86,
            3: 0.00015,
            4: 0.014,
            5: 0.016,
            6: 0.094,
            7: 0.074,
            8: 0.17,
            9: 0.014,
            10: 0.0025,
            11: 0.011,
            12: 0.0062,
            13: 5.1,
        }[attributes["subcategory_id"]]
    )
    assert (
        attributes["piQ"]
        == {
            1: 1.0,
            2: 1.0,
            3: 1.0,
            4: 1.0,
            5: 1.0,
            6: 1.0,
            7: 1.0,
            8: 1.0,
            9: 1.0,
            10: 1.0,
            11: 1.0,
            12: 1.0,
            13: 1.0,
        }[attributes["subcategory_id"]]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
)
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_count_resistor(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 3
    test_attributes["subcategory_id"] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(test_attributes)

    assert isinstance(attributes, dict)
    assert (
        attributes["lambda_b"]
        == {
            1: 0.0005,
            2: 0.0012,
            3: 0.012,
            4: 0.0023,
            5: 0.0085,
            6: 0.014,
            7: 0.008,
            8: 0.065,
            9: 0.025,
            10: 0.33,
            11: 0.15,
            12: 0.15,
            13: 0.043,
            14: 0.05,
            15: 0.048,
        }[attributes["subcategory_id"]]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
)
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_count_capacitor(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 4
    test_attributes["subcategory_id"] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(test_attributes)

    assert isinstance(attributes, dict)
    assert (
        attributes["lambda_b"]
        == {
            1: 0.0036,
            2: 0.0047,
            3: 0.0021,
            4: 0.0029,
            5: 0.0041,
            6: 0.0023,
            7: 0.0005,
            8: 0.018,
            9: 0.00032,
            10: 0.0036,
            11: 0.00078,
            12: 0.0018,
            13: 0.0061,
            14: 0.024,
            15: 0.029,
            16: 0.08,
            17: 0.033,
            18: 0.8,
            19: 0.4,
        }[attributes["subcategory_id"]]
    )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_count_inductor(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 5
    test_attributes["subcategory_id"] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(test_attributes)

    assert isinstance(attributes, dict)
    assert (
        attributes["lambda_b"]
        == {
            1: 0.0035,
            2: 0.0017,
        }[attributes["subcategory_id"]]
    )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_count_relay(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 6
    test_attributes["subcategory_id"] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(test_attributes)

    assert isinstance(attributes, dict)
    assert (
        attributes["lambda_b"]
        == {
            1: 0.13,
            2: 0.4,
        }[attributes["subcategory_id"]]
    )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5])
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_count_switch(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 7
    test_attributes["subcategory_id"] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(test_attributes)

    assert isinstance(attributes, dict)
    assert (
        attributes["lambda_b"]
        == {
            1: 0.001,
            2: 0.15,
            3: 0.33,
            4: 0.56,
            5: 0.11,
        }[attributes["subcategory_id"]]
    )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5])
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_count_connection(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 8
    test_attributes["subcategory_id"] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(test_attributes)

    assert isinstance(attributes, dict)
    assert (
        attributes["lambda_b"]
        == {
            1: 0.011,
            2: 0.0054,
            3: 0.0019,
            4: 0.053,
            5: 0.0026,
        }[attributes["subcategory_id"]]
    )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_count_meter(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 9
    test_attributes["subcategory_id"] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(test_attributes)

    assert isinstance(attributes, dict)
    assert (
        attributes["lambda_b"]
        == {
            1: 10.0,
            2: 0.09,
        }[attributes["subcategory_id"]]
    )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4])
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_count_miscellaneous(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 10
    test_attributes["subcategory_id"] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(test_attributes)

    assert isinstance(attributes, dict)
    assert (
        attributes["lambda_b"]
        == {
            1: 0.032,
            2: 0.022,
            3: 0.01,
            4: 3.9,
        }[attributes["subcategory_id"]]
    )


@pytest.mark.unit
@pytest.mark.parametrize("category_id", [1, 4])
@pytest.mark.parametrize(
    "environment_active_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
@pytest.mark.usefixtures("test_attributes")
def test_get_environment_factor_pi_e_list(
    category_id,
    environment_active_id,
    test_attributes,
):
    """Returns a float value for the environment factor (piE) on success.

    This tests the component types with environment factors lists that are not
    subcategory dependent.
    """
    test_attributes["category_id"] = category_id
    test_attributes["environment_active_id"] = environment_active_id
    _pi_e = milhdbk217f._get_environment_factor(test_attributes)

    assert isinstance(_pi_e, float)
    assert (
        _pi_e
        == {
            1: [
                0.5,
                2.0,
                4.0,
                4.0,
                6.0,
                4.0,
                5.0,
                5.0,
                8.0,
                8.0,
                0.5,
                5.0,
                12.0,
                220.0,
            ],
            4: [
                1.0,
                6.0,
                9.0,
                9.0,
                19.0,
                13.0,
                29.0,
                20.0,
                43.0,
                24.0,
                0.5,
                14.0,
                32.0,
                320.0,
            ],
        }[category_id][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.parametrize("category_id", [2, 3, 5, 7, 9, 10])
@pytest.mark.parametrize(
    "environment_active_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.usefixtures("test_attributes")
def test_get_environment_factor_pi_e_dict(
    category_id,
    environment_active_id,
    subcategory_id,
    test_attributes,
):
    """Returns a float value for the environment factor (piE) on success.

    This tests the component types with environment factors lists that are subcategory
    dependent.
    """
    test_attributes["category_id"] = category_id
    test_attributes["environment_active_id"] = environment_active_id
    test_attributes["subcategory_id"] = subcategory_id
    _pi_e = milhdbk217f._get_environment_factor(test_attributes)

    assert isinstance(_pi_e, float)
    assert (
        _pi_e
        == {
            2: {
                1: [
                    1.0,
                    6.0,
                    9.0,
                    9.0,
                    19.0,
                    13.0,
                    29.0,
                    20.0,
                    43.0,
                    24.0,
                    0.5,
                    14.0,
                    32.0,
                    320.0,
                ],
                2: [
                    1.0,
                    2.0,
                    5.0,
                    4.0,
                    11.0,
                    4.0,
                    5.0,
                    7.0,
                    12.0,
                    16.0,
                    0.5,
                    9.0,
                    24.0,
                    250.0,
                ],
            },
            3: {
                1: [
                    1.0,
                    3.0,
                    8.0,
                    5.0,
                    13.0,
                    4.0,
                    5.0,
                    7.0,
                    11.0,
                    19.0,
                    0.5,
                    11.0,
                    27.0,
                    490.0,
                ],
                2: [
                    1.0,
                    2.0,
                    8.0,
                    4.0,
                    14.0,
                    4.0,
                    8.0,
                    10.0,
                    18.0,
                    19.0,
                    0.2,
                    10.0,
                    28.0,
                    510.0,
                ],
            },
            5: {
                1: [
                    1.0,
                    6.0,
                    12.0,
                    5.0,
                    16.0,
                    6.0,
                    8.0,
                    7.0,
                    9.0,
                    24.0,
                    0.5,
                    13.0,
                    34.0,
                    610.0,
                ],
                2: [
                    1.0,
                    4.0,
                    12.0,
                    5.0,
                    16.0,
                    5.0,
                    7.0,
                    6.0,
                    8.0,
                    24.0,
                    0.5,
                    13.0,
                    34.0,
                    610.0,
                ],
            },
            7: {
                1: [
                    1.0,
                    3.0,
                    18.0,
                    8.0,
                    29.0,
                    10.0,
                    18.0,
                    13.0,
                    22.0,
                    46.0,
                    0.5,
                    25.0,
                    67.0,
                    1200.0,
                ],
                2: [
                    1.0,
                    3.0,
                    18.0,
                    8.0,
                    29.0,
                    10.0,
                    18.0,
                    13.0,
                    22.0,
                    46.0,
                    0.5,
                    25.0,
                    67.0,
                    1200.0,
                ],
            },
            9: {
                1: [
                    1.0,
                    2.0,
                    12.0,
                    7.0,
                    18.0,
                    5.0,
                    8.0,
                    16.0,
                    25.0,
                    26.0,
                    0.5,
                    14.0,
                    38.0,
                    0.0,
                ],
                2: [
                    1.0,
                    4.0,
                    25.0,
                    12.0,
                    35.0,
                    28.0,
                    42.0,
                    58.0,
                    73.0,
                    60.0,
                    1.1,
                    60.0,
                    0.0,
                    0.0,
                ],
            },
            10: {
                1: [
                    1.0,
                    3.0,
                    10.0,
                    6.0,
                    16.0,
                    12.0,
                    17.0,
                    22.0,
                    28.0,
                    23.0,
                    0.5,
                    13.0,
                    32.0,
                    500.0,
                ],
                2: [
                    1.0,
                    2.0,
                    6.0,
                    4.0,
                    9.0,
                    7.0,
                    9.0,
                    11.0,
                    13.0,
                    11.0,
                    0.8,
                    7.0,
                    15.0,
                    120.0,
                ],
            },
        }[category_id][subcategory_id][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
@pytest.mark.usefixtures("test_attributes")
def test_get_environment_factor_pi_e_list_or_dict(
    environment_active_id,
    test_attributes,
):
    """Returns a float value for the environment factor (piE) on success.

    This tests the component types with environment factors lists that are sometimes
    subcategory dependent and sometimes subcategory with another parameter dependent.
    """
    test_attributes["category_id"] = 6
    test_attributes["environment_active_id"] = environment_active_id
    test_attributes["quality_id"] = 1
    test_attributes["subcategory_id"] = 1
    _pi_e = milhdbk217f._get_environment_factor(test_attributes)

    assert isinstance(_pi_e, float)
    assert (
        _pi_e
        == [
            1.0,
            2.0,
            15.0,
            8.0,
            27.0,
            7.0,
            9.0,
            11.0,
            12.0,
            46.0,
            0.50,
            25.0,
            66.0,
            0.0,
        ][environment_active_id - 1]
    )

    test_attributes["environment_active_id"] = environment_active_id
    test_attributes["subcategory_id"] = 2
    _pi_e = milhdbk217f._get_environment_factor(test_attributes)

    assert isinstance(_pi_e, float)
    assert (
        _pi_e
        == [
            1.0,
            3.0,
            12.0,
            6.0,
            17.0,
            12.0,
            19.0,
            21.0,
            32.0,
            23.0,
            0.4,
            12.0,
            33.0,
            590.0,
        ][environment_active_id - 1]
    )
    test_attributes["category_id"] = 8
    test_attributes["environment_active_id"] = environment_active_id
    test_attributes["quality_id"] = 1
    test_attributes["subcategory_id"] = 1
    _pi_e = milhdbk217f._get_environment_factor(test_attributes)

    assert isinstance(_pi_e, float)
    assert (
        _pi_e
        == [
            1.0,
            1.0,
            8.0,
            5.0,
            13.0,
            3.0,
            5.0,
            8.0,
            12.0,
            19.0,
            0.5,
            10.0,
            27.0,
            490.0,
        ][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.parametrize("category_id", [1, 2, 3, 4, 6, 7, 9])
@pytest.mark.usefixtures("test_attributes")
def test_get_part_stress_quality_factor(
    category_id,
    test_attributes,
):
    """Returns a float value for the quality factor (piQ) on success."""
    test_attributes["category_id"] = category_id
    test_attributes["hazard_rate_method_id"] = 2
    test_attributes["quality_id"] = 1
    test_attributes["subcategory_id"] = 1
    _pi_q = milhdbk217f._get_quality_factor(test_attributes)

    assert isinstance(_pi_q, float)
    assert (
        _pi_q == {1: 0.25, 2: 0.7, 3: 0.03, 4: 3.0, 6: 0.1, 7: 1.0, 9: 1.0}[category_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5, 6, 7, 8, 9])
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_stress_integrated_circuit(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 1
    test_attributes["hazard_rate_method_id"] = 2
    test_attributes["technology_id"] = 2
    if subcategory_id in [1, 2, 9]:
        test_attributes["n_elements"] = 1000
    elif subcategory_id == 3:
        test_attributes["n_elements"] = 256000
    elif subcategory_id == 4:
        test_attributes["n_elements"] = 16
    elif subcategory_id in [5, 6, 7, 8]:
        test_attributes["n_elements"] = 64000
    test_attributes["subcategory_id"] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(test_attributes)

    assert isinstance(_attributes, dict)
    assert _attributes["hazard_rate_active"] == pytest.approx(
        {
            1: 0.0179731104,
            2: 0.0028351463,
            3: 0.0031601411,
            4: 0.1151073357,
            5: 0.0085295868,
            6: 0.0020320013,
            7: 0.0017840729,
            8: 0.0056893704,
            9: 0.0017881831,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_stress_semiconductor(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 2
    test_attributes["hazard_rate_method_id"] = 2
    test_attributes["subcategory_id"] = subcategory_id
    test_attributes["type_id"] = 1
    _attributes = milhdbk217f._do_calculate_part_stress(test_attributes)

    assert isinstance(_attributes, dict)
    assert (
        _attributes["lambda_b"]
        == {
            1: 0.0038,
            2: 0.22,
            3: 0.00074,
            4: 0.012,
            5: 0.0083,
            6: 0.18,
            7: 0.05457227133806658,
            8: 0.022567580836231026,
            9: 0.06,
            10: 0.0022,
            11: 0.0055,
            12: 0.003483,
            13: 3.23,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
)
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_stress_resistor(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 3
    test_attributes["hazard_rate_method_id"] = 2
    test_attributes["subcategory_id"] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(test_attributes)

    assert isinstance(_attributes, dict)
    assert _attributes["lambda_b"] == pytest.approx(
        {
            1: 0.0011214964,
            2: 0.011448407,
            3: 0.0271525,
            4: 6e-05,
            5: 29.4960372,
            6: 0.059569839,
            7: 0.013394233,
            8: 0.021,
            9: 1.14863509,
            10: 4.3626779,
            11: 0.6693008,
            12: 0.2991167,
            13: 0.3569577,
            14: 1.2913242,
            15: 17.4152588,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
)
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_stress_capacitor(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 4
    test_attributes["hazard_rate_method_id"] = 2
    test_attributes["subcategory_id"] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(test_attributes)

    assert isinstance(_attributes, dict)
    assert _attributes["lambda_b"] == pytest.approx(
        {
            1: 0.029446888,
            2: 0.039376653,
            3: 0.017120284,
            4: 0.023625992,
            5: 0.033898162,
            6: 0.018832312,
            7: 0.0020862349,
            8: 0.027466957,
            9: 0.0013652039,
            10: 0.0047536583,
            11: 0.0029795643,
            12: 0.022463773,
            13: 0.0098840599,
            14: 0.049020516,
            15: 0.023826308,
            16: 0.097709587,
            17: 0.10353372,
            18: 0.091220763,
            19: 0.48854794,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_stress_inductor(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 5
    test_attributes["hazard_rate_method_id"] = 2
    test_attributes["subcategory_id"] = subcategory_id
    test_attributes["temperature_hot_spot"] = 103.4
    _attributes = milhdbk217f._do_calculate_part_stress(test_attributes)

    assert isinstance(_attributes, dict)
    assert _attributes["lambda_b"] == pytest.approx(
        {1: 0.22012999, 2: 0.040968637}[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_stress_relay(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 6
    test_attributes["hazard_rate_method_id"] = 2
    test_attributes["subcategory_id"] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(test_attributes)

    assert isinstance(_attributes, dict)
    assert _attributes["lambda_b"] == pytest.approx(
        {1: 0.0067988024, 2: 0.4}[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 5])
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_stress_switch(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 7
    test_attributes["hazard_rate_method_id"] = 2
    test_attributes["subcategory_id"] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(test_attributes)

    assert isinstance(_attributes, dict)
    assert _attributes["lambda_b"] == {1: 0.034, 5: 0.02}[subcategory_id]


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5])
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_stress_connection(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 8
    test_attributes["hazard_rate_method_id"] = 2
    test_attributes["lambda_b"] = 0.004963485
    test_attributes["subcategory_id"] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(test_attributes)

    assert isinstance(_attributes, dict)
    assert _attributes["hazard_rate_active"] == pytest.approx(
        {1: 0.004963485, 2: 0.004963485, 3: 0.003952999, 4: 0.03083736, 5: 0.0078}[
            subcategory_id
        ]
    )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_stress_meter(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 9
    test_attributes["hazard_rate_method_id"] = 2
    test_attributes["subcategory_id"] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(test_attributes)

    assert isinstance(_attributes, dict)
    assert _attributes["lambda_b"] == {1: 20.0, 2: 0.09}[subcategory_id]


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4])
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_part_stress_miscellaneous(
    subcategory_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["category_id"] = 10
    test_attributes["hazard_rate_method_id"] = 2
    test_attributes["piE"] = 10.0
    test_attributes["subcategory_id"] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(test_attributes)

    assert isinstance(_attributes, dict)
    assert _attributes["hazard_rate_active"] == pytest.approx(
        {1: 0.01427067, 2: 0.0638, 3: 0.01, 4: 1.82547348}[subcategory_id]
    )
