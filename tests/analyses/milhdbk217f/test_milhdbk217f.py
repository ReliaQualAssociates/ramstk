# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.test_milhdbk217f.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the milhdbk217f class."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import milhdbk217f

ATTRIBUTES = {
    'hardware_id': 12,
    'category_id': 4,
    'subcategory_id': 1,
    'add_adj_factor': 0.0,
    'application_id': 1,
    'area': 1.5,
    'capacitance': 0.0000033,
    'configuration_id': 1,
    'construction_id': 1,
    'contact_form_id': 1,
    'contact_gauge': 20,
    'contact_rating_id': 1,
    'current_operating': 0.14,
    'current_rated': 0.5,
    'current_ratio': 0.28,
    'duty_cycle': 100.0,
    'environment_active_id': 1,
    'family_id': 1,
    'feature_size': 1.5,
    'frequency_operating': 1.5,
    'hazard_rate_method_id': 1,
    'insert_id': 1,
    'insulation_id': 1,
    'matching_id': 1,
    'mult_adj_factor': 1.0,
    'n_active_pins': 14,
    'n_circuit_planes': 3,
    'n_cycles': 32,
    'n_elements': 8,
    'n_hand_soldered': 5,
    'n_wave_soldered': 138,
    'package_id': 1,
    'power_operating': 0.5,
    'power_rated': 0.75,
    'power_ratio': 0.67,
    'quality_id': 2,
    'quantity': 1,
    'resistance': 0.05,
    'specification_id': 1,
    'technology_id': 1,
    'temperature_active': 45.0,
    'temperature_case': 38.2,
    'temperature_rated_max': 105.0,
    'temperature_rise': 10.0,
    'theta_jc': 12.0,
    'type_id': 1,
    'voltage_ac_operating': 0.04,
    'voltage_dc_operating': 3.3,
    'voltage_rated': 12.0,
    'voltage_ratio': 0.54,
    'weight': 0.5,
    'years_in_production': 3,
    'hazard_rate_active': 0.0,
    'lambda_b': 0.0,
    'piE': 2.0,
    'piQ': 0.0
}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("category_id", [1, 3, 4, 5, 6, 7, 8, 9, 10])
@pytest.mark.parametrize("subcategory_id", [1, 2])
def test_get_part_count_quality_factor(category_id, subcategory_id):
    """_get_part_count_quality_factor() should return a float value for piQ on success."""
    ATTRIBUTES['type_id'] = 1
    _pi_q = milhdbk217f._get_part_count_quality_factor(category_id,
                                                       subcategory_id, 2)

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
        assert _pi_q == {1: 1.0, 3: 0.1, 4: 0.1, 5: 1.0, 8: 2.0}[category_id]


# ----- ----- ----- ----- BEGIN PARTS COUNT TESTS ----- ----- ----- ----- #
@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_do_calculate_part_count_integrated_circuit(subcategory_id):
    """_do_calculate_part_count() should return the integratedcircuit attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 1
    ATTRIBUTES['technology_id'] = 2
    if subcategory_id in [1, 2, 9]:
        ATTRIBUTES['n_elements'] = 1000
    elif subcategory_id == 3:
        ATTRIBUTES['n_elements'] = 256000
    elif subcategory_id == 4:
        ATTRIBUTES['n_elements'] = 16
    elif subcategory_id in [5, 6, 7, 8]:
        ATTRIBUTES['n_elements'] = 64000
    ATTRIBUTES['subcategory_id'] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(**ATTRIBUTES)

    assert isinstance(attributes, dict)
    assert attributes['lambda_b'] == {
        1: 0.033,
        2: 0.01,
        3: 0.0061,
        4: 0.093,
        5: 0.0059,
        6: 0.0061,
        7: 0.0055,
        8: 0.014,
        9: 0.0085
    }[attributes['subcategory_id']]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
def test_do_calculate_part_count_semiconductor(subcategory_id):
    """_do_calculate_part_count() should return the Semiconductor attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 2
    ATTRIBUTES['type_id'] = 1
    ATTRIBUTES['quality_id'] = 2
    ATTRIBUTES['subcategory_id'] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(**ATTRIBUTES)

    assert isinstance(attributes, dict)
    assert attributes['lambda_b'] == {
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
        13: 5.1
    }[attributes['subcategory_id']]
    assert attributes['piQ'] == {
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
        13: 1.0
    }[attributes['subcategory_id']]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
