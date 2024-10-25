# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdk217f.models.connection.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Connection MIL-HDBK-217F Constants and Calculations Module."""

# Standard Library Imports
from math import exp
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.constants.connection.constants import (
    FACTOR_KEYS,
    INSERT_TEMP_FACTORS,
    LAMBDA_B_FACTORS,
    PART_COUNT_LAMBDA_B,
    PART_COUNT_PI_Q,
    PART_STRESS_LAMBDA_B,
    PART_STRESS_PI_Q,
    PI_E,
    PI_K,
    REF_TEMPS,
)


def calculate_part_count(**attributes: Dict[str, int]) -> float:
    """Wrap get_part_count_lambda_b().

    This wrapper allows us to pass an attribute dict from a generic parts count
    function.

    :param attributes: the attributes for the connection being calculated.
    :return: _base_hr; the parts count base hazard rates.
    :rtype: float
    """
    _subcategory_id = attributes["subcategory_id"]
    _environment_active_id = attributes["environment_active_id"]
    _type_id = attributes["type_id"]
    _quality_id = attributes["quality_id"]

    _part_count_lambda_b = _get_part_count_lambda_b(
        _subcategory_id, _environment_active_id, _type_id
    )
    _pi_q = PART_COUNT_PI_Q[_quality_id]

    return _part_count_lambda_b * _pi_q


