# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Switch.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Switch Reliability Calculations Module."""

# Standard Library Imports
from math import exp
from typing import Any, Dict

PART_COUNT_LAMBDA_B = {
    1: [
        0.0010, 0.0030, 0.018, 0.0080, 0.029, 0.010, 0.018, 0.013, 0.022,
        0.046, 0.0005, 0.025, 0.067, 1.2
    ],
    2: [
        0.15, 0.44, 2.7, 1.2, 4.3, 1.5, 2.7, 1.9, 3.3, 6.8, 0.74, 3.7, 9.9,
        180.0
    ],
    3: [
        0.33, 0.99, 5.9, 2.6, 9.5, 3.3, 5.9, 4.3, 7.2, 15.0, 0.16, 8.2, 22.0,
        390.0
    ],
    4: [
        0.56, 1.7, 10.0, 4.5, 16.0, 5.6, 10.0, 7.3, 12.0, 26.0, 0.26, 14.0,
        38.0, 670.0
    ],
    5: {
        1: [
            0.11, 0.23, 1.7, 0.91, 3.1, 0.8, 1.0, 1.3, 1.4, 5.2, 0.057, 2.8,
            7.5, 0.0
        ],
        2: [
            0.060, 0.12, 0.90, 0.48, 1.6, 0.42, 0.54, 0.66, 0.72, 2.8, 0.030,
            1.5, 4.0, 0.0
        ]
    }
}
PART_COUNT_PI_Q = {
    1: [1.0, 20.0],
    2: [1.0, 20.0],
    3: [1.0, 50.0],
    4: [1.0, 10.0],
    5: [1.0, 8.4]
}
PART_STRESS_LAMBDA_B = {
    1: {
        1: [0.00045, 0.034],
        2: [0.0027, 0.04]
    },
    5: [0.02, 0.038, 0.038]
}
PART_STRESS_PI_Q = {5: [1.0, 8.4]}
PI_C = {
    1: [1.0, 1.5, 1.7, 2.0, 2.5, 3.0, 4.2, 5.5, 8.0],
    5: [1.0, 2.0, 3.0, 4.0]
}
PI_E = {
    1: [
        1.0, 3.0, 18.0, 8.0, 29.0, 10.0, 18.0, 13.0, 22.0, 46.0, 0.5, 25.0,
        67.0, 1200.0
    ],
    2: [
        1.0, 3.0, 18.0, 8.0, 29.0, 10.0, 18.0, 13.0, 22.0, 46.0, 0.5, 25.0,
        67.0, 1200.0
    ],
    3: [
        1.0, 3.0, 18.0, 8.0, 29.0, 10.0, 18.0, 13.0, 22.0, 46.0, 0.5, 25.0,
        67.0, 1200.0
    ],
    4: [
        1.0, 3.0, 18.0, 8.0, 29.0, 10.0, 18.0, 13.0, 22.0, 46.0, 0.5, 25.0,
        67.0, 1200.0
    ],
    5: [
        1.0, 2.0, 15.0, 8.0, 27.0, 7.0, 9.0, 11.0, 12.0, 46.0, 0.5, 25.0, 67.0,
        0.0
    ]
}


def calculate_load_stress_factor(application_id: int,
                                 current_ratio: float) -> float:
    """
    Calculate the load stress factor (piL).

    :param int application_id: the load application identifier of the switch.
    :param float current_ratio: the ratio of operating current to rated
        current.
    :return: _pi_l; the load stress factor.
    :rtype: float
    """
    _pi_l = 0.0
    if application_id == 1:  # Resistive
        _pi_l = exp((current_ratio / 0.8)**2.0)
    elif application_id == 2:  # Inductive
        _pi_l = exp((current_ratio / 0.4)**2.0)
    elif application_id == 3:  # Capacitive
        _pi_l = exp((current_ratio / 0.2)**2.0)

    return _pi_l


def calculate_part_count(**attributes: Dict[str, Any]) -> float:
    """
    Wrap get_part_count_lambda_b().

    This wrapper allows us to pass an attributes dict from a generic parts
    count function.

    :param dict attributes: the attributes for the connection being calculated.
    :return: _base_hr; the parts count base hazard rates.
    :rtype: float
    """
    return get_part_count_lambda_b(attributes['subcategory_id'],
                                   attributes['environment_active_id'],
                                   attributes['construction_id'])