def test_do_calculate_part_count_resistor(subcategory_id):
    """_do_calculate_part_count() should return the Resistor attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 3
    ATTRIBUTES['subcategory_id'] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(**ATTRIBUTES)

    assert isinstance(attributes, dict)
    assert attributes['lambda_b'] == {
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
        15: 0.048
    }[attributes['subcategory_id']]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
def test_do_calculate_part_count_capacitor(subcategory_id):
    """_do_calculate_part_count() should return the Capacitor attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 4
    ATTRIBUTES['subcategory_id'] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(**ATTRIBUTES)

    assert isinstance(attributes, dict)
    assert attributes['lambda_b'] == {
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
        19: 0.4
    }[attributes['subcategory_id']]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
def test_do_calculate_part_count_inductor(subcategory_id):
    """_do_calculate_part_count() should return the Inductor attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 5
    ATTRIBUTES['subcategory_id'] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(**ATTRIBUTES)

    assert isinstance(attributes, dict)
    assert attributes['lambda_b'] == {
        1: 0.0035,
        2: 0.0017
    }[attributes['subcategory_id']]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
def test_do_calculate_part_count_relay(subcategory_id):
    """_do_calculate_part_count() should return the Relay attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 6
    ATTRIBUTES['subcategory_id'] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(**ATTRIBUTES)

    assert isinstance(attributes, dict)
    assert attributes['lambda_b'] == {
        1: 0.13,
        2: 0.4
    }[attributes['subcategory_id']]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5])
def test_do_calculate_part_count_switch(subcategory_id):
    """_do_calculate_part_count() should return the Switch attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 7
    ATTRIBUTES['subcategory_id'] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(**ATTRIBUTES)

    assert isinstance(attributes, dict)
    assert attributes['lambda_b'] == {
        1: 0.001,
        2: 0.15,
        3: 0.33,
        4: 0.56,
        5: 0.11
    }[attributes['subcategory_id']]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5])
def test_do_calculate_part_count_connection(subcategory_id):
    """_do_calculate_part_count() should return the Connection attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 8
    ATTRIBUTES['subcategory_id'] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(**ATTRIBUTES)

    assert isinstance(attributes, dict)
    assert attributes['lambda_b'] == {
        1: 0.011,
        2: 0.0054,
        3: 0.0019,
        4: 0.053,
        5: 0.0026
    }[attributes['subcategory_id']]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
def test_do_calculate_part_count_meter(subcategory_id):
    """_do_calculate_part_count() should return the Meter attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 9
    ATTRIBUTES['subcategory_id'] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(**ATTRIBUTES)

    assert isinstance(attributes, dict)
    assert attributes['lambda_b'] == {
        1: 10.0,
        2: 0.09
    }[attributes['subcategory_id']]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4])
def test_do_calculate_part_count_miscellaneous(subcategory_id):
    """_do_calculate_part_count() should return the misscellaneous component attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 10
    ATTRIBUTES['subcategory_id'] = subcategory_id
    attributes = milhdbk217f._do_calculate_part_count(**ATTRIBUTES)

    assert isinstance(attributes, dict)
    assert attributes['lambda_b'] == {
        1: 0.032,
        2: 0.022,
        3: 0.01,
        4: 3.9
    }[attributes['subcategory_id']]


# ----- ----- ----- ----- END PARTS COUNT TESTS ----- ----- ----- ----- #


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("category_id", [1, 2, 3, 4, 5, 7, 8, 9, 10])
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4])
def test_get_environment_factor(category_id, subcategory_id):
    """_get_environment_factor() should return a float value on success."""
    if category_id == 9 and subcategory_id in [3, 4]:
        subcategory_id = subcategory_id - 2
    _pi_e = milhdbk217f._get_environment_factor(category_id, subcategory_id, 1,
                                                1)

    assert isinstance(_pi_e, float)
    assert _pi_e == {
        1: {
            1: 0.5,
            2: 2.0,
            3: 4.0,
            4: 4.0
        },
        2: {
            1: 1.0,
            2: 6.0,
            3: 9.0,
            4: 9.0
        },
        3: {
            1: 1.0,
            2: 3.0,
            3: 8.0,
            4: 5.0
        },
        4: {
            1: 1.0,
            2: 6.0,
            3: 9.0,
            4: 9.0
        },
        5: {
            1: 1.0,
            2: 6.0,
            3: 12.0,
            4: 5.0
        },
        7: {
            1: 1.0,
            2: 3.0,
            3: 18.0,
            4: 8.0
        },
        8: {
            1: 1.0,
            2: 1.0,
            3: 8.0,
            4: 5.0
        },
        9: {
            1: 1.0,
            2: 2.0
        },
        10: {
            1: 1.0,
            2: 3.0,
            3: 10.0,
            4: 6.0
        }
    }[category_id][subcategory_id]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("category_id", [1, 3, 4, 6, 7, 8, 9, 10])
