# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Meter.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Meter MIL-HDBK-217F Calculations Module."""

# Standard Library Imports
from typing import Any, Dict

PART_COUNT_LAMBDA_B = {
    1: {
        1: [
            10.0, 20.0, 120.0, 70.0, 180.0, 50.0, 80.0, 160.0, 250.0, 260.0,
            5.0, 140.0, 380.0, 0.0
        ],
        2: [
            15.0, 30.0, 180.0, 105.0, 270.0, 75.0, 120.0, 240.0, 375.0, 390.0,
            7.5, 210.0, 570.0, 0.0
        ],
        3: [
            40.0, 80.0, 480.0, 280.0, 720.0, 200.0, 320.0, 640.0, 1000.0,
            1040.0, 20.0, 560.0, 1520.0, 0.0
        ]
    },
    2: {
        1: [
            0.09, 0.36, 2.3, 1.1, 3.2, 2.5, 3.8, 5.2, 6.6, 5.4, 0.099, 5.4,
            0.0, 0.0
        ],
        2: [
            0.15, 0.61, 2.8, 1.8, 5.4, 4.3, 6.4, 8.9, 11.0, 9.2, 0.17, 9.2,
            0.0, 0.0
        ]
    }
}
PART_COUNT_PI_Q = {1: [1.0, 1.0], 2: [1.0, 3.4]}
PART_STRESS_LAMBDA_B = {1: [20.0, 30.0, 80.0], 2: 0.09}
PART_STRESS_PI_Q = {2: [1.0, 3.4]}
PI_E = {
    1: [
        1.0, 2.0, 12.0, 7.0, 18.0, 5.0, 8.0, 16.0, 25.0, 26.0, 0.5, 14.0, 38.0,
        0.0
    ],
    2: [
        1.0, 4.0, 25.0, 12.0, 35.0, 28.0, 42.0, 58.0, 73.0, 60.0, 1.1, 60.0,
        0.0, 0.0
    ]
}
PI_F = [1.0, 1.0, 2.8]


def calculate_part_count(**attributes: Dict[str, Any]) -> float:
    """Wrap get_part_count_lambda_b().

    This wrapper allows us to pass an attributes dict from a generic parts
    count function.

    :param attributes: the attributes for the connection being calculated.
    :return: _base_hr; the parts count base hazard rates.
    :rtype: float
    """
    return get_part_count_lambda_b(
        subcategory_id=attributes['subcategory_id'],
        type_id=attributes['type_id'],
        environment_active_id=attributes['environment_active_id'])


def calculate_part_stress(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the part stress hazard rate for a meter.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: attributes; the keyword argument (hardware attribute)
        dictionary with updated values.
    :rtype: dict
    """
    attributes['lambda_b'] = get_part_stress_lambda_b(
        attributes['subcategory_id'], attributes['type_id'])
    attributes['piT'] = get_temperature_stress_factor(
        attributes['temperature_active'], attributes['temperature_rated_max'])

    # Determine the application factor (piA) and function factor (piF).
    if attributes['subcategory_id'] == 2:
        attributes['piA'] = (1.7 if (attributes['type_id']) - (1) else 1.0)
        attributes['piF'] = PI_F[attributes['application_id'] - 1]

    attributes['hazard_rate_active'] = (attributes['lambda_b']
                                        * attributes['piE'])
    if attributes['subcategory_id'] == 2:
        attributes['hazard_rate_active'] = (attributes['hazard_rate_active']
                                            * attributes['piA']
                                            * attributes['piF']
                                            * attributes['piQ'])
    elif attributes['subcategory_id'] == 1:
        attributes['hazard_rate_active'] = (attributes['hazard_rate_active']
                                            * attributes['piT'])

    return attributes


def get_part_count_lambda_b(**kwargs: Dict[str, int]) -> float:
    """Retrieve the parts count base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.  The dictionary PART_COUNT_217F_LAMBDA_B contains the
    MIL-HDBK-217F parts count base hazard rates.  Keys are for
    PART_COUNT_217F_LAMBDA_B are:

        #. subcategory_id
        #. environment_active_id
        #. type id

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory    |              Meter            | MIL-HDBK-217F   |
    |       ID       |              Style            |    Section      |
    +================+===============================+=================+
    |        1       | Elapsed Time                  |       12.4      |
    +----------------+-------------------------------+-----------------+
    |        2       | Panel                         |       18.1      |
    +----------------+-------------------------------+-----------------+

    :param subcategory_id: the subcategory identifier.
    :param type_id: the type of meter identifier.
    :param environment_active_id: the active environment identifier.
    :return: _base_hr; the parts count base hazard rate.
    :rtype: float
    :raise: IndexError if passed an unknown active environment ID.
    :raise: KeyError if passed an unknown subcategory ID or type ID.
    """
    _subcategory_id = kwargs.get('subcategory_id', 0)
    _type_id = kwargs.get('type_id', 0)
    _environment_active_id = kwargs.get('environment_active_id', 0)

    return PART_COUNT_LAMBDA_B[_subcategory_id][_type_id][
        _environment_active_id - 1]


def get_part_stress_lambda_b(subcategory_id: int, type_id: int) -> float:
    """Retrieve the part stress base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    stress method.

    :param subcategory_id: the subcategory identifier.
    :param type_id: the meter type identifier.
    :return: _lambda_b; the part stress base hazard rate or 0.0 if an unknown
        subcategory ID is passed.
    :rtype: float
    :raise: IndexError when passed an unknown type ID.
    """
    if subcategory_id == 1:
        _lambda_b = PART_STRESS_LAMBDA_B[1][type_id - 1]
    elif subcategory_id == 2:
        _lambda_b = PART_STRESS_LAMBDA_B[2]
    else:
        _lambda_b = 0.0

    return _lambda_b


def get_temperature_stress_factor(temperature_active: float,
                                  temperature_rated_max: float) -> float:
    """Retrieve the temperature stress factor (piT).

    :param subcategory_id: the subcategory identifier.
    :param temperature_active: the operating ambient temperature in C.
    :param temperature_rated_max: the maxmimum rated operating
        temperature in C.
    :return: _pi_t; the value of piT associated with the operating temperature.
    :rtype: float
    :raise: TypeError if passed a string for either temperature.
    :raise: ZeroDivisionError if passed a rated maximum temperature = 0.0.
    """
    _temperature_ratio = (temperature_active / temperature_rated_max)

    if 0.0 < _temperature_ratio <= 0.5:
        _pi_t = 0.5
    elif 0.5 < _temperature_ratio <= 0.6:
        _pi_t = 0.6
    elif 0.6 < _temperature_ratio <= 0.8:
        _pi_t = 0.8
    elif 0.8 < _temperature_ratio <= 1.0:
        _pi_t = 1.0

    return _pi_t
