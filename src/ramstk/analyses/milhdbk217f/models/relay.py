# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdbk217f.models.relay.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Relay MIL-HDBK-217F Calculations Module."""

# Standard Library Imports
from math import exp
from typing import Dict, Union

PART_COUNT_LAMBDA_B = {
    1: {
        1: [
            0.13,
            0.28,
            2.1,
            1.1,
            3.8,
            1.1,
            1.4,
            1.9,
            2.0,
            7.0,
            0.66,
            3.5,
            10.0,
            0.0,
        ],
        2: [
            0.43,
            0.89,
            6.9,
            3.6,
            12.0,
            3.4,
            4.4,
            6.2,
            6.7,
            22.0,
            0.21,
            11.0,
            32.0,
            0.0,
        ],
        3: [
            0.13,
            0.26,
            2.1,
            1.1,
            3.8,
            1.1,
            1.4,
            1.9,
            2.0,
            7.0,
            0.66,
            3.5,
            10.0,
            0.0,
        ],
        4: [
            0.11,
            0.23,
            1.8,
            0.92,
            3.3,
            0.96,
            1.2,
            2.1,
            2.3,
            6.5,
            0.54,
            3.0,
            9.0,
            0.0,
        ],
        5: [
            0.29,
            0.60,
            4.8,
            2.4,
            8.2,
            2.3,
            2.9,
            4.1,
            4.5,
            15.0,
            0.14,
            7.6,
            22.0,
            0.0,
        ],
        6: [
            0.88,
            1.8,
            14.0,
            7.4,
            26.0,
            7.1,
            9.1,
            13.0,
            14.0,
            46.0,
            0.44,
            24.0,
            67.0,
            0.0,
        ],
    },
    2: {
        1: [
            0.40,
            1.2,
            4.8,
            2.4,
            6.8,
            4.8,
            7.6,
            8.4,
            13.0,
            9.2,
            0.16,
            4.8,
            13.0,
            240.0,
        ],
        2: [
            0.50,
            1.5,
            6.0,
            3.0,
            8.5,
            5.0,
            9.5,
            11.0,
            16.0,
            12.0,
            0.20,
            5.0,
            17.0,
            300.0,
        ],
    },
}
PART_COUNT_PI_Q = {1: [0.6, 3.0, 9.0], 2: [0.0, 1.0, 4.0]}
PART_STRESS_PI_Q = {1: [0.1, 0.3, 0.45, 0.6, 1.0, 1.5, 3.0], 2: [1.0, 4.0]}
PI_C = {1: [1.0, 1.5, 1.75, 2.0, 2.5, 3.0, 4.25, 5.5, 8.0]}
PI_E = {
    1: {
        1: [
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
        ],
        2: [
            2.0,
            5.0,
            44.0,
            24.0,
            78.0,
            15.0,
            20.0,
            28.0,
            38.0,
            140.0,
            1.0,
            72.0,
            200.0,
            0.0,
        ],
    },
    2: [
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
    ],
}
PI_F = {
    1: {
        1: {
            1: [4.0, 8.0],
            2: [6.0, 18.0],
            3: [1.0, 3.0],
            4: [4.0, 8.0],
            5: [7.0, 14.0],
            6: [7.0, 14.0],
        }
    },
    2: {
        1: {1: [3.0, 6.0], 2: [5.0, 10.0], 3: [6.0, 12.0]},
        2: {
            1: [5.0, 10.0],
            2: [2.0, 6.0],
            3: [6.0, 12.0],
            4: [100.0, 100.0],
            5: [10.0, 20.0],
        },
        3: {1: [10.0, 20.0], 2: [100.0, 100.0]},
        4: {1: [6.0, 12.0], 2: [1.0, 3.0]},
        5: {1: [25.0, 0.0], 2: [6.0, 0.0]},
        6: {1: [10.0, 20.0]},
        7: {1: [9.0, 12.0]},
        8: {1: [10.0, 20.0], 2: [5.0, 10.0], 3: [5.0, 10.0]},
    },
    3: {
        1: {1: [20.0, 40.0], 2: [5.0, 10.0]},
        2: {
            1: [3.0, 6.0],
            2: [1.0, 3.0],
            3: [2.0, 6.0],
            4: [3.0, 6.0],
            5: [2.0, 6.0],
            6: [2.0, 6.0],
        },
    },
    4: {1: {1: [7.0, 14.0], 2: [12.0, 24.0], 3: [10.0, 20.0], 4: [5.0, 10.0]}},
}