def calculate_part_stress(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress active hazard rate for a connection.

    This function calculates the MIL-HDBK-217F hazard rate using the part stress method.

    :param attributes: the attributes for the connection being calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary with
        updated values.
    :rtype: dict
    """
    attributes["temperature_rise"] = _calculate_insert_temperature(
        attributes["contact_gauge"], attributes["current_operating"]
    )
    attributes["piC"] = _calculate_complexity_factor(attributes["n_circuit_planes"])
    attributes["piP"] = _calculate_active_pins_factor(attributes["n_active_pins"])
    attributes["piK"] = _get_mate_unmate_factor(attributes["n_cycles"])

    attributes["piQ"] = 1.0
    if attributes["subcategory_id"] in {4, 5}:
        attributes["piQ"] = PART_STRESS_PI_Q[attributes["subcategory_id"]][
            attributes["quality_id"]
        ]

    attributes["piE"] = _calculate_piE(attributes)

    _factor_key = (
        _get_factor_key(
            attributes["type_id"],
            attributes["specification_id"],
            attributes["insert_id"],
        )
        if attributes["subcategory_id"] == 1
        else 5
    )

    _contact_temp = (
        attributes["temperature_active"] + attributes["temperature_rise"] + 273.0
    )

    attributes["lambda_b"] = _calculate_part_stress_lambda_b(
        attributes["subcategory_id"],
        attributes["type_id"],
        _contact_temp,
        _factor_key,
    )

    attributes["hazard_rate_active"] = _calculate_hazard_rate_active(attributes)

    return attributes


def set_default_values(
    **attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value of various parameters.

    :param attributes: the attribute dict for the connection being calculated.
    :return: attributes; the updated attribute dict.
    :rtype: dict
    """
    attributes["temperature_rise"] = (
        _set_default_temperature_rise(
            attributes["subcategory_id"], attributes["type_id"]
        )
        if attributes["temperature_rise"] < 0.0
        else attributes["temperature_rise"]
    )

    attributes["n_cycles"] = (
        3.0 if attributes["n_cycles"] < 0.0 else attributes["n_cycles"]
    )

    attributes["n_active_pins"] = (
        _set_default_active_pins(attributes["subcategory_id"], attributes["type_id"])
        if attributes["n_active_pins"] <= 0.0
        else attributes["n_active_pins"]
    )

    return attributes


def _calculate_active_pins_factor(n_active_pins: int) -> float:
    """Calculate the active pins factor (piP).

    :param n_active_pins: the number of active pins in the connector.
    :return: _pi_p; the calculated value of piP.
    :rtype: float
    """
    return exp(((n_active_pins - 1) / 10.0) ** 0.51064)


def _calculate_complexity_factor(n_circuit_planes: int) -> float:
    """Calculate the complexity factor (piC).

    :param n_circuit_planes: the number of planes in the PCB/PWA.
    :return: _pi_c; the calculated value of the complexity factor.
    :rtype: float
    """
    return 0.65 * n_circuit_planes**0.63 if n_circuit_planes > 2 else 1.0


def _calculate_hazard_rate_active(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Calculate the active hazard rate based on subcategory."""
    _lambda_b = attributes["lambda_b"]
    _piE = attributes["piE"]
    _piQ = attributes["piQ"]
    _piP = attributes["piP"]
    _piK = attributes["piK"]
    _subcategory_id = attributes["subcategory_id"]

    _hazard_rate = _lambda_b * _piE * _piQ
    if _subcategory_id == 3:
        return _hazard_rate * _piP
    elif _subcategory_id == 4:
        return (
            _hazard_rate
            * (
                attributes["n_wave_soldered"] * attributes["piC"]
                + attributes["n_hand_soldered"] * (attributes["piC"] + 13.0)
            )
            * _piQ
        )
    elif _subcategory_id == 5:
        return _hazard_rate * _piQ
    return _hazard_rate * _piK * _piP


def _calculate_insert_temperature(
    contact_gauge: int, current_operating: float
) -> float:
    """Calculate the insert temperature.

    Operating current can be passed as float or integer:
    >>> calculate_insert_temperature(1, 16, 0.05)
    0.0010736063482992093
    >>> calculate_insert_temperature(1, 16, 5)
    5.380777957087587

    A KeyError is raised if the contact gauge are unknown:
    >>> calculate_insert_temperature(1, 6, 0.05)
    Traceback (most recent call last):
        ...
    KeyError: 6

    A TypeError is raised if the operating current is passed as a string:
    >>> calculate_insert_temperature(1, 16, '0.05')
    Traceback (most recent call last):
        ...
    TypeError: unsupported operand type(s) for ** or pow(): 'str' and 'float'

    :param contact_gauge: the standard gauge of the connection contact.
    :param current_operating: the nominal current carried by each
        connection contact.
    :return: _temperature_rise; the calculated temperature of the connection's
        insert.
    :rtype: float
    :raise: KeyError when an unknown contact gauge is passed.
    :raise: TypeError when the operating current is passed as a string.
    """
    _fo = INSERT_TEMP_FACTORS[contact_gauge]

    return _fo * current_operating**1.85


def _calculate_part_stress_lambda_b(
    subcategory_id: int,
    type_id: int,
    contact_temperature: float,
    factor_key: int,
) -> float:
    """Calculate part stress base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F base hazard rate for the parts
    stress method.

    .. important:: the contact temperature must be calculated by the calling
        function as it is not an attribute of a Connection.

    :param subcategory_id: the subcategory identifier.
    :param type_id: the connection type identifier.
    :param contact_temperature: the operating temperature of the
        contacts.
    :return: _base_hr; the calculates base hazard rate.
    :rtype: float
    :raise: IndexError if passed an unknown type ID.
    :raise: ZeroDivisionError if passed contact temperature = 0.0.
    """
    _ref_temp = REF_TEMPS[factor_key]

    if subcategory_id in {4, 5}:
        return PART_STRESS_LAMBDA_B[subcategory_id][type_id - 1]
    elif subcategory_id == 3:
        return 0.00042

    _factors = LAMBDA_B_FACTORS[factor_key]
    return _factors[0] * exp(
        (_factors[1] / contact_temperature)
        + (contact_temperature / _ref_temp) ** _factors[2]
    )


def _calculate_piE(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Calculate the piE value based on category and subcategory."""
    _category_id = attributes["category_id"]
    _subcategory_id = attributes["subcategory_id"]
    _environment_id = attributes["environment_id"]

    if _category_id in {1, 2}:
        return PI_E[_category_id][_subcategory_id][_environment_id]
    elif _category_id in {3, 4, 5}:
        return PI_E[_category_id][_environment_id]
    return 1.0


def _get_factor_key(type_id: int, specification_id: int, insert_id: int) -> int:
    """Retrieve the reference temperature key for the connection.

    :param type_id: the connection type identifier.
    :param specification_id: the connection governing specification identifier.
    :param insert_id: the insert material identifier.
    :return: _key; the key to use to select the reference temperature and other factors.
    :rtype: int
    """
    # Reference temperature is used to calculate base hazard rate for
    # circular/rack and panel connectors.  To get the reference temperature
    # dictionary key, we query the key dictionary in which the first key is
    # the connector type ID, second key is the specification ID.  The insert
    # material ID is the index in the list returned.
    return FACTOR_KEYS[type_id][specification_id][insert_id - 1]


def _get_mate_unmate_factor(n_cycles: float) -> float:
    """Retrieve the mating/unmating factor (piK).

    :param n_cycles: the average number of mate/unmate cycles expected per hour of
        operation.
    :return: _pi_k; the mate_unmate_factor.
    :rtype: float
    """
    if n_cycles <= 0.05:
        return PI_K[0]
    elif 0.05 < n_cycles <= 0.5:
        return PI_K[1]
    elif 0.5 < n_cycles <= 5.0:
        return PI_K[2]
    elif 5.0 < n_cycles <= 50.0:
        return PI_K[3]
    else:
        return PI_K[4]


def _get_part_count_lambda_b(
    subcategory_id: int,
    environment_active_id: int,
    type_id: int,
) -> float:
    """Retrieve the parts count base hazard rate (lambda b) from MIL-HDBK-217F.

    This function retrieves the MIL-HDBK-217F parts count base hazard rate.
    The dictionary PART_COUNT_LAMBDA_B contains the MIL-HDBK-217F parts count
    base hazard rates.  Keys are for PART_COUNT_LAMBDA_B are:

        #. subcategory_id
        #. environment_active_id
        #. type id; if the connection subcategory is NOT type dependent, then
            the second key will be zero.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory    |           Connection          | MIL-HDBK-217F   |
    |       ID       |              Style            |    Section      |
    +================+===============================+=================+
    |        1       | Circular, Rack and Panel,     |       15.1      |
    |                | Coaxial, Triaxial             |                 |
    +----------------+-------------------------------+-----------------+
    |        2       | PCB/PWA Edge                  |       15.2      |
    +----------------+-------------------------------+-----------------+
    |        3       | IC Socket                     |       15.3      |
    +----------------+-------------------------------+-----------------+
    |        4       | Plated Through Hole (PTH)     |       16.1      |
    +----------------+-------------------------------+-----------------+
    |        5       | Non-PTH                       |       17.1      |
    +----------------+-------------------------------+-----------------+

    :param subcategory_id: the subcategory ID for the connection being calculated.
    :param environment_active_id: the active operating environment ID for the connection
        being calculated.
    :param type_id: the type ID for the connection being calculated.
    :return: _base_hr; the parts count base hazard rate.
    :rtype: float
    :raise: KeyError if passed an unknown subcategory ID or type ID.
    :raise: IndexError if passed an unknown active environment ID.
    """
    return (
        PART_COUNT_LAMBDA_B[subcategory_id][type_id][environment_active_id - 1]
        if subcategory_id in {1, 5}
        else PART_COUNT_LAMBDA_B[subcategory_id][environment_active_id - 1]
    )


def _set_default_active_pins(
    subcategory_id: int,
    type_id: int,
) -> int:
    """Set the default number of active pins value.

    :param subcategory_id: the subcategory ID of the connection with missing defaults.
    :return: _n_active_pins
    :rtype: int
    """
    _thresholds = {
        (1, 1): 40,
        (1, 2): 40,
        (1, 3): 40,
        (1, 4): 2,
        (1, 5): 3,
        (2, None): 40,
        (3, None): 24,
        (4, None): 1000,
    }

    return _thresholds.get(
        (subcategory_id, type_id), _thresholds.get((subcategory_id, None), 0)
    )


def _set_default_temperature_rise(
    subcategory_id: int,
    type_id: int,
) -> float:
    """Set the default temperature rise value.

    :param subcategory_id: the subcategory ID of the connection with missing defaults.
    :return: _temperature_rise
    :rtype: float
    """
    if subcategory_id == 1 and type_id in {1, 2, 3}:
        return 10.0
    elif subcategory_id == 1 and type_id in {4, 5}:
        return 5.0
    elif subcategory_id == 2:
        return 10.0
    return 0.0
