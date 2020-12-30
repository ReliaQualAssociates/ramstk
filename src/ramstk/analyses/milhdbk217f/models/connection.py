# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Connection.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Connection MIL-HDBK-217F Constants and Calculations Module."""

# Standard Library Imports
from math import exp
from typing import Any, Dict

PART_COUNT_LAMBDA_B = {
    1: {
        1: [
            0.011, 0.14, 0.11, 0.069, 0.20, 0.058, 0.098, 0.23, 0.34, 0.37,
            0.0054, 0.16, 0.42, 6.8
        ],
        2: [
            0.012, 0.015, 0.13, 0.075, 0.21, 0.06, 0.1, 0.22, 0.32, 0.38,
            0.0061, 0.18, 0.54, 7.3
        ]
    },
    2: [
        0.0054, 0.021, 0.055, 0.035, 0.10, 0.059, 0.11, 0.085, 0.16, 0.19,
        0.0027, 0.078, 0.21, 3.4
    ],
    3: [
        0.0019, 0.0058, 0.027, 0.012, 0.035, 0.015, 0.023, 0.021, 0.025, 0.048,
        0.00097, 0.027, 0.070, 1.3
    ],
    4: [
        0.053, 0.11, 0.37, 0.69, 0.27, 0.27, 0.43, 0.85, 1.5, 1.0, 0.027, 0.53,
        1.4, 27.0
    ],
    5: {
        1: [
            0.0026, 0.0052, 0.018, 0.010, 0.029, 0.010, 0.016, 0.016, 0.021,
            0.042, 0.0013, 0.023, 0.062, 1.1
        ],
        2: [
            0.00014, 0.00028, 0.00096, 0.00056, 0.0015, 0.00056, 0.00084,
            0.00084, 0.0011, 0.0022, 0.00007, 0.0013, 0.0034, 0.059
        ],
        3: [
            0.00026, 0.00052, 0.0018, 0.0010, 0.0029, 0.0010, 0.0016, 0.0016,
            0.0021, 0.0042, 0.00013, 0.0023, 0.0062, 0.11
        ],
        4: [
            0.000050, 0.000100, 0.000350, 0.000200, 0.000550, 0.000200,
            0.000300, 0.000300, 0.000400, 0.000800, 0.000025, 0.000450,
            0.001200, 0.021000
        ],
        5: [
            0.0000035, 0.000007, 0.000025, 0.000014, 0.000039, 0.000014,
            0.000021, 0.000021, 0.000028, 0.000056, 0.0000018, 0.000031,
            0.000084, 0.0015
        ],
        6: [
            0.00012, 0.00024, 0.00084, 0.00048, 0.0013, 0.00048, 0.00072,
            0.00072, 0.00096, 0.0019, 0.00005, 0.0011, 0.0029, 0.050
        ],
        7: [
            0.000069, 0.000138, 0.000483, 0.000276, 0.000759, 0.000276,
            0.000414, 0.000414, 0.000552, 0.001104, 0.000035, 0.000621,
            0.001656, 0.02898
        ]
    }
}
PART_COUNT_PI_Q = [1.0, 2.0]
PART_STRESS_LAMBDA_B = {
    4: [0.000041, 0.00026],
    5: [0.0026, 0.00014, 0.00026, 0.00005, 0.0000035, 0.00012, 0.000069]
}
PART_STRESS_PI_Q = {4: [1.0, 2.0], 5: [1.0, 1.0, 2.0, 20.0]}
PI_E = {
    1: {
        1: [
            1.0, 1.0, 8.0, 5.0, 13.0, 3.0, 5.0, 8.0, 12.0, 19.0, 0.5, 10.0,
            27.0, 490.0
        ],
        2: [
            2.0, 5.0, 21.0, 10.0, 27.0, 12.0, 18.0, 17.0, 25.0, 37.0, 0.8,
            20.0, 54.0, 970.0
        ]
    },
    2: {
        1: [
            1.0, 3.0, 8.0, 5.0, 13.0, 6.0, 11.0, 6.0, 11.0, 19.0, 0.5, 10.0,
            27.0, 490.0
        ],
        2: [
            2.0, 7.0, 17.0, 10.0, 26.0, 14.0, 22.0, 14.0, 22.0, 37.0, 0.8,
            20.0, 54.0, 970.0
        ]
    },
    3: [
        1.0, 3.0, 14.0, 6.0, 18.0, 8.0, 12.0, 11.0, 13.0, 25.0, 0.5, 14.0,
        36.0, 650.0
    ],
    4: [
        1.0, 2.0, 7.0, 5.0, 13.0, 5.0, 8.0, 16.0, 28.0, 19.0, 0.5, 10.0, 27.0,
        500.0
    ],
    5: [
        1.0, 2.0, 7.0, 4.0, 11.0, 4.0, 6.0, 6.0, 8.0, 16.0, 0.5, 9.0, 24.0,
        420.0
    ]
}
PI_K = [1.0, 1.5, 2.0, 3.0, 4.0]
REF_TEMPS = {1: 473.0, 2: 423.0, 3: 373.0, 4: 358.0, 5: 423.0}