@pytest.mark.parametrize("subcategory_id", [1, 2])
def test_get_part_stress_quality_factor(category_id, subcategory_id):
    """_get_part_stress_quality_factor() should return a float value for piQ on success."""
    if category_id == 7:
        subcategory_id = 5
    elif category_id == 8:
        subcategory_id = subcategory_id + 3
    elif category_id == 9:
        subcategory_id = 2
    _pi_q = milhdbk217f._get_part_stress_quality_factor(
        category_id, subcategory_id, 2)

    assert isinstance(_pi_q, float)
    if category_id == 1:
        assert _pi_q == 1.0
    elif category_id == 3:
        assert _pi_q == 0.1
    elif category_id == 4 and subcategory_id == 1:
        assert _pi_q == 7.0
    elif category_id == 4 and subcategory_id == 2:
        assert _pi_q == 3.0
    elif category_id == 6 and subcategory_id == 1:
        assert _pi_q == 0.3
    elif category_id == 6 and subcategory_id == 2:
        assert _pi_q == 4.0
    elif category_id == 7:
        assert _pi_q == 8.4
    elif category_id == 8 and subcategory_id == 4:
        assert _pi_q == 2.0
    elif category_id == 8 and subcategory_id == 5:
        assert _pi_q == 1.0
    elif category_id == 9:
        assert _pi_q == 3.4
    elif category_id == 10 and subcategory_id == 1:
        assert _pi_q == 2.1
    elif category_id == 10 and subcategory_id == 2:
        assert _pi_q == 2.9


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_do_calculate_part_stress_integrated_circuit(subcategory_id):
    """_do_calculate_part_stress() should return the integratedcircuit attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 1
    ATTRIBUTES['technology_id'] = 2
    if subcategory_id in [1, 2, 9]:
        ATTRIBUTES['n_elements'] = 1000
    elif subcategory_id == 3:
        ATTRIBUTES['n_elements'] = 256000
    elif subcategory_id == 4:
        ATTRIBUTES['n_elements'] = 16
    elif subcategory_id in [5, 6, 7, 8]:
        ATTRIBUTES['n_elements'] = 64000
    ATTRIBUTES['subcategory_id'] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['hazard_rate_active'] == pytest.approx({
        1: 0.0179731104,
        2: 0.0028351463,
        3: 0.0031601411,
        4: 0.1151073357,
        5: 0.0085295868,
        6: 0.0020320013,
        7: 0.0017840729,
        8: 0.0056893704,
        9: 0.0017881831
    }[subcategory_id])


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
def test_do_calculate_part_stress_semiconductor(subcategory_id):
    """_do_calculate_stress_count() should return the Semiconductor attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 2
    ATTRIBUTES['subcategory_id'] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['lambda_b'] == {
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
        12: 0.430043,
        13: 3.23
    }[subcategory_id]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