def calculate_part_stress_lambda_b(subcategory_id: int, quality_id: int,
                                   construction_id: int, application_id: int,
                                   n_elements: int) -> float:
    """
    Calculate the part stress base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    stress method.

    :param int subcategory_id: the subcategory identifier.
    :param int quality_id: the quality level identifier.
    :param int construction_id: the construction type identifier.
    :param int application_id: the switch application identifier.
    :param int n_elements: the number of switch contacts.
    :return: _lambda_b; the calculated part stress base hazard rate.
    :rtype: float
    :raise: IndexError if passed an unknown quality ID or application ID.
    :raise: KeyError is passed an unknown construction ID.
    """
    _dic_factors = {
        2: [[0.1, 0.00045, 0.0009], [0.1, 0.23, 0.63]],
        3: [[0.0067, 0.00003, 0.00003], [0.1, 0.02, 0.06]],
        4: [[0.0067, 0.062], [0.086, 0.089]]
    }

    if subcategory_id == 1:
        _lambda_b = PART_STRESS_LAMBDA_B[1][construction_id][quality_id - 1]
    elif subcategory_id in [2, 3]:
        _lambda_bE = _dic_factors[subcategory_id][quality_id - 1][0]
        _lambda_bC = _dic_factors[subcategory_id][quality_id - 1][1]
        _lambda_b0 = _dic_factors[subcategory_id][quality_id - 1][2]
        if construction_id == 1:
            _lambda_b = (_lambda_bE + n_elements * _lambda_bC)
        else:
            _lambda_b = (_lambda_bE + n_elements * _lambda_b0)
    elif subcategory_id == 4:
        _lambda_b1 = _dic_factors[subcategory_id][quality_id - 1][0]
        _lambda_b2 = _dic_factors[subcategory_id][quality_id - 1][1]
        _lambda_b = (_lambda_b1 + n_elements * _lambda_b2)
    elif subcategory_id == 5:
        _lambda_b = PART_STRESS_LAMBDA_B[5][application_id - 1]
    else:
        _lambda_b = 0.0

    return _lambda_b


def calculate_part_stress(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate the part stress hazard rate for a switch.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: attributes; the keyword argument (hardware attribute)
        dictionary with updated values.
    :rtype: dict
    """
    attributes['lambda_b'] = calculate_part_stress_lambda_b(
        attributes['subcategory_id'], attributes['quality_id'],
        attributes['construction_id'], attributes['application_id'],
        attributes['n_elements'])
    attributes['piL'] = calculate_load_stress_factor(
        attributes['application_id'], attributes['current_ratio'])

    # Determine the contact form and quantity factor (piC).
    if attributes['subcategory_id'] in [1, 5]:
        attributes['piC'] = PI_C[attributes['subcategory_id']][
            attributes['contact_form_id'] - 1]

    # Determine the cycling factor (piCYC).
    if attributes['n_cycles'] <= 1:
        attributes['piCYC'] = 1.0
    else:
        attributes['piCYC'] = float(attributes['n_cycles'])

    # Determine the use factor (piU).
    attributes['piU'] = (10.0 if (attributes['application_id']) - (1) else 1.0)

    attributes['hazard_rate_active'] = (attributes['lambda_b'] *
                                        attributes['piE'])
    if attributes['subcategory_id'] == 1:
        attributes['hazard_rate_active'] = (attributes['hazard_rate_active'] *
                                            attributes['piCYC'] *
                                            attributes['piL'] *
                                            attributes['piC'])
    elif attributes['subcategory_id'] in [2, 3, 4]:
        attributes['hazard_rate_active'] = (attributes['hazard_rate_active'] *
                                            attributes['piCYC'] *
                                            attributes['piL'])
    elif attributes['subcategory_id'] == 5:
        attributes['hazard_rate_active'] = (attributes['hazard_rate_active'] *
                                            attributes['piC'] *
                                            attributes['piU'] *
                                            attributes['piQ'])

    return attributes


def get_part_count_lambda_b(subcategory_id: int, environment_active_id: int,
                            construction_id: int) -> float:
    r"""
    Retrieve the parts count base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.  The dictionary PART_COUNT_217F_LAMBDA_B contains the
    MIL-HDBK-217F parts count base hazard rates.  Keys are for
    PART_COUNT_217F_LAMBDA_B are:

        #. subcategory_id
        #. environment_active_id
        #. construction_id; if the switch subcategory is NOT construction
            dependent, then the second key will be zero.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory \  |             Switch \          | MIL-HDBK-217F \ |
    |       ID       |              Style            |    Section      |
    +================+===============================+=================+
    |        1       | Toggle or Pushbutton          |       15.1      |
    +----------------+-------------------------------+-----------------+
    |        2       | Sensitive                     |       15.2      |
    +----------------+-------------------------------+-----------------+
    |        3       | Rotary                        |       15.3      |
    +----------------+-------------------------------+-----------------+
    |        4       | Thumbwheel                    |       16.1      |
    +----------------+-------------------------------+-----------------+
    |        5       | Circuit Breaker               |       17.1      |
    +----------------+-------------------------------+-----------------+

    :param int subcategory_id: the subcategory identifier.
    :param int environment_active_id: the active environment identifier.
    :param int construction_id: the construction identifier.
    :return: _base_hr; the parts count base hazard rate.
    :rtype: float
    :raise: IndexError if passed an unknown active environment ID.
    :raise: KeyError if passed an unknown subcategory ID or construction ID.
    """
    if subcategory_id == 5:
        _base_hr = PART_COUNT_LAMBDA_B[subcategory_id][construction_id][
            environment_active_id - 1]
    else:
        _base_hr = PART_COUNT_LAMBDA_B[subcategory_id][environment_active_id -
                                                       1]

    return _base_hr