def calculate_active_pins_factor(n_active_pins: int) -> float:
    """Calculate the active pins factor (piP).

    :param n_active_pins: the number of active pins in the connector.
    :return: _pi_p; the calculated value of piP.
    :rtype: float
    """
    return exp(((n_active_pins - 1) / 10.0)**0.51064)


def calculate_complexity_factor(n_circuit_planes: int) -> float:
    """Calculate the complexity factor (piC).

    :param n_circuit_planes: the number of planes in the PCB/PWA.
    :return: _pi_c; the calculated value of the complexity factor.
    :rtype: float
    """
    if n_circuit_planes > 2:
        _pi_c = 0.65 * n_circuit_planes**0.63
    else:
        _pi_c = 1.0

    return _pi_c


def calculate_insert_temperature(contact_gauge: int,
                                 current_operating: float) -> float:
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
    _dic_factors = {12: 0.1, 16: 0.274, 20: 0.64, 22: 0.989, 26: 2.1}

    _fo = _dic_factors[contact_gauge]
    _temperature_rise = (_fo * current_operating**1.85)

    return _temperature_rise


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
        environment_active_id=attributes['environment_active_id'],
        type_id=attributes['type_id'])


def calculate_part_stress(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the part stress active hazard rate for a connection.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :param attributes: the attributes for the connection being calculated.
    :return: attributes; the keyword argument (hardware attribute)
        dictionary with updated values.
    :rtype: dict
    """
    attributes['temperature_rise'] = calculate_insert_temperature(
        attributes['contact_gauge'], attributes['current_operating'])
    attributes['piC'] = calculate_complexity_factor(
        attributes['n_circuit_planes'])
    attributes['piP'] = calculate_active_pins_factor(
        attributes['n_active_pins'])
    attributes['piK'] = get_mate_unmate_factor(attributes['n_cycles'])

    if attributes['subcategory_id'] == 1:
        _factor_key = get_factor_key(attributes['type_id'],
                                     attributes['specification_id'],
                                     attributes['insert_id'])
    else:
        _factor_key = 5
    _contact_temp = (attributes['temperature_active']
                     + attributes['temperature_rise'] + 273.0)

    attributes['lambda_b'] = calculate_part_stress_lambda_b(
        attributes['subcategory_id'], attributes['type_id'], _contact_temp,
        _factor_key)

    attributes['hazard_rate_active'] = (attributes['lambda_b']
                                        * attributes['piE'])
    if attributes['subcategory_id'] == 3:
        attributes['hazard_rate_active'] = (attributes['hazard_rate_active']
                                            * attributes['piP'])
    elif attributes['subcategory_id'] == 4:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] *
            (attributes['n_wave_soldered'] * attributes['piC']
             + attributes['n_hand_soldered'] *
             (attributes['piC'] + 13.0)) * attributes['piQ'])
    elif attributes['subcategory_id'] == 5:
        attributes['hazard_rate_active'] = (attributes['hazard_rate_active']
                                            * attributes['piQ'])
    else:
        attributes['hazard_rate_active'] = (attributes['hazard_rate_active']
                                            * attributes['piK']
                                            * attributes['piP'])

    return attributes


def calculate_part_stress_lambda_b(subcategory_id: int, type_id: int,
                                   contact_temperature: float,
                                   factor_key: int) -> float:
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
    # Factors are used to calculate base hazard rate for circular/rack and
    # panel connectors.  Key is from dictionary above (1 - 4) or contact
    # gauge (22 - 12).
    _dic_factors = {
        1: [0.2, -1592.0, 5.36],
        2: [0.431, -2073.6, 4.66],
        3: [0.19, -1298.0, 4.25],
        4: [0.77, -1528.8, 4.72],
        5: [0.216, -2073.6, 4.66],
    }

    _ref_temp = REF_TEMPS[factor_key]
    _f0 = _dic_factors[factor_key][0]
    _f1 = _dic_factors[factor_key][1]
    _f2 = _dic_factors[factor_key][2]

    if subcategory_id in [4, 5]:
        _lambda_b = PART_STRESS_LAMBDA_B[subcategory_id][type_id - 1]
    elif subcategory_id == 3:
        _lambda_b = 0.00042
    else:
        _lambda_b = _f0 * exp((_f1 / contact_temperature)
                              + (contact_temperature / _ref_temp)**_f2)

    return _lambda_b


def get_factor_key(type_id: int, specification_id: int, insert_id: int) -> int:
    """Retrieve the reference temperature key for the connection.

    :param subcategory_id: the subcategory identifier.
    :param type_id: the connection type identifier.
    :param specification_id: the connection governing specification
        identifier.
    :param insert_id: the insert material identifier.
    :return: _key; the key to use to select the reference temperature and other
        factors.
    :rtype: int
    """
    # Reference temperature is used to calculate base hazard rate for
    # circular/rack and panel connectors.  To get the reference temperature
    # dictionary key, we quesry the key dictionary in which the first key is
    # the connector type ID, second key is the specification ID.  The insert
    # material ID is the index in the list returned.
    _dic_keys = {
        1: {
            1: [2, 2, 2, 2, 2, 2],
            2: [2, 2, 2, 2, 2, 2],
            3: [1, 1, 1, 2, 2, 2, 2, 2, 2],
            4: [1, 1, 1, 2, 2, 2, 2, 2, 2],
            5: [1, 1, 1, 2, 2, 2, 2, 2, 2]
        },
        2: {
            1: [2, 2, 2, 2, 2, 2, 4, 4, 4],
            2: [1, 1, 1, 2, 2, 2, 2, 2, 2, 4, 4, 4],
            3: [1, 1, 1, 2, 2, 2, 2, 2, 2],
            4: [1, 1, 1, 2, 2, 2, 2, 2, 2],
            5: [2, 2, 2, 2, 2, 2],
            6: [2, 2, 2, 2, 2, 2]
        },
        3: {
            1: [2, 2, 2, 2, 2, 2, 4, 4, 4],
            2: [2, 2, 2, 2, 2, 2, 4, 4, 4]
        },
        4: {
            1: [3, 3],
            2: [3, 3],
            3: [3, 3],
            4: [3, 3],
            5: [3, 3],
            6: [3, 3],
            7: [3, 3],
            8: [3, 3, 2, 2, 2, 2, 2, 2]
        },
        5: {
            1: [3, 3, 2, 2, 2, 2, 2, 2]
        }
    }
    return _dic_keys[type_id][specification_id][insert_id - 1]


def get_mate_unmate_factor(n_cycles: float) -> float:
    """Retrieve the mating/unmating factor (piK).

    :param n_cycles: the average number of mate/unmate cycles expected
        per hour of operation.
    :return: _pi_k; the mate_unmate_factor.
    :rtype: float
    """
    if n_cycles <= 0.05:
        _pi_k = PI_K[0]
    elif 0.05 < n_cycles <= 0.5:
        _pi_k = PI_K[1]
    elif 0.5 < n_cycles <= 5.0:
        _pi_k = PI_K[2]
    elif 5.0 < n_cycles <= 50.0:
        _pi_k = PI_K[3]
    else:
        _pi_k = PI_K[4]

    return _pi_k


def get_part_count_lambda_b(**kwargs: Dict[str, int]) -> float:
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

    :param id_keys: the ID's used as keys when selecting
        the base hazard rate.  The keys are subcategory_id,
        environment_active_id, and type_id.
    :return: _base_hr; the parts count base hazard rate.
    :rtype: float
    :raise: KeyError if passed an unknown subcategory ID or type ID.
    :raise: IndexError if passed an unknown active environment ID.
    """
    _subcategory_id = kwargs.get('subcategory_id', 0)
    _type_id = kwargs.get('type_id', 0)
    _environment_active_id = kwargs.get('environment_active_id', 0)

    if _subcategory_id in [1, 5]:
        _base_hr = PART_COUNT_LAMBDA_B[_subcategory_id][_type_id][
            _environment_active_id - 1]
    else:
        _base_hr = PART_COUNT_LAMBDA_B[_subcategory_id][_environment_active_id
                                                        - 1]

    return _base_hr