def calculate_part_count(**attributes: Dict[str, Union[float, int, str]]) -> float:
    """Wrap get_part_count_lambda_b().

    This wrapper allows us to pass an attribute dict from a generic parts
    count function.

    :param attributes: the attributes for the connection being calculated.
    :return: _base_hr; the parts count base hazard rates.
    :rtype: float
    """
    return get_part_count_lambda_b(
        attributes["subcategory_id"],
        attributes["type_id"],
        attributes["environment_active_id"],
    )


def calculate_part_stress(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress hazard rate for a relay.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    attributes["lambda_b"] = calculate_part_stress_lambda_b(
        attributes["subcategory_id"],
        attributes["type_id"],
        attributes["temperature_active"],
    )
    attributes["piCYC"] = calculate_cycling_factor(
        attributes["quality_id"], attributes["n_cycles"]
    )
    attributes["piL"] = calculate_load_stress_factor(
        attributes["technology_id"], attributes["current_ratio"]
    )
    attributes["piE"] = get_environment_factor(
        attributes["subcategory_id"],
        attributes["quality_id"],
        attributes["environment_active_id"],
    )
    attributes["piF"] = get_application_construction_factor(
        attributes["quality_id"],
        attributes["contact_rating_id"],
        attributes["construction_id"],
        attributes["application_id"],
    )

    if attributes["subcategory_id"] == 1:
        attributes["piC"] = PI_C[attributes["subcategory_id"]][
            attributes["contact_form_id"] - 1
        ]

    attributes["hazard_rate_active"] = (
        attributes["lambda_b"] * attributes["piQ"] * attributes["piE"]
    )
    if attributes["subcategory_id"] == 1:
        attributes["hazard_rate_active"] = (
            attributes["hazard_rate_active"]
            * attributes["piL"]
            * attributes["piC"]
            * attributes["piCYC"]
            * attributes["piF"]
        )

    return attributes


def calculate_cycling_factor(
    quality_id: int,
    n_cycles: float,
) -> float:
    """Calculate the cycling factor (piCYC) for the relay.

    :param quality_id: the quality level identifier.
    :param n_cycles: the number of relay cycles per hour in application.
    :return: _pi_cyc; the calculated cycling factor.
    :rtype: float
    """
    if quality_id in {1, 2, 3, 4, 5, 6} and n_cycles < 1.0:
        return 0.1
    elif quality_id == 7 and n_cycles > 1000.0:
        return (n_cycles / 100.0) ** 2.0
    elif quality_id == 7 and 10.0 < n_cycles < 1000.0:
        return n_cycles / 10.0
    else:
        return 0.0


def calculate_load_stress_factor(
    technology_id: int,
    current_ratio: float,
) -> float:
    """Calculate the load stress factor (piL).

    Only subcategory 1 relays use this in their calculation.

    :param technology_id: the relay technology identifier.
    :param current_ratio: the operating current ratio of the relay.
    :return: _pi_l; the calculated value of piL.
    :rtype: float
    """
    if technology_id == 1:
        return (current_ratio / 0.8) ** 2.0
    elif technology_id == 2:
        return (current_ratio / 0.4) ** 2.0
    elif technology_id == 3:
        return (current_ratio / 0.2) ** 2.0
    else:
        return 0.0


def calculate_part_stress_lambda_b(
    subcategory_id: int,
    type_id: int,
    temperature_active: float,
) -> float:
    """Calculate the base hazard rate for the relay.

    :param subcategory_id: the subcategory identifier.
    :param type_id: the relay type identifier.
    :param temperature_active: the operating ambient temperature of the
        relay in C.
    :return: _lambda_b; the calculated part stress base hazard rate or 0.0 if
        passed an unknown subcategory ID.
    :rtype: float
    """
    _dic_factors = {
        1: [[0.00555, 352.0, 15.7], [0.0054, 377.0, 10.4]],
        2: [0.4, 0.5, 0.5],
    }
    _lambda_b = 0.0

    if subcategory_id == 1:
        _f0 = _dic_factors[subcategory_id][type_id - 1][0]
        _f1 = _dic_factors[subcategory_id][type_id - 1][1]
        _f2 = _dic_factors[subcategory_id][type_id - 1][2]
        _lambda_b = _f0 * exp(((temperature_active + 273.0) / _f1) ** _f2)
    elif subcategory_id == 2:
        _lambda_b = _dic_factors[subcategory_id][type_id - 1]

    return _lambda_b


def get_application_construction_factor(
    quality_id: int,
    contact_rating_id: int,
    construction_id: int,
    application_id: int,
) -> float:
    """Calculate the construction factor (piF) for the relay.

    :param quality_id: the quality level identifier.
    :param contact_rating_id: the relay contact current rating identifier.
    :param construction_id: the relay construction identifier.
    :param application_id: the relay application identifier.
    :return: _pi_f; the selected application factor.
    :rtype: float
    :raise: KeyError if passed an unknown contact rating ID, construction ID,
        or application ID.
    """
    _quality = 1 if quality_id in {1, 2, 3, 4, 5, 6} else 2
    return PI_F[contact_rating_id][application_id][construction_id][_quality - 1]


def get_environment_factor(
    subcategory_id: int,
    quality_id: int,
    environment_active_id: int,
) -> float:
    """Retrieve the environment factor (pi_E).

    :param subcategory_id: the subcategory identifier.
    :param quality_id: the quality level identifier.
    :param environment_active_id: the active environment identifier.
    :return: _pi_e; the selected environment factor.
    :rtype: float
    :raise: IndexError if passed an unknown active environment ID.
    :raise: KeyError if passed an unknown subcategory ID.
    """
    _quality = 1 if quality_id in {1, 2, 3, 4, 5, 6} else 2
    return (
        PI_E[subcategory_id][_quality][environment_active_id - 1]
        if subcategory_id == 1
        else PI_E[subcategory_id][environment_active_id - 1]
    )


def get_part_count_lambda_b(
    subcategory_id: int,
    type_id: int,
    environment_active_id: int,
) -> float:
    """Retrieve the parts count base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.  The dictionary PART_COUNT_217F_LAMBDA_B contains the
    MIL-HDBK-217F parts count base hazard rates.  Keys are for
    PART_COUNT_217F_LAMBDA_B are:

        #. subcategory_id
        #. environment_active_id
        #. type id; if the relay subcategory is NOT type dependent, then
            the second key will be zero.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory    |              Relay            | MIL-HDBK-217F   |
    |       ID       |              Style            |    Section      |
    +================+===============================+=================+
    |        1       | Mechanical                    |       13.1      |
    +----------------+-------------------------------+-----------------+
    |        2       | Solid State                   |       13.2      |
    +----------------+-------------------------------+-----------------+

    :param subcategory_id: the subcategory identifier.
    :param type_id: the relay type identifier.
    :param environment_active_id: the active environment identifier.
    :return: _base_hr; the parts count base hazard rate.
    :rtype: float
    :raise: IndexError if passed an unknown active environment ID.
    :raise: KeyError if passed an unknown subcategory ID or type ID.
    """
    return PART_COUNT_LAMBDA_B[subcategory_id][type_id][environment_active_id - 1]


def set_default_values(
    **attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value of various parameters.

    The subcategory ID and the type ID must be set for default values to be applied.

    :param attributes: the attribute dict for the relay being calculated.
    :return: attributes; the updated attribute dict.
    :rtype: dict
    """
    if attributes["quality_id"] <= 0:
        attributes["quality_id"] = _set_default_quality(attributes["subcategory_id"])

    if attributes["current_ratio"] <= 0.0:
        attributes["current_ratio"] = 0.5

    attributes["technology_id"] = _set_default_load_type(
        attributes["technology_id"], attributes["type_id"]
    )

    attributes["contact_form_id"] = _set_default_contact_form(
        attributes["contact_form_id"], attributes["type_id"]
    )

    attributes["contact_rating_id"] = _set_default_contact_rating(
        attributes["contact_rating_id"], attributes["type_id"]
    )

    attributes["application_id"] = _set_default_application(
        attributes["application_id"], attributes["type_id"]
    )

    attributes["construction_id"] = _set_default_construction(
        attributes["construction_id"], attributes["type_id"]
    )

    attributes["duty_cycle"] = _set_default_duty_cycle(
        attributes["duty_cycle"], attributes["type_id"]
    )

    attributes["temperature_rated_max"] = _set_default_rated_temperature(
        attributes["temperature_rated_max"], attributes["type_id"]
    )

    return attributes


def _set_default_quality(subcategory_id: int) -> int:
    """Set the default quality for mechanical relays.

    :param subcategory_id: the subcategory ID of the relay with missing defaults.
    :return: _quality_id
    :rtype: float
    """
    return 5 if subcategory_id == 4 else 1


def _set_default_load_type(technology_id: int, type_id: int) -> int:
    """Set the default max rated temperature for mechanical relays.

    :param technology_id: the current technology ID (represents the load type).
    :param type_id: the type ID of the relay with missing defaults.
    :return: _contact_form_id
    :rtype: int
    """
    if technology_id > 0:
        return technology_id
    else:
        return 1 if type_id in {1, 3, 4, 6} else 2


def _set_default_contact_form(contact_form_id: int, type_id: int) -> int:
    """Set the default contact form for mechanical relays.

    :param contact_form_id: the current contact form ID.
    :param type_id: the type ID of the relay with missing defaults.
    :return: _contact_form_id
    :rtype: int
    """
    if contact_form_id > 0:
        return contact_form_id
    else:
        return 1 if type_id in {4, 5} else 6


def _set_default_contact_rating(contact_rating_id: int, type_id: int) -> int:
    """Set the default contact rating for mechanical relays.

    :param contact_form_id: the current contact rating ID.
    :param type_id: the type ID of the relay with missing defaults.
    :return: _contact_rating_id
    :rtype: int
    """
    if contact_rating_id > 0:
        return contact_rating_id
    else:
        return {1: 2, 2: 4, 3: 2, 4: 1, 5: 2, 6: 2}[type_id]


def _set_default_application(application_id: int, type_id: int) -> int:
    """Set the default application for mechanical relays.

    :param application_id: the current application ID.
    :param type_id: the type ID of the relay with missing defaults.
    :return: _application_id
    :rtype: int
    """
    if application_id > 0:
        return application_id
    else:
        return {1: 1, 2: 1, 3: 8, 4: 1, 5: 6, 6: 3}[type_id]


def _set_default_construction(construction_id: int, type_id: int) -> int:
    """Set the default construction for mechanical relays.

    :param construction_id: the current construction ID.
    :param application_id: the current application ID of the relay with missing
        defaults.
    :param contact_rating_id: the contact rating ID of the relay with missing defaults.
    :return: _contact_rating_id
    :rtype: int
    """
    if construction_id > 0:
        return construction_id
    else:
        return {1: 2, 2: 4, 3: 2, 4: 2, 5: 1, 6: 2}[type_id]


def _set_default_duty_cycle(duty_cycle: float, type_id: int) -> float:
    """Set the default max rated temperature for mechanical relays.

    :param duty_cycle: the current duty cycle.
    :param type_id: the type ID of the relay with missing defaults.
    :return: _duty_cycle
    :rtype: float
    """
    if duty_cycle > 0.0:
        return duty_cycle
    else:
        return 20.0 if type_id == 4 else 10.0


def _set_default_rated_temperature(rated_temperature_max: float, type_id: int) -> float:
    """Set the default max rated temperature for mechanical relays.

    :param rated_temperature_max: the current maximum rated temperature.
    :param type_id: the type ID of the relay with missing defaults.
    :return: _rated_temperature_max
    :rtype: float
    """
    if rated_temperature_max > 0.0:
        return rated_temperature_max
    else:
        return 85.0 if type_id == 4 else 125.0