def test_do_calculate_part_stress_resistor(subcategory_id):
    """_do_calculate_part_stress() should return the Resistor attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 3
    ATTRIBUTES['subcategory_id'] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['lambda_b'] == pytest.approx({
        1: 0.0011214964,
        2: 0.011448407,
        3: 0.019880339,
        4: 6e-05,
        5: 18.22977643,
        6: 0.059569839,
        7: 0.013394233,
        8: 0.021,
        9: 1.14863509,
        10: 6.5446862,
        11: 1.57184534,
        12: 0.51086149,
        13: 0.48906678,
        14: 2.46176874,
        15: 27.067582787
    }[subcategory_id])


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
def test_do_calculate_part_stress_capacitor(subcategory_id):
    """_do_calculate_part_stress() should return the Capacitor attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 4
    ATTRIBUTES['subcategory_id'] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['lambda_b'] == pytest.approx({
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
        19: 0.48854794
    }[subcategory_id])


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
def test_do_calculate_part_stress_inductor(subcategory_id):
    """_do_calculate_part_stress() should return the Inductor attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 5
    ATTRIBUTES['subcategory_id'] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['lambda_b'] == pytest.approx({
        1: 0.22012999,
        2: 0.040968637
    }[subcategory_id])


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
def test_do_calculate_part_stress_relay(subcategory_id):
    """_do_calculate_part_stress() should return the Relay attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 6
    ATTRIBUTES['subcategory_id'] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['lambda_b'] == pytest.approx({
        1: 0.0067988024,
        2: 0.4
    }[subcategory_id])


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 5])
def test_do_calculate_part_stress_switch(subcategory_id):
    """_do_calculate_part_stress() should return the Switch attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 7
    ATTRIBUTES['subcategory_id'] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['lambda_b'] == {1: 0.034, 5: 0.02}[subcategory_id]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5])
def test_do_calculate_part_stress_connection(subcategory_id):
    """_do_calculate_part_stress() should return the Connection attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 8
    ATTRIBUTES['subcategory_id'] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['hazard_rate_active'] == pytest.approx({
        1: 0.015571943,
        2: 0.0078040363,
        3: 0.0013176662,
        4: 0.020558237,
        5: 0.0026
    }[subcategory_id])


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
def test_do_calculate_part_stress_meter(subcategory_id):
    """_do_calculate_part_stress() should return the Meter attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 9
    ATTRIBUTES['subcategory_id'] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['lambda_b'] == {1: 20.0, 2: 0.09}[subcategory_id]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4])
def test_do_calculate_part_stress_miscellaneous(subcategory_id):
    """_do_calculate_part_stress() should return the misscellaneous component attribute dict with updated values on success."""
    ATTRIBUTES['category_id'] = 10
    ATTRIBUTES['piE'] = 10.0
    ATTRIBUTES['subcategory_id'] = subcategory_id
    _attributes = milhdbk217f._do_calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['hazard_rate_active'] == pytest.approx({
        1: 0.029968406,
        2: 0.0638,
        3: 0.01,
        4: 1.82547348
    }[subcategory_id])


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("hazard_rate_method_id", [1, 2])
def test_do_calculate_active_hazard_rate(hazard_rate_method_id):
    """do_calculate_active_hazard_rate() should return the component attribute dict with updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = hazard_rate_method_id

    def on_message(attributes):
        assert isinstance(attributes, dict)
        assert attributes['hazard_rate_active'] == {
            1: 3.9,
            2: 1.8254734762892308
        }[attributes['hazard_rate_method_id']]

    pub.subscribe(on_message, 'succeed_predict_reliability')

    milhdbk217f.do_predict_active_hazard_rate(**ATTRIBUTES)


@pytest.mark.unit
@pytest.mark.calculation
def test_do_calculate_active_hazard_rate_negative_input():
    """do_calculate_active_hazard_rate() should raise a ZeroDivisionError when passed a negative input for various components."""
    ATTRIBUTES['category_id'] = 2
    ATTRIBUTES['subcategory_id'] = 2
    ATTRIBUTES['type_id'] = 4
    ATTRIBUTES['power_rated'] = -0.05
    ATTRIBUTES['hazard_rate_method_id'] = 2

    def on_message(error_message):
        assert error_message == (
            'Failed to predict MIL-HDBK-217F hazard rate for '
            'hardware ID 12; one or more inputs has a '
            'negative or missing value. Hardware item '
            'category ID=2, subcategory ID=2, rated '
            'power=-0.050000, number of elements=1000.')

    pub.subscribe(on_message, 'fail_predict_reliability')

    milhdbk217f.do_predict_active_hazard_rate(**ATTRIBUTES)


@pytest.mark.unit
@pytest.mark.calculation
def test_do_calculate_active_hazard_rate_zero_input():
    """do_calculate_active_hazard_rate() should raise a ZeroDivisionError when passed an input equal to 0.0 for various components."""
    ATTRIBUTES['category_id'] = 4
    ATTRIBUTES['subcategory_id'] = 4
    ATTRIBUTES['voltage_ac_operating'] = 0.0
    ATTRIBUTES['voltage_dc_operating'] = 0.0
    ATTRIBUTES['hazard_rate_method_id'] = 2

    def on_message(error_message):
        assert error_message == (
            'Failed to predict MIL-HDBK-217F hazard rate for '
            'hardware ID 12; one or more inputs has a value '
            'of 0.0.  Hardware item category ID=4, '
            'subcategory ID=4, operating ac '
            'voltage=0.000000, operating DC '
            'voltage=0.000000, operating '
            'temperature=45.000000, temperature '
            'rise=10.000000, rated maximum '
            'temperature=105.000000, feature '
            'size=1.500000, surface area=1.500000, and item '
            'weight=0.500000.')

    pub.subscribe(on_message, 'fail_predict_reliability')

    milhdbk217f.do_predict_active_hazard_rate(**ATTRIBUTES)
