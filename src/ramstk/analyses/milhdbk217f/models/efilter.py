# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Filter.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Filter MIL-HDBK-217F Constants and Calculations Module."""

# Standard Library Imports
from typing import Any, Dict

PART_COUNT_LAMBDA_B = {
    1: [
        0.022, 0.044, 0.13, 0.088, 0.20, 0.15, 0.20, 0.24, 0.29, 0.24, 0.018,
        0.15, 0.33, 2.6
    ],
    2: [
        0.12, 0.24, 0.72, 0.48, 1.1, 0.84, 1.1, 1.3, 1.6, 1.3, 0.096, 0.84,
        1.8, 1.4
    ],
    3:
    [0.27, 0.54, 1.6, 1.1, 2.4, 1.9, 2.4, 3.0, 3.5, 3.0, 0.22, 1.9, 4.1, 32.0]
}
PART_STRESS_LAMBDA_B = {1: 0.022, 2: 0.12, 3: 0.12, 4: 0.27}
PI_E = [
    1.0, 2.0, 6.0, 4.0, 9.0, 7.0, 9.0, 11.0, 13.0, 11.0, 0.8, 7.0, 15.0, 120.0
]
PI_Q = [1.0, 2.9]


def calculate_part_count(**attributes: Dict[str, int]) -> float:
    """Wrap get_part_count_lambda_b().

    This wrapper allows us to pass an attributes dict from a generic parts
    count function.

    :param attributes: the attributes for the filter being calculated.
    :return: _base_hr; the parts count base hazard rate.
    :rtype: float
    """
    return get_part_count_lambda_b(
        attributes['type_id'],  # type: ignore
        attributes['environment_active_id'])  # type: ignore


def calculate_part_stress(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the part stress active hazard rate for a filter.

    :param attributes: the attributes for the filter being calculated.
    :return: attributes; the keyword argument (hardware attribute)
             dictionary with updated values.
    :rtype: dict
    :raise: KeyError if an unknown type ID is passed.
    """
    attributes['lambda_b'] = PART_STRESS_LAMBDA_B[  # type: ignore
        attributes['type_id']]  # type: ignore

    attributes['hazard_rate_active'] = (
        attributes['lambda_b']  # type: ignore
        * attributes['piQ'] * attributes['piE'])

    return attributes


def get_part_count_lambda_b(type_id: int, environment_active_id: int) -> float:
    """Retrievee the part count base hazard rate for a filter.

    :param type_id: the filter type identifer.
    :param environment_active_id: the active environment identifier.
    :return: _base_hr; the part count base hazard rate for the active
        environment.
    :rtype: float
    :raise: IndexError if an unknown active environment ID is passed.
    :raise: KeyError if an unknown type ID is passed.
    """
    return PART_COUNT_LAMBDA_B[type_id][environment_active_id - 1]
